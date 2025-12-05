# GDPR Implementation Guide for BizOSaaS Platform

**Immediate Action Required**: GDPR compliance gap (42.9%) must be addressed before international deployment

## Overview

This guide provides concrete implementation steps for GDPR compliance across the BizOSaaS platform's 58 microservices.

## 1. Privacy Policy and Transparency (Article 13)

### Create Privacy Policy Service

```bash
mkdir -p services/privacy-policy-service
cd services/privacy-policy-service
```

### Privacy Policy API Implementation

```python
# services/privacy-policy-service/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="Privacy Policy Service")
templates = Jinja2Templates(directory="templates")

@app.get("/privacy-policy/{language}")
async def get_privacy_policy(language: str, request: Request):
    """Serve privacy policy in requested language"""
    supported_languages = ["en", "de", "fr", "es", "it"]
    if language not in supported_languages:
        language = "en"
    
    return templates.TemplateResponse(
        f"privacy_policy_{language}.html", 
        {"request": request, "language": language}
    )

@app.get("/api/privacy/data-processing-info")
async def get_data_processing_info():
    """Article 13 - Information about data processing"""
    return {
        "controller": {
            "name": "BizOSaaS Platform",
            "contact": "privacy@bizosaas.com",
            "dpo_contact": "dpo@bizosaas.com"
        },
        "purposes": [
            {
                "purpose": "User Account Management",
                "legal_basis": "Contract",
                "data_categories": ["Identity data", "Contact data"],
                "retention_period": "Duration of account + 3 years"
            },
            {
                "purpose": "AI-Powered Marketing Services",
                "legal_basis": "Legitimate Interest",
                "data_categories": ["Marketing data", "Behavioral data"],
                "retention_period": "2 years from last interaction"
            }
        ],
        "recipients": [
            "Internal marketing team",
            "AI service providers (with DPA)",
            "Cloud infrastructure providers (with DPA)"
        ],
        "rights": [
            "Right of access",
            "Right to rectification", 
            "Right to erasure",
            "Right to data portability",
            "Right to object",
            "Right to restrict processing"
        ]
    }
```

### Privacy Policy Templates

