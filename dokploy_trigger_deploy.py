import requests
import json
import urllib.parse

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
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 Triggering Final Deployment\n")
    
    print("📦 Deploying Core-Stack (sot3ld)...")
    core_result = call_trpc("compose.redeploy", {"composeId": "CbM3L2Z3LJemaumOC6Yd4"})
    print(f"  Result: {json.dumps(core_result, indent=2)}\n")
    
    print("📦 Deploying Postiz-Stack (pltjdr)...")
    postiz_result = call_trpc("compose.redeploy", {"composeId": "EYKt_rt5nqcBHTpD25633"})
    print(f"  Result: {json.dumps(postiz_result, indent=2)}\n")
    
    print("✅ Deployment triggered. Waiting 30 seconds before checking status...")
    import time
    time.sleep(30)
    
    print("\n📊 Checking deployment status...\n")
    
    # Check Core-Stack
    core_status = call_trpc("compose.one", {"composeId": "CbM3L2Z3LJemaumOC6Yd4"}, method="GET")
    core_data = core_status.get("result", {}).get("data", {}).get("json", {})
    print(f"Core-Stack Status: {core_data.get('composeStatus')}")
    
    # Check Postiz-Stack
    postiz_status = call_trpc("compose.one", {"composeId": "EYKt_rt5nqcBHTpD25633"}, method="GET")
    postiz_data = postiz_status.get("result", {}).get("data", {}).get("json", {})
    print(f"Postiz-Stack Status: {postiz_data.get('composeStatus')}")
    
    print("\n💡 Check deployment progress in Dokploy UI: https://dk.bizoholic.com")
