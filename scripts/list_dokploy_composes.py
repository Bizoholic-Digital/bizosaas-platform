import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"

def call_api(endpoint):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    print(f"Calling: {url}")
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    try:
        return response.json()
    except:
        return response.text


print("Fetching projects...")
res = call_api("project.all")

if isinstance(res, dict) and 'result' in res: # Trpc style? No, REST usually returns raw json or {data: ...}
    # Handling potential TRPC style or standard REST
    data = res.get('result', {}).get('data', {}).get('json', [])
    if not data and isinstance(res, list): 
        data = res
elif isinstance(res, list):
    data = res
else:
    data = []


if data and len(data) > 0:
    # Check environments
    envs = data[0].get('environments', [])
    if envs and len(envs) > 0:
        pass

target_id = "2hd_XXqQX_30pZFMOMb7k"
print(f"Fetching details for {target_id}...")
res = call_api(f"compose.one?composeId={target_id}")
print(json.dumps(res, indent=2))
