"""
Platform Factory - Factory pattern for creating platform clients
Provides centralized platform client creation and management
"""

import logging
from typing import Dict, Optional, List, Any
from functools import lru_cache

from .base_platform_client import BasePlatformClient, AuthCredentials
from .platform_registry import get_platform_registry, PlatformRegistry
from .unified_data_models import UniversalBusinessData

logger = logging.getLogger(__name__)

class PlatformFactory:
    """
    Factory for creating and managing platform clients
    Provides caching, validation, and lifecycle management
    """
    
    def __init__(self):
        self.registry: PlatformRegistry = get_platform_registry()
        self._client_cache: Dict[str, BasePlatformClient] = {}
        self._health_status: Dict[str, bool] = {}
        
    @lru_cache(maxsize=50)
    def get_platform_client(self, platform_name: str) -> Optional[BasePlatformClient]:
        """
        Get a platform client instance with caching
        
        Args:
            platform_name: Name of the platform
            
        Returns:
            Platform client instance or None if not available
        """
        # Check cache first
        if platform_name in self._client_cache:
            return self._client_cache[platform_name]
        
        # Create new client
        client = self.registry.get_platform_client(platform_name)
        if client:
            self._client_cache[platform_name] = client
            logger.info(f"Created and cached client for platform: {platform_name}")
        else:
            logger.error(f"Failed to create client for platform: {platform_name}")
        
        return client
    
    def get_clients_for_tier(self, tier_name: str) -> List[BasePlatformClient]:
        """
        Get all platform clients for a specific tier
        
        Args:
            tier_name: Platform tier (tier_1, tier_2, etc.)
            
        Returns:
            List of platform clients
        """
        from .platform_registry import PlatformTier
        
        clients = []
        try:
            tier = PlatformTier(tier_name)
            platform_names = self.registry.list_platforms(tier=tier)
            
            for platform_name in platform_names:
                client = self.get_platform_client(platform_name)
                if client:
                    clients.append(client)
        except ValueError:
            logger.error(f"Invalid tier name: {tier_name}")
        
        return clients
    
    def get_tier_1_clients(self) -> List[BasePlatformClient]:
        """Get all Tier 1 platform clients"""
        return self.get_clients_for_tier("tier_1")
    
    def get_write_capable_clients(self) -> List[BasePlatformClient]:
        """Get all clients that support write operations"""
        clients = []
        write_capable_platforms = self.registry.get_write_capable_platforms()
        
        for platform_name in write_capable_platforms:
            client = self.get_platform_client(platform_name)
            if client:
                clients.append(client)
        
        return clients
    
    def get_clients_with_capability(self, capability_name: str) -> List[BasePlatformClient]:
        """
        Get all clients that support a specific capability
        
        Args:
            capability_name: Name of the capability
            
        Returns:
            List of platform clients
        """
        from .base_platform_client import PlatformCapability
        
        clients = []
        try:
            capability = PlatformCapability(capability_name)
            platform_names = self.registry.get_platforms_by_capability(capability)
            
            for platform_name in platform_names:
                client = self.get_platform_client(platform_name)
                if client:
                    clients.append(client)
        except ValueError:
            logger.error(f"Invalid capability name: {capability_name}")
        
        return clients
    
    async def validate_credentials(self, platform_name: str, 
                                 credentials: AuthCredentials) -> bool:
        """
        Validate credentials for a platform
        
        Args:
            platform_name: Name of the platform
            credentials: Authentication credentials
            
        Returns:
            bool: True if credentials are valid
        """
        client = self.get_platform_client(platform_name)
        if not client:
            return False
        
        try:
            return await client.validate_credentials(credentials)
        except Exception as e:
            logger.error(f"Credential validation failed for {platform_name}: {str(e)}")
            return False
    
    async def test_platform_connection(self, platform_name: str) -> bool:
        """
        Test connection to a platform
        
        Args:
            platform_name: Name of the platform
            
        Returns:
            bool: True if platform is reachable
        """
        client = self.get_platform_client(platform_name)
        if not client:
            return False
        
        try:
            is_healthy = await client.health_check()
            self._health_status[platform_name] = is_healthy
            return is_healthy
        except Exception as e:
            logger.error(f"Health check failed for {platform_name}: {str(e)}")
            self._health_status[platform_name] = False
            return False
    
    async def test_all_platforms(self) -> Dict[str, bool]:
        """
        Test connection to all registered platforms
        
        Returns:
            Dict mapping platform names to health status
        """
        results = {}
        platform_names = self.registry.list_platforms()
        
        for platform_name in platform_names:
            results[platform_name] = await self.test_platform_connection(platform_name)
        
        return results
    
    def get_platform_status(self, platform_name: str) -> Dict[str, Any]:
        """
        Get comprehensive status for a platform
        
        Args:
            platform_name: Name of the platform
            
        Returns:
            Dict with platform status information
        """
        client = self.get_platform_client(platform_name)
        metadata = self.registry.get_platform_metadata(platform_name)
        capabilities = self.registry.get_platform_capabilities(platform_name)
        
        status = {
            "platform_name": platform_name,
            "client_available": client is not None,
            "last_health_check": self._health_status.get(platform_name),
            "metadata": metadata.__dict__ if metadata else None,
            "capabilities": {
                "supported_operations": [op.value for op in capabilities.supported_operations] if capabilities else [],
                "read_only": capabilities.read_only if capabilities else None,
                "rate_limits": {
                    "per_minute": capabilities.rate_limit_per_minute if capabilities else None,
                    "per_day": capabilities.rate_limit_per_day if capabilities else None
                } if capabilities else None
            } if capabilities else None
        }
        
        return status
    
    def get_all_platform_status(self) -> List[Dict[str, Any]]:
        """Get status for all platforms"""
        results = []
        platform_names = self.registry.list_platforms()
        
        for platform_name in platform_names:
            results.append(self.get_platform_status(platform_name))
        
        return results
    
    def clear_cache(self, platform_name: Optional[str] = None):
        """
        Clear platform client cache
        
        Args:
            platform_name: Specific platform to clear, or None for all
        """
        if platform_name:
            if platform_name in self._client_cache:
                del self._client_cache[platform_name]
                logger.info(f"Cleared cache for platform: {platform_name}")
        else:
            self._client_cache.clear()
            logger.info("Cleared all platform client cache")
    
    def get_recommended_platforms_for_business(self, business_data: UniversalBusinessData) -> List[str]:
        """
        Get recommended platforms for a specific business
        
        Args:
            business_data: Business data to analyze
            
        Returns:
            List of recommended platform names, ordered by priority
        """
        recommendations = []
        
        # Always recommend Tier 1 platforms
        tier_1_platforms = self.registry.get_tier_1_platforms()
        recommendations.extend(tier_1_platforms)
        
        # Add business-type specific recommendations
        if business_data.categories and business_data.categories.business_type:
            business_type = business_data.categories.business_type.value
            
            # Restaurant-specific platforms
            if business_type == "restaurant":
                recommendations.extend(["tripadvisor", "opentable", "grubhub"])
            
            # Retail-specific platforms
            elif business_type == "retail":
                recommendations.extend(["foursquare", "nextdoor"])
            
            # Healthcare-specific platforms
            elif business_type == "healthcare":
                recommendations.extend(["healthgrades", "vitals"])
            
            # Hospitality-specific platforms
            elif business_type == "hospitality":
                recommendations.extend(["tripadvisor", "booking", "expedia"])
        
        # Location-specific recommendations
        if business_data.location:
            # US-specific platforms
            if business_data.location.country == "US":
                recommendations.extend(["yellow_pages", "superpages", "citysearch"])
            
            # International platforms for other countries
            elif business_data.location.country in ["CA", "AU", "UK"]:
                recommendations.append("foursquare")
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        seen = set()
        for platform in recommendations:
            if platform not in seen and platform in self.registry.list_platforms():
                unique_recommendations.append(platform)
                seen.add(platform)
        
        return unique_recommendations
    
    def get_factory_stats(self) -> Dict[str, Any]:
        """Get factory statistics"""
        return {
            "total_registered_platforms": len(self.registry.list_platforms()),
            "cached_clients": len(self._client_cache),
            "health_check_results": self._health_status.copy(),
            "tier_1_platforms": len(self.registry.get_tier_1_platforms()),
            "write_capable_platforms": len(self.registry.get_write_capable_platforms()),
            "read_only_platforms": len(self.registry.get_read_only_platforms())
        }

# Global factory instance
_platform_factory: Optional[PlatformFactory] = None

def get_platform_factory() -> PlatformFactory:
    """Get the global platform factory instance"""
    global _platform_factory
    if _platform_factory is None:
        _platform_factory = PlatformFactory()
    return _platform_factory

def get_platform_client(platform_name: str) -> Optional[BasePlatformClient]:
    """
    Convenience function to get a platform client
    
    Args:
        platform_name: Name of the platform
        
    Returns:
        Platform client instance or None
    """
    factory = get_platform_factory()
    return factory.get_platform_client(platform_name)

# Global factory instance
platform_factory = get_platform_factory()