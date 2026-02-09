"""
Advanced Multi-Platform Sync Orchestrator
Enhanced version using the platform abstraction layer for 15+ platforms
"""

import asyncio
import json
import logging
from enum import Enum
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from ..models.business import Business, BusinessPlatform, BusinessSyncLog
from ..models.base import SyncStatus, ConflictResolution
from ..core.database import get_async_session
from ..core.config import settings
from ..platform_abstraction.platform_factory import get_platform_factory, PlatformFactory
from ..platform_abstraction.platform_registry import get_platform_registry, PlatformRegistry, PlatformTier
from ..platform_abstraction.base_platform_client import (
    BasePlatformClient, PlatformResponse, AuthCredentials, SyncOperation
)
from ..platform_abstraction.unified_data_models import (
    UniversalBusinessData, UniversalSyncMapping
)

logger = logging.getLogger(__name__)

class SyncStrategy(str, Enum):
    """Sync strategy types"""
    AGGRESSIVE = "aggressive"  # Sync to all available platforms
    CONSERVATIVE = "conservative"  # Sync to Tier 1 platforms only
    SELECTIVE = "selective"  # Sync based on business type/location
    CUSTOM = "custom"  # Custom platform selection

class SyncPriority(str, Enum):
    """Sync priority levels"""
    CRITICAL = "critical"  # Must complete successfully
    HIGH = "high"  # Important but can fail
    MEDIUM = "medium"  # Nice to have
    LOW = "low"  # Background sync

@dataclass
class SyncRequest:
    """Enhanced sync request with platform intelligence"""
    business_id: str
    strategy: SyncStrategy = SyncStrategy.CONSERVATIVE
    operations: List[SyncOperation] = field(default_factory=list)
    platforms: Optional[List[str]] = None  # If None, auto-select
    priority: SyncPriority = SyncPriority.MEDIUM
    conflict_resolution: ConflictResolution = ConflictResolution.ASK_USER
    max_concurrent: int = 3  # Max concurrent platform operations
    retry_failed: bool = True
    notify_on_completion: bool = True
    
    def __post_init__(self):
        if not self.operations:
            self.operations = [SyncOperation.UPDATE]

@dataclass
class SyncResult:
    """Enhanced sync result with detailed analytics"""
    business_id: str
    request_id: str
    overall_success: bool
    total_platforms: int
    successful_platforms: int
    failed_platforms: int
    platform_results: Dict[str, PlatformResponse] = field(default_factory=dict)
    conflicts_detected: int = 0
    conflicts_resolved: int = 0
    execution_time: float = 0.0
    cost_estimate: float = 0.0  # API cost estimate
    recommendations: List[str] = field(default_factory=list)

@dataclass
class PlatformRecommendation:
    """AI-powered platform recommendation"""
    platform: str
    priority: SyncPriority
    rationale: str
    expected_roi: float
    estimated_setup_time: int  # in minutes

