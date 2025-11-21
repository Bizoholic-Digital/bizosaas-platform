#!/usr/bin/env python3
"""
GDPR Compliance Service - Immediate Implementation
Critical compliance fixes for BizOSaaS platform
"""

from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid
import asyncio
import httpx
import json
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@shared-postgres:5433/bizosaas_compliance")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(
    title="GDPR Compliance Service",
    description="Critical GDPR compliance implementation for BizOSaaS platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

# ========================================================================================
# ENUMS AND MODELS
# ========================================================================================

class ConsentType(str, Enum):
    ESSENTIAL = "essential"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    PERSONALIZATION = "personalization"
    AI_TRAINING = "ai_training"
    THIRD_PARTY = "third_party"

class LegalBasis(str, Enum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"

class DataCategory(str, Enum):
    IDENTITY = "identity"
    CONTACT = "contact"
    FINANCIAL = "financial"
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    HEALTH = "health"
    BIOMETRIC = "biometric"

class RequestStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

# ========================================================================================
# DATABASE MODELS
# ========================================================================================

class UserConsent(Base):
    __tablename__ = "user_consents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)
    consent_type = Column(String(50), nullable=False)
    consent_given = Column(Boolean, nullable=False)
    legal_basis = Column(String(50), nullable=False)
    purpose_description = Column(Text)
    
    # Audit trail
    consent_date = Column(DateTime, default=datetime.utcnow)
    withdrawal_date = Column(DateTime)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    source_platform = Column(String(50))
    
    # Additional metadata
    processing_context = Column(JSONB)
    retention_period_days = Column(Integer, default=730)  # 2 years default
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataSubjectRequest(Base):
    __tablename__ = "data_subject_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, index=True)
    request_type = Column(String(50), nullable=False)  # export, delete, rectify, restrict, object
    status = Column(String(50), default=RequestStatus.PENDING)
    
    # Request details
    request_reason = Column(Text)
    data_categories = Column(JSONB)  # Categories of data requested
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    
    # Processing details
    request_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)  # 30 days from request
    completion_date = Column(DateTime)
    
    # Verification
    verification_method = Column(String(100))
    verification_completed = Column(Boolean, default=False)
    verification_token = Column(String(255))
    
    # Results
    response_data = Column(JSONB)
    processing_log = Column(JSONB)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataProcessingActivity(Base):
    __tablename__ = "data_processing_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(100), nullable=False)
    processing_purpose = Column(Text, nullable=False)
    legal_basis = Column(String(50), nullable=False)
    
    # Data details
    data_categories = Column(JSONB)
    data_subjects = Column(JSONB)  # Categories of individuals
    recipients = Column(JSONB)  # Who receives the data
    
    # Retention and security
    retention_period_days = Column(Integer)
    security_measures = Column(JSONB)
    international_transfers = Column(JSONB)
    
    # Impact assessment
    dpia_required = Column(Boolean, default=False)
    dpia_completed = Column(Boolean, default=False)
    dpia_date = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DataBreach(Base):
    __tablename__ = "data_breaches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    breach_reference = Column(String(100), unique=True, nullable=False)
    
    # Breach details
    nature_of_breach = Column(Text, nullable=False)
    breach_type = Column(String(50))  # unauthorized_access, data_loss, etc.
    severity_level = Column(String(20))  # low, medium, high, critical
    
    # Timeline
    discovery_date = Column(DateTime, nullable=False)
    occurrence_date = Column(DateTime)
    containment_date = Column(DateTime)
    
    # Impact assessment
    affected_data_categories = Column(JSONB)
    approximate_affected_individuals = Column(Integer)
    likely_consequences = Column(Text)
    
    # Notifications
    authority_notification_required = Column(Boolean, default=False)
    authority_notification_sent = Column(Boolean, default=False)
    authority_notification_date = Column(DateTime)
    
    individual_notification_required = Column(Boolean, default=False)
    individual_notification_sent = Column(Boolean, default=False)
    individual_notification_date = Column(DateTime)
    
    # Response measures
    containment_measures = Column(JSONB)
    remedial_actions = Column(JSONB)
    preventive_measures = Column(JSONB)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ComplianceAuditLog(Base):
    __tablename__ = "compliance_audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(100), nullable=False)
    audit_type = Column(String(50), nullable=False)  # consent, access, deletion, etc.
    
    # Event details
    event_description = Column(Text)
    user_id = Column(String(255), index=True)
    resource_affected = Column(String(255))
    action_taken = Column(String(100))
    
    # Result
    compliance_status = Column(String(50))  # compliant, violation, warning
    risk_level = Column(String(20))  # low, medium, high, critical
    
    # Context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_id = Column(String(255))
    session_id = Column(String(255))
    
    # Additional data
    audit_data = Column(JSONB)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

