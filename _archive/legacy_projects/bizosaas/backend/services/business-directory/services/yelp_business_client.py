"""
Yelp Fusion API Client
Handles business listing sync with Yelp using Yelp Fusion API
"""

import asyncio
import json
import logging
import time
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from circuitbreaker import circuit

from ..models.base import PlatformIntegration
from ..core.config import settings
from ..core.database import get_async_session

logger = logging.getLogger(__name__)

@dataclass
class YelpAPIResponse:
    """Structured Yelp API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    rate_limit_remaining: Optional[int] = None

class YelpRateLimiter:
    """Rate limiter for Yelp API calls"""
    
    def __init__(self, calls_per_second: int = 5):
        self.calls_per_second = calls_per_second
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire rate limit permission"""
        async with self.lock:
            now = time.time()
            # Remove calls older than 1 second
            self.calls = [call for call in self.calls if now - call < 1.0]
            
            if len(self.calls) >= self.calls_per_second:
                sleep_time = 1.0 - (now - self.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    return await self.acquire()
            
            self.calls.append(now)

class YelpBusinessClient:
    """Yelp Fusion API client for business management"""
    
    def __init__(self):
        self.base_url = "https://api.yelp.com/v3"
        self.rate_limiter = YelpRateLimiter()
        self.session = None
        
    async def get_session(self) -> httpx.AsyncClient:
        """Get HTTP session with authentication"""
        if not self.session:
            headers = {
                "Authorization": f"Bearer {settings.YELP_API_KEY}",
                "Content-Type": "application/json"
            }
            self.session = httpx.AsyncClient(
                headers=headers,
                timeout=30.0,
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )
        return self.session
    
    @circuit(failure_threshold=5, recovery_timeout=60)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> YelpAPIResponse:
        """Make API request with retry and circuit breaker"""
        await self.rate_limiter.acquire()
        
        session = await self.get_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = await session.request(method, url, **kwargs)
            
            # Check rate limiting headers
            rate_limit_remaining = response.headers.get("RateLimit-Remaining")
            
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                logger.warning(f"Yelp API rate limit exceeded. Retry after {retry_after} seconds")
                await asyncio.sleep(retry_after)
                return await self._make_request(method, endpoint, **kwargs)
            
            response.raise_for_status()
            
            return YelpAPIResponse(
                success=True,
                data=response.json() if response.content else {},
                status_code=response.status_code,
                rate_limit_remaining=int(rate_limit_remaining) if rate_limit_remaining else None
            )
            
        except httpx.HTTPStatusError as e:
            error_msg = f"Yelp API HTTP error: {e.response.status_code}"
            if e.response.content:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('description', '')}"
                except:
                    pass
                    
            logger.error(error_msg)
            return YelpAPIResponse(
                success=False,
                error=error_msg,
                status_code=e.response.status_code
            )
            
        except Exception as e:
            logger.error(f"Yelp API request failed: {str(e)}")
            return YelpAPIResponse(success=False, error=str(e))
    
    async def search_businesses(self, term: str = None, location: str = None, 
                              latitude: float = None, longitude: float = None,
                              radius: int = None, categories: str = None,
                              limit: int = 20, offset: int = 0) -> YelpAPIResponse:
        """Search for businesses on Yelp"""
        params = {"limit": min(limit, 50), "offset": offset}
        
        if term:
            params["term"] = term
        if location:
            params["location"] = location
        if latitude and longitude:
            params["latitude"] = latitude
            params["longitude"] = longitude
        if radius:
            params["radius"] = min(radius, 40000)  # Max 40km
        if categories:
            params["categories"] = categories
        
        return await self._make_request("GET", "businesses/search", params=params)
    
    async def get_business_details(self, business_id: str) -> YelpAPIResponse:
        """Get detailed business information"""
        return await self._make_request("GET", f"businesses/{business_id}")
    
    async def get_business_reviews(self, business_id: str, locale: str = "en_US") -> YelpAPIResponse:
        """Get business reviews"""
        params = {"locale": locale}
        return await self._make_request("GET", f"businesses/{business_id}/reviews", params=params)
    
    async def autocomplete(self, text: str, latitude: float = None, 
                          longitude: float = None) -> YelpAPIResponse:
        """Get autocomplete suggestions"""
        params = {"text": text}
        if latitude and longitude:
            params["latitude"] = latitude
            params["longitude"] = longitude
        
        return await self._make_request("GET", "autocomplete", params=params)
    
    async def get_categories(self, locale: str = "en_US") -> YelpAPIResponse:
        """Get list of Yelp categories"""
        params = {"locale": locale}
        return await self._make_request("GET", "categories", params=params)
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None

