from ..platform_abstraction.base_platform_client import ReadOnlyPlatformClient, PlatformCapabilities, PlatformCapability
from ..platform_abstraction.platform_registry import register_platform, PlatformMetadata, PlatformTier, PlatformCategory

class SuperpagesClient(ReadOnlyPlatformClient):
    def __init__(self, platform_name: str = "superpages"):
        super().__init__(platform_name)
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[PlatformCapability.SEARCH_LISTINGS, PlatformCapability.CLAIM_LISTING],
            read_only=False
        )

register_platform(
    SuperpagesClient,
    PlatformMetadata(
        name="superpages",
        display_name="Superpages",
        tier=PlatformTier.TIER_3,
        category=PlatformCategory.DIRECTORY,
        description="Verizon business directory",
        website="https://www.superpages.com"
    ),
    PlatformCapabilities(
        platform_name="superpages",
        supported_operations=[PlatformCapability.SEARCH_LISTINGS, PlatformCapability.CLAIM_LISTING],
        read_only=False
    )
)