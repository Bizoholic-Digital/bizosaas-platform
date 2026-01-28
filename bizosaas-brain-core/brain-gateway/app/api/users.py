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
    job_title: Optional[str] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None

@router.get("/me")
async def get_me(
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    db_user = None
    try:
        from uuid import UUID
        # Only query if it looks like a UUID
        UUID(str(user.id))
        db_user = db.query(User).filter(User.id == user.id).first()
    except:
        # Fallback for non-UUID strings (like Clerk IDs)
        db_user = None
        
    if not db_user:
        # Fallback to info from current_user (from JWT/Clerk)
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.name.split()[0] if user.name else "",
            "last_name": " ".join(user.name.split()[1:]) if user.name and " " in user.name else "",
            "role": user.role
        }
    
    prefs = db_user.platform_preferences or {}
    
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "phone": db_user.phone,
        "avatar_url": db_user.avatar_url,
        "role": db_user.role,
        "job_title": prefs.get("job_title"),
        "timezone": prefs.get("timezone", "UTC"),
        "locale": prefs.get("locale", "en-US"),
        "company": db_user.tenant.name if db_user.tenant else None
    }

@router.patch("/me")
async def update_me(
    update_data: UserProfileUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    db_user = None
    try:
        from uuid import UUID
        UUID(str(user.id))
        db_user = db.query(User).filter(User.id == user.id).first()
    except:
        db_user = None
        
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
    
    # Update preferences
    if not db_user.platform_preferences:
        db_user.platform_preferences = {}
        
    preferences_changed = False
    
    if update_data.job_title is not None:
        db_user.platform_preferences["job_title"] = update_data.job_title
        preferences_changed = True
        
    if update_data.timezone is not None:
        db_user.platform_preferences["timezone"] = update_data.timezone
        preferences_changed = True

    if update_data.locale is not None:
        db_user.platform_preferences["locale"] = update_data.locale
        preferences_changed = True
        
    # Force SQLAlchemy to detect change if only JSON content changed
    if preferences_changed:
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(db_user, "platform_preferences")
    
    db.commit()
    db.refresh(db_user)
    
    return {"status": "success", "message": "Profile updated"}

@router.post("/me/change-password")
async def change_password(
    passwords: Dict[str, str] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user),
    identity: Any = Depends(lambda: None) # We'll fetch it inside to avoid circular check
):
    """Update current user's password."""
    new_password = passwords.get("new_password")
    if not new_password:
        raise HTTPException(status_code=400, detail="New password is required")
    
    from app.dependencies import get_identity_port
    identity_port = get_identity_port()
    
    success = await identity_port.change_password(user.id, new_password)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update password")
    
    return {"status": "success", "message": "Password updated successfully"}

@router.post("/me/mfa")
async def toggle_mfa(
    mfa_data: Dict[str, bool] = Body(...),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Enable or disable MFA."""
    enabled = mfa_data.get("enabled", False)
    
    from app.dependencies import get_identity_port
    identity_port = get_identity_port()
    
    success = await identity_port.toggle_mfa(user.id, enabled)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update MFA settings")
    
    return {"status": "success", "message": f"MFA {'enabled' if enabled else 'disabled'}"}
