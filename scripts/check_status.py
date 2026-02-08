import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
COMPOSE_ID = "IqBW7qKCwSKw0UYBiaf7c" # Wagtail

def check_status():
    print(f"🔍 Checking status for Compose ID: {COMPOSE_ID}")
    try:
        url = f"{BASE_URL}/compose.one?composeId={COMPOSE_ID}"
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        data = res.json()
        print("\n📂 Compose Details:")
        print(f"Name: {data.get('name')}")
        print(f"AppName: {data.get('appName')}")
        print(f"Domains: {json.dumps(data.get('domains', []), indent=2)}")
    except Exception as e:
        print(f"❌ Failed to get compose details: {e}")

    try:
        url = f"{BASE_URL}/compose.deployments?composeId={COMPOSE_ID}"
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        deployments = res.json()
        if deployments:
            latest = deployments[0]
            print("\n🚀 Latest Deployment:")
            print(f"ID: {latest.get('deploymentId')}")
            print(f"Status: {latest.get('deploymentStatus')}")
            print(f"Created At: {latest.get('createdAt')}")
        else:
            print("\n⚠️ No deployments found.")
    except Exception as e:
        print(f"❌ Failed to get deployments: {e}")

if __name__ == "__main__":
    check_status()
