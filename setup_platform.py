"""
BizOSaas Platform - Final Production Setup Script
Usage: python3 setup_platform.py

This script performs the final programmatic configuration of Dokploy services,
mapping the dedicated Neon DB connection strings to their respective stacks.
"""

import requests
import json
import os

# --- DOKPLOY CONFIG ---
DOKPLOY_API_KEY = "uQNgAbKuxBzqnOtsHjyWILZTbkPCbzLPxqTsFMbdrIDILQHnuGcHwlYmwarwKXpu"
DOKPLOY_BASE_URL = "https://dk.bizoholic.com/api/trpc"

CORE_SERVICE_ID = "CbM3L2Z3LJemaumOC6Yd4"
POSTIZ_SERVICE_ID = "EYKt_rt5nqcBHTpD25633"

HEADERS = {
    "x-api-key": DOKPLOY_API_KEY,
    "Content-Type": "application/json"
}

# --- NEON CONNECTION STRINGS (from credentials.md) ---
NEON_STRINGS = {
    "billing": "postgresql://neondb_owner:npg_YzTUuaJS9f6P@ep-dawn-firefly-ai3eotz2-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require",
    "core": "postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-shy-night-a13tnr7n-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require",
    "social": "postgresql://neondb_owner:npg_YzVhMI0qHfb2@ep-green-feather-aiuo1vhb-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
}

# --- HELPERS ---

def call_trpc(endpoint, data):
    url = f"{DOKPLOY_BASE_URL}/{endpoint}"
    payload = {"json": data}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def update_env(service_id, env_str):
    print(f"Update Environment Variables for service: {service_id}")
    return call_trpc("compose.update", {"composeId": service_id, "env": env_str})

def create_domain(service_id, host, port, service_name):
    print(f"🌐 mapping domain: {host} -> {service_name}:{port}")
    return call_trpc("domain.create", {
        "composeId": service_id,
        "host": host,
        "port": port,
        "serviceName": service_name,
        "certificateType": "letsencrypt",
        "https": True
    })

def deploy(service_id):
    print(f"🚀 Triggering Deployment for service: {service_id}")
    return call_trpc("compose.deploy", {"composeId": service_id})

# --- WORKFLOW ---

def run_final_migration():
    print("✨ Starting Final Infrastructure Migration Sync...")

    # 1. Update Core Stack (Brain Gateway + Agents)
    # Using Neon Account 2 (The user's 'alagirirajeshoutlook' account)
    core_env = f"""# Core Stack Env
DATABASE_URL={NEON_STRINGS['core']}
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
TEMPORAL_ADDRESS=ap-south-2.aws.api.temporal.io:7233
TEMPORAL_NAMESPACE=bizosaas-platform-mtls.mdqxv
TEMPORAL_API_KEY=eyJhbGciOiJFUzI1NiIsICJraWQiOiJXdnR3YUEifQ.eyJhY2NvdW50X2lkIjoibWRxeHYiLCAiYXVkIjpbInRlbXBvcmFsLmlvIl0sICJleHAiOjE4MzM5NDA1MDYsICJpc3MiOiJ0ZW1wb3JhbC5pbyIsICJqdGkiOiJZOHNoczRyYlJCNzN0R1NnUUV1dzJvZEdyeEI5ZjRoZSIsICJrZXlfaWQiOiJZOHNoczRyYlJCNzN0R1NnUUV1dzJvZEdyeEI5ZjRoZSIsICJzdWIiOiI0ZWU0YmExNjM2OGY0YWExOTQzNTNlOGEyODZhZWEyNiJ9.w167BDlyIAL_1wKMsrzlmkBw5FsWbZIRLoryP_eG2T1KcAXnE7VLm86PU4U-EAEtkMY_579SMwzt3ya9kJqO_g
VAULT_TOKEN=staging-root-token-bizosaas-2025
VAULT_URL=http://brain-vault:8200
OPENAI_API_KEY=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
ANTHROPIC_API_KEY=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
OPENROUTER_API_KEY=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
GITHUB_TOKEN=ac740acd740032bc16dcf4147c96bff89d2d680e
POSTIZ_API_URL=https://postiz.bizoholic.net/api
"""
    update_env(CORE_SERVICE_ID, core_env)
    create_domain(CORE_SERVICE_ID, "api.bizoholic.net", 8000, "brain-gateway")
    deploy(CORE_SERVICE_ID)

    # 2. Update Postiz Stack (Social)
    # Using Neon Account 3 (The user's 'bizo_com_digital' account)
    postiz_env = f"""# Postiz Stack Env
DATABASE_URL={NEON_STRINGS['social']}
REDIS_URL=redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0
TEMPORAL_ADDRESS=ap-south-2.aws.api.temporal.io:7233
TEMPORAL_NAMESPACE=bizosaas-platform-mtls.mdqxv
MAIN_URL=https://postiz.bizoholic.net
FRONTEND_URL=https://postiz.bizoholic.net
NEXT_PUBLIC_BACKEND_URL=https://postiz.bizoholic.net/api
"""
    update_env(POSTIZ_SERVICE_ID, postiz_env)
    create_domain(POSTIZ_SERVICE_ID, "postiz.bizoholic.net", 5000, "postiz-app")
    deploy(POSTIZ_SERVICE_ID)

    print("\n🏁 Programmatic Migration Complete. Check Dokploy for deployment status.")

if __name__ == "__main__":
    run_final_migration()
