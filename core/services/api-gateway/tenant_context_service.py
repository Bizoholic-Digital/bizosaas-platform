"""
Unified Tenant Context Management Service
Coordinates tenant context across Wagtail CMS, Saleor, Django CRM, and other BizOSaaS services
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import jwt
from fastapi import HTTPException
import redis.asyncio as redis

logger = logging.getLogger(__name__)


@dataclass
class TenantContext:
    """Unified tenant context structure"""
    
    # Core tenant identification
    tenant_id: str
    bizosaas_tenant_id: str
    
    # Domain and routing
    domain: str
    subdomain: Optional[str] = None
    full_domain: str = ""
    
    # Tenant metadata
    name: str = ""
    slug: str = ""
    is_active: bool = True
    subscription_tier: str = "tier_1"
    
    # Service-specific contexts
    wagtail_context: Optional[Dict[str, Any]] = None
    saleor_context: Optional[Dict[str, Any]] = None
    crm_context: Optional[Dict[str, Any]] = None
    
    # User context
    user_id: Optional[str] = None
    user_role: Optional[str] = None
    user_permissions: List[str] = None
    
    # Feature access and limits
    features: List[str] = None
    tier_limits: Dict[str, Any] = None
    
    # Branding and UI
    branding: Dict[str, str] = None
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    cached_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.full_domain:
            self.full_domain = f"{self.subdomain}.{self.domain}" if self.subdomain else self.domain
        
        if self.user_permissions is None:
            self.user_permissions = []
        
        if self.features is None:
            self.features = []
        
        if self.tier_limits is None:
            self.tier_limits = {}
        
        if self.branding is None:
            self.branding = {}
        
        if not self.cached_at:
            self.cached_at = datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with datetime serialization"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TenantContext':
        """Create from dictionary with datetime deserialization"""
        # Convert ISO strings back to datetime objects
        datetime_fields = ['created_at', 'updated_at', 'cached_at']
        for field in datetime_fields:
            if data.get(field) and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except ValueError:
                    data[field] = None
        return cls(**data)


class TenantContextService:
    """
    Unified tenant context management service
    Coordinates tenant information across all BizOSaaS services
    """
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.service_configs = {
            'wagtail': {
                'url': 'http://localhost:8006',
                'endpoints': {
                    'tenant_info': '/api/v2/tenant-info/',
                    'site_info': '/api/v2/site-info/'
                }
            },
            'saleor': {
                'url': 'http://localhost:8009',
                'endpoints': {
                    'organization_info': '/api/organization-info/',
                    'graphql': '/graphql/'
                }
            },
            'crm': {
                'url': 'http://localhost:8007',
                'endpoints': {
                    'tenant_info': '/api/tenant-info/',
                    'user_info': '/api/user-info/'
                }
            }
        }
        
        # Cache settings
        self.cache_ttl = 300  # 5 minutes
        self.cache_prefix = "tenant_context"
    
    async def initialize(self):
        """Initialize the service with Redis connection"""
        try:
            self.redis_client = redis.from_url("redis://localhost:6379/2")
            await self.redis_client.ping()
            logger.info("TenantContextService initialized with Redis connection")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Using in-memory cache.")
            self.redis_client = None
    
    async def resolve_tenant_context(
        self, 
        domain: str, 
        user_id: Optional[str] = None,
        force_refresh: bool = False
    ) -> Optional[TenantContext]:
        """
        Resolve complete tenant context from domain
        Coordinates with all services to build unified context
        """
        
        # Check cache first
        cache_key = f"{self.cache_prefix}:{domain}:{user_id or 'anonymous'}"
        
        if not force_refresh:
            cached_context = await self._get_from_cache(cache_key)
            if cached_context:
                return cached_context
        
        logger.info(f"Resolving tenant context for domain: {domain}")
        
        # Resolve tenant from all services in parallel
        tasks = []
        
        # Get Wagtail tenant/site info
        tasks.append(self._get_wagtail_context(domain))
        
        # Get Saleor organization info
        tasks.append(self._get_saleor_context(domain))
        
        # Get CRM tenant info
        tasks.append(self._get_crm_context(domain))
        
        try:
            # Execute all service calls in parallel
            wagtail_context, saleor_context, crm_context = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            
            # Handle exceptions from individual services
            if isinstance(wagtail_context, Exception):
                logger.warning(f"Wagtail context failed: {wagtail_context}")
                wagtail_context = None
            
            if isinstance(saleor_context, Exception):
                logger.warning(f"Saleor context failed: {saleor_context}")
                saleor_context = None
            
            if isinstance(crm_context, Exception):
                logger.warning(f"CRM context failed: {crm_context}")
                crm_context = None
            
            # Build unified context
            unified_context = await self._build_unified_context(
                domain=domain,
                wagtail_context=wagtail_context,
                saleor_context=saleor_context,
                crm_context=crm_context,
                user_id=user_id
            )
            
            if unified_context:
                # Cache the result
                await self._store_in_cache(cache_key, unified_context)
                
                logger.info(f"Successfully resolved tenant context for {domain}")
                return unified_context
            else:
                logger.warning(f"No tenant context found for domain: {domain}")
                return None
                
        except Exception as e:
            logger.error(f"Error resolving tenant context for {domain}: {e}")
            return None
    
    async def _get_wagtail_context(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get tenant context from Wagtail CMS"""
        try:
            async with aiohttp.ClientSession() as session:
                # First try to get site info by domain
                url = f"{self.service_configs['wagtail']['url']}/api/v2/site-info/"
                params = {'domain': domain}
                
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'service': 'wagtail',
                            'site_id': data.get('site_id'),
                            'site_name': data.get('site_name'),
                            'tenant_id': data.get('tenant_id'),
                            'tenant_name': data.get('tenant_name'),
                            'theme_settings': data.get('theme_settings'),
                            'seo_settings': data.get('seo_settings'),
                            'pages_count': data.get('pages_count', 0)
                        }
                    else:
                        logger.warning(f"Wagtail API returned status {response.status} for domain {domain}")
                        return None
                        
        except asyncio.TimeoutError:
            logger.warning(f"Wagtail API timeout for domain {domain}")
            return None
        except Exception as e:
            logger.error(f"Error getting Wagtail context for {domain}: {e}")
            return None
    
    async def _get_saleor_context(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get organization context from Saleor"""
        try:
            async with aiohttp.ClientSession() as session:
                # Query organization info by domain
                url = f"{self.service_configs['saleor']['url']}/api/organization-info/"
                params = {'domain': domain}
                
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'service': 'saleor',
                            'organization_id': data.get('organization_id'),
                            'organization_name': data.get('organization_name'),
                            'organization_slug': data.get('organization_slug'),
                            'subscription_tier': data.get('subscription_tier'),
                            'tier_limits': data.get('tier_limits'),
                            'features': data.get('features', []),
                            'branding': data.get('branding', {}),
                            'products_count': data.get('products_count', 0),
                            'orders_count': data.get('orders_count', 0)
                        }
                    else:
                        logger.warning(f"Saleor API returned status {response.status} for domain {domain}")
                        return None
                        
        except asyncio.TimeoutError:
            logger.warning(f"Saleor API timeout for domain {domain}")
            return None
        except Exception as e:
            logger.error(f"Error getting Saleor context for {domain}: {e}")
            return None
    
    async def _get_crm_context(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get tenant context from Django CRM"""
        try:
            async with aiohttp.ClientSession() as session:
                # Query tenant info by domain
                url = f"{self.service_configs['crm']['url']}/api/tenant-info/"
                params = {'domain': domain}
                
                async with session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'service': 'crm',
                            'tenant_id': data.get('tenant_id'),
                            'tenant_name': data.get('tenant_name'),
                            'leads_count': data.get('leads_count', 0),
                            'customers_count': data.get('customers_count', 0),
                            'campaigns_count': data.get('campaigns_count', 0),
                            'settings': data.get('settings', {})
                        }
                    else:
                        logger.warning(f"CRM API returned status {response.status} for domain {domain}")
                        return None
                        
        except asyncio.TimeoutError:
            logger.warning(f"CRM API timeout for domain {domain}")
            return None
        except Exception as e:
            logger.error(f"Error getting CRM context for {domain}: {e}")
            return None
    
    async def _build_unified_context(
        self,
        domain: str,
        wagtail_context: Optional[Dict[str, Any]],
        saleor_context: Optional[Dict[str, Any]],
        crm_context: Optional[Dict[str, Any]],
        user_id: Optional[str] = None
    ) -> Optional[TenantContext]:
        """
        Build unified tenant context from individual service contexts
        """
        
        # Must have at least one service context
        if not any([wagtail_context, saleor_context, crm_context]):
            return None
        
        # Extract core tenant information (prioritize Saleor > Wagtail > CRM)
        tenant_id = None
        bizosaas_tenant_id = None
        tenant_name = ""
        tenant_slug = ""
        subscription_tier = "tier_1"
        features = []
        tier_limits = {}
        branding = {}
        
        # Extract from Saleor (highest priority)
        if saleor_context:
            tenant_id = saleor_context.get('organization_id')
            tenant_name = saleor_context.get('organization_name', '')
            tenant_slug = saleor_context.get('organization_slug', '')
            subscription_tier = saleor_context.get('subscription_tier', 'tier_1')
            features.extend(saleor_context.get('features', []))
            tier_limits.update(saleor_context.get('tier_limits', {}))
            branding.update(saleor_context.get('branding', {}))
        
        # Extract from Wagtail
        if wagtail_context:
            if not tenant_id:
                tenant_id = wagtail_context.get('tenant_id')
            if not tenant_name:
                tenant_name = wagtail_context.get('tenant_name', '')
        
        # Extract from CRM
        if crm_context:
            if not tenant_id:
                tenant_id = crm_context.get('tenant_id')
            if not tenant_name:
                tenant_name = crm_context.get('tenant_name', '')
        
        # Generate BizOSaaS tenant ID if not available
        if not bizosaas_tenant_id:
            bizosaas_tenant_id = tenant_id or self._generate_tenant_id(domain)
        
        # Parse domain for subdomain
        domain_parts = domain.split('.')
        subdomain = None
        if len(domain_parts) > 2:
            subdomain = domain_parts[0]
            parent_domain = '.'.join(domain_parts[1:])
        else:
            parent_domain = domain
        
        # Build unified context
        context = TenantContext(
            tenant_id=tenant_id or bizosaas_tenant_id,
            bizosaas_tenant_id=bizosaas_tenant_id,
            domain=parent_domain,
            subdomain=subdomain,
            full_domain=domain,
            name=tenant_name,
            slug=tenant_slug,
            is_active=True,
            subscription_tier=subscription_tier,
            wagtail_context=wagtail_context,
            saleor_context=saleor_context,
            crm_context=crm_context,
            user_id=user_id,
            features=features,
            tier_limits=tier_limits,
            branding=branding,
            created_at=datetime.now(timezone.utc)
        )
        
        return context
    
    def _generate_tenant_id(self, domain: str) -> str:
        """Generate a tenant ID from domain"""
        return hashlib.md5(domain.encode()).hexdigest()
    
    async def _get_from_cache(self, cache_key: str) -> Optional[TenantContext]:
        """Get tenant context from cache"""
        if not self.redis_client:
            return None
        
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                data = json.loads(cached_data)
                return TenantContext.from_dict(data)
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
        
        return None
    
    async def _store_in_cache(self, cache_key: str, context: TenantContext):
        """Store tenant context in cache"""
        if not self.redis_client:
            return
        
        try:
            data = json.dumps(context.to_dict())
            await self.redis_client.setex(cache_key, self.cache_ttl, data)
        except Exception as e:
            logger.warning(f"Cache store error: {e}")
    
    async def invalidate_cache(self, domain: str, user_id: Optional[str] = None):
        """Invalidate cached tenant context"""
        if not self.redis_client:
            return
        
        try:
            cache_key = f"{self.cache_prefix}:{domain}:{user_id or 'anonymous'}"
            await self.redis_client.delete(cache_key)
            logger.info(f"Invalidated cache for {domain}")
        except Exception as e:
            logger.warning(f"Cache invalidation error: {e}")
    
    async def sync_tenant_across_services(
        self, 
        tenant_context: TenantContext,
        sync_config: Optional[Dict[str, bool]] = None
    ) -> Dict[str, bool]:
        """
        Synchronize tenant information across all services
        Returns status of sync operations
        """
        if sync_config is None:
            sync_config = {
                'wagtail': True,
                'saleor': True, 
                'crm': True
            }
        
        results = {}
        tasks = []
        
        if sync_config.get('wagtail', True):
            tasks.append(('wagtail', self._sync_to_wagtail(tenant_context)))
        
        if sync_config.get('saleor', True):
            tasks.append(('saleor', self._sync_to_saleor(tenant_context)))
        
        if sync_config.get('crm', True):
            tasks.append(('crm', self._sync_to_crm(tenant_context)))
        
        # Execute sync operations in parallel
        for service, task in tasks:
            try:
                result = await task
                results[service] = result
            except Exception as e:
                logger.error(f"Sync to {service} failed: {e}")
                results[service] = False
        
        return results
    
    async def _sync_to_wagtail(self, context: TenantContext) -> bool:
        """Sync tenant context to Wagtail"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.service_configs['wagtail']['url']}/api/v2/tenant-sync/"
                data = {
                    'tenant_id': context.bizosaas_tenant_id,
                    'name': context.name,
                    'domain': context.full_domain,
                    'subdomain': context.subdomain,
                    'branding': context.branding
                }
                
                async with session.post(url, json=data, timeout=10) as response:
                    return response.status in [200, 201]
                    
        except Exception as e:
            logger.error(f"Wagtail sync error: {e}")
            return False
    
    async def _sync_to_saleor(self, context: TenantContext) -> bool:
        """Sync tenant context to Saleor"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.service_configs['saleor']['url']}/api/organization-sync/"
                data = {
                    'bizosaas_tenant_id': context.bizosaas_tenant_id,
                    'name': context.name,
                    'domain': context.full_domain,
                    'subdomain': context.subdomain,
                    'subscription_tier': context.subscription_tier,
                    'branding': context.branding
                }
                
                async with session.post(url, json=data, timeout=10) as response:
                    return response.status in [200, 201]
                    
        except Exception as e:
            logger.error(f"Saleor sync error: {e}")
            return False
    
    async def _sync_to_crm(self, context: TenantContext) -> bool:
        """Sync tenant context to CRM"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.service_configs['crm']['url']}/api/tenant-sync/"
                data = {
                    'tenant_id': context.bizosaas_tenant_id,
                    'name': context.name,
                    'domain': context.full_domain,
                    'subdomain': context.subdomain,
                    'subscription_tier': context.subscription_tier
                }
                
                async with session.post(url, json=data, timeout=10) as response:
                    return response.status in [200, 201]
                    
        except Exception as e:
            logger.error(f"CRM sync error: {e}")
            return False


# Global instance
tenant_context_service = TenantContextService()