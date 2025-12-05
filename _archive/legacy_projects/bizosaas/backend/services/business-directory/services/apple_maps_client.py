"""
Apple Maps Connect API Client
Handles business registration and management with Apple Maps
"""

import asyncio
import json
import logging
import time
import jwt
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
class AppleAPIResponse:
    """Structured Apple Maps API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    rate_limit_remaining: Optional[int] = None

class AppleRateLimiter:
    """Rate limiter for Apple Maps API calls"""
    
    def __init__(self, calls_per_minute: int = 1000):
        self.calls_per_minute = calls_per_minute
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire rate limit permission"""
        async with self.lock:
            now = time.time()
            # Remove calls older than 1 minute
            self.calls = [call for call in self.calls if now - call < 60.0]
            
            if len(self.calls) >= self.calls_per_minute:
                sleep_time = 60.0 - (now - self.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    return await self.acquire()
            
            self.calls.append(now)

class AppleMapsClient:
    """Apple Maps Connect API client for business management"""
    
    def __init__(self):
        self.base_url = "https://api.businessconnect.apple.com/v1"
        self.rate_limiter = AppleRateLimiter()
        self.session = None
        self._token_cache = {}
        
    def _generate_jwt_token(self) -> str:
        """Generate JWT token for Apple Maps Connect API"""
        # Cache token for 1 hour
        cache_key = "apple_maps_token"
        if cache_key in self._token_cache:
            token_data = self._token_cache[cache_key]
            if datetime.now() < token_data["expires"]:
                return token_data["token"]
        
        # Generate new token
        headers = {
            "alg": "ES256",
            "kid": settings.APPLE_MAPS_KEY_ID
        }
        
        payload = {
            "iss": settings.APPLE_MAPS_TEAM_ID,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,  # 1 hour
            "aud": "https://api.businessconnect.apple.com"
        }
        
        # Load private key
        with open(settings.APPLE_MAPS_PRIVATE_KEY_PATH, 'r') as key_file:
            private_key = key_file.read()
        
        token = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)
        
        # Cache token
        self._token_cache[cache_key] = {
            "token": token,
            "expires": datetime.now() + timedelta(minutes=55)  # Refresh 5 minutes early
        }
        
        return token
        
    async def get_session(self) -> httpx.AsyncClient:
        """Get HTTP session with authentication"""
        if not self.session:
            token = self._generate_jwt_token()
            headers = {
                "Authorization": f"Bearer {token}",
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
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> AppleAPIResponse:
        """Make API request with retry and circuit breaker"""
        await self.rate_limiter.acquire()
        
        session = await self.get_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = await session.request(method, url, **kwargs)
            
            # Check rate limiting headers
            rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
            
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                logger.warning(f"Apple Maps API rate limit exceeded. Retry after {retry_after} seconds")
                await asyncio.sleep(retry_after)
                return await self._make_request(method, endpoint, **kwargs)
            
            response.raise_for_status()
            
            return AppleAPIResponse(
                success=True,
                data=response.json() if response.content else {},
                status_code=response.status_code,
                rate_limit_remaining=int(rate_limit_remaining) if rate_limit_remaining else None
            )
            
        except httpx.HTTPStatusError as e:
            error_msg = f"Apple Maps API HTTP error: {e.response.status_code}"
            if e.response.content:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', '')}"
                except:
                    pass
                    
            logger.error(error_msg)
            return AppleAPIResponse(
                success=False,
                error=error_msg,
                status_code=e.response.status_code
            )
            
        except Exception as e:
            logger.error(f"Apple Maps API request failed: {str(e)}")
            return AppleAPIResponse(success=False, error=str(e))
    
    async def search_places(self, query: str, limit: int = 10, 
                           latitude: float = None, longitude: float = None,
                           radius: int = None) -> AppleAPIResponse:
        """Search for places in Apple Maps"""
        params = {
            "q": query,
            "limit": min(limit, 50)
        }
        
        if latitude and longitude:
            params["ll"] = f"{latitude},{longitude}"
        if radius:
            params["radius"] = min(radius, 100000)  # Max 100km
        
        return await self._make_request("GET", "search", params=params)
    
    async def get_place_details(self, place_id: str) -> AppleAPIResponse:
        """Get detailed place information"""
        return await self._make_request("GET", f"places/{place_id}")
    
    async def register_business(self, business_data: Dict[str, Any]) -> AppleAPIResponse:
        """Register a new business with Apple Maps"""
        return await self._make_request("POST", "places", json=business_data)
    
    async def update_business(self, place_id: str, business_data: Dict[str, Any]) -> AppleAPIResponse:
        """Update existing business information"""
        return await self._make_request("PUT", f"places/{place_id}", json=business_data)
    
    async def claim_business(self, place_id: str, verification_data: Dict[str, Any]) -> AppleAPIResponse:
        """Claim an existing business listing"""
        return await self._make_request("POST", f"places/{place_id}/claim", json=verification_data)
    
    async def get_business_status(self, place_id: str) -> AppleAPIResponse:
        """Get business verification status"""
        return await self._make_request("GET", f"places/{place_id}/status")
    
    async def upload_photo(self, place_id: str, photo_data: bytes, 
                          photo_type: str = "LOGO") -> AppleAPIResponse:
        """Upload business photo"""
        files = {"photo": photo_data}
        data = {"type": photo_type}
        
        return await self._make_request("POST", f"places/{place_id}/photos", 
                                      files=files, data=data)
    
    async def get_categories(self) -> AppleAPIResponse:
        """Get list of Apple Maps business categories"""
        return await self._make_request("GET", "categories")
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None

# Platform-specific data mappers
class AppleMapsDataMapper:
    """Maps Apple Maps API responses to our unified business data format"""
    
    @staticmethod
    def map_place_from_search(apple_place: Dict[str, Any]) -> Dict[str, Any]:
        """Map Apple Maps search result to unified business format"""
        location = apple_place.get("location", {})
        coordinates = location.get("coordinate", {})
        address = location.get("address", {})
        
        return {
            "platform": "apple_maps",
            "platform_id": apple_place.get("id"),
            "name": apple_place.get("name"),
            "description": apple_place.get("description"),
            "phone": apple_place.get("telephone"),
            "website_url": apple_place.get("url"),
            "category": apple_place.get("category"),
            "categories": apple_place.get("categories", []),
            "location": {
                "address": address.get("streetAddress"),
                "city": address.get("locality"),
                "state": address.get("administrativeArea"),
                "postal_code": address.get("postalCode"),
                "country": address.get("countryCode"),
                "formatted_address": apple_place.get("formattedAddress")
            },
            "coordinates": {
                "latitude": coordinates.get("latitude"),
                "longitude": coordinates.get("longitude")
            },
            "platform_data": {
                "muid": apple_place.get("muid"),
                "confidence": apple_place.get("confidence"),
                "display_map_region": location.get("displayMapRegion")
            }
        }
    
    @staticmethod
    def map_place_details(apple_place: Dict[str, Any]) -> Dict[str, Any]:
        """Map detailed Apple Maps place data to unified format"""
        base_data = AppleMapsDataMapper.map_place_from_search(apple_place)
        
        # Add detailed information
        hours = apple_place.get("hours", [])
        if hours:
            base_data["hours"] = {
                "periods": [
                    {
                        "day": period.get("day"),
                        "start": period.get("open"),
                        "end": period.get("close")
                    }
                    for period in hours
                ]
            }
        
        # Add additional details
        base_data.update({
            "email": apple_place.get("email"),
            "fax": apple_place.get("fax"),
            "rating": apple_place.get("rating"),
            "review_count": apple_place.get("reviewCount"),
            "price_range": apple_place.get("priceRange")
        })
        
        # Update platform data with more details
        base_data["platform_data"].update({
            "verification_status": apple_place.get("verificationStatus"),
            "claimed": apple_place.get("claimed"),
            "accessibility": apple_place.get("accessibility", {}),
            "amenities": apple_place.get("amenities", [])
        })
        
        return base_data
    
    @staticmethod
    def create_business_registration_payload(business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Apple Maps business registration payload"""
        location = business_data.get("location", {})
        coordinates = business_data.get("coordinates", {})
        
        payload = {
            "name": business_data.get("name"),
            "description": business_data.get("description"),
            "telephone": business_data.get("phone"),
            "url": business_data.get("website_url"),
            "email": business_data.get("email"),
            "category": business_data.get("category"),
            "location": {
                "address": {
                    "streetAddress": location.get("address"),
                    "locality": location.get("city"),
                    "administrativeArea": location.get("state"),
                    "postalCode": location.get("postal_code"),
                    "countryCode": location.get("country", "US")
                },
                "coordinate": {
                    "latitude": coordinates.get("latitude"),
                    "longitude": coordinates.get("longitude")
                }
            }
        }
        
        # Add hours if available
        hours = business_data.get("hours", {}).get("periods", [])
        if hours:
            payload["hours"] = [
                {
                    "day": period.get("day"),
                    "open": period.get("start"),
                    "close": period.get("end")
                }
                for period in hours
            ]
        
        # Add additional details
        if business_data.get("price_range"):
            payload["priceRange"] = business_data["price_range"]
        
        if business_data.get("amenities"):
            payload["amenities"] = business_data["amenities"]
        
        return payload
    
    @staticmethod
    def map_categories(apple_categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Apple Maps categories to unified format"""
        categories = []
        for category in apple_categories.get("categories", []):
            categories.append({
                "platform": "apple_maps",
                "category_id": category.get("id"),
                "name": category.get("name"),
                "display_name": category.get("displayName"),
                "parent_id": category.get("parentId"),
                "level": category.get("level")
            })
        return categories

# Global instance
apple_maps_client = AppleMapsClient()