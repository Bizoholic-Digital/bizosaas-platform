from ..platform_abstraction.base_platform_client import ReadOnlyPlatformClient, PlatformCapabilities, PlatformCapability
from ..platform_abstraction.platform_registry import register_platform, PlatformMetadata, PlatformTier, PlatformCategory

class HereMapsClient(ReadOnlyPlatformClient):
    def __init__(self, platform_name: str = "here_maps"):
        super().__init__(platform_name)
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[PlatformCapability.SEARCH_LISTINGS],
            read_only=True,
            rate_limit_per_minute=1000
        )

register_platform(
    HereMapsClient,
    PlatformMetadata(
        name="here_maps",
        display_name="HERE Maps",
        tier=PlatformTier.TIER_2,
        category=PlatformCategory.MAPPING_SERVICE,
        description="Enterprise mapping solutions",
        website="https://www.here.com"
    ),
    PlatformCapabilities(
        platform_name="here_maps",
        supported_operations=[PlatformCapability.SEARCH_LISTINGS],
        read_only=True
    )
)