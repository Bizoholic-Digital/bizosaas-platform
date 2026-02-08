import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

configs = [
    {
        "name": "Wagtail CMS",
        "composeId": "IqBW7qKCwSKw0UYBiaf7c",
        "serviceName": "wagtail-cms",
        "port": 8000,
        "domains": ["wagtail.bizoholic.net"],
        "env": """DATABASE_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/wagtail_db?sslmode=require
REDIS_URL=redis://bizosaas-redis:6379/2
SECRET_KEY=wagtail-secret-key-production
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1,wagtail-cms,wagtail.bizoholic.net,*.bizosaas.local"""
    },
    {
        "name": "SEO Panel",
        "composeId": "-ShbMgQjuEzlKOl28uXtX",
        "serviceName": "seopanel-app",
        "port": 80,
        "domains": ["seo.bizoholic.net"],
        "env": """MYSQL_ROOT_PASSWORD=BizOSaaS2025@StagingDB
MYSQL_DATABASE=seopanel
MYSQL_USER=seopanel
MYSQL_PASSWORD=BizOSaaS2025@StagingDB
DB_HOST=seopanel-db
DB_USER=seopanel
DB_PASS=BizOSaaS2025@StagingDB
DB_NAME=seopanel"""
    }
]

def configure_service(config):
    print(f"🔧 Configuring {config['name']}...")
    
    # 1. Update Environment Variables
    update_url = f"{BASE_URL}/compose.update"
    payload = {
        "composeId": config['composeId'],
        "env": config['env']
    }
    try:
        response = requests.post(update_url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"✅ Updated Environment Variables")
    except Exception as e:
        print(f"❌ Failed to update env: {e}")
        if hasattr(e, 'response') and e.response: print(e.response.text)

    # 2. Add Domains
    # Note: Using domain.create endpoint assumption. If fails, we might need to check API docs or project details structure.
    # Based on observation, domain creation might be separate.
    # Let's try to find existing domains first to avoid duplicate? 
    # For now, just try to create.
    domain_create_url = f"{BASE_URL}/domain.create"
    
    for domain in config['domains']:
        domain_payload = {
            "composeId": config['composeId'],
            "host": domain,
            "port": config['port'],
            "serviceName": config['serviceName'],
            "https": True,
            "path": "/"
        }
        try:
            response = requests.post(domain_create_url, headers=headers, json=domain_payload)
            response.raise_for_status()
            print(f"✅ Assigned Domain: {domain}")
        except Exception as e:
            print(f"❌ Failed to assign domain {domain}: {e}")
            if hasattr(e, 'response') and e.response: print(e.response.text)

if __name__ == "__main__":
    for c in configs:
        configure_service(c)
