"""
Google Maps Platform Client
Specialized client for Google Maps Places API (separate from Google Business Profile)
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..platform_abstraction.base_platform_client import (
    BasePlatformClient, PlatformCapabilities, PlatformCapability,
    PlatformResponse, AuthCredentials, SyncOperation
)
from ..platform_abstraction.unified_data_models import (
    UniversalBusinessData, UniversalLocation, UniversalContact,
    UniversalHours, UniversalCategory, UniversalPhoto, BusinessStatus
)
from ..platform_abstraction.platform_registry import (
    register_platform, PlatformMetadata, PlatformTier, PlatformCategory
)

logger = logging.getLogger(__name__)

class GoogleMapsClient(BasePlatformClient):
    """
    Google Maps Platform client for Places API operations
    Different from Google Business Profile - focuses on map presence and place data
    """
    
    def __init__(self, platform_name: str = "google_maps"):
        super().__init__(platform_name)
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.places_url = f"{self.base_url}/place"
        self.geocoding_url = f"{self.base_url}/geocode/json"
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        """Google Maps capabilities"""
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[
                PlatformCapability.SEARCH_LISTINGS,
                PlatformCapability.ANALYTICS,  # Place insights
            ],
            read_only=True,  # Google Maps Places API is mostly read-only
            requires_verification=False,
            supports_bulk=True,
            rate_limit_per_minute=600,
            rate_limit_per_day=10000
        )
    
    async def authenticate(self, credentials: AuthCredentials) -> bool:
        """
        Authenticate with Google Maps API
        
        Args:
            credentials: Should contain 'api_key'
            
        Returns:
            bool: True if API key is valid
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            self.logger.error("Google Maps API key not provided")
            return False
        
        try:
            # Test the API key with a simple geocoding request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.geocoding_url,
                    params={
                        "address": "1600 Amphitheatre Parkway, Mountain View, CA",
                        "key": api_key
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("status") != "REQUEST_DENIED"
                
                return False
                
        except Exception as e:
            self.logger.error(f"Google Maps authentication failed: {str(e)}")
            return False
    
    async def create_listing(self, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        """
        Google Maps doesn't support creating listings via API
        Businesses appear on Google Maps through various sources
        """
        return self.create_error_response(
            SyncOperation.CREATE,
            "Google Maps doesn't support creating listings via API. "
            "Use Google Business Profile for business listings."
        )
    
    async def update_listing(self, platform_id: str, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        """Google Maps doesn't support updating listings via API"""
        return self.create_error_response(
            SyncOperation.UPDATE,
            "Google Maps doesn't support updating listings via API. "
            "Use Google Business Profile for business management."
        )
    
    async def get_listing(self, platform_id: str,
                         credentials: AuthCredentials) -> PlatformResponse:
        """
        Get place details from Google Maps
        
        Args:
            platform_id: Google place_id
            credentials: Google Maps API credentials
            
        Returns:
            PlatformResponse with place details
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.GET,
                "Google Maps API key required"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.places_url}/details/json",
                    params={
                        "place_id": platform_id,
                        "fields": "place_id,name,formatted_address,geometry,formatted_phone_number,"
                                "website,business_status,opening_hours,price_level,rating,"
                                "user_ratings_total,types,photos,reviews",
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "OK":
                        place_data = data.get("result", {})
                        universal_data = self.transform_to_universal(place_data)
                        
                        return self.create_success_response(
                            SyncOperation.GET,
                            {
                                "place_data": place_data,
                                "universal_data": universal_data.to_dict()
                            },
                            platform_id=platform_id
                        )
                    else:
                        return self.create_error_response(
                            SyncOperation.GET,
                            f"Google Maps API error: {data.get('status')}"
                        )
                else:
                    return self.create_error_response(
                        SyncOperation.GET,
                        f"HTTP error: {response.status_code}",
                        status_code=response.status_code
                    )
                    
        except Exception as e:
            return self.create_error_response(
                SyncOperation.GET,
                f"Failed to get place details: {str(e)}"
            )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def search_listings(self, query: str, location: str,
                            credentials: AuthCredentials) -> PlatformResponse:
        """
        Search for places on Google Maps
        
        Args:
            query: Search query (business name, type, etc.)
            location: Location string or coordinates
            credentials: Google Maps API credentials
            
        Returns:
            PlatformResponse with search results
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.SEARCH,
                "Google Maps API key required"
            )
        
        try:
            # Use Text Search to find places
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.places_url}/textsearch/json",
                    params={
                        "query": f"{query} {location}",
                        "fields": "place_id,name,formatted_address,geometry,rating,"
                                "user_ratings_total,business_status,types,photos",
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "OK":
                        results = data.get("results", [])
                        
                        # Transform results to universal format
                        universal_results = []
                        for place in results:
                            try:
                                universal_data = self.transform_to_universal(place)
                                universal_results.append({
                                    "platform_id": place.get("place_id"),
                                    "universal_data": universal_data.to_dict(),
                                    "raw_data": place,
                                    "match_score": self._calculate_match_score(place, query, location)
                                })
                            except Exception as e:
                                self.logger.warning(f"Failed to transform place data: {str(e)}")
                                continue
                        
                        return self.create_success_response(
                            SyncOperation.SEARCH,
                            {
                                "results": universal_results,
                                "total_results": len(universal_results),
                                "next_page_token": data.get("next_page_token")
                            }
                        )
                    else:
                        return self.create_error_response(
                            SyncOperation.SEARCH,
                            f"Google Maps API error: {data.get('status')}"
                        )
                else:
                    return self.create_error_response(
                        SyncOperation.SEARCH,
                        f"HTTP error: {response.status_code}",
                        status_code=response.status_code
                    )
                    
        except Exception as e:
            return self.create_error_response(
                SyncOperation.SEARCH,
                f"Search failed: {str(e)}"
            )
    
    async def get_place_photos(self, place_id: str, credentials: AuthCredentials,
                             max_width: int = 1600) -> PlatformResponse:
        """
        Get photos for a place
        
        Args:
            place_id: Google place ID
            credentials: API credentials
            max_width: Maximum photo width
            
        Returns:
            PlatformResponse with photo URLs
        """
        # First get place details to get photo references
        place_response = await self.get_listing(place_id, credentials)
        
        if not place_response.success:
            return place_response
        
        place_data = place_response.data.get("place_data", {})
        photos = place_data.get("photos", [])
        
        if not photos:
            return self.create_success_response(
                SyncOperation.GET,
                {"photos": []},
                platform_id=place_id
            )
        
        api_key = credentials.get_credential("api_key")
        photo_urls = []
        
        for photo in photos[:10]:  # Limit to 10 photos
            photo_reference = photo.get("photo_reference")
            if photo_reference:
                photo_url = (
                    f"{self.places_url}/photo"
                    f"?maxwidth={max_width}"
                    f"&photo_reference={photo_reference}"
                    f"&key={api_key}"
                )
                photo_urls.append({
                    "url": photo_url,
                    "width": photo.get("width"),
                    "height": photo.get("height"),
                    "html_attributions": photo.get("html_attributions", [])
                })
        
        return self.create_success_response(
            SyncOperation.GET,
            {"photos": photo_urls},
            platform_id=place_id
        )
    
    def transform_to_universal(self, place_data: Dict[str, Any]) -> UniversalBusinessData:
        """Transform Google Maps place data to universal format"""
        # Basic information
        name = place_data.get("name", "")
        
        # Location
        location = None
        if "geometry" in place_data and "location" in place_data["geometry"]:
            geo_location = place_data["geometry"]["location"]
            location = UniversalLocation(
                formatted_address=place_data.get("formatted_address"),
                latitude=geo_location.get("lat"),
                longitude=geo_location.get("lng"),
                place_id=place_data.get("place_id")
            )
            
            # Parse address components if available
            if "address_components" in place_data:
                self._parse_address_components(location, place_data["address_components"])
        
        # Contact information
        contact = UniversalContact(
            primary_phone=place_data.get("formatted_phone_number"),
            website=place_data.get("website")
        )
        
        # Business hours
        hours = None
        if "opening_hours" in place_data:
            hours = self._parse_opening_hours(place_data["opening_hours"])
        
        # Categories
        categories = None
        if "types" in place_data:
            primary_type = place_data["types"][0] if place_data["types"] else None
            categories = UniversalCategory(
                primary_category=primary_type,
                secondary_categories=place_data["types"][1:] if len(place_data["types"]) > 1 else []
            )
        
        # Business status
        status = BusinessStatus.OPERATIONAL
        if place_data.get("business_status") == "CLOSED_TEMPORARILY":
            status = BusinessStatus.TEMPORARILY_CLOSED
        elif place_data.get("business_status") == "CLOSED_PERMANENTLY":
            status = BusinessStatus.PERMANENTLY_CLOSED
        
        # Photos
        photos = []
        if "photos" in place_data:
            for photo in place_data["photos"][:5]:  # Limit to 5 photos
                photos.append(UniversalPhoto(
                    url=f"photo_reference:{photo.get('photo_reference')}",  # Will be converted to actual URL
                    width=photo.get("width"),
                    height=photo.get("height")
                ))
        
        # Reviews and ratings
        overall_rating = place_data.get("rating")
        total_reviews = place_data.get("user_ratings_total", 0)
        
        return UniversalBusinessData(
            name=name,
            status=status,
            location=location,
            contact=contact,
            hours=hours,
            categories=categories,
            photos=photos,
            overall_rating=overall_rating,
            total_reviews=total_reviews,
            attributes={
                "google_place_id": place_data.get("place_id"),
                "price_level": place_data.get("price_level"),
                "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{place_data.get('place_id')}" if place_data.get("place_id") else None
            }
        )
    
    def transform_from_universal(self, business_data: UniversalBusinessData) -> Dict[str, Any]:
        """Transform universal data to Google Maps format (not used for read-only API)"""
        return {
            "name": business_data.name,
            "formatted_address": business_data.location.formatted_address if business_data.location else None,
            "types": [business_data.categories.primary_category] + business_data.categories.secondary_categories if business_data.categories else [],
            "phone": business_data.contact.primary_phone if business_data.contact else None,
            "website": business_data.contact.website if business_data.contact else None
        }
    
    def _parse_address_components(self, location: UniversalLocation, components: List[Dict[str, Any]]):
        """Parse Google Maps address components"""
        for component in components:
            types = component.get("types", [])
            long_name = component.get("long_name", "")
            
            if "street_number" in types:
                location.street_address = long_name
            elif "route" in types:
                if location.street_address:
                    location.street_address += f" {long_name}"
                else:
                    location.street_address = long_name
            elif "locality" in types:
                location.city = long_name
            elif "administrative_area_level_1" in types:
                location.state = component.get("short_name", long_name)
            elif "postal_code" in types:
                location.postal_code = long_name
            elif "country" in types:
                location.country = component.get("short_name", long_name)
    
    def _parse_opening_hours(self, hours_data: Dict[str, Any]) -> UniversalHours:
        """Parse Google Maps opening hours"""
        hours = UniversalHours()
        
        if "periods" in hours_data:
            for period in hours_data["periods"]:
                if "open" in period:
                    day = period["open"].get("day", 0)  # 0 = Sunday, 1 = Monday, etc.
                    open_time = period["open"].get("time", "0000")
                    close_time = period.get("close", {}).get("time", "2359")
                    
                    # Convert day number to day name
                    day_names = ["sunday", "monday", "tuesday", "wednesday", 
                               "thursday", "friday", "saturday"]
                    day_name = day_names[day] if day < len(day_names) else "monday"
                    
                    # Format time as HH:MM
                    open_formatted = f"{open_time[:2]}:{open_time[2:]}"
                    close_formatted = f"{close_time[:2]}:{close_time[2:]}"
                    
                    # Add to appropriate day
                    day_hours = getattr(hours, day_name, [])
                    if day_hours is None:
                        day_hours = []
                        setattr(hours, day_name, day_hours)
                    
                    day_hours.append({
                        "open": open_formatted,
                        "close": close_formatted
                    })
        
        return hours
    
    def _calculate_match_score(self, place: Dict[str, Any], query: str, location: str) -> float:
        """Calculate match score for search results"""
        score = 0.0
        
        # Name matching
        name = place.get("name", "").lower()
        query_lower = query.lower()
        if query_lower in name:
            score += 0.4
        
        # Address matching
        address = place.get("formatted_address", "").lower()
        location_lower = location.lower()
        if location_lower in address:
            score += 0.3
        
        # Rating boost
        rating = place.get("rating", 0)
        if rating > 4.0:
            score += 0.2
        elif rating > 3.0:
            score += 0.1
        
        # Review count boost
        review_count = place.get("user_ratings_total", 0)
        if review_count > 100:
            score += 0.1
        
        return min(score, 1.0)

# Register the platform
register_platform(
    GoogleMapsClient,
    PlatformMetadata(
        name="google_maps",
        display_name="Google Maps",
        tier=PlatformTier.TIER_1,
        category=PlatformCategory.MAPPING_SERVICE,
        description="Google's mapping and location platform",
        website="https://maps.google.com",
        api_docs_url="https://developers.google.com/maps",
        primary_markets=["US", "Global"]
    ),
    PlatformCapabilities(
        platform_name="google_maps",
        supported_operations=[
            PlatformCapability.SEARCH_LISTINGS,
            PlatformCapability.ANALYTICS,
        ],
        read_only=True,
        requires_verification=False,
        supports_bulk=True,
        rate_limit_per_minute=600,
        rate_limit_per_day=10000
    )
)