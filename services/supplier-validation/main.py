#!/usr/bin/env python3
"""
Supplier Validation Workflow [P9] - BizOSaaS Platform
Human-in-the-Loop (HITL) Approval System with Business License Verification

This service provides comprehensive supplier validation capabilities including:
- Multi-step human validation workflow with role-based approvals
- Business license verification and document management
- AI-powered supplier quality assessment and risk scoring
- Compliance checking and audit trail
- Integration with Product Sourcing Workflow [P8]
- Indian market-specific validation (GST, PAN, Aadhaar)

Author: BizOSaaS Platform Team
Version: 1.0.0
Port: 8027 (Supplier Validation Service)
"""

import asyncio
import io
import json
import logging
import os
import hashlib
import mimetypes
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

import aiohttp
import asyncpg
import redis
import boto3
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
import requests
from textblob import TextBlob
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import cv2
import pytesseract
from PIL import Image
import re
import phonenumbers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Supplier Validation Workflow [P9]",
    description="Human-in-the-Loop Approval System with Business License Verification",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/bizosaas")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
BRAIN_API_URL = os.getenv("BRAIN_API_URL", "http://localhost:8001")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "supplier-documents")
API_KEY = os.getenv("API_KEY", "your-api-key")
GST_API_KEY = os.getenv("GST_API_KEY", "")
PAN_API_KEY = os.getenv("PAN_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Database connection
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Enums for supplier validation workflow
class SupplierStatus(str, Enum):
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    DOCUMENTS_REQUIRED = "documents_required"
    COMPLIANCE_CHECK = "compliance_check"
    MANAGER_REVIEW = "manager_review"
    DIRECTOR_APPROVAL = "director_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    BLACKLISTED = "blacklisted"

class DocumentType(str, Enum):
    BUSINESS_LICENSE = "business_license"
    GST_CERTIFICATE = "gst_certificate"
    PAN_CARD = "pan_card"
    BANK_STATEMENT = "bank_statement"
    INCORPORATION_CERTIFICATE = "incorporation_certificate"
    TAX_RETURN = "tax_return"
    TRADE_LICENSE = "trade_license"
    QUALITY_CERTIFICATE = "quality_certificate"
    INSURANCE_POLICY = "insurance_policy"
    FINANCIAL_STATEMENT = "financial_statement"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class UserRole(str, Enum):
    ANALYST = "analyst"
    MANAGER = "manager"
    DIRECTOR = "director"
    ADMIN = "admin"

class ValidationStep(str, Enum):
    DOCUMENT_UPLOAD = "document_upload"
    AUTOMATED_VERIFICATION = "automated_verification"
    ANALYST_REVIEW = "analyst_review"
    MANAGER_APPROVAL = "manager_approval"
    DIRECTOR_APPROVAL = "director_approval"
    COMPLIANCE_CHECK = "compliance_check"
    FINAL_APPROVAL = "final_approval"

# Pydantic models
class SupplierRegistration(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    contact_person: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=10, max_length=500)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    country: str = Field(default="India", max_length=100)
    pincode: str = Field(..., regex=r'^\d{6}$')
    website: Optional[str] = Field(None, regex=r'^https?://.+')
    business_type: str = Field(..., min_length=2, max_length=100)
    industry: str = Field(..., min_length=2, max_length=100)
    products_offered: List[str] = Field(..., min_items=1)
    annual_revenue: Optional[float] = Field(None, ge=0)
    employee_count: Optional[int] = Field(None, ge=1)
    gst_number: Optional[str] = Field(None, regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
    pan_number: Optional[str] = Field(None, regex=r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
    
    @validator('phone')
    def validate_phone(cls, v):
        try:
            parsed = phonenumbers.parse(v, "IN")
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except:
            raise ValueError("Invalid phone number format")

class DocumentUpload(BaseModel):
    supplier_id: str
    document_type: DocumentType
    file_name: str
    file_size: int
    content_type: str
    metadata: Optional[Dict[str, Any]] = None

class ValidationDecision(BaseModel):
    supplier_id: str
    decision: str = Field(..., regex=r'^(approve|reject|request_more_info)$')
    comments: str = Field(..., min_length=10, max_length=1000)
    requested_documents: Optional[List[DocumentType]] = None
    risk_flags: Optional[List[str]] = None

class SupplierUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    products_offered: Optional[List[str]] = None
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None

class RiskAssessment(BaseModel):
    supplier_id: str
    risk_level: RiskLevel
    risk_score: float = Field(..., ge=0, le=100)
    risk_factors: List[str]
    recommendations: List[str]
    compliance_issues: Optional[List[str]] = None

# Data classes for internal processing
@dataclass
class SupplierProfile:
    id: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    website: Optional[str]
    business_type: str
    industry: str
    products_offered: List[str]
    annual_revenue: Optional[float]
    employee_count: Optional[int]
    gst_number: Optional[str]
    pan_number: Optional[str]
    status: SupplierStatus
    risk_level: RiskLevel
    risk_score: float
    created_at: datetime
    updated_at: datetime
    created_by: str
    assigned_analyst: Optional[str] = None
    assigned_manager: Optional[str] = None

@dataclass
class ValidationWorkflow:
    id: str
    supplier_id: str
    current_step: ValidationStep
    status: SupplierStatus
    steps_completed: List[ValidationStep]
    pending_actions: List[str]
    approvals: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

@dataclass
class Document:
    id: str
    supplier_id: str
    document_type: DocumentType
    file_name: str
    file_path: str
    file_size: int
    content_type: str
    upload_date: datetime
    uploaded_by: str
    verification_status: str
    extracted_data: Optional[Dict[str, Any]] = None
    ai_analysis: Optional[Dict[str, Any]] = None

# AI-powered risk assessment engine
class SupplierRiskAssessmentEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    async def assess_supplier_risk(self, supplier_data: Dict[str, Any], documents: List[Document]) -> RiskAssessment:
        """Perform comprehensive AI-powered risk assessment"""
        try:
            # Extract features for risk assessment
            features = self._extract_risk_features(supplier_data, documents)
            
            # Calculate risk score
            risk_score = await self._calculate_risk_score(features)
            
            # Determine risk level
            risk_level = self._determine_risk_level(risk_score)
            
            # Identify risk factors
            risk_factors = await self._identify_risk_factors(supplier_data, documents)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(risk_level, risk_factors)
            
            # Check compliance issues
            compliance_issues = await self._check_compliance_issues(supplier_data)
            
            return RiskAssessment(
                supplier_id=supplier_data['id'],
                risk_level=risk_level,
                risk_score=risk_score,
                risk_factors=risk_factors,
                recommendations=recommendations,
                compliance_issues=compliance_issues
            )
            
        except Exception as e:
            logger.error(f"Error in risk assessment: {str(e)}")
            return RiskAssessment(
                supplier_id=supplier_data['id'],
                risk_level=RiskLevel.HIGH,
                risk_score=75.0,
                risk_factors=["Assessment error occurred"],
                recommendations=["Manual review required"]
            )
    
    def _extract_risk_features(self, supplier_data: Dict[str, Any], documents: List[Document]) -> Dict[str, float]:
        """Extract numerical features for risk assessment"""
        features = {}
        
        # Company age estimation (if available)
        features['has_website'] = 1.0 if supplier_data.get('website') else 0.0
        features['employee_count'] = float(supplier_data.get('employee_count', 0))
        features['annual_revenue'] = float(supplier_data.get('annual_revenue', 0))
        features['document_count'] = float(len(documents))
        features['has_gst'] = 1.0 if supplier_data.get('gst_number') else 0.0
        features['has_pan'] = 1.0 if supplier_data.get('pan_number') else 0.0
        features['product_diversity'] = float(len(supplier_data.get('products_offered', [])))
        
        # Document verification scores
        verified_docs = sum(1 for doc in documents if doc.verification_status == 'verified')
        features['doc_verification_ratio'] = verified_docs / len(documents) if documents else 0.0
        
        return features
    
    async def _calculate_risk_score(self, features: Dict[str, float]) -> float:
        """Calculate risk score using AI model or rules-based approach"""
        try:
            # Base risk calculation
            risk_score = 50.0  # Neutral starting point
            
            # Positive factors (reduce risk)
            if features.get('has_gst', 0) and features.get('has_pan', 0):
                risk_score -= 15
            
            if features.get('employee_count', 0) > 50:
                risk_score -= 10
            
            if features.get('annual_revenue', 0) > 10000000:  # 1 crore
                risk_score -= 10
            
            if features.get('doc_verification_ratio', 0) > 0.8:
                risk_score -= 15
            
            if features.get('has_website', 0):
                risk_score -= 5
            
            # Negative factors (increase risk)
            if features.get('document_count', 0) < 3:
                risk_score += 20
            
            if features.get('employee_count', 0) < 10:
                risk_score += 10
            
            if features.get('doc_verification_ratio', 0) < 0.5:
                risk_score += 25
            
            # Ensure score is within bounds
            risk_score = max(0, min(100, risk_score))
            
            return risk_score
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            return 75.0  # High risk as default
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determine risk level based on score"""
        if risk_score >= 80:
            return RiskLevel.CRITICAL
        elif risk_score >= 60:
            return RiskLevel.HIGH
        elif risk_score >= 40:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    async def _identify_risk_factors(self, supplier_data: Dict[str, Any], documents: List[Document]) -> List[str]:
        """Identify specific risk factors"""
        risk_factors = []
        
        # Missing critical information
        if not supplier_data.get('gst_number'):
            risk_factors.append("Missing GST registration")
        
        if not supplier_data.get('pan_number'):
            risk_factors.append("Missing PAN card details")
        
        # Business validation
        if not supplier_data.get('website'):
            risk_factors.append("No business website")
        
        if supplier_data.get('employee_count', 0) < 5:
            risk_factors.append("Very small team size")
        
        # Document validation
        required_docs = [DocumentType.BUSINESS_LICENSE, DocumentType.GST_CERTIFICATE, DocumentType.PAN_CARD]
        uploaded_types = [doc.document_type for doc in documents]
        
        for req_doc in required_docs:
            if req_doc not in uploaded_types:
                risk_factors.append(f"Missing {req_doc.value}")
        
        # Verification issues
        unverified_docs = [doc for doc in documents if doc.verification_status != 'verified']
        if unverified_docs:
            risk_factors.append(f"{len(unverified_docs)} documents pending verification")
        
        return risk_factors
    
    def _generate_recommendations(self, risk_level: RiskLevel, risk_factors: List[str]) -> List[str]:
        """Generate specific recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == RiskLevel.CRITICAL:
            recommendations.extend([
                "Immediate manual review required",
                "Verify all documents through primary sources",
                "Conduct on-site inspection",
                "Request additional financial guarantees"
            ])
        
        elif risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "Enhanced due diligence required",
                "Verify business registration",
                "Check references from existing clients",
                "Limited initial order quantity"
            ])
        
        elif risk_level == RiskLevel.MEDIUM:
            recommendations.extend([
                "Standard verification process",
                "Monitor initial transactions closely",
                "Regular performance reviews"
            ])
        
        else:  # LOW risk
            recommendations.extend([
                "Standard onboarding process",
                "Regular compliance monitoring"
            ])
        
        # Specific recommendations based on risk factors
        for factor in risk_factors:
            if "Missing GST" in factor:
                recommendations.append("Request GST registration certificate")
            elif "Missing PAN" in factor:
                recommendations.append("Request PAN card verification")
            elif "website" in factor:
                recommendations.append("Verify business presence through other channels")
        
        return list(set(recommendations))  # Remove duplicates
    
    async def _check_compliance_issues(self, supplier_data: Dict[str, Any]) -> List[str]:
        """Check for compliance issues"""
        compliance_issues = []
        
        # GST validation
        gst_number = supplier_data.get('gst_number')
        if gst_number:
            is_valid_gst = await self._validate_gst_number(gst_number)
            if not is_valid_gst:
                compliance_issues.append("Invalid GST number format or registration")
        
        # PAN validation
        pan_number = supplier_data.get('pan_number')
        if pan_number:
            is_valid_pan = self._validate_pan_number(pan_number)
            if not is_valid_pan:
                compliance_issues.append("Invalid PAN number format")
        
        # Industry-specific compliance
        industry = supplier_data.get('industry', '').lower()
        if 'food' in industry or 'pharmaceutical' in industry:
            compliance_issues.append("Requires additional industry-specific certifications")
        
        return compliance_issues
    
    async def _validate_gst_number(self, gst_number: str) -> bool:
        """Validate GST number through API"""
        try:
            if not GST_API_KEY:
                return self._validate_gst_format(gst_number)
            
            # API validation would go here
            # For now, just format validation
            return self._validate_gst_format(gst_number)
            
        except Exception as e:
            logger.error(f"Error validating GST: {str(e)}")
            return False
    
    def _validate_gst_format(self, gst_number: str) -> bool:
        """Validate GST number format"""
        pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
        return bool(re.match(pattern, gst_number))
    
    def _validate_pan_number(self, pan_number: str) -> bool:
        """Validate PAN number format"""
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pattern, pan_number))

