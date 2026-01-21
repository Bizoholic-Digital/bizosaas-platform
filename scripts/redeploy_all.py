import requests
import json
import time

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "http://194.238.16.237:3000/api/trpc"

def call_trpc(endpoint, data):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json={"json": data}, headers=headers)
    return response.json()

stacks = {
    "core-stack": "QiOdwXQi4ZQCM3Qg_KNcl",
    "client-portal": "zz6VpI3h8BFXPUTZZb01G",
    "admin-portal": "NlDPTf6BZgSQilinf2YaU",
    "business-directory": "jRJrq-UIekuq6XBaDOhh6",
    "lago-stack": "cbgmdr52hGC7XrA53Cw7z"
}

for name, stack_id in stacks.items():
    print(f"Deploying {name} ({stack_id})...")
    res = call_trpc("compose.deploy", {"composeId": stack_id})
    print(f"Result {name}: {res}")
    time.sleep(2) # Give it some time
