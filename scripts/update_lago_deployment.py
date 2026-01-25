import requests
import json
import sys
import time

# Configuration
API_URL = "https://dk.bizoholic.com/api/trpc"
API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
COMPOSE_FILE = "docker-compose.lago.yml"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def get_project_id():
    print("Fetching projects...")
    response = requests.get(f"{API_URL}/project.all", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching projects: {response.text}")
        sys.exit(1)
    
    data = response.json()
    try:
        # Assuming the first project is the target, as per previous scripts
        project = data['result']['data']['json'][0]
        return project['projectId']
    except (KeyError, IndexError):
        print("Could not find valid project in response")
        sys.exit(1)

def find_lago_service(project_id):
    print("Searching for Lago service...")
    query = {"0": {"projectId": project_id}}
    encoded_query = json.dumps(query)
    
    response = requests.get(f"{API_URL}/compose.all?batch=1&input={encoded_query}", headers=headers)
    
    if response.status_code != 200:
        print(f"Error checking services: {response.text}")
        sys.exit(1)
        
    data = response.json()
    try:
        services = data[0]['result']['data']['json']
        for svc in services:
            if "lago" in svc['appName'].lower():
                print(f"Found Lago service: {svc['appName']} ({svc['composeId']})")
                return svc['composeId']
    except (IndexError, KeyError):
        print("Error parsing service list")
        
    print("Lago service not found via API")
    return None

def update_compose(compose_id):
    print(f"Reading {COMPOSE_FILE}...")
    try:
        with open(COMPOSE_FILE, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File {COMPOSE_FILE} not found!")
        sys.exit(1)
        
    print("Uploading updated configuration...")
    payload = {
        "json": {
            "composeId": compose_id,
            "composeFile": content,
            "sourceType": "raw"
        }
    }
    
    response = requests.post(f"{API_URL}/compose.update", headers=headers, json=payload)
    if response.status_code == 200:
        print("Configuration updated successfully.")
    else:
        print(f"Error uploading config: {response.text}")
        sys.exit(1)

def redeploy_service(compose_id):
    print("Triggering deployment...")
    payload = {
        "json": {
            "composeId": compose_id
        }
    }
    
    response = requests.post(f"{API_URL}/compose.deploy", headers=headers, json=payload)
    if response.status_code == 200:
        print("Deployment triggered successfully! 🚀")
    else:
        print(f"Error triggering deployment: {response.text}")
        sys.exit(1)

def main():
    # project_id = get_project_id()
    # compose_id = find_lago_service(project_id)
    
    # Manual ID from investigation
    compose_id = "gV4VNE43cna6LM7BGTYnn"
    
    if compose_id:
        update_compose(compose_id)
        redeploy_service(compose_id)
    else:
        print("Could not update Lago deployment - Service not found")

if __name__ == "__main__":
    main()
