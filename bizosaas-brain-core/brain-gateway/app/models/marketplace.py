import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class AffiliatePartner(Base):
    """
    Represents an external theme provider or affiliate program (e.g., Envato).
    """
    __tablename__ = "affiliate_partners"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    website_url = Column(String, nullable=True)
    api_key_vault_path = Column(String, nullable=True) # Path to secret in Vault
    api_config = Column(JSON, default={}) # Credentials, endpoints, etc.
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    themes = relationship("ThemeTemplate", back_populates="partner", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "website_url": self.website_url,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class ThemeTemplate(Base):
    """
    Represents a specific website theme/template available in the marketplace.
    """
    __tablename__ = "theme_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    partner_id = Column(String, ForeignKey("affiliate_partners.id"), nullable=False)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String, index=True) # e.g., 'e-commerce', 'blog', 'saas'
    price = Column(Numeric(10, 2), default=0.00)
    currency = Column(String, default="USD")
    
    preview_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    affiliate_link = Column(String, nullable=True)
    
    tags = Column(JSON, default=[]) # e.g., ['modern', 'dark-mode', 'responsive']
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    partner = relationship("AffiliatePartner", back_populates="themes")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "category": self.category,
            "price": float(self.price) if self.price else 0.0,
            "currency": self.currency,
            "preview_url": self.preview_url,
            "thumbnail_url": self.thumbnail_url,
            "affiliate_link": self.affiliate_link,
            "tags": self.tags,
            "partner_name": self.partner.name if self.partner else None
        }
