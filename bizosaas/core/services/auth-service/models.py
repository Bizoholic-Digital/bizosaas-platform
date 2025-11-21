"""
Database models for BizOSaaS Authentication Service
Using fastapi-users with PostgreSQL backend
"""
from datetime import datetime
from typing import Optional
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class Tenant(Base):
    """Multi-tenant organization model"""
    __tablename__ = "tenants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="tenant")

class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model extending fastapi-users base"""
    __tablename__ = "users"
    
    # Additional fields beyond fastapi-users base
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), default="user")  # super_admin, tenant_admin, user, readonly, agent
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    avatar = Column(String(500))
    allowed_services = Column(String(1000))  # JSON string of allowed service IDs
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    
    def __repr__(self):
        return f"<User {self.email}>"
