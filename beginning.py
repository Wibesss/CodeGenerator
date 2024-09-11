from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, blue, cyan
from github import Github
import time
from datetime import datetime, timezone
import os

end_time = time.time()
start_time = end_time - 86400

with open("token.txt", "r") as file:
    ACCESS_TOKEN = file.read().strip()
    
g = Github(ACCESS_TOKEN)


for i in range(3):
    start_time_str = datetime.fromtimestamp(start_time, tz=timezone.utc).strftime('%Y-%m-%d')
    end_time_str = datetime.fromtimestamp(end_time, tz=timezone.utc).strftime('%Y-%m-%d')
    query = f"language:python created:{start_time_str}..{end_time_str}"
    print(query)
    end_time -= 86400
    start_time -= 86400
    
    try:
        result = g.search_repositories(query)
        print(yellow(f"Total repositories found: {result.totalCount}"))
        
        for repository in result:
            clone_url = repository.clone_url
            owner_login = repository.owner.login
            repo_name = repository.name

            # Create a directory for the owner if it doesn't exist
            repo_dir = f"repos/{owner_login}/{repo_name}"
            os.makedirs(repo_dir, exist_ok=True)

            print(blue(f"Cloning into: {repo_dir}"))
            os.system(f"git clone {clone_url} {repo_dir}")
            print(cyan(bold(f"Current start time {start_time}")))

    except Exception as e:
        print(red(bold(f"Error: {e}")))
        print(red(bold(f"Broke for some reason ...")))
        time.sleep(120)
        
        