# ========================================================================================
# PYDANTIC MODELS
# ========================================================================================

class ConsentRequest(BaseModel):
    user_id: str
    consents: List[Dict[str, Any]]
    source_platform: str = "web"

class ConsentWithdrawalRequest(BaseModel):
    user_id: str
    consent_type: ConsentType
    reason: Optional[str] = None

class DataExportRequest(BaseModel):
    user_id: str
    export_format: str = "json"
    data_categories: Optional[List[DataCategory]] = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    include_deleted: bool = False

class DataDeletionRequest(BaseModel):
    user_id: str
    reason: str
    delete_type: str = "full"  # full, partial, anonymize
    data_categories: Optional[List[DataCategory]] = None

class BreachReport(BaseModel):
    nature_of_breach: str
    breach_type: str
    severity_level: str
    discovery_date: datetime
    occurrence_date: Optional[datetime] = None
    affected_data_categories: List[str]
    approximate_affected_individuals: int
    likely_consequences: str

# ========================================================================================
# CORE GDPR IMPLEMENTATION
# ========================================================================================

class GDPRComplianceService:
    """Core GDPR compliance service"""
    
    def __init__(self):
        self.service_registry = self._get_service_registry()
        
    def _get_service_registry(self) -> Dict[str, Dict[str, str]]:
        """Registry of all services with their data endpoints"""
        return {
            "auth-service": {
                "url": "http://auth-service:3001",
                "export_endpoint": "/api/users/{user_id}/data",
                "delete_endpoint": "/api/users/{user_id}",
                "data_categories": ["identity", "authentication", "security"]
            },
            "user-management": {
                "url": "http://user-management:8006",
                "export_endpoint": "/api/users/{user_id}/profile",
                "delete_endpoint": "/api/users/{user_id}/profile",
                "data_categories": ["identity", "contact", "preferences"]
            },
            "django-crm": {
                "url": "http://django-crm:8007",
                "export_endpoint": "/api/customers/{user_id}/data",
                "delete_endpoint": "/api/customers/{user_id}",
                "data_categories": ["contact", "behavioral", "commercial"]
            },
            "ai-agents": {
                "url": "http://ai-agents:8001",
                "export_endpoint": "/api/users/{user_id}/interactions",
                "delete_endpoint": "/api/users/{user_id}/data",
                "data_categories": ["behavioral", "ai_training", "preferences"]
            },
            "analytics-service": {
                "url": "http://analytics-service:8003",
                "export_endpoint": "/api/users/{user_id}/analytics",
                "delete_endpoint": "/api/users/{user_id}/analytics",
                "data_categories": ["behavioral", "technical", "usage"]
            },
            "telegram-integration": {
                "url": "http://telegram-integration:4007",
                "export_endpoint": "/api/users/{user_id}/messages",
                "delete_endpoint": "/api/users/{user_id}/messages",
                "data_categories": ["communication", "behavioral"]
            },
            "payment-service": {
                "url": "http://payment-service:8004",
                "export_endpoint": "/api/users/{user_id}/payments",
                "delete_endpoint": "/api/users/{user_id}/payments",
                "data_categories": ["financial", "transaction"]
            }
        }
    
    async def process_data_export_request(
        self, 
        request: DataExportRequest, 
        db: Session
    ) -> str:
        """Process GDPR Article 20 - Right to data portability"""
        
        # Create request record
        data_request = DataSubjectRequest(
            user_id=request.user_id,
            request_type="export",
            request_reason="Data portability request",
            data_categories=request.data_categories or [],
            date_range_start=request.date_range_start,
            date_range_end=request.date_range_end,
            due_date=datetime.utcnow() + timedelta(days=30),
            verification_token=str(uuid.uuid4())
        )
        
        db.add(data_request)
        db.commit()
        db.refresh(data_request)
        
        # Start background aggregation
        asyncio.create_task(
            self._aggregate_user_data_background(str(data_request.id), request, db)
        )
        
        return str(data_request.id)
    
    async def _aggregate_user_data_background(
        self, 
        request_id: str, 
        export_request: DataExportRequest,
        db: Session
    ):
        """Aggregate user data from all services"""
        
        # Update status to processing
        data_request = db.query(DataSubjectRequest).filter(
            DataSubjectRequest.id == request_id
        ).first()
        
        if not data_request:
            return
            
        data_request.status = RequestStatus.PROCESSING
        db.commit()
        
        aggregated_data = {
            "export_metadata": {
                "user_id": export_request.user_id,
                "export_date": datetime.utcnow().isoformat(),
                "format": export_request.export_format,
                "request_id": request_id,
                "legal_basis": "GDPR Article 20 - Right to data portability"
            },
            "services_data": {},
            "processing_log": []
        }
        
        # Collect data from each service
        async with httpx.AsyncClient() as client:
            for service_name, service_info in self.service_registry.items():
                try:
                    url = service_info["url"] + service_info["export_endpoint"].format(
                        user_id=export_request.user_id
                    )
                    
                    response = await client.get(url, timeout=60.0)
                    
                    if response.status_code == 200:
                        service_data = response.json()
                        aggregated_data["services_data"][service_name] = {
                            "data": service_data,
                            "categories": service_info["data_categories"],
                            "collection_date": datetime.utcnow().isoformat(),
                            "status": "success"
                        }
                    else:
                        aggregated_data["services_data"][service_name] = {
                            "error": f"HTTP {response.status_code}",
                            "status": "failed"
                        }
                        
                    aggregated_data["processing_log"].append({
                        "service": service_name,
                        "status": "success" if response.status_code == 200 else "failed",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    
                except Exception as e:
                    aggregated_data["services_data"][service_name] = {
                        "error": str(e),
                        "status": "error"
                    }
                    aggregated_data["processing_log"].append({
                        "service": service_name,
                        "status": "error",
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })
        
        # Update request with results
        data_request.status = RequestStatus.COMPLETED
        data_request.completion_date = datetime.utcnow()
        data_request.response_data = aggregated_data
        db.commit()
        
        # Send notification email
        await self._send_export_notification(export_request.user_id, request_id)
    
    async def process_data_deletion_request(
        self, 
        request: DataDeletionRequest, 
        db: Session
    ) -> str:
        """Process GDPR Article 17 - Right to erasure"""
        
        # Create deletion request record
        data_request = DataSubjectRequest(
            user_id=request.user_id,
            request_type="delete",
            request_reason=request.reason,
            data_categories=request.data_categories or [],
            due_date=datetime.utcnow() + timedelta(days=30),
            verification_token=str(uuid.uuid4())
        )
        
        db.add(data_request)
        db.commit()
        db.refresh(data_request)
        
        # Start background deletion
        asyncio.create_task(
            self._delete_user_data_background(str(data_request.id), request, db)
        )
        
        return str(data_request.id)
    
    async def _delete_user_data_background(
        self, 
        request_id: str, 
        deletion_request: DataDeletionRequest,
        db: Session
    ):
        """Delete user data from all services"""
        
        # Update status to processing
        data_request = db.query(DataSubjectRequest).filter(
            DataSubjectRequest.id == request_id
        ).first()
        
        if not data_request:
            return
            
        data_request.status = RequestStatus.PROCESSING
        db.commit()
        
        deletion_results = {
            "deletion_metadata": {
                "user_id": deletion_request.user_id,
                "deletion_date": datetime.utcnow().isoformat(),
                "reason": deletion_request.reason,
                "request_id": request_id,
                "legal_basis": "GDPR Article 17 - Right to erasure"
            },
            "services_deletion": {},
            "deletion_log": []
        }
        
        # Delete data from each service
        async with httpx.AsyncClient() as client:
            for service_name, service_info in self.service_registry.items():
                try:
                    url = service_info["url"] + service_info["delete_endpoint"].format(
                        user_id=deletion_request.user_id
                    )
                    
                    payload = {
                        "reason": deletion_request.reason,
                        "request_id": request_id,
                        "delete_type": deletion_request.delete_type
                    }
                    
                    response = await client.delete(url, json=payload, timeout=60.0)
                    
                    deletion_results["services_deletion"][service_name] = {
                        "status": "success" if response.status_code in [200, 204] else "failed",
                        "response_code": response.status_code,
                        "data_categories": service_info["data_categories"],
                        "deletion_date": datetime.utcnow().isoformat()
                    }
                        
                    deletion_results["deletion_log"].append({
                        "service": service_name,
                        "status": "success" if response.status_code in [200, 204] else "failed",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    
                except Exception as e:
                    deletion_results["services_deletion"][service_name] = {
                        "status": "error",
                        "error": str(e),
                        "deletion_date": datetime.utcnow().isoformat()
                    }
                    deletion_results["deletion_log"].append({
                        "service": service_name,
                        "status": "error",
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    })
        
        # Determine overall success
        successful_deletions = sum(
            1 for result in deletion_results["services_deletion"].values()
            if result["status"] == "success"
        )
        total_services = len(self.service_registry)
        
        if successful_deletions == total_services:
            final_status = RequestStatus.COMPLETED
        elif successful_deletions > 0:
            final_status = RequestStatus.PARTIAL
        else:
            final_status = RequestStatus.FAILED
        
        # Update request with results
        data_request.status = final_status
        data_request.completion_date = datetime.utcnow()
        data_request.response_data = deletion_results
        db.commit()
        
        # Log audit trail
        await self._log_deletion_audit(deletion_request.user_id, deletion_results, db)
        
        # Send confirmation notification
        await self._send_deletion_notification(deletion_request.user_id, request_id)
    
    async def _send_export_notification(self, user_id: str, request_id: str):
        """Send email notification for completed data export"""
        # Implementation for email notification
        pass
    
    async def _send_deletion_notification(self, user_id: str, request_id: str):
        """Send email notification for completed data deletion"""
        # Implementation for email notification
        pass
    
    async def _log_deletion_audit(self, user_id: str, deletion_results: Dict, db: Session):
        """Log deletion audit trail"""
        audit_log = ComplianceAuditLog(
            service_name="gdpr-compliance-service",
            audit_type="data_deletion",
            event_description=f"User data deletion completed for user {user_id}",
            user_id=user_id,
            action_taken="data_deletion",
            compliance_status="compliant",
            audit_data=deletion_results
        )
        db.add(audit_log)
        db.commit()

# ========================================================================================
# API ENDPOINTS
# ========================================================================================

gdpr_service = GDPRComplianceService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/gdpr/consent/record")
async def record_consent(
    request: ConsentRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Record user consent preferences"""
    
    consent_records = []
    
    for consent_data in request.consents:
        consent_record = UserConsent(
            user_id=request.user_id,
            consent_type=consent_data["type"],
            consent_given=consent_data["given"],
            legal_basis=consent_data.get("legal_basis", "consent"),
            purpose_description=consent_data.get("purpose", ""),
            ip_address=http_request.client.host,
            user_agent=http_request.headers.get("user-agent", ""),
            source_platform=request.source_platform,
            processing_context=consent_data.get("context", {})
        )
        
        db.add(consent_record)
        consent_records.append(consent_record)
    
    db.commit()
    
    # Log compliance audit
    audit_log = ComplianceAuditLog(
        service_name="gdpr-compliance-service",
        audit_type="consent_recording",
        event_description=f"Consent recorded for user {request.user_id}",
        user_id=request.user_id,
        action_taken="consent_update",
        compliance_status="compliant",
        ip_address=http_request.client.host,
        audit_data={"consents_recorded": len(consent_records)}
    )
    db.add(audit_log)
    db.commit()
    
    return {
        "status": "success",
        "message": f"Recorded {len(consent_records)} consent preferences",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/gdpr/consent/withdraw")
async def withdraw_consent(
    request: ConsentWithdrawalRequest,
    db: Session = Depends(get_db)
):
    """Withdraw specific consent"""
    
    # Find active consent
    consent_record = db.query(UserConsent).filter(
        UserConsent.user_id == request.user_id,
        UserConsent.consent_type == request.consent_type,
        UserConsent.consent_given == True,
        UserConsent.withdrawal_date.is_(None)
    ).first()
    
    if not consent_record:
        raise HTTPException(status_code=404, detail="No active consent found")
    
    # Withdraw consent
    consent_record.withdrawal_date = datetime.utcnow()
    consent_record.consent_given = False
    
    # Create withdrawal record
    withdrawal_record = UserConsent(
        user_id=request.user_id,
        consent_type=request.consent_type,
        consent_given=False,
        legal_basis="withdrawal",
        purpose_description=f"Consent withdrawn: {request.reason or 'User request'}"
    )
    
    db.add(withdrawal_record)
    db.commit()
    
    return {
        "status": "success",
        "message": f"Consent for {request.consent_type} withdrawn",
        "withdrawal_date": consent_record.withdrawal_date.isoformat()
    }

@app.get("/api/gdpr/consent/status/{user_id}")
async def get_consent_status(user_id: str, db: Session = Depends(get_db)):
    """Get current consent status for user"""
    
    consent_status = {}
    
    for consent_type in ConsentType:
        latest_consent = db.query(UserConsent).filter(
            UserConsent.user_id == user_id,
            UserConsent.consent_type == consent_type
        ).order_by(UserConsent.consent_date.desc()).first()
        
        if latest_consent:
            consent_status[consent_type.value] = {
                "given": latest_consent.consent_given and latest_consent.withdrawal_date is None,
                "date": latest_consent.consent_date.isoformat(),
                "withdrawal_date": latest_consent.withdrawal_date.isoformat() if latest_consent.withdrawal_date else None,
                "purpose": latest_consent.purpose_description,
                "legal_basis": latest_consent.legal_basis
            }
        else:
            consent_status[consent_type.value] = {
                "given": False,
                "date": None,
                "purpose": f"Default {consent_type.value} processing",
                "legal_basis": "not_specified"
            }
    
    return consent_status

@app.post("/api/gdpr/data/export")
async def request_data_export(
    request: DataExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """GDPR Article 20 - Right to data portability"""
    
    request_id = await gdpr_service.process_data_export_request(request, db)
    
    return {
        "status": "processing",
        "request_id": request_id,
        "message": "Data export request initiated",
        "estimated_completion": "within 30 days",
        "legal_basis": "GDPR Article 20 - Right to data portability"
    }

@app.delete("/api/gdpr/data/delete")
async def request_data_deletion(
    request: DataDeletionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """GDPR Article 17 - Right to erasure"""
    
    request_id = await gdpr_service.process_data_deletion_request(request, db)
    
    return {
        "status": "processing",
        "request_id": request_id,
        "message": "Data deletion request initiated",
        "estimated_completion": "within 30 days",
        "legal_basis": "GDPR Article 17 - Right to erasure"
    }

@app.get("/api/gdpr/requests/{request_id}/status")
async def get_request_status(request_id: str, db: Session = Depends(get_db)):
    """Get status of GDPR data request"""
    
    data_request = db.query(DataSubjectRequest).filter(
        DataSubjectRequest.id == request_id
    ).first()
    
    if not data_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {
        "request_id": request_id,
        "type": data_request.request_type,
        "status": data_request.status,
        "request_date": data_request.request_date.isoformat(),
        "due_date": data_request.due_date.isoformat(),
        "completion_date": data_request.completion_date.isoformat() if data_request.completion_date else None,
        "download_url": f"/api/gdpr/requests/{request_id}/download" if data_request.status == "completed" and data_request.request_type == "export" else None
    }

@app.post("/api/gdpr/breach/report")
async def report_breach(
    report: BreachReport,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Report data breach for GDPR Article 33 compliance"""
    
    breach_record = DataBreach(
        breach_reference=f"BR-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
        nature_of_breach=report.nature_of_breach,
        breach_type=report.breach_type,
        severity_level=report.severity_level,
        discovery_date=report.discovery_date,
        occurrence_date=report.occurrence_date,
        affected_data_categories=report.affected_data_categories,
        approximate_affected_individuals=report.approximate_affected_individuals,
        likely_consequences=report.likely_consequences,
        authority_notification_required=report.severity_level in ["high", "critical"],
        individual_notification_required=report.severity_level == "critical"
    )
    
    db.add(breach_record)
    db.commit()
    
    # Schedule notifications if required
    if breach_record.authority_notification_required:
        # Schedule 72-hour notification
        background_tasks.add_task(
            schedule_authority_notification, 
            str(breach_record.id), 
            72
        )
    
    return {
        "breach_id": str(breach_record.id),
        "breach_reference": breach_record.breach_reference,
        "status": "reported",
        "authority_notification_deadline": (datetime.utcnow() + timedelta(hours=72)).isoformat() if breach_record.authority_notification_required else None,
        "next_steps": "Investigation initiated"
    }

@app.get("/api/gdpr/compliance/audit")
async def get_compliance_audit(
    days: int = 30,
    service_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get compliance audit trail"""
    
    query = db.query(ComplianceAuditLog).filter(
        ComplianceAuditLog.timestamp >= datetime.utcnow() - timedelta(days=days)
    )
    
    if service_name:
        query = query.filter(ComplianceAuditLog.service_name == service_name)
    
    audit_logs = query.order_by(ComplianceAuditLog.timestamp.desc()).limit(1000).all()
    
    return {
        "total_logs": len(audit_logs),
        "date_range": f"Last {days} days",
        "service_filter": service_name,
        "logs": [
            {
                "id": str(log.id),
                "service": log.service_name,
                "audit_type": log.audit_type,
                "description": log.event_description,
                "user_id": log.user_id,
                "compliance_status": log.compliance_status,
                "risk_level": log.risk_level,
                "timestamp": log.timestamp.isoformat()
            }
            for log in audit_logs
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GDPR Compliance Service",
        "version": "1.0.0",
        "features": [
            "GDPR Article 13 - Transparency",
            "GDPR Article 17 - Right to erasure",
            "GDPR Article 20 - Data portability",
            "GDPR Article 33 - Breach notification",
            "Consent management",
            "Compliance audit logging"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

async def schedule_authority_notification(breach_id: str, hours: int):
    """Schedule supervisory authority notification"""
    # Wait for deadline minus buffer time
    await asyncio.sleep((hours - 6) * 3600)  # 6-hour buffer
    
    # Implementation for authority notification
    logger.info(f"Authority notification deadline approaching for breach {breach_id}")

def create_tables():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8050, reload=True)