"""
Credential Management Module for BYOK Architecture
Handles dual-mode credential resolution and management
"""

from .key_resolution import (
    KeyResolutionService,
    CredentialStrategy,
    BillingModel,
    ResolvedCredentials,
    KeyHealthStatus,
    get_key_resolution_service,
    initialize_key_resolution_service
)

__all__ = [
    'KeyResolutionService',
    'CredentialStrategy', 
    'BillingModel',
    'ResolvedCredentials',
    'KeyHealthStatus',
    'get_key_resolution_service',
    'initialize_key_resolution_service'
]