```html
<!-- services/privacy-policy-service/templates/privacy_policy_en.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Privacy Policy - BizOSaaS Platform</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Privacy Policy</h1>
    <p><strong>Last Updated:</strong> September 15, 2025</p>
    
    <h2>1. Controller Information</h2>
    <p>
        <strong>Data Controller:</strong> BizOSaaS Platform<br>
        <strong>Contact:</strong> privacy@bizosaas.com<br>
        <strong>Data Protection Officer:</strong> dpo@bizosaas.com
    </p>
    
    <h2>2. Data We Collect</h2>
    <ul>
        <li><strong>Identity Data:</strong> Name, username, email address</li>
        <li><strong>Contact Data:</strong> Email, phone number, address</li>
        <li><strong>Marketing Data:</strong> Marketing preferences, communication history</li>
        <li><strong>Technical Data:</strong> IP address, browser type, device information</li>
        <li><strong>Usage Data:</strong> How you use our platform and services</li>
    </ul>
    
    <h2>3. How We Use Your Data</h2>
    <table border="1">
        <tr>
            <th>Purpose</th>
            <th>Legal Basis</th>
            <th>Data Categories</th>
            <th>Retention Period</th>
        </tr>
        <tr>
            <td>Account Management</td>
            <td>Contract Performance</td>
            <td>Identity, Contact</td>
            <td>Duration of account + 3 years</td>
        </tr>
        <tr>
            <td>AI Marketing Services</td>
            <td>Legitimate Interest</td>
            <td>Marketing, Usage, Technical</td>
            <td>2 years from last interaction</td>
        </tr>
        <tr>
            <td>Customer Support</td>
            <td>Contract Performance</td>
            <td>Identity, Contact, Usage</td>
            <td>3 years from last support interaction</td>
        </tr>
    </table>
    
    <h2>4. Your Rights Under GDPR</h2>
    <p>You have the following rights regarding your personal data:</p>
    <ul>
        <li><strong>Right of Access:</strong> Request a copy of your personal data</li>
        <li><strong>Right to Rectification:</strong> Correct inaccurate personal data</li>
        <li><strong>Right to Erasure:</strong> Request deletion of your personal data</li>
        <li><strong>Right to Data Portability:</strong> Receive your data in a machine-readable format</li>
        <li><strong>Right to Object:</strong> Object to processing based on legitimate interests</li>
        <li><strong>Right to Restrict Processing:</strong> Limit how we process your data</li>
    </ul>
    
    <p>To exercise your rights, visit <a href="/user/privacy-dashboard">Privacy Dashboard</a> or contact us at privacy@bizosaas.com</p>
    
    <h2>5. Data Sharing and Transfers</h2>
    <p>We may share your data with:</p>
    <ul>
        <li>Service providers with appropriate Data Processing Agreements</li>
        <li>Legal authorities when required by law</li>
        <li>Business partners with your explicit consent</li>
    </ul>
    
    <p>For international transfers outside the EU, we use Standard Contractual Clauses and conduct Transfer Impact Assessments.</p>
    
    <h2>6. Data Security</h2>
    <p>We implement appropriate technical and organizational measures including:</p>
    <ul>
        <li>Encryption of data at rest and in transit</li>
        <li>Multi-factor authentication</li>
        <li>Regular security audits and penetration testing</li>
        <li>Staff training on data protection</li>
    </ul>
    
    <h2>7. Contact Information</h2>
    <p>
        For any privacy-related questions or to exercise your rights:<br>
        <strong>Email:</strong> privacy@bizosaas.com<br>
        <strong>Data Protection Officer:</strong> dpo@bizosaas.com<br>
        <strong>Supervisory Authority:</strong> You can lodge a complaint with your local data protection authority
    </p>
</body>
</html>
```

## 2. User Rights Implementation (Articles 17 & 20)

### Data Rights Service

