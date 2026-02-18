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
    # 1. Postiz (pltjdr) -> EYKt_rt5nqcBHTpD25633
    # Need to make sure DATABASE_URL is also mapped to POSTIZ_DATABASE_URL
    print("\n📦 Updating Postiz Stack (pltjdr) Env...")
    postiz_env = """# Postiz Stack Env
DATABASE_URL=postgresql://neondb_owner:npg_YzVhMI0qHfb2@ep-green-feather-aiuo1vhb-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
POSTIZ_DATABASE_URL=postgresql://neondb_owner:npg_YzVhMI0qHfb2@ep-green-feather-aiuo1vhb-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
TEMPORAL_ADDRESS=ap-south-2.aws.api.temporal.io:7233
TEMPORAL_NAMESPACE=bizosaas-platform-mtls.mdqxv
MAIN_URL=https://postiz.bizoholic.net
FRONTEND_URL=https://postiz.bizoholic.net
NEXT_PUBLIC_BACKEND_URL=https://postiz.bizoholic.net/api
POSTIZ_JWT_SECRET=iyQ+Z0egmGAHdkBEsGPe5+u78WcDj0OWniocepqvQvc=
"""
    call_trpc("compose.update", {"composeId": "EYKt_rt5nqcBHTpD25633", "env": postiz_env})
    
    # 2. Core (sot3ld) -> CbM3L2Z3LJemaumOC6Yd4
    print("📦 Updating Core Stack (sot3ld) Env...")
    core_env = """# Core Stack Env
DATABASE_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-shy-night-a13tnr7n-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
TEMPORAL_ADDRESS=ap-south-2.aws.api.temporal.io:7233
TEMPORAL_NAMESPACE=bizosaas-platform-mtls.mdqxv
TEMPORAL_API_KEY=eyJhbGciOiJFUzI1NiIsICJraWQiOiJXdnR3YUEifQ.eyJhY2NvdW50X2lkIjoibWRxeHYiLCAiYXVkIjpbInRlbXBvcmFsLmlvIl0sICJleHAiOjE4MzM5NDA1MDYsICJpc3MiOiJ0ZW1wb3JhbC5pbyIsICJqdGkiOiJZOHNoczRyYlJCNzN0R1NnUUV1dzJvZEdyeEI5ZjRoZSIsICJrZXlfaWQiOiJZOHNoczRyYlJCNzN0R1NnUUV1dzJvZEdyeEI5ZjRoZSIsICJzdWIiOiI0ZWU0YmExNjM2OGY0YWExOTQzNTNlOGEyODZhZWEyNiJ9.w167BDlyIAL_1wKMsrzlmkBw5FsWbZIRLoryP_eG2T1KcAXnE7VLm86PU4U-EAEtkMY_579SMwzt3ya9kJqO_g
VAULT_TOKEN=staging-root-token-bizosaas-2025
VAULT_URL=http://brain-vault:8200
OPENAI_API_KEY=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
ANTHROPIC_API_KEY=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
GITHUB_TOKEN=ac740acd740032bc16dcf4147c96bff89d2d680e
POSTIZ_API_URL=https://postiz.bizoholic.net/api
"""
    call_trpc("compose.update", {"composeId": "CbM3L2Z3LJemaumOC6Yd4", "env": core_env})
    
    print("\n🚀 Final Redeployment Trigger...")
    call_trpc("compose.redeploy", {"composeId": "CbM3L2Z3LJemaumOC6Yd4"})
    call_trpc("compose.redeploy", {"composeId": "EYKt_rt5nqcBHTpD25633"})
    
    print("✅ Configuration alignment and redeployment triggered.")
