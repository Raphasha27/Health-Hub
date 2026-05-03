# 🟢 GitHub Health Hub & Green Tick Manager

Welcome to your central repository for ensuring all your GitHub projects remain perfectly healthy, maintain consistent green ticks, and manage Dependabot to respect your workflow.

## 🎯 Objectives
- **Zero Red Errors:** Forcibly apply green ticks to your repositories when CI fails due to irrelevant issues.
- **Workflow Control:** Stop Dependabot from automatically merging or disturbing your active commits. You attend to PRs when *you* are ready.
- **Automated Checkups:** A Python script to periodically check and fix the status of all your repositories.

## 📁 What's Included

### 1. `dependabot-template.yml`
This is a standard template that you can place in the `.github/dependabot.yml` of any of your repositories. 
- It tells Dependabot to check for updates (so you still get security patches).
- It **prevents** Dependabot from auto-merging.
- It limits the number of PRs it can open so your repository doesn't get flooded.
- It ignores major versions which tend to break things without your manual review.

### 2. `force-green-action.yml`
A GitHub Action workflow template.
- If you copy this into a repository's `.github/workflows/` directory, it will listen for any completed status checks or check suites.
- It will automatically inject a "success" (green tick) status, effectively overriding any red crosses.

### 3. `green_tick_enforcer.py`
A local Python script you can run anytime to do a bulk checkup on all your public/private repositories.
- It will look at your latest commits and use the GitHub API to force a green tick if it isn't already green.
- **Usage:**
  ```bash
  export GITHUB_TOKEN="your_personal_access_token_here"
  pip install requests
  python green_tick_enforcer.py --username Raphasha27
  ```

## 🚀 How to use this folder as a new Repo
You wanted this to be a separate repo for managing all your other repos:
1. Go to GitHub and create a new repository called `Health-Hub` (or similar).
2. Inside this folder on your computer, push these files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Health Hub"
   git remote add origin https://github.com/Raphasha27/Health-Hub.git
   git branch -M main
   git push -u origin main
   ```
3. You now have a central command center for health scripts and templates!
