from ..platform_abstraction.base_platform_client import ReadOnlyPlatformClient, PlatformCapabilities, PlatformCapability
from ..platform_abstraction.platform_registry import register_platform, PlatformMetadata, PlatformTier, PlatformCategory

class MapQuestClient(ReadOnlyPlatformClient):
    def __init__(self, platform_name: str = "mapquest"):
        super().__init__(platform_name)
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[PlatformCapability.SEARCH_LISTINGS],
            read_only=True
        )

register_platform(
    MapQuestClient,
    PlatformMetadata(
        name="mapquest",
        display_name="MapQuest",
        tier=PlatformTier.TIER_2,
        category=PlatformCategory.MAPPING_SERVICE,
        description="Navigation and directions platform",
        website="https://www.mapquest.com"
    ),
    PlatformCapabilities(
        platform_name="mapquest",
        supported_operations=[PlatformCapability.SEARCH_LISTINGS],
        read_only=True
    )
)