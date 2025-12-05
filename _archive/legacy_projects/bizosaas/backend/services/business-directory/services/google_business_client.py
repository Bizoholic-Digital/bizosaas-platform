"""
Google Business Profile API Client
Robust API client with rate limiting, error handling, and retry mechanisms
"""

import asyncio
import json
import logging
import time
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass

import httpx
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from circuitbreaker import circuit
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from ..models.google_integration import GoogleAccount, GoogleCacheEntry
from ..core.config import settings
from ..core.database import get_async_session
from .google_auth_service import google_auth_service

logger = logging.getLogger(__name__)


@dataclass
class APIResponse:
    """Structured API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    from_cache: bool = False


class RateLimiter:
    """Rate limiter for Google API calls"""
    
    def __init__(self, calls_per_minute: int = 600):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire rate limit permission"""
        async with self.lock:
            now = time.time()
            # Remove calls older than 1 minute
            self.calls = [call_time for call_time in self.calls if now - call_time < 60]
            
            if len(self.calls) >= self.calls_per_minute:
                # Calculate wait time
                oldest_call = min(self.calls)
                wait_time = 60 - (now - oldest_call)
                if wait_time > 0:
                    logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)
                    return await self.acquire()
            
            self.calls.append(now)


class GoogleBusinessClient:
    """
    Comprehensive Google Business Profile API client with robust error handling
    """
    
    def __init__(self):
        self.api_version = getattr(settings, 'GOOGLE_API_VERSION', 'v1')
        self.request_timeout = getattr(settings, 'GOOGLE_REQUEST_TIMEOUT', 30)
        self.max_retries = getattr(settings, 'GOOGLE_MAX_RETRIES', 3)
        self.rate_limiter = RateLimiter(
            calls_per_minute=getattr(settings, 'GOOGLE_RATE_LIMIT_PER_MINUTE', 600)
        )
        
        # Circuit breaker configuration
        self._circuit_failure_threshold = 5
        self._circuit_recovery_timeout = 60
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((HttpError, ConnectionError, TimeoutError))
    )
    async def get_business_locations(self, account: GoogleAccount) -> APIResponse:
        """
        Get all business locations for a Google account
        
        Args:
            account: GoogleAccount instance with valid credentials
            
        Returns:
            APIResponse with locations data
        """
        try:
            await self.rate_limiter.acquire()
            
            # Check cache first
            cache_key = f"locations_{account.google_account_id}"
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                return APIResponse(success=True, data=cached_response, from_cache=True)
            
            # Get valid credentials
            credentials = await google_auth_service.get_valid_credentials(account)
            if not credentials:
                return APIResponse(success=False, error="Invalid or expired credentials")
            
            # Build Google Business Profile API service
            service = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
            
            # Get accounts first
            accounts_result = service.accounts().list().execute()
            
            if not accounts_result.get('accounts'):
                return APIResponse(success=True, data={"locations": []})
            
            all_locations = []
            
            # Get locations for each account
            for google_account in accounts_result['accounts']:
                account_name = google_account['name']
                
                try:
                    locations_result = service.accounts().locations().list(
                        parent=account_name,
                        readMask="*"
                    ).execute()
                    
                    locations = locations_result.get('locations', [])
                    all_locations.extend(locations)
                    
                except HttpError as e:
                    if e.resp.status == 403:
                        logger.warning(f"No access to locations for account {account_name}")
                        continue
                    else:
                        raise
            
            response_data = {
                "locations": all_locations,
                "total_count": len(all_locations),
                "retrieved_at": datetime.utcnow().isoformat()
            }
            
            # Cache the response
            await self._save_to_cache(
                cache_key, 
                response_data, 
                ttl_minutes=30  # Cache for 30 minutes
            )
            
            logger.info(f"Retrieved {len(all_locations)} locations for account {account.email}")
            
            return APIResponse(success=True, data=response_data)
            
        except HttpError as e:
            error_msg = f"Google API error: {e.resp.status} - {e.content.decode()}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg, status_code=e.resp.status)
        except Exception as e:
            error_msg = f"Unexpected error getting locations: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((HttpError, ConnectionError, TimeoutError))
    )
    async def get_location_details(self, account: GoogleAccount, location_name: str) -> APIResponse:
        """
        Get detailed information for a specific location
        
        Args:
            account: GoogleAccount instance
            location_name: Google location resource name
            
        Returns:
            APIResponse with location details
        """
        try:
            await self.rate_limiter.acquire()
            
            # Check cache first
            cache_key = f"location_details_{location_name}"
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                return APIResponse(success=True, data=cached_response, from_cache=True)
            
            # Get valid credentials
            credentials = await google_auth_service.get_valid_credentials(account)
            if not credentials:
                return APIResponse(success=False, error="Invalid or expired credentials")
            
            # Build service
            service = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
            
            # Get location details
            location = service.accounts().locations().get(
                name=location_name,
                readMask="*"
            ).execute()
            
            # Cache the response
            await self._save_to_cache(
                cache_key,
                location,
                ttl_minutes=60  # Cache for 1 hour
            )
            
            logger.info(f"Retrieved details for location {location_name}")
            
            return APIResponse(success=True, data=location)
            
        except HttpError as e:
            error_msg = f"Google API error getting location details: {e.resp.status} - {e.content.decode()}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg, status_code=e.resp.status)
        except Exception as e:
            error_msg = f"Unexpected error getting location details: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((HttpError, ConnectionError, TimeoutError))
    )
    async def update_location(
        self, 
        account: GoogleAccount, 
        location_name: str, 
        update_data: Dict[str, Any]
    ) -> APIResponse:
        """
        Update a business location
        
        Args:
            account: GoogleAccount instance
            location_name: Google location resource name
            update_data: Data to update
            
        Returns:
            APIResponse with update result
        """
        try:
            await self.rate_limiter.acquire()
            
            # Get valid credentials
            credentials = await google_auth_service.get_valid_credentials(account)
            if not credentials:
                return APIResponse(success=False, error="Invalid or expired credentials")
            
            # Build service
            service = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
            
            # Prepare update mask based on provided data
            update_mask = ",".join(update_data.keys())
            
            # Update location
            updated_location = service.accounts().locations().patch(
                name=location_name,
                body=update_data,
                updateMask=update_mask
            ).execute()
            
            # Invalidate cache for this location
            cache_key = f"location_details_{location_name}"
            await self._invalidate_cache(cache_key)
            
            logger.info(f"Updated location {location_name}")
            
            return APIResponse(success=True, data=updated_location)
            
        except HttpError as e:
            error_msg = f"Google API error updating location: {e.resp.status} - {e.content.decode()}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg, status_code=e.resp.status)
        except Exception as e:
            error_msg = f"Unexpected error updating location: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    async def get_location_reviews(self, account: GoogleAccount, location_name: str) -> APIResponse:
        """
        Get reviews for a specific location
        
        Args:
            account: GoogleAccount instance
            location_name: Google location resource name
            
        Returns:
            APIResponse with reviews data
        """
        try:
            await self.rate_limiter.acquire()
            
            # Check cache first
            cache_key = f"location_reviews_{location_name}"
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                return APIResponse(success=True, data=cached_response, from_cache=True)
            
            # Get valid credentials
            credentials = await google_auth_service.get_valid_credentials(account)
            if not credentials:
                return APIResponse(success=False, error="Invalid or expired credentials")
            
            # Note: Google Business Profile API has limited review access
            # Reviews are mostly read-only and require special permissions
            logger.warning("Review access is limited in Google Business Profile API")
            
            return APIResponse(
                success=True, 
                data={"reviews": [], "note": "Review access limited by Google API"}
            )
            
        except Exception as e:
            error_msg = f"Error getting location reviews: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=Exception)
    async def get_location_insights(self, account: GoogleAccount, location_name: str) -> APIResponse:
        """
        Get insights/analytics for a specific location
        
        Args:
            account: GoogleAccount instance
            location_name: Google location resource name
            
        Returns:
            APIResponse with insights data
        """
        try:
            await self.rate_limiter.acquire()
            
            # Check cache first
            cache_key = f"location_insights_{location_name}"
            cached_response = await self._get_from_cache(cache_key)
            if cached_response:
                return APIResponse(success=True, data=cached_response, from_cache=True)
            
            # Get valid credentials
            credentials = await google_auth_service.get_valid_credentials(account)
            if not credentials:
                return APIResponse(success=False, error="Invalid or expired credentials")
            
            # Build Business Profile Performance API service
            try:
                service = build('mybusinessbusinessinformation', 'v1', credentials=credentials)
                
                # Get basic location data as insights
                location = service.accounts().locations().get(
                    name=location_name,
                    readMask="name,metadata"
                ).execute()
                
                insights_data = {
                    "location_name": location.get('name'),
                    "metadata": location.get('metadata', {}),
                    "retrieved_at": datetime.utcnow().isoformat(),
                    "note": "Full insights require Google Business Profile Performance API access"
                }
                
                # Cache the response
                await self._save_to_cache(
                    cache_key,
                    insights_data,
                    ttl_minutes=240  # Cache for 4 hours
                )
                
                return APIResponse(success=True, data=insights_data)
                
            except HttpError as e:
                if e.resp.status == 403:
                    return APIResponse(
                        success=False, 
                        error="Insights access requires additional API permissions"
                    )
                raise
            
        except Exception as e:
            error_msg = f"Error getting location insights: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    async def create_location_post(
        self, 
        account: GoogleAccount, 
        location_name: str, 
        post_data: Dict[str, Any]
    ) -> APIResponse:
        """
        Create a post for a business location
        
        Args:
            account: GoogleAccount instance
            location_name: Google location resource name
            post_data: Post content and settings
            
        Returns:
            APIResponse with post creation result
        """
        try:
            await self.rate_limiter.acquire()
            
            # Get valid credentials
            credentials = await google_auth_service.get_valid_credentials(account)
            if not credentials:
                return APIResponse(success=False, error="Invalid or expired credentials")
            
            # Note: Post creation requires Google My Business API v4
            # This is a placeholder for the implementation
            logger.info("Post creation functionality requires Google My Business API v4")
            
            return APIResponse(
                success=False, 
                error="Post creation not yet implemented - requires Google My Business API v4"
            )
            
        except Exception as e:
            error_msg = f"Error creating location post: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    async def batch_get_locations(
        self, 
        account: GoogleAccount, 
        location_names: List[str]
    ) -> APIResponse:
        """
        Get multiple locations in a batch request
        
        Args:
            account: GoogleAccount instance
            location_names: List of Google location resource names
            
        Returns:
            APIResponse with batch location data
        """
        try:
            # Process in chunks to respect API limits
            chunk_size = 10
            all_locations = []
            
            for i in range(0, len(location_names), chunk_size):
                chunk = location_names[i:i + chunk_size]
                
                # Process each location in the chunk
                chunk_results = []
                for location_name in chunk:
                    result = await self.get_location_details(account, location_name)
                    if result.success:
                        chunk_results.append(result.data)
                    else:
                        logger.warning(f"Failed to get details for {location_name}: {result.error}")
                
                all_locations.extend(chunk_results)
                
                # Add small delay between chunks
                if i + chunk_size < len(location_names):
                    await asyncio.sleep(0.1)
            
            return APIResponse(
                success=True, 
                data={
                    "locations": all_locations,
                    "total_requested": len(location_names),
                    "total_retrieved": len(all_locations)
                }
            )
            
        except Exception as e:
            error_msg = f"Error in batch get locations: {str(e)}"
            logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    async def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get data from cache"""
        try:
            async with get_async_session() as session:
                from sqlalchemy import select
                
                result = await session.execute(
                    select(GoogleCacheEntry)
                    .where(GoogleCacheEntry.cache_key == cache_key)
                )
                cache_entry = result.scalar_one_or_none()
                
                if cache_entry and not cache_entry.is_expired:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return cache_entry.response_data
                elif cache_entry and cache_entry.is_expired:
                    # Clean up expired entry
                    await session.delete(cache_entry)
                    await session.commit()
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting from cache: {str(e)}")
            return None
    
    async def _save_to_cache(
        self, 
        cache_key: str, 
        data: Dict[str, Any], 
        ttl_minutes: int = 60
    ):
        """Save data to cache"""
        try:
            async with get_async_session() as session:
                from sqlalchemy import delete
                
                # Remove existing entry
                await session.execute(
                    delete(GoogleCacheEntry).where(GoogleCacheEntry.cache_key == cache_key)
                )
                
                # Create new entry
                cache_entry = GoogleCacheEntry(
                    cache_key=cache_key,
                    endpoint="google_business_api",
                    response_data=data,
                    expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes)
                )
                session.add(cache_entry)
                await session.commit()
                
                logger.debug(f"Cached data for key: {cache_key}")
                
        except Exception as e:
            logger.error(f"Error saving to cache: {str(e)}")
    
    async def _invalidate_cache(self, cache_key: str):
        """Invalidate cache entry"""
        try:
            async with get_async_session() as session:
                from sqlalchemy import delete
                
                await session.execute(
                    delete(GoogleCacheEntry).where(GoogleCacheEntry.cache_key == cache_key)
                )
                await session.commit()
                
                logger.debug(f"Invalidated cache for key: {cache_key}")
                
        except Exception as e:
            logger.error(f"Error invalidating cache: {str(e)}")
    
    async def get_api_quota_status(self) -> Dict[str, Any]:
        """
        Get current API quota usage status
        
        Returns:
            Dictionary with quota information
        """
        try:
            # This is a simplified quota tracking
            # In production, you'd want more sophisticated quota monitoring
            
            current_minute = int(time.time() // 60)
            calls_this_minute = len([
                call_time for call_time in self.rate_limiter.calls 
                if int(call_time // 60) == current_minute
            ])
            
            return {
                "calls_this_minute": calls_this_minute,
                "rate_limit": self.rate_limiter.calls_per_minute,
                "remaining_calls": max(0, self.rate_limiter.calls_per_minute - calls_this_minute),
                "reset_time": (current_minute + 1) * 60
            }
            
        except Exception as e:
            logger.error(f"Error getting quota status: {str(e)}")
            return {"error": str(e)}


# Service instance
google_business_client = GoogleBusinessClient()