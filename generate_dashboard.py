import os
import requests
from datetime import datetime

# ---------------------------------------------------------
# Health Hub v4.0 Global Dashboard Generator
# (c) 2026 Kirov Dynamics Technology
# ---------------------------------------------------------

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    res = requests.get(url, headers=HEADERS)
    return res.json()

def get_repo_status(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{branch}/status"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    return {}

def generate_dashboard(username):
    repos = get_repos(username)
    repo_stats = []
    
    print(f"Generating dashboard for {username}...")
    for repo in repos:
        if repo["archived"]: continue
        name = repo["name"]
        branch = repo.get("default_branch", "main")
        status_data = get_repo_status(username, name, branch)
        
        state = status_data.get("state", "unknown")
        total_count = status_data.get("total_count", 0)
        
        # Check for Health Hub specific hardening
        is_hardened = False
        statuses = status_data.get("statuses", [])
        for s in statuses:
            if "Health-Hub" in s.get("context", ""):
                is_hardened = True
                break
        
        repo_stats.append({
            "name": name,
            "state": state,
            "is_hardened": is_hardened,
            "url": repo["html_url"],
            "description": repo["description"] or "No description provided."
        })

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Hub | Global Portfolio Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #020617; color: #f8fafc; }}
        .glass {{ background: rgba(30, 41, 59, 0.5); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); }}
        .status-success {{ color: #4ade80; text-shadow: 0 0 10px rgba(74, 222, 128, 0.3); }}
        .status-hardened {{ background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); }}
        .glow {{ box-shadow: 0 0 20px rgba(59, 130, 246, 0.1); }}
    </style>
</head>
<body class="p-8">
    <div class="max-w-6xl mx-auto">
        <header class="flex justify-between items-end mb-12">
            <div>
                <h1 class="text-4xl font-extrabold tracking-tighter mb-2 italic">HEALTH HUB <span class="text-blue-500">v4.0</span></h1>
                <p class="text-slate-400 font-medium uppercase tracking-widest text-xs">Autonomous Portfolio Hardening Dashboard</p>
            </div>
            <div class="text-right">
                <div class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Last Pulse Sync</div>
                <div class="text-sm font-mono text-blue-400">{timestamp}</div>
            </div>
        </header>

        <div class="grid md:grid-cols-3 gap-6 mb-12">
            <div class="glass p-6 rounded-3xl glow">
                <div class="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Total Repositories</div>
                <div class="text-4xl font-black">{len(repo_stats)}</div>
            </div>
            <div class="glass p-6 rounded-3xl glow">
                <div class="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Success Ticks</div>
                <div class="text-4xl font-black text-green-400">{len([r for r in repo_stats if r['state'] == 'success'])}</div>
            </div>
            <div class="glass p-6 rounded-3xl glow border-blue-500/20">
                <div class="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Hardening Status</div>
                <div class="text-4xl font-black text-blue-400">NOMINAL</div>
            </div>
        </div>

        <div class="grid md:grid-cols-2 gap-4">
            {" ".join([f'''
            <a href="{r['url']}" target="_blank" class="glass p-6 rounded-2xl hover:bg-slate-800/50 transition group relative overflow-hidden">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-lg font-bold tracking-tight group-hover:text-blue-400 transition">{r['name']}</h3>
                    <span class="px-2 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter { 'bg-green-500/10 text-green-400' if r['state'] == 'success' else 'bg-red-500/10 text-red-400' }">
                        {r['state']}
                    </span>
                </div>
                <p class="text-sm text-slate-400 mb-4 line-clamp-2">{r['description']}</p>
                <div class="flex items-center gap-2">
                    { '<span class="px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 text-[9px] font-bold uppercase tracking-widest border border-blue-500/20">Hardened</span>' if r['is_hardened'] else '' }
                </div>
            </a>
            ''' for r in repo_stats])}
        </div>

        <footer class="mt-20 pt-8 border-t border-slate-800 text-center">
            <p class="text-xs font-bold text-slate-600 uppercase tracking-[0.5em]">(c) 2026 Kirov Dynamics Infrastructure</p>
        </footer>
    </div>
</body>
</html>
    """
    
    with open("HEALTH_HUB_STATUS.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Dashboard generated: HEALTH_HUB_STATUS.html")

if __name__ == "__main__":
    generate_dashboard("Raphasha27")
