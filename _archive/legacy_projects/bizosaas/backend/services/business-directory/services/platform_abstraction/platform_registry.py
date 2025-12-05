"""
Platform Registry - Central registry for all platform clients
Manages platform discovery, instantiation, and capabilities
"""

import logging
from typing import Dict, List, Optional, Type, Set
from dataclasses import dataclass
from enum import Enum

from .base_platform_client import BasePlatformClient, PlatformCapabilities, PlatformCapability

logger = logging.getLogger(__name__)

class PlatformTier(str, Enum):
    """Platform tiers based on importance and market reach"""
    TIER_1 = "tier_1"      # Essential platforms (Google, Apple, Facebook, etc.)
    TIER_2 = "tier_2"      # Recommended platforms (TripAdvisor, Foursquare, etc.)
    TIER_3 = "tier_3"      # Industry-specific platforms (Yellow Pages, etc.)
    TIER_4 = "tier_4"      # Niche/regional platforms

class PlatformCategory(str, Enum):
    """Platform categories for better organization"""
    SEARCH_ENGINE = "search_engine"        # Google Maps, Bing Maps
    SOCIAL_MEDIA = "social_media"          # Facebook, Instagram
    REVIEW_PLATFORM = "review_platform"    # Yelp, TripAdvisor
    MAPPING_SERVICE = "mapping_service"    # Apple Maps, Here Maps
    DIRECTORY = "directory"                # Yellow Pages, Superpages
    INDUSTRY_SPECIFIC = "industry_specific" # OpenTable, Zillow, etc.

@dataclass
class PlatformMetadata:
    """Metadata about a platform"""
    name: str
    display_name: str
    tier: PlatformTier
    category: PlatformCategory
    description: str
    website: str
    api_docs_url: Optional[str] = None
    logo_url: Optional[str] = None
    primary_markets: List[str] = None  # Geographic markets where platform is primary
    supported_business_types: List[str] = None  # Business types supported
    monthly_active_users: Optional[int] = None
    is_active: bool = True
    requires_approval: bool = False  # Some platforms require approval for API access
    
    def __post_init__(self):
        if self.primary_markets is None:
            self.primary_markets = []
        if self.supported_business_types is None:
            self.supported_business_types = []

