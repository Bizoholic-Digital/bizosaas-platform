from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.models.user import User
from domain.ports.identity_port import AuthenticatedUser
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter(prefix="/api/users", tags=["users"])

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    job_title: Optional[str] = None  # We can store this in platform_preferences or a new field

@router.get("/me")
async def get_me(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        # Fallback to info from current_user (from JWT/Clerk)
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.name.split()[0] if user.name else "",
            "last_name": " ".join(user.name.split()[1:]) if user.name and " " in user.name else "",
            "role": user.role
        }
    
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "phone": db_user.phone,
        "avatar_url": db_user.avatar_url,
        "role": db_user.role,
        "job_title": db_user.platform_preferences.get("job_title") if db_user.platform_preferences else None,
        "company": db_user.tenant.name if db_user.tenant else None
    }

@router.patch("/me")
async def update_me(
    update_data: UserProfileUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found in local database")
    
    if update_data.first_name is not None:
        db_user.first_name = update_data.first_name
    if update_data.last_name is not None:
        db_user.last_name = update_data.last_name
    if update_data.phone is not None:
        db_user.phone = update_data.phone
    if update_data.avatar_url is not None:
        db_user.avatar_url = update_data.avatar_url
    
    if update_data.job_title is not None:
        if not db_user.platform_preferences:
            db_user.platform_preferences = {}
        db_user.platform_preferences["job_title"] = update_data.job_title
    
    db.commit()
    db.refresh(db_user)
    
    return {"status": "success", "message": "Profile updated"}
