import httpx
import sys
import json
from datetime import datetime, timedelta

def generate_token():
    base_url = "https://auth-sso.bizoholic.net/api/v3"
    auth = ("akadmin", "Bizoholic2025!Admin")
    
    print(f"Connecting to {base_url}...")
    
    with httpx.Client(auth=auth, timeout=30.0) as client:
        # 1. Get akadmin user PK
        print("Fetching akadmin user profile...")
        try:
            resp = client.get(f"{base_url}/core/users/?username=akadmin")
            if resp.status_code != 200:
                print(f"Failed to fetch user: {resp.status_code} - {resp.text}")
                return
            
            results = resp.json().get("results", [])
            if not results:
                print("No user found with username akadmin")
                return
            
            user_pk = results[0]["pk"]
            print(f"Found akadmin PK: {user_pk}")
            
            # 2. Create a new token
            print("Creating new API token...")
            identifier = f"brain-gateway-token-{int(datetime.now().timestamp())}"
            token_data = {
                "identifier": identifier,
                "intent": "api",
                "user": user_pk,
                "expiring": False # Long-lived token
            }
            
            resp = client.post(f"{base_url}/core/tokens/", json=token_data)
            if resp.status_code != 201:
                print(f"Failed to create token: {resp.status_code} - {resp.text}")
                return
            
            token_obj = resp.json()
            # In Authentik, the actual token string is often in 'key' or requires 'view_key'
            # Let's see what we got.
            print(f"Token created successfully: {token_obj.get('identifier')}")
            
            # The token value is usually only shown once or requires a separate call
            # For identifier-based tokens, it might be in 'key'
            actual_token = token_obj.get("key")
            if actual_token:
                print(f"AUTHENTIK_API_TOKEN={actual_token}")
            else:
                print("Token key not in response. Attempting to retrieve token key...")
                # Try to get the key explicitly if it exists
                resp = client.get(f"{base_url}/core/tokens/{identifier}/view_key/")
                if resp.status_code == 200:
                   key_val = resp.json().get("key")
                   print(f"AUTHENTIK_API_TOKEN={key_val}")
                else:
                   print(f"Could not retrieve key: {resp.status_code} - {resp.text}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    generate_token()
