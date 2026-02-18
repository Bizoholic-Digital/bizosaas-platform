import requests
import json

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"
CORE_ID = "CbM3L2Z3LJemaumOC6Yd4"
POSTIZ_ID = "EYKt_rt5nqcBHTpD25633"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    print("🚀 Triggering Final Deployments...")
    res_c = call_trpc("compose.deploy", {"composeId": CORE_ID})
    print(f"  Core Deploy Result: {json.dumps(res_c)}")
    
    res_p = call_trpc("compose.deploy", {"composeId": POSTIZ_ID})
    print(f"  Postiz Deploy Result: {json.dumps(res_p)}")
