import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

SERVICES = {
    "admin-portal": "NlDPTf6BZgSQilinf2YaU",
    "client-portal": "zz6VpI3h8BFXPUTZZb01G",
    "business-directory": "jRJrq-UIekuq6XBaDOhh6"
}

DOMAINS = {
    "admin-portal": "https://admin.bizoholic.net",
    "client-portal": "https://app.bizoholic.net",
    "business-directory": "https://directory.bizoholic.net"
}

AUTHENTIK_ISSUER = "https://auth-sso.bizoholic.net/application/o/bizosaas-platform/"
AUTHENTIK_ID = "bizosaas-portal"
AUTHENTIK_SECRET = "BizOSaaS2024!AuthentikSecret"

def update_env(compose_id, service_name):
    print(f"Updating {service_name} ({compose_id})...")
    
    # Get current env
    url_get = f"{BASE_URL}/compose.one?batch=1&input={json.dumps({'0': {'json': {'composeId': compose_id}}})}"
    resp = requests.get(url_get, headers={"x-api-key": API_KEY})
    data = resp.json()[0]['result']['data']['json']
    current_env = data.get('env', '')
    
    # Parse env
    env_lines = current_env.split('\n')
    new_env_lines = []
    
    # Keys to remove
    to_remove = ["NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY", "CLERK_SECRET_KEY"]
    
    for line in env_lines:
        line = line.strip()
        if not line: continue
        parts = line.split('=')
        k = parts[0]
        if k not in to_remove:
            new_env_lines.append(line)
            
    # Add new keys
    new_keys = {
        "AUTH_AUTHENTIK_ID": AUTHENTIK_ID,
        "NEXT_PUBLIC_AUTH_AUTHENTIK_ID": AUTHENTIK_ID,
        "AUTH_AUTHENTIK_SECRET": AUTHENTIK_SECRET,
        "AUTH_AUTHENTIK_ISSUER": AUTHENTIK_ISSUER,
        "NEXTAUTH_URL": DOMAINS[service_name],
        "AUTH_URL": DOMAINS[service_name],
        "NEXTAUTH_SECRET": "BizOSaaS2025!Secret!NextAuth",
        "AUTH_SECRET": "BizOSaaS2025!Secret!NextAuth",
        "AUTH_TRUST_HOST": "true",
        "AUTH_SUCCESS_URL": DOMAINS[service_name] + "/dashboard"
    }
    
    for k, v in new_keys.items():
        # Check if already exists, update or add
        found = False
        for i, line in enumerate(new_env_lines):
            if line.startswith(f"{k}="):
                new_env_lines[i] = f"{k}={v}"
                found = True
                break
        if not found:
            new_env_lines.append(f"{k}={v}")
            
    updated_env = '\n'.join(new_env_lines)
    
    # Update on Dokploy
    url_update = f"{BASE_URL}/compose.update?batch=1"
    payload = {
        "0": {
            "json": {
                "composeId": compose_id,
                "env": updated_env,
                "sourceType": "raw"
            }
        }
    }
    
    resp_up = requests.post(url_update, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp_up.status_code == 200:
        print(f"  Successfully updated env for {service_name}")
    else:
        print(f"  Failed to update env for {service_name}: {resp_up.text}")

    # Trigger redeploy
    url_redeploy = f"{BASE_URL}/compose.deploy?batch=1"
    resp_dep = requests.post(url_redeploy, headers={"x-api-key": API_KEY, "Content-Type": "application/json"}, json=payload)
    if resp_dep.status_code == 200:
        print(f"  Deployment triggered for {service_name}")
    else:
        print(f"  Failed to trigger deployment for {service_name}: {resp_dep.text}")

for name, cid in SERVICES.items():
    update_env(cid, name)
