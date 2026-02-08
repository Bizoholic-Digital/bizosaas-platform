import requests
import json
import yaml
import sys
import os
import time

# Configuration
API_URL = "https://dk.bizoholic.com/api/trpc"
API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
COMPOSE_FILE = "docker-compose.authentik.yml"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def get_project_and_env():
    print("Fetching projects...")
    response = requests.get(f"{API_URL}/project.all", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching projects: {response.text}")
        sys.exit(1)
    
    data = response.json()
    projects = data.get('result', {}).get('data', {}).get('json', [])
    
    if not projects:
        print("No projects found.")
        sys.exit(1)
        
    # Prefer existing project or pick first
    target_project = projects[0]
    for p in projects:
        if "bizosaas" in p.get('name', '').lower() or "platform" in p.get('name', '').lower():
            target_project = p
            break
            
    project_id = target_project['projectId']
    project_name = target_project['name']
    
    # Get environment
    environments = target_project.get('environments', [])
    if not environments:
        print(f"No environments found in project {project_name}")
        sys.exit(1)
        
    env_id = environments[0]['environmentId']
    
    print(f"Using Project: {project_name} ({project_id})")
    print(f"Using Environment: {environments[0]['name']} ({env_id})")
    
    return project_id, env_id

def check_existing_service(project_id):
    print("Checking for existing 'authentik-sso' service...")
    # TRPC query format
    query = {"0": {"projectId": project_id}}
    encoded_query = json.dumps(query)
    
    response = requests.get(f"{API_URL}/compose.all?batch=1&input={encoded_query}", headers=headers)
    
    if response.status_code != 200:
        print(f"Error checking services: {response.text}")
        return None
        
    data = response.json()
    try:
        services = data[0]['result']['data']['json']
        for svc in services:
            if svc['appName'] == 'authentik-sso':
                return svc['composeId']
    except (IndexError, KeyError):
        pass
        
    return None

def remove_service(compose_id):
    print(f"Removing existing service {compose_id}...")
    payload = {"json": {"composeId": compose_id}}
    response = requests.post(f"{API_URL}/compose.remove", headers=headers, json=payload)
    if response.status_code == 200:
        print("Service removed successfully.")
        time.sleep(2)
    else:
        print(f"Error removing service: {response.text}")

def create_service(project_id, env_id):
    print("Creating new Authentik SSO service...")
    payload = {
        "json": {
            "name": "Authentik SSO",
            "appName": "authentik-sso",
            "description": "Enterprise SSO (Self-Hosted)",
            "composeType": "docker-compose",
            "sourceType": "raw",
            "projectId": project_id,
            "environmentId": env_id
        }
    }
    
    response = requests.post(f"{API_URL}/compose.create", headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error creating service: {response.text}")
        sys.exit(1)
        
    data = response.json()
    try:
        compose_id = data['result']['data']['json']['composeId']
        print(f"Service created with ID: {compose_id}")
        return compose_id
    except KeyError:
        print(f"Unexpected response format: {data}")
        sys.exit(1)

def upload_compose(compose_id):
    print(f"Reading {COMPOSE_FILE}...")
    try:
        with open(COMPOSE_FILE, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File {COMPOSE_FILE} not found!")
        sys.exit(1)
        
    print("Uploading configuration...")
    payload = {
        "json": {
            "composeId": compose_id,
            "composeFile": content,
            "sourceType": "raw"
        }
    }
    
    response = requests.post(f"{API_URL}/compose.update", headers=headers, json=payload)
    if response.status_code == 200:
        print("Configuration uploaded successfully.")
    else:
        print(f"Error uploading config: {response.text}")
        sys.exit(1)

def deploy_service(compose_id):
    print("Triggering deployment...")
    payload = {
        "json": {
            "composeId": compose_id
        }
    }
    
    response = requests.post(f"{API_URL}/compose.deploy", headers=headers, json=payload)
    if response.status_code == 200:
        print("Deployment triggered successfully! 🚀")
        print("\nNext Steps:")
        print("1. Wait ~2 minutes for deployment")
        print("2. Check logs: docker logs -f authentik-server")
        print("3. Acces UI: https://sso.bizoholic.net/if/flow/initial-setup/")
    else:
        print(f"Error triggering deployment: {response.text}")
        sys.exit(1)

def main():
    print("=== Authentik Deployment Script ===")
    project_id, env_id = get_project_and_env()
    
    existing_id = check_existing_service(project_id)
    if existing_id:
        remove_service(existing_id)
        
    compose_id = create_service(project_id, env_id)
    upload_compose(compose_id)
    deploy_service(compose_id)

if __name__ == "__main__":
    main()
