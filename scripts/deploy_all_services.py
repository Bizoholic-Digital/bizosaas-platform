#!/usr/bin/env python3
"""
Deploy all BizOSaaS services in the correct order
"""
import requests
import time

DOKPLOY_URL = "http://localhost:3000"
API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"

# Deployment order (dependencies first)
DEPLOYMENT_ORDER = [
    ("Vault", "1W8TCez-7vt661vt7-4Wn"),
    ("Core Stack", "QiOdwXQi4ZQCM3Qg_KNcl"),
    ("Lago Stack", "cbgmdr52hGC7XrA53Cw7z"),
    ("Client Portal", "zz6VpI3h8BFXPUTZZb01G"),
    ("Admin Portal", "NlDPTf6BZgSQilinf2YaU"),
    ("Business Directory", "jRJrq-UIekuq6XBaDOhh6")
]

def deploy_service(name, compose_id):
    """Deploy a service via Dokploy API"""
    url = f"{DOKPLOY_URL}/api/trpc/compose.deploy"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    payload = {"json": {"composeId": compose_id}}
    
    print(f"🚀 Deploying {name}...")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("result", {}).get("data", {}).get("json", {}).get("success"):
            print(f"✅ {name} deployment queued successfully")
            return True
        else:
            print(f"❌ {name} deployment failed: {result}")
            return False
    else:
        print(f"❌ {name} deployment failed: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("BizOSaaS Complete Deployment")
    print("=" * 60)
    print()
    
    success_count = 0
    failed_count = 0
    
    for name, compose_id in DEPLOYMENT_ORDER:
        if deploy_service(name, compose_id):
            success_count += 1
        else:
            failed_count += 1
        
        # Wait between deployments to avoid overwhelming the server
        print("⏳ Waiting 10 seconds before next deployment...")
        time.sleep(10)
        print()
    
    print("=" * 60)
    print(f"Deployment Summary:")
    print(f"  ✅ Successful: {success_count}")
    print(f"  ❌ Failed: {failed_count}")
    print("=" * 60)
    print()
    print("⏳ Waiting 60 seconds for services to start...")
    print("Then check: https://api.bizoholic.net/health")

if __name__ == "__main__":
    main()