# Document verification engine
class DocumentVerificationEngine:
    def __init__(self):
        self.supported_formats = {'.pdf', '.jpg', '.jpeg', '.png', '.tiff'}
    
    async def verify_document(self, document: Document, file_content: bytes) -> Dict[str, Any]:
        """Perform comprehensive document verification"""
        try:
            verification_result = {
                'status': 'pending',
                'confidence_score': 0.0,
                'extracted_data': {},
                'verification_checks': {},
                'issues': []
            }
            
            # File format validation
            if not self._validate_file_format(document.file_name):
                verification_result['issues'].append("Unsupported file format")
                verification_result['status'] = 'failed'
                return verification_result
            
            # Extract text from document
            extracted_text = await self._extract_text_from_document(file_content, document.content_type)
            
            # Document-specific verification
            if document.document_type == DocumentType.GST_CERTIFICATE:
                verification_result = await self._verify_gst_certificate(extracted_text, verification_result)
            elif document.document_type == DocumentType.PAN_CARD:
                verification_result = await self._verify_pan_card(extracted_text, verification_result)
            elif document.document_type == DocumentType.BUSINESS_LICENSE:
                verification_result = await self._verify_business_license(extracted_text, verification_result)
            else:
                verification_result = await self._verify_generic_document(extracted_text, verification_result)
            
            # Calculate overall confidence score
            verification_result['confidence_score'] = self._calculate_confidence_score(verification_result)
            
            # Determine final status
            if verification_result['confidence_score'] >= 0.8:
                verification_result['status'] = 'verified'
            elif verification_result['confidence_score'] >= 0.6:
                verification_result['status'] = 'partially_verified'
            else:
                verification_result['status'] = 'failed'
            
            return verification_result
            
        except Exception as e:
            logger.error(f"Error verifying document: {str(e)}")
            return {
                'status': 'error',
                'confidence_score': 0.0,
                'extracted_data': {},
                'verification_checks': {},
                'issues': [f"Verification error: {str(e)}"]
            }
    
    def _validate_file_format(self, filename: str) -> bool:
        """Validate if file format is supported"""
        file_ext = Path(filename).suffix.lower()
        return file_ext in self.supported_formats
    
    async def _extract_text_from_document(self, file_content: bytes, content_type: str) -> str:
        """Extract text from document using OCR"""
        try:
            if content_type.startswith('image/'):
                # Use PIL and pytesseract for image OCR
                image = Image.open(io.BytesIO(file_content))
                text = pytesseract.image_to_string(image)
                return text
            elif content_type == 'application/pdf':
                # For PDF, would need PDF processing library
                # For now, return empty string
                return ""
            else:
                return ""
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""
    
    async def _verify_gst_certificate(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify GST certificate specific fields"""
        checks = {}
        
        # Look for GST number pattern
        gst_pattern = r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}'
        gst_matches = re.findall(gst_pattern, text)
        
        if gst_matches:
            result['extracted_data']['gst_number'] = gst_matches[0]
            checks['gst_number_found'] = True
        else:
            checks['gst_number_found'] = False
            result['issues'].append("GST number not found in document")
        
        # Look for business name
        if len(text.strip()) > 50:
            checks['sufficient_content'] = True
        else:
            checks['sufficient_content'] = False
            result['issues'].append("Insufficient content in document")
        
        result['verification_checks'].update(checks)
        return result
    
    async def _verify_pan_card(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify PAN card specific fields"""
        checks = {}
        
        # Look for PAN number pattern
        pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        pan_matches = re.findall(pan_pattern, text)
        
        if pan_matches:
            result['extracted_data']['pan_number'] = pan_matches[0]
            checks['pan_number_found'] = True
        else:
            checks['pan_number_found'] = False
            result['issues'].append("PAN number not found in document")
        
        # Look for name
        if 'name' in text.lower() or len(text.strip()) > 30:
            checks['name_section_found'] = True
        else:
            checks['name_section_found'] = False
            result['issues'].append("Name section not clearly visible")
        
        result['verification_checks'].update(checks)
        return result
    
    async def _verify_business_license(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify business license specific fields"""
        checks = {}
        
        # Look for license keywords
        license_keywords = ['license', 'registration', 'certificate', 'permit']
        found_keywords = [kw for kw in license_keywords if kw.lower() in text.lower()]
        
        if found_keywords:
            checks['license_keywords_found'] = True
            result['extracted_data']['license_type'] = found_keywords[0]
        else:
            checks['license_keywords_found'] = False
            result['issues'].append("No license/registration keywords found")
        
        # Look for dates
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{4}',
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            dates_found.extend(re.findall(pattern, text))
        
        if dates_found:
            checks['dates_found'] = True
            result['extracted_data']['dates'] = dates_found
        else:
            checks['dates_found'] = False
        
        result['verification_checks'].update(checks)
        return result
    
    async def _verify_generic_document(self, text: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify generic document"""
        checks = {}
        
        # Basic content validation
        if len(text.strip()) > 100:
            checks['sufficient_content'] = True
        else:
            checks['sufficient_content'] = False
            result['issues'].append("Document appears to have insufficient readable content")
        
        # Look for business-related keywords
        business_keywords = ['company', 'business', 'firm', 'enterprise', 'corporation', 'ltd', 'pvt']
        found_business_keywords = [kw for kw in business_keywords if kw.lower() in text.lower()]
        
        if found_business_keywords:
            checks['business_context_found'] = True
        else:
            checks['business_context_found'] = False
        
        result['verification_checks'].update(checks)
        return result
    
    def _calculate_confidence_score(self, result: Dict[str, Any]) -> float:
        """Calculate overall confidence score based on verification checks"""
        checks = result.get('verification_checks', {})
        total_checks = len(checks)
        
        if total_checks == 0:
            return 0.0
        
        passed_checks = sum(1 for check in checks.values() if check)
        base_score = passed_checks / total_checks
        
        # Adjust based on issues
        issue_count = len(result.get('issues', []))
        issue_penalty = min(0.3, issue_count * 0.1)
        
        final_score = max(0.0, base_score - issue_penalty)
        return round(final_score, 2)

# Human-in-the-Loop workflow manager
class HITLWorkflowManager:
    def __init__(self):
        self.redis_client = redis_client
    
    async def create_workflow(self, supplier_id: str, created_by: str) -> ValidationWorkflow:
        """Create new validation workflow"""
        workflow_id = str(uuid.uuid4())
        
        workflow = ValidationWorkflow(
            id=workflow_id,
            supplier_id=supplier_id,
            current_step=ValidationStep.DOCUMENT_UPLOAD,
            status=SupplierStatus.PENDING,
            steps_completed=[],
            pending_actions=["Upload required documents"],
            approvals={},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Store in Redis for quick access
        await self._store_workflow(workflow)
        
        # Create workflow tasks
        await self._create_workflow_tasks(workflow)
        
        return workflow
    
    async def advance_workflow(self, workflow_id: str, decision: ValidationDecision, user_id: str, user_role: UserRole) -> ValidationWorkflow:
        """Advance workflow to next step based on decision"""
        workflow = await self._get_workflow(workflow_id)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Validate user permissions for current step
        if not self._validate_user_permissions(workflow.current_step, user_role):
            raise HTTPException(status_code=403, detail="Insufficient permissions for this workflow step")
        
        # Process decision
        if decision.decision == "approve":
            workflow = await self._approve_current_step(workflow, decision, user_id, user_role)
        elif decision.decision == "reject":
            workflow = await self._reject_workflow(workflow, decision, user_id)
        else:  # request_more_info
            workflow = await self._request_more_information(workflow, decision, user_id)
        
        # Update workflow
        workflow.updated_at = datetime.utcnow()
        await self._store_workflow(workflow)
        
        # Send notifications
        await self._send_workflow_notifications(workflow, decision, user_id)
        
        return workflow
    
    async def _approve_current_step(self, workflow: ValidationWorkflow, decision: ValidationDecision, user_id: str, user_role: UserRole) -> ValidationWorkflow:
        """Approve current step and advance workflow"""
        current_step = workflow.current_step
        
        # Record approval
        workflow.approvals[current_step.value] = {
            'approved_by': user_id,
            'approved_at': datetime.utcnow().isoformat(),
            'role': user_role.value,
            'comments': decision.comments
        }
        
        # Mark step as completed
        if current_step not in workflow.steps_completed:
            workflow.steps_completed.append(current_step)
        
        # Determine next step
        next_step, next_status = self._get_next_workflow_step(current_step, user_role)
        
        workflow.current_step = next_step
        workflow.status = next_status
        
        # Update pending actions
        workflow.pending_actions = self._get_pending_actions_for_step(next_step)
        
        return workflow
    
    async def _reject_workflow(self, workflow: ValidationWorkflow, decision: ValidationDecision, user_id: str) -> ValidationWorkflow:
        """Reject workflow"""
        workflow.status = SupplierStatus.REJECTED
        workflow.approvals['rejection'] = {
            'rejected_by': user_id,
            'rejected_at': datetime.utcnow().isoformat(),
            'reason': decision.comments,
            'risk_flags': decision.risk_flags or []
        }
        workflow.pending_actions = ["Supplier rejected - no further action required"]
        
        return workflow
    
    async def _request_more_information(self, workflow: ValidationWorkflow, decision: ValidationDecision, user_id: str) -> ValidationWorkflow:
        """Request more information from supplier"""
        workflow.status = SupplierStatus.DOCUMENTS_REQUIRED
        workflow.current_step = ValidationStep.DOCUMENT_UPLOAD
        
        # Add to approvals for tracking
        workflow.approvals[f'more_info_request_{len(workflow.approvals)}'] = {
            'requested_by': user_id,
            'requested_at': datetime.utcnow().isoformat(),
            'comments': decision.comments,
            'requested_documents': [doc.value for doc in (decision.requested_documents or [])]
        }
        
        # Update pending actions
        pending_docs = [doc.value for doc in (decision.requested_documents or [])]
        if pending_docs:
            workflow.pending_actions = [f"Upload missing document: {doc}" for doc in pending_docs]
        else:
            workflow.pending_actions = ["Provide additional information as requested"]
        
        return workflow
    
    def _get_next_workflow_step(self, current_step: ValidationStep, user_role: UserRole) -> tuple[ValidationStep, SupplierStatus]:
        """Determine next workflow step and status"""
        workflow_progression = {
            ValidationStep.DOCUMENT_UPLOAD: (ValidationStep.AUTOMATED_VERIFICATION, SupplierStatus.UNDER_REVIEW),
            ValidationStep.AUTOMATED_VERIFICATION: (ValidationStep.ANALYST_REVIEW, SupplierStatus.UNDER_REVIEW),
            ValidationStep.ANALYST_REVIEW: (ValidationStep.MANAGER_APPROVAL, SupplierStatus.MANAGER_REVIEW),
            ValidationStep.MANAGER_APPROVAL: (ValidationStep.COMPLIANCE_CHECK, SupplierStatus.COMPLIANCE_CHECK),
            ValidationStep.COMPLIANCE_CHECK: (ValidationStep.DIRECTOR_APPROVAL, SupplierStatus.DIRECTOR_APPROVAL),
            ValidationStep.DIRECTOR_APPROVAL: (ValidationStep.FINAL_APPROVAL, SupplierStatus.APPROVED),
            ValidationStep.FINAL_APPROVAL: (ValidationStep.FINAL_APPROVAL, SupplierStatus.APPROVED)
        }
        
        return workflow_progression.get(current_step, (current_step, SupplierStatus.UNDER_REVIEW))
    
    def _validate_user_permissions(self, step: ValidationStep, user_role: UserRole) -> bool:
        """Validate if user has permission for current workflow step"""
        permission_matrix = {
            ValidationStep.ANALYST_REVIEW: [UserRole.ANALYST, UserRole.MANAGER, UserRole.DIRECTOR, UserRole.ADMIN],
            ValidationStep.MANAGER_APPROVAL: [UserRole.MANAGER, UserRole.DIRECTOR, UserRole.ADMIN],
            ValidationStep.DIRECTOR_APPROVAL: [UserRole.DIRECTOR, UserRole.ADMIN],
            ValidationStep.COMPLIANCE_CHECK: [UserRole.ANALYST, UserRole.MANAGER, UserRole.DIRECTOR, UserRole.ADMIN],
            ValidationStep.FINAL_APPROVAL: [UserRole.DIRECTOR, UserRole.ADMIN]
        }
        
        allowed_roles = permission_matrix.get(step, [UserRole.ANALYST, UserRole.MANAGER, UserRole.DIRECTOR, UserRole.ADMIN])
        return user_role in allowed_roles
    
    def _get_pending_actions_for_step(self, step: ValidationStep) -> List[str]:
        """Get pending actions for workflow step"""
        action_map = {
            ValidationStep.DOCUMENT_UPLOAD: ["Upload required documents"],
            ValidationStep.AUTOMATED_VERIFICATION: ["Automated verification in progress"],
            ValidationStep.ANALYST_REVIEW: ["Pending analyst review"],
            ValidationStep.MANAGER_APPROVAL: ["Pending manager approval"],
            ValidationStep.DIRECTOR_APPROVAL: ["Pending director approval"],
            ValidationStep.COMPLIANCE_CHECK: ["Compliance verification in progress"],
            ValidationStep.FINAL_APPROVAL: ["Final approval processing"]
        }
        
        return action_map.get(step, ["Unknown step"])
    
    async def _store_workflow(self, workflow: ValidationWorkflow):
        """Store workflow in Redis"""
        workflow_data = asdict(workflow)
        # Convert datetime objects to ISO strings
        workflow_data['created_at'] = workflow.created_at.isoformat()
        workflow_data['updated_at'] = workflow.updated_at.isoformat()
        
        self.redis_client.setex(
            f"workflow:{workflow.id}",
            3600 * 24 * 30,  # 30 days
            json.dumps(workflow_data, default=str)
        )
    
    async def _get_workflow(self, workflow_id: str) -> Optional[ValidationWorkflow]:
        """Get workflow from Redis"""
        workflow_data = self.redis_client.get(f"workflow:{workflow_id}")
        if not workflow_data:
            return None
        
        data = json.loads(workflow_data)
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        return ValidationWorkflow(**data)
    
    async def _create_workflow_tasks(self, workflow: ValidationWorkflow):
        """Create workflow tasks and notifications"""
        # This would integrate with task management system
        pass
    
    async def _send_workflow_notifications(self, workflow: ValidationWorkflow, decision: ValidationDecision, user_id: str):
        """Send workflow notifications"""
        # This would integrate with notification system
        pass

# Initialize global instances
risk_engine = SupplierRiskAssessmentEngine()
doc_verification_engine = DocumentVerificationEngine()
workflow_manager = HITLWorkflowManager()

# Initialize Brain API integration
from brain_api_integration import initialize_integrations, notify_status_change, handle_supplier_approval

# Database operations
async def get_db_connection():
    """Get database connection"""
    return await asyncpg.connect(DATABASE_URL)

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    # This would integrate with the actual authentication system
    # For now, return a mock user
    return {
        "id": "user-123",
        "role": UserRole.ANALYST,
        "email": "analyst@bizosaas.com"
    }

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Supplier Validation Workflow [P9]",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Supplier validation dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_redirect(request: Request):
    """Dashboard redirect"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.post("/suppliers/register")
async def register_supplier(
    supplier_data: SupplierRegistration,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """Register new supplier and initiate validation workflow"""
    try:
        supplier_id = str(uuid.uuid4())
        
        # Create supplier profile
        supplier_profile = SupplierProfile(
            id=supplier_id,
            company_name=supplier_data.company_name,
            contact_person=supplier_data.contact_person,
            email=supplier_data.email,
            phone=supplier_data.phone,
            address=supplier_data.address,
            city=supplier_data.city,
            state=supplier_data.state,
            country=supplier_data.country,
            pincode=supplier_data.pincode,
            website=supplier_data.website,
            business_type=supplier_data.business_type,
            industry=supplier_data.industry,
            products_offered=supplier_data.products_offered,
            annual_revenue=supplier_data.annual_revenue,
            employee_count=supplier_data.employee_count,
            gst_number=supplier_data.gst_number,
            pan_number=supplier_data.pan_number,
            status=SupplierStatus.PENDING,
            risk_level=RiskLevel.MEDIUM,
            risk_score=50.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=current_user["id"]
        )
        
        # Store supplier in database
        conn = await get_db_connection()
        try:
            await conn.execute("""
                INSERT INTO suppliers (
                    id, company_name, contact_person, email, phone, address, city, state, country, pincode,
                    website, business_type, industry, products_offered, annual_revenue, employee_count,
                    gst_number, pan_number, status, risk_level, risk_score, created_at, updated_at, created_by
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24
                )
            """, 
                supplier_id, supplier_profile.company_name, supplier_profile.contact_person,
                supplier_profile.email, supplier_profile.phone, supplier_profile.address,
                supplier_profile.city, supplier_profile.state, supplier_profile.country,
                supplier_profile.pincode, supplier_profile.website, supplier_profile.business_type,
                supplier_profile.industry, json.dumps(supplier_profile.products_offered),
                supplier_profile.annual_revenue, supplier_profile.employee_count,
                supplier_profile.gst_number, supplier_profile.pan_number, supplier_profile.status.value,
                supplier_profile.risk_level.value, supplier_profile.risk_score,
                supplier_profile.created_at, supplier_profile.updated_at, supplier_profile.created_by
            )
        finally:
            await conn.close()
        
        # Create validation workflow
        workflow = await workflow_manager.create_workflow(supplier_id, current_user["id"])
        
        # Perform initial risk assessment in background
        background_tasks.add_task(perform_initial_risk_assessment, supplier_id)
        
        # Notify Brain API of new supplier registration
        background_tasks.add_task(notify_status_change, supplier_id, "new", "pending", {"workflow_id": workflow.id})
        
        return {
            "supplier_id": supplier_id,
            "workflow_id": workflow.id,
            "status": supplier_profile.status,
            "message": "Supplier registered successfully. Please upload required documents.",
            "required_documents": [
                DocumentType.BUSINESS_LICENSE,
                DocumentType.GST_CERTIFICATE,
                DocumentType.PAN_CARD
            ]
        }
        
    except Exception as e:
        logger.error(f"Error registering supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to register supplier: {str(e)}")

@app.post("/suppliers/{supplier_id}/documents/upload")
async def upload_document(
    supplier_id: str,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    current_user = Depends(get_current_user)
):
    """Upload document for supplier validation"""
    try:
        # Validate file
        if file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        if not doc_verification_engine._validate_file_format(file.filename):
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Read file content
        file_content = await file.read()
        
        # Generate unique filename
        file_extension = Path(file.filename).suffix
        unique_filename = f"{supplier_id}_{document_type.value}_{uuid.uuid4()}{file_extension}"
        
        # Store file (in production, would use S3 or similar)
        upload_dir = Path("/tmp/supplier_documents")
        upload_dir.mkdir(exist_ok=True)
        file_path = upload_dir / unique_filename
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Create document record
        document_id = str(uuid.uuid4())
        document = Document(
            id=document_id,
            supplier_id=supplier_id,
            document_type=document_type,
            file_name=file.filename,
            file_path=str(file_path),
            file_size=file.size,
            content_type=file.content_type,
            upload_date=datetime.utcnow(),
            uploaded_by=current_user["id"],
            verification_status="pending"
        )
        
        # Store document metadata in database
        conn = await get_db_connection()
        try:
            await conn.execute("""
                INSERT INTO supplier_documents (
                    id, supplier_id, document_type, file_name, file_path, file_size,
                    content_type, upload_date, uploaded_by, verification_status
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            """, 
                document_id, supplier_id, document_type.value, file.filename,
                str(file_path), file.size, file.content_type, document.upload_date,
                current_user["id"], "pending"
            )
        finally:
            await conn.close()
        
        # Perform document verification
        verification_result = await doc_verification_engine.verify_document(document, file_content)
        
        # Update document with verification results
        conn = await get_db_connection()
        try:
            await conn.execute("""
                UPDATE supplier_documents 
                SET verification_status = $1, extracted_data = $2, ai_analysis = $3
                WHERE id = $4
            """, 
                verification_result['status'],
                json.dumps(verification_result['extracted_data']),
                json.dumps(verification_result),
                document_id
            )
        finally:
            await conn.close()
        
        return {
            "document_id": document_id,
            "verification_status": verification_result['status'],
            "confidence_score": verification_result['confidence_score'],
            "extracted_data": verification_result['extracted_data'],
            "issues": verification_result['issues']
        }
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")

@app.get("/suppliers/{supplier_id}")
async def get_supplier(
    supplier_id: str,
    current_user = Depends(get_current_user)
):
    """Get supplier details"""
    try:
        conn = await get_db_connection()
        try:
            # Get supplier data
            supplier_row = await conn.fetchrow("""
                SELECT * FROM suppliers WHERE id = $1
            """, supplier_id)
            
            if not supplier_row:
                raise HTTPException(status_code=404, detail="Supplier not found")
            
            # Get documents
            document_rows = await conn.fetch("""
                SELECT * FROM supplier_documents WHERE supplier_id = $1 ORDER BY upload_date DESC
            """, supplier_id)
            
            # Get workflow
            workflow_row = await conn.fetchrow("""
                SELECT * FROM supplier_workflows WHERE supplier_id = $1 ORDER BY created_at DESC LIMIT 1
            """, supplier_id)
            
        finally:
            await conn.close()
        
        # Format response
        supplier_data = dict(supplier_row)
        supplier_data['products_offered'] = json.loads(supplier_data['products_offered']) if supplier_data['products_offered'] else []
        
        documents = []
        for doc_row in document_rows:
            doc_data = dict(doc_row)
            doc_data['extracted_data'] = json.loads(doc_data['extracted_data']) if doc_data['extracted_data'] else {}
            doc_data['ai_analysis'] = json.loads(doc_data['ai_analysis']) if doc_data['ai_analysis'] else {}
            documents.append(doc_data)
        
        workflow_data = dict(workflow_row) if workflow_row else None
        
        return {
            "supplier": supplier_data,
            "documents": documents,
            "workflow": workflow_data
        }
        
    except Exception as e:
        logger.error(f"Error getting supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get supplier: {str(e)}")

@app.post("/suppliers/{supplier_id}/review")
async def review_supplier(
    supplier_id: str,
    decision: ValidationDecision,
    current_user = Depends(get_current_user)
):
    """Submit review decision for supplier"""
    try:
        # Get current workflow
        conn = await get_db_connection()
        try:
            workflow_row = await conn.fetchrow("""
                SELECT * FROM supplier_workflows WHERE supplier_id = $1 ORDER BY created_at DESC LIMIT 1
            """, supplier_id)
            
            if not workflow_row:
                raise HTTPException(status_code=404, detail="No active workflow found for supplier")
            
        finally:
            await conn.close()
        
        workflow_id = workflow_row['id']
        user_role = UserRole(current_user["role"])
        
        # Advance workflow
        updated_workflow = await workflow_manager.advance_workflow(
            workflow_id, decision, current_user["id"], user_role
        )
        
        # Get old status for notification
        old_status = workflow_row['status']
        
        # Update supplier status in database
        conn = await get_db_connection()
        try:
            await conn.execute("""
                UPDATE suppliers SET status = $1, updated_at = $2 WHERE id = $3
            """, updated_workflow.status.value, datetime.utcnow(), supplier_id)
            
            # Notify Brain API of status change
            await notify_status_change(supplier_id, old_status, updated_workflow.status.value, {
                "decision": decision.decision,
                "current_step": updated_workflow.current_step.value,
                "reviewer": current_user["id"]
            })
            
            # Store workflow state
            await conn.execute("""
                UPDATE supplier_workflows 
                SET current_step = $1, status = $2, steps_completed = $3, 
                    pending_actions = $4, approvals = $5, updated_at = $6
                WHERE id = $7
            """, 
                updated_workflow.current_step.value,
                updated_workflow.status.value,
                json.dumps([step.value for step in updated_workflow.steps_completed]),
                json.dumps(updated_workflow.pending_actions),
                json.dumps(updated_workflow.approvals),
                updated_workflow.updated_at,
                workflow_id
            )
        finally:
            await conn.close()
        
        return {
            "workflow_id": updated_workflow.id,
            "current_step": updated_workflow.current_step,
            "status": updated_workflow.status,
            "pending_actions": updated_workflow.pending_actions,
            "message": f"Review decision '{decision.decision}' processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error reviewing supplier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process review: {str(e)}")

@app.get("/suppliers/{supplier_id}/risk-assessment")
async def get_risk_assessment(
    supplier_id: str,
    current_user = Depends(get_current_user)
):
    """Get AI-powered risk assessment for supplier"""
    try:
        conn = await get_db_connection()
        try:
            # Get supplier data
            supplier_row = await conn.fetchrow("""
                SELECT * FROM suppliers WHERE id = $1
            """, supplier_id)
            
            if not supplier_row:
                raise HTTPException(status_code=404, detail="Supplier not found")
            
            # Get documents
            document_rows = await conn.fetch("""
                SELECT * FROM supplier_documents WHERE supplier_id = $1
            """, supplier_id)
            
        finally:
            await conn.close()
        
        # Convert to required format
        supplier_data = dict(supplier_row)
        supplier_data['products_offered'] = json.loads(supplier_data['products_offered']) if supplier_data['products_offered'] else []
        
        documents = []
        for doc_row in document_rows:
            doc_data = dict(doc_row)
            doc_data['extracted_data'] = json.loads(doc_data['extracted_data']) if doc_data['extracted_data'] else {}
            doc_data['ai_analysis'] = json.loads(doc_data['ai_analysis']) if doc_data['ai_analysis'] else {}
            
            documents.append(Document(
                id=doc_data['id'],
                supplier_id=doc_data['supplier_id'],
                document_type=DocumentType(doc_data['document_type']),
                file_name=doc_data['file_name'],
                file_path=doc_data['file_path'],
                file_size=doc_data['file_size'],
                content_type=doc_data['content_type'],
                upload_date=doc_data['upload_date'],
                uploaded_by=doc_data['uploaded_by'],
                verification_status=doc_data['verification_status'],
                extracted_data=doc_data['extracted_data'],
                ai_analysis=doc_data['ai_analysis']
            ))
        
        # Perform risk assessment
        risk_assessment = await risk_engine.assess_supplier_risk(supplier_data, documents)
        
        # Update supplier with risk assessment
        conn = await get_db_connection()
        try:
            await conn.execute("""
                UPDATE suppliers 
                SET risk_level = $1, risk_score = $2, updated_at = $3
                WHERE id = $4
            """, 
                risk_assessment.risk_level.value,
                risk_assessment.risk_score,
                datetime.utcnow(),
                supplier_id
            )
        finally:
            await conn.close()
        
        return risk_assessment
        
    except Exception as e:
        logger.error(f"Error getting risk assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get risk assessment: {str(e)}")

@app.get("/suppliers")
async def list_suppliers(
    status: Optional[SupplierStatus] = None,
    risk_level: Optional[RiskLevel] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user)
):
    """List suppliers with filtering and pagination"""
    try:
        offset = (page - 1) * page_size
        
        # Build query
        where_clauses = []
        params = []
        param_count = 0
        
        if status:
            param_count += 1
            where_clauses.append(f"status = ${param_count}")
            params.append(status.value)
        
        if risk_level:
            param_count += 1
            where_clauses.append(f"risk_level = ${param_count}")
            params.append(risk_level.value)
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        # Add pagination params
        param_count += 1
        limit_param = f"${param_count}"
        params.append(page_size)
        
        param_count += 1
        offset_param = f"${param_count}"
        params.append(offset)
        
        conn = await get_db_connection()
        try:
            # Get suppliers
            suppliers_query = f"""
                SELECT * FROM suppliers 
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT {limit_param} OFFSET {offset_param}
            """
            
            supplier_rows = await conn.fetch(suppliers_query, *params)
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM suppliers WHERE {where_clause}"
            total_count = await conn.fetchval(count_query, *params[:-2])  # Exclude limit and offset params
            
        finally:
            await conn.close()
        
        # Format response
        suppliers = []
        for row in supplier_rows:
            supplier_data = dict(row)
            supplier_data['products_offered'] = json.loads(supplier_data['products_offered']) if supplier_data['products_offered'] else []
            suppliers.append(supplier_data)
        
        return {
            "suppliers": suppliers,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size
            }
        }
        
    except Exception as e:
        logger.error(f"Error listing suppliers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list suppliers: {str(e)}")

@app.get("/workflows/{workflow_id}")
async def get_workflow(
    workflow_id: str,
    current_user = Depends(get_current_user)
):
    """Get workflow details"""
    try:
        workflow = await workflow_manager._get_workflow(workflow_id)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return {
            "id": workflow.id,
            "supplier_id": workflow.supplier_id,
            "current_step": workflow.current_step,
            "status": workflow.status,
            "steps_completed": workflow.steps_completed,
            "pending_actions": workflow.pending_actions,
            "approvals": workflow.approvals,
            "created_at": workflow.created_at.isoformat(),
            "updated_at": workflow.updated_at.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")

@app.get("/dashboard/analytics")
async def get_dashboard_analytics(
    current_user = Depends(get_current_user)
):
    """Get dashboard analytics for supplier validation"""
    try:
        conn = await get_db_connection()
        try:
            # Get supplier counts by status
            status_counts = await conn.fetch("""
                SELECT status, COUNT(*) as count 
                FROM suppliers 
                GROUP BY status
            """)
            
            # Get risk level distribution
            risk_counts = await conn.fetch("""
                SELECT risk_level, COUNT(*) as count 
                FROM suppliers 
                GROUP BY risk_level
            """)
            
            # Get recent activity
            recent_suppliers = await conn.fetch("""
                SELECT id, company_name, status, created_at, risk_level, risk_score
                FROM suppliers 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            
            # Get approval metrics
            workflow_stats = await conn.fetch("""
                SELECT 
                    current_step,
                    COUNT(*) as count,
                    AVG(EXTRACT(EPOCH FROM (updated_at - created_at))/3600) as avg_hours
                FROM supplier_workflows 
                GROUP BY current_step
            """)
            
        finally:
            await conn.close()
        
        # Format response
        status_distribution = {row['status']: row['count'] for row in status_counts}
        risk_distribution = {row['risk_level']: row['count'] for row in risk_counts}
        
        recent_activity = []
        for row in recent_suppliers:
            supplier_data = dict(row)
            recent_activity.append(supplier_data)
        
        workflow_metrics = {}
        for row in workflow_stats:
            workflow_metrics[row['current_step']] = {
                'count': row['count'],
                'avg_processing_hours': round(row['avg_hours'], 2) if row['avg_hours'] else 0
            }
        
        return {
            "summary": {
                "total_suppliers": sum(status_distribution.values()),
                "pending_review": status_distribution.get('under_review', 0) + status_distribution.get('manager_review', 0),
                "approved_suppliers": status_distribution.get('approved', 0),
                "rejected_suppliers": status_distribution.get('rejected', 0)
            },
            "status_distribution": status_distribution,
            "risk_distribution": risk_distribution,
            "recent_activity": recent_activity,
            "workflow_metrics": workflow_metrics
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@app.post("/suppliers/{supplier_id}/validate-comprehensive")
async def validate_supplier_comprehensive(
    supplier_id: str,
    current_user = Depends(get_current_user)
):
    """Perform comprehensive validation of supplier using enhanced validation engine"""
    try:
        from validation_engine import ComprehensiveSupplierValidator
        
        # Get supplier data
        conn = await get_db_connection()
        try:
            supplier_row = await conn.fetchrow("SELECT * FROM suppliers WHERE id = $1", supplier_id)
            if not supplier_row:
                raise HTTPException(status_code=404, detail="Supplier not found")
            
        finally:
            await conn.close()
        
        # Convert to dict and prepare for validation
        supplier_data = dict(supplier_row)
        supplier_data['products_offered'] = json.loads(supplier_data['products_offered']) if supplier_data['products_offered'] else []
        
        # Perform comprehensive validation
        validator = ComprehensiveSupplierValidator()
        validation_results = await validator.validate_supplier_comprehensively(supplier_data)
        overall_score, issues, recommendations = validator.calculate_overall_validation_score(validation_results)
        
        # Store validation results
        conn = await get_db_connection()
        try:
            await conn.execute("""
                INSERT INTO supplier_validation_results (
                    supplier_id, validation_type, results, overall_score, issues, recommendations, validated_by, validated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, 
                supplier_id, 'comprehensive', json.dumps({k: v.__dict__ for k, v in validation_results.items()}, default=str),
                overall_score, json.dumps(issues), json.dumps(recommendations), current_user["id"], datetime.utcnow()
            )
        except:
            # Table might not exist, create it
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS supplier_validation_results (
                    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
                    supplier_id VARCHAR(36) NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
                    validation_type VARCHAR(50) NOT NULL,
                    results JSONB NOT NULL,
                    overall_score DECIMAL(5,2) NOT NULL,
                    issues JSONB DEFAULT '[]',
                    recommendations JSONB DEFAULT '[]',
                    validated_by VARCHAR(36) NOT NULL,
                    validated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                )
            """)
            # Try insert again
            await conn.execute("""
                INSERT INTO supplier_validation_results (
                    supplier_id, validation_type, results, overall_score, issues, recommendations, validated_by, validated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, 
                supplier_id, 'comprehensive', json.dumps({k: v.__dict__ for k, v in validation_results.items()}, default=str),
                overall_score, json.dumps(issues), json.dumps(recommendations), current_user["id"], datetime.utcnow()
            )
        finally:
            await conn.close()
        
        return {
            "supplier_id": supplier_id,
            "overall_score": overall_score,
            "validation_results": validation_results,
            "issues": issues,
            "recommendations": recommendations,
            "validation_summary": {
                "total_validations": len(validation_results),
                "passed_validations": sum(1 for result in validation_results.values() if result.is_valid),
                "confidence_level": "High" if overall_score >= 0.8 else "Medium" if overall_score >= 0.6 else "Low"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive validation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.get("/suppliers/{supplier_id}/workflow-history")
async def get_workflow_history(
    supplier_id: str,
    current_user = Depends(get_current_user)
):
    """Get complete workflow history for a supplier"""
    try:
        conn = await get_db_connection()
        try:
            # Get workflow history
            workflows = await conn.fetch("""
                SELECT * FROM supplier_workflows 
                WHERE supplier_id = $1 
                ORDER BY created_at DESC
            """, supplier_id)
            
            # Get audit log
            audit_logs = await conn.fetch("""
                SELECT * FROM supplier_audit_log 
                WHERE supplier_id = $1 
                ORDER BY timestamp DESC
                LIMIT 50
            """, supplier_id)
            
            # Get validation results
            validation_results = await conn.fetch("""
                SELECT * FROM supplier_validation_results 
                WHERE supplier_id = $1 
                ORDER BY validated_at DESC
            """, supplier_id)
            
        finally:
            await conn.close()
        
        # Format response
        workflow_history = []
        for workflow in workflows:
            workflow_data = dict(workflow)
            workflow_data['steps_completed'] = json.loads(workflow_data['steps_completed']) if workflow_data['steps_completed'] else []
            workflow_data['pending_actions'] = json.loads(workflow_data['pending_actions']) if workflow_data['pending_actions'] else []
            workflow_data['approvals'] = json.loads(workflow_data['approvals']) if workflow_data['approvals'] else {}
            workflow_history.append(workflow_data)
        
        audit_history = []
        for log in audit_logs:
            log_data = dict(log)
            log_data['details'] = json.loads(log_data['details']) if log_data['details'] else {}
            audit_history.append(log_data)
        
        validation_history = []
        for result in validation_results:
            result_data = dict(result)
            result_data['results'] = json.loads(result_data['results']) if result_data['results'] else {}
            result_data['issues'] = json.loads(result_data['issues']) if result_data['issues'] else []
            result_data['recommendations'] = json.loads(result_data['recommendations']) if result_data['recommendations'] else []
            validation_history.append(result_data)
        
        return {
            "supplier_id": supplier_id,
            "workflow_history": workflow_history,
            "audit_history": audit_history,
            "validation_history": validation_history
        }
        
    except Exception as e:
        logger.error(f"Error getting workflow history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow history: {str(e)}")

@app.post("/suppliers/bulk-action")
async def bulk_supplier_action(
    action: str,
    supplier_ids: List[str],
    comments: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Perform bulk actions on multiple suppliers"""
    try:
        if action not in ['approve', 'reject', 'assign_analyst', 'request_documents']:
            raise HTTPException(status_code=400, detail="Invalid bulk action")
        
        results = []
        conn = await get_db_connection()
        try:
            for supplier_id in supplier_ids:
                try:
                    # Get supplier
                    supplier = await conn.fetchrow("SELECT * FROM suppliers WHERE id = $1", supplier_id)
                    if not supplier:
                        results.append({
                            "supplier_id": supplier_id,
                            "status": "error",
                            "message": "Supplier not found"
                        })
                        continue
                    
                    # Perform action based on type
                    if action == 'approve':
                        await conn.execute("""
                            UPDATE suppliers SET status = 'approved', updated_at = $1 WHERE id = $2
                        """, datetime.utcnow(), supplier_id)
                        
                    elif action == 'reject':
                        await conn.execute("""
                            UPDATE suppliers SET status = 'rejected', updated_at = $1 WHERE id = $2
                        """, datetime.utcnow(), supplier_id)
                    
                    elif action == 'assign_analyst':
                        await conn.execute("""
                            UPDATE suppliers SET assigned_analyst = $1, updated_at = $2 WHERE id = $3
                        """, current_user["id"], datetime.utcnow(), supplier_id)
                    
                    # Log the action
                    await conn.execute("""
                        INSERT INTO supplier_audit_log (
                            supplier_id, action, performed_by, timestamp, details
                        ) VALUES ($1, $2, $3, $4, $5)
                    """, 
                        supplier_id, f'bulk_{action}', current_user["id"], datetime.utcnow(),
                        json.dumps({"comments": comments, "bulk_operation": True})
                    )
                    
                    results.append({
                        "supplier_id": supplier_id,
                        "status": "success",
                        "message": f"Action {action} completed successfully"
                    })
                    
                except Exception as e:
                    results.append({
                        "supplier_id": supplier_id,
                        "status": "error",
                        "message": str(e)
                    })
        
        finally:
            await conn.close()
        
        success_count = sum(1 for r in results if r["status"] == "success")
        
        return {
            "action": action,
            "total_suppliers": len(supplier_ids),
            "successful": success_count,
            "failed": len(supplier_ids) - success_count,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in bulk action: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bulk action failed: {str(e)}")

# Background task functions
async def perform_initial_risk_assessment(supplier_id: str):
    """Perform initial risk assessment for new supplier"""
    try:
        conn = await get_db_connection()
        try:
            # Get supplier data
            supplier_row = await conn.fetchrow("SELECT * FROM suppliers WHERE id = $1", supplier_id)
            if not supplier_row:
                return
            
            supplier_data = dict(supplier_row)
            supplier_data['products_offered'] = json.loads(supplier_data['products_offered']) if supplier_data['products_offered'] else []
            
            # Get documents (may be empty for initial assessment)
            document_rows = await conn.fetch("SELECT * FROM supplier_documents WHERE supplier_id = $1", supplier_id)
            documents = [Document(**dict(row)) for row in document_rows]
            
            # Perform risk assessment
            risk_assessment = await risk_engine.assess_supplier_risk(supplier_data, documents)
            
            # Update supplier with risk assessment
            await conn.execute("""
                UPDATE suppliers 
                SET risk_level = $1, risk_score = $2, updated_at = $3
                WHERE id = $4
            """, 
                risk_assessment.risk_level.value,
                risk_assessment.risk_score,
                datetime.utcnow(),
                supplier_id
            )
            
            logger.info(f"Initial risk assessment completed for supplier {supplier_id}: {risk_assessment.risk_level.value}")
            
        finally:
            await conn.close()
            
    except Exception as e:
        logger.error(f"Error in initial risk assessment for supplier {supplier_id}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    # Create database tables
    asyncio.run(create_database_tables())
    
    logger.info("Supplier Validation Workflow [P9] starting on port 8027")
    logger.info("Dashboard available at: http://localhost:8027/dashboard")
    logger.info("API Documentation: http://localhost:8027/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8027,
        reload=True,
        log_level="info"
    )

async def create_database_tables():
    """Create database tables for supplier validation"""
    conn = await get_db_connection()
    try:
        # Create suppliers table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id VARCHAR(36) PRIMARY KEY,
                company_name VARCHAR(200) NOT NULL,
                contact_person VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address TEXT NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL DEFAULT 'India',
                pincode VARCHAR(10) NOT NULL,
                website VARCHAR(500),
                business_type VARCHAR(100) NOT NULL,
                industry VARCHAR(100) NOT NULL,
                products_offered JSONB NOT NULL,
                annual_revenue DECIMAL(15,2),
                employee_count INTEGER,
                gst_number VARCHAR(15),
                pan_number VARCHAR(10),
                status VARCHAR(50) NOT NULL DEFAULT 'pending',
                risk_level VARCHAR(20) NOT NULL DEFAULT 'medium',
                risk_score DECIMAL(5,2) NOT NULL DEFAULT 50.0,
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                created_by VARCHAR(36) NOT NULL,
                assigned_analyst VARCHAR(36),
                assigned_manager VARCHAR(36)
            )
        """)
        
        # Create supplier_documents table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS supplier_documents (
                id VARCHAR(36) PRIMARY KEY,
                supplier_id VARCHAR(36) NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
                document_type VARCHAR(50) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                file_size INTEGER NOT NULL,
                content_type VARCHAR(100) NOT NULL,
                upload_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                uploaded_by VARCHAR(36) NOT NULL,
                verification_status VARCHAR(50) NOT NULL DEFAULT 'pending',
                extracted_data JSONB,
                ai_analysis JSONB
            )
        """)
        
        # Create supplier_workflows table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS supplier_workflows (
                id VARCHAR(36) PRIMARY KEY,
                supplier_id VARCHAR(36) NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
                current_step VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL,
                steps_completed JSONB NOT NULL DEFAULT '[]',
                pending_actions JSONB NOT NULL DEFAULT '[]',
                approvals JSONB NOT NULL DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
            )
        """)
        
        # Create indexes
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_suppliers_status ON suppliers(status)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_suppliers_risk_level ON suppliers(risk_level)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_suppliers_created_at ON suppliers(created_at)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_supplier_documents_supplier_id ON supplier_documents(supplier_id)")
        await conn.execute("CREATE INDEX IF NOT EXISTS idx_supplier_workflows_supplier_id ON supplier_workflows(supplier_id)")
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
    finally:
        await conn.close()

@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    # Create database tables
    await create_database_tables()
    
    # Initialize Brain API integration
    try:
        await initialize_integrations()
        logger.info("Brain API integration initialized successfully")
    except Exception as e:
        logger.warning(f"Brain API integration failed: {str(e)} - continuing in standalone mode")
    
    logger.info("Supplier Validation Workflow [P9] startup complete")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Supplier Validation Workflow [P9] starting on port 8027")
    logger.info("Dashboard available at: http://localhost:8027/dashboard")
    logger.info("API Documentation: http://localhost:8027/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8027,
        reload=True,
        log_level="info"
    )