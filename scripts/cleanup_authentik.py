import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def delete_service(compose_id):
    url = f"{BASE_URL}/compose.delete?batch=1"
    payload = {"0": {"json": {"composeId": compose_id}}}
    resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    print(f"Deleted {compose_id}: {resp.status_code}")

# IDs found in turn 5006 and 5046
ids_to_delete = ["8cVDmdOdkh14ipfBtA7ZT", "gBz-keh6WjFQ2zlgg95oQ", "IwCFsJnynd94Nstbv6qy6"]

for cid in ids_to_delete:
    delete_service(cid)
