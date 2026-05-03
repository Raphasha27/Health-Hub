import os
import requests
import argparse

# ---------------------------------------------------------
# GitHub Health Hub - Unblocker Script
# This script removes branch protection rules from your 
# repositories so that no bots, CI checks, or reviews 
# are ever required before you merge or push changes.
# ---------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def remove_branch_protection(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/protection"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"[SUCCESS] Removed branch protection for {repo} on branch '{branch}'. You are now fully unblocked!")
    elif response.status_code == 404:
        print(f"[INFO] No branch protection found for {repo} on branch '{branch}'.")
    else:
        print(f"[ERROR] Failed to remove protection for {repo}: {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Remove all merge/review blocks from repos.")
    parser.add_argument("--username", required=True, help="Your GitHub username")
    args = parser.parse_args()
    
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable is not set.")
        return

    print(f"Removing merge blocks and required reviews for user: {args.username}")
    repos = get_repositories(args.username)
    
    for repo in repos:
        if repo.get("archived") or repo.get("disabled"):
            continue
        
        default_branch = repo.get("default_branch", "main")
        print(f"\nChecking {repo['name']}...")
        remove_branch_protection(args.username, repo["name"], default_branch)

if __name__ == "__main__":
    main()
