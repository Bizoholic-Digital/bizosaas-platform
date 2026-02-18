import requests
import json
import urllib.parse
import subprocess

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc_get(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    input_data = {"json": data if data else {}}
    query_str = urllib.parse.quote(json.dumps(input_data))
    url = f"{url}?input={query_str}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def call_trpc_post(endpoint, data):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    print("🔍 ULTIMATE PROJECT SCAN (using project.one)...")
    projects_res = call_trpc_get("project.all")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    for proj in projects:
        p_id = proj["projectId"]
        print(f"\n📁 Scanning Project: {proj['name']} ({p_id})")
        p_one = call_trpc_get("project.one", {"projectId": p_id})
        data = p_one.get("result", {}).get("data", {}).get("json", {})
        
        envs = data.get("environments", [])
        for env in envs:
            # Apps
            for a in env.get("applications", []):
                print(f"    - [APP] {a['name']} (appName: {a.get('appName')})")
                if "brain" in a['name'].lower() or "ai-agents" in a['name'].lower() or "postiz" in a['name'].lower():
                    if proj['name'] != "BizOSaaS-Platform":
                        print(f"      ☢️ LEGACY APP DETECTED! Stopping {a['applicationId']}...")
                        call_trpc_post("application.stop", {"applicationId": a['applicationId']})
            
            # Composes
            for c in env.get("composes", []):
                print(f"    - [COMPOSE] {c['name']} (ID: {c['composeId']})")
                if "core" in c['name'].lower() or "postiz" in c['name'].lower():
                    if proj['name'] != "BizOSaaS-Platform":
                        print(f"      ☢️ LEGACY COMPOSE DETECTED! Stopping {c['composeId']}...")
                        call_trpc_post("compose.stop", {"composeId": c['composeId']})

    print("\n✅ Ultimate project scan and legacy stop completed.")
