import requests
import os
import time

# Use the internal docker network URL since they are in the same network
LAGO_URL = "http://lago-api:3000/api/v1/ping"
# Or potentially the public one if internal networking fails
# LAGO_URL = "https://billing-api.bizoholic.net/api/v1/ping"

print(f"Testing connectivity to Lago at {LAGO_URL}...")

try:
    response = requests.get(LAGO_URL, timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print("✅ SUCCESS: Connected to Lago!")
    else:
        print("❌ FAILURE: Non-200 response")
except Exception as e:
    print(f"❌ FAILURE: Could not connect. Error: {e}")
