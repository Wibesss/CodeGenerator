from colorama import Fore, Style, init
from github import Github, GithubException
import time
from datetime import datetime, timezone, timedelta
import os
import requests

init(autoreset=True)

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=1)

with open("token.txt", "r") as file:
    ACCESS_TOKEN = file.read().strip()

g = Github(ACCESS_TOKEN)

def download_python_files(repo, path, save_dir):
    contents = repo.get_contents(path)
    for content_file in contents:
        if content_file.type == "dir":
            
            if any(lib_dir in content_file.path.lower() for lib_dir in [
                "site-packages", "venv", "env", "node_modules", "dist", "build", "tests", "test", "specs", "e2e"
            ]):
                continue
            
            download_python_files(repo, content_file.path, save_dir)
            
        elif content_file.name.endswith(".py"):
            download_url = content_file.download_url
            file_path = os.path.join(save_dir, content_file.path)
            try:
                response = requests.head(download_url)
                response.raise_for_status()
                
                file_size_bytes = response.headers.get('Content-Length')
                
                if file_size_bytes:
                    file_size_bytes = int(file_size_bytes)
                    
                    if file_size_bytes == 0:
                        print(Fore.YELLOW + f"Skipping empty file: {content_file.path}")
                        continue
                    
                    file_size_kb = file_size_bytes / 1024
                    file_size_kb_str = f"{file_size_kb:.2f} KB"
                else:
                    file_size_kb_str = 'Unknown size'
                
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                print(Fore.BLUE + f"Downloading {content_file.path}", end='')
                
                response = requests.get(download_url, stream=True)
                response.raise_for_status()
                
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                
                print(Fore.GREEN + f" (Size: {file_size_kb_str})")
                
            except requests.RequestException as e:
                print(Fore.RED + f" Error downloading file: {e}")


def process_repository(repository):
    owner_login = repository.owner.login
    repo_name = repository.name
    repo_dir = f"repos/{owner_login}/{repo_name}"
    os.makedirs(repo_dir, exist_ok=True)
    print(Fore.GREEN + f"Processing repository: {repo_name}")
    try:
        download_python_files(repository, "", repo_dir)
        print(Fore.CYAN + Style.BRIGHT + f"Finished processing repository: {repo_name}")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Failed to process {repo_name}: {e}")

for i in range(3):
    start_time_str = start_time.strftime('%Y-%m-%d')
    end_time_str = end_time.strftime('%Y-%m-%d')
    query = f"language:python created:{start_time_str}..{end_time_str}"
    
    print(Fore.YELLOW + f"Searching for repositories created between {start_time_str} and {end_time_str}")
    
    try:
        result = g.search_repositories(query)
        print(Fore.YELLOW + f"Total repositories found: {result.totalCount}")

        for repository in result:
            process_repository(repository)
            print(Fore.CYAN + Style.BRIGHT + f"Current start time: {start_time_str}")
        
        print(Fore.GREEN + Style.BRIGHT + f"Finished processing for start time: {start_time_str}")

    except GithubException as e:
        print(Fore.RED + Style.BRIGHT + f"Error: {e}")
        print(Fore.RED + Style.BRIGHT + "Waiting for 2 minutes due to API limit...")
        time.sleep(120)

    end_time -= timedelta(days=1)
    start_time -= timedelta(days=1)
