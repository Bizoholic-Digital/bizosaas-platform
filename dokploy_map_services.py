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
    print("🔍 FINAL VALIDATION Audit...")
    projects_res = call_trpc("project.all")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    mapping = []
    for proj in projects:
        p_id = proj["projectId"]
        p_one = call_trpc("project.one", {"projectId": p_id})
        data = p_one.get("result", {}).get("data", {}).get("json", {})
        
        envs = data.get("environments", [])
        for env in envs:
            # CORRECTED FIELD NAMES: 'compose' and 'applications'
            for c in env.get("compose", []):
                mapping.append({
                    "project": proj["name"],
                    "service": c["name"],
                    "appName": c["appName"],
                    "id": c["composeId"],
                    "type": "COMPOSE",
                    "status": c.get("composeStatus")
                })
            for a in env.get("applications", []):
                mapping.append({
                    "project": proj["name"],
                    "service": a["name"],
                    "appName": a["appName"],
                    "id": a["applicationId"],
                    "type": "APP",
                    "status": a.get("status")
                })

    # Target Mapping
    targets = {
        "compose-generate-haptic-transmitter-pltjdr": "NEW Postiz",
        "compose-compress-wireless-alarm-sot3ld": "NEW Core",
        "compose-input-cross-platform-feed-3szzkr": "OLD Postiz",
        "compose-synthesize-online-feed-gb95pq": "OLD Core"
    }

    print("\n📊 Service Status Report:")
    for target_appName, label in targets.items():
        found = False
        for m in mapping:
            if m["appName"] == target_appName:
                print(f"  {label} ({target_appName}): Status = {m['status']} (Project: {m['project']})")
                found = True
        if not found:
            print(f"  {label} ({target_appName}): NOT FOUND (Expected if deleted or hidden)")

    print("\n📦 Relevant Catalog:")
    for m in mapping:
        if m["project"] == "BizOSaaS-Platform":
            print(f"  [{m['type']}] {m['service']} ({m['appName']}) -> {m['status']}")
