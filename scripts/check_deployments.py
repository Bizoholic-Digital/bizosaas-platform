import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_deployments(compose_id):
    url = f"{BASE_URL}/deployment.allByComposeId?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22composeId%22%3A%22{compose_id}%22%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        data = resp.json()
        print(f"Deployments for {compose_id}:")
        try:
            deployments = data[0]['result']['data']['json']
            for d in deployments[:5]: # Last 5
                print(f"  ID: {d.get('deploymentId')} | Status: {d.get('status')} | Created: {d.get('createdAt')}")
        except Exception as e:
            print(f"  Error parsing response: {e}")
            print(data)
    else:
        print(f"Failed to get deployments for {compose_id}: {resp.status_code} {resp.text}")

# Authentik
get_deployments("zLqTvD03_ThlZKYpSyUUf")
# Vault
get_deployments("osD7Up5T4VcZzok5yLyXo")
