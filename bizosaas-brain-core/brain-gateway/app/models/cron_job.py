"""
CronJob model — scheduled platform maintenance jobs.
Covers cleanup, security scanning, health checks, optimization, and compliance runs.
"""
import enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, JSON
from app.models.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class CronJobStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    running = "running"
    failed = "failed"


class CronJobType(str, enum.Enum):
    cleanup = "cleanup"
    security_scan = "security_scan"
    health_check = "health_check"
    optimization = "optimization"
    compliance_check = "compliance_check"
    custom = "custom"


class CronJob(Base):
    __tablename__ = "cron_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    job_type = Column(Enum(CronJobType), nullable=False, default=CronJobType.custom)
    schedule = Column(String(60), nullable=False)   # cron expression e.g. "0 2 * * *"
    status = Column(Enum(CronJobStatus), nullable=False, default=CronJobStatus.active)
    is_system = Column(Boolean, default=False)       # system jobs cannot be deleted
    last_run = Column(DateTime, nullable=True)
    last_run_status = Column(String(20), nullable=True)  # "success" | "failed"
    last_run_output = Column(Text, nullable=True)
    next_run = Column(DateTime, nullable=True)
    config = Column(JSON, nullable=True)             # job-specific config params
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