class AdvancedMultiPlatformOrchestrator:
    """
    Advanced orchestrator for managing sync across 15+ platforms
    with AI-powered recommendations and intelligent conflict resolution
    """
    
    def __init__(self):
        self.factory: PlatformFactory = get_platform_factory()
        self.registry: PlatformRegistry = get_platform_registry()
        self._active_syncs: Dict[str, SyncRequest] = {}
        self._sync_history: List[SyncResult] = []
        
    async def sync_business_intelligent(self, request: SyncRequest,
                                      auth_data: Dict[str, AuthCredentials] = None) -> SyncResult:
        """
        Intelligent business sync with auto-platform selection and optimization
        
        Args:
            request: Sync request configuration
            auth_data: Authentication data by platform
            
        Returns:
            Comprehensive sync result
        """
        request_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        auth_data = auth_data or {}
        
        logger.info(f"Starting intelligent sync {request_id} for business {request.business_id}")
        
        try:
            # Store active sync
            self._active_syncs[request_id] = request
            
            # Get business data
            async with get_async_session() as session:
                business = await self._get_business(session, request.business_id)
                if not business:
                    return SyncResult(
                        business_id=request.business_id,
                        request_id=request_id,
                        overall_success=False,
                        total_platforms=0,
                        successful_platforms=0,
                        failed_platforms=0,
                        recommendations=["Business not found in database"]
                    )
                
                # Convert to universal format
                universal_data = await self._convert_to_universal(business)
                
                # Select platforms intelligently
                target_platforms = await self._select_platforms_intelligently(
                    request, universal_data, auth_data
                )
                
                # Execute sync operations
                platform_results = await self._execute_parallel_sync(
                    universal_data, target_platforms, request.operations, 
                    auth_data, request.max_concurrent
                )
                
                # Analyze results and detect conflicts
                conflicts = await self._analyze_sync_results(
                    platform_results, universal_data
                )
                
                # Generate recommendations
                recommendations = await self._generate_recommendations(
                    platform_results, universal_data, conflicts
                )
                
                # Calculate execution time
                execution_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Create comprehensive result
                successful = sum(1 for r in platform_results.values() if r.success)
                failed = len(platform_results) - successful
                
                result = SyncResult(
                    business_id=request.business_id,
                    request_id=request_id,
                    overall_success=failed == 0,
                    total_platforms=len(platform_results),
                    successful_platforms=successful,
                    failed_platforms=failed,
                    platform_results=platform_results,
                    conflicts_detected=len(conflicts),
                    conflicts_resolved=0,  # Will be updated after resolution
                    execution_time=execution_time,
                    recommendations=recommendations
                )
                
                # Log results
                await self._log_sync_results(session, result)
                
                # Store in history
                self._sync_history.append(result)
                
                logger.info(
                    f"Sync {request_id} completed: {successful}/{len(platform_results)} platforms successful"
                )
                
                return result
                
        except Exception as e:
            logger.error(f"Sync {request_id} failed with error: {str(e)}")
            return SyncResult(
                business_id=request.business_id,
                request_id=request_id,
                overall_success=False,
                total_platforms=0,
                successful_platforms=0,
                failed_platforms=0,
                recommendations=[f"Sync failed with error: {str(e)}"]
            )
        
        finally:
            # Cleanup
            if request_id in self._active_syncs:
                del self._active_syncs[request_id]
    
    async def _select_platforms_intelligently(self, request: SyncRequest,
                                            universal_data: UniversalBusinessData,
                                            auth_data: Dict[str, AuthCredentials]) -> List[str]:
        """
        Intelligently select platforms based on business data and strategy
        
        Args:
            request: Sync request
            universal_data: Business data in universal format
            auth_data: Available authentication data
            
        Returns:
            List of selected platform names
        """
        if request.platforms:
            # Use explicitly provided platforms
            return request.platforms
        
        selected_platforms = []
        
        if request.strategy == SyncStrategy.AGGRESSIVE:
            # Use all available platforms with auth data
            selected_platforms = [
                platform for platform in auth_data.keys()
                if platform in self.registry.list_platforms()
            ]
            
        elif request.strategy == SyncStrategy.CONSERVATIVE:
            # Use only Tier 1 platforms
            tier_1_platforms = self.registry.get_tier_1_platforms()
            selected_platforms = [
                platform for platform in tier_1_platforms
                if platform in auth_data
            ]
            
        elif request.strategy == SyncStrategy.SELECTIVE:
            # Use AI-powered recommendations
            recommendations = await self._get_ai_platform_recommendations(
                universal_data, auth_data
            )
            selected_platforms = [r.platform for r in recommendations[:10]]  # Top 10
            
        else:  # CUSTOM
            # Use factory recommendations
            selected_platforms = self.factory.get_recommended_platforms_for_business(
                universal_data
            )
            # Filter by available auth data
            selected_platforms = [
                platform for platform in selected_platforms
                if platform in auth_data
            ]
        
        logger.info(f"Selected {len(selected_platforms)} platforms: {selected_platforms}")
        return selected_platforms
    
    async def _execute_parallel_sync(self, universal_data: UniversalBusinessData,
                                   platforms: List[str], operations: List[SyncOperation],
                                   auth_data: Dict[str, AuthCredentials],
                                   max_concurrent: int) -> Dict[str, PlatformResponse]:
        """
        Execute sync operations in parallel with concurrency control
        
        Args:
            universal_data: Business data to sync
            platforms: Target platforms
            operations: Operations to perform
            auth_data: Authentication data
            max_concurrent: Maximum concurrent operations
            
        Returns:
            Results by platform
        """
        results = {}
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def sync_platform(platform_name: str) -> Tuple[str, PlatformResponse]:
            async with semaphore:
                try:
                    client = self.factory.get_platform_client(platform_name)
                    if not client:
                        return platform_name, PlatformResponse(
                            success=False,
                            operation=operations[0],
                            platform=platform_name,
                            error="Platform client not available"
                        )
                    
                    credentials = auth_data.get(platform_name)
                    if not credentials:
                        return platform_name, PlatformResponse(
                            success=False,
                            operation=operations[0],
                            platform=platform_name,
                            error="No authentication credentials provided"
                        )
                    
                    # Execute primary operation
                    primary_op = operations[0]
                    
                    if primary_op == SyncOperation.CREATE:
                        response = await client.create_listing(universal_data, credentials)
                    elif primary_op == SyncOperation.UPDATE:
                        # Need to get platform ID first
                        platform_id = await self._get_platform_id(
                            universal_data.attributes.get("business_id", ""), platform_name
                        )
                        if platform_id:
                            response = await client.update_listing(platform_id, universal_data, credentials)
                        else:
                            # Try to create instead
                            response = await client.create_listing(universal_data, credentials)
                    elif primary_op == SyncOperation.SEARCH:
                        response = await client.search_listings(
                            universal_data.name,
                            f"{universal_data.location.city}, {universal_data.location.state}" if universal_data.location else "",
                            credentials
                        )
                    else:
                        response = PlatformResponse(
                            success=False,
                            operation=primary_op,
                            platform=platform_name,
                            error=f"Operation {primary_op} not supported by orchestrator"
                        )
                    
                    return platform_name, response
                    
                except Exception as e:
                    return platform_name, PlatformResponse(
                        success=False,
                        operation=operations[0],
                        platform=platform_name,
                        error=f"Sync failed: {str(e)}"
                    )
        
        # Execute all platform syncs in parallel
        tasks = [sync_platform(platform) for platform in platforms]
        completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for task_result in completed_tasks:
            if isinstance(task_result, Exception):
                logger.error(f"Task failed with exception: {str(task_result)}")
                continue
            
            platform_name, response = task_result
            results[platform_name] = response
        
        return results
    
    async def _get_ai_platform_recommendations(self, universal_data: UniversalBusinessData,
                                             auth_data: Dict[str, AuthCredentials]) -> List[PlatformRecommendation]:
        """
        Get AI-powered platform recommendations based on business data
        
        Args:
            universal_data: Business data
            auth_data: Available authentication
            
        Returns:
            List of platform recommendations
        """
        recommendations = []
        
        # Business type specific recommendations
        business_type = universal_data.categories.business_type if universal_data.categories else None
        location = universal_data.location
        
        # Tier 1 platforms - always recommend if auth available
        tier_1_platforms = self.registry.get_tier_1_platforms()
        for platform in tier_1_platforms:
            if platform in auth_data:
                rationale = f"Tier 1 platform with high market reach"
                roi = 0.8  # High ROI
                if business_type and business_type.value == "restaurant" and platform == "yelp":
                    roi = 0.95  # Very high for restaurants
                elif business_type and business_type.value == "hospitality" and platform == "tripadvisor":
                    roi = 0.90  # Very high for hospitality
                
                recommendations.append(PlatformRecommendation(
                    platform=platform,
                    priority=SyncPriority.CRITICAL,
                    rationale=rationale,
                    expected_roi=roi,
                    estimated_setup_time=15
                ))
        
        # Business type specific platforms
        if business_type:
            if business_type.value == "restaurant":
                if "tripadvisor" in auth_data:
                    recommendations.append(PlatformRecommendation(
                        platform="tripadvisor",
                        priority=SyncPriority.HIGH,
                        rationale="Essential for restaurant visibility",
                        expected_roi=0.85,
                        estimated_setup_time=20
                    ))
            
            elif business_type.value == "hospitality":
                for platform in ["tripadvisor"]:
                    if platform in auth_data:
                        recommendations.append(PlatformRecommendation(
                            platform=platform,
                            priority=SyncPriority.HIGH,
                            rationale="Critical for hospitality business",
                            expected_roi=0.90,
                            estimated_setup_time=25
                        ))
        
        # Geographic recommendations
        if location and location.country == "US":
            us_platforms = ["yellow_pages", "superpages"]
            for platform in us_platforms:
                if platform in auth_data:
                    recommendations.append(PlatformRecommendation(
                        platform=platform,
                        priority=SyncPriority.MEDIUM,
                        rationale="Strong US market presence",
                        expected_roi=0.6,
                        estimated_setup_time=10
                    ))
        
        # Sort by expected ROI
        recommendations.sort(key=lambda x: x.expected_roi, reverse=True)
        
        return recommendations
    
    async def _analyze_sync_results(self, platform_results: Dict[str, PlatformResponse],
                                  universal_data: UniversalBusinessData) -> List[Dict[str, Any]]:
        """
        Analyze sync results to detect conflicts and issues
        
        Args:
            platform_results: Results from platform sync operations
            universal_data: Original business data
            
        Returns:
            List of detected conflicts
        """
        conflicts = []
        
        # Analyze successful results for data conflicts
        successful_results = {
            platform: result for platform, result in platform_results.items()
            if result.success and result.data
        }
        
        if len(successful_results) > 1:
            # Compare data across platforms to detect conflicts
            data_fields = ["name", "address", "phone", "website"]
            
            for field in data_fields:
                values = {}
                for platform, result in successful_results.items():
                    platform_data = result.data.get("universal_data", {})
                    if field in platform_data:
                        values[platform] = platform_data[field]
                
                # Check for conflicts in this field
                unique_values = set(str(v).lower() for v in values.values() if v)
                if len(unique_values) > 1:
                    conflicts.append({
                        "type": f"{field}_conflict",
                        "field": field,
                        "platforms": list(values.keys()),
                        "values": values,
                        "severity": "high" if field in ["name", "phone"] else "medium"
                    })
        
        return conflicts
    
    async def _generate_recommendations(self, platform_results: Dict[str, PlatformResponse],
                                      universal_data: UniversalBusinessData,
                                      conflicts: List[Dict[str, Any]]) -> List[str]:
        """
        Generate actionable recommendations based on sync results
        
        Args:
            platform_results: Platform sync results
            universal_data: Business data
            conflicts: Detected conflicts
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Analyze success rate
        total_platforms = len(platform_results)
        successful_platforms = sum(1 for r in platform_results.values() if r.success)
        success_rate = successful_platforms / total_platforms if total_platforms > 0 else 0
        
        if success_rate < 0.5:
            recommendations.append(
                "Low success rate detected. Consider reviewing API credentials and platform configurations."
            )
        elif success_rate < 0.8:
            recommendations.append(
                "Moderate success rate. Some platforms may require additional setup or verification."
            )
        
        # Analyze failed platforms
        failed_platforms = [
            platform for platform, result in platform_results.items()
            if not result.success
        ]
        
        if failed_platforms:
            auth_failures = [
                platform for platform, result in platform_results.items()
                if not result.success and "auth" in result.error.lower()
            ]
            
            if auth_failures:
                recommendations.append(
                    f"Authentication issues detected for: {', '.join(auth_failures)}. "
                    "Please verify API credentials."
                )
        
        # Conflict analysis
        if conflicts:
            high_severity_conflicts = [c for c in conflicts if c.get("severity") == "high"]
            if high_severity_conflicts:
                recommendations.append(
                    f"Critical data conflicts detected in {len(high_severity_conflicts)} fields. "
                    "Immediate review recommended to ensure data consistency."
                )
            else:
                recommendations.append(
                    f"{len(conflicts)} minor data conflicts detected. "
                    "Consider reviewing data consistency across platforms."
                )
        
        # Platform coverage recommendations
        tier_1_coverage = len([
            platform for platform in platform_results.keys()
            if platform in self.registry.get_tier_1_platforms()
        ])
        
        if tier_1_coverage < 3:
            recommendations.append(
                "Limited Tier 1 platform coverage. Consider adding more primary platforms "
                "for maximum market reach."
            )
        
        # Business-specific recommendations
        if universal_data.categories and universal_data.categories.business_type:
            business_type = universal_data.categories.business_type.value
            
            if business_type == "restaurant" and "tripadvisor" not in platform_results:
                recommendations.append(
                    "Restaurant businesses benefit significantly from TripAdvisor presence. "
                    "Consider adding TripAdvisor integration."
                )
            
            elif business_type == "hospitality" and "tripadvisor" not in platform_results:
                recommendations.append(
                    "Hospitality businesses should prioritize TripAdvisor for customer acquisition."
                )
        
        return recommendations
    
    async def get_sync_analytics(self, business_id: Optional[str] = None,
                               timeframe_days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive sync analytics
        
        Args:
            business_id: Optional business filter
            timeframe_days: Analysis timeframe
            
        Returns:
            Analytics dashboard data
        """
        cutoff_date = datetime.utcnow() - timedelta(days=timeframe_days)
        
        # Filter sync history
        relevant_syncs = [
            sync for sync in self._sync_history
            if (not business_id or sync.business_id == business_id)
        ]
        
        if not relevant_syncs:
            return {
                "total_syncs": 0,
                "success_rate": 0,
                "platform_performance": {},
                "recommendations": ["No sync data available for analysis"]
            }
        
        # Calculate metrics
        total_syncs = len(relevant_syncs)
        successful_syncs = sum(1 for sync in relevant_syncs if sync.overall_success)
        success_rate = successful_syncs / total_syncs
        
        # Platform performance analysis
        platform_stats = defaultdict(lambda: {"attempts": 0, "successes": 0})
        
        for sync in relevant_syncs:
            for platform, result in sync.platform_results.items():
                platform_stats[platform]["attempts"] += 1
                if result.success:
                    platform_stats[platform]["successes"] += 1
        
        platform_performance = {}
        for platform, stats in platform_stats.items():
            platform_performance[platform] = {
                "success_rate": stats["successes"] / stats["attempts"] if stats["attempts"] > 0 else 0,
                "total_attempts": stats["attempts"],
                "successful_attempts": stats["successes"]
            }
        
        # Average execution time
        avg_execution_time = sum(sync.execution_time for sync in relevant_syncs) / total_syncs
        
        # Most common conflicts
        all_conflicts = []
        for sync in relevant_syncs:
            all_conflicts.extend([f["type"] for f in sync.platform_results.values() if hasattr(f, 'conflicts')])
        
        conflict_frequency = defaultdict(int)
        for conflict in all_conflicts:
            conflict_frequency[conflict] += 1
        
        return {
            "total_syncs": total_syncs,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "platform_performance": platform_performance,
            "conflict_frequency": dict(conflict_frequency),
            "most_reliable_platforms": sorted(
                platform_performance.items(),
                key=lambda x: x[1]["success_rate"],
                reverse=True
            )[:5],
            "least_reliable_platforms": sorted(
                platform_performance.items(),
                key=lambda x: x[1]["success_rate"]
            )[:3],
            "recommendations": self._generate_analytics_recommendations(
                success_rate, platform_performance, conflict_frequency
            )
        }
    
    def _generate_analytics_recommendations(self, success_rate: float,
                                          platform_performance: Dict[str, Dict[str, Any]],
                                          conflict_frequency: Dict[str, int]) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        if success_rate < 0.7:
            recommendations.append(
                "Overall success rate is below optimal. Consider reviewing platform configurations."
            )
        
        # Find problematic platforms
        problematic_platforms = [
            platform for platform, stats in platform_performance.items()
            if stats["success_rate"] < 0.6 and stats["total_attempts"] > 5
        ]
        
        if problematic_platforms:
            recommendations.append(
                f"These platforms show consistent issues: {', '.join(problematic_platforms)}. "
                "Consider reviewing their integration or temporarily disabling them."
            )
        
        return recommendations
    
    async def _get_business(self, session: AsyncSession, business_id: str) -> Optional[Business]:
        """Get business by ID"""
        result = await session.execute(select(Business).where(Business.id == business_id))
        return result.scalar_one_or_none()
    
    async def _convert_to_universal(self, business: Business) -> UniversalBusinessData:
        """Convert business model to universal format"""
        # This would convert the database Business model to UniversalBusinessData
        # Implementation depends on your Business model structure
        return UniversalBusinessData(
            name=business.name,
            description=business.description,
            # ... map other fields
        )
    
    async def _get_platform_id(self, business_id: str, platform: str) -> Optional[str]:
        """Get platform-specific ID for a business"""
        async with get_async_session() as session:
            result = await session.execute(
                select(BusinessPlatform).where(
                    and_(
                        BusinessPlatform.business_id == business_id,
                        BusinessPlatform.platform == platform
                    )
                )
            )
            platform_business = result.scalar_one_or_none()
            return platform_business.platform_id if platform_business else None
    
    async def _log_sync_results(self, session: AsyncSession, result: SyncResult):
        """Log sync results to database"""
        for platform, response in result.platform_results.items():
            sync_log = BusinessSyncLog(
                business_id=result.business_id,
                platform=platform,
                operation=response.operation,
                success=response.success,
                error_message=response.error,
                executed_at=datetime.utcnow(),
                request_id=result.request_id
            )
            session.add(sync_log)
        
        await session.commit()

# Global orchestrator instance
advanced_orchestrator = AdvancedMultiPlatformOrchestrator()