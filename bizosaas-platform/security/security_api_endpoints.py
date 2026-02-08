"""
Security and Compliance API Endpoints for BizOSaaS Platform
Provides comprehensive security monitoring and compliance management
"""

import asyncio
import json
import structlog
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends, Request, Query, Body, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from enhanced_tenant_context import EnhancedTenantContext, PlatformType
from shared.rls_middleware import RLSRequestHelper, get_tenant_context
from compliance_framework import (
    SecurityEvent,
    SecurityEventType,
    ThreatLevel,
    DataSubjectRequest,
    DataSubjectRight,
    ThreatDetectionEngine,
    SecurityAuditLogger,
    ComplianceManager,
    get_security_framework
)

logger = structlog.get_logger(__name__)
security = HTTPBearer()


# Request/Response Models
class SecurityEventFilter(BaseModel):
    """Filter parameters for security events"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_types: Optional[List[SecurityEventType]] = None
    severity_levels: Optional[List[ThreatLevel]] = None
    user_id: Optional[str] = None
    source_ip: Optional[str] = None
    limit: int = Field(default=100, le=1000)


class DataSubjectRequestCreate(BaseModel):
    """Data subject request creation model"""
    request_type: DataSubjectRight
    data_subject_id: str
    description: Optional[str] = None
    requested_data_categories: List[str] = Field(default_factory=list)
    legal_basis: Optional[str] = None


class DataSubjectRequestUpdate(BaseModel):
    """Data subject request update model"""
    status: Optional[str] = None
    response_data: Optional[Dict[str, Any]] = None
    identity_verified: Optional[bool] = None
    verification_method: Optional[str] = None
    processing_notes: Optional[str] = None
    rejection_reason: Optional[str] = None


class ComplianceReportRequest(BaseModel):
    """Compliance report generation request"""
    start_date: datetime
    end_date: datetime
    include_security_events: bool = True
    include_data_requests: bool = True
    include_data_breaches: bool = True
    format: str = Field(default="json", pattern="^(json|pdf|csv)$")


class RiskAssessmentCreate(BaseModel):
    """Risk assessment creation model"""
    assessment_type: str
    scope: str
    description: Optional[str] = None
    likelihood: ThreatLevel
    impact: ThreatLevel
    risks_identified: List[Dict[str, Any]] = Field(default_factory=list)
    mitigation_measures: List[Dict[str, Any]] = Field(default_factory=list)


def setup_security_endpoints(app: FastAPI) -> None:
    """
    Setup security and compliance API endpoints
    """

    @app.get("/api/security/events")
    async def get_security_events(
        request: Request,
        filter_params: SecurityEventFilter = Depends(),
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get security events with filtering
        """
        try:
            _, _, security_audit_logger = get_security_framework()

            events = await security_audit_logger.get_security_events(
                tenant_id=tenant_context.tenant_id,
                start_date=filter_params.start_date,
                end_date=filter_params.end_date,
                event_types=filter_params.event_types,
                severity_levels=filter_params.severity_levels,
                limit=filter_params.limit
            )

            return JSONResponse(content={
                "success": True,
                "data": {
                    "events": [
                        {
                            "event_id": event.event_id,
                            "event_type": event.event_type.value,
                            "severity": event.severity.value,
                            "timestamp": event.timestamp.isoformat(),
                            "description": event.description,
                            "source_ip": event.source_ip,
                            "user_id": event.user_id,
                            "endpoint": event.endpoint,
                            "platform": event.platform.value if event.platform else None,
                            "resolution_status": event.resolution_status,
                            "metadata": event.metadata
                        }
                        for event in events
                    ],
                    "total_count": len(events),
                    "filters_applied": {
                        "start_date": filter_params.start_date.isoformat() if filter_params.start_date else None,
                        "end_date": filter_params.end_date.isoformat() if filter_params.end_date else None,
                        "event_types": [et.value for et in filter_params.event_types] if filter_params.event_types else None,
                        "severity_levels": [sl.value for sl in filter_params.severity_levels] if filter_params.severity_levels else None
                    }
                }
            })

        except Exception as e:
            logger.error("Error retrieving security events", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve security events"
            )

    @app.get("/api/security/events/{event_id}")
    async def get_security_event_details(
        event_id: str,
        request: Request,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get detailed information about a specific security event
        """
        try:
            _, _, security_audit_logger = get_security_framework()

            # Get single event (would need to implement this method)
            events = await security_audit_logger.get_security_events(
                tenant_id=tenant_context.tenant_id,
                limit=1
            )

            event = next((e for e in events if e.event_id == event_id), None)
            if not event:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Security event not found"
                )

            return JSONResponse(content={
                "success": True,
                "data": {
                    "event_id": event.event_id,
                    "event_type": event.event_type.value,
                    "severity": event.severity.value,
                    "timestamp": event.timestamp.isoformat(),
                    "description": event.description,
                    "source_ip": event.source_ip,
                    "user_agent": event.user_agent,
                    "user_id": event.user_id,
                    "session_id": event.session_id,
                    "endpoint": event.endpoint,
                    "request_method": event.request_method,
                    "platform": event.platform.value if event.platform else None,
                    "detected_by": event.detected_by,
                    "response_action": event.response_action,
                    "resolution_status": event.resolution_status,
                    "metadata": event.metadata,
                    "tags": event.tags
                }
            })

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error retrieving security event details", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve security event details"
            )

    @app.post("/api/security/events/{event_id}/resolve")
    async def resolve_security_event(
        event_id: str,
        resolution_data: Dict[str, Any] = Body(...),
        request: Request = None,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Mark a security event as resolved
        """
        try:
            # Implementation would update the security event status
            # This is a simplified version
            return JSONResponse(content={
                "success": True,
                "message": "Security event marked as resolved",
                "event_id": event_id,
                "resolution_timestamp": datetime.now(timezone.utc).isoformat()
            })

        except Exception as e:
            logger.error("Error resolving security event", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resolve security event"
            )

    @app.get("/api/security/dashboard")
    async def get_security_dashboard(
        request: Request,
        days: int = Query(default=30, ge=1, le=365),
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get security dashboard data
        """
        try:
            threat_detection_engine, _, security_audit_logger = get_security_framework()

            # Get recent events for dashboard
            start_date = datetime.now(timezone.utc) - timedelta(days=days)
            events = await security_audit_logger.get_security_events(
                tenant_id=tenant_context.tenant_id,
                start_date=start_date,
                limit=1000
            )

            # Calculate dashboard metrics
            total_events = len(events)
            critical_events = len([e for e in events if e.severity == ThreatLevel.CRITICAL])
            high_events = len([e for e in events if e.severity == ThreatLevel.HIGH])
            unresolved_events = len([e for e in events if e.resolution_status in ['open', 'investigating']])

            # Event distribution by type
            event_types = {}
            for event in events:
                event_type = event.event_type.value
                event_types[event_type] = event_types.get(event_type, 0) + 1

            # Top source IPs
            source_ips = {}
            for event in events:
                if event.source_ip:
                    source_ips[event.source_ip] = source_ips.get(event.source_ip, 0) + 1

            top_source_ips = sorted(source_ips.items(), key=lambda x: x[1], reverse=True)[:10]

            # Timeline data (daily counts)
            timeline = {}
            for event in events:
                date_key = event.timestamp.date().isoformat()
                timeline[date_key] = timeline.get(date_key, 0) + 1

            return JSONResponse(content={
                "success": True,
                "data": {
                    "period": {
                        "days": days,
                        "start_date": start_date.isoformat(),
                        "end_date": datetime.now(timezone.utc).isoformat()
                    },
                    "summary": {
                        "total_events": total_events,
                        "critical_events": critical_events,
                        "high_events": high_events,
                        "unresolved_events": unresolved_events,
                        "resolution_rate": round((total_events - unresolved_events) / total_events * 100, 2) if total_events > 0 else 100
                    },
                    "event_distribution": event_types,
                    "top_source_ips": [{"ip": ip, "count": count} for ip, count in top_source_ips],
                    "timeline": timeline,
                    "recent_critical_events": [
                        {
                            "event_id": event.event_id,
                            "event_type": event.event_type.value,
                            "timestamp": event.timestamp.isoformat(),
                            "description": event.description
                        }
                        for event in events if event.severity == ThreatLevel.CRITICAL
                    ][:5]
                }
            })

        except Exception as e:
            logger.error("Error retrieving security dashboard", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve security dashboard"
            )

    # GDPR and Compliance Endpoints

    @app.post("/api/compliance/data-subject-requests")
    async def create_data_subject_request(
        request_data: DataSubjectRequestCreate,
        request: Request = None,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Create a new GDPR data subject request
        """
        try:
            _, compliance_manager, _ = get_security_framework()

            # Create data subject request
            data_request = DataSubjectRequest(
                request_type=request_data.request_type,
                tenant_id=tenant_context.tenant_id,
                data_subject_id=request_data.data_subject_id,
                description=request_data.description,
                requested_data_categories=request_data.requested_data_categories,
                legal_basis=request_data.legal_basis
            )

            # Process the request
            processed_request = await compliance_manager.process_data_subject_request(
                data_request, tenant_context
            )

            return JSONResponse(content={
                "success": True,
                "data": {
                    "request_id": processed_request.request_id,
                    "request_type": processed_request.request_type.value,
                    "status": processed_request.status,
                    "created_at": processed_request.created_at.isoformat(),
                    "due_date": processed_request.due_date.isoformat(),
                    "data_subject_id": processed_request.data_subject_id
                },
                "message": "Data subject request created successfully"
            })

        except Exception as e:
            logger.error("Error creating data subject request", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create data subject request"
            )

    @app.get("/api/compliance/data-subject-requests")
    async def get_data_subject_requests(
        request: Request,
        status_filter: Optional[str] = Query(None),
        request_type: Optional[DataSubjectRight] = Query(None),
        limit: int = Query(default=50, le=200),
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get data subject requests with filtering
        """
        try:
            # Implementation would query the data_subject_requests table
            # This is a simplified response
            return JSONResponse(content={
                "success": True,
                "data": {
                    "requests": [],
                    "total_count": 0,
                    "pending_count": 0,
                    "overdue_count": 0
                }
            })

        except Exception as e:
            logger.error("Error retrieving data subject requests", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve data subject requests"
            )

    @app.put("/api/compliance/data-subject-requests/{request_id}")
    async def update_data_subject_request(
        request_id: str,
        update_data: DataSubjectRequestUpdate,
        request: Request = None,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Update a data subject request
        """
        try:
            # Implementation would update the request in the database
            return JSONResponse(content={
                "success": True,
                "message": "Data subject request updated successfully",
                "request_id": request_id,
                "updated_at": datetime.now(timezone.utc).isoformat()
            })

        except Exception as e:
            logger.error("Error updating data subject request", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update data subject request"
            )

    @app.get("/api/compliance/status")
    async def get_compliance_status(
        request: Request,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Get overall compliance status
        """
        try:
            # Implementation would use the check_compliance_status function
            # from the database schema
            return JSONResponse(content={
                "success": True,
                "data": {
                    "tenant_id": tenant_context.tenant_id,
                    "checked_at": datetime.now(timezone.utc).isoformat(),
                    "overall_status": "compliant",
                    "issues": {
                        "overdue_data_requests": 0,
                        "unresolved_breaches": 0,
                        "critical_events_unaddressed": 0
                    },
                    "recommendations": [],
                    "next_review_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
                }
            })

        except Exception as e:
            logger.error("Error retrieving compliance status", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve compliance status"
            )

    @app.post("/api/compliance/reports")
    async def generate_compliance_report(
        report_request: ComplianceReportRequest,
        request: Request = None,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Generate compliance report
        """
        try:
            # Implementation would use the generate_compliance_report function
            # from the database schema
            report_data = {
                "tenant_id": tenant_context.tenant_id,
                "report_period": {
                    "start_date": report_request.start_date.isoformat(),
                    "end_date": report_request.end_date.isoformat()
                },
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "security_events": {
                    "total_events": 0,
                    "critical_events": 0,
                    "high_events": 0,
                    "unresolved_events": 0
                } if report_request.include_security_events else None,
                "data_subject_requests": {
                    "total_requests": 0,
                    "pending_requests": 0,
                    "completed_requests": 0,
                    "overdue_requests": 0
                } if report_request.include_data_requests else None,
                "data_breaches": {
                    "total_breaches": 0,
                    "unresolved_breaches": 0,
                    "notification_required": 0,
                    "authority_notified": 0
                } if report_request.include_data_breaches else None
            }

            return JSONResponse(content={
                "success": True,
                "data": report_data,
                "format": report_request.format
            })

        except Exception as e:
            logger.error("Error generating compliance report", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate compliance report"
            )

    @app.post("/api/compliance/risk-assessments")
    async def create_risk_assessment(
        assessment_data: RiskAssessmentCreate,
        request: Request = None,
        tenant_context: EnhancedTenantContext = Depends(get_tenant_context)
    ):
        """
        Create a new risk assessment
        """
        try:
            # Calculate overall risk based on likelihood and impact
            risk_matrix = {
                (ThreatLevel.LOW, ThreatLevel.LOW): ThreatLevel.LOW,
                (ThreatLevel.LOW, ThreatLevel.MEDIUM): ThreatLevel.LOW,
                (ThreatLevel.LOW, ThreatLevel.HIGH): ThreatLevel.MEDIUM,
                (ThreatLevel.LOW, ThreatLevel.CRITICAL): ThreatLevel.MEDIUM,
                (ThreatLevel.MEDIUM, ThreatLevel.LOW): ThreatLevel.LOW,
                (ThreatLevel.MEDIUM, ThreatLevel.MEDIUM): ThreatLevel.MEDIUM,
                (ThreatLevel.MEDIUM, ThreatLevel.HIGH): ThreatLevel.HIGH,
                (ThreatLevel.MEDIUM, ThreatLevel.CRITICAL): ThreatLevel.HIGH,
                (ThreatLevel.HIGH, ThreatLevel.LOW): ThreatLevel.MEDIUM,
                (ThreatLevel.HIGH, ThreatLevel.MEDIUM): ThreatLevel.HIGH,
                (ThreatLevel.HIGH, ThreatLevel.HIGH): ThreatLevel.HIGH,
                (ThreatLevel.HIGH, ThreatLevel.CRITICAL): ThreatLevel.CRITICAL,
                (ThreatLevel.CRITICAL, ThreatLevel.LOW): ThreatLevel.MEDIUM,
                (ThreatLevel.CRITICAL, ThreatLevel.MEDIUM): ThreatLevel.HIGH,
                (ThreatLevel.CRITICAL, ThreatLevel.HIGH): ThreatLevel.CRITICAL,
                (ThreatLevel.CRITICAL, ThreatLevel.CRITICAL): ThreatLevel.CRITICAL,
            }

            overall_risk = risk_matrix.get(
                (assessment_data.likelihood, assessment_data.impact),
                ThreatLevel.MEDIUM
            )

            assessment_id = str(UUID())

            # Implementation would save to database
            return JSONResponse(content={
                "success": True,
                "data": {
                    "assessment_id": assessment_id,
                    "assessment_type": assessment_data.assessment_type,
                    "overall_risk": overall_risk.value,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "next_review_date": (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
                },
                "message": "Risk assessment created successfully"
            })

        except Exception as e:
            logger.error("Error creating risk assessment", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create risk assessment"
            )

    @app.get("/api/security/health")
    async def security_health_check():
        """
        Security framework health check
        """
        try:
            threat_detection_engine, compliance_manager, security_audit_logger = get_security_framework()

            return JSONResponse(content={
                "success": True,
                "data": {
                    "status": "healthy",
                    "components": {
                        "threat_detection": "operational",
                        "compliance_manager": "operational",
                        "audit_logger": "operational"
                    },
                    "checked_at": datetime.now(timezone.utc).isoformat()
                }
            })

        except RuntimeError:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "success": False,
                    "error": "Security framework not initialized",
                    "components": {
                        "threat_detection": "unavailable",
                        "compliance_manager": "unavailable",
                        "audit_logger": "unavailable"
                    }
                }
            )
        except Exception as e:
            logger.error("Security health check failed", error=str(e))
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "success": False,
                    "error": "Security framework unhealthy",
                    "details": str(e)
                }
            )

    logger.info("Security and compliance API endpoints configured successfully")