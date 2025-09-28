"""
Foursquare Platform Client
Location intelligence platform integration
"""

from ..platform_abstraction.base_platform_client import ReadOnlyPlatformClient, PlatformCapabilities, PlatformCapability
from ..platform_abstraction.unified_data_models import UniversalBusinessData
from ..platform_abstraction.platform_registry import register_platform, PlatformMetadata, PlatformTier, PlatformCategory

class FoursquareClient(ReadOnlyPlatformClient):
    def __init__(self, platform_name: str = "foursquare"):
        super().__init__(platform_name)
        self.base_url = "https://api.foursquare.com/v3"
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[PlatformCapability.SEARCH_LISTINGS],
            read_only=True,
            rate_limit_per_minute=5000,
            rate_limit_per_day=100000
        )

# Register platform
register_platform(
    FoursquareClient,
    PlatformMetadata(
        name="foursquare",
        display_name="Foursquare",
        tier=PlatformTier.TIER_2,
        category=PlatformCategory.MAPPING_SERVICE,
        description="Location intelligence platform",
        website="https://foursquare.com",
        api_docs_url="https://developer.foursquare.com"
    ),
    PlatformCapabilities(
        platform_name="foursquare",
        supported_operations=[PlatformCapability.SEARCH_LISTINGS],
        read_only=True,
        rate_limit_per_minute=5000,
        rate_limit_per_day=100000
    )
)