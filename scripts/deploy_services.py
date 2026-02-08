import requests
import json
import os

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

services = [
    {
        "name": "Wagtail CMS",
        "composeId": "IqBW7qKCwSKw0UYBiaf7c",
        "file": "docker-compose.wagtail-cms.yml"
    },
    {
        "name": "SEO Panel",
        "composeId": "-ShbMgQjuEzlKOl28uXtX",
        "file": "docker-compose.seo-panel.yml"
    },
    {
        "name": "Core Stack",
        "composeId": "QiOdwXQi4ZQCM3Qg_KNcl",
        "file": "bizosaas-brain-core/deploy/docker-compose.core.yml"
    }
]

def deploy_service(service):
    print(f"🚀 Deploying {service['name']}...")
    
    # Read Compose File
    try:
        with open(service['file'], 'r') as f:
            compose_content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {service['file']}")
        return

    # Update Compose
    update_url = f"{BASE_URL}/compose.update"
    payload = {
        "composeId": service['composeId'],
        "composeFile": compose_content
    }
    
    try:
        response = requests.post(update_url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"✅ Updated configuration for {service['name']}")
    except Exception as e:
        print(f"❌ Failed to update {service['name']}: {e}")
        if hasattr(e, 'response') and e.response:
            print(e.response.text)
        return

    # Trigger Deployment
    deploy_url = f"{BASE_URL}/compose.deploy"
    payload = {
        "composeId": service['composeId']
    }
    
    try:
        response = requests.post(deploy_url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"ignored: {response.text}") # Sometimes returns json
        print(f"✅ Deployment triggered for {service['name']}")
    except Exception as e:
        print(f"❌ Failed to deploy {service['name']}: {e}")
        if hasattr(e, 'response') and e.response:
            print(e.response.text)

if __name__ == "__main__":
    for s in services:
        deploy_service(s)
