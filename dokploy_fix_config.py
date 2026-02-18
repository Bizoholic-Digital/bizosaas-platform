import requests
import json
import urllib.parse

API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
BASE_URL = "https://dk.bizoholic.com/api/trpc"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def call_trpc(endpoint, data=None, method="POST"):
    url = f"{BASE_URL}/{endpoint}"
    if method == "GET":
        input_str = json.dumps({"json": data if data else {}}, separators=(',', ':'))
        query_str = urllib.parse.quote(input_str)
        url = f"{url}?input={query_str}"
        response = requests.get(url, headers=HEADERS)
    else:
        payload = {"json": data if data else {}}
        response = requests.post(url, headers=HEADERS, json=payload)
    
    try:
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🔧 Fixing Deployment Issues\n")
    
    # 1. Switch Core-Stack back to GitHub mode with correct path
    print("📦 Reconfiguring Core-Stack to use GitHub...")
    core_update = call_trpc("compose.update", {
        "composeId": "CbM3L2Z3LJemaumOC6Yd4",
        "sourceType": "github",
        "repository": "bizosaas-platform",
        "owner": "Bizoholic-Digital",
        "branch": "staging",
        "composePath": "infrastructure/compose/docker-compose.core-stack.yml"
    })
    print(f"  Result: {core_update.get('result', {}).get('data', {}).get('json', {}).get('sourceType')}")
    
    # 2. Switch Postiz-Stack back to GitHub mode
    print("\n📦 Reconfiguring Postiz-Stack to use GitHub...")
    postiz_update = call_trpc("compose.update", {
        "composeId": "EYKt_rt5nqcBHTpD25633",
        "sourceType": "github",
        "repository": "bizosaas-platform",
        "owner": "Bizoholic-Digital",
        "branch": "staging",
        "composePath": "docker-compose.postiz.yml"
    })
    print(f"  Result: {postiz_update.get('result', {}).get('data', {}).get('json', {}).get('sourceType')}")
    
    # 3. Update Postiz env vars to use correct names (without POSTIZ_ prefix for the ones Docker Compose expects)
    print("\n📦 Updating Postiz environment variables...")
    postiz_env = """# Postiz Stack Env
DATABASE_URL=postgresql://neondb_owner:npg_YzVhMI0qHfb2@ep-green-feather-aiuo1vhb-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
POSTIZ_DATABASE_URL=postgresql://neondb_owner:npg_YzVhMI0qHfb2@ep-green-feather-aiuo1vhb-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
TEMPORAL_ADDRESS=ap-south-2.aws.api.temporal.io:7233
TEMPORAL_NAMESPACE=bizosaas-platform-mtls.mdqxv
TEMPORAL_API_KEY=eyJhbGciOiJFUzI1NiIsICJraWQiOiJXdnR3YUEifQ.eyJhY2NvdW50X2lkIjoibWRxeHYiLCAiYXVkIjpbInRlbXBvcmFsLmlvIl0sICJleHAiOjE4MzM5NDA1MDYsICJpc3MiOiJ0ZW1wb3JhbC5pbyIsICJqdGkiOiJZOHNoczRyYlJCNzN0R1NnUUV1dzJvZEdyeEI5ZjRoZSIsICJrZXlfaWQiOiJZOHNoczRyYlJCNzN0R1NnUUV1dzJvZEdyeEI5ZjRoZSIsICJzdWIiOiI0ZWU0YmExNjM2OGY0YWExOTQzNTNlOGEyODZhZWEyNiJ9.w167BDlyIAL_1wKMsrzlmkBw5FsWbZIRLoryP_eG2T1KcAXnE7VLm86PU4U-EAEtkMY_579SMwzt3ya9kJqO_g
OPENAI_API_KEY=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
POSTIZ_JWT_SECRET=iyQ+Z0egmGAHdkBEsGPe5+u78WcDj0OWniocepqvQvc=
POSTIZ_AUTHENTIK_CLIENT_ID=your_client_id_here
POSTIZ_AUTHENTIK_CLIENT_SECRET=your_client_secret_here
MAIN_URL=https://postiz.bizoholic.net
FRONTEND_URL=https://postiz.bizoholic.net
NEXT_PUBLIC_BACKEND_URL=https://postiz.bizoholic.net/api
"""
    call_trpc("compose.update", {"composeId": "EYKt_rt5nqcBHTpD25633", "env": postiz_env})
    
    print("\n✅ Configuration updated. Ready to redeploy after cleaning up old containers.")
    print("\n⚠️  MANUAL STEP REQUIRED:")
    print("    Run on server: docker rm -f postiz-app 19dcfac165e3")
    print("    Then trigger redeployment via Dokploy UI or API")
