import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def update_domain(domain_data):
    domain_id = domain_data['domainId']
    print(f"Updating domain {domain_id} to enable HTTPS...")
    url = f"{BASE_URL}/domain.update?batch=1"
    payload = {
        "0": {
            "json": {
                "domainId": domain_id,
                "host": domain_data['host'],
                "path": domain_data['path'],
                "port": domain_data['port'],
                "serviceName": domain_data['serviceName'],
                "https": True,
                "certificateType": "letsencrypt"
            }
        }
    }
    resp = requests.post(url, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp.status_code == 200:
        print(f"  Successfully updated domain {domain_id}")
    else:
        print(f"  Failed to update domain {domain_id}: {resp.text}")

# Get domain IDs from compose.one or list them
def fix_domains(compose_id):
    url_one = f"{BASE_URL}/compose.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22composeId%22%3A%22{compose_id}%22%7D%7D%7D"
    resp = requests.get(url_one, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        domains = resp.json()[0]['result']['data']['json'].get('domains', [])
        for d in domains:
            update_domain(d)

fix_domains("zLqTvD03_ThlZKYpSyUUf") # Authentik
fix_domains("osD7Up5T4VcZzok5yLyXo") # Vault
