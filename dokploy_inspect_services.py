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
    # sot3ld (New Core) -> composeId: CbM3L2Z3LJemaumOC6Yd4
    # pltjdr (New Postiz) -> composeId: EYKt_rt5nqcBHTpD25633
    
    targets = [
        {"id": "CbM3L2Z3LJemaumOC6Yd4", "name": "Core-Stack (sot3ld)"},
        {"id": "EYKt_rt5nqcBHTpD25633", "name": "Postiz-Stack (pltjdr)"}
    ]
    
    for target in targets:
        print(f"\n🔍 Inspecting {target['name']}...")
        res = call_trpc("compose.one", {"composeId": target["id"]})
        data = res.get("result", {}).get("data", {}).get("json", {})
        
        if data:
            print(f"  Status: {data.get('composeStatus')}")
            deployments = data.get("deployments", [])
            print(f"  Deployments Count: {len(deployments)}")
            if deployments:
                latest = deployments[0]
                print(f"  Latest Dep ID: {latest['deploymentId']}")
                print(f"  Dep Status: {latest['status']}")
                print(f"  Error: {latest.get('error')}")
                if latest.get("log"):
                    print(f"  Log (last 200 chars): {latest['log'][-200:]}")
        else:
            print("  Service not found.")
