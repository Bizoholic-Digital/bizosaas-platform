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
    targets = [
        {"id": "CbM3L2Z3LJemaumOC6Yd4", "name": "Core-Stack (sot3ld)"},
        {"id": "EYKt_rt5nqcBHTpD25633", "name": "Postiz-Stack (pltjdr)"}
    ]
    
    for target in targets:
        print(f"\n{'='*60}")
        print(f"📋 {target['name']}")
        print('='*60)
        
        # Get compose details
        res = call_trpc("compose.one", {"composeId": target["id"]})
        data = res.get("result", {}).get("data", {}).get("json", {})
        
        if not data:
            print("❌ No data found")
            continue
            
        deployments = data.get("deployments", [])
        print(f"\n📊 Total Deployments: {len(deployments)}")
        
        if deployments:
            # Show last 3 deployments
            for i, dep in enumerate(deployments[:3]):
                print(f"\n--- Deployment {i+1} ---")
                print(f"  ID: {dep['deploymentId']}")
                print(f"  Title: {dep['title']}")
                print(f"  Status: {dep['status']}")
                print(f"  Created: {dep['createdAt']}")
                print(f"  Log Path: {dep.get('logPath', 'N/A')}")
                
                # Try to read the log via deployment.one
                if dep.get('deploymentId'):
                    log_res = call_trpc("deployment.one", {"deploymentId": dep['deploymentId']})
                    log_data = log_res.get("result", {}).get("data", {}).get("json", {})
                    
                    if log_data and log_data.get("logPath"):
                        print(f"\n  📄 Log Content (last 500 chars):")
                        log_content = log_data.get("log", "NO LOG")
                        print(f"  {log_content[-500:]}")
