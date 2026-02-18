import requests
import json

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data, method="POST"):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def update_env(compose_id, env_str):
    data = {"composeId": compose_id, "env": env_str}
    return call_trpc("compose.update", data)

def create_domain(compose_id, host, port=80, service_name="", https=True):
    data = {
        "composeId": compose_id,
        "host": host,
        "port": port,
        "service_name": service_name,
        "https": https,
        "path": "/",
        "certificateType": "letsencrypt"
    }
    # Some Dokploy versions use service_name, some use serviceName
    # Let's try both or check the API
    data["serviceName"] = service_name
    return call_trpc("domain.create", data)

def deploy_compose(compose_id):
    data = {"composeId": compose_id}
    return call_trpc("compose.deploy", data)

if __name__ == "__main__":
    core_id = "PW095Z8RFCzSdZ1bxha97"
    postiz_id = "bYH9mTmaYnWXg7wv2-MoI"
    
    # 1. Update Core Domains
    print("Assigning domains to core-stack...")
    create_domain(core_id, "api.bizoholic.net", port=8000, service_name="brain-gateway")

    # 2. Update Postiz Domains
    print("Assigning domains to postiz-stack...")
    create_domain(postiz_id, "postiz.bizoholic.net", port=5000, service_name="postiz-app")

    # 3. Trigger Deployment
    print("🚀 Triggering deployment for core-stack...")
    deploy_compose(core_id)
    
    print("🚀 Triggering deployment for postiz-stack...")
    deploy_compose(postiz_id)

    print("🏁 Deployment triggers sent.")
