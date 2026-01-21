import requests
import json

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

# 1. Update Client Portal Domain Port (from 3003 to 3000)
print("Updating Client Portal domain...")
res = call_trpc("domain.update", {
    "domainId": "pCAIaf75bVnavDpFQwbfd",
    "port": 3000
})
print("Result Client Portal:", res)

# 2. Add Vault Domain
# applicationId: xFPHD7N1DMPeqqzjYAqlC
print("Adding Vault domain...")
res = call_trpc("domain.create", {
    "applicationId": "xFPHD7N1DMPeqqzjYAqlC",
    "host": "vault.bizoholic.net",
    "port": 8200,
    "https": True,
    "certificateType": "letsencrypt",
    "path": "/",
    "internalPath": "/"
})
print("Result Vault:", res)

# 3. Add Admin Dashboard Domain
print("Adding Admin Dashboard domain...")
res = call_trpc("domain.create", {
    "composeId": "NlDPTf6BZgSQilinf2YaU",
    "host": "admin.bizoholic.net",
    "port": 3000,
    "https": True,
    "certificateType": "letsencrypt",
    "serviceName": "admin-dashboard",
    "path": "/",
    "internalPath": "/"
})
print("Result Admin:", res)

# 4. Add Business Directory Domain
print("Adding Business Directory domain...")
res = call_trpc("domain.create", {
    "composeId": "jRJrq-UIekuq6XBaDOhh6",
    "host": "directory.bizoholic.net",
    "port": 3005,
    "https": True,
    "certificateType": "letsencrypt",
    "serviceName": "business-directory",
    "path": "/",
    "internalPath": "/"
})
print("Result Directory:", res)

# 5. Add Billing Domain (Lago Front)
print("Adding Billing Front domain...")
res = call_trpc("domain.create", {
    "composeId": "cbgmdr52hGC7XrA53Cw7z",
    "host": "billing.bizoholic.net",
    "port": 80,
    "https": True,
    "certificateType": "letsencrypt",
    "serviceName": "lago-front",
    "path": "/",
    "internalPath": "/"
})
print("Result Billing Front:", res)

# 6. Add Billing API Domain (Lago API)
print("Adding Billing API domain...")
res = call_trpc("domain.create", {
    "composeId": "cbgmdr52hGC7XrA53Cw7z",
    "host": "billing-api.bizoholic.net",
    "port": 3000,
    "https": True,
    "certificateType": "letsencrypt",
    "serviceName": "lago-api",
    "path": "/",
    "internalPath": "/"
})
print("Result Billing API:", res)
