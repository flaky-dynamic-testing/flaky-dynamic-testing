# flaky-dynamic-testing
flaky-dynamic-testing

# Directory Structure

## data
The data directory contains the following subdirectories:
- `popular_repos`: Contains csv files for popular Java and Rust repositories.
- `dynamic_tools`: Contains csv files for dynamic analysis tools.

### Popular_repos
The directory `Popular_repos` contains csv files for popular Java and Rust repositories. The data was collected on 30/04/2024 16:36:59, so the popularity of the repositories may have changed since then.
The csv files contain the following columns:
<!-- Name,Link,Default Branch,SHA,Stargazers Count,Forks Count,Date -->
<!-- joaomlneto/travis-ci-tutorial-java,https://github.com/joaomlneto/travis-ci-tutorial-java,master,f35723e317bb63a403719d82f2b054458babf472,37,510,29/03/2024 13:46:44 -->
<!-- eg:  -->
- Name: The name of the repository (e.g., joaomlneto/travis-ci-tutorial-java)
- Link: The link to the repository (e.g., https://github.com/joaomlneto/travis-ci-tutorial-java)
- Default Branch: The default branch of the repository (e.g., master)
- SHA: The SHA of the repository (e.g., f35723e317bb63a403719d82f2b054458babf472)
- Stargazers Count: The number of stars the repository has (e.g., 37)
- Forks Count: The number of forks the repository has (e.g., 510)
- Date: The date and time when the data was collected (e.g., 29/03/2024 13:46:44)

### dynamic_tools
The directory `NDRunners` contains Python scripts that allow for easy management of extracting GitHub Action logs and nondeterminism analysis. This nondeterminism analysis functions based on the `difflib` library in Python. `difflib` is a python builtin library that computes deltas (in other words, file comparisons). File comparisons are made based on the same operating system the tools were run in across the 10 different branches made in each one. To run any of these tools, you must make sure you first have the AbstractReader.py class and then the desired Runner script. Here is an example for one of the dynamic analysis tools: 

*Note that you'll need to make sure you have enough API requests to be able to run all projects (if desired). You can check how many API requests you've made by calling the following command -->* `curl -H "Authorization: token <APItoken> " https://api.github.com/rate_limit`


```
if __name__ == '__main__':
  repo_usr = "<-- insert repository owner/organization -->"
  repos = [<-- list all repositories that contain "Run JPF" -->]
  output_dir = "<--insert the directory you want to store all runner logs-->"
  token = "<-- this can be a organization GitHub API token or a personal access token (choose classic)-->"

  for repo in repos:
    jpf = JPFReader(repo_usr, repo, output_dir, token)
    repo_nd_results = jpf.nondeterminism_analysis() // allows for manual dynamic analysis if needed
```

Supported Dynamic Analysis Tools (at the moment): 
1. JavaPathFinder (JPF)
2. CASR
3. VMware Chap
4. Klee
5. Google AddressSanitizer (also Google LeakSanitizer in certain projects)
6. Google MemorySanitizer
7. Google ThreadSanitizer
8. Valgrind
