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