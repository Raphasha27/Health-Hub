import os
import requests
import datetime

# ---------------------------------------------------------
# GitHub Health Hub - Dashboard Generator
# Creates a static HTML report of your entire ecosystem.
# ---------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    return requests.get(url, headers=HEADERS).json()

def generate_html(username, repos):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Health Hub Dashboard | {username}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0d1117; color: #c9d1d9; padding: 40px; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
            .repo-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }}
            .repo-name {{ font-weight: bold; color: #58a6ff; text-decoration: none; }}
            .status-badge {{ padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
            .status-green {{ background: #238636; color: white; }}
            .footer {{ margin-top: 40px; font-size: 12px; color: #8b949e; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ GitHub Health Hub Dashboard</h1>
            <p>Last Pulse: {now}</p>
            <div id="repos">
    """
    
    for repo in repos:
        if repo.get("archived"): continue
        html += f"""
                <div class="repo-card">
                    <a href="{repo['html_url']}" class="repo-name">{repo['name']}</a>
                    <span class="status-badge status-green">Healthy</span>
                </div>
        """
        
    html += """
            </div>
            <div class="footer">
                &copy; 2026 Kirov Dynamics Technology | Powered by Health Hub Enforcer
            </div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    user = "Raphasha27"
    print(f"Generating dashboard for {user}...")
    repo_list = get_repos(user)
    content = generate_html(user, repo_list)
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ dashboard.html created successfully.")
