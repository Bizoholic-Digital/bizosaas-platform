import requests
import json
import time

TOKENS = {
    "billing": "napi_4oxbdh3kp44d9w3ula4t317v0ibct98itxfjayo5qole30fnduwj01vf9xivdq7i",
    "core": "napi_y043x8lntqvfwo0s7tkhj1ddqrgld0z75xcyk4d799t0sqx3smcp52e64qdhptps",
    "social": "napi_6itv94txjfctr8v8zblhgcmb0sv5wfzgaaq4b5ic05na3837pi642d7y6xpfwbjl"
}

BASE_URL = "https://api.neon.tech/api/v2"

def call_neon(token, endpoint, method="GET", data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    url = f"{BASE_URL}/{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=headers, verify=False)
    else:
        response = requests.post(url, headers=headers, json=data, verify=False)
    
    try:
        return response.json()
    except:
        return response.text

def setup_account(name, token):
    print(f"🚀 Setting up Neon Account for {name}...")
    
    # 1. Check existing projects
    projects = call_neon(token, "projects")
    if isinstance(projects, dict) and projects.get("projects"):
        project = projects["projects"][0]
        print(f"  ✅ Found existing project: {project['id']}")
    else:
        # 2. Create new project
        print(f"  ✨ Creating new project: bizosaas-{name}...")
        res = call_neon(token, "projects", method="POST", data={"project": {"name": f"bizosaas-{name}"}})
        if "project" in res:
            project = res["project"]
            print(f"  ✅ Created project: {project['id']}")
        else:
            print(f"  ❌ Failed to create project: {res}")
            return None

    # 3. Wait for endpoints if needed
    proj_id = project["id"]
    for _ in range(10):
        endpoints = call_neon(token, f"projects/{proj_id}/endpoints")
        if isinstance(endpoints, dict) and endpoints.get("endpoints"):
            ep = endpoints["endpoints"][0]
            host = ep["host"]
            print(f"  🔗 Host: {host}")
            
            # 4. Get connection information
            # Neon typically creates a 'neondb' database by default.
            # We need the user and password.
            # We can get them from the 'roles' and 'passwords' endpoints.
            roles = call_neon(token, f"projects/{proj_id}/roles")
            if isinstance(roles, dict) and roles.get("roles"):
                role = roles["roles"][0]
                user = role["name"]
                
                # Get password for the role
                pw_res = call_neon(token, f"projects/{proj_id}/roles/{user}/reveal_password")
                password = pw_res.get("password")
                
                conn_str = f"postgresql://{user}:{password}@{host}/neondb?sslmode=require"
                print(f"  📍 Connection String: {conn_str}")
                return conn_str
        
        print("  ⏳ Waiting for endpoint...")
        time.sleep(2)
    
    return None

if __name__ == "__main__":
    results = {}
    for name, token in TOKENS.items():
        results[name] = setup_account(name, token)
        print("-" * 40)
    
    with open("neon_setup_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n🎉 Setup Complete. Results saved to neon_setup_results.json")
