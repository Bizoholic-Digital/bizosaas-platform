"""
Platform Abstraction Layer for Multi-Platform Directory Sync
Provides unified interface for all directory and mapping platforms
"""

from .base_platform_client import BasePlatformClient, PlatformCapabilities
from .platform_factory import PlatformFactory, get_platform_client
from .platform_registry import PlatformRegistry, register_platform
from .unified_data_models import (
    UniversalBusinessData,
    UniversalLocation,
    UniversalHours,
    UniversalContact,
    UniversalCategory,
    UniversalReview,
    UniversalPhoto
)

__all__ = [
    "BasePlatformClient",
    "PlatformCapabilities", 
    "PlatformFactory",
    "get_platform_client",
    "PlatformRegistry",
    "register_platform",
    "UniversalBusinessData",
    "UniversalLocation", 
    "UniversalHours",
    "UniversalContact",
    "UniversalCategory",
    "UniversalReview",
    "UniversalPhoto"
]