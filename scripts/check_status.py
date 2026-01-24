import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_status(compose_id):
    url = f"{BASE_URL}/compose.one?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22composeId%22%3A%22{compose_id}%22%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        data = resp.json()
        print(f"Status for {compose_id}:")
        # Extract the information we need
        try:
            compose_data = data[0]['result']['data']['json']
            print(f"  Name: {compose_data.get('name')}")
            print(f"  Status: {compose_data.get('status')}")
            # Check domains
            domains = compose_data.get('domains', [])
            print(f"  Domains: {len(domains)}")
            for d in domains:
                print(f"    - {d.get('name')}: {d.get('host')}:{d.get('port')} (SSL: {d.get('certificateType')})")
        except Exception as e:
            print(f"  Error parsing response: {e}")
            print(data)
    else:
        print(f"Failed to get status for {compose_id}: {resp.status_code} {resp.text}")

# Authentik
get_status("zLqTvD03_ThlZKYpSyUUf")
# Vault
get_status("osD7Up5T4VcZzok5yLyXo")
