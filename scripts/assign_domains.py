import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def add_domain_to_compose(compose_id, service_name, domain_name, port):
    print(f"Adding domain {domain_name} to {service_name} in {compose_id}...")
    url = f"{BASE_URL}/domain.create?batch=1"
    payload = {
        "0": {
            "json": {
                "name": domain_name,
                "host": domain_name,
                "port": port,
                "composeId": compose_id,
                "serviceName": service_name,
                "certificateType": "none"  # Use 'none' if Cloudflare proxy is on, or 'letsencrypt' if not
            }
        }
    }
    resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"Successfully assigned {domain_name}")
    else:
        print(f"Failed to assign {domain_name}: {resp.text}")

# Assign official domains via Dokploy API
# Authentik
add_domain_to_compose("zLqTvD03_ThlZKYpSyUUf", "authentik-server", "auth-sso.bizoholic.net", 9000)
add_domain_to_compose("zLqTvD03_ThlZKYpSyUUf", "authentik-server", "sso.bizoholic.net", 9000)

# Vault
add_domain_to_compose("osD7Up5T4VcZzok5yLyXo", "vault", "vault.bizoholic.net", 8200)