```python
# services/data-rights-service/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import asyncio
import httpx
from datetime import datetime
import json

app = FastAPI(title="Data Rights Service")

# Database models
class DataRequest(BaseModel):
    id: str
    user_id: str
    request_type: str  # export, delete, rectify
    status: str  # pending, processing, completed, failed
    request_date: datetime
    completion_date: Optional[datetime] = None
    verification_token: str
    response_data: Optional[dict] = None

class UserDataExport(BaseModel):
    user_id: str
    export_format: str = "json"
    include_deleted: bool = False
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None

@app.post("/api/data-rights/export")
async def request_data_export(
    export_request: UserDataExport,
    current_user: dict = Depends(verify_user_token),
    db: Session = Depends(get_db)
):
    """Article 20 - Right to data portability"""
    
    # Verify user identity
    if export_request.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Create data request record
    request_id = str(uuid4())
    data_request = DataRequest(
        id=request_id,
        user_id=export_request.user_id,
        request_type="export",
        status="processing",
        request_date=datetime.utcnow(),
        verification_token=generate_verification_token()
    )
    
    db.add(data_request)
    db.commit()
    
    # Start background data aggregation
    asyncio.create_task(aggregate_user_data(request_id, export_request))
    
    return {
        "request_id": request_id,
        "status": "processing",
        "message": "Data export request initiated. You will receive an email when ready.",
        "estimated_completion": "within 30 days"
    }

async def aggregate_user_data(request_id: str, export_request: UserDataExport):
    """Aggregate user data from all services"""
    
    # Services to query for user data
    services = [
        {"name": "auth-service", "url": "http://auth-service:3001", "endpoint": "/api/users/{user_id}/data"},
        {"name": "django-crm", "url": "http://django-crm:8007", "endpoint": "/api/customers/{user_id}/data"},
        {"name": "ai-agents", "url": "http://ai-agents:8001", "endpoint": "/api/users/{user_id}/interactions"},
        {"name": "analytics-service", "url": "http://analytics-service:8003", "endpoint": "/api/users/{user_id}/analytics"},
        {"name": "campaign-management", "url": "http://campaign-management:8008", "endpoint": "/api/users/{user_id}/campaigns"},
        {"name": "user-management", "url": "http://user-management:8006", "endpoint": "/api/users/{user_id}/profile"},
        {"name": "notification", "url": "http://notification:8005", "endpoint": "/api/users/{user_id}/notifications"},
        {"name": "payment-service", "url": "http://payment-service:8004", "endpoint": "/api/users/{user_id}/payments"},
        {"name": "telegram-integration", "url": "http://telegram-integration:4007", "endpoint": "/api/users/{user_id}/messages"}
    ]
    
    aggregated_data = {
        "user_id": export_request.user_id,
        "export_date": datetime.utcnow().isoformat(),
        "export_format": export_request.export_format,
        "services": {}
    }
    
    async with httpx.AsyncClient() as client:
        for service in services:
            try:
                url = service["url"] + service["endpoint"].format(user_id=export_request.user_id)
                response = await client.get(url, timeout=30.0)
                
                if response.status_code == 200:
                    service_data = response.json()
                    aggregated_data["services"][service["name"]] = service_data
                else:
                    aggregated_data["services"][service["name"]] = {"error": f"HTTP {response.status_code}"}
                    
            except Exception as e:
                aggregated_data["services"][service["name"]] = {"error": str(e)}
    
    # Update request status
    db = next(get_db())
    data_request = db.query(DataRequest).filter(DataRequest.id == request_id).first()
    if data_request:
        data_request.status = "completed"
        data_request.completion_date = datetime.utcnow()
        data_request.response_data = aggregated_data
        db.commit()
    
    # Send notification email with secure download link
    await send_export_notification(export_request.user_id, request_id)

@app.delete("/api/data-rights/delete")
async def request_data_deletion(
    user_id: str,
    reason: str,
    current_user: dict = Depends(verify_user_token),
    db: Session = Depends(get_db)
):
    """Article 17 - Right to erasure (Right to be forgotten)"""
    
    # Verify user identity
    if user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Create deletion request
    request_id = str(uuid4())
    data_request = DataRequest(
        id=request_id,
        user_id=user_id,
        request_type="delete",
        status="processing",
        request_date=datetime.utcnow(),
        verification_token=generate_verification_token()
    )
    
    db.add(data_request)
    db.commit()
    
    # Start background deletion process
    asyncio.create_task(delete_user_data(request_id, user_id, reason))
    
    return {
        "request_id": request_id,
        "status": "processing",
        "message": "Data deletion request initiated.",
        "estimated_completion": "within 30 days"
    }

async def delete_user_data(request_id: str, user_id: str, reason: str):
    """Delete or anonymize user data across all services"""
    
    # Services to delete data from
    deletion_services = [
        {"name": "auth-service", "url": "http://auth-service:3001", "endpoint": "/api/users/{user_id}"},
        {"name": "django-crm", "url": "http://django-crm:8007", "endpoint": "/api/customers/{user_id}"},
        {"name": "ai-agents", "url": "http://ai-agents:8001", "endpoint": "/api/users/{user_id}/data"},
        {"name": "analytics-service", "url": "http://analytics-service:8003", "endpoint": "/api/users/{user_id}"},
        {"name": "user-management", "url": "http://user-management:8006", "endpoint": "/api/users/{user_id}"},
        {"name": "telegram-integration", "url": "http://telegram-integration:4007", "endpoint": "/api/users/{user_id}"}
    ]
    
    deletion_results = {}
    
    async with httpx.AsyncClient() as client:
        for service in deletion_services:
            try:
                url = service["url"] + service["endpoint"].format(user_id=user_id)
                response = await client.delete(
                    url, 
                    json={"reason": reason, "request_id": request_id},
                    timeout=60.0
                )
                
                deletion_results[service["name"]] = {
                    "status": "success" if response.status_code in [200, 204] else "failed",
                    "response_code": response.status_code,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except Exception as e:
                deletion_results[service["name"]] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
    
    # Update request status
    db = next(get_db())
    data_request = db.query(DataRequest).filter(DataRequest.id == request_id).first()
    if data_request:
        all_successful = all(result["status"] == "success" for result in deletion_results.values())
        data_request.status = "completed" if all_successful else "partial_failure"
        data_request.completion_date = datetime.utcnow()
        data_request.response_data = deletion_results
        db.commit()
    
    # Log deletion audit trail
    await log_deletion_audit(user_id, reason, deletion_results)
    
    # Send confirmation notification
    await send_deletion_confirmation(user_id, request_id, deletion_results)

@app.get("/api/data-rights/status/{request_id}")
async def get_request_status(
    request_id: str,
    current_user: dict = Depends(verify_user_token),
    db: Session = Depends(get_db)
):
    """Get status of data rights request"""
    
    data_request = db.query(DataRequest).filter(DataRequest.id == request_id).first()
    if not data_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Verify user owns this request
    if data_request.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return {
        "request_id": request_id,
        "type": data_request.request_type,
        "status": data_request.status,
        "request_date": data_request.request_date,
        "completion_date": data_request.completion_date,
        "download_url": f"/api/data-rights/download/{request_id}" if data_request.status == "completed" and data_request.request_type == "export" else None
    }
```

