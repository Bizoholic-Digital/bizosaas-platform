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
        print(f"Error parsing response for {endpoint}: {e}")
        return {"error": str(e), "status_code": response.status_code}

def update_compose(compose_id, updates):
    print(f"⚙️ Updating Compose Service {compose_id} with {updates}...")
    # First get the current config
    # Actually, compose.update takes many fields. We should be careful.
    # But based on project.one output, we know what to send.
    res = call_trpc("compose.update", {"composeId": compose_id, **updates}, method="POST")
    print(f"  Result: {json.dumps(res)}")
    return res

def redeploy_compose(compose_id):
    print(f"🚀 Redeploying Compose Service {compose_id}...")
    res = call_trpc("compose.redeploy", {"composeId": compose_id}, method="POST")
    print(f"  Result: {json.dumps(res)}")
    return res

if __name__ == "__main__":
    # From projects_full.json analysis:
    # sot3ld (New Core) -> composeId: CbM3L2Z3LJemaumOC6Yd4
    # pltjdr (New Postiz) -> composeId: EYKt_rt5nqcBHTpD25633
    
    # 1. Update Core-Stack (sot3ld)
    update_compose("CbM3L2Z3LJemaumOC6Yd4", {
        "repository": "bizosaas-platform",
        "composePath": "infrastructure/compose/docker-compose.core-stack.yml"
    })
    
    # 2. Update Postiz-Stack (pltjdr)
    update_compose("EYKt_rt5nqcBHTpD25633", {
        "repository": "bizosaas-platform",
        "composePath": "docker-compose.postiz.yml"
    })
    
    # 3. Trigger Redeployments
    redeploy_compose("CbM3L2Z3LJemaumOC6Yd4") # Core
    redeploy_compose("EYKt_rt5nqcBHTpD25633") # Postiz
    
    print("\n✅ Final deployment triggers sent.")
