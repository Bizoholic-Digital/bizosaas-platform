import requests
import sys
import time

# Configuration
API_URL = "https://dk.bizoholic.com/api/trpc"
API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"

# Service Mapping
SERVICES = [
    {
        "name": "Client Portal",
        "id": "zz6VpI3h8BFXPUTZZb01G",
        "file": "docker-compose.client-portal.yml"
    },
    {
        "name": "Admin Portal",
        "id": "NlDPTf6BZgSQilinf2YaU",
        "file": "portals/admin-dashboard/docker-compose.yml"
    }
]

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def update_compose(service):
    print(f"[{service['name']}] Reading {service['file']}...")
    try:
        with open(service['file'], 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File {service['file']} not found!")
        sys.exit(1)
        
    print(f"[{service['name']}] Uploading updated configuration...")
    payload = {
        "json": {
            "composeId": service['id'],
            "composeFile": content,
            "sourceType": "raw"
        }
    }
    
    response = requests.post(f"{API_URL}/compose.update", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"[{service['name']}] Configuration updated successfully.")
    else:
        print(f"[{service['name']}] Error uploading config: {response.text}")
        sys.exit(1)

def redeploy_service(service):
    print(f"[{service['name']}] Triggering deployment...")
    payload = {
        "json": {
            "composeId": service['id']
        }
    }
    
    response = requests.post(f"{API_URL}/compose.deploy", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"[{service['name']}] Deployment triggered successfully! 🚀")
    else:
        print(f"[{service['name']}] Error triggering deployment: {response.text}")
        sys.exit(1)

def main():
    print("=== Updating Portals ===")
    for service in SERVICES:
        update_compose(service)
        redeploy_service(service)
        print("---")

if __name__ == "__main__":
    main()
