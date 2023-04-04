import os
import random
import datetime
from github import Github
import config

def get_file_urls():
    # Create a Github instance using the access token
    g = Github(config.ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(config.REPO_NAME)

    # Base URL for raw file access
    base_url = 'https://raw.githubusercontent.com'

    # Get a list of all files in the repository with .png, .jpg, or .jpeg extensions
    files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file_ext = os.path.splitext(file_content.name)[1]
            if file_ext in ['.png', '.jpg', '.jpeg']:
                files.append(file_content)

    # Filter out file URLs that have already been returned
    filtered_files = []
    for file in files:
        folder_path = os.path.dirname(file.path)
        log_file_name = os.path.basename(folder_path) + '_file_log.txt'
        log_file_path = os.path.join(folder_path, log_file_name)

        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                log_lines = f.read().splitlines()
            log_urls = [line.split('\t')[0] for line in log_lines]
            file_url = f"{base_url}/{config.REPO_NAME}/main/{file.path}"
            if file_url not in log_urls:
                filtered_files.append(file)

    # Generate a random file URL from the remaining file URLs
    if filtered_files:
        file = random.choice(filtered_files)
        file_url = f"{base_url}/{config.REPO_NAME}/main/{file.path}"

        # Get the folder path and log file path
        folder_path = os.path.dirname(file.path)
        folder_name = os.path.basename(folder_path)
        log_file_name = folder_name + '_file_log.txt'
        log_file_path = os.path.join(folder_path, log_file_name)

        # Write the selected file URL and the date and time to the log file
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file_path, 'a') as f:
            f.write(f"{file_url}\t{now}\n")

        return file_url, folder_name
    else:
        return None, None