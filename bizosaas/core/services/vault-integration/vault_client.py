#!/usr/bin/env python3
"""
HashiCorp Vault Integration for BizoholicSaaS BYOK (Bring Your Own Key)
Secure credential management for AI agents and external service integrations
"""

import asyncio
import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import httpx
from pydantic import BaseModel, Field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CredentialType(str, Enum):
    """Types of credentials stored in Vault"""
    API_KEY = "api_key"
    OAUTH_TOKEN = "oauth_token" 
    DATABASE_PASSWORD = "database_password"
    JWT_SECRET = "jwt_secret"
    WEBHOOK_SECRET = "webhook_secret"
    ENCRYPTION_KEY = "encryption_key"
    AMAZON_SP_API = "amazon_sp_api"
    GOOGLE_ADS_API = "google_ads_api"
    FACEBOOK_ADS_API = "facebook_ads_api"
    OPENAI_API_KEY = "openai_api_key"

class CredentialRequest(BaseModel):
    """Request model for storing credentials"""
    credential_type: CredentialType
    service_name: str
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    data: Dict[str, Any]
    tags: List[str] = Field(default_factory=list)
    expires_at: Optional[datetime] = None

class VaultCredential(BaseModel):
    """Vault credential response model"""
    path: str
    credential_type: CredentialType
    service_name: str
    tenant_id: Optional[str]
    user_id: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime]

