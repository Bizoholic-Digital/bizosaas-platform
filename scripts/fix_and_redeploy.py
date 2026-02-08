import requests
import json
import time

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def update_and_deploy(compose_id, file_path=None, content=None):
    if file_path:
        with open(file_path, 'r') as f:
            content = f.read()
    
    print(f"Updating configuration for {compose_id}...")
    url_update = f"{BASE_URL}/compose.update?batch=1"
    payload = {
        "0": {
            "json": {
                "composeId": compose_id,
                "composeFile": content,
                "sourceType": "raw"
            }
        }
    }
    
    resp = requests.post(url_update, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"Successfully updated {compose_id}")
    else:
        print(f"Failed to update {compose_id}: {resp.text}")
        return

    print(f"Triggering deployment for {compose_id}...")
    url_deploy = f"{BASE_URL}/compose.deploy?batch=1"
    resp = requests.post(url_deploy, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"Deployment triggered for {compose_id}")
    else:
        print(f"Failed to trigger deployment for {compose_id}: {resp.text}")

# Authentik Service Configuration
AUTHENTIK_ID = "zLqTvD03_ThlZKYpSyUUf"

# Vault Service Configuration
VAULT_ID = "osD7Up5T4VcZzok5yLyXo"
VAULT_COMPOSE = """
services:
  vault:
    image: hashicorp/vault:latest
    cap_add:
      - IPC_LOCK
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=staging-root-token-bizosaas-2025
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    ports:
      - "8200"
    volumes:
      - vault-data:/vault/file
    command: server -dev -dev-root-token-id=staging-root-token-bizosaas-2025 -dev-listen-address=0.0.0.0:8200
    networks:
      - dokploy-network
    restart: unless-stopped
    healthcheck:
      test: [ "CMD", "vault", "status", "-address=http://127.0.0.1:8200" ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M

volumes:
  vault-data:

networks:
  dokploy-network:
    external: true
    name: dokploy-network
"""

print("Starting Fix and Redeploy...")
update_and_deploy(AUTHENTIK_ID, file_path="docker-compose.authentik.yml")
update_and_deploy(VAULT_ID, content=VAULT_COMPOSE)
print("Done.")
