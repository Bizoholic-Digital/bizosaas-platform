"""
GDPR Compliance Integration for Brain Gateway
Proxies requests to the GDPR compliance service
"""

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import httpx
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/gdpr", tags=["GDPR Compliance"])

# GDPR Service Configuration
GDPR_SERVICE_URL = "http://gdpr-compliance-service:8009"

# ========================================================================================
# PYDANTIC MODELS (matching GDPR service)
# ========================================================================================

class ConsentType(str, Enum):
    ESSENTIAL = "essential"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    PERSONALIZATION = "personalization"
    AI_TRAINING = "ai_training"
    THIRD_PARTY = "third_party"

class DataCategory(str, Enum):
    IDENTITY = "identity"
    CONTACT = "contact"
    FINANCIAL = "financial"
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    HEALTH = "health"
    BIOMETRIC = "biometric"

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
# PROXY ENDPOINTS
# ========================================================================================

@router.post("/consent/record")
async def record_consent(
    request: ConsentRequest,
    http_request: Request
):
    """
    Record user consent preferences
    Proxies to GDPR compliance service
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GDPR_SERVICE_URL}/api/gdpr/consent/record",
                json=request.dict(),
                headers={"X-Forwarded-For": http_request.client.host},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"GDPR service error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to record consent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to record consent: {str(e)}")

@router.post("/consent/withdraw")
async def withdraw_consent(request: ConsentWithdrawalRequest):
    """
    Withdraw specific consent
    Proxies to GDPR compliance service
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GDPR_SERVICE_URL}/api/gdpr/consent/withdraw",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to withdraw consent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to withdraw consent: {str(e)}")

@router.get("/consent/status/{user_id}")
async def get_consent_status(user_id: str):
    """
    Get current consent status for user
    Proxies to GDPR compliance service
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GDPR_SERVICE_URL}/api/gdpr/consent/status/{user_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to get consent status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get consent status: {str(e)}")

@router.post("/data/export")
async def request_data_export(
    request: DataExportRequest,
    background_tasks: BackgroundTasks
):
    """
    GDPR Article 20 - Right to data portability
    Request export of all user data
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GDPR_SERVICE_URL}/api/gdpr/data/export",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to request data export: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to request data export: {str(e)}")

@router.delete("/data/delete")
async def request_data_deletion(
    request: DataDeletionRequest,
    background_tasks: BackgroundTasks
):
    """
    GDPR Article 17 - Right to erasure
    Request deletion of all user data
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{GDPR_SERVICE_URL}/api/gdpr/data/delete",
                json=request.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to request data deletion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to request data deletion: {str(e)}")

@router.get("/requests/{request_id}/status")
async def get_request_status(request_id: str):
    """
    Get status of GDPR data request (export or deletion)
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GDPR_SERVICE_URL}/api/gdpr/requests/{request_id}/status",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to get request status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get request status: {str(e)}")

@router.get("/requests/{request_id}/download")
async def download_export_data(request_id: str):
    """
    Download exported user data
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GDPR_SERVICE_URL}/api/gdpr/requests/{request_id}/download",
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to download export data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download export data: {str(e)}")

@router.post("/breach/report")
async def report_breach(
    report: BreachReport,
    background_tasks: BackgroundTasks
):
    """
    Report data breach for GDPR Article 33 compliance
    Internal use only - requires admin authentication
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GDPR_SERVICE_URL}/api/gdpr/breach/report",
                json=report.dict(),
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error(f"Failed to report breach: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to report breach: {str(e)}")

@router.get("/health")
async def gdpr_health_check():
    """
    Check GDPR compliance service health
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GDPR_SERVICE_URL}/health",
                timeout=5.0
            )
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "gdpr_service": "connected",
                "timestamp": datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "gdpr_service": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
