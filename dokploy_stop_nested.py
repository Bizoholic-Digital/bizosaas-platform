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
    potential_old_projects = ["p4fmYaVZ_iDFDH4XSDnOU", "5vSEXRRbEyUsnh0Ji2-IJ"]
    
    for pid in potential_old_projects:
        print(f"\n🔍 Inspecting Project ID: {pid}")
        res = call_trpc("project.one", {"projectId": pid})
        # print(json.dumps(res, indent=2))
        
        data = res.get("result", {}).get("data", {}).get("json", {})
        envs = data.get("environments", [])
        if not envs:
             print("  ❌ No environments found in project.one output.")
             continue
             
        for env in envs:
            print(f"  🌐 Env: {env['name']} ({env['environmentId']})")
            # Look for composes/applications here
            for c in env.get("composes", []):
                print(f"    📦 Compose: {c['name']} ({c['composeId']}) Status: {c['composeStatus']}")
                if "core" in c['name'].lower() or "postiz" in c['name'].lower() or "brain" in name:
                     print(f"      🛑 Stopping {c['name']}...")
                     call_trpc("compose.stop", {"composeId": c["composeId"]}, method="POST")
            
            for a in env.get("applications", []):
                print(f"    🚀 App: {a['name']} ({a['applicationId']}) Status: {a['applicationStatus']}")
                if "core" in a['name'].lower() or "postiz" in a['name'].lower() or "brain" in name:
                     print(f"      🛑 Stopping {a['name']}...")
                     call_trpc("application.stop", {"applicationId": a["applicationId"]}, method="POST")
