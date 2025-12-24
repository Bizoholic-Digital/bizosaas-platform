from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User, Tenant
import os
import re
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Using argon2 to match existing database entries
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: str | None = None

class RegisterResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    message: str

def get_password_hash(password):
    return pwd_context.hash(password)

def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search("[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    if not re.search("[a-z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
    if not re.search("[0-9]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one digit")

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    # 1. Validate password strength
    validate_password_strength(data.password)
    
    # 2. Check if user exists
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 3. Hash password using Argon2
    hashed_password = get_password_hash(data.password)
    
    # 4. Create or Find Tenant
    tenant_id = None
    if data.company_name:
        # Create a basic slug
        slug = re.sub(r'[^a-zA-Z0-9]', '-', data.company_name.lower())
        # Ensure slug is not empty and unique
        if not slug:
            slug = "company-" + str(uuid.uuid4())[:8]
            
        existing_tenant = db.query(Tenant).filter(Tenant.slug == slug).first()
        if existing_tenant:
            tenant_id = existing_tenant.id
        else:
            new_tenant = Tenant(
                name=data.company_name,
                slug=slug,
                status="active"
            )
            db.add(new_tenant)
            db.flush() # Get tenant.id
            tenant_id = new_tenant.id
    else:
        # For this system, we require a tenant
        raise HTTPException(status_code=400, detail="Company name is required for registration")
    
    # 5. Create user in database
    new_user = User(
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
        tenant_id=tenant_id,
        is_active=True,
        is_superuser=False,
        is_verified=False,
        role="user",
        login_count=0,
        failed_login_attempts=0,
        two_factor_enabled=False,
        marketing_consent=False
    )
    db.add(new_user)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    db.refresh(new_user)
    
    return RegisterResponse(
        id=str(new_user.id),
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        message="User registered successfully"
    )
