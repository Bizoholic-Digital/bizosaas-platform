import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

def get_latest_deployment(compose_id):
    # Try different procedure name
    url = f"{BASE_URL}/deployment.all?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22composeId%22%3A%22{compose_id}%22%7D%7D%7D"
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        try:
            deployments = resp.json()[0]['result']['data']['json']
            if deployments:
                return deployments[0]
        except:
            pass
    return None

def get_logs(deployment_id):
    url = f"{BASE_URL}/deployment.getLogs?batch=1&input=%7B%220%22%3A%7B%22json%22%3B%7B%22deploymentId%22%3A%22{deployment_id}%22%7D%7D%7D"
    # Wait, the semicolon in URL above is a typo, fixing to colon
    url = url.replace(';', ':')
    resp = requests.get(url, headers={"x-api-key": API_KEY})
    if resp.status_code == 200:
        try:
            return resp.json()[0]['result']['data']['json']
        except:
            pass
    return None

def check_service(compose_id, name):
    print(f"Checking {name} ({compose_id})...")
    dep = get_latest_deployment(compose_id)
    if dep:
        print(f"  Latest Deployment: {dep.get('deploymentId')} | Status: {dep.get('status')}")
        logs = get_logs(dep.get('deploymentId'))
        if logs:
            print("  --- Deployment Logs (Last 10 lines) ---")
            lines = logs.split('\n')
            for line in lines[-10:]:
                print(f"    {line}")
        else:
            print("  No logs found for deployment.")
    else:
        print("  No deployments found.")

check_service("zLqTvD03_ThlZKYpSyUUf", "Authentik")
check_service("osD7Up5T4VcZzok5yLyXo", "Vault")
