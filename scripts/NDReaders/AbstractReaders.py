#  Nondeterminism Dynamic Analysis Python Abstract Class
#
#  Copyright (c) 2024.
#
#  This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from typing import TypeVar, Iterable
import os
import requests
import re 

T = TypeVar('T')

class AbstractReader(ABC):
    def import_file(self, output_dir, repo_name, action_name, start_phrase, apitoken):
        output_dir = os.path.expanduser(output_dir)
        repo_folder = os.path.join(output_dir, repo_name)
        os.makedirs(repo_folder, exist_ok=True)

        self.download_artifacts(self.repo_user, self.repo_name, repo_folder, action_name, apitoken)
        
        for job_folder in os.listdir(repo_folder):
            job_folder_path = os.path.join(repo_folder, job_folder)

            if not os.path.isdir(job_folder_path):
                continue

            for filename in os.listdir(job_folder_path):
                if filename.endswith(".txt"): 
                    log_filename = os.path.join(job_folder_path, filename)

                    try:
                        with open(log_filename, 'r') as file:
                            lines = file.readlines()

                        iso_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?'
                        def remove_timestamp(line):
                            return re.sub(iso_pattern, '', line).lstrip()

                        modified_lines = [remove_timestamp(line) for line in lines]

                        with open(log_filename, 'w') as f:
                            f.writelines(modified_lines)

                        start_pattern = rf"{start_phrase}.*"
                        end_pattern = r"Post job cleanup\."

                        with open(log_filename, 'r') as file:
                            input_text = file.read()

                        start_match = re.search(start_pattern, input_text)
                        end_match = re.search(end_pattern, input_text)

                        if start_match and end_match:
                            start_index = start_match.start()
                            end_index = end_match.start()

                            extracted_text = input_text[start_index:end_index]

                            with open(log_filename, 'w') as file: 
                                file.write(extracted_text.strip())
                        else:
                            print("Failed to cleanup log! Skipping....")
                            continue
                                                
                    except FileNotFoundError:
                        print(f"Invalid location! File {log_filename} not found.")

    def download_artifacts(self, repo_owner, repo_name, output_dir,  workflow_name, pat_token):
        excluded_branches = ['main', 'master', '1.8', '3.2', '4.1', '2.x', '2023.x', '3.x', 'dev', 'devel', 'develop', 'release-v2', 'trunk', 'uinverse', 'v5-master', 'next', 'v1.x']
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {pat_token}"
        }

        branches_response = requests.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches",
            headers=headers
        )
        branches_response.raise_for_status()
        branches = [branch['name'] for branch in branches_response.json() if branch['name'] not in excluded_branches]

        for branch in branches:
            runs_response = requests.get(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs",
                params={"branch": branch},
                headers=headers
            )
            runs_response.raise_for_status()
            runs = runs_response.json()['workflow_runs']
            filtered_runs = [run for run in runs if run['name'] == workflow_name]

            for run in filtered_runs:
                jobs_response = requests.get(
                    f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{run['id']}/jobs",
                    headers=headers
                )
                jobs_response.raise_for_status()
                jobs = jobs_response.json()['jobs']

                for job in jobs:
                    job_folder = os.path.join(output_dir, f"job_{job['name']}")
                    os.makedirs(job_folder, exist_ok=True) 

                    job_logs_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/jobs/{job['id']}/logs"
                    job_logs_filename = os.path.join(job_folder, f"{branch}.txt")
                    response = requests.get(
                        job_logs_url,
                        headers=headers
                    )
                    response.raise_for_status()
                    with open(job_logs_filename, 'wb') as f:
                        f.write(response.content)
