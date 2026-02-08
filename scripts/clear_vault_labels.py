import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "http://localhost:3000/api/trpc"

def call_trpc(endpoint, data):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json={"json": data}, headers=headers)
    return response.json()

app_id = "xFPHD7N1DMPeqqzjYAqlC"

# Clear manual swarm labels
payload = {
    "applicationId": app_id,
    "labelsSwarm": {} # Empty map
}

print("Clearing Vault Application Labels...")
res = call_trpc("application.update", payload)
print("Result:", res)

print("Redeploying Vault...")
res = call_trpc("application.deploy", {"applicationId": app_id})
print("Result:", res)
