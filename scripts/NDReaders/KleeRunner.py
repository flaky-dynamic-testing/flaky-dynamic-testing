from AbstractReader import AbstractReader, T
import os 
import difflib

class KleeRunner(AbstractReader):
    def __init__(self, repo_user, repo_name, output_dir, token):
        self.output_dir = output_dir
        self.repo_user = repo_user
        self.repo_name = repo_name
        self.results = {}
        self.token = token 
        self.import_file(self.output_dir, self.repo_name, "Run Klee", "KLEE: output directory ", self.token)
    
    def nondeterminism_analysis(self): 
        output_dir = os.path.expanduser(self.output_dir)
        repo_folder = os.path.join(output_dir, self.repo_name)
        nondeterminism = False
        all_nd_results = []

        try:
            os.makedirs(repo_folder, exist_ok=True)
            # Iterate through all job folders in repo_folder
            for job_folder in os.listdir(repo_folder):
                job_folder_path = os.path.join(repo_folder, job_folder)

                # Skip non-directory entries
                if not os.path.isdir(job_folder_path):
                    continue
                
                file_names = sorted(os.listdir(job_folder_path))
                for i in range(len(file_names) - 1):
                    file_path1 = os.path.join(job_folder_path, file_names[i])
                    file_path2 = os.path.join(job_folder_path, file_names[i + 1])

                    if os.path.isfile(file_path1) and os.path.isfile(file_path2):
                        differences = []
                        with open(file_path1, 'r', encoding='utf-8') as file1, open(file_path2, 'r', encoding='utf-8') as file2:
                            lines1 = file1.readlines()
                            lines2 = file2.readlines()

                            differ = difflib.Differ()
                            diff = list(differ.compare(lines1, lines2))

                            for j, line in enumerate(diff):
                                # Check for differences (lines starting with '-' or '+')
                                if line.startswith('-'):
                                    differences.append(f"File #1: {os.path.basename(file_path1).replace('.txt', '')} -----> Line {j+1}: {line.strip()}")
                                elif line.startswith('+'):
                                    differences.append(f"File #2: {os.path.basename(file_path2).replace('.txt', '')} -----> Line {j+1}: {line.strip()}")

                        if differences:
                            nondeterminism = True
                            print("Found nondeterminism! (check below for the differences found)")
                            print(f"Filename #1: {file_path1} <-------> Filename #2: {file_path2}")
                            for diff in differences:
                                print(diff)
                            print("\n\n\n")

                            all_nd_results.append(differences)
                    
        except OSError as e:
            print(f"Error creating or accessing directory {repo_folder}: {e}")
        
        except Exception as e:
            print(f"Error: {e}")

        if (not nondeterminism):
            print("No nondeterminism detected!")
            return "None reported"
        else:
            return all_nd_results
