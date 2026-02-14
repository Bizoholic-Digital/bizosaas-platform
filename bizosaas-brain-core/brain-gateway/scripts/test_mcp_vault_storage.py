import asyncio
import os
import sys
from uuid import UUID

# Add parent directory to path
sys.path.append(os.getcwd())

from app.dependencies import SessionLocal
from app.services.mcp_installation_service import McpInstallationService
from app.models.mcp import UserMcpInstallation, McpRegistry
from app.adapters.vault_adapter import VaultAdapter

async def test_secure_installation():
    db = SessionLocal()
    user_id = "test-user-123"
    mcp_slug = "wordpress"
    
    # Sample config with secrets
    config = {
        "site_url": "https://test-wp.com",
        "username": "admin",
        "api_key": "wp-app-pass-xyz-123", # Sensitive
        "secret_token": "highly-secret-key" # Sensitive
    }
    
    print(f"--- Starting Secure Installation Test for {mcp_slug} ---")
    
    try:
        # 1. Ensure MCP exists in registry for testing
        mcp = db.query(McpRegistry).filter(McpRegistry.slug == mcp_slug).first()
        if not mcp:
            print(f"Adding mock MCP {mcp_slug} for test")
            from app.models.mcp import McpCategory
            cat = db.query(McpCategory).first()
            mcp = McpRegistry(
                name="WordPress",
                slug=mcp_slug,
                category_id=cat.id,
                mcp_config={"type": "standard"}
            )
            db.add(mcp)
            db.commit()

        # 2. Perform installation
        print("Installing MCP via McpInstallationService...")
        installation = await McpInstallationService.install_with_vault(
            db=db,
            user_id=user_id,
            mcp_slug=mcp_slug,
            config=config
        )
        
        print(f"Installation Success! ID: {installation.id}")
        print(f"Public Config in DB: {installation.config}")
        print(f"Credentials Path: {installation.credentials_path}")
        
        # Verify secrets are NOT in DB
        assert "api_key" not in installation.config
        assert "secret_token" not in installation.config
        print("✅ Success: Secrets NOT found in database config.")
        
        # 3. Verify secrets ARE in Vault
        vault = VaultAdapter()
        vault_secrets = vault.get_secret_sync(installation.credentials_path)
        print(f"Retrieved from Vault: {vault_secrets}")
        
        assert vault_secrets["api_key"] == config["api_key"]
        assert vault_secrets["secret_token"] == config["secret_token"]
        print("✅ Success: Secrets correctly stored in Vault.")
        
        # 4. Test decryption helper
        full_config = McpInstallationService.get_decrypted_config(installation)
        assert full_config["api_key"] == config["api_key"]
        assert full_config["site_url"] == config["site_url"]
        print("✅ Success: Full config correctly reconstructed.")
        
        # Clean up
        db.delete(installation)
        db.commit()
        print("Test record cleaned up.")

    except Exception as e:
        print(f"❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure Vault env vars are set
    if not os.getenv("VAULT_ADDR") or not os.getenv("VAULT_TOKEN"):
        print("ERROR: VAULT_ADDR and VAULT_TOKEN must be set.")
        sys.exit(1)
        
    asyncio.run(test_secure_installation())
