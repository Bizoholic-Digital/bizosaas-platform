"""
TripAdvisor Platform Client
Travel and hospitality review platform integration
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..platform_abstraction.base_platform_client import (
    ReadOnlyPlatformClient, PlatformCapabilities, PlatformCapability,
    PlatformResponse, AuthCredentials, SyncOperation
)
from ..platform_abstraction.unified_data_models import (
    UniversalBusinessData, UniversalLocation, UniversalContact,
    UniversalHours, UniversalCategory, UniversalPhoto, UniversalReview,
    BusinessStatus, BusinessType
)
from ..platform_abstraction.platform_registry import (
    register_platform, PlatformMetadata, PlatformTier, PlatformCategory
)

logger = logging.getLogger(__name__)

class TripAdvisorClient(ReadOnlyPlatformClient):
    """
    TripAdvisor client for travel and hospitality businesses
    Primarily focused on restaurants, hotels, and attractions
    """
    
    def __init__(self, platform_name: str = "tripadvisor"):
        super().__init__(platform_name)
        self.base_url = "https://api.tripadvisor.com/api/partner/2.0"
        
    @property
    def capabilities(self) -> PlatformCapabilities:
        """TripAdvisor capabilities"""
        return PlatformCapabilities(
            platform_name=self.platform_name,
            supported_operations=[
                PlatformCapability.SEARCH_LISTINGS,
                PlatformCapability.MANAGE_REVIEWS,
                PlatformCapability.MANAGE_PHOTOS,
            ],
            read_only=True,  # TripAdvisor API is read-only
            requires_verification=True,  # Requires API key approval
            supports_bulk=True,
            rate_limit_per_minute=500,
            rate_limit_per_day=50000
        )
    
    async def authenticate(self, credentials: AuthCredentials) -> bool:
        """
        Authenticate with TripAdvisor API
        
        Args:
            credentials: Should contain 'api_key'
            
        Returns:
            bool: True if API key is valid
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            self.logger.error("TripAdvisor API key not provided")
            return False
        
        try:
            # Test the API key with a simple location search
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params={
                        "q": "restaurant",
                        "location": "New York",
                        "key": api_key
                    },
                    timeout=10
                )
                
                return response.status_code in [200, 400]  # 400 might indicate valid key but bad params
                
        except Exception as e:
            self.logger.error(f"TripAdvisor authentication failed: {str(e)}")
            return False
    
    async def get_listing(self, platform_id: str,
                         credentials: AuthCredentials) -> PlatformResponse:
        """
        Get business details from TripAdvisor
        
        Args:
            platform_id: TripAdvisor location ID
            credentials: TripAdvisor API credentials
            
        Returns:
            PlatformResponse with business details
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.GET,
                "TripAdvisor API key required"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/location/{platform_id}",
                    params={
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    universal_data = self.transform_to_universal(data)
                    
                    return self.create_success_response(
                        SyncOperation.GET,
                        {
                            "location_data": data,
                            "universal_data": universal_data.to_dict()
                        },
                        platform_id=platform_id
                    )
                else:
                    return self.create_error_response(
                        SyncOperation.GET,
                        f"TripAdvisor API error: {response.status_code}",
                        status_code=response.status_code
                    )
                    
        except Exception as e:
            return self.create_error_response(
                SyncOperation.GET,
                f"Failed to get TripAdvisor listing: {str(e)}"
            )
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def search_listings(self, query: str, location: str,
                            credentials: AuthCredentials) -> PlatformResponse:
        """
        Search for businesses on TripAdvisor
        
        Args:
            query: Search query (restaurant, hotel, etc.)
            location: Location string
            credentials: TripAdvisor API credentials
            
        Returns:
            PlatformResponse with search results
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.SEARCH,
                "TripAdvisor API key required"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params={
                        "q": query,
                        "location": location,
                        "category": self._determine_category(query),
                        "limit": 20,
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("data", [])
                    
                    # Transform results to universal format
                    universal_results = []
                    for location_data in results:
                        try:
                            universal_data = self.transform_to_universal(location_data)
                            universal_results.append({
                                "platform_id": location_data.get("location_id"),
                                "universal_data": universal_data.to_dict(),
                                "raw_data": location_data,
                                "match_score": self._calculate_match_score(location_data, query)
                            })
                        except Exception as e:
                            self.logger.warning(f"Failed to transform TripAdvisor data: {str(e)}")
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
                        f"TripAdvisor API error: {response.status_code}",
                        status_code=response.status_code
                    )
                    
        except Exception as e:
            return self.create_error_response(
                SyncOperation.SEARCH,
                f"TripAdvisor search failed: {str(e)}"
            )
    
    async def _get_reviews_impl(self, platform_id: str,
                              credentials: AuthCredentials) -> PlatformResponse:
        """
        Get reviews for a TripAdvisor listing
        
        Args:
            platform_id: TripAdvisor location ID
            credentials: API credentials
            
        Returns:
            PlatformResponse with reviews
        """
        api_key = credentials.get_credential("api_key")
        if not api_key:
            return self.create_error_response(
                SyncOperation.GET,
                "TripAdvisor API key required"
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/location/{platform_id}/reviews",
                    params={
                        "limit": 50,
                        "language": "en",
                        "key": api_key
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    reviews_data = data.get("data", [])
                    
                    # Transform reviews to universal format
                    universal_reviews = []
                    for review in reviews_data:
                        try:
                            universal_review = UniversalReview(
                                rating=review.get("rating", 0),
                                text=review.get("text"),
                                author_name=review.get("user", {}).get("username"),
                                author_photo=review.get("user", {}).get("avatar", {}).get("large"),
                                created_at=self._parse_date(review.get("published_date")),
                                platform_review_id=review.get("id")
                            )
                            universal_reviews.append(universal_review.to_dict())
                        except Exception as e:
                            self.logger.warning(f"Failed to transform review: {str(e)}")
                            continue
                    
                    return self.create_success_response(
                        SyncOperation.GET,
                        {
                            "reviews": universal_reviews,
                            "total_reviews": len(universal_reviews)
                        },
                        platform_id=platform_id
                    )
                else:
                    return self.create_error_response(
                        SyncOperation.GET,
                        f"Failed to get reviews: {response.status_code}",
                        status_code=response.status_code
                    )
                    
        except Exception as e:
            return self.create_error_response(
                SyncOperation.GET,
                f"Failed to get TripAdvisor reviews: {str(e)}"
            )
    
    def transform_to_universal(self, location_data: Dict[str, Any]) -> UniversalBusinessData:
        """Transform TripAdvisor location data to universal format"""
        # Basic information
        name = location_data.get("name", "")
        description = location_data.get("description")
        
        # Location
        location = None
        address_obj = location_data.get("address_obj", {})
        if address_obj:
            location = UniversalLocation(
                street_address=address_obj.get("street1"),
                city=address_obj.get("city"),
                state=address_obj.get("state"),
                postal_code=address_obj.get("postalcode"),
                country=address_obj.get("country"),
                formatted_address=location_data.get("address"),
                latitude=float(location_data.get("latitude")) if location_data.get("latitude") else None,
                longitude=float(location_data.get("longitude")) if location_data.get("longitude") else None
            )
        
        # Contact information
        contact = UniversalContact(
            primary_phone=location_data.get("phone"),
            website=location_data.get("website"),
            email=location_data.get("email")
        )
        
        # Categories - TripAdvisor specific
        categories = None
        category = location_data.get("category", {})
        if category:
            business_type = self._map_tripadvisor_category_to_business_type(category.get("name", ""))
            categories = UniversalCategory(
                primary_category=category.get("name"),
                secondary_categories=location_data.get("subcategory", []),
                business_type=business_type
            )
        
        # Photos
        photos = []
        if "photo" in location_data:
            photo_data = location_data["photo"]
            photos.append(UniversalPhoto(
                url=photo_data.get("images", {}).get("large", {}).get("url"),
                caption=photo_data.get("caption"),
                width=photo_data.get("images", {}).get("large", {}).get("width"),
                height=photo_data.get("images", {}).get("large", {}).get("height"),
                is_primary=True
            ))
        
        # Reviews and ratings
        overall_rating = float(location_data.get("rating", 0)) if location_data.get("rating") else None
        total_reviews = int(location_data.get("num_reviews", 0))
        
        # Operating status
        status = BusinessStatus.OPERATIONAL
        if location_data.get("is_closed"):
            status = BusinessStatus.PERMANENTLY_CLOSED
        
        return UniversalBusinessData(
            name=name,
            description=description,
            status=status,
            location=location,
            contact=contact,
            categories=categories,
            photos=photos,
            overall_rating=overall_rating,
            total_reviews=total_reviews,
            attributes={
                "tripadvisor_id": location_data.get("location_id"),
                "tripadvisor_url": location_data.get("web_url"),
                "ranking": location_data.get("ranking"),
                "price_level": location_data.get("price_level"),
                "cuisine": location_data.get("cuisine"),
                "awards": location_data.get("awards", []),
                "amenities": location_data.get("amenities", [])
            }
        )
    
    def transform_from_universal(self, business_data: UniversalBusinessData) -> Dict[str, Any]:
        """Transform universal data to TripAdvisor format (not used for read-only API)"""
        return {
            "name": business_data.name,
            "description": business_data.description,
            "address_obj": {
                "street1": business_data.location.street_address if business_data.location else None,
                "city": business_data.location.city if business_data.location else None,
                "state": business_data.location.state if business_data.location else None,
                "postalcode": business_data.location.postal_code if business_data.location else None,
                "country": business_data.location.country if business_data.location else None
            },
            "phone": business_data.contact.primary_phone if business_data.contact else None,
            "website": business_data.contact.website if business_data.contact else None,
            "category": business_data.categories.primary_category if business_data.categories else None
        }
    
    def _determine_category(self, query: str) -> str:
        """Determine TripAdvisor category from search query"""
        query_lower = query.lower()
        
        if any(term in query_lower for term in ["restaurant", "food", "dining", "eat"]):
            return "restaurants"
        elif any(term in query_lower for term in ["hotel", "stay", "accommodation"]):
            return "hotels"
        elif any(term in query_lower for term in ["attraction", "tour", "activity", "museum"]):
            return "attractions"
        else:
            return "restaurants"  # Default to restaurants
    
    def _map_tripadvisor_category_to_business_type(self, category: str) -> BusinessType:
        """Map TripAdvisor category to universal business type"""
        category_lower = category.lower()
        
        if "restaurant" in category_lower or "food" in category_lower:
            return BusinessType.RESTAURANT
        elif "hotel" in category_lower or "accommodation" in category_lower:
            return BusinessType.HOSPITALITY
        elif "attraction" in category_lower or "museum" in category_lower:
            return BusinessType.ENTERTAINMENT
        elif "spa" in category_lower or "beauty" in category_lower:
            return BusinessType.BEAUTY
        else:
            return BusinessType.OTHER
    
    def _calculate_match_score(self, location_data: Dict[str, Any], query: str) -> float:
        """Calculate match score for search results"""
        score = 0.0
        
        # Name matching
        name = location_data.get("name", "").lower()
        query_lower = query.lower()
        if query_lower in name:
            score += 0.3
        
        # Rating boost
        rating = location_data.get("rating")
        if rating:
            if rating >= 4.5:
                score += 0.3
            elif rating >= 4.0:
                score += 0.2
            elif rating >= 3.5:
                score += 0.1
        
        # Review count boost
        num_reviews = location_data.get("num_reviews", 0)
        if num_reviews > 500:
            score += 0.2
        elif num_reviews > 100:
            score += 0.1
        
        # Ranking boost (lower is better)
        ranking = location_data.get("ranking")
        if ranking and ranking <= 10:
            score += 0.2
        elif ranking and ranking <= 50:
            score += 0.1
        
        return min(score, 1.0)
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse TripAdvisor date string"""
        if not date_string:
            return None
        
        try:
            # TripAdvisor typically uses YYYY-MM-DD format
            return datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            try:
                # Try with time included
                return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                self.logger.warning(f"Unable to parse date: {date_string}")
                return None

# Register the platform
register_platform(
    TripAdvisorClient,
    PlatformMetadata(
        name="tripadvisor",
        display_name="TripAdvisor",
        tier=PlatformTier.TIER_2,
        category=PlatformCategory.REVIEW_PLATFORM,
        description="Travel and hospitality review platform",
        website="https://www.tripadvisor.com",
        api_docs_url="https://developer-tripadvisor.com",
        supported_business_types=["restaurant", "hospitality", "entertainment"],
        requires_approval=True  # TripAdvisor requires API approval
    ),
    PlatformCapabilities(
        platform_name="tripadvisor",
        supported_operations=[
            PlatformCapability.SEARCH_LISTINGS,
            PlatformCapability.MANAGE_REVIEWS,
            PlatformCapability.MANAGE_PHOTOS,
        ],
        read_only=True,
        requires_verification=True,
        supports_bulk=True,
        rate_limit_per_minute=500,
        rate_limit_per_day=50000
    )
)