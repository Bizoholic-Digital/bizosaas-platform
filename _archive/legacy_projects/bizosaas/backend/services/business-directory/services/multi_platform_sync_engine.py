"""
Multi-Platform Directory Sync Engine
Orchestrates synchronization across Google, Yelp, Facebook, and Apple Maps
"""

import asyncio
import json
import logging
from enum import Enum
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from ..models.business import Business, BusinessPlatform, BusinessSyncLog
from ..models.base import SyncStatus, ConflictResolution
from ..core.database import get_async_session
from ..core.config import settings
from .google_business_client import google_business_client, GoogleDataMapper
from .yelp_business_client import yelp_client, YelpDataMapper
from .facebook_business_client import facebook_client, FacebookDataMapper
from .apple_maps_client import apple_maps_client, AppleMapsDataMapper

logger = logging.getLogger(__name__)

class Platform(str, Enum):
    GOOGLE = "google"
    YELP = "yelp"
    FACEBOOK = "facebook"
    APPLE_MAPS = "apple_maps"

class SyncOperation(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    CLAIM = "claim"
    VERIFY = "verify"

class ConflictType(str, Enum):
    NAME_MISMATCH = "name_mismatch"
    ADDRESS_MISMATCH = "address_mismatch"
    PHONE_MISMATCH = "phone_mismatch"
    HOURS_MISMATCH = "hours_mismatch"
    CATEGORY_MISMATCH = "category_mismatch"
    DUPLICATE_LISTING = "duplicate_listing"

@dataclass
class SyncResult:
    """Result of a sync operation"""
    platform: Platform
    operation: SyncOperation
    success: bool
    business_id: Optional[str] = None
    platform_id: Optional[str] = None
    error: Optional[str] = None
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    data: Optional[Dict[str, Any]] = None

@dataclass
class ConflictDetail:
    """Details of a data conflict between platforms"""
    conflict_type: ConflictType
    platforms: List[Platform]
    field_name: str
    values: Dict[Platform, Any]
    suggested_resolution: Optional[str] = None
    priority: int = 1  # 1=high, 2=medium, 3=low

@dataclass
class BatchSyncRequest:
    """Batch sync request configuration"""
    businesses: List[str]  # Business IDs
    platforms: List[Platform]
    operations: List[SyncOperation]
    conflict_resolution: ConflictResolution = ConflictResolution.ASK_USER
    batch_size: int = 10
    delay_between_batches: float = 5.0

class MultiPlatformSyncEngine:
    """Main sync engine for coordinating multi-platform operations"""
    
    def __init__(self):
        self.platform_clients = {
            Platform.GOOGLE: google_business_client,
            Platform.YELP: yelp_client,
            Platform.FACEBOOK: facebook_client,
            Platform.APPLE_MAPS: apple_maps_client
        }
        
        self.data_mappers = {
            Platform.GOOGLE: GoogleDataMapper,
            Platform.YELP: YelpDataMapper,
            Platform.FACEBOOK: FacebookDataMapper,
            Platform.APPLE_MAPS: AppleMapsDataMapper
        }
    
    async def sync_business_to_platform(self, business_id: str, platform: Platform,
                                       operation: SyncOperation = SyncOperation.UPDATE,
                                       auth_data: Dict[str, Any] = None) -> SyncResult:
        """Sync a single business to a specific platform"""
        try:
            async with get_async_session() as session:
                # Get business data
                business = await self._get_business(session, business_id)
                if not business:
                    return SyncResult(
                        platform=platform,
                        operation=operation,
                        success=False,
                        error="Business not found"
                    )
                
                # Get platform-specific data
                platform_data = await self._get_platform_data(session, business_id, platform)
                
                # Execute platform-specific sync
                result = await self._sync_to_platform(
                    business, platform, operation, platform_data, auth_data
                )
                
                # Log sync operation
                await self._log_sync_operation(session, business_id, platform, operation, result)
                
                return result
                
        except Exception as e:
            logger.error(f"Sync failed for business {business_id} to {platform}: {str(e)}")
            return SyncResult(
                platform=platform,
                operation=operation,
                success=False,
                error=str(e)
            )
    
    async def sync_business_to_all_platforms(self, business_id: str,
                                           auth_data: Dict[Platform, Dict[str, Any]] = None,
                                           exclude_platforms: List[Platform] = None) -> List[SyncResult]:
        """Sync a business to all enabled platforms"""
        platforms = [p for p in Platform if p not in (exclude_platforms or [])]
        auth_data = auth_data or {}
        
        results = []
        for platform in platforms:
            result = await self.sync_business_to_platform(
                business_id, platform, SyncOperation.UPDATE, auth_data.get(platform)
            )
            results.append(result)
            
            # Add delay between platform syncs to avoid rate limits
            await asyncio.sleep(2)
        
        return results
    
    async def batch_sync(self, request: BatchSyncRequest,
                        auth_data: Dict[Platform, Dict[str, Any]] = None) -> List[SyncResult]:
        """Execute batch sync operations"""
        all_results = []
        auth_data = auth_data or {}
        
        # Process in batches
        for i in range(0, len(request.businesses), request.batch_size):
            batch_businesses = request.businesses[i:i + request.batch_size]
            batch_results = []
            
            # Process current batch
            for business_id in batch_businesses:
                for platform in request.platforms:
                    for operation in request.operations:
                        result = await self.sync_business_to_platform(
                            business_id, platform, operation, auth_data.get(platform)
                        )
                        batch_results.append(result)
                        
                        # Small delay between operations
                        await asyncio.sleep(0.5)
            
            all_results.extend(batch_results)
            
            # Delay between batches
            if i + request.batch_size < len(request.businesses):
                await asyncio.sleep(request.delay_between_batches)
        
        return all_results
    
    async def detect_conflicts(self, business_id: str) -> List[ConflictDetail]:
        """Detect conflicts across platforms for a business"""
        conflicts = []
        
        async with get_async_session() as session:
            # Get all platform data for the business
            platform_data = {}
            for platform in Platform:
                data = await self._get_platform_data(session, business_id, platform)
                if data:
                    platform_data[platform] = data
            
            if len(platform_data) < 2:
                return conflicts  # Need at least 2 platforms to detect conflicts
            
            # Check for name conflicts
            conflicts.extend(self._detect_field_conflicts(
                platform_data, "name", ConflictType.NAME_MISMATCH
            ))
            
            # Check for address conflicts
            conflicts.extend(self._detect_address_conflicts(platform_data))
            
            # Check for phone conflicts
            conflicts.extend(self._detect_field_conflicts(
                platform_data, "phone", ConflictType.PHONE_MISMATCH
            ))
            
            # Check for category conflicts
            conflicts.extend(self._detect_category_conflicts(platform_data))
            
            # Check for hours conflicts
            conflicts.extend(self._detect_hours_conflicts(platform_data))
        
        return conflicts
    
    async def resolve_conflict(self, business_id: str, conflict: ConflictDetail,
                             resolution_strategy: ConflictResolution,
                             preferred_value: Any = None) -> bool:
        """Resolve a specific conflict"""
        try:
            if resolution_strategy == ConflictResolution.USE_GOOGLE:
                source_platform = Platform.GOOGLE
            elif resolution_strategy == ConflictResolution.USE_LATEST:
                source_platform = await self._get_most_recent_platform(business_id, conflict.field_name)
            elif resolution_strategy == ConflictResolution.USE_PREFERRED and preferred_value is not None:
                # Apply preferred value to all platforms
                return await self._apply_value_to_platforms(
                    business_id, conflict.platforms, conflict.field_name, preferred_value
                )
            else:
                return False
            
            if source_platform in conflict.values:
                source_value = conflict.values[source_platform]
                target_platforms = [p for p in conflict.platforms if p != source_platform]
                
                return await self._apply_value_to_platforms(
                    business_id, target_platforms, conflict.field_name, source_value
                )
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to resolve conflict: {str(e)}")
            return False
    
    async def get_sync_status(self, business_id: str) -> Dict[Platform, Dict[str, Any]]:
        """Get sync status for all platforms"""
        status = {}
        
        async with get_async_session() as session:
            for platform in Platform:
                platform_business = await self._get_platform_business(session, business_id, platform)
                if platform_business:
                    status[platform] = {
                        "platform_id": platform_business.platform_id,
                        "last_synced": platform_business.last_synced,
                        "sync_status": platform_business.sync_status,
                        "last_error": platform_business.last_error,
                        "is_verified": platform_business.is_verified,
                        "is_claimed": platform_business.is_claimed
                    }
                else:
                    status[platform] = {
                        "platform_id": None,
                        "last_synced": None,
                        "sync_status": SyncStatus.NOT_SYNCED,
                        "last_error": None,
                        "is_verified": False,
                        "is_claimed": False
                    }
        
        return status
    
    async def schedule_sync(self, business_id: str, platforms: List[Platform],
                           schedule_time: datetime = None) -> str:
        """Schedule a sync operation for later execution"""
        schedule_time = schedule_time or datetime.utcnow()
        sync_id = str(uuid.uuid4())
        
        # In a real implementation, this would be stored in a task queue
        # For now, we'll store it in the database
        async with get_async_session() as session:
            sync_log = BusinessSyncLog(
                id=sync_id,
                business_id=business_id,
                platforms=",".join(platforms),
                operation=SyncOperation.UPDATE,
                scheduled_at=schedule_time,
                status=SyncStatus.PENDING
            )
            session.add(sync_log)
            await session.commit()
        
        return sync_id
    
    # Helper methods
    
    async def _sync_to_platform(self, business: Business, platform: Platform,
                               operation: SyncOperation, platform_data: Dict[str, Any],
                               auth_data: Dict[str, Any]) -> SyncResult:
        """Execute sync to specific platform"""
        client = self.platform_clients[platform]
        mapper = self.data_mappers[platform]
        
        try:
            if platform == Platform.GOOGLE:
                return await self._sync_to_google(business, operation, platform_data, auth_data)
            elif platform == Platform.YELP:
                return await self._sync_to_yelp(business, operation, platform_data, auth_data)
            elif platform == Platform.FACEBOOK:
                return await self._sync_to_facebook(business, operation, platform_data, auth_data)
            elif platform == Platform.APPLE_MAPS:
                return await self._sync_to_apple_maps(business, operation, platform_data, auth_data)
            else:
                return SyncResult(
                    platform=platform,
                    operation=operation,
                    success=False,
                    error=f"Unsupported platform: {platform}"
                )
                
        except Exception as e:
            return SyncResult(
                platform=platform,
                operation=operation,
                success=False,
                error=str(e)
            )
    
    async def _sync_to_google(self, business: Business, operation: SyncOperation,
                             platform_data: Dict[str, Any], auth_data: Dict[str, Any]) -> SyncResult:
        """Sync to Google Business Profile"""
        client = self.platform_clients[Platform.GOOGLE]
        
        if operation == SyncOperation.CREATE:
            # Create new Google listing
            google_data = GoogleDataMapper.create_business_payload(business.__dict__)
            response = await client.create_location(auth_data.get("account_id"), google_data)
            
            if response.success:
                return SyncResult(
                    platform=Platform.GOOGLE,
                    operation=operation,
                    success=True,
                    platform_id=response.data.get("name"),
                    data=response.data
                )
            else:
                return SyncResult(
                    platform=Platform.GOOGLE,
                    operation=operation,
                    success=False,
                    error=response.error
                )
        
        elif operation == SyncOperation.UPDATE and platform_data:
            # Update existing Google listing
            location_name = platform_data.get("platform_id")
            google_data = GoogleDataMapper.create_business_payload(business.__dict__)
            response = await client.update_location(location_name, google_data)
            
            return SyncResult(
                platform=Platform.GOOGLE,
                operation=operation,
                success=response.success,
                platform_id=location_name,
                error=response.error,
                data=response.data
            )
        
        return SyncResult(
            platform=Platform.GOOGLE,
            operation=operation,
            success=False,
            error="Invalid operation or missing platform data"
        )
    
    async def _sync_to_yelp(self, business: Business, operation: SyncOperation,
                           platform_data: Dict[str, Any], auth_data: Dict[str, Any]) -> SyncResult:
        """Sync to Yelp (read-only, claim existing listings)"""
        client = self.platform_clients[Platform.YELP]
        
        if operation == SyncOperation.CLAIM:
            # Search for existing business on Yelp
            response = await client.search_businesses(
                term=business.name,
                location=f"{business.city}, {business.state}"
            )
            
            if response.success and response.data.get("businesses"):
                # Find best match
                best_match = self._find_best_yelp_match(business, response.data["businesses"])
                if best_match:
                    return SyncResult(
                        platform=Platform.YELP,
                        operation=operation,
                        success=True,
                        platform_id=best_match["id"],
                        data=best_match
                    )
            
            return SyncResult(
                platform=Platform.YELP,
                operation=operation,
                success=False,
                error="No matching Yelp listing found"
            )
        
        return SyncResult(
            platform=Platform.YELP,
            operation=operation,
            success=False,
            error="Yelp only supports claiming existing listings"
        )
    
    async def _sync_to_facebook(self, business: Business, operation: SyncOperation,
                               platform_data: Dict[str, Any], auth_data: Dict[str, Any]) -> SyncResult:
        """Sync to Facebook Business Page"""
        client = self.platform_clients[Platform.FACEBOOK]
        access_token = auth_data.get("access_token")
        
        if not access_token:
            return SyncResult(
                platform=Platform.FACEBOOK,
                operation=operation,
                success=False,
                error="Facebook access token required"
            )
        
        if operation == SyncOperation.UPDATE and platform_data:
            # Update existing Facebook page
            page_id = platform_data.get("platform_id")
            facebook_data = FacebookDataMapper.create_update_payload(business.__dict__)
            response = await client.update_page_info(page_id, access_token, **facebook_data)
            
            return SyncResult(
                platform=Platform.FACEBOOK,
                operation=operation,
                success=response.success,
                platform_id=page_id,
                error=response.error,
                data=response.data
            )
        
        return SyncResult(
            platform=Platform.FACEBOOK,
            operation=operation,
            success=False,
            error="Facebook sync requires existing page"
        )
    
    async def _sync_to_apple_maps(self, business: Business, operation: SyncOperation,
                                 platform_data: Dict[str, Any], auth_data: Dict[str, Any]) -> SyncResult:
        """Sync to Apple Maps"""
        client = self.platform_clients[Platform.APPLE_MAPS]
        
        if operation == SyncOperation.CREATE:
            # Register new business with Apple Maps
            apple_data = AppleMapsDataMapper.create_business_registration_payload(business.__dict__)
            response = await client.register_business(apple_data)
            
            if response.success:
                return SyncResult(
                    platform=Platform.APPLE_MAPS,
                    operation=operation,
                    success=True,
                    platform_id=response.data.get("id"),
                    data=response.data
                )
            else:
                return SyncResult(
                    platform=Platform.APPLE_MAPS,
                    operation=operation,
                    success=False,
                    error=response.error
                )
        
        elif operation == SyncOperation.UPDATE and platform_data:
            # Update existing Apple Maps listing
            place_id = platform_data.get("platform_id")
            apple_data = AppleMapsDataMapper.create_business_registration_payload(business.__dict__)
            response = await client.update_business(place_id, apple_data)
            
            return SyncResult(
                platform=Platform.APPLE_MAPS,
                operation=operation,
                success=response.success,
                platform_id=place_id,
                error=response.error,
                data=response.data
            )
        
        return SyncResult(
            platform=Platform.APPLE_MAPS,
            operation=operation,
            success=False,
            error="Invalid operation or missing platform data"
        )
    
    def _detect_field_conflicts(self, platform_data: Dict[Platform, Dict[str, Any]],
                               field_name: str, conflict_type: ConflictType) -> List[ConflictDetail]:
        """Detect conflicts in a specific field across platforms"""
        conflicts = []
        values = {}
        
        for platform, data in platform_data.items():
            value = data.get(field_name)
            if value:
                values[platform] = value
        
        if len(set(str(v).lower() for v in values.values())) > 1:
            conflicts.append(ConflictDetail(
                conflict_type=conflict_type,
                platforms=list(values.keys()),
                field_name=field_name,
                values=values,
                priority=1 if field_name in ["name", "phone"] else 2
            ))
        
        return conflicts
    
    def _detect_address_conflicts(self, platform_data: Dict[Platform, Dict[str, Any]]) -> List[ConflictDetail]:
        """Detect address conflicts across platforms"""
        conflicts = []
        addresses = {}
        
        for platform, data in platform_data.items():
            location = data.get("location", {})
            formatted_address = location.get("formatted_address")
            if formatted_address:
                # Normalize address for comparison
                normalized = " ".join(formatted_address.lower().split())
                addresses[platform] = normalized
        
        if len(set(addresses.values())) > 1:
            conflicts.append(ConflictDetail(
                conflict_type=ConflictType.ADDRESS_MISMATCH,
                platforms=list(addresses.keys()),
                field_name="location.formatted_address",
                values=addresses,
                priority=1
            ))
        
        return conflicts
    
    def _detect_category_conflicts(self, platform_data: Dict[Platform, Dict[str, Any]]) -> List[ConflictDetail]:
        """Detect category conflicts across platforms"""
        conflicts = []
        categories = {}
        
        for platform, data in platform_data.items():
            platform_categories = data.get("categories", [])
            if platform_categories:
                # Use primary category (first one)
                primary_category = platform_categories[0] if isinstance(platform_categories, list) else platform_categories
                categories[platform] = str(primary_category).lower()
        
        if len(set(categories.values())) > 1:
            conflicts.append(ConflictDetail(
                conflict_type=ConflictType.CATEGORY_MISMATCH,
                platforms=list(categories.keys()),
                field_name="categories",
                values=categories,
                priority=2
            ))
        
        return conflicts
    
    def _detect_hours_conflicts(self, platform_data: Dict[Platform, Dict[str, Any]]) -> List[ConflictDetail]:
        """Detect hours conflicts across platforms"""
        # This is a simplified version - in reality, you'd need more sophisticated
        # hours comparison logic
        conflicts = []
        hours_data = {}
        
        for platform, data in platform_data.items():
            hours = data.get("hours", {})
            if hours:
                # Simple hash of hours for comparison
                hours_str = json.dumps(hours, sort_keys=True)
                hours_data[platform] = hours_str
        
        if len(set(hours_data.values())) > 1:
            conflicts.append(ConflictDetail(
                conflict_type=ConflictType.HOURS_MISMATCH,
                platforms=list(hours_data.keys()),
                field_name="hours",
                values=hours_data,
                priority=2
            ))
        
        return conflicts
    
    def _find_best_yelp_match(self, business: Business, yelp_businesses: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find the best matching Yelp business"""
        # Simple matching logic - in reality, you'd use more sophisticated matching
        for yelp_business in yelp_businesses:
            name_match = business.name.lower() in yelp_business.get("name", "").lower()
            location = yelp_business.get("location", {})
            city_match = business.city.lower() == location.get("city", "").lower()
            
            if name_match and city_match:
                return yelp_business
        
        return None
    
    async def _get_business(self, session: AsyncSession, business_id: str) -> Optional[Business]:
        """Get business by ID"""
        result = await session.execute(select(Business).where(Business.id == business_id))
        return result.scalar_one_or_none()
    
    async def _get_platform_data(self, session: AsyncSession, business_id: str, platform: Platform) -> Optional[Dict[str, Any]]:
        """Get platform-specific data for a business"""
        result = await session.execute(
            select(BusinessPlatform).where(
                and_(BusinessPlatform.business_id == business_id, BusinessPlatform.platform == platform)
            )
        )
        platform_business = result.scalar_one_or_none()
        return platform_business.platform_data if platform_business else None
    
    async def _get_platform_business(self, session: AsyncSession, business_id: str, platform: Platform) -> Optional[BusinessPlatform]:
        """Get BusinessPlatform record"""
        result = await session.execute(
            select(BusinessPlatform).where(
                and_(BusinessPlatform.business_id == business_id, BusinessPlatform.platform == platform)
            )
        )
        return result.scalar_one_or_none()
    
    async def _log_sync_operation(self, session: AsyncSession, business_id: str, platform: Platform,
                                 operation: SyncOperation, result: SyncResult):
        """Log sync operation"""
        sync_log = BusinessSyncLog(
            business_id=business_id,
            platform=platform,
            operation=operation,
            success=result.success,
            error_message=result.error,
            executed_at=datetime.utcnow()
        )
        session.add(sync_log)
        await session.commit()

# Global instance
sync_engine = MultiPlatformSyncEngine()