# Platform-specific data mappers
class YelpDataMapper:
    """Maps Yelp API responses to our unified business data format"""
    
    @staticmethod
    def map_business_from_search(yelp_business: Dict[str, Any]) -> Dict[str, Any]:
        """Map Yelp search result to unified business format"""
        coordinates = yelp_business.get("coordinates", {})
        location = yelp_business.get("location", {})
        
        return {
            "platform": "yelp",
            "platform_id": yelp_business.get("id"),
            "name": yelp_business.get("name"),
            "alias": yelp_business.get("alias"),
            "description": None,  # Not available in search results
            "phone": yelp_business.get("phone"),
            "website_url": yelp_business.get("url"),
            "image_url": yelp_business.get("image_url"),
            "rating": yelp_business.get("rating"),
            "review_count": yelp_business.get("review_count"),
            "price": yelp_business.get("price"),
            "categories": [cat.get("title") for cat in yelp_business.get("categories", [])],
            "is_closed": yelp_business.get("is_closed"),
            "location": {
                "address": location.get("address1"),
                "address2": location.get("address2"),
                "city": location.get("city"),
                "state": location.get("state"),
                "postal_code": location.get("zip_code"),
                "country": location.get("country"),
                "formatted_address": ", ".join(filter(None, [
                    location.get("address1"),
                    location.get("city"),
                    location.get("state"),
                    location.get("zip_code")
                ]))
            },
            "coordinates": {
                "latitude": coordinates.get("latitude"),
                "longitude": coordinates.get("longitude")
            },
            "platform_data": {
                "transactions": yelp_business.get("transactions", []),
                "distance": yelp_business.get("distance")
            }
        }
    
    @staticmethod
    def map_business_details(yelp_business: Dict[str, Any]) -> Dict[str, Any]:
        """Map detailed Yelp business data to unified format"""
        base_data = YelpDataMapper.map_business_from_search(yelp_business)
        
        # Add detailed information
        hours = yelp_business.get("hours", [])
        if hours:
            hours_data = hours[0].get("open", [])
            base_data["hours"] = {
                "periods": [
                    {
                        "day": period.get("day"),
                        "start": period.get("start"),
                        "end": period.get("end")
                    }
                    for period in hours_data
                ],
                "is_open_now": hours[0].get("is_open_now")
            }
        
        # Add photos
        base_data["photos"] = yelp_business.get("photos", [])
        
        # Add special hours
        special_hours = yelp_business.get("special_hours", [])
        if special_hours:
            base_data["special_hours"] = special_hours
        
        # Update platform data with more details
        base_data["platform_data"].update({
            "messaging": yelp_business.get("messaging"),
            "attributes": yelp_business.get("attributes", {})
        })
        
        return base_data
    
    @staticmethod
    def map_reviews(yelp_reviews: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Yelp reviews to unified format"""
        reviews = []
        for review in yelp_reviews.get("reviews", []):
            user = review.get("user", {})
            reviews.append({
                "platform": "yelp",
                "review_id": review.get("id"),
                "author_name": user.get("name"),
                "author_profile_photo": user.get("image_url"),
                "rating": review.get("rating"),
                "text": review.get("text"),
                "time_created": review.get("time_created"),
                "url": review.get("url"),
                "platform_data": {
                    "user_id": user.get("id"),
                    "user_profile_url": user.get("profile_url")
                }
            })
        return reviews

# Global instance
yelp_client = YelpBusinessClient()