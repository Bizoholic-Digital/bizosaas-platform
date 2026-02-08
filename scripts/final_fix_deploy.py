import requests
import json

API_KEY = "mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug"
BASE_URL = "https://dk.bizoholic.com/api"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

services = [
    {
        "name": "Wagtail CMS",
        "composeId": "IqBW7qKCwSKw0UYBiaf7c",
        "file": "docker-compose.wagtail-cms.yml",
        "env": """DATABASE_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/wagtail_db?sslmode=require
REDIS_URL=redis://bizosaas-redis:6379/2
SECRET_KEY=wagtail-secret-key-production
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1,wagtail-cms,wagtail.bizoholic.net,*.bizosaas.local"""
    },
    {
        "name": "SEO Panel",
        "composeId": "-ShbMgQjuEzlKOl28uXtX",
        "file": "docker-compose.seo-panel.yml",
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

def fix_service(service):
    print(f"🔧 Fixing {service['name']}...")
    payload_config = {
        "composeId": service['composeId'],
        "sourceType": "github",
        "repository": "bizosaas-platform",
        "owner": "Bizoholic-Digital",
        "branch": "staging-fix",
        "composePath": service['file']
    }
    
    try:
        with open(service['file'], 'r') as f:
            payload_config['composeFile'] = f.read()
    except:
        payload_config['composeFile'] = "ignored"

    try:
        res = requests.post(f"{BASE_URL}/compose.update", headers=HEADERS, json=payload_config)
        res.raise_for_status()
        print("    ✅ Config Updated")
    except Exception as e:
        print(f"    ❌ Config Update Failed: {e}")

    payload_env = {
        "composeId": service['composeId'],
        "env": service['env']
    }
    try:
        res = requests.post(f"{BASE_URL}/compose.update", headers=HEADERS, json=payload_env)
        res.raise_for_status()
        print("    ✅ Env Vars Set")
    except Exception as e:
        print(f"    ❌ Env Update Failed: {e}")

    try:
        res = requests.post(f"{BASE_URL}/compose.deploy", headers=HEADERS, json={"composeId": service['composeId']})
        res.raise_for_status()
        print("    ✅ Deployment Queued")
    except Exception as e:
        print(f"    ❌ Deploy Failed: {e}")

if __name__ == "__main__":
    for s in services:
        fix_service(s)
