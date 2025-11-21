"""
Base Platform Client - Abstract interface for all directory platforms
Defines the contract that all platform clients must implement
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from .unified_data_models import UniversalBusinessData, UniversalSyncMapping

logger = logging.getLogger(__name__)

class PlatformCapability(str, Enum):
    """Platform capabilities - what operations are supported"""
    CREATE_LISTING = "create_listing"
    UPDATE_LISTING = "update_listing"
    DELETE_LISTING = "delete_listing"
    SEARCH_LISTINGS = "search_listings"
    CLAIM_LISTING = "claim_listing"
    VERIFY_LISTING = "verify_listing"
    MANAGE_REVIEWS = "manage_reviews"
    MANAGE_PHOTOS = "manage_photos"
    MANAGE_POSTS = "manage_posts"
    ANALYTICS = "analytics"
    BULK_OPERATIONS = "bulk_operations"

class SyncOperation(str, Enum):
    """Types of sync operations"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    CLAIM = "claim"
    VERIFY = "verify"
    SEARCH = "search"
    GET = "get"

class SyncStatus(str, Enum):
    """Sync operation status"""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    PENDING = "pending"
    RATE_LIMITED = "rate_limited"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not_found"

@dataclass
class PlatformCapabilities:
    """Defines what a platform can do"""
    platform_name: str
    supported_operations: List[PlatformCapability] = field(default_factory=list)
    read_only: bool = False
    requires_verification: bool = False
    supports_bulk: bool = False
    rate_limit_per_minute: int = 60
    rate_limit_per_day: int = 10000
    
    def can_perform(self, operation: PlatformCapability) -> bool:
        """Check if platform supports an operation"""
        return operation in self.supported_operations
    
    def is_write_capable(self) -> bool:
        """Check if platform supports write operations"""
        write_ops = [
            PlatformCapability.CREATE_LISTING,
            PlatformCapability.UPDATE_LISTING,
            PlatformCapability.DELETE_LISTING
        ]
        return not self.read_only and any(op in self.supported_operations for op in write_ops)

@dataclass
class PlatformResponse:
    """Standard response from platform operations"""
    success: bool
    operation: SyncOperation
    platform: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    platform_id: Optional[str] = None
    from_cache: bool = False
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[datetime] = None
    
    @property
    def is_rate_limited(self) -> bool:
        """Check if response indicates rate limiting"""
        return self.status_code == 429 or "rate limit" in (self.error or "").lower()

