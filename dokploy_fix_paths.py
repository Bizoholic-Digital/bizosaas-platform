import requests
import json

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data):
    url = f"{DOKPLOY_BASE_URL if 'DOKPLOY_BASE_URL' in globals() else BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def update_compose_path(compose_id, path):
    print(f"Updating composePath for {compose_id} to {path}...")
    # The 'compose.update' tool documentation says it accepts all application config fields.
    # We saw 'composePath' in the 'compose.one' output.
    data = {"composeId": compose_id, "composePath": path}
    return call_trpc("compose.update", data)

if __name__ == "__main__":
    core_id = "PW095Z8RFCzSdZ1bxha97"
    postiz_id = "bYH9mTmaYnWXg7wv2-MoI"
    
    # Update Core Stack to use its specific file
    # Wait, in Dokploy, if we provide the content directly via 'composeFile', 
    # the 'composePath' usually doesn't matter unless it's pulling from Git.
    # However, the user sees the old path. Let's force it to something descriptive.
    
    update_compose_path(core_id, "./docker-compose.core-stack.yml")
    update_compose_path(postiz_id, "./docker-compose.postiz.yml")
    
    print("\n✅ Path updates sent. Now triggering redeployment to be sure.")
    
    call_trpc("compose.deploy", {"composeId": core_id})
    call_trpc("compose.deploy", {"composeId": postiz_id})