class PlatformRegistry:
    """
    Central registry for all platform clients
    Manages platform discovery, instantiation, and metadata
    """
    
    _instance: Optional['PlatformRegistry'] = None
    _platforms: Dict[str, Type[BasePlatformClient]] = {}
    _metadata: Dict[str, PlatformMetadata] = {}
    _capabilities: Dict[str, PlatformCapabilities] = {}
    
    def __new__(cls) -> 'PlatformRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._load_default_platforms()
    
    def register_platform(self, platform_class: Type[BasePlatformClient],
                         metadata: PlatformMetadata,
                         capabilities: PlatformCapabilities) -> None:
        """
        Register a platform client
        
        Args:
            platform_class: The platform client class
            metadata: Platform metadata
            capabilities: Platform capabilities
        """
        platform_name = metadata.name
        
        if platform_name in self._platforms:
            logger.warning(f"Platform {platform_name} is already registered. Overriding.")
        
        self._platforms[platform_name] = platform_class
        self._metadata[platform_name] = metadata
        self._capabilities[platform_name] = capabilities
        
        logger.info(f"Registered platform: {platform_name} ({metadata.tier.value})")
    
    def get_platform_client(self, platform_name: str) -> Optional[BasePlatformClient]:
        """
        Get an instance of a platform client
        
        Args:
            platform_name: Name of the platform
            
        Returns:
            Platform client instance or None if not found
        """
        if platform_name not in self._platforms:
            logger.error(f"Platform {platform_name} not found in registry")
            return None
        
        try:
            platform_class = self._platforms[platform_name]
            return platform_class(platform_name)
        except Exception as e:
            logger.error(f"Failed to instantiate platform {platform_name}: {str(e)}")
            return None
    
    def get_platform_metadata(self, platform_name: str) -> Optional[PlatformMetadata]:
        """Get metadata for a platform"""
        return self._metadata.get(platform_name)
    
    def get_platform_capabilities(self, platform_name: str) -> Optional[PlatformCapabilities]:
        """Get capabilities for a platform"""
        return self._capabilities.get(platform_name)
    
    def list_platforms(self, tier: Optional[PlatformTier] = None,
                      category: Optional[PlatformCategory] = None,
                      active_only: bool = True) -> List[str]:
        """
        List registered platforms
        
        Args:
            tier: Filter by platform tier
            category: Filter by platform category
            active_only: Only return active platforms
            
        Returns:
            List of platform names
        """
        platforms = []
        
        for platform_name, metadata in self._metadata.items():
            if active_only and not metadata.is_active:
                continue
            
            if tier and metadata.tier != tier:
                continue
            
            if category and metadata.category != category:
                continue
            
            platforms.append(platform_name)
        
        return platforms
    
    def get_platforms_by_capability(self, capability: PlatformCapability) -> List[str]:
        """
        Get platforms that support a specific capability
        
        Args:
            capability: The capability to search for
            
        Returns:
            List of platform names that support the capability
        """
        platforms = []
        
        for platform_name, caps in self._capabilities.items():
            if caps.can_perform(capability):
                platforms.append(platform_name)
        
        return platforms
    
    def get_tier_1_platforms(self) -> List[str]:
        """Get all Tier 1 platforms"""
        return self.list_platforms(tier=PlatformTier.TIER_1)
    
    def get_write_capable_platforms(self) -> List[str]:
        """Get platforms that support write operations"""
        return self.get_platforms_by_capability(PlatformCapability.CREATE_LISTING)
    
    def get_read_only_platforms(self) -> List[str]:
        """Get read-only platforms"""
        platforms = []
        
        for platform_name, caps in self._capabilities.items():
            if not caps.is_write_capable():
                platforms.append(platform_name)
        
        return platforms
    
    def get_platform_summary(self) -> Dict[str, Any]:
        """Get a summary of all registered platforms"""
        summary = {
            "total_platforms": len(self._platforms),
            "by_tier": {},
            "by_category": {},
            "capabilities_summary": {},
            "active_platforms": 0
        }
        
        # Count by tier
        for tier in PlatformTier:
            summary["by_tier"][tier.value] = len(self.list_platforms(tier=tier))
        
        # Count by category
        for category in PlatformCategory:
            summary["by_category"][category.value] = len(self.list_platforms(category=category))
        
        # Count by capabilities
        for capability in PlatformCapability:
            summary["capabilities_summary"][capability.value] = len(
                self.get_platforms_by_capability(capability)
            )
        
        # Count active platforms
        summary["active_platforms"] = len(self.list_platforms(active_only=True))
        
        return summary
    
    def validate_platform_configuration(self) -> Dict[str, List[str]]:
        """
        Validate platform configuration and return issues
        
        Returns:
            Dict with validation issues by category
        """
        issues = {
            "missing_tier_1": [],
            "missing_capabilities": [],
            "inactive_important": [],
            "configuration_errors": []
        }
        
        # Check for missing Tier 1 platforms
        expected_tier_1 = [
            "google_business", "google_maps", "yelp", "facebook",
            "apple_maps", "bing_maps", "bing_places"
        ]
        
        for platform in expected_tier_1:
            if platform not in self._platforms:
                issues["missing_tier_1"].append(platform)
        
        # Check for platforms missing critical capabilities
        for platform_name, caps in self._capabilities.items():
            if not caps.supported_operations:
                issues["missing_capabilities"].append(f"{platform_name}: no operations defined")
        
        # Check for inactive important platforms
        for platform_name, metadata in self._metadata.items():
            if metadata.tier == PlatformTier.TIER_1 and not metadata.is_active:
                issues["inactive_important"].append(platform_name)
        
        return issues
    
    def _load_default_platforms(self):
        """Load default platform metadata (without actual implementations)"""
        # This will be populated as platform clients are registered
        # For now, we define the expected platforms
        
        default_platforms = [
            # Tier 1 - Essential
            PlatformMetadata(
                name="google_business",
                display_name="Google Business Profile",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.SEARCH_ENGINE,
                description="Google's business listing platform",
                website="https://business.google.com",
                api_docs_url="https://developers.google.com/my-business",
                primary_markets=["US", "Global"],
                monthly_active_users=4500000000
            ),
            PlatformMetadata(
                name="google_maps",
                display_name="Google Maps",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.MAPPING_SERVICE,
                description="Google's mapping and location platform",
                website="https://maps.google.com",
                api_docs_url="https://developers.google.com/maps",
                primary_markets=["US", "Global"]
            ),
            PlatformMetadata(
                name="yelp",
                display_name="Yelp",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.REVIEW_PLATFORM,
                description="Local business review platform",
                website="https://www.yelp.com",
                api_docs_url="https://www.yelp.com/developers",
                primary_markets=["US", "CA", "AU", "UK"]
            ),
            PlatformMetadata(
                name="facebook",
                display_name="Facebook Business",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.SOCIAL_MEDIA,
                description="Facebook business pages",
                website="https://business.facebook.com",
                api_docs_url="https://developers.facebook.com/docs/pages-api",
                primary_markets=["Global"],
                monthly_active_users=2900000000
            ),
            PlatformMetadata(
                name="apple_maps",
                display_name="Apple Maps",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.MAPPING_SERVICE,
                description="Apple's mapping platform",
                website="https://mapsconnect.apple.com",
                api_docs_url="https://developer.apple.com/maps",
                primary_markets=["US", "Global"],
                requires_approval=True
            ),
            PlatformMetadata(
                name="bing_maps",
                display_name="Bing Maps",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.MAPPING_SERVICE,
                description="Microsoft's mapping platform",
                website="https://www.bing.com/maps",
                api_docs_url="https://docs.microsoft.com/en-us/bingmaps",
                primary_markets=["US"]
            ),
            PlatformMetadata(
                name="bing_places",
                display_name="Bing Places",
                tier=PlatformTier.TIER_1,
                category=PlatformCategory.SEARCH_ENGINE,
                description="Bing's business listing platform",
                website="https://www.bingplaces.com",
                primary_markets=["US"]
            ),
            
            # Tier 2 - Recommended
            PlatformMetadata(
                name="tripadvisor",
                display_name="TripAdvisor",
                tier=PlatformTier.TIER_2,
                category=PlatformCategory.REVIEW_PLATFORM,
                description="Travel and hospitality review platform",
                website="https://www.tripadvisor.com",
                api_docs_url="https://developer-tripadvisor.com",
                supported_business_types=["restaurant", "hospitality", "entertainment"]
            ),
            PlatformMetadata(
                name="foursquare",
                display_name="Foursquare",
                tier=PlatformTier.TIER_2,
                category=PlatformCategory.MAPPING_SERVICE,
                description="Location intelligence platform",
                website="https://foursquare.com",
                api_docs_url="https://developer.foursquare.com",
                primary_markets=["US", "Global"]
            ),
            PlatformMetadata(
                name="here_maps",
                display_name="HERE Maps",
                tier=PlatformTier.TIER_2,
                category=PlatformCategory.MAPPING_SERVICE,
                description="Enterprise mapping solutions",
                website="https://www.here.com",
                api_docs_url="https://developer.here.com",
                primary_markets=["EU", "Global"]
            ),
            PlatformMetadata(
                name="mapquest",
                display_name="MapQuest",
                tier=PlatformTier.TIER_2,
                category=PlatformCategory.MAPPING_SERVICE,
                description="Navigation and directions platform",
                website="https://www.mapquest.com",
                api_docs_url="https://developer.mapquest.com",
                primary_markets=["US"]
            ),
            
            # Tier 3 - Industry-specific
            PlatformMetadata(
                name="yellow_pages",
                display_name="Yellow Pages",
                tier=PlatformTier.TIER_3,
                category=PlatformCategory.DIRECTORY,
                description="Traditional business directory",
                website="https://www.yellowpages.com",
                primary_markets=["US"]
            ),
            PlatformMetadata(
                name="superpages",
                display_name="Superpages",
                tier=PlatformTier.TIER_3,
                category=PlatformCategory.DIRECTORY,
                description="Verizon business directory",
                website="https://www.superpages.com",
                primary_markets=["US"]
            )
        ]
        
        # Store metadata but don't register clients yet
        for metadata in default_platforms:
            self._metadata[metadata.name] = metadata

# Global registry instance
def get_platform_registry() -> PlatformRegistry:
    """Get the global platform registry instance"""
    return PlatformRegistry()

def register_platform(platform_class: Type[BasePlatformClient],
                     metadata: PlatformMetadata,
                     capabilities: PlatformCapabilities) -> None:
    """
    Convenience function to register a platform
    
    Args:
        platform_class: The platform client class
        metadata: Platform metadata
        capabilities: Platform capabilities
    """
    registry = get_platform_registry()
    registry.register_platform(platform_class, metadata, capabilities)

# Platform registry instance
platform_registry = get_platform_registry()