@dataclass 
class AuthCredentials:
    """Authentication credentials for platform access"""
    platform: str
    credentials: Dict[str, Any]
    expires_at: Optional[datetime] = None
    refresh_token: Optional[str] = None
    
    def is_expired(self) -> bool:
        """Check if credentials are expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() >= self.expires_at
    
    def get_credential(self, key: str) -> Optional[str]:
        """Get a specific credential value"""
        return self.credentials.get(key)

class BasePlatformClient(ABC):
    """
    Abstract base class for all platform clients
    Defines the contract that all platform integrations must follow
    """
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")
        self._capabilities: Optional[PlatformCapabilities] = None
        self._rate_limiter: Optional[Any] = None
        
    @property
    @abstractmethod
    def capabilities(self) -> PlatformCapabilities:
        """Get platform capabilities"""
        pass
    
    @abstractmethod
    async def authenticate(self, credentials: AuthCredentials) -> bool:
        """
        Authenticate with the platform
        
        Args:
            credentials: Platform-specific authentication credentials
            
        Returns:
            bool: True if authentication successful
        """
        pass
    
    @abstractmethod
    async def create_listing(self, business_data: UniversalBusinessData, 
                           credentials: AuthCredentials) -> PlatformResponse:
        """
        Create a new business listing on the platform
        
        Args:
            business_data: Universal business data
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with creation result
        """
        pass
    
    @abstractmethod
    async def update_listing(self, platform_id: str, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        """
        Update an existing business listing
        
        Args:
            platform_id: Platform-specific listing ID
            business_data: Updated business data
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with update result
        """
        pass
    
    @abstractmethod
    async def get_listing(self, platform_id: str, 
                         credentials: AuthCredentials) -> PlatformResponse:
        """
        Retrieve a business listing from the platform
        
        Args:
            platform_id: Platform-specific listing ID
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with listing data
        """
        pass
    
    @abstractmethod
    async def search_listings(self, query: str, location: str,
                            credentials: AuthCredentials) -> PlatformResponse:
        """
        Search for business listings on the platform
        
        Args:
            query: Search query (business name, category, etc.)
            location: Geographic location for search
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with search results
        """
        pass
    
    async def delete_listing(self, platform_id: str,
                           credentials: AuthCredentials) -> PlatformResponse:
        """
        Delete a business listing (if supported)
        
        Args:
            platform_id: Platform-specific listing ID
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with deletion result
        """
        if not self.capabilities.can_perform(PlatformCapability.DELETE_LISTING):
            return PlatformResponse(
                success=False,
                operation=SyncOperation.DELETE,
                platform=self.platform_name,
                error=f"{self.platform_name} does not support listing deletion"
            )
        
        return await self._delete_listing_impl(platform_id, credentials)
    
    async def claim_listing(self, platform_id: str,
                          credentials: AuthCredentials) -> PlatformResponse:
        """
        Claim an existing business listing (if supported)
        
        Args:
            platform_id: Platform-specific listing ID
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with claim result
        """
        if not self.capabilities.can_perform(PlatformCapability.CLAIM_LISTING):
            return PlatformResponse(
                success=False,
                operation=SyncOperation.CLAIM,
                platform=self.platform_name,
                error=f"{self.platform_name} does not support listing claiming"
            )
        
        return await self._claim_listing_impl(platform_id, credentials)
    
    async def verify_listing(self, platform_id: str,
                           credentials: AuthCredentials) -> PlatformResponse:
        """
        Verify a business listing (if supported)
        
        Args:
            platform_id: Platform-specific listing ID
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with verification result
        """
        if not self.capabilities.can_perform(PlatformCapability.VERIFY_LISTING):
            return PlatformResponse(
                success=False,
                operation=SyncOperation.VERIFY,
                platform=self.platform_name,
                error=f"{self.platform_name} does not support listing verification"
            )
        
        return await self._verify_listing_impl(platform_id, credentials)
    
    async def get_reviews(self, platform_id: str,
                        credentials: AuthCredentials) -> PlatformResponse:
        """
        Get reviews for a business listing (if supported)
        
        Args:
            platform_id: Platform-specific listing ID
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with reviews data
        """
        if not self.capabilities.can_perform(PlatformCapability.MANAGE_REVIEWS):
            return PlatformResponse(
                success=False,
                operation=SyncOperation.GET,
                platform=self.platform_name,
                error=f"{self.platform_name} does not support review management"
            )
        
        return await self._get_reviews_impl(platform_id, credentials)
    
    async def get_analytics(self, platform_id: str,
                          credentials: AuthCredentials) -> PlatformResponse:
        """
        Get analytics data for a business listing (if supported)
        
        Args:
            platform_id: Platform-specific listing ID
            credentials: Platform authentication
            
        Returns:
            PlatformResponse with analytics data
        """
        if not self.capabilities.can_perform(PlatformCapability.ANALYTICS):
            return PlatformResponse(
                success=False,
                operation=SyncOperation.GET,
                platform=self.platform_name,
                error=f"{self.platform_name} does not support analytics"
            )
        
        return await self._get_analytics_impl(platform_id, credentials)
    
    # Abstract methods for platform-specific implementations
    
    async def _delete_listing_impl(self, platform_id: str,
                                 credentials: AuthCredentials) -> PlatformResponse:
        """Platform-specific delete implementation"""
        raise NotImplementedError
    
    async def _claim_listing_impl(self, platform_id: str,
                                credentials: AuthCredentials) -> PlatformResponse:
        """Platform-specific claim implementation"""
        raise NotImplementedError
    
    async def _verify_listing_impl(self, platform_id: str,
                                 credentials: AuthCredentials) -> PlatformResponse:
        """Platform-specific verify implementation"""
        raise NotImplementedError
    
    async def _get_reviews_impl(self, platform_id: str,
                              credentials: AuthCredentials) -> PlatformResponse:
        """Platform-specific get reviews implementation"""
        raise NotImplementedError
    
    async def _get_analytics_impl(self, platform_id: str,
                                credentials: AuthCredentials) -> PlatformResponse:
        """Platform-specific get analytics implementation"""
        raise NotImplementedError
    
    # Utility methods
    
    def transform_to_universal(self, platform_data: Dict[str, Any]) -> UniversalBusinessData:
        """
        Transform platform-specific data to universal format
        Must be implemented by each platform client
        
        Args:
            platform_data: Platform-specific business data
            
        Returns:
            UniversalBusinessData: Standardized business data
        """
        raise NotImplementedError(f"{self.platform_name} must implement transform_to_universal")
    
    def transform_from_universal(self, business_data: UniversalBusinessData) -> Dict[str, Any]:
        """
        Transform universal data to platform-specific format
        Must be implemented by each platform client
        
        Args:
            business_data: Universal business data
            
        Returns:
            Dict: Platform-specific data format
        """
        raise NotImplementedError(f"{self.platform_name} must implement transform_from_universal")
    
    async def validate_credentials(self, credentials: AuthCredentials) -> bool:
        """
        Validate authentication credentials
        
        Args:
            credentials: Platform credentials to validate
            
        Returns:
            bool: True if credentials are valid
        """
        try:
            return await self.authenticate(credentials)
        except Exception as e:
            self.logger.error(f"Credential validation failed: {str(e)}")
            return False
    
    def create_error_response(self, operation: SyncOperation, error: str,
                            status_code: Optional[int] = None) -> PlatformResponse:
        """Create a standardized error response"""
        return PlatformResponse(
            success=False,
            operation=operation,
            platform=self.platform_name,
            error=error,
            status_code=status_code
        )
    
    def create_success_response(self, operation: SyncOperation, data: Dict[str, Any],
                              platform_id: Optional[str] = None) -> PlatformResponse:
        """Create a standardized success response"""
        return PlatformResponse(
            success=True,
            operation=operation,
            platform=self.platform_name,
            data=data,
            platform_id=platform_id
        )
    
    async def health_check(self) -> bool:
        """
        Perform a health check on the platform API
        
        Returns:
            bool: True if platform is healthy
        """
        try:
            # Basic connectivity test - each platform can override
            return True
        except Exception as e:
            self.logger.error(f"Health check failed for {self.platform_name}: {str(e)}")
            return False
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get current rate limit information"""
        return {
            "per_minute": self.capabilities.rate_limit_per_minute,
            "per_day": self.capabilities.rate_limit_per_day,
            "platform": self.platform_name
        }

class ReadOnlyPlatformClient(BasePlatformClient):
    """
    Base class for read-only platforms (like Yelp)
    Provides default implementations that return "not supported" errors
    """
    
    async def create_listing(self, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        return self.create_error_response(
            SyncOperation.CREATE,
            f"{self.platform_name} is read-only and does not support creating listings"
        )
    
    async def update_listing(self, platform_id: str, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        return self.create_error_response(
            SyncOperation.UPDATE,
            f"{self.platform_name} is read-only and does not support updating listings"
        )
    
    async def _delete_listing_impl(self, platform_id: str,
                                 credentials: AuthCredentials) -> PlatformResponse:
        return self.create_error_response(
            SyncOperation.DELETE,
            f"{self.platform_name} is read-only and does not support deleting listings"
        )