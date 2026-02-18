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
        # TRPC POST uses {"json": {...}} in the body
        payload = {"json": data if data else {}}
        response = requests.post(url, headers=HEADERS, json=payload)
    
    try:
        return response.json()
    except Exception as e:
        print(f"Error parsing response for {endpoint}: {e}")
        return {"error": str(e), "status_code": response.status_code}

if __name__ == "__main__":
    # From projects_full.json analysis:
    # 3szzkr (Old Postiz) -> composeId: ejfhY3aMJcFl8m3coSYxK
    # gb95pq (Old Core) -> composeId: QiOdwXQi4ZQCM3Qg_KNcl
    
    old_services = [
        {"id": "ejfhY3aMJcFl8m3coSYxK", "name": "OLD Postiz (3szzkr)"},
        {"id": "QiOdwXQi4ZQCM3Qg_KNcl", "name": "OLD Core (gb95pq)"}
    ]
    
    for service in old_services:
        print(f"\nProcessing {service['name']}...")
        print(f"🛑 Stopping {service['id']}...")
        res = call_trpc("compose.stop", {"composeId": service["id"]}, method="POST")
        print(f"  Result: {json.dumps(res)}")
    
    print("\n✅ Cleanup step completed. Containers should now be freed up.")
