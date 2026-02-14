import logging
import os
from typing import Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.mcp import UserMcpInstallation, McpRegistry
from app.adapters.vault_adapter import VaultAdapter

logger = logging.getLogger(__name__)

class McpInstallationService:
    """
    Manages the secure installation of MCPs, ensuring sensitive credentials
    are stored in HashiCorp Vault instead of the main database.
    """
    
    # Fields considered sensitive and should be moved to Vault
    SENSITIVE_PATTERNS = [
        "api_key", "apikey", "password", "secret", "token", 
        "access_token", "refresh_token", "client_secret", "key",
        "private_key", "auth_token", "client_id", "cert", "db_pass"
    ]

    @classmethod
    def _is_sensitive(cls, key: str) -> bool:
        """Determines if a configuration key holds sensitive data."""
        k = key.lower()
        return any(pattern in k for pattern in cls.SENSITIVE_PATTERNS)

    @classmethod
    def segregate_credentials(cls, config: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Splits a configuration into public metadata and sensitive credentials.
        """
        public_config = {}
        sensitive_credentials = {}
        
        for k, v in config.items():
            if cls._is_sensitive(k):
                sensitive_credentials[k] = v
            else:
                public_config[k] = v
                
        return public_config, sensitive_credentials

    @classmethod
    async def install_with_vault(
        cls, 
        db: Session, 
        user_id: str, 
        mcp_slug: str, 
        config: Dict[str, Any]
    ) -> UserMcpInstallation:
        """
        Securely installs an MCP by storing credentials in Vault.
        """
        # 1. Fetch MCP
        mcp = db.query(McpRegistry).filter(McpRegistry.slug == mcp_slug).first()
        if not mcp:
            raise ValueError(f"MCP with slug '{mcp_slug}' not found")

        # 2. Segregate sensitive data
        public_config, secrets = cls.segregate_credentials(config)
        
        # 3. Create installation record
        installation = UserMcpInstallation(
            user_id=user_id,
            mcp_id=mcp.id,
            status="pending",
            config=public_config
        )
        
        # 4. Store secrets in Vault if any exist
        if secrets:
            mount_point = os.getenv("VAULT_MOUNT_POINT", "bizosaas")
            vault = VaultAdapter(mount_point=mount_point)
            
            # Path: tenants/{user_id}/connectors/{mcp_slug}
            # Note: Using user_id as tenant_id for now as per orchestrator convention
            vault_path = f"tenants/{user_id}/connectors/{mcp_slug}"
            
            logger.info(f"Storing secrets in Vault for user {user_id} at {vault_path}")
            success = vault.store_secret_sync(vault_path, secrets)
            
            if not success:
                logger.error(f"Failed to store secrets in Vault for {vault_path}")
                # We could raise an error here or proceed if Vault is optional (but it's not for us)
                raise RuntimeError("Vault storage failed. Cannot proceed with secure installation.")
                
            installation.credentials_path = vault_path

        db.add(installation)
        db.commit()
        db.refresh(installation)
        
        return installation

    @classmethod
    def get_decrypted_config(cls, installation: UserMcpInstallation) -> Dict[str, Any]:
        """
        Retrieves the full configuration (public + secrets) for an installation.
        Used by the orchestrator/agents.
        """
        full_config = (installation.config or {}).copy()
        
        if installation.credentials_path:
            mount_point = os.getenv("VAULT_MOUNT_POINT", "bizosaas")
            vault = VaultAdapter(mount_point=mount_point)
            
            secrets = vault.get_secret_sync(installation.credentials_path)
            if secrets:
                full_config.update(secrets)
            else:
                logger.warning(f"Could not retrieve secrets from Vault path: {installation.credentials_path}")
                
        return full_config
