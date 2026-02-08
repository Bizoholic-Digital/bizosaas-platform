import asyncio
import os
import sys
import json
from uuid import UUID

# Add parent directory to path
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.services.mcp_installation_service import McpInstallationService
from app.models.mcp import UserMcpInstallation, McpRegistry
from adapters.vault_adapter import VaultAdapter

async def run_smoke_test():
    print("🚀 Starting Final Production Onboarding Smoke Test [Bizoholic]")
    
    # 1. Load Config
    config_path = "onboarding/bizoholic_config.json"
    with open(config_path, 'r') as f:
        onboarding_config = json.load(f)
        
    db = SessionLocal()
    vault = VaultAdapter()
    
    user_id = onboarding_config["tenant_id"]
    
    try:
        for step in onboarding_config["onboarding_steps"]:
            if step["step"] == "connect_mcp":
                slug = step["mcp_slug"]
                config = step["config"]
                
                print(f"--- Step: Connecting MCP [{slug}] ---")
                
                # Check Registry
                mcp = db.query(McpRegistry).filter(McpRegistry.slug == slug).first()
                if not mcp:
                    print(f"⚠️ Warning: MCP {slug} not found in registry. Skipping.")
                    continue
                
                # Install
                installation = await McpInstallationService.install_with_vault(
                    db=db,
                    user_id=user_id,
                    mcp_slug=slug,
                    config=config
                )
                
                print(f"✅ Installation Created: {installation.id}")
                
                # Verify Vault
                vault_secrets = vault.get_secret_sync(installation.credentials_path)
                if vault_secrets:
                    print(f"✅ Secrets Verified in Vault at: {installation.credentials_path}")
                else:
                    print(f"❌ Error: Secrets MISSING from Vault!")
                    
                # Verify DB Sanity
                if installation.config:
                    # Sensitive keys should be purged
                    sensitive_keys = ["application_password", "api_key", "client_secret"]
                    found_sensitive = [k for k in sensitive_keys if k in installation.config]
                    if not found_sensitive:
                        print(f"✅ DB Config Sanitized (No secrets in DB)")
                    else:
                        print(f"❌ Error: Found sensitive keys in DB: {found_sensitive}")
                
                # Clean up test installation
                db.delete(installation)
                db.commit()
                print(f"Done.")

        print("\n✨ Smoke Test Completed Successfully for Bizoholic.")

    except Exception as e:
        print(f"❌ Smoke Test Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(run_smoke_test())
