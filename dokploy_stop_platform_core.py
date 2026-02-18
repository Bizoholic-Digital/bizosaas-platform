import requests
import json
import urllib.parse

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

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

if __name__ == "__main__":
    # Project: platform-core (p4fmYaVZ_iDFDH4XSDnOU)
    proj_id = "p4fmYaVZ_iDFDH4XSDnOU"
    print(f"🔍 Inspecting platform-core ({proj_id})...")
    
    envs_res = call_trpc("environment.all", {"projectId": proj_id})
    print(f"Environments: {json.dumps(envs_res, indent=2)}")
    
    envs = envs_res.get("result", {}).get("data", {}).get("json", [])
    for env in envs:
        env_id = env["environmentId"]
        print(f"\n🌐 Env: {env['name']} ({env_id})")
        
        comp_res = call_trpc("compose.all", {"environmentId": env_id})
        composes = comp_res.get("result", {}).get("data", {}).get("json", [])
        for c in composes:
            print(f"  📦 Compose: {c['name']} (ID: {c['composeId']}) Status: {c.get('composeStatus')}")
            # If it's running, STOP IT.
            print(f"  🛑 Stopping {c['name']}...")
            call_trpc("compose.stop", {"composeId": c["composeId"]}, method="POST")
            
        app_res = call_trpc("application.all", {"environmentId": env_id})
        apps = app_res.get("result", {}).get("data", {}).get("json", [])
        for a in apps:
            print(f"  🚀 Application: {a['name']} (ID: {a['applicationId']}) Status: {a.get('applicationStatus')}")
            print(f"  🛑 Stopping {a['name']}...")
            call_trpc("application.stop", {"applicationId": a["applicationId"]}, method="POST")
