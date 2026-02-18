import requests
import json
import urllib.parse
import time

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None, method="POST"):
    url = f"{BASE_URL}/{endpoint}"
    if method == "GET":
        input_str = json.dumps({"json": data if data else {}}, separators=(',', ':'))
        query_str = urllib.parse.quote(input_str)
        url = f"{url}?input={query_str}"
        response = requests.get(url, headers=HEADERS)
    else:
        payload = {"json": data if data else {}}
        response = requests.post(url, headers=HEADERS, json=payload)
    
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e), "status": response.status_code}

def fix_service(compose_id, repo, path):
    print(f"\n🛠️ Fixing Service {compose_id}...")
    # 1. Update config
    update_res = call_trpc("compose.update", {
        "composeId": compose_id,
        "repository": repo,
        "composePath": path,
        "branch": "staging",
        "owner": "Bizoholic-Digital"
    })
    print(f"  Update Result: {json.dumps(update_res)}")
    
    # 2. Verify config
    verify_res = call_trpc("compose.one", {"composeId": compose_id}, method="GET")
    data = verify_res.get("result", {}).get("data", {}).get("json", {})
    actual_repo = data.get("repository")
    actual_path = data.get("composePath")
    print(f"  Verified Config: Repo={actual_repo}, Path={actual_path}")
    
    if actual_repo == repo and actual_path == path:
        print("  ✅ Config standardizing success.")
        # 3. Redeploy
        print("  🚀 Triggering redeploy...")
        redeploy_res = call_trpc("compose.redeploy", {"composeId": compose_id})
        print(f"  Redeploy Result: {json.dumps(redeploy_res)}")
    else:
        print("  ⚠️ Update did NOT persist as expected.")

if __name__ == "__main__":
    # Core
    fix_service("CbM3L2Z3LJemaumOC6Yd4", "bizosaas-platform", "infrastructure/compose/docker-compose.core-stack.yml")
    # Postiz
    fix_service("EYKt_rt5nqcBHTpD25633", "bizosaas-platform", "docker-compose.postiz.yml")
    
    print("\n✅ Force update complete.")
