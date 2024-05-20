# This script creates a csv file named `data/checked_projects.csv` with the following columns, and also populate the csv file with with the tool and the project names so that the researchers can run the tool on the project locally and record the finding in the csv file:
# steps_to_reproduce_file,tool,project,can_run_locally,has_nondeterminism,remarks

# usage: python create_checked_pojects_dataset.py
# output: data/checked_projects.csv


# Additional comments:
# The script requires java and rust projects that are extracted earlier. Both csv have the same headers: Name,Link,Default Branch,SHA,Stargazers Count,Forks Count,Date
# The script also requires the tools_path csv file that has the following headers: `Language,Name,Link to the tool,Last update`


# imports
import pandas


# projects
java_projects_path = "/Users/talank/research/flaky-dynamic-testing/data/popular_repos/repositories_java.csv"
rust_projects_path = "/Users/talank/research/flaky-dynamic-testing/data/popular_repos/repositories_rust.csv"
tools_path = "/Users/talank/research/flaky-dynamic-testing/data/dynamic_tools/Programming Languages.csv"

df = pandas.DataFrame(columns=['ID', 'steps_to_reproduce_file', 'language', 'tool', 'tool_link', 'project', 'project_link', 'project_default_branch', 'project_sha', 'can_run_locally', 'has_nondeterminism', 'steps_to_reproduce', 'remarks'])

java_df = pandas.read_csv(java_projects_path)
rust_df = pandas.read_csv(rust_projects_path)

tools_df = pandas.read_csv(tools_path)
tools_df_java = tools_df[tools_df['Language'] == 'Java']
tools_df_rust = tools_df[tools_df['Language'] == 'Rust']

id = 1

for i, r in tools_df_java.iterrows():
    for index, row in java_df.iterrows():
        steps_to_reproduce_file_name = r['Name'] + "_" + row['Name'] + ".md"
        steps_to_reproduce_file_name = steps_to_reproduce_file_name.replace(" ", "_")
        steps_to_reproduce_file_name = steps_to_reproduce_file_name.replace("/", "_")
        tool_link = r['Link to the tool']
        project_link = row['Link']
        default_branch = row['Default Branch']
        sha = row['SHA']
        
        df = df._append({'ID':id, 'steps_to_reproduce_file': steps_to_reproduce_file_name, 'language':'Java', 'tool': r['Name'], 'tool_link': r['Link to the tool'], 'project': row['Name'], 'project_link': row['Link'], 'project_default_branch':default_branch , 'project_sha':sha ,'can_run_locally': '', 'has_nondeterminism': '', 'steps_to_reproduce':'', 'remarks': ''}, ignore_index=True)
        
        id += 1
        
for i, r in tools_df_rust.iterrows():
    for index, row in rust_df.iterrows():
        steps_to_reproduce_file_name = r['Name'] + "_" + row['Name'] + ".md"
        steps_to_reproduce_file_name = steps_to_reproduce_file_name.replace(" ", "_")
        steps_to_reproduce_file_name = steps_to_reproduce_file_name.replace("/", "_")
        tool_link = r['Link to the tool']
        project_link = row['Link']
        default_branch = row['Default Branch']
        sha = row['SHA']
        
        df = df._append({'ID':id, 'steps_to_reproduce_file': steps_to_reproduce_file_name, 'language':'Rust', 'tool': r['Name'], 'tool_link': r['Link to the tool'], 'project': row['Name'], 'project_link': row['Link'], 'project_default_branch':default_branch , 'project_sha':sha ,'can_run_locally': '', 'has_nondeterminism': '', 'steps_to_reproduce':'', 'remarks': ''}, ignore_index=True)

        
        id += 1
        
# save the dataframe to a csv file
df.to_csv("../data/checked_projects.csv", index=False)
        