## 3. Consent Management System

### Consent Service Implementation

```python
# services/consent-management-service/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from enum import Enum
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="Consent Management Service")

class ConsentType(str, Enum):
    ESSENTIAL = "essential"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    PERSONALIZATION = "personalization"
    THIRD_PARTY = "third_party"

class LegalBasis(str, Enum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"

class ConsentRecord(BaseModel):
    id: str
    user_id: str
    consent_type: ConsentType
    consent_given: bool
    legal_basis: LegalBasis
    purpose_description: str
    consent_date: datetime
    withdrawal_date: Optional[datetime] = None
    source: str  # web, mobile, api
    ip_address: str
    user_agent: str

@app.post("/api/consent/record")
async def record_consent(
    user_id: str,
    consents: List[dict],
    request: Request,
    db: Session = Depends(get_db)
):
    """Record user consent preferences"""
    
    consent_records = []
    
    for consent_data in consents:
        consent_record = ConsentRecord(
            id=str(uuid4()),
            user_id=user_id,
            consent_type=consent_data["type"],
            consent_given=consent_data["given"],
            legal_basis=consent_data.get("legal_basis", LegalBasis.CONSENT),
            purpose_description=consent_data["purpose"],
            consent_date=datetime.utcnow(),
            source="web",
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", "")
        )
        
        db.add(consent_record)
        consent_records.append(consent_record)
    
    db.commit()
    
    # Propagate consent to relevant services
    await propagate_consent_to_services(user_id, consents)
    
    return {
        "message": "Consent preferences recorded",
        "records": len(consent_records),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/consent/withdraw")
async def withdraw_consent(
    user_id: str,
    consent_type: ConsentType,
    db: Session = Depends(get_db)
):
    """Withdraw specific consent"""
    
    # Find active consent record
    consent_record = db.query(ConsentRecord).filter(
        ConsentRecord.user_id == user_id,
        ConsentRecord.consent_type == consent_type,
        ConsentRecord.consent_given == True,
        ConsentRecord.withdrawal_date.is_(None)
    ).first()
    
    if consent_record:
        consent_record.withdrawal_date = datetime.utcnow()
        db.commit()
        
        # Notify services of consent withdrawal
        await notify_consent_withdrawal(user_id, consent_type)
        
        return {
            "message": f"Consent for {consent_type} withdrawn",
            "withdrawal_date": consent_record.withdrawal_date.isoformat()
        }
    else:
        raise HTTPException(status_code=404, detail="No active consent found")

@app.get("/api/consent/status/{user_id}")
async def get_consent_status(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get current consent status for user"""
    
    # Get latest consent for each type
    consent_status = {}
    
    for consent_type in ConsentType:
        latest_consent = db.query(ConsentRecord).filter(
            ConsentRecord.user_id == user_id,
            ConsentRecord.consent_type == consent_type
        ).order_by(ConsentRecord.consent_date.desc()).first()
        
        if latest_consent:
            consent_status[consent_type.value] = {
                "given": latest_consent.consent_given and latest_consent.withdrawal_date is None,
                "date": latest_consent.consent_date.isoformat(),
                "withdrawal_date": latest_consent.withdrawal_date.isoformat() if latest_consent.withdrawal_date else None,
                "purpose": latest_consent.purpose_description,
                "legal_basis": latest_consent.legal_basis.value
            }
        else:
            consent_status[consent_type.value] = {
                "given": False,
                "date": None,
                "purpose": get_default_purpose(consent_type),
                "legal_basis": "not_specified"
            }
    
    return consent_status

async def propagate_consent_to_services(user_id: str, consents: List[dict]):
    """Notify all services of consent changes"""
    
    services = [
        "analytics-service",
        "marketing-automation-service", 
        "ai-agents",
        "notification"
    ]
    
    consent_payload = {
        "user_id": user_id,
        "consents": consents,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    async with httpx.AsyncClient() as client:
        for service in services:
            try:
                await client.post(
                    f"http://{service}/api/consent/update",
                    json=consent_payload,
                    timeout=10.0
                )
            except Exception as e:
                logger.error(f"Failed to propagate consent to {service}: {e}")
```

