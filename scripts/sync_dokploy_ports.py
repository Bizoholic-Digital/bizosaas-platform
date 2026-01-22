import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "http://194.238.16.237:3000/api/trpc"

def call_trpc(endpoint, data=None):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    if data is not None:
        response = requests.post(url, json={"json": data}, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    return response.json()

# 1. Fetch all domains
print("Fetching all domains...")
res = call_trpc("domain.all", {})
domains = res.get("result", {}).get("data", {}).get("json", [])

if not domains:
    print("No domains found or error in response.")
    print(res)
    exit(1)

# Mapping of hosts to desired ports
desired_ports = {
    "api.bizoholic.net": 8000,
    "admin.bizoholic.net": 3000,
    "app.bizoholic.net": 3000,
    "directory.bizoholic.net": 3000,
    "billing.bizoholic.net": 80,
    "billing-api.bizoholic.net": 3000,
    "vault.bizoholic.net": 8200
}

# 2. Update domains that don't match
for domain in domains:
    host = domain.get("host")
    current_port = domain.get("port")
    domain_id = domain.get("domainId")
    
    if host in desired_ports:
        target_port = desired_ports[host]
        if current_port != target_port:
            print(f"Updating {host}: {current_port} -> {target_port} (ID: {domain_id})")
            update_res = call_trpc("domain.update", {
                "domainId": domain_id,
                "port": target_port
            })
            print("Response:", update_res)
        else:
            print(f"OK: {host} is already on port {current_port}")
    else:
        print(f"Skipping unknown host: {host}")

print("\nCleaning up manual Traefik config files on server...")
