import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def start_compose(compose_id):
    print(f"Starting {compose_id}...")
    url = f"{BASE_URL}/compose.start?batch=1"
    payload = {"0": {"json": {"composeId": compose_id}}}
    resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"  Successfully started {compose_id}")
    else:
        print(f"  Failed to start {compose_id}: {resp.text}")

# Authentik
start_compose("zLqTvD03_ThlZKYpSyUUf")
# Vault
start_compose("osD7Up5T4VcZzok5yLyXo")
