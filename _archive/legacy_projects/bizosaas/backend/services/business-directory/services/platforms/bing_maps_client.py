"""
Bing Maps Platform Client
Microsoft's mapping platform integration
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

class BingMapsClient(BasePlatformClient):
    """
    Bing Maps Platform client for location and mapping operations
    """
    
    def __init__(self, platform_name: str = "bing_maps"):
        super().__init__(platform_name)
        self.base_url = "https://dev.virtualearth.net/REST/v1"
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        """Bing Maps capabilities"""
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[
                PlatformCapability.SEARCH_LISTINGS,
            ],
            read_only=True,  # Bing Maps is primarily for search/geocoding
            requires_verification=False,
            supports_bulk=True,
            rate_limit_per_minute=250,  # Bing Maps rate limits
            rate_limit_per_day=125000
        )
    
    async def authenticate(self, credentials: AuthCredentials) -> bool:
        """
        Authenticate with Bing Maps API
        
        Args:
            credentials: Should contain 'api_key' (Bing Maps Key)
            
        Returns:
            bool: True if API key is valid
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            self.logger.error("Bing Maps API key not provided")
            return False
        
        try:
            # Test the API key with a simple location query
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/Locations",
                    params={
                        "query": "Microsoft, Redmond, WA",
                        "key": api_key
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("statusCode") == 200
                
                return False
                
        except Exception as e:
            self.logger.error(f"Bing Maps authentication failed: {str(e)}")
            return False
    
    async def create_listing(self, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        """Bing Maps doesn't support creating listings via API"""
        return self.create_error_response(
            SyncOperation.CREATE,
            "Bing Maps doesn't support creating listings via API"
        )
    
    async def update_listing(self, platform_id: str, business_data: UniversalBusinessData,
                           credentials: AuthCredentials) -> PlatformResponse:
        """Bing Maps doesn't support updating listings via API"""
        return self.create_error_response(
            SyncOperation.UPDATE,
            "Bing Maps doesn't support updating listings via API"
        )
    
    async def get_listing(self, platform_id: str,
                         credentials: AuthCredentials) -> PlatformResponse:
        """
        Get location details from Bing Maps
        
        Args:
            platform_id: Location ID or coordinates
            credentials: Bing Maps API credentials
            
        Returns:
            PlatformResponse with location details
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.GET,
                "Bing Maps API key required"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/Locations/{platform_id}",
                    params={
                        "includeEntityTypes": "Business,PopulatedPlace",
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("statusCode") == 200 and data.get("resourceSets"):
                        resources = data["resourceSets"][0].get("resources", [])
                        if resources:
                            location_data = resources[0]
                            universal_data = self.transform_to_universal(location_data)
                            
                            return self.create_success_response(
                                SyncOperation.GET,
                                {
                                    "location_data": location_data,
                                    "universal_data": universal_data.to_dict()
                                },
                                platform_id=platform_id
                            )
                    
                    return self.create_error_response(
                        SyncOperation.GET,
                        "Location not found on Bing Maps"
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
                f"Failed to get location: {str(e)}"
            )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def search_listings(self, query: str, location: str,
                            credentials: AuthCredentials) -> PlatformResponse:
        """
        Search for locations on Bing Maps
        
        Args:
            query: Search query (business name, type, etc.)
            location: Location string or coordinates
            credentials: Bing Maps API credentials
            
        Returns:
            PlatformResponse with search results
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.SEARCH,
                "Bing Maps API key required"
            )
        
        try:
            # Combine query and location for search
            search_query = f"{query}, {location}".strip(", ")
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/Locations",
                    params={
                        "query": search_query,
                        "maxResults": 20,
                        "includeEntityTypes": "Business,PopulatedPlace",
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("statusCode") == 200 and data.get("resourceSets"):
                        resources = data["resourceSets"][0].get("resources", [])
                        
                        # Transform results to universal format
                        universal_results = []
                        for location_data in resources:
                            try:
                                universal_data = self.transform_to_universal(location_data)
                                universal_results.append({
                                    "platform_id": self._extract_location_id(location_data),
                                    "universal_data": universal_data.to_dict(),
                                    "raw_data": location_data,
                                    "match_score": self._calculate_match_score(location_data, query, location)
                                })
                            except Exception as e:
                                self.logger.warning(f"Failed to transform location data: {str(e)}")
                                continue
                        
                        return self.create_success_response(
                            SyncOperation.SEARCH,
                            {
                                "results": universal_results,
                                "total_results": len(universal_results)
                            }
                        )
                    else:
                        return self.create_error_response(
                            SyncOperation.SEARCH,
                            f"Bing Maps API error: {data.get('statusDescription', 'Unknown error')}"
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
    
    async def geocode_address(self, address: str, credentials: AuthCredentials) -> PlatformResponse:
        """
        Geocode an address using Bing Maps
        
        Args:
            address: Address to geocode
            credentials: Bing Maps API credentials
            
        Returns:
            PlatformResponse with geocoding results
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.GET,
                "Bing Maps API key required"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/Locations",
                    params={
                        "query": address,
                        "maxResults": 1,
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("statusCode") == 200 and data.get("resourceSets"):
                        resources = data["resourceSets"][0].get("resources", [])
                        if resources:
                            location_data = resources[0]
                            point = location_data.get("point", {})
                            coordinates = point.get("coordinates", [])
                            
                            geocode_result = {
                                "latitude": coordinates[0] if len(coordinates) > 0 else None,
                                "longitude": coordinates[1] if len(coordinates) > 1 else None,
                                "formatted_address": location_data.get("name"),
                                "confidence": location_data.get("confidence"),
                                "match_code": location_data.get("matchCodes", [])
                            }
                            
                            return self.create_success_response(
                                SyncOperation.GET,
                                {"geocoding": geocode_result}
                            )
                    
                    return self.create_error_response(
                        SyncOperation.GET,
                        "Address not found"
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
                f"Geocoding failed: {str(e)}"
            )
    
    def transform_to_universal(self, location_data: Dict[str, Any]) -> UniversalBusinessData:
        """Transform Bing Maps location data to universal format"""
        # Basic information
        name = location_data.get("name", "")
        
        # Extract coordinates
        point = location_data.get("point", {})
        coordinates = point.get("coordinates", [])
        
        # Location
        location = UniversalLocation(
            formatted_address=location_data.get("name"),
            latitude=coordinates[0] if len(coordinates) > 0 else None,
            longitude=coordinates[1] if len(coordinates) > 1 else None
        )
        
        # Parse address if available
        address = location_data.get("address", {})
        if address:
            location.street_address = address.get("addressLine")
            location.city = address.get("locality")
            location.state = address.get("adminDistrict")
            location.postal_code = address.get("postalCode")
            location.country = address.get("countryRegion")
        
        # Entity type mapping to categories
        categories = None
        entity_type = location_data.get("entityType")
        if entity_type:
            categories = UniversalCategory(
                primary_category=entity_type.lower(),
                secondary_categories=[]
            )
        
        # Contact information (limited in Bing Maps)
        contact = UniversalContact()
        
        return UniversalBusinessData(
            name=name,
            status=BusinessStatus.OPERATIONAL,
            location=location,
            contact=contact,
            categories=categories,
            attributes={
                "bing_location_id": self._extract_location_id(location_data),
                "confidence": location_data.get("confidence"),
                "match_codes": location_data.get("matchCodes", []),
                "entity_type": entity_type,
                "bing_maps_url": self._generate_bing_maps_url(coordinates[0], coordinates[1]) if len(coordinates) >= 2 else None
            }
        )
    
    def transform_from_universal(self, business_data: UniversalBusinessData) -> Dict[str, Any]:
        """Transform universal data to Bing Maps format (not used for read-only API)"""
        return {
            "name": business_data.name,
            "address": {
                "addressLine": business_data.location.street_address if business_data.location else None,
                "locality": business_data.location.city if business_data.location else None,
                "adminDistrict": business_data.location.state if business_data.location else None,
                "postalCode": business_data.location.postal_code if business_data.location else None,
                "countryRegion": business_data.location.country if business_data.location else None
            },
            "point": {
                "coordinates": [
                    business_data.location.latitude,
                    business_data.location.longitude
                ] if business_data.location and business_data.location.latitude and business_data.location.longitude else None
            }
        }
    
    def _extract_location_id(self, location_data: Dict[str, Any]) -> str:
        """Extract a unique identifier for the location"""
        # Bing Maps doesn't provide stable IDs, so create one from coordinates
        point = location_data.get("point", {})
        coordinates = point.get("coordinates", [])
        if len(coordinates) >= 2:
            return f"bing_{coordinates[0]}_{coordinates[1]}"
        
        # Fallback to address hash
        name = location_data.get("name", "")
        return f"bing_{hash(name)}"
    
    def _generate_bing_maps_url(self, lat: float, lon: float) -> str:
        """Generate Bing Maps URL for coordinates"""
        return f"https://www.bing.com/maps?q={lat},{lon}"
    
    def _calculate_match_score(self, location_data: Dict[str, Any], query: str, location: str) -> float:
        """Calculate match score for search results"""
        score = 0.0
        
        # Name matching
        name = location_data.get("name", "").lower()
        query_lower = query.lower()
        if query_lower in name:
            score += 0.4
        
        # Confidence from Bing Maps
        confidence = location_data.get("confidence", "Low")
        if confidence == "High":
            score += 0.3
        elif confidence == "Medium":
            score += 0.2
        else:
            score += 0.1
        
        # Entity type relevance
        entity_type = location_data.get("entityType", "").lower()
        if entity_type == "business":
            score += 0.2
        
        # Match codes (quality indicators)
        match_codes = location_data.get("matchCodes", [])
        if "Good" in match_codes:
            score += 0.1
        
        return min(score, 1.0)

# Register the platform
register_platform(
    BingMapsClient,
    PlatformMetadata(
        name="bing_maps",
        display_name="Bing Maps",
        tier=PlatformTier.TIER_1,
        category=PlatformCategory.MAPPING_SERVICE,
        description="Microsoft's mapping platform",
        website="https://www.bing.com/maps",
        api_docs_url="https://docs.microsoft.com/en-us/bingmaps",
        primary_markets=["US"]
    ),
    PlatformCapabilities(
        platform_name="bing_maps",
        supported_operations=[
            PlatformCapability.SEARCH_LISTINGS,
        ],
        read_only=True,
        requires_verification=False,
        supports_bulk=True,
        rate_limit_per_minute=250,
        rate_limit_per_day=125000
    )
)