## 4. Data Breach Notification (Article 33)

### Breach Detection and Notification Service

```python
# services/breach-notification-service/main.py
from fastapi import FastAPI
from datetime import datetime, timedelta
import asyncio
from enum import Enum

app = FastAPI(title="Breach Notification Service")

class BreachSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class BreachType(str, Enum):
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_LOSS = "data_loss"
    SYSTEM_COMPROMISE = "system_compromise"
    INSIDER_THREAT = "insider_threat"

@app.post("/api/breach/report")
async def report_breach(
    breach_type: BreachType,
    severity: BreachSeverity,
    description: str,
    affected_users: List[str],
    data_categories: List[str],
    reported_by: str
):
    """Report a data breach incident"""
    
    breach_id = str(uuid4())
    
    breach_record = {
        "id": breach_id,
        "type": breach_type,
        "severity": severity,
        "description": description,
        "affected_users": affected_users,
        "data_categories": data_categories,
        "reported_by": reported_by,
        "discovery_date": datetime.utcnow(),
        "status": "investigating"
    }
    
    # Start 72-hour countdown for supervisory authority notification
    if severity in [BreachSeverity.HIGH, BreachSeverity.CRITICAL]:
        asyncio.create_task(schedule_authority_notification(breach_id, 72))
    
    # Assess if user notification is required
    if requires_user_notification(severity, data_categories):
        asyncio.create_task(schedule_user_notification(breach_id, affected_users))
    
    # Immediate internal notification
    await notify_dpo_and_management(breach_record)
    
    return {
        "breach_id": breach_id,
        "status": "reported",
        "authority_notification_deadline": (datetime.utcnow() + timedelta(hours=72)).isoformat(),
        "next_steps": "Investigation initiated"
    }

async def schedule_authority_notification(breach_id: str, hours: int):
    """GDPR Article 33 - 72-hour notification to supervisory authority"""
    
    # Wait for deadline minus buffer time for preparation
    await asyncio.sleep((hours - 6) * 3600)  # 6-hour buffer
    
    # Generate notification report
    breach_assessment = await generate_breach_assessment(breach_id)
    
    # Send to supervisory authority
    await send_authority_notification(breach_assessment)
    
    # Update breach record
    await update_breach_status(breach_id, "authority_notified")

async def generate_breach_assessment(breach_id: str) -> dict:
    """Generate comprehensive breach assessment report"""
    
    return {
        "breach_id": breach_id,
        "assessment_date": datetime.utcnow().isoformat(),
        "nature_of_breach": "Description of what happened",
        "categories_of_data": ["Personal identifiers", "Contact details"],
        "approximate_number_affected": 1500,
        "likely_consequences": "Risk of identity theft",
        "measures_taken": [
            "Incident containment",
            "Security patches applied",
            "User password reset required"
        ],
        "contact_information": {
            "dpo": "dpo@bizosaas.com",
            "security_team": "security@bizosaas.com"
        }
    }
```

