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

def force_inject_config(compose_id, file_path):
    print(f"\n💉 Injecting config for {compose_id} from {file_path}...")
    if not os.path.exists(file_path):
        print(f"  ❌ File not found: {file_path}")
        return
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Use compose.update to set MUST the compose file content
    # Note: we might need to set sourceType to "raw" if github is failing
    res = call_trpc("compose.update", {
        "composeId": compose_id,
        "composeFile": content,
        "sourceType": "raw" # TEMPORARILY SET TO RAW TO FIX NOW
    })
    print(f"  Update Result: {json.dumps(res)}")
    
    # 2. Redeploy
    redeploy = call_trpc("compose.redeploy", {"composeId": compose_id})
    print(f"  Redeploy Result: {json.dumps(redeploy)}")

if __name__ == "__main__":
    # sot3ld (New Core) -> composeId: CbM3L2Z3LJemaumOC6Yd4
    # pltjdr (New Postiz) -> composeId: EYKt_rt5nqcBHTpD25633
    
    force_inject_config("CbM3L2Z3LJemaumOC6Yd4", "infrastructure/compose/docker-compose.core-stack.yml")
    force_inject_config("EYKt_rt5nqcBHTpD25633", "docker-compose.postiz.yml")
    
    print("\n✅ Force injection complete. Final verification pending.")
