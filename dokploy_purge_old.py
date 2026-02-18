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
    # From projects_full.json analysis:
    # 3szzkr (Old Postiz) -> composeId: ejfhY3aMJcFl8m3coSYxK
    # gb95pq (Old Core) -> composeId: QiOdwXQi4ZQCM3Qg_KNcl
    
    old_services = [
        {"id": "ejfhY3aMJcFl8m3coSYxK", "name": "OLD Postiz (3szzkr)"},
        {"id": "QiOdwXQi4ZQCM3Qg_KNcl", "name": "OLD Core (gb95pq)"}
    ]
    
    for service in old_services:
        print(f"\n🗑️ Removing redundant Service {service['name']} ({service['id']})...")
        res = call_trpc("compose.remove", {"composeId": service["id"]})
        print(f"  Result: {json.dumps(res)}")
    
    print("\n🚀 Now triggering redeployment for NEW stacks...")
    # CbM3L2Z3LJemaumOC6Yd4 (Core)
    # EYKt_rt5nqcBHTpD25633 (Postiz)
    
    call_trpc("compose.redeploy", {"composeId": "CbM3L2Z3LJemaumOC6Yd4"})
    call_trpc("compose.redeploy", {"composeId": "EYKt_rt5nqcBHTpD25633"})
    
    print("✅ Cleanup and redeploy triggered.")
