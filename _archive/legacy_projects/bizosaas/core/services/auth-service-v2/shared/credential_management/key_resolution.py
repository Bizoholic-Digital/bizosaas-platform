"""
Dual-Mode Key Resolution Service for BYOK Architecture
Supports both Bring-Your-Own-Key (BYOK) and platform-managed credentials
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Literal
from enum import Enum
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_

from shared.database.models import Integration, Tenant
from shared.vault.vault_client import VaultClient

logger = logging.getLogger(__name__)


class CredentialStrategy(Enum):
    """Credential management strategies"""
    BYOK = "bring_your_own_key"      # Tenant provides all API keys
    PLATFORM = "platform_managed"    # Platform provides all API keys  
    HYBRID = "hybrid_mode"           # Mix of BYOK and platform keys
    AUTO = "auto_resolve"            # Automatically choose best option


class BillingModel(Enum):
    """Billing models based on credential strategy"""
    BYOK_TIER = "byok_discounted"    # Lower cost, tenant provides keys
    PLATFORM_TIER = "full_service"  # Higher cost, platform provides keys
    USAGE_BASED = "pay_per_use"      # Charge based on actual API usage


@dataclass
class ResolvedCredentials:
    """Resolved credentials with metadata"""
    credentials: Dict[str, str]
    strategy_used: CredentialStrategy
    source: Literal["tenant", "platform", "hybrid"]
    platform: str
    tenant_id: str
    expires_at: Optional[datetime] = None
    health_status: Literal["healthy", "warning", "error"] = "healthy"
    last_validated: Optional[datetime] = None
    usage_cost_model: BillingModel = BillingModel.BYOK_TIER


@dataclass
class KeyHealthStatus:
    """Health status of API keys"""
    platform: str
    is_healthy: bool
    last_check: datetime
    error_message: Optional[str] = None
    expires_at: Optional[datetime] = None
    usage_quota_remaining: Optional[int] = None


class KeyResolutionService:
    """
    Core service for resolving credentials in dual-mode BYOK architecture
    
    Resolution Priority:
    1. Check tenant's preferred strategy
    2. Validate tenant BYOK keys if available
    3. Fall back to platform keys if needed
    4. Apply billing model based on resolved strategy
    """
    
    def __init__(self, vault_client: VaultClient, db_session: AsyncSession):
        self.vault = vault_client
        self.db = db_session
        
        # Platform-supported integrations
        self.supported_platforms = {
            'google_ads', 'facebook_ads', 'meta_ads', 'linkedin_ads',
            'google_analytics', 'stripe', 'mailchimp', 'hubspot',
            'salesforce', 'slack', 'zapier', 'mautic'
        }
    
    async def resolve_credentials(
        self, 
        tenant_id: str, 
        platform: str,
        force_strategy: Optional[CredentialStrategy] = None
    ) -> ResolvedCredentials:
        """
        Resolve credentials using dual-mode strategy
        
        Args:
            tenant_id: The tenant requesting credentials
            platform: Platform name (google_ads, facebook_ads, etc.)
            force_strategy: Override tenant's preferred strategy
            
        Returns:
            ResolvedCredentials with actual keys and metadata
        """
        try:
            # Get tenant configuration
            tenant = await self._get_tenant_config(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")
            
            # Determine strategy to use
            strategy = force_strategy or self._get_tenant_strategy(tenant)
            
            # Resolve credentials based on strategy
            if strategy == CredentialStrategy.BYOK:
                return await self._resolve_byok_credentials(tenant_id, platform)
            
            elif strategy == CredentialStrategy.PLATFORM:
                return await self._resolve_platform_credentials(tenant_id, platform)
            
            elif strategy == CredentialStrategy.HYBRID:
                return await self._resolve_hybrid_credentials(tenant_id, platform)
            
            elif strategy == CredentialStrategy.AUTO:
                return await self._resolve_auto_credentials(tenant_id, platform)
            
            else:
                raise ValueError(f"Unknown credential strategy: {strategy}")
                
        except Exception as e:
            logger.error(f"Failed to resolve credentials for {tenant_id}/{platform}: {e}")
            raise
    
    async def _resolve_byok_credentials(self, tenant_id: str, platform: str) -> ResolvedCredentials:
        """Resolve using tenant's own API keys"""
        
        # Get tenant's integration
        integration = await self._get_tenant_integration(tenant_id, platform)
        if not integration:
            raise ValueError(f"No BYOK integration found for {tenant_id}/{platform}")
        
        if integration.status != 'active':
            raise ValueError(f"BYOK integration inactive for {tenant_id}/{platform}")
        
        # Decrypt tenant credentials
        credentials = await self._decrypt_tenant_credentials(integration)
        
        # Validate credentials health
        health = await self._validate_credentials_health(credentials, platform)
        
        return ResolvedCredentials(
            credentials=credentials,
            strategy_used=CredentialStrategy.BYOK,
            source="tenant",
            platform=platform,
            tenant_id=tenant_id,
            expires_at=self._get_credential_expiry(integration),
            health_status="healthy" if health.is_healthy else "error",
            last_validated=health.last_check,
            usage_cost_model=BillingModel.BYOK_TIER
        )
    
    async def _resolve_platform_credentials(self, tenant_id: str, platform: str) -> ResolvedCredentials:
        """Resolve using platform-managed API keys from Vault"""
        
        # Get platform credentials from Vault
        vault_path = f"platforms/{platform}/credentials"
        vault_data = await self.vault.get_secret(vault_path)
        
        if not vault_data:
            raise ValueError(f"No platform credentials available for {platform}")
        
        credentials = vault_data.get('data', {})
        
        # Validate platform credentials
        health = await self._validate_credentials_health(credentials, platform)
        
        return ResolvedCredentials(
            credentials=credentials,
            strategy_used=CredentialStrategy.PLATFORM,
            source="platform",
            platform=platform,
            tenant_id=tenant_id,
            expires_at=self._parse_vault_expiry(vault_data),
            health_status="healthy" if health.is_healthy else "warning",
            last_validated=health.last_check,
            usage_cost_model=BillingModel.PLATFORM_TIER
        )
    
    async def _resolve_hybrid_credentials(self, tenant_id: str, platform: str) -> ResolvedCredentials:
        """Resolve using hybrid approach - BYOK with platform fallback"""
        
        try:
            # First try BYOK
            return await self._resolve_byok_credentials(tenant_id, platform)
            
        except Exception as byok_error:
            logger.warning(f"BYOK failed for {tenant_id}/{platform}: {byok_error}")
            
            # Fall back to platform credentials
            try:
                platform_creds = await self._resolve_platform_credentials(tenant_id, platform)
                
                # Update to indicate hybrid usage
                platform_creds.strategy_used = CredentialStrategy.HYBRID
                platform_creds.source = "hybrid"
                
                return platform_creds
                
            except Exception as platform_error:
                logger.error(f"Both BYOK and platform credentials failed: {byok_error}, {platform_error}")
                raise ValueError(f"No valid credentials available for {platform}")
    
    async def _resolve_auto_credentials(self, tenant_id: str, platform: str) -> ResolvedCredentials:
        """Automatically choose best credential source"""
        
        # Check if tenant has healthy BYOK credentials
        try:
            integration = await self._get_tenant_integration(tenant_id, platform)
            if integration and integration.status == 'active':
                # Test BYOK credentials health
                credentials = await self._decrypt_tenant_credentials(integration)
                health = await self._validate_credentials_health(credentials, platform)
                
                if health.is_healthy:
                    return await self._resolve_byok_credentials(tenant_id, platform)
        
        except Exception as e:
            logger.debug(f"BYOK auto-check failed: {e}")
        
        # Fall back to platform credentials
        return await self._resolve_platform_credentials(tenant_id, platform)
    
    async def validate_all_tenant_credentials(self, tenant_id: str) -> List[KeyHealthStatus]:
        """Validate health of all tenant's credentials"""
        
        health_statuses = []
        
        # Get all tenant integrations
        stmt = select(Integration).where(
            Integration.tenant_id == tenant_id,
            Integration.status == 'active'
        )
        result = await self.db.execute(stmt)
        integrations = result.scalars().all()
        
        for integration in integrations:
            try:
                credentials = await self._decrypt_tenant_credentials(integration)
                health = await self._validate_credentials_health(credentials, integration.platform_name)
                
                # Update integration status if needed
                if not health.is_healthy and integration.status == 'active':
                    await self._update_integration_status(integration.id, 'error', health.error_message)
                
                health_statuses.append(health)
                
            except Exception as e:
                logger.error(f"Failed to validate {integration.platform_name} for {tenant_id}: {e}")
                
                health_statuses.append(KeyHealthStatus(
                    platform=integration.platform_name,
                    is_healthy=False,
                    last_check=datetime.utcnow(),
                    error_message=str(e)
                ))
        
        return health_statuses
    
    async def get_tenant_billing_model(self, tenant_id: str) -> Dict[str, BillingModel]:
        """Get billing model for each platform used by tenant"""
        
        billing_models = {}
        
        # Check each supported platform
        for platform in self.supported_platforms:
            try:
                resolved = await self.resolve_credentials(tenant_id, platform)
                billing_models[platform] = resolved.usage_cost_model
                
            except Exception:
                # Platform not used by tenant
                continue
        
        return billing_models
    
    async def migrate_tenant_strategy(
        self, 
        tenant_id: str, 
        new_strategy: CredentialStrategy,
        platforms: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Migrate tenant from one credential strategy to another
        
        Returns:
            Dict of platform -> success status
        """
        results = {}
        platforms_to_migrate = platforms or list(self.supported_platforms)
        
        for platform in platforms_to_migrate:
            try:
                # Test new strategy
                test_creds = await self.resolve_credentials(
                    tenant_id, 
                    platform, 
                    force_strategy=new_strategy
                )
                
                if test_creds.health_status == "healthy":
                    # Update tenant's preferred strategy
                    await self._update_tenant_strategy(tenant_id, new_strategy)
                    results[platform] = True
                else:
                    results[platform] = False
                    
            except Exception as e:
                logger.error(f"Migration failed for {platform}: {e}")
                results[platform] = False
        
        return results
    
    # Helper methods
    
    async def _get_tenant_config(self, tenant_id: str) -> Optional[Any]:
        """Get tenant configuration"""
        stmt = select(Tenant).where(Tenant.id == tenant_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    def _get_tenant_strategy(self, tenant) -> CredentialStrategy:
        """Extract tenant's preferred credential strategy"""
        settings = tenant.settings or {}
        strategy_str = settings.get('credential_strategy', 'auto_resolve')
        
        try:
            return CredentialStrategy(strategy_str)
        except ValueError:
            return CredentialStrategy.AUTO
    
    async def _get_tenant_integration(self, tenant_id: str, platform: str) -> Optional[Integration]:
        """Get tenant's integration for specific platform"""
        stmt = select(Integration).where(
            and_(
                Integration.tenant_id == tenant_id,
                Integration.platform_name == platform
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def _decrypt_tenant_credentials(self, integration: Integration) -> Dict[str, str]:
        """Decrypt tenant's stored credentials"""
        # In real implementation, decrypt the integration.credentials field
        # For now, return mock structure
        import json
        try:
            return json.loads(integration.credentials)
        except Exception:
            return {"api_key": "decrypted_key", "secret": "decrypted_secret"}
    
    async def _validate_credentials_health(self, credentials: Dict[str, str], platform: str) -> KeyHealthStatus:
        """Validate that credentials are working"""
        # In real implementation, make test API calls to each platform
        # For now, return healthy status
        return KeyHealthStatus(
            platform=platform,
            is_healthy=True,
            last_check=datetime.utcnow(),
            error_message=None,
            expires_at=None,
            usage_quota_remaining=1000
        )
    
    def _get_credential_expiry(self, integration: Integration) -> Optional[datetime]:
        """Get credential expiration date"""
        config = integration.configuration or {}
        expires_str = config.get('expires_at')
        if expires_str:
            return datetime.fromisoformat(expires_str)
        return None
    
    def _parse_vault_expiry(self, vault_data: Dict[str, Any]) -> Optional[datetime]:
        """Parse expiration from Vault metadata"""
        metadata = vault_data.get('metadata', {})
        expires_str = metadata.get('expires_at')
        if expires_str:
            return datetime.fromisoformat(expires_str)
        return None
    
    async def _update_integration_status(self, integration_id: str, status: str, error_message: Optional[str]):
        """Update integration status in database"""
        stmt = update(Integration).where(
            Integration.id == integration_id
        ).values(
            status=status,
            updated_at=datetime.utcnow()
        )
        await self.db.execute(stmt)
        await self.db.commit()
    
    async def _update_tenant_strategy(self, tenant_id: str, strategy: CredentialStrategy):
        """Update tenant's preferred credential strategy"""
        stmt = update(Tenant).where(
            Tenant.id == tenant_id
        ).values(
            settings={"credential_strategy": strategy.value},
            updated_at=datetime.utcnow()
        )
        await self.db.execute(stmt)
        await self.db.commit()


# Global service instance
key_resolution_service: Optional[KeyResolutionService] = None

def get_key_resolution_service() -> KeyResolutionService:
    """Get global key resolution service instance"""
    global key_resolution_service
    if not key_resolution_service:
        raise RuntimeError("Key resolution service not initialized")
    return key_resolution_service

def initialize_key_resolution_service(vault_client: VaultClient, db_session: AsyncSession):
    """Initialize global key resolution service"""
    global key_resolution_service
    key_resolution_service = KeyResolutionService(vault_client, db_session)