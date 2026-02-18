import requests
import json
import urllib3

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKENS = {
    "acc1": "napi_4oxbdh3kp44d9w3ula4t317v0ibct98itxfjayo5qole30fnduwj01vf9xivdq7i",
    "acc2": "napi_y043x8lntqvfwo0s7tkhj1ddqrgld0z75xcyk4d799t0sqx3smcp52e64qdhptps",
    "acc3": "napi_6itv94txjfctr8v8zblhgcmb0sv5wfzgaaq4b5ic05na3837pi642d7y6xpfwbjl"
}

BASE_URL = "https://api.neon.tech/api/v2"

def call_neon(token, endpoint):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/{endpoint}"
    # Use verify=False to bypass SSL issues
    response = requests.get(url, headers=headers, verify=False)
    try:
        return response.json()
    except:
        return response.text

if __name__ == "__main__":
    for name, token in TOKENS.items():
        print(f"Checking Neon {name}...")
        projects = call_neon(token, "projects")
        with open(f"neon_{name}_projects.json", "w") as f:
            json.dump(projects, f, indent=2)
        
        # If there are projects, get connection strings
        if isinstance(projects, dict) and "projects" in projects and projects["projects"]:
            proj_id = projects["projects"][0]["id"]
            print(f"  Found project: {proj_id}. Fetching connection details...")
            details = call_neon(token, f"projects/{proj_id}")
            with open(f"neon_{name}_details.json", "w") as f:
                json.dump(details, f, indent=2)
            
            # Get connection strings (endpoints)
            endpoints = call_neon(token, f"projects/{proj_id}/endpoints")
            with open(f"neon_{name}_endpoints.json", "w") as f:
                json.dump(endpoints, f, indent=2)
