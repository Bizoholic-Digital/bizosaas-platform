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
    # Environments from platform-core and marketing-suite
    env_ids = ["j5ifoftZ7sMPQCpcSUBE3", "9AsXQvtfKvkwM0_WFCHXQ"]
    
    for eid in env_ids:
        print(f"\n🌐 Querying Env ID: {eid}")
        
        comps = call_trpc("compose.all", {"environmentId": eid})
        data = comps.get("result", {}).get("data", {}).get("json", [])
        for c in data:
            print(f"  📦 Compose: {c['name']} ({c['composeId']}) Status: {c['composeStatus']}")
            print(f"    🛑 STOPPING...")
            call_trpc("compose.stop", {"composeId": c["composeId"]}, method="POST")

        apps = call_trpc("application.all", {"environmentId": eid})
        data = apps.get("result", {}).get("data", {}).get("json", [])
        for a in data:
            print(f"  🚀 App: {a['name']} ({a['applicationId']}) Status: {a['applicationStatus']}")
            print(f"    🛑 STOPPING...")
            call_trpc("application.stop", {"applicationId": a["applicationId"]}, method="POST")

    print("\n✅ Targeted env stop completed.")
