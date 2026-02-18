import requests
import json
import urllib.parse
import subprocess

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
NEW_PROJECT_ID = "BJNbkCSMjewPiAnCusl8H"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None, method="GET"):
    if method == "GET":
        input_data = {"json": data if data else {}}
        query_str = urllib.parse.quote(json.dumps(input_data))
        url = f"{BASE_URL}/{endpoint}?input={query_str}"
        response = requests.get(url, headers=HEADERS)
    else:
        url = f"{BASE_URL}/{endpoint}"
        payload = {"json": data}
        response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def kill_legacy_vps():
    print("🧨 Nuking legacy containers on VPS...")
    containers = ["postiz-app", "temporal", "postiz-postgres", "temporal-postgresql", "postiz-redis"]
    for c in containers:
        cmd = f"sshpass -p '&k3civYG5Q6YPb' ssh -o StrictHostKeyChecking=no root@194.238.16.237 'docker rm -f {c} || true'"
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    kill_legacy_vps()
    
    print("🔍 Searching for legacy service remnants in Dokploy...")
    projects_res = call_trpc("project.all")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    for proj in projects:
        proj_id = proj["projectId"]
        if proj_id == NEW_PROJECT_ID:
            continue
            
        res = call_trpc("project.one", {"projectId": proj_id})
        data = res.get("result", {}).get("data", {}).get("json", {})
        
        for env in data.get("environments", []):
            for compose in env.get("composes", []):
                name = compose["name"].lower()
                if "postiz" in name or "temporal" in name:
                    print(f"🛑 Stopping legacy compose: {compose['name']} ({compose['composeId']})")
                    call_trpc("compose.stop", {"composeId": compose["composeId"]}, method="POST")
                    # Delete them to be sure
                    print(f"🗑️ Deleting legacy compose: {compose['name']}")
                    call_trpc("compose.remove", {"composeId": compose["composeId"]}, method="POST")

    print("\n🚀 Triggering FRESH DEPLOYMENT for new modular stacks...")
    # Core
    call_trpc("compose.deploy", {"composeId": "PW095Z8RFCzSdZ1bxha97"}, method="POST")
    # Postiz
    call_trpc("compose.deploy", {"composeId": "bYH9mTmaYnWXg7wv2-MoI"}, method="POST")
    
    print("\n✅ Cleanup and Redeploy initiated.")
