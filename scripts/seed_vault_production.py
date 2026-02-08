import hvac
import os
import sys

# Vault Configuration
VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "staging-root-token-bizosaas-2025")
MOUNT_POINT = "bizosaas"

def seed_production_vault():
    print(f"Connecting to Vault at {VAULT_ADDR}...")
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
    
    if not client.is_authenticated():
        print("Authentication failed!")
        return

    print("Authenticated successfully.")

    # Enable kv-v2 secrets engine at 'bizosaas' if not exists
    engines = client.sys.list_mounted_secrets_engines()
    if f"{MOUNT_POINT}/" not in engines:
        print(f"Enabling '{MOUNT_POINT}' kv-v2 secrets engine...")
        client.sys.enable_secrets_engine(backend_type="kv", path=MOUNT_POINT, options={"version": "2"})
    else:
        print(f"'{MOUNT_POINT}' engine already enabled.")

    # 1. Platform Secrets: Brain Gateway
    bg_secrets = {
        "DATABASE_URL": os.environ.get("GATEWAY_DATABASE_URL", ""),
        "REDIS_URL": os.environ.get("REDIS_URL", ""),
        "JWT_SECRET": os.environ.get("JWT_SECRET", ""),
        "TEMPORAL_HOST": os.environ.get("TEMPORAL_HOST", ""),
        "GITHUB_TOKEN": os.environ.get("GH_TOKEN", "")
    }
    
    # 2. Platform Secrets: Admin Dashboard
    admin_secrets = {
        "NEXTAUTH_SECRET": os.environ.get("NEXTAUTH_SECRET", ""),
        "AUTHENTIK_CLIENT_ID": os.environ.get("AUTHENTIK_CLIENT_ID", ""),
        "AUTHENTIK_CLIENT_SECRET": os.environ.get("AUTHENTIK_CLIENT_SECRET", "")
    }
    
    # 3. Platform Secrets: Client Portal
    client_secrets = {
        "NEXTAUTH_SECRET": os.environ.get("NEXTAUTH_SECRET", ""),
        "AUTHENTIK_CLIENT_ID": os.environ.get("AUTHENTIK_CLIENT_ID", ""),
        "AUTHENTIK_CLIENT_SECRET": os.environ.get("AUTHENTIK_CLIENT_SECRET", "")
    }
    
    # 4. Infrastructure Secrets
    infra_secrets = {
        "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "REDIS_PASSWORD": os.environ.get("REDIS_PASSWORD", "")
    }
    
    # 5. Integration Secrets
    integrations = {
        "openai": {"OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "")},
        "anthropic": {"ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "")},
        "google": {"GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY", "")},
        "openrouter": {"OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY", "")},
        "clerk": {
            "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY": os.environ.get("CLERK_PUBLISHABLE_KEY", ""),
            "CLERK_SECRET_KEY": os.environ.get("CLERK_SECRET_KEY", "")
        },
        "stripe": {"STRIPE_SECRET_KEY": os.environ.get("STRIPE_SECRET_KEY", "")}
    }

    # Write Secrets
    print("Writing platform secrets...")
    client.secrets.kv.v2.create_or_update_secret(path="platform/brain-gateway", mount_point=MOUNT_POINT, secret=bg_secrets)
    client.secrets.kv.v2.create_or_update_secret(path="platform/admin-dashboard", mount_point=MOUNT_POINT, secret=admin_secrets)
    client.secrets.kv.v2.create_or_update_secret(path="platform/client-portal", mount_point=MOUNT_POINT, secret=client_secrets)
    client.secrets.kv.v2.create_or_update_secret(path="platform/infrastructure", mount_point=MOUNT_POINT, secret=infra_secrets)

    print("Writing integration secrets...")
    for name, data in integrations.items():
        client.secrets.kv.v2.create_or_update_secret(path=f"integrations/{name}", mount_point=MOUNT_POINT, secret=data)

    print("Vault seeding complete!")

if __name__ == "__main__":
    seed_production_vault()