class HashiCorpVaultClient:
    """HashiCorp Vault client for BYOK credential management"""
    
    def __init__(self, vault_url: str = None, vault_token: str = None):
        self.vault_url = vault_url or os.getenv("VAULT_URL", "http://localhost:8200")
        self.vault_token = vault_token or os.getenv("VAULT_TOKEN", "root")  # Dev token
        self.mount_point = "bizosaas"
        self.client = httpx.AsyncClient(
            base_url=self.vault_url,
            headers={
                "X-Vault-Token": self.vault_token,
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    async def initialize_vault_engine(self):
        """Initialize KV v2 secret engine for BizoholicSaaS"""
        try:
            # Check if secret engine already exists
            response = await self.client.get("/v1/sys/mounts")
            mounts = response.json()
            
            if f"{self.mount_point}/" not in mounts.get("data", {}):
                # Create KV v2 secret engine
                payload = {
                    "type": "kv",
                    "options": {"version": "2"},
                    "description": "BizoholicSaaS BYOK Credential Storage"
                }
                
                response = await self.client.post(
                    f"/v1/sys/mounts/{self.mount_point}",
                    json=payload
                )
                
                if response.status_code in [200, 204]:
                    logger.info(f"Successfully created secret engine: {self.mount_point}")
                else:
                    logger.error(f"Failed to create secret engine: {response.text}")
                    
            else:
                logger.info(f"Secret engine {self.mount_point} already exists")
                
        except Exception as e:
            logger.error(f"Error initializing Vault engine: {e}")
    
    async def store_credential(self, credential: CredentialRequest) -> Dict[str, Any]:
        """Store credential securely in Vault with BYOK pattern"""
        try:
            # Build path based on tenant isolation
            if credential.tenant_id:
                path = f"{self.mount_point}/data/tenants/{credential.tenant_id}/{credential.service_name}/{credential.credential_type}"
            else:
                path = f"{self.mount_point}/data/global/{credential.service_name}/{credential.credential_type}"
            
            # Prepare metadata
            metadata = {
                "credential_type": credential.credential_type,
                "service_name": credential.service_name,
                "tenant_id": credential.tenant_id,
                "user_id": credential.user_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": credential.expires_at.isoformat() if credential.expires_at else None,
                "tags": credential.tags
            }
            
            # Store credential data
            payload = {
                "data": credential.data,
                "metadata": metadata
            }
            
            response = await self.client.post(f"/v1/{path}", json=payload)
            
            if response.status_code in [200, 204]:
                logger.info(f"Successfully stored credential: {path}")
                return {
                    "success": True,
                    "path": path,
                    "version": response.json().get("data", {}).get("version", 1)
                }
            else:
                logger.error(f"Failed to store credential: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error storing credential: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_credential(self, service_name: str, credential_type: CredentialType, tenant_id: str = None) -> Optional[Dict[str, Any]]:
        """Retrieve credential from Vault with tenant isolation"""
        try:
            # Build path based on tenant isolation
            if tenant_id:
                path = f"{self.mount_point}/data/tenants/{tenant_id}/{service_name}/{credential_type}"
            else:
                path = f"{self.mount_point}/data/global/{service_name}/{credential_type}"
            
            response = await self.client.get(f"/v1/{path}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "data": data["data"]["data"],
                    "metadata": data["data"]["metadata"],
                    "version": data["data"]["version"]
                }
            elif response.status_code == 404:
                logger.warning(f"Credential not found: {path}")
                return None
            else:
                logger.error(f"Failed to retrieve credential: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving credential: {e}")
            return None
    
    async def list_credentials(self, tenant_id: str = None, service_name: str = None) -> List[str]:
        """List available credentials with optional filtering"""
        try:
            if tenant_id and service_name:
                path = f"{self.mount_point}/metadata/tenants/{tenant_id}/{service_name}"
            elif tenant_id:
                path = f"{self.mount_point}/metadata/tenants/{tenant_id}"
            elif service_name:
                path = f"{self.mount_point}/metadata/global/{service_name}"
            else:
                path = f"{self.mount_point}/metadata"
            
            response = await self.client.get(f"/v1/{path}?list=true")
            
            if response.status_code == 200:
                return response.json().get("data", {}).get("keys", [])
            else:
                logger.error(f"Failed to list credentials: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error listing credentials: {e}")
            return []
    
    async def update_credential(self, service_name: str, credential_type: CredentialType, new_data: Dict[str, Any], tenant_id: str = None) -> Dict[str, Any]:
        """Update existing credential"""
        try:
            # Get current credential to preserve metadata
            current = await self.get_credential(service_name, credential_type, tenant_id)
            if not current:
                return {"success": False, "error": "Credential not found"}
            
            # Build path
            if tenant_id:
                path = f"{self.mount_point}/data/tenants/{tenant_id}/{service_name}/{credential_type}"
            else:
                path = f"{self.mount_point}/data/global/{service_name}/{credential_type}"
            
            # Update metadata
            metadata = current["metadata"]
            metadata["updated_at"] = datetime.now(timezone.utc).isoformat()
            
            payload = {
                "data": new_data,
                "metadata": metadata
            }
            
            response = await self.client.post(f"/v1/{path}", json=payload)
            
            if response.status_code in [200, 204]:
                logger.info(f"Successfully updated credential: {path}")
                return {
                    "success": True,
                    "path": path,
                    "version": response.json().get("data", {}).get("version", 1)
                }
            else:
                logger.error(f"Failed to update credential: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error updating credential: {e}")
            return {"success": False, "error": str(e)}
    
    async def delete_credential(self, service_name: str, credential_type: CredentialType, tenant_id: str = None) -> Dict[str, Any]:
        """Delete credential (soft delete - keeps versions)"""
        try:
            if tenant_id:
                path = f"{self.mount_point}/data/tenants/{tenant_id}/{service_name}/{credential_type}"
            else:
                path = f"{self.mount_point}/data/global/{service_name}/{credential_type}"
            
            response = await self.client.delete(f"/v1/{path}")
            
            if response.status_code in [200, 204]:
                logger.info(f"Successfully deleted credential: {path}")
                return {"success": True, "path": path}
            else:
                logger.error(f"Failed to delete credential: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error deleting credential: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_ai_agent_credentials(self, tenant_id: str, agent_name: str) -> Dict[str, Any]:
        """Get all credentials needed by a specific AI agent"""
        try:
            credentials = {}
            
            # Common AI service credentials
            ai_services = [
                ("openai", CredentialType.OPENAI_API_KEY),
                ("anthropic", CredentialType.API_KEY),
                ("google_ads", CredentialType.GOOGLE_ADS_API),
                ("facebook_ads", CredentialType.FACEBOOK_ADS_API),
                ("amazon_sp_api", CredentialType.AMAZON_SP_API)
            ]
            
            for service_name, cred_type in ai_services:
                cred = await self.get_credential(service_name, cred_type, tenant_id)
                if cred:
                    credentials[service_name] = cred["data"]
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error getting AI agent credentials: {e}")
            return {}
    
    async def rotate_credential(self, service_name: str, credential_type: CredentialType, new_data: Dict[str, Any], tenant_id: str = None) -> Dict[str, Any]:
        """Rotate credential with versioning support"""
        try:
            # Store new version
            result = await self.update_credential(service_name, credential_type, new_data, tenant_id)
            
            if result["success"]:
                logger.info(f"Successfully rotated credential: {service_name}/{credential_type}")
                
                # Schedule old version cleanup (could be implemented with Vault policies)
                # For now, just log the rotation
                logger.info(f"Credential rotation completed for {service_name}/{credential_type} - Version: {result['version']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error rotating credential: {e}")
            return {"success": False, "error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Vault health and connection"""
        try:
            response = await self.client.get("/v1/sys/health")
            health_data = response.json()
            
            return {
                "vault_healthy": not health_data.get("sealed", True),
                "vault_initialized": health_data.get("initialized", False),
                "vault_version": health_data.get("version", "unknown"),
                "cluster_id": health_data.get("cluster_id", "unknown"),
                "mount_point": self.mount_point,
                "connection_status": "connected"
            }
            
        except Exception as e:
            logger.error(f"Vault health check failed: {e}")
            return {
                "vault_healthy": False,
                "connection_status": "failed",
                "error": str(e)
            }
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

# Singleton instance for the application
vault_client = HashiCorpVaultClient()

async def get_vault_client() -> HashiCorpVaultClient:
    """Get configured Vault client instance"""
    return vault_client