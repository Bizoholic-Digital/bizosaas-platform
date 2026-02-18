from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, JSON, Numeric, Date, ARRAY, Text
from sqlalchemy.orm import relationship
from .base import Base
from .utils import GUID
import uuid
from datetime import datetime

class DirectoryListing(Base):
    __tablename__ = "directory_listings"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    business_slug = Column(String(255), unique=True, nullable=False, index=True)
    business_name = Column(String(255), nullable=False)
    google_place_id = Column(String(255), unique=True, nullable=True, index=True)
    
    # Contact Information
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    phone = Column(String(50), nullable=True)
    whatsapp = Column(String(50), nullable=True)
    email = Column(String(320), nullable=True)
    website = Column(String(255), nullable=True)
    video_url = Column(String(512), nullable=True)
    
    # Business Details
    category = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    hours_of_operation = Column(JSON, nullable=True)
    amenities = Column(JSON, nullable=True, default=[]) # List of amenity strings
    tags = Column(ARRAY(String), nullable=True, default=[])
    
    # Rich Content
    social_media = Column(JSON, nullable=True, default={}) # {facebook, twitter, instagram, linkedin, etc}
    pricing_info = Column(JSON, nullable=True, default={}) # {range, currency, description}
    events = Column(JSON, nullable=True, default=[]) # List of event objects
    products = Column(JSON, nullable=True, default=[]) # List of product objects
    coupons = Column(JSON, nullable=True, default=[]) # List of coupon objects
    
    # Google Places Data
    google_rating = Column(Numeric(2, 1), nullable=True)
    google_reviews_count = Column(Integer, nullable=True)
    google_photos = Column(JSON, nullable=True)
    google_data = Column(JSON, nullable=True) # Full place details
    
    # Ownership & Claims
    claimed = Column(Boolean, default=False, index=True)
    claimed_by = Column(GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    claimed_at = Column(DateTime(timezone=True), nullable=True)
    verification_status = Column(String(50), default="unverified")
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    canonical_url = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(50), default="active", index=True) # active, inactive, suspended
    visibility = Column(String(50), default="public", index=True) # public, private, unlisted
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    analytics = relationship("DirectoryAnalytics", back_populates="listing", cascade="all, delete-orphan")
    claim_requests = relationship("DirectoryClaimRequest", back_populates="listing")
    enquiries = relationship("DirectoryEnquiry", back_populates="listing")
    events_list = relationship("DirectoryEvent", back_populates="listing", cascade="all, delete-orphan")
    coupons_list = relationship("DirectoryCoupon", back_populates="listing", cascade="all, delete-orphan")

class DirectoryEnquiry(Base):
    __tablename__ = "directory_enquiries"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    listing_id = Column(GUID, ForeignKey("directory_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    
    status = Column(String(20), default="new") # new, read, replied, spam
    source = Column(String(50), default="directory") # listing_page, contact_form
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    listing = relationship("DirectoryListing", back_populates="enquiries")

class DirectoryEvent(Base):
    __tablename__ = "directory_events"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    listing_id = Column(GUID, ForeignKey("directory_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    location = Column(String(255), nullable=True)
    image_url = Column(String(512), nullable=True)
    external_link = Column(String(512), nullable=True)
    
    status = Column(String(20), default="upcoming") # upcoming, ongoing, past, cancelled
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    listing = relationship("DirectoryListing", back_populates="events_list")

class DirectoryCoupon(Base):
    __tablename__ = "directory_coupons"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    listing_id = Column(GUID, ForeignKey("directory_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    code = Column(String(50), nullable=True)
    discount_value = Column(String(100), nullable=True) # e.g. "20% OFF", "$10 OFF"
    expiry_date = Column(DateTime(timezone=True), nullable=True)
    terms_link = Column(String(512), nullable=True)
    
    status = Column(String(20), default="active") # active, expired, disabled
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    listing = relationship("DirectoryListing", back_populates="coupons_list")

class DirectoryAnalytics(Base):
    __tablename__ = "directory_analytics"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    listing_id = Column(GUID, ForeignKey("directory_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Traffic Metrics
    page_views = Column(Integer, default=0)
    unique_visitors = Column(Integer, default=0)
    
    # Engagement Metrics
    phone_clicks = Column(Integer, default=0)
    website_clicks = Column(Integer, default=0)
    direction_clicks = Column(Integer, default=0)
    
    # Conversion Metrics
    claim_requests = Column(Integer, default=0)
    upgrade_requests = Column(Integer, default=0)
    
    # Time-based
    date = Column(Date, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    listing = relationship("DirectoryListing", back_populates="analytics")

class DirectoryClaimRequest(Base):
    __tablename__ = "directory_claim_requests"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    listing_id = Column(GUID, ForeignKey("directory_listings.id"), nullable=False, index=True)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False, index=True)
    
    # Verification Details
    verification_method = Column(String(50)) # email, phone, document
    verification_data = Column(JSON, nullable=True)
    verification_code = Column(String(20), nullable=True)
    verification_expiry = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    status = Column(String(50), default="pending") # pending, approved, rejected
    reviewed_by = Column(GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    listing = relationship("DirectoryListing", back_populates="claim_requests")
