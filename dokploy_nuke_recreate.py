import requests
import json
import time

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
PROJECT_ID = "BJNbkCSMjewPiAnCusl8H"
ENV_ID = "UXUyK3hNtHi_bPA7lkYkI"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def nuke_and_recreate():
    # 1. IDs to nuke
    core_id = "PW095Z8RFCzSdZ1bxha97"
    postiz_id = "bYH9mTmaYnWXg7wv2-MoI"
    
    print("🧨 Nuking existing modular services in Dokploy...")
    call_trpc("compose.stop", {"composeId": core_id})
    call_trpc("compose.remove", {"composeId": core_id})
    call_trpc("compose.stop", {"composeId": postiz_id})
    call_trpc("compose.remove", {"composeId": postiz_id})
    
    time.sleep(5) # Wait for cleanup
    
    # 2. Re-create Core Stack
    print("🆕 Re-creating Core Stack as RAW...")
    with open("/home/alagiri/projects/bizosaas-platform/infrastructure/compose/docker-compose.core-stack.yml", "r") as f:
        core_compose = f.read()
    
    core_res = call_trpc("compose.create", {
        "name": "core-stack",
        "description": "Unified Core Platform Stack (Raw)",
        "environmentId": ENV_ID,
        "composeFile": core_compose,
        "sourceType": "raw"
    })
    new_core_id = core_res.get("result", {}).get("data", {}).get("json", {}).get("composeId")
    print(f"  New Core ID: {new_core_id}")
    
    # 3. Re-create Postiz Stack
    print("🆕 Re-creating Postiz Stack as RAW...")
    with open("/home/alagiri/projects/bizosaas-platform/docker-compose.postiz.yml", "r") as f:
        postiz_compose = f.read()
        
    postiz_res = call_trpc("compose.create", {
        "name": "postiz-stack",
        "description": "Unified Social Stack (Raw)",
        "environmentId": ENV_ID,
        "composeFile": postiz_compose,
        "sourceType": "raw"
    })
    new_postiz_id = postiz_res.get("result", {}).get("data", {}).get("json", {}).get("composeId")
    print(f"  New Postiz ID: {new_postiz_id}")
    
    # 4. Map Domains and Env Vars using setup_platform logic
    # (Simplified for this script to just finish the job)
    print("🔗 Mapping Domains and Syncing Envs...")
    # This will require updating the setup_platform.py with new IDs
    return new_core_id, new_postiz_id

if __name__ == "__main__":
    c_id, p_id = nuke_and_recreate()
    print(f"\n✅ RECREATED SERVICES. NEW IDs: CORE={c_id}, POSTIZ={p_id}")
    print("⚠️ PLEASE UPDATE setup_platform.py WITH THESE IDs AND RUN IT.")
