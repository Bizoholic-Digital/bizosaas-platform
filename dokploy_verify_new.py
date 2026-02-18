import requests
import json

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
CORE_ID = "CbM3L2Z3LJemaumOC6Yd4"
POSTIZ_ID = "EYKt_rt5nqcBHTpD25633"

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
    print("📋 Checking New Core Stack Status...")
    core = call_trpc("compose.one", {"composeId": CORE_ID})
    c_status = core.get("result", {}).get("data", {}).get("json", {}).get("composeStatus")
    print(f"  Status: {c_status}")
    
    print("\n📋 Checking New Postiz Stack Status...")
    postiz = call_trpc("compose.one", {"composeId": POSTIZ_ID})
    p_status = postiz.get("result", {}).get("data", {}).get("json", {}).get("composeStatus")
    print(f"  Status: {p_status}")
    
    # Check for any deployments
    print("\n🚀 Latest Core Deployments:")
    for d in core.get("result", {}).get("data", {}).get("json", {}).get("deployments", [])[:3]:
        print(f"    - ID: {d['deploymentId']} Status: {d['status']} Created: {d['createdAt']}")

    print("\n🚀 Latest Postiz Deployments:")
    for d in postiz.get("result", {}).get("data", {}).get("json", {}).get("deployments", [])[:3]:
        print(f"    - ID: {d['deploymentId']} Status: {d['status']} Created: {d['createdAt']}")
