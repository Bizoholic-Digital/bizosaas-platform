#!/usr/bin/env python3
"""
Configure all BizOSaaS domains in Dokploy
"""
import requests
import json

DOKPLOY_URL = "http://localhost:3000"
API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"

# Service IDs from Dokploy
SERVICES = {
    "core-stack": "QiOdwXQi4ZQCM3Qg_KNcl",
    "vault": "1W8TCez-7vt661vt7-4Wn",
    "lago-stack": "cbgmdr52hGC7XrA53Cw7z",
    "client-portal": "zz6VpI3h8BFXPUTZZb01G",
    "admin-portal": "NlDPTf6BZgSQilinf2YaU",
    "business-directory": "jRJrq-UIekuq6XBaDOhh6"
}

# Domain configurations
DOMAINS = [
    {
        "service": "core-stack",
        "serviceName": "brain-gateway",
        "host": "api.bizoholic.net",
        "port": 8000,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    },
    {
        "service": "vault",
        "serviceName": "vault",
        "host": "vault.bizoholic.net",
        "port": 8200,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    },
    {
        "service": "lago-stack",
        "serviceName": "lago-front",
        "host": "billing.bizoholic.net",
        "port": 80,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    },
    {
        "service": "lago-stack",
        "serviceName": "lago-api",
        "host": "billing-api.bizoholic.net",
        "port": 3000,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    },
    {
        "service": "client-portal",
        "serviceName": "client-portal",
        "host": "app.bizoholic.net",
        "port": 3000,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    },
    {
        "service": "admin-portal",
        "serviceName": "admin-portal",
        "host": "admin.bizoholic.net",
        "port": 3000,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    },
    {
        "service": "business-directory",
        "serviceName": "business-directory",
        "host": "directory.bizoholic.net",
        "port": 3000,
        "path": "/",
        "https": True,
        "certificateType": "letsencrypt"
    }
]

def call_trpc(method, input_data):
    """Call Dokploy TRPC API"""
    url = f"{DOKPLOY_URL}/api/trpc/{method}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    payload = {"json": input_data}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error calling {method}: {response.status_code}")
        print(response.text)
        return None

def create_domain(domain_config):
    """Create a domain in Dokploy"""
    service_id = SERVICES.get(domain_config["service"])
    if not service_id:
        print(f"⚠️  Service ID not found for {domain_config['service']}")
        return None
    
    input_data = {
        "composeId": service_id,
        "host": domain_config["host"],
        "port": domain_config["port"],
        "path": domain_config["path"],
        "serviceName": domain_config["serviceName"],
        "https": domain_config["https"],
        "certificateType": domain_config["certificateType"]
    }
    
    print(f"Creating domain: {domain_config['host']} → {domain_config['serviceName']}:{domain_config['port']}")
    result = call_trpc("domain.create", input_data)
    
    if result:
        print(f"✅ Created: {domain_config['host']}")
        return result
    else:
        print(f"❌ Failed: {domain_config['host']}")
        return None

def main():
    print("=" * 60)
    print("Configuring BizOSaaS Domains in Dokploy")
    print("=" * 60)
    print()
    
    for domain in DOMAINS:
        create_domain(domain)
        print()
    
    print("=" * 60)
    print("Domain configuration complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
