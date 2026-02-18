import requests
import json

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data, method="GET"):
    if method == "GET":
        import urllib.parse
        input_data = {"json": data}
        query_str = urllib.parse.quote(json.dumps(input_data))
        url = f"{BASE_URL}/{endpoint}?input={query_str}"
        response = requests.get(url, headers=HEADERS)
    else:
        url = f"{BASE_URL}/{endpoint}"
        payload = {"json": data}
        response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    core_id = "PW095Z8RFCzSdZ1bxha97"
    postiz_id = "bYH9mTmaYnWXg7wv2-MoI"
    
    print(f"--- Inspecting Core Stack ({core_id}) ---")
    core_res = call_trpc("compose.one", {"composeId": core_id})
    print(json.dumps(core_res, indent=2))
    
    print(f"\n--- Inspecting Postiz Stack ({postiz_id}) ---")
    postiz_res = call_trpc("compose.one", {"composeId": postiz_id})
    print(json.dumps(postiz_res, indent=2))
