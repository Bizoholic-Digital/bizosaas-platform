import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# From credentials.md (already in my context)
client_id = "BJUxH0Y6o2jpCw8hXONlqASebaAE3HAc"
client_secret = "fvNY5hSSF9iHaw4e62OG0r9akKFhY42Q-gTXvImHgDeoROa0WubbW_G_wZUWyLK5"

print("Fetching Aura API Token...")
try:
    response = httpx.post(
        "https://api.neo4j.io/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    token = response.json()["access_token"]
    print("Token fetched successfully.")

    print("Fetching instances...")
    instances_resp = httpx.get(
        "https://api.neo4j.io/v1/instances",
        headers={"Authorization": f"Bearer {token}"}
    )
    instances_resp.raise_for_status()
    instances = instances_resp.json()["data"]
    
    if not instances:
        print("No instances found.")
    else:
        for inst in instances:
            print(f"Name: {inst.get('name')}")
            print(f"ID: {inst.get('id')}")
            print(f"Connection URL: {inst.get('connection_url')}")
            print(f"Status: {inst.get('status')}")
            print("-" * 20)

except Exception as e:
    print(f"ERROR: {e}")
    if hasattr(e, 'response'):
        print(f"Response: {e.response.text}")
