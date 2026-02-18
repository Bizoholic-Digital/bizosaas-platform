import requests
import json
import urllib.parse
import os

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
    targets = [
        {"id": "CbM3L2Z3LJemaumOC6Yd4", "file": "core_logs.txt", "name": "Core-Stack"},
        {"id": "EYKt_rt5nqcBHTpD25633", "file": "postiz_logs.txt", "name": "Postiz-Stack"}
    ]
    
    for target in targets:
        print(f"📥 Extracting logs for {target['name']}...")
        res = call_trpc("compose.one", {"composeId": target["id"]})
        data = res.get("result", {}).get("data", {}).get("json", {})
        
        deployments = data.get("deployments", [])
        if deployments:
            latest = deployments[0]
            log_content = latest.get("log", "NO LOG CONTENT")
            with open(target["file"], "w") as f:
                f.write(log_content)
            print(f"  ✅ Saved to {target['file']} (Size: {len(log_content)} chars)")
        else:
            print(f"  ❌ No deployments found for {target['name']}")
