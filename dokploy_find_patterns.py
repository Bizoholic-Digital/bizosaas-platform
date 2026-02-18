import requests
import json
import urllib.parse

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    import urllib.parse
    input_data = {"json": data if data else {}}
    query_str = urllib.parse.quote(json.dumps(input_data))
    url = f"{url}?input={query_str}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

if __name__ == "__main__":
    print("🔍 Searching for ANY raw compose service patterns...")
    projects_res = call_trpc("project.all")
    projects = projects_res.get("result", {}).get("data", {}).get("json", [])
    
    for proj in projects:
        proj_id = proj["projectId"]
        env_res = call_trpc("environment.all", {"projectId": proj_id})
        envs = env_res.get("result", {}).get("data", {}).get("json", [])
        for env in envs:
            env_id = env["environmentId"]
            comp_res = call_trpc("compose.all", {"environmentId": env_id})
            composes = comp_res.get("result", {}).get("data", {}).get("json", [])
            for c in composes:
                if c.get("sourceType") == "raw":
                    print(f"  ✨ FOUND RAW PATTERN in {proj['name']} / {env['name']}: {c['name']}")
                    print(json.dumps(c, indent=2))
                else:
                    print(f"  - {proj['name']} / {env['name']}: {c['name']} (source: {c.get('sourceType')})")

    print("\n✅ Search completed.")
