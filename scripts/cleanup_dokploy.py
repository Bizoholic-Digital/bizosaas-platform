import requests
import json
import sys

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def delete_compose(compose_id):
    print(f"Deleting {compose_id}...")
    url = f"{BASE_URL}/compose.delete?batch=1"
    payload = {"0": {"json": {"composeId": compose_id, "deleteVolumes": False}}}
    resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"Successfully deleted {compose_id}")
    else:
        print(f"Failed to delete {compose_id}: {resp.text}")

# Specific IDs to cleanup
ids_to_delete = ["8cVDmdOdkh14ipfBtA7ZT", "gBz-keh6WjFQ2zlgg95oQ", "1W8TCez-7vt661vt7-4Wn", "IwCFsJnynd94Nstbv6qy6"]

for cid in ids_to_delete:
    delete_compose(cid)
