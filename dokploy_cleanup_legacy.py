import requests
import json
import urllib.parse

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
NEW_PROJECT_ID = "BJNbkCSMjewPiAnCusl8H"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None, method="GET"):
    if method == "GET":
        input_data = {"json": data if data else {}}
        query_str = urllib.parse.quote(json.dumps(input_data))
        url = f"{BASE_URL}/{endpoint}?input={query_str}"
        response = requests.get(url, headers=HEADERS)
    else:
        url = f"{BASE_URL}/{endpoint}"
        payload = {"json": data}
        response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    print("🔍 Fetching all projects to identify legacy services...")
    projects_res = call_trpc("project.all")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    legacy_services = []
    
    for proj in projects:
        proj_id = proj["projectId"]
        proj_name = proj["name"]
        if proj_id == NEW_PROJECT_ID:
            continue
            
        print(f"Checking project: {proj_name} ({proj_id})")
        # Get compose services in this project
        # TRPC endpoint for compose.all requires environmentId or similar? 
        # Actually project.one returns services usually.
        proj_detail = call_trpc("project.one", {"projectId": proj_id})
        data = proj_detail.get("result", {}).get("data", {}).get("json", {})
        
        # Check environments -> compose
        for env in data.get("environments", []):
            for compose in env.get("composes", []):
                name = compose["name"].lower()
                if "core" in name or "postiz" in name or "brain" in name:
                    print(f"  ⚠️ Found potential legacy service: {compose['name']} (ID: {compose['composeId']})")
                    legacy_services.append({"id": compose["composeId"], "name": compose["name"], "type": "compose"})
            
            # Also check applications
            for app in env.get("applications", []):
                name = app["name"].lower()
                if "core" in name or "postiz" in name or "brain" in name:
                    print(f"  ⚠️ Found potential legacy application: {app['name']} (ID: {app['applicationId']})")
                    legacy_services.append({"id": app["applicationId"], "name": app["name"], "type": "application"})

    print(f"\nFound {len(legacy_services)} legacy services to stop.")
    
    for svc in legacy_services:
        print(f"🛑 Stopping {svc['type']} {svc['name']} ({svc['id']})...")
        if svc["type"] == "compose":
            res = call_trpc("compose.stop", {"composeId": svc["id"]}, method="POST")
        else:
            res = call_trpc("application.stop", {"applicationId": svc["id"]}, method="POST")
        print(f"  Result: {json.dumps(res)}")

    print("\n✅ Legacy services cleanup requested.")
