import requests
import json
import urllib.parse
import subprocess

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None, method="POST"):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def fix_service(service_id, name, compose_content):
    print(f"🔧 Fixing Service: {name} ({service_id})...")
    # Set sourceType to 'docker-compose' (which means text input in Dokploy)
    # and clear the git-related fields
    data = {
        "composeId": service_id,
        "sourceType": "docker-compose", 
        "composeFile": compose_content,
        "composePath": "./docker-compose.yml" # Reset to default or something non-nested
    }
    res = call_trpc("compose.update", data)
    print(f"  Update Result: {json.dumps(res)}")
    
    print(f"  🚀 Redeploying {name}...")
    res = call_trpc("compose.deploy", {"composeId": service_id})
    print(f"  Deploy Result: {json.dumps(res)}")

if __name__ == "__main__":
    # --- CORE STACK ---
    core_id = "PW095Z8RFCzSdZ1bxha97"
    with open("/home/alagiri/projects/bizosaas-platform/infrastructure/compose/docker-compose.core-stack.yml", "r") as f:
        core_compose = f.read()
    fix_service(core_id, "core-stack", core_compose)
    
    # --- POSTIZ STACK ---
    postiz_id = "bYH9mTmaYnWXg7wv2-MoI"
    with open("/home/alagiri/projects/bizosaas-platform/docker-compose.postiz.yml", "r") as f:
        postiz_compose = f.read()
    fix_service(postiz_id, "postiz-stack", postiz_compose)
    
    print("\n✅ Service corrections sent.")
