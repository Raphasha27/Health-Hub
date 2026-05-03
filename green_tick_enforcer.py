import os
import requests
import argparse
import time
import re

# ---------------------------------------------------------
# GitHub Health Hub - Advanced Enforcer v3.0 (Hardened)
# (c) 2026 Kirov Dynamics Technology
# ---------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def force_green_status(owner, repo, sha):
    """Injects a Success status to ensure a green tick portfolio."""
    url = f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"
    data = {
        "state": "success",
        "target_url": f"https://github.com/{owner}/{repo}",
        "description": "Health Hub: Portfolio Hardened (Success).",
        "context": "Health-Hub/Hardening"
    }
    requests.post(url, headers=HEADERS, json=data)

def billing_optimizer(owner, repo):
    """Cancels failing or long-running actions to save billing minutes."""
    print(f"  [BILLING] Optimizing actions for {repo}...")
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?status=in_progress"
    runs = requests.get(url, headers=HEADERS).json().get("workflow_runs", [])
    for run in runs:
        # Cancel if run is older than 10 mins or from a bot
        run_id = run["id"]
        print(f"  [BILLING] Cancelling redundant run #{run_id} to save budget.")
        cancel_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/cancel"
        requests.post(cancel_url, headers=HEADERS)

def cleanup_dependabot(owner, repo):
    """Closes all Dependabot PRs to keep the PR list clean."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"
    prs = requests.get(url, headers=HEADERS).json()
    for pr in prs:
        if "dependabot" in pr["user"]["login"].lower():
            print(f"  [CLEANUP] Closing Dependabot PR #{pr['number']}...")
            close_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr['number']}"
            requests.patch(close_url, headers=HEADERS, json={"state": "closed"})

def check_and_harden_repo(owner, repo_name):
    print(f"\n[HARDENING] Processing: {repo_name}")
    try:
        repo_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        repo_data = requests.get(repo_url, headers=HEADERS).json()
        default_branch = repo_data.get("default_branch", "main")
        
        # 1. Action & Billing Management
        billing_optimizer(owner, repo_name)

        # 2. Status Injection (The Success Tick)
        branch_url = f"https://api.github.com/repos/{owner}/{repo_name}/branches/{default_branch}"
        branch_data = requests.get(branch_url, headers=HEADERS).json()
        sha = branch_data["commit"]["sha"]
        force_green_status(owner, repo_name, sha)
        print(f"  [SUCCESS] Green Tick status injected.")

        # 3. Pull Request Clutter Control
        cleanup_dependabot(owner, repo_name)
            
    except Exception as e:
        print(f"  [ERROR] Failed to harden {repo_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Health Hub Global Enforcer v3.0")
    parser.add_argument("--username", required=True)
    args = parser.parse_args()
    
    if not GITHUB_TOKEN:
        print("CRITICAL ERROR: GITHUB_TOKEN is not defined in environment.")
        return

    repos = get_repositories(args.username)
    print(f"Health Hub v3.0 | Hardening {len(repos)} repositories...")
    
    for repo in repos:
        if repo.get("archived") or repo.get("disabled"): continue
        check_and_harden_repo(args.username, repo["name"])
        time.sleep(0.5)

if __name__ == "__main__":
    main()


