import requests
import json
import urllib.parse

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    import urllib.parse
    input_data = {"json": data if data else {}}
    query_str = urllib.parse.quote(json.dumps(input_data))
    url = f"{url}?input={query_str}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    print("🔍 ULTIMATE Deep Scanning ALL Dokploy Projects...")
    projects_res = call_trpc("project.all")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    for proj in projects:
        proj_id = proj["projectId"]
        print(f"\n📁 Project: {proj['name']} ({proj_id})")
        
        env_res = call_trpc("environment.all", {"projectId": proj_id})
        envs = env_res.get("result", {}).get("data", {}).get("json", [])
        
        for env in envs:
            env_id = env["environmentId"]
            print(f"  🌐 Environment: {env['name']} ({env_id})")
            
            # Check Applications
            app_res = call_trpc("application.all", {"environmentId": env_id})
            apps = app_res.get("result", {}).get("data", {}).get("json", [])
            for a in apps:
                print(f"    - [APP] {a['name']} (ID: {a['applicationId']}, appName: {a.get('appName')})")
                
            # Check Compose Stacks
            comp_res = call_trpc("compose.all", {"environmentId": env_id})
            composes = comp_res.get("result", {}).get("data", {}).get("json", [])
            for c in composes:
                print(f"    - [COMPOSE] {c['name']} (ID: {c['composeId']}, Source: {c.get('sourceType')})")

    print("\n✅ Ultimate scan completed.")
