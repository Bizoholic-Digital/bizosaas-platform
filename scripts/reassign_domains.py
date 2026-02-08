import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_service_data(compose_id):
    url = f"{BASE_URL}/compose.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22composeId%22%3A%22{compose_id}%22%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        return resp.json()[0]['result']['data']['json']
    return None

def delete_domain(domain_id):
    url = f"{BASE_URL}/domain.delete?batch=1"
    payload = {"0": {"json": {"domainId": domain_id}}}
    resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"  Deleted domain {domain_id}")
    else:
        print(f"  Failed to delete domain {domain_id}: {resp.text}")

def clean_and_reassign(compose_id, service_name, domains_list):
    print(f"Cleaning up {compose_id} ({service_name})...")
    data = get_service_data(compose_id)
    if not data:
        print(f"  Failed to get data for {compose_id}")
        return

    # Delete all existing domains
    existing_domains = data.get('domains', [])
    for d in existing_domains:
        delete_domain(d.get('domainId'))

    # Re-assign
    for domain, port in domains_list:
        print(f"  Assigning {domain}:{port} with letsencrypt...")
        url = f"{BASE_URL}/domain.create?batch=1"
        payload = {
            "0": {
                "json": {
                    "name": domain.replace('.', '-'),
                    "host": domain,
                    "port": port,
                    "composeId": compose_id,
                    "serviceName": service_name,
                    "certificateType": "letsencrypt"
                }
            }
        }
        resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
        if resp.status_code == 200:
            print(f"  Successfully assigned {domain}")
        else:
            print(f"  Failed to assign {domain}: {resp.text}")

# Authentik
clean_and_reassign("zLqTvD03_ThlZKYpSyUUf", "authentik-server", [
    ("auth-sso.bizoholic.net", 9000),
    ("sso.bizoholic.net", 9000)
])

# Vault
clean_and_reassign("osD7Up5T4VcZzok5yLyXo", "vault", [
    ("vault.bizoholic.net", 8200)
])
