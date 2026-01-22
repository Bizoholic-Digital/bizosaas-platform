import requests
import os

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "http://localhost:3000/api/trpc"

STACKS = {
    "core-stack": {"id": "QiOdwXQi4ZQCM3Qg_KNcl", "file": "docker-compose.core.yml"},
    "lago-stack": {"id": "cbgmdr52hGC7XrA53Cw7z", "file": "docker-compose.lago.yml"},
    "client-portal": {"id": "zz6VpI3h8BFXPUTZZb01G", "file": "docker-compose.client-portal.yml"},
    "admin-portal": {"id": "NlDPTf6BZgSQilinf2YaU", "file": "docker-compose.admin-portal.yml"},
    "business-directory": {"id": "jRJrq-UIekuq6XBaDOhh6", "file": "docker-compose.directory.yml"},
    "vault": {"id": "1W8TCez-7vt661vt7-4Wn", "file": "docker-compose.vault.yml"}
}

def call_trpc(endpoint, data):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json={"json": data}, headers=headers)
    return response.json()

def main():
    print("Updating Dokploy Compose configurations...")
    repo_path = "/root/bizosaas-platform"
    
    for name, config in STACKS.items():
        file_path = os.path.join(repo_path, config["file"])
        if not os.path.exists(file_path):
            print(f"Skipping {name}: File not found at {file_path}")
            continue
            
        print(f"Reading {config['file']}...")
        with open(file_path, "r") as f:
            content = f.read()
            
        print(f"Updating {name} ({config['id']})...")
        # Verify inputs for compose.update
        # Usually takes composeId and composeFile
        data = {
            "composeId": config["id"],
            "composeFile": content
        }
        
        res = call_trpc("compose.update", data)
        print(f"Update Result: {res}")
        
        # After update, we deploy
        print(f"Deploying {name}...")
        res = call_trpc("compose.deploy", {"composeId": config["id"]})
        print(f"Deploy Result: {res}")
        print("-" * 40)

if __name__ == "__main__":
    main()
