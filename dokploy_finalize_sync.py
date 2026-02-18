import requests
import json
import time
import subprocess

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
CORE_ID = "CbM3L2Z3LJemaumOC6Yd4"
POSTIZ_ID = "EYKt_rt5nqcBHTpD25633"
GITHUB_ID = "QZnupLM5a8IgYpTloLpdZ"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def finalize_sync():
    # 1. Update Core Service to use GitHub + Modular Path
    print("🛠️ Updating Core Stack to GitHub (Modular Path)...")
    call_trpc("compose.update", {
        "composeId": CORE_ID,
        "sourceType": "github",
        "githubId": GITHUB_ID,
        "repository": "Bizoholic-Digital/bizosaas-platform",
        "owner": "Bizoholic-Digital",
        "branch": "staging",
        "composePath": "./infrastructure/compose/docker-compose.core-stack.yml"
    })

    # 2. Update Postiz Service to use GitHub + Modular Path
    print("🛠️ Updating Postiz Stack to GitHub (Modular Path)...")
    call_trpc("compose.update", {
        "composeId": POSTIZ_ID,
        "sourceType": "github",
        "githubId": GITHUB_ID,
        "repository": "Bizoholic-Digital/bizosaas-platform",
        "owner": "Bizoholic-Digital",
        "branch": "staging",
        "composePath": "./docker-compose.postiz.yml"
    })

    # 3. Aggressive Container Prune on VPS
    print("🧹 Aggressively pruning containers on VPS...")
    cmds = [
        "docker stop postiz-app temporal bizosaas-brain-staging bizosaas-ai-agents-staging brain-mcp-github || true",
        "docker rm postiz-app temporal bizosaas-brain-staging bizosaas-ai-agents-staging brain-mcp-github || true",
        "docker stop postiz-postgres postiz-redis temporal-postgresql || true",
        "docker rm postiz-postgres postiz-redis temporal-postgresql || true"
    ]
    for cmd in cmds:
        subprocess.run(["sshpass", "-p", "&k3civYG5Q6YPb", "ssh", "-o", "StrictHostKeyChecking=no", "root@194.238.16.237", cmd])

    # 4. Trigger Redeployment
    print("🚀 Triggering Final CLEAN Redeployments...")
    call_trpc("compose.deploy", {"composeId": CORE_ID})
    call_trpc("compose.deploy", {"composeId": POSTIZ_ID})

if __name__ == "__main__":
    finalize_sync()
    print("\n✅ Final platform sync completed. Check Dokploy for 'done' status.")
