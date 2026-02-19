"""
Cron Job Admin API — manage scheduled platform maintenance jobs.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.cron_job import CronJob, CronJobStatus, CronJobType
from app.dependencies import require_role, get_db
from app.domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/cron-jobs", tags=["admin-cron-jobs"])


class CronJobCreate(BaseModel):
    name: str
    description: Optional[str] = None
    job_type: CronJobType = CronJobType.custom
    schedule: str  # cron expression
    config: Optional[Dict[str, Any]] = None


class CronJobUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    schedule: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


def _format(job: CronJob) -> dict:
    return {
        "id": str(job.id),
        "name": job.name,
        "description": job.description,
        "job_type": job.job_type,
        "schedule": job.schedule,
        "status": job.status,
        "is_system": job.is_system,
        "last_run": job.last_run.isoformat() if job.last_run else None,
        "last_run_status": job.last_run_status,
        "last_run_output": job.last_run_output,
        "next_run": job.next_run.isoformat() if job.next_run else None,
        "config": job.config,
        "created_at": job.created_at.isoformat() if job.created_at else None,
    }


@router.get("")
async def list_cron_jobs(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """List all scheduled cron jobs."""
    jobs = db.query(CronJob).order_by(CronJob.created_at).all()
    return {"total": len(jobs), "jobs": [_format(j) for j in jobs]}


@router.post("", status_code=201)
async def create_cron_job(
    payload: CronJobCreate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Create a new cron job."""
    existing = db.query(CronJob).filter(CronJob.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Cron job '{payload.name}' already exists.")
    job = CronJob(**payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return _format(job)


@router.get("/{job_id}")
async def get_cron_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    job = db.query(CronJob).filter(CronJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Cron job not found.")
    return _format(job)


@router.put("/{job_id}")
async def update_cron_job(
    job_id: str,
    payload: CronJobUpdate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    job = db.query(CronJob).filter(CronJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Cron job not found.")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(job, field, value)
    job.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(job)
    return _format(job)


@router.put("/{job_id}/enable")
async def enable_cron_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Enable (unpause) a cron job."""
    job = db.query(CronJob).filter(CronJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Cron job not found.")
    job.status = CronJobStatus.active
    db.commit()
    return {"status": "enabled", "id": job_id}


@router.put("/{job_id}/disable")
async def disable_cron_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Pause a cron job."""
    job = db.query(CronJob).filter(CronJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Cron job not found.")
    job.status = CronJobStatus.paused
    db.commit()
    return {"status": "paused", "id": job_id}


@router.delete("/{job_id}", status_code=204)
async def delete_cron_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Delete a custom cron job (system jobs cannot be deleted)."""
    job = db.query(CronJob).filter(CronJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Cron job not found.")
    if job.is_system:
        raise HTTPException(status_code=403, detail="System cron jobs cannot be deleted.")
    db.delete(job)
    db.commit()


@router.post("/{job_id}/run-now")
async def run_cron_job_now(
    job_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Manually trigger a cron job immediately (runs safety scan for health/security jobs)."""
    job = db.query(CronJob).filter(CronJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Cron job not found.")

    result = {"triggered": True, "job": job.name, "timestamp": datetime.utcnow().isoformat()}

    # Run safety scan for applicable job types
    if job.job_type in (CronJobType.security_scan, CronJobType.health_check, CronJobType.compliance_check):
        from app.core.agents.safety_monitor_agent import safety_monitor_agent
        if job.job_type == CronJobType.health_check:
            scan = await safety_monitor_agent.run_health_check(db)
        else:
            scan = await safety_monitor_agent.scan_recent_outputs(db, hours=24)
        result["output"] = scan

        # Persist result to job
        job.last_run = datetime.utcnow()
        job.last_run_status = "success"
        job.last_run_output = str(scan)[:2000]
        db.commit()

    return result
