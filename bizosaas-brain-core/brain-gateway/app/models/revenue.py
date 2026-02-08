from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON, Boolean, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .base import Base

class PortalRevenue(Base):
    __tablename__ = "portal_revenue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Source details (e.g., 'domain_purchase', 'affiliate_commission', 'subscription')
    source_type = Column(String(50), nullable=False, index=True)
    source_id = Column(String(100), nullable=True) # External ID like Namecheap transaction ID
    
    # Vendor/Partner details
    partner_name = Column(String(100), nullable=True) # 'Namecheap', 'Hostinger', 'GoDaddy', 'Wordpress'
    
    # Financials
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    commission_amount = Column(Float, default=0.0) # Our platform's cut
    partner_payout = Column(Float, default=0.0) # Amount to be paid to partner (if we collect and payout)
    
    status = Column(String(20), default="pending", index=True) # 'pending', 'collected', 'payout_completed'
    details = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DomainInventory(Base):
    __tablename__ = "domain_inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    domain_name = Column(String(255), nullable=False, unique=True, index=True)
    registrar = Column(String(50)) # 'namecheap', 'godaddy', etc.
    
    status = Column(String(20), default="active") # 'active', 'expired', 'transferring'
    expiry_date = Column(DateTime, nullable=True)
    
    # Mapping details
    target_service = Column(String(50), nullable=True) # 'directory', 'wordpress', 'custom'
    target_slug = Column(String(100), nullable=True) # The slug it maps to (e.g. business-slug)
    
    auto_renew = Column(Boolean, default=True)
    dns_configured = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DomainSearchHistory(Base):
    __tablename__ = "domain_search_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    query = Column(String(255), nullable=False)
    tlds_searched = Column(JSON, nullable=True) # List of TLDs searched
    results = Column(JSON, nullable=True) # Cache of availability results
    
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
