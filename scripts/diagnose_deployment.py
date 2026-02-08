import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"

SERVICES = [
    ("sFHT3Oiep0z9UZmvby1QM", "Thrillring"),
    ("2hd_XXqQX_30pZFMOMb7k", "CMS")
]

def call_api(endpoint):
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

for cid, name in SERVICES:
    print(f"--- Diagnosing {name} ({cid}) ---")
    # Get Compose Details
    details = call_api(f"compose.one?composeId={cid}")
    path = details.get('composePath', 'UNKNOWN')
    print(f"Current Compose Path: {path}")
    
    # Try runtime logs
    print("Fetching runtime logs...")
    logs_res = call_api(f"compose.logs?composeId={cid}")
    # Inspect type
    if isinstance(logs_res, dict) and 'logs' in logs_res:
         print(logs_res['logs'][-1000:])
    elif isinstance(logs_res, str):
         print(logs_res[-1000:])
    else:
         print(json.dumps(logs_res, indent=2))
    
    # Get Deployments
    deployments = call_api(f"deployment.all?composeId={cid}")
    if isinstance(deployments, list) and len(deployments) > 0:
        last = deployments[0]
        did = last.get('deploymentId')
        status = last.get('status')
        print(f"Last Deployment: {did} ({status})")
        
        # Get Logs (or detailed deployment info)
        dep_details = call_api(f"deployment.one?deploymentId={did}")
        log = dep_details.get('log', '')
        # print last 500 chars of log
        print("Log tail:")
        print(log[-1000:] if log else "No logs")
    else:
        print("No deployments found.")
    print("\n")
