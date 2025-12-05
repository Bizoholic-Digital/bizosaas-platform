"""
Unified Data Models for Multi-Platform Sync
Platform-agnostic data structures for business information
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime, time
from dataclasses import dataclass, field
from enum import Enum
import json

class BusinessStatus(str, Enum):
    """Universal business status across platforms"""
    OPERATIONAL = "operational"
    TEMPORARILY_CLOSED = "temporarily_closed"
    PERMANENTLY_CLOSED = "permanently_closed"
    COMING_SOON = "coming_soon"
    
class BusinessType(str, Enum):
    """Universal business type categories"""
    RESTAURANT = "restaurant"
    RETAIL = "retail"
    SERVICE = "service"
    HEALTHCARE = "healthcare"
    AUTOMOTIVE = "automotive"
    BEAUTY = "beauty"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    FINANCIAL = "financial"
    FITNESS = "fitness"
    HOME_SERVICES = "home_services"
    HOSPITALITY = "hospitality"
    LEGAL = "legal"
    MANUFACTURING = "manufacturing"
    NONPROFIT = "nonprofit"
    PROFESSIONAL = "professional"
    REAL_ESTATE = "real_estate"
    TECHNOLOGY = "technology"
    TRANSPORTATION = "transportation"
    OTHER = "other"

class DayOfWeek(str, Enum):
    """Universal day of week representation"""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

@dataclass
class UniversalContact:
    """Universal contact information"""
    primary_phone: Optional[str] = None
    secondary_phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_phone": self.primary_phone,
            "secondary_phone": self.secondary_phone,
            "email": self.email,
            "website": self.website
        }

@dataclass
class UniversalLocation:
    """Universal location/address information"""
    street_address: Optional[str] = None
    street_address_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    formatted_address: Optional[str] = None
    place_id: Optional[str] = None  # Universal place identifier
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "street_address": self.street_address,
            "street_address_2": self.street_address_2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "formatted_address": self.formatted_address,
            "place_id": self.place_id
        }

@dataclass
class UniversalHours:
    """Universal business hours representation"""
    monday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    tuesday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    wednesday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    thursday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    friday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    saturday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    sunday: Optional[List[Dict[str, str]]] = field(default_factory=list)
    
    special_hours: Optional[List[Dict[str, Any]]] = field(default_factory=list)  # Holidays, etc.
    
    def add_hours(self, day: DayOfWeek, open_time: str, close_time: str):
        """Add hours for a specific day"""
        day_attr = getattr(self, day.value)
        if day_attr is None:
            day_attr = []
            setattr(self, day.value, day_attr)
        
        day_attr.append({
            "open": open_time,
            "close": close_time
        })
    
    def is_open_24_7(self) -> bool:
        """Check if business is open 24/7"""
        all_days = [self.monday, self.tuesday, self.wednesday, self.thursday, 
                   self.friday, self.saturday, self.sunday]
        return all(
            day and len(day) == 1 and day[0]["open"] == "00:00" and day[0]["close"] == "23:59"
            for day in all_days
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "monday": self.monday,
            "tuesday": self.tuesday,
            "wednesday": self.wednesday,
            "thursday": self.thursday,
            "friday": self.friday,
            "saturday": self.saturday,
            "sunday": self.sunday,
            "special_hours": self.special_hours
        }

@dataclass
class UniversalCategory:
    """Universal business category"""
    primary_category: str
    secondary_categories: List[str] = field(default_factory=list)
    industry: Optional[str] = None
    business_type: Optional[BusinessType] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_category": self.primary_category,
            "secondary_categories": self.secondary_categories,
            "industry": self.industry,
            "business_type": self.business_type.value if self.business_type else None
        }

@dataclass
class UniversalPhoto:
    """Universal photo/media representation"""
    url: str
    caption: Optional[str] = None
    alt_text: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    is_primary: bool = False
    photo_type: Optional[str] = None  # logo, cover, interior, exterior, product, etc.
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "caption": self.caption,
            "alt_text": self.alt_text,
            "width": self.width,
            "height": self.height,
            "is_primary": self.is_primary,
            "photo_type": self.photo_type
        }

@dataclass
class UniversalReview:
    """Universal review representation"""
    rating: float
    text: Optional[str] = None
    author_name: Optional[str] = None
    author_photo: Optional[str] = None
    created_at: Optional[datetime] = None
    platform_review_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rating": self.rating,
            "text": self.text,
            "author_name": self.author_name,
            "author_photo": self.author_photo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "platform_review_id": self.platform_review_id
        }

@dataclass
class UniversalBusinessData:
    """
    Universal business data model that works across all platforms
    This is the single source of truth for business information
    """
    # Core business information
    name: str
    description: Optional[str] = None
    status: BusinessStatus = BusinessStatus.OPERATIONAL
    
    # Location information
    location: Optional[UniversalLocation] = None
    
    # Contact information
    contact: Optional[UniversalContact] = None
    
    # Business hours
    hours: Optional[UniversalHours] = None
    
    # Categories and classification
    categories: Optional[UniversalCategory] = None
    
    # Media
    photos: List[UniversalPhoto] = field(default_factory=list)
    logo_url: Optional[str] = None
    
    # Reviews and ratings
    reviews: List[UniversalReview] = field(default_factory=list)
    overall_rating: Optional[float] = None
    total_reviews: int = 0
    
    # Additional attributes
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "location": self.location.to_dict() if self.location else None,
            "contact": self.contact.to_dict() if self.contact else None,
            "hours": self.hours.to_dict() if self.hours else None,
            "categories": self.categories.to_dict() if self.categories else None,
            "photos": [photo.to_dict() for photo in self.photos],
            "logo_url": self.logo_url,
            "reviews": [review.to_dict() for review in self.reviews],
            "overall_rating": self.overall_rating,
            "total_reviews": self.total_reviews,
            "attributes": self.attributes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UniversalBusinessData':
        """Create from dictionary"""
        location = None
        if data.get("location"):
            location = UniversalLocation(**data["location"])
        
        contact = None
        if data.get("contact"):
            contact = UniversalContact(**data["contact"])
        
        hours = None
        if data.get("hours"):
            hours = UniversalHours(**data["hours"])
        
        categories = None
        if data.get("categories"):
            cat_data = data["categories"].copy()
            if "business_type" in cat_data and cat_data["business_type"]:
                cat_data["business_type"] = BusinessType(cat_data["business_type"])
            categories = UniversalCategory(**cat_data)
        
        photos = []
        if data.get("photos"):
            photos = [UniversalPhoto(**photo) for photo in data["photos"]]
        
        reviews = []
        if data.get("reviews"):
            for review in data["reviews"]:
                if "created_at" in review and review["created_at"]:
                    review["created_at"] = datetime.fromisoformat(review["created_at"])
                reviews.append(UniversalReview(**review))
        
        # Handle datetime fields
        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])
        
        updated_at = None
        if data.get("updated_at"):
            updated_at = datetime.fromisoformat(data["updated_at"])
        
        return cls(
            name=data["name"],
            description=data.get("description"),
            status=BusinessStatus(data.get("status", BusinessStatus.OPERATIONAL)),
            location=location,
            contact=contact,
            hours=hours,
            categories=categories,
            photos=photos,
            logo_url=data.get("logo_url"),
            reviews=reviews,
            overall_rating=data.get("overall_rating"),
            total_reviews=data.get("total_reviews", 0),
            attributes=data.get("attributes", {}),
            created_at=created_at,
            updated_at=updated_at
        )
    
    def add_photo(self, url: str, is_primary: bool = False, **kwargs):
        """Add a photo to the business"""
        photo = UniversalPhoto(url=url, is_primary=is_primary, **kwargs)
        
        # If this is primary, make sure no other photo is primary
        if is_primary:
            for existing_photo in self.photos:
                existing_photo.is_primary = False
        
        self.photos.append(photo)
    
    def add_review(self, rating: float, **kwargs):
        """Add a review and update overall rating"""
        review = UniversalReview(rating=rating, **kwargs)
        self.reviews.append(review)
        
        # Recalculate overall rating
        self.total_reviews = len(self.reviews)
        if self.total_reviews > 0:
            self.overall_rating = sum(r.rating for r in self.reviews) / self.total_reviews
    
    def get_primary_photo(self) -> Optional[UniversalPhoto]:
        """Get the primary photo"""
        for photo in self.photos:
            if photo.is_primary:
                return photo
        return self.photos[0] if self.photos else None
    
    def validate(self) -> List[str]:
        """Validate business data and return list of errors"""
        errors = []
        
        if not self.name or not self.name.strip():
            errors.append("Business name is required")
        
        if not self.location:
            errors.append("Location is required")
        elif not self.location.city or not self.location.state:
            errors.append("City and state are required in location")
        
        if self.contact and self.contact.email:
            if "@" not in self.contact.email:
                errors.append("Invalid email format")
        
        if self.overall_rating is not None:
            if not (0 <= self.overall_rating <= 5):
                errors.append("Overall rating must be between 0 and 5")
        
        return errors

@dataclass  
class UniversalSyncMapping:
    """Maps universal business data to platform-specific IDs and data"""
    business_id: str
    platform: str
    platform_id: str
    platform_data: Dict[str, Any] = field(default_factory=dict)
    last_synced: Optional[datetime] = None
    sync_status: str = "pending"
    is_verified: bool = False
    is_claimed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "business_id": self.business_id,
            "platform": self.platform,
            "platform_id": self.platform_id,
            "platform_data": self.platform_data,
            "last_synced": self.last_synced.isoformat() if self.last_synced else None,
            "sync_status": self.sync_status,
            "is_verified": self.is_verified,
            "is_claimed": self.is_claimed
        }