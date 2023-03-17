import os
import random
import datetime
from github import Github
import config

def get_file_urls(folder_path=""):
    # Create a Github instance using the access token
    g = Github(config.ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(config.REPO_NAME)

    # Base URL for raw file access
    base_url = 'https://raw.githubusercontent.com'

    # Get a list of all files in the repository
    files = []
    contents = repo.get_contents(folder_path)
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            files.append(file_content)

    # Create a folder-specific log file
    log_file_name = os.path.basename(folder_path) + '_file_log.txt'
    log_file_path = os.path.join(folder_path, log_file_name)

    # Filter out file URLs that have already been returned
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            log_urls = f.read().splitlines()
        files = [file for file in files if f"{base_url}/{config.REPO_NAME}/main/{file.path}" not in log_urls]

    # Generate a random file URL from the remaining file URLs
    if files:
        file = random.choice(files)
        file_url = f"{base_url}/{config.REPO_NAME}/main/{file.path}"

        # Write the selected file URL and the date and time to the log file
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file_path, 'a') as f:
            f.write(f"{file_url}\t{now}\n")

        return file_url
    else:
        return None