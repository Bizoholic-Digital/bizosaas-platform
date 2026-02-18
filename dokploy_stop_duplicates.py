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
    # Duplicates to stop:
    # z7bwrg -> bYH9mTmaYnWXg7wv2-MoI
    # 3zxb4j -> PW095Z8RFCzSdZ1bxha97
    
    duplicates = [
        {"id": "bYH9mTmaYnWXg7wv2-MoI", "name": "DUPE Postiz (z7bwrg)"},
        {"id": "PW095Z8RFCzSdZ1bxha97", "name": "DUPE Core (3zxb4j)"}
    ]
    
    for dupe in duplicates:
        print(f"🛑 Stopping duplicate {dupe['name']}...")
        res = call_trpc("compose.stop", {"composeId": dupe["id"]})
        print(f"  Result: {json.dumps(res)}")
    
    print("\n🚀 Retriggering final stacks one last time...")
    call_trpc("compose.redeploy", {"composeId": "CbM3L2Z3LJemaumOC6Yd4"}) # Core
    call_trpc("compose.redeploy", {"composeId": "EYKt_rt5nqcBHTpD25633"}) # Postiz
    
    print("✅ Duplicates stopped and final stacks triggered.")
