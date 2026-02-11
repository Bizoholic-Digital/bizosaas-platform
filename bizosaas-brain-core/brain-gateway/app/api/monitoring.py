from fastapi import APIRouter, Depends
from app.services.monitoring_service import MonitoringService
from app.dependencies import get_current_user
from domain.ports.identity_port import AuthenticatedUser

router = APIRouter()
monitor = MonitoringService()

@router.get("/status")
async def get_platform_status(current_user: AuthenticatedUser = Depends(get_current_user)):
    """Unified health and status check for the platform admin"""
    if not current_user.is_superuser:
        return {"error": "Unauthorized"}
        
    health = await monitor.get_system_health()
    storage = await monitor.check_neon_storage()
    credits = await monitor.check_api_credits()
    
    return {
        "health": health,
        "storage": storage,
        "credits": credits
    }

@router.get("/storage")
async def check_storage(current_user: AuthenticatedUser = Depends(get_current_user)):
    if not current_user.is_superuser:
        return {"error": "Unauthorized"}
    return await monitor.check_neon_storage()

@router.get("/credits")
async def check_credits(current_user: AuthenticatedUser = Depends(get_current_user)):
    if not current_user.is_superuser:
        return {"error": "Unauthorized"}
    return await monitor.check_api_credits()
