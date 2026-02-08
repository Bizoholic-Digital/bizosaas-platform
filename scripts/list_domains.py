import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_all_domains():
    # Procedure might be domain.all
    url = f"{BASE_URL}/domain.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        data = resp.json()
        print("All Domains:")
        try:
            domains = data[0]['result']['data']['json']
            for d in domains:
                print(f"  Host: {d.get('host')} | Port: {d.get('port')} | SSL: {d.get('certificateType')} | https: {d.get('https')}")
        except Exception as e:
            # print(f"  Error: {e}")
            # print(data)
            pass
    else:
        print(f"Failed: {resp.status_code} {resp.text}")

get_all_domains()
