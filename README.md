# GitHub Follower Analysis

GitHub Follower Analysis is a command-line tool that allows users to gather information about the followers and followings of a GitHub user. The tool utilizes the GitHub API to retrieve data, which is then stored in a SQLite database for further analysis. Additionally, it has the capability to download profile pictures of the GitHub users.

## Requirements

- `requests` library
- `PyGithub` library

You can install the required libraries using the following command:

```bash
pip install requests PyGithub
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ALIILAPRO/GitHub-Account-Analyzer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd GitHub-Account-Analyzer
   ```

3. Open the script and enter your GitHub Personal Access Token in the access_token variable.

4. Run python file:
   ```bash
   python gitlyzer.py
   ```

## License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](https://github.com/ALIILAPRO/GitHub-Account-Analyzer/blob/main/LICENSE) file for details.