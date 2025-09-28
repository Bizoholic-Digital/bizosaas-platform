"""
Business Directory Models
Database models for business listings, categories, reviews, events, products, and coupons
"""

from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Index, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from typing import Optional, List, Dict, Any
import json
import uuid
from datetime import datetime

from .base import (
    BusinessBaseModel, 
    CategoryBaseModel, 
    BaseModel, 
    RatingMixin, 
    MediaMixin,
    register_model
)


@register_model
class BusinessCategory(CategoryBaseModel):
    """
    Hierarchical business categories with tenant isolation
    """
    __tablename__ = "business_categories"
    
    # Category-specific fields
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        doc="Category active status"
    )
    
    business_count = Column(
        Integer,
        default=0,
        nullable=False,
        doc="Number of businesses in this category"
    )
    
    # SEO fields
    keywords = Column(
        String(500),
        nullable=True,
        doc="SEO keywords for category"
    )
    
    # Parent relationship
    parent = relationship(
        "BusinessCategory",
        remote_side="BusinessCategory.id",
        backref="children"
    )
    
    def __repr__(self):
        return f"<BusinessCategory(name='{self.name}', tenant_id='{self.tenant_id}')>"
    
    @property
    def full_path(self) -> str:
        """Get full category path"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
    
    def get_subcategories(self, include_inactive: bool = False) -> List['BusinessCategory']:
        """Get all subcategories"""
        query_filter = [BusinessCategory.parent_id == self.id]
        if not include_inactive:
            query_filter.append(BusinessCategory.is_active == True)
        # This would be implemented with a database query
        return []
    
    def update_business_count(self, count: int):
        """Update business count for this category"""
        self.business_count = count


@register_model
class BusinessListing(BusinessBaseModel, RatingMixin, MediaMixin):
    """
    Main business listing model with comprehensive business information
    """
    __tablename__ = "business_listings"
    
    # Basic business information
    name = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Business name"
    )
    
    description = Column(
        Text,
        nullable=True,
        doc="Business description"
    )
    
    short_description = Column(
        String(500),
        nullable=True,
        doc="Short business description for listings"
    )
    
    # Category relationship
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey('business_categories.id'),
        nullable=True,
        index=True,
        doc="Primary business category"
    )
    
    category = relationship("BusinessCategory", backref="businesses")
    
    # Contact information
    email = Column(
        String(255),
        nullable=True,
        index=True,
        doc="Business email address"
    )
    
    phone = Column(
        String(50),
        nullable=True,
        doc="Business phone number"
    )
    
    website = Column(
        String(500),
        nullable=True,
        doc="Business website URL"
    )
    
    # Address information
    address_line_1 = Column(
        String(255),
        nullable=True,
        doc="Primary address line"
    )
    
    address_line_2 = Column(
        String(255),
        nullable=True,
        doc="Secondary address line"
    )
    
    city = Column(
        String(100),
        nullable=True,
        index=True,
        doc="City"
    )
    
    state = Column(
        String(100),
        nullable=True,
        index=True,
        doc="State or province"
    )
    
    postal_code = Column(
        String(20),
        nullable=True,
        doc="Postal or ZIP code"
    )
    
    country = Column(
        String(100),
        nullable=True,
        index=True,
        doc="Country"
    )
    
    # Business hours (JSON format)\n    business_hours = Column(\n        JSON,\n        nullable=True,\n        doc=\"Business hours in JSON format\"\n    )\n    \n    # Social media links\n    social_media = Column(\n        JSON,\n        nullable=True,\n        doc=\"Social media links in JSON format\"\n    )\n    \n    # Business features and amenities\n    amenities = Column(\n        JSON,\n        nullable=True,\n        doc=\"Business amenities and features\"\n    )\n    \n    # Pricing information\n    price_range = Column(\n        String(10),\n        nullable=True,\n        doc=\"Price range indicator (e.g., $, $$, $$$, $$$$)\"\n    )\n    \n    # Business validation\n    is_claimed = Column(\n        Boolean,\n        default=False,\n        nullable=False,\n        index=True,\n        doc=\"Whether business is claimed by owner\"\n    )\n    \n    claimed_at = Column(\n        DateTime(timezone=True),\n        nullable=True,\n        doc=\"When business was claimed\"\n    )\n    \n    claimed_by = Column(\n        UUID(as_uuid=True),\n        nullable=True,\n        doc=\"User who claimed the business\"\n    )\n    \n    # SEO and additional metadata\n    tags = Column(\n        JSON,\n        nullable=True,\n        doc=\"Business tags for categorization\"\n    )\n    \n    # Business owner information\n    owner_name = Column(\n        String(255),\n        nullable=True,\n        doc=\"Business owner name\"\n    )\n    \n    owner_email = Column(\n        String(255),\n        nullable=True,\n        doc=\"Business owner email\"\n    )\n    \n    @validates('email', 'owner_email')\n    def validate_email(self, key, email):\n        \"\"\"Validate email format\"\"\"\n        if email:\n            import re\n            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n            if not re.match(pattern, email):\n                raise ValueError(f\"Invalid email format: {email}\")\n        return email\n    \n    @validates('website')\n    def validate_website(self, key, website):\n        \"\"\"Validate website URL\"\"\"\n        if website and not website.startswith(('http://', 'https://')):\n            website = f\"https://{website}\"\n        return website\n    \n    def __repr__(self):\n        return f\"<BusinessListing(name='{self.name}', city='{self.city}')>\"\n    \n    def update_search_content(self):\n        \"\"\"Update search content for vector embedding\"\"\"\n        content_parts = [\n            self.name or \"\",\n            self.description or \"\",\n            self.short_description or \"\",\n            self.city or \"\",\n            self.state or \"\",\n            \" \".join(self.tag_list),\n            self.category.name if self.category else \"\"\n        ]\n        self.search_content = \" \".join(filter(None, content_parts))\n    \n    @property\n    def full_address(self) -> str:\n        \"\"\"Get formatted full address\"\"\"\n        parts = [\n            self.address_line_1,\n            self.address_line_2,\n            self.city,\n            self.state,\n            self.postal_code,\n            self.country\n        ]\n        return \", \".join(filter(None, parts))\n    \n    @property\n    def tag_list(self) -> List[str]:\n        \"\"\"Get tags as list\"\"\"\n        try:\n            return self.tags if isinstance(self.tags, list) else []\n        except (TypeError, AttributeError):\n            return []\n    \n    @property\n    def amenity_list(self) -> List[str]:\n        \"\"\"Get amenities as list\"\"\"\n        try:\n            return self.amenities if isinstance(self.amenities, list) else []\n        except (TypeError, AttributeError):\n            return []\n    \n    @property\n    def social_links(self) -> Dict[str, str]:\n        \"\"\"Get social media links\"\"\"\n        try:\n            return self.social_media if isinstance(self.social_media, dict) else {}\n        except (TypeError, AttributeError):\n            return {}\n    \n    @property\n    def hours_today(self) -> Optional[Dict[str, str]]:\n        \"\"\"Get today's business hours\"\"\"\n        if not self.business_hours:\n            return None\n        \n        try:\n            hours = self.business_hours if isinstance(self.business_hours, dict) else {}\n            today = datetime.now().strftime('%A').lower()\n            return hours.get(today)\n        except (TypeError, AttributeError):\n            return None\n    \n    def add_tag(self, tag: str):\n        \"\"\"Add tag to business\"\"\"\n        tags = self.tag_list\n        if tag not in tags:\n            tags.append(tag)\n            self.tags = tags\n    \n    def remove_tag(self, tag: str):\n        \"\"\"Remove tag from business\"\"\"\n        tags = self.tag_list\n        if tag in tags:\n            tags.remove(tag)\n            self.tags = tags\n    \n    def claim_business(self, user_id: str):\n        \"\"\"Claim business for a user\"\"\"\n        self.is_claimed = True\n        self.claimed_by = uuid.UUID(user_id)\n        self.claimed_at = datetime.utcnow()\n\n\n@register_model\nclass BusinessReview(BaseModel, MediaMixin):\n    \"\"\"Business reviews and ratings\"\"\"\n    __tablename__ = \"business_reviews\"\n    \n    # Review relationships\n    business_id = Column(\n        UUID(as_uuid=True),\n        ForeignKey('business_listings.id', ondelete='CASCADE'),\n        nullable=False,\n        index=True,\n        doc=\"Business being reviewed\"\n    )\n    \n    business = relationship(\"BusinessListing\", backref=\"reviews\")\n    \n    # Reviewer information\n    reviewer_name = Column(\n        String(255),\n        nullable=True,\n        doc=\"Reviewer name\"\n    )\n    \n    reviewer_email = Column(\n        String(255),\n        nullable=True,\n        doc=\"Reviewer email\"\n    )\n    \n    reviewer_id = Column(\n        UUID(as_uuid=True),\n        nullable=True,\n        index=True,\n        doc=\"Registered user who wrote review\"\n    )\n    \n    # Review content\n    title = Column(\n        String(255),\n        nullable=True,\n        doc=\"Review title\"\n    )\n    \n    content = Column(\n        Text,\n        nullable=True,\n        doc=\"Review content\"\n    )\n    \n    rating = Column(\n        Integer,\n        nullable=False,\n        doc=\"Rating score (1-5)\"\n    )\n    \n    # Review status and moderation\n    is_approved = Column(\n        Boolean,\n        default=False,\n        nullable=False,\n        index=True,\n        doc=\"Review approval status\"\n    )\n    \n    is_featured = Column(\n        Boolean,\n        default=False,\n        nullable=False,\n        doc=\"Featured review flag\"\n    )\n    \n    moderation_notes = Column(\n        Text,\n        nullable=True,\n        doc=\"Internal moderation notes\"\n    )\n    \n    # Review metadata\n    helpful_count = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Number of helpful votes\"\n    )\n    \n    visit_date = Column(\n        DateTime(timezone=True),\n        nullable=True,\n        doc=\"Date of business visit\"\n    )\n    \n    @validates('rating')\n    def validate_rating(self, key, rating):\n        \"\"\"Validate rating is between 1 and 5\"\"\"\n        if rating < 1 or rating > 5:\n            raise ValueError(\"Rating must be between 1 and 5\")\n        return rating\n    \n    def __repr__(self):\n        return f\"<BusinessReview(business_id='{self.business_id}', rating={self.rating})>\"\n    \n    def approve(self):\n        \"\"\"Approve the review\"\"\"\n        self.is_approved = True\n    \n    def mark_helpful(self):\n        \"\"\"Increment helpful count\"\"\"\n        self.helpful_count += 1\n\n\n@register_model\nclass BusinessEvent(BaseModel, MediaMixin):\n    \"\"\"Business events and announcements\"\"\"\n    __tablename__ = \"business_events\"\n    \n    # Event relationships\n    business_id = Column(\n        UUID(as_uuid=True),\n        ForeignKey('business_listings.id', ondelete='CASCADE'),\n        nullable=False,\n        index=True,\n        doc=\"Business hosting the event\"\n    )\n    \n    business = relationship(\"BusinessListing\", backref=\"events\")\n    \n    # Event information\n    title = Column(\n        String(255),\n        nullable=False,\n        doc=\"Event title\"\n    )\n    \n    description = Column(\n        Text,\n        nullable=True,\n        doc=\"Event description\"\n    )\n    \n    # Event timing\n    start_date = Column(\n        DateTime(timezone=True),\n        nullable=False,\n        index=True,\n        doc=\"Event start date and time\"\n    )\n    \n    end_date = Column(\n        DateTime(timezone=True),\n        nullable=True,\n        index=True,\n        doc=\"Event end date and time\"\n    )\n    \n    # Event details\n    location = Column(\n        String(500),\n        nullable=True,\n        doc=\"Event location (if different from business)\"\n    )\n    \n    event_type = Column(\n        String(100),\n        nullable=True,\n        index=True,\n        doc=\"Type of event\"\n    )\n    \n    is_free = Column(\n        Boolean,\n        default=True,\n        nullable=False,\n        doc=\"Whether event is free\"\n    )\n    \n    price = Column(\n        String(50),\n        nullable=True,\n        doc=\"Event price\"\n    )\n    \n    max_attendees = Column(\n        Integer,\n        nullable=True,\n        doc=\"Maximum number of attendees\"\n    )\n    \n    registration_url = Column(\n        String(500),\n        nullable=True,\n        doc=\"Event registration URL\"\n    )\n    \n    # Event status\n    is_published = Column(\n        Boolean,\n        default=False,\n        nullable=False,\n        index=True,\n        doc=\"Event published status\"\n    )\n    \n    is_cancelled = Column(\n        Boolean,\n        default=False,\n        nullable=False,\n        doc=\"Event cancelled status\"\n    )\n    \n    def __repr__(self):\n        return f\"<BusinessEvent(title='{self.title}', start_date='{self.start_date}')>\"\n    \n    @property\n    def is_upcoming(self) -> bool:\n        \"\"\"Check if event is upcoming\"\"\"\n        return self.start_date > datetime.utcnow() and not self.is_cancelled\n    \n    @property\n    def is_ongoing(self) -> bool:\n        \"\"\"Check if event is currently ongoing\"\"\"\n        now = datetime.utcnow()\n        return (self.start_date <= now <= (self.end_date or self.start_date) \n                and not self.is_cancelled)\n    \n    def cancel(self):\n        \"\"\"Cancel the event\"\"\"\n        self.is_cancelled = True\n\n\n@register_model\nclass BusinessProduct(BaseModel, MediaMixin):\n    \"\"\"Products or services offered by businesses\"\"\"\n    __tablename__ = \"business_products\"\n    \n    # Product relationships\n    business_id = Column(\n        UUID(as_uuid=True),\n        ForeignKey('business_listings.id', ondelete='CASCADE'),\n        nullable=False,\n        index=True,\n        doc=\"Business offering the product\"\n    )\n    \n    business = relationship(\"BusinessListing\", backref=\"products\")\n    \n    # Product information\n    name = Column(\n        String(255),\n        nullable=False,\n        index=True,\n        doc=\"Product name\"\n    )\n    \n    description = Column(\n        Text,\n        nullable=True,\n        doc=\"Product description\"\n    )\n    \n    category = Column(\n        String(100),\n        nullable=True,\n        index=True,\n        doc=\"Product category\"\n    )\n    \n    # Pricing\n    price = Column(\n        String(50),\n        nullable=True,\n        doc=\"Product price\"\n    )\n    \n    price_currency = Column(\n        String(3),\n        nullable=True,\n        doc=\"Price currency code\"\n    )\n    \n    # Product details\n    sku = Column(\n        String(100),\n        nullable=True,\n        index=True,\n        doc=\"Product SKU\"\n    )\n    \n    is_available = Column(\n        Boolean,\n        default=True,\n        nullable=False,\n        index=True,\n        doc=\"Product availability\"\n    )\n    \n    specifications = Column(\n        JSON,\n        nullable=True,\n        doc=\"Product specifications\"\n    )\n    \n    def __repr__(self):\n        return f\"<BusinessProduct(name='{self.name}', business_id='{self.business_id}')>\"\n\n\n@register_model\nclass BusinessCoupon(BaseModel):\n    \"\"\"Coupons and promotional offers\"\"\"\n    __tablename__ = \"business_coupons\"\n    \n    # Coupon relationships\n    business_id = Column(\n        UUID(as_uuid=True),\n        ForeignKey('business_listings.id', ondelete='CASCADE'),\n        nullable=False,\n        index=True,\n        doc=\"Business offering the coupon\"\n    )\n    \n    business = relationship(\"BusinessListing\", backref=\"coupons\")\n    \n    # Coupon information\n    title = Column(\n        String(255),\n        nullable=False,\n        doc=\"Coupon title\"\n    )\n    \n    description = Column(\n        Text,\n        nullable=True,\n        doc=\"Coupon description\"\n    )\n    \n    # Discount details\n    discount_type = Column(\n        String(20),\n        nullable=False,\n        doc=\"Discount type (percentage, fixed, bogo)\"\n    )\n    \n    discount_value = Column(\n        String(50),\n        nullable=False,\n        doc=\"Discount value\"\n    )\n    \n    # Coupon validity\n    valid_from = Column(\n        DateTime(timezone=True),\n        nullable=False,\n        index=True,\n        doc=\"Coupon valid from date\"\n    )\n    \n    valid_until = Column(\n        DateTime(timezone=True),\n        nullable=False,\n        index=True,\n        doc=\"Coupon expiry date\"\n    )\n    \n    # Usage limits\n    usage_limit = Column(\n        Integer,\n        nullable=True,\n        doc=\"Maximum number of uses\"\n    )\n    \n    usage_count = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Current usage count\"\n    )\n    \n    # Coupon code\n    coupon_code = Column(\n        String(50),\n        nullable=True,\n        index=True,\n        doc=\"Coupon code for redemption\"\n    )\n    \n    # Terms and conditions\n    terms = Column(\n        Text,\n        nullable=True,\n        doc=\"Coupon terms and conditions\"\n    )\n    \n    is_active = Column(\n        Boolean,\n        default=True,\n        nullable=False,\n        index=True,\n        doc=\"Coupon active status\"\n    )\n    \n    def __repr__(self):\n        return f\"<BusinessCoupon(title='{self.title}', business_id='{self.business_id}')>\"\n    \n    @property\n    def is_valid(self) -> bool:\n        \"\"\"Check if coupon is currently valid\"\"\"\n        now = datetime.utcnow()\n        return (self.is_active and \n                self.valid_from <= now <= self.valid_until and\n                (self.usage_limit is None or self.usage_count < self.usage_limit))\n    \n    def redeem(self) -> bool:\n        \"\"\"Redeem the coupon\"\"\"\n        if self.is_valid:\n            self.usage_count += 1\n            return True\n        return False\n\n\n@register_model\nclass BusinessAnalytics(BaseModel):\n    \"\"\"Business analytics and metrics\"\"\"\n    __tablename__ = \"business_analytics\"\n    \n    # Analytics relationships\n    business_id = Column(\n        UUID(as_uuid=True),\n        ForeignKey('business_listings.id', ondelete='CASCADE'),\n        nullable=False,\n        index=True,\n        doc=\"Business being tracked\"\n    )\n    \n    business = relationship(\"BusinessListing\", backref=\"analytics\")\n    \n    # Metrics data\n    date = Column(\n        DateTime(timezone=True),\n        nullable=False,\n        index=True,\n        doc=\"Analytics date\"\n    )\n    \n    views = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Number of views\"\n    )\n    \n    clicks = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Number of clicks\"\n    )\n    \n    phone_calls = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Number of phone calls\"\n    )\n    \n    website_visits = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Number of website visits\"\n    )\n    \n    direction_requests = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"Number of direction requests\"\n    )\n    \n    # Review metrics\n    new_reviews = Column(\n        Integer,\n        default=0,\n        nullable=False,\n        doc=\"New reviews received\"\n    )\n    \n    average_rating = Column(\n        String(5),\n        nullable=True,\n        doc=\"Average rating for the day\"\n    )\n    \n    def __repr__(self):\n        return f\"<BusinessAnalytics(business_id='{self.business_id}', date='{self.date}')>\"\n\n\n# Add table arguments for performance indexes\nfor model_class in [BusinessListing, BusinessReview, BusinessEvent, BusinessProduct, BusinessCoupon]:\n    # Add composite indexes for common queries\n    original_table_args = getattr(model_class, '__table_args__', ())\n    if hasattr(original_table_args, '__iter__') and not isinstance(original_table_args, str):\n        model_class.__table_args__ = original_table_args + (\n            Index(f'ix_{model_class.__tablename__}_business_tenant', 'business_id', 'tenant_id'),\n            Index(f'ix_{model_class.__tablename__}_created_tenant', 'created_at', 'tenant_id'),\n        )\n\n# Special indexes for search and filtering\nBusinessListing.__table_args__ = getattr(BusinessListing, '__table_args__', ()) + (\n    Index('ix_business_listings_location', 'city', 'state', 'country'),\n    Index('ix_business_listings_rating', 'rating_average', 'rating_count'),\n    Index('ix_business_listings_search', 'name', 'city', 'category_id'),\n)