import requests
import json
import urllib.parse

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
CORE_ID = "PW095Z8RFCzSdZ1bxha97"
POSTIZ_ID = "bYH9mTmaYnWXg7wv2-MoI"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None, method="POST"):
    url = f"{BASE_URL}/{endpoint}"
    if method == "GET":
        import urllib.parse
        input_data = {"json": data if data else {}}
        query_str = urllib.parse.quote(json.dumps(input_data))
        url = f"{url}?input={query_str}"
        response = requests.get(url, headers=HEADERS)
    else:
        payload = {"json": data}
        response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    # 1. Update our new services to use 'raw' source type
    print("🛠️ Updating new services to 'raw' source type...")
    
    with open("/home/alagiri/projects/bizosaas-platform/infrastructure/compose/docker-compose.core-stack.yml", "r") as f:
        core_compose = f.read()
    call_trpc("compose.update", {"composeId": CORE_ID, "sourceType": "raw", "composeFile": core_compose})

    with open("/home/alagiri/projects/bizosaas-platform/docker-compose.postiz.yml", "r") as f:
        postiz_compose = f.read()
    call_trpc("compose.update", {"composeId": POSTIZ_ID, "sourceType": "raw", "composeFile": postiz_compose})

    # 2. Global scan to find ANY service with the same appNames
    print("\n🔍 Scanning for conflicting appNames...")
    # These are the appNames we found on the VPS
    conflicting_app_names = ["compose-synthesize-online-feed-gb95pq", "compose-calculate-1080p-bus-z7bwrg"]
    
    projects_res = call_trpc("project.all", method="GET")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    for proj in projects:
        proj_id = proj["projectId"]
        env_res = call_trpc("environment.all", {"projectId": proj_id}, method="GET")
        envs = env_res.get("result", {}).get("data", {}).get("json", [])
        
        for env in envs:
            env_id = env["environmentId"]
            comp_res = call_trpc("compose.all", {"environmentId": env_id}, method="GET")
            composes = comp_res.get("result", {}).get("data", {}).get("json", [])
            for c in composes:
                app_name = c.get("appName")
                cid = c["composeId"]
                if app_name in conflicting_app_names and cid not in [CORE_ID, POSTIZ_ID]:
                    print(f"  🚨 FOUND PHANTOM CONFLICT: {c['name']} (ID: {cid}) in Project {proj['name']}")
                    print(f"    🛑 STOPPING & REMOVING LEGACY PHANTOM...")
                    call_trpc("compose.stop", {"composeId": cid}, method="POST")
                    call_trpc("compose.remove", {"composeId": cid}, method="POST")

    print("\n🚀 Triggering CLEAN REDEPLOYMENT...")
    call_trpc("compose.deploy", {"composeId": CORE_ID}, method="POST")
    call_trpc("compose.deploy", {"composeId": POSTIZ_ID}, method="POST")
    
    print("\n✅ Platform cleanup and modular re-sync finalized.")
