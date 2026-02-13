import os
import hvac
from dotenv import load_dotenv

# Load local .env
load_dotenv()

VAULT_ADDR = os.getenv("VAULT_ADDR", "https://vault.bizoholic.net")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
MOUNT_POINT = "secret"
SECRET_PATH = "bizosaas/gateway/config"

secrets_to_migrate = [
    "OPENAI_API_KEY",
    "SERPAPI_API_KEY",
    "PAGESPEED_API_KEY",
    "TEMPORAL_API_KEY",
    "REDIS_URL",
    "DATABASE_URL",
    "POSTIZ_API_KEY",
    "CMS_WAGTAIL_API_TOKEN",
    "CMS_WORDPRESS_PASSWORD"
]

data = {}
for key in secrets_to_migrate:
    val = os.getenv(key)
    if val:
        data[key] = val
        print(f"Prepared {key}")

if not data:
    print("No secrets found to migrate.")
    exit(0)

client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
if not client.is_authenticated():
    print("Vault authentication failed!")
    exit(1)

try:
    client.secrets.kv.v2.create_or_update_secret(
        path=SECRET_PATH,
        secret=data,
        mount_point=MOUNT_POINT
    )
    print(f"Successfully migrated {len(data)} secrets to Vault at {MOUNT_POINT}/{SECRET_PATH}")
except Exception as e:
    print(f"Error migrating to Vault: {e}")
