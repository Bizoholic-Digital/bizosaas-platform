from ..platform_abstraction.base_platform_client import ReadOnlyPlatformClient, PlatformCapabilities, PlatformCapability
from ..platform_abstraction.platform_registry import register_platform, PlatformMetadata, PlatformTier, PlatformCategory

class YellowPagesClient(ReadOnlyPlatformClient):
    def __init__(self, platform_name: str = "yellow_pages"):
        super().__init__(platform_name)
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[PlatformCapability.SEARCH_LISTINGS, PlatformCapability.CLAIM_LISTING],
            read_only=False
        )

register_platform(
    YellowPagesClient,
    PlatformMetadata(
        name="yellow_pages",
        display_name="Yellow Pages",
        tier=PlatformTier.TIER_3,
        category=PlatformCategory.DIRECTORY,
        description="Traditional business directory",
        website="https://www.yellowpages.com"
    ),
    PlatformCapabilities(
        platform_name="yellow_pages",
        supported_operations=[PlatformCapability.SEARCH_LISTINGS, PlatformCapability.CLAIM_LISTING],
        read_only=False
    )
)