## 5. Service-Specific Implementation Examples

### Auth Service GDPR Updates

```python
# services/auth-service/gdpr_endpoints.py

@app.get("/api/users/{user_id}/data")
async def export_user_auth_data(user_id: str):
    """Export user authentication data for GDPR compliance"""
    
    user_data = {
        "user_profile": {
            "user_id": user_id,
            "email": user.email,
            "username": user.username,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "email_verified": user.email_verified,
            "account_status": user.status
        },
        "login_history": [
            {
                "timestamp": login.timestamp.isoformat(),
                "ip_address": login.ip_address,
                "user_agent": login.user_agent,
                "success": login.success
            }
            for login in user.login_attempts[-100:]  # Last 100 attempts
        ],
        "security_settings": {
            "two_factor_enabled": user.two_factor_enabled,
            "password_last_changed": user.password_changed_at.isoformat(),
            "security_questions_set": bool(user.security_questions)
        },
        "consent_records": [
            {
                "consent_type": consent.consent_type,
                "given": consent.consent_given,
                "date": consent.consent_date.isoformat(),
                "purpose": consent.purpose_description
            }
            for consent in user.consent_records
        ]
    }
    
    return user_data

@app.delete("/api/users/{user_id}")
async def delete_user_account(user_id: str, reason: str):
    """Delete user account and associated data"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Log deletion for audit trail
    deletion_log = DeletionAuditLog(
        user_id=user_id,
        reason=reason,
        deleted_by="user_request",
        deletion_date=datetime.utcnow(),
        data_categories=["identity", "authentication", "security"]
    )
    db.add(deletion_log)
    
    # Delete user data
    db.delete(user)
    
    # Delete related records
    db.query(LoginAttempt).filter(LoginAttempt.user_id == user_id).delete()
    db.query(SecurityQuestion).filter(SecurityQuestion.user_id == user_id).delete()
    
    db.commit()
    
    return {"message": "User account deleted successfully", "deletion_date": datetime.utcnow().isoformat()}
```

### CRM Service GDPR Updates

```python
# services/django-crm/gdpr_views.py

@api_view(['GET'])
def export_customer_data(request, customer_id):
    """Export customer data for GDPR Article 20"""
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    customer_data = {
        "customer_profile": {
            "id": str(customer.id),
            "company_name": customer.company_name,
            "contact_person": customer.contact_person,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address,
            "created_at": customer.created_at.isoformat(),
            "last_updated": customer.updated_at.isoformat()
        },
        "leads": [
            {
                "id": str(lead.id),
                "title": lead.title,
                "status": lead.status,
                "value": str(lead.value),
                "created_at": lead.created_at.isoformat(),
                "source": lead.source
            }
            for lead in customer.leads.all()
        ],
        "campaigns": [
            {
                "id": str(campaign.id),
                "name": campaign.name,
                "type": campaign.campaign_type,
                "sent_at": campaign.sent_at.isoformat() if campaign.sent_at else None,
                "opened": campaign.opened,
                "clicked": campaign.clicked
            }
            for campaign in customer.campaign_interactions.all()
        ],
        "support_tickets": [
            {
                "id": str(ticket.id),
                "subject": ticket.subject,
                "status": ticket.status,
                "created_at": ticket.created_at.isoformat(),
                "resolved_at": ticket.resolved_at.isoformat() if ticket.resolved_at else None
            }
            for ticket in customer.support_tickets.all()
        ]
    }
    
    return Response(customer_data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_customer_data(request, customer_id):
    """Delete customer data for GDPR Article 17"""
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    # Log deletion request
    DeletionLog.objects.create(
        customer_id=customer_id,
        reason=request.data.get('reason', 'User request'),
        deleted_by=request.user.id if request.user.is_authenticated else 'anonymous',
        deletion_date=timezone.now()
    )
    
    # Delete or anonymize related data
    customer.leads.all().delete()
    customer.campaign_interactions.all().delete()
    customer.support_tickets.update(customer_name="[DELETED]", customer_email="[DELETED]")
    
    # Delete customer record
    customer.delete()
    
    return Response(
        {"message": "Customer data deleted successfully"}, 
        status=status.HTTP_204_NO_CONTENT
    )
```

## 6. Frontend Privacy Dashboard

### User Privacy Dashboard Component

```typescript
// services/frontend-nextjs/components/PrivacyDashboard.tsx
import React, { useState, useEffect } from 'react';
import { Button, Card, Switch, Alert, Modal } from 'antd';

interface ConsentStatus {
  essential: { given: boolean; date: string; purpose: string };
  analytics: { given: boolean; date: string; purpose: string };
  marketing: { given: boolean; date: string; purpose: string };
  personalization: { given: boolean; date: string; purpose: string };
}

const PrivacyDashboard: React.FC = () => {
  const [consents, setConsents] = useState<ConsentStatus | null>(null);
  const [exportModalVisible, setExportModalVisible] = useState(false);
  const [deleteModalVisible, setDeleteModalVisible] = useState(false);

  useEffect(() => {
    fetchConsentStatus();
  }, []);

  const fetchConsentStatus = async () => {
    try {
      const response = await fetch('/api/consent/status', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setConsents(data);
    } catch (error) {
      console.error('Failed to fetch consent status:', error);
    }
  };

  const updateConsent = async (consentType: string, given: boolean) => {
    try {
      await fetch('/api/consent/record', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify([{
          type: consentType,
          given: given,
          purpose: getConsentPurpose(consentType)
        }])
      });
      
      fetchConsentStatus(); // Refresh status
    } catch (error) {
      console.error('Failed to update consent:', error);
    }
  };

  const requestDataExport = async () => {
    try {
      const response = await fetch('/api/data-rights/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          export_format: 'json',
          include_deleted: false
        })
      });
      
      const result = await response.json();
      alert(`Data export requested. Request ID: ${result.request_id}`);
      setExportModalVisible(false);
    } catch (error) {
      console.error('Failed to request data export:', error);
    }
  };

  const requestDataDeletion = async () => {
    try {
      const response = await fetch('/api/data-rights/delete', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          reason: 'User requested account deletion'
        })
      });
      
      const result = await response.json();
      alert(`Data deletion requested. Request ID: ${result.request_id}`);
      setDeleteModalVisible(false);
    } catch (error) {
      console.error('Failed to request data deletion:', error);
    }
  };

  const getConsentPurpose = (consentType: string): string => {
    const purposes = {
      essential: 'Required for basic platform functionality and security',
      analytics: 'Help us improve the platform by analyzing usage patterns',
      marketing: 'Send you relevant marketing communications and offers',
      personalization: 'Personalize your experience and content recommendations'
    };
    return purposes[consentType] || '';
  };

  if (!consents) {
    return <div>Loading privacy settings...</div>;
  }

  return (
    <div className="privacy-dashboard">
      <h1>Privacy Dashboard</h1>
      <p>Manage your data privacy settings and exercise your rights under GDPR.</p>

      <Card title="Consent Management" style={{ marginBottom: 24 }}>
        {Object.entries(consents).map(([type, consent]) => (
          <div key={type} style={{ marginBottom: 16, padding: 16, border: '1px solid #f0f0f0', borderRadius: 4 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ margin: 0, textTransform: 'capitalize' }}>{type.replace('_', ' ')}</h4>
                <p style={{ margin: '4px 0', color: '#666', fontSize: '14px' }}>
                  {getConsentPurpose(type)}
                </p>
                {consent.date && (
                  <p style={{ margin: 0, color: '#999', fontSize: '12px' }}>
                    Last updated: {new Date(consent.date).toLocaleDateString()}
                  </p>
                )}
              </div>
              <Switch
                checked={consent.given}
                onChange={(checked) => updateConsent(type, checked)}
                disabled={type === 'essential'} // Essential cookies cannot be disabled
              />
            </div>
          </div>
        ))}
        
        {consents.essential.given === false && (
          <Alert
            message="Essential cookies are required for platform functionality and cannot be disabled."
            type="info"
            showIcon
          />
        )}
      </Card>

      <Card title="Your Data Rights" style={{ marginBottom: 24 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 16 }}>
          <div>
            <h4>Right to Data Portability</h4>
            <p>Download a copy of your personal data in a machine-readable format.</p>
            <Button onClick={() => setExportModalVisible(true)}>
              Request Data Export
            </Button>
          </div>
          
          <div>
            <h4>Right to Erasure</h4>
            <p>Request deletion of your personal data from our systems.</p>
            <Button danger onClick={() => setDeleteModalVisible(true)}>
              Delete My Data
            </Button>
          </div>
          
          <div>
            <h4>Right to Rectification</h4>
            <p>Update or correct your personal information.</p>
            <Button href="/profile/edit">
              Edit Profile
            </Button>
          </div>
          
          <div>
            <h4>Right to Object</h4>
            <p>Object to processing based on legitimate interests.</p>
            <Button href="/privacy/object">
              File Objection
            </Button>
          </div>
        </div>
      </Card>

      <Card title="Privacy Information">
        <p>
          For more information about how we process your data, please read our{' '}
          <a href="/privacy-policy" target="_blank">Privacy Policy</a>.
        </p>
        <p>
          If you have any questions or concerns about your privacy, please contact our Data Protection Officer at{' '}
          <a href="mailto:dpo@bizosaas.com">dpo@bizosaas.com</a>.
        </p>
        <p>
          You also have the right to lodge a complaint with your local supervisory authority if you believe 
          your data protection rights have been violated.
        </p>
      </Card>

      {/* Data Export Modal */}
      <Modal
        title="Request Data Export"
        open={exportModalVisible}
        onOk={requestDataExport}
        onCancel={() => setExportModalVisible(false)}
        okText="Request Export"
      >
        <p>This will create a comprehensive export of all your personal data stored in our systems.</p>
        <p>You will receive an email notification when your data export is ready for download (within 30 days).</p>
        <Alert
          message="The export will include all personal data across all services you have used."
          type="info"
          showIcon
        />
      </Modal>

      {/* Data Deletion Modal */}
      <Modal
        title="Request Data Deletion"
        open={deleteModalVisible}
        onOk={requestDataDeletion}
        onCancel={() => setDeleteModalVisible(false)}
        okText="Confirm Deletion"
        okButtonProps={{ danger: true }}
      >
        <Alert
          message="Warning: This action cannot be undone"
          description="Deleting your data will permanently remove your account and all associated information from our systems."
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
        <p>This will:</p>
        <ul>
          <li>Permanently delete your account and profile</li>
          <li>Remove all your personal data from our systems</li>
          <li>Cancel any active subscriptions</li>
          <li>Delete all your created content and preferences</li>
        </ul>
        <p>Are you sure you want to proceed?</p>
      </Modal>
    </div>
  );
};

export default PrivacyDashboard;
```

This comprehensive GDPR implementation guide provides the foundation for bringing the BizOSaaS platform into full compliance with European data protection regulations. The implementation should be prioritized and completed within 30 days to enable international deployment.