"""
Admin API for schedule management.

Provides endpoints for creating, listing, updating, and managing
Temporal schedules for analytics workflows.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import logging

from app.dependencies import require_role, AuthenticatedUser
from app.services.schedule_manager import get_schedule_manager
from app.config.schedule_config import get_schedule_specs
from temporalio.client import Client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/schedules", tags=["Admin - Schedules"])


# Pydantic models
class CreateScheduleRequest(BaseModel):
    """Request to create a new schedule."""
    schedule_id: str = Field(..., description="Unique schedule identifier")
    cron: str = Field(..., description="Cron expression (minute hour day month day_of_week)")
    snapshot_type: str = Field(..., description="Snapshot type (hourly, daily, weekly)")
    time_range_hours: int = Field(..., description="Hours to analyze per run")
    timezone: str = Field(default="UTC", description="Timezone for schedule")
    description: str = Field(default="", description="Schedule description")


class UpdateScheduleRequest(BaseModel):
    """Request to update a schedule."""
    cron: str | None = Field(None, description="New cron expression")
    timezone: str | None = Field(None, description="New timezone")
    description: str | None = Field(None, description="New description")


class ScheduleResponse(BaseModel):
    """Schedule information response."""
    schedule_id: str
    state: str
    next_run: str | None
    last_run: str | None
    spec: str


# Dependency to get Temporal client
async def get_temporal_client() -> Client:
    """Get connected Temporal client."""
    from app.config.settings import settings
    client = await Client.connect(settings.temporal_address)
    return client


@router.post("/analytics", status_code=status.HTTP_201_CREATED)
async def create_analytics_schedule(
    request: CreateScheduleRequest,
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    temporal_client: Client = Depends(get_temporal_client)
):
    """
    Create a new analytics schedule.
    
    Requires Super Admin role.
    """
    try:
        manager = await get_schedule_manager(temporal_client)
        
        await manager.create_analytics_schedule(
            schedule_id=request.schedule_id,
            cron=request.cron,
            snapshot_type=request.snapshot_type,
            time_range_hours=request.time_range_hours,
            timezone_str=request.timezone,
            description=request.description
        )
        
        return {
            "message": f"Schedule {request.schedule_id} created successfully",
            "schedule_id": request.schedule_id
        }
    
    except Exception as e:
        logger.error(f"Failed to create schedule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create schedule: {str(e)}"
        )


@router.get("", response_model=List[ScheduleResponse])
async def list_schedules(
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    temporal_client: Client = Depends(get_temporal_client)
):
    """
    List all analytics schedules.
    
    Requires Super Admin role.
    """
    try:
        manager = await get_schedule_manager(temporal_client)
        schedules = await manager.list_schedules()
        
        return [
            ScheduleResponse(
                schedule_id=s["schedule_id"],
                state=s["state"],
                next_run=s["next_run"].isoformat() if s["next_run"] else None,
                last_run=s["last_run"].isoformat() if s["last_run"] else None,
                spec=s["spec"]
            )
            for s in schedules
        ]
    
    except Exception as e:
        logger.error(f"Failed to list schedules: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list schedules: {str(e)}"
        )


@router.get("/specs")
async def get_schedule_specifications(
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get configured schedule specifications.
    
    Returns the default schedule configurations from environment.
    Requires Super Admin role.
    """
    return {
        "schedules": get_schedule_specs()
    }


@router.post("/{schedule_id}/pause")
async def pause_schedule(
    schedule_id: str,
    note: str = "",
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    temporal_client: Client = Depends(get_temporal_client)
):
    """
    Pause a schedule.
    
    Requires Super Admin role.
    """
    try:
        manager = await get_schedule_manager(temporal_client)
        await manager.pause_schedule(schedule_id, note)
        
        return {
            "message": f"Schedule {schedule_id} paused successfully",
            "schedule_id": schedule_id
        }
    
    except Exception as e:
        logger.error(f"Failed to pause schedule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pause schedule: {str(e)}"
        )


@router.post("/{schedule_id}/resume")
async def resume_schedule(
    schedule_id: str,
    note: str = "",
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    temporal_client: Client = Depends(get_temporal_client)
):
    """
    Resume a paused schedule.
    
    Requires Super Admin role.
    """
    try:
        manager = await get_schedule_manager(temporal_client)
        await manager.resume_schedule(schedule_id, note)
        
        return {
            "message": f"Schedule {schedule_id} resumed successfully",
            "schedule_id": schedule_id
        }
    
    except Exception as e:
        logger.error(f"Failed to resume schedule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resume schedule: {str(e)}"
        )


@router.post("/{schedule_id}/trigger")
async def trigger_schedule(
    schedule_id: str,
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    temporal_client: Client = Depends(get_temporal_client)
):
    """
    Manually trigger a schedule to run immediately.
    
    Requires Super Admin role.
    """
    try:
        manager = await get_schedule_manager(temporal_client)
        await manager.trigger_schedule(schedule_id)
        
        return {
            "message": f"Schedule {schedule_id} triggered successfully",
            "schedule_id": schedule_id
        }
    
    except Exception as e:
        logger.error(f"Failed to trigger schedule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger schedule: {str(e)}"
        )


@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: str,
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    temporal_client: Client = Depends(get_temporal_client)
):
    """
    Delete a schedule.
    
    Requires Super Admin role.
    """
    try:
        manager = await get_schedule_manager(temporal_client)
        await manager.delete_schedule(schedule_id)
        
        return {
            "message": f"Schedule {schedule_id} deleted successfully",
            "schedule_id": schedule_id
        }
    
    except Exception as e:
        logger.error(f"Failed to delete schedule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete schedule: {str(e)}"
        )
