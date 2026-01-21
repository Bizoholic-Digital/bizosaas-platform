import hvac
import os
import time

# Configuration
VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "staging-root-token-bizosaas-2025")

def seed_vault():
    print(f"Connecting to Vault at {VAULT_ADDR}...")
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    
    if not client.is_authenticated():
        print("Authentication failed!")
        return

    print("Authenticated successfully.")

    # Enable kv-v2 secrets engine at 'bizosaas'
    engines = client.sys.list_mounted_secrets_engines()
    if "bizosaas/" not in engines:
        print("Enabling 'bizosaas' kv-v2 secrets engine...")
        client.sys.enable_secrets_engine(backend_type="kv", path="bizosaas", options={"version": "2"})
    else:
        print("'bizosaas' engine already enabled.")

    # Secrets Data
    bg_secrets = {
        "OPENAI_API_KEY": "sk-proj-placeholder",
        "ANTHROPIC_API_KEY": "sk-ant-placeholder",
        "GOOGLE_API_KEY": "AIzaSy-placeholder",
        "JWT_SECRET": "vdMxrD6bZpZk6lClpkSP56+WNapkPAG5lY+BojEA/u7ffehUKcVL7re6xRaPWUCZffoxXF9ZFuU+KcZSWpz6CA==",
        "DATABASE_URL": "postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require",
        "REDIS_URL": "redis://default:Gt7QxXA4ybMzYzD9e6KIBULfnv1IU6f9@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0"
    }

    clerk_secrets = {
        "publishable_key": "pk_test_placeholder",
        "secret_key": "sk_test_placeholder"
    }

    # Write Secrets
    print("Writing secrets to bizosaas/data/platform/brain-gateway...")
    client.secrets.kv.v2.create_or_update_secret(
        path="platform/brain-gateway",
        mount_point="bizosaas",
        secret=bg_secrets
    )

    print("Writing secrets to bizosaas/data/clerk...")
    client.secrets.kv.v2.create_or_update_secret(
        path="clerk",
        mount_point="bizosaas",
        secret=clerk_secrets
    )
    
    print("Vault seeding complete!")

if __name__ == "__main__":
    seed_vault()
