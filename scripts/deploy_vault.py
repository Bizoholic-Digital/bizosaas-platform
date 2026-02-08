import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

COMPOSE_FILE = """
services:
  vault:
    image: hashicorp/vault:latest
    cap_add:
      - IPC_LOCK
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=staging-root-token-bizosaas-2025
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: [ "CMD-SHELL", "VAULT_ADDR=http://127.0.0.1:8200 vault status" ]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M

networks:
  dokploy-network:
    external: true
    name: dokploy-network
"""

def deploy_vault():
    compose_id = "osD7Up5T4VcZzok5yLyXo"
    print(f"Updating Vault ({compose_id})...")
    
    url_update = f"{BASE_URL}/compose.update?batch=1"
    payload = {
        "0": {
            "json": {
                "composeId": compose_id,
                "composeFile": COMPOSE_FILE
            }
        }
    }
    
    resp = requests.post(url_update, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print("Vault updated successfully")
    else:
        print(f"Failed to update Vault: {resp.text}")
        
    # Deploy
    url_deploy = f"{BASE_URL}/compose.deploy?batch=1"
    requests.post(url_deploy, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    print("Vault deployment triggered")

if __name__ == "__main__":
    deploy_vault()
