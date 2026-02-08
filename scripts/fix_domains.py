import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

services = [
    {
        "name": "Wagtail CMS",
        "composeId": "IqBW7qKCwSKw0UYBiaf7c",
        "serviceName": "wagtail-cms",
        "port": 8000,
        "domain": "wagtail.bizoholic.net"
    },
    {
        "name": "SEO Panel",
        "composeId": "-ShbMgQjuEzlKOl28uXtX",
        "serviceName": "seopanel-app",
        "port": 80,
        "domain": "seo.bizoholic.net"
    }
]

def fix_domain(service):
    print(f"🔧 Fixing domain for {service['name']}...")
    
    # 1. Get current domains to find ID
    try:
        res = requests.get(f"{BASE_URL}/compose.one?composeId={service['composeId']}", headers=HEADERS)
        res.raise_for_status()
        data = res.json()
        current_domains = data.get('domains', [])
    except Exception as e:
        print(f"❌ Failed to get details: {e}")
        return

    # 2. Delete existing target domain
    for d in current_domains:
        if d['host'] == service['domain']:
            print(f"  - Deleting existing domain: {d['host']} (ID: {d['domainId']})")
            try:
                # Assuming domain.delete takes domainId
                # Payload might be { "domainId": "..." } or url parameter
                # Trying POST with body
                res = requests.post(f"{BASE_URL}/domain.delete", headers=HEADERS, json={"domainId": d['domainId'], "composeId": service['composeId']})
                if res.status_code != 200:
                   print(f"    ⚠️ Delete failed (Status {res.status_code}): {res.text}")
                else:
                   print("    ✅ Deleted")
            except Exception as e:
                print(f"    ❌ Delete error: {e}")

    # 3. Create new domain with LetsEncrypt
    print(f"  - Creating new domain: {service['domain']} with LetsEncrypt")
    payload = {
        "composeId": service['composeId'],
        "host": service['domain'],
        "port": service['port'],
        "serviceName": service['serviceName'],
        "https": True,
        "path": "/",
        "certificateType": "letsencrypt" 
    }
    try:
        res = requests.post(f"{BASE_URL}/domain.create", headers=HEADERS, json=payload)
        res.raise_for_status()
        print("    ✅ Created")
    except Exception as e:
        print(f"    ❌ Create error: {e}")
        if hasattr(e, 'response') and e.response: print(e.response.text)

    # 4. Trigger Deploy to apply
    print(f"  - Triggering Deployment...")
    try:
        res = requests.post(f"{BASE_URL}/compose.deploy", headers=HEADERS, json={"composeId": service['composeId']})
        res.raise_for_status()
        print("    ✅ Deployment Queued")
    except Exception as e:
        print(f"    ❌ Deploy error: {e}")

if __name__ == "__main__":
    for s in services:
        fix_domain(s)
