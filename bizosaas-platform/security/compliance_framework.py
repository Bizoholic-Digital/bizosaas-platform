"""
Comprehensive Security and Compliance Framework for BizOSaaS Platform
Implements GDPR compliance, audit logging, and AI-powered threat detection
"""

import asyncio
import json
import structlog
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Set, Union
from uuid import UUID, uuid4
from enum import Enum
from dataclasses import dataclass, field, asdict
from pydantic import BaseModel, Field

import asyncpg
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import ipaddress
import re
from cryptography.fernet import Fernet
import jwt

from enhanced_tenant_context import EnhancedTenantContext, PlatformType
from shared.rls_manager import RLSManager

logger = structlog.get_logger(__name__)


class ComplianceStandard(str, Enum):
    """Supported compliance standards"""
    GDPR = "gdpr"
    CCPA = "ccpa"
    PIPEDA = "pipeda"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    HIPAA = "hipaa"


class DataClassification(str, Enum):
    """Data classification levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PERSONAL = "personal"
    SENSITIVE_PERSONAL = "sensitive_personal"


class SecurityEventType(str, Enum):
    """Types of security events"""
    # Authentication events
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    TOKEN_ISSUED = "token_issued"
    TOKEN_EXPIRED = "token_expired"

    # Access control events
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    PERMISSION_CHANGE = "permission_change"

    # Data events
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    DATA_DELETION = "data_deletion"
    DATA_BREACH = "data_breach"
    PERSONAL_DATA_ACCESS = "personal_data_access"

    # System events
    SYSTEM_ERROR = "system_error"
    CONFIGURATION_CHANGE = "configuration_change"
    BACKUP_CREATED = "backup_created"
    BACKUP_RESTORED = "backup_restored"

    # Threat detection
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    BRUTE_FORCE_ATTACK = "brute_force_attack"
    SQL_INJECTION_ATTEMPT = "sql_injection_attempt"
    XSS_ATTEMPT = "xss_attempt"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    ANOMALOUS_BEHAVIOR = "anomalous_behavior"

    # AI-specific events
    AI_MODEL_ACCESS = "ai_model_access"
    AI_BIAS_DETECTED = "ai_bias_detected"
    AI_PROMPT_INJECTION = "ai_prompt_injection"
    AI_DATA_LEAKAGE = "ai_data_leakage"


class ThreatLevel(str, Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DataSubjectRight(str, Enum):
    """GDPR data subject rights"""
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    RESTRICT_PROCESSING = "restrict_processing"
    DATA_PORTABILITY = "data_portability"
    OBJECT_PROCESSING = "object_processing"
    WITHDRAW_CONSENT = "withdraw_consent"


@dataclass
class SecurityEvent:
    """Security event data structure"""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: SecurityEventType = SecurityEventType.SYSTEM_ERROR
    severity: ThreatLevel = ThreatLevel.LOW
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Context
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    platform: Optional[PlatformType] = None

    # Event details
    description: str = ""
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None
    request_method: Optional[str] = None

    # Additional data
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    # Detection and response
    detected_by: str = "system"
    response_action: Optional[str] = None
    resolution_status: str = "open"


@dataclass
class DataSubjectRequest:
    """GDPR data subject request"""
    request_id: str = field(default_factory=lambda: str(uuid4()))
    request_type: DataSubjectRight = DataSubjectRight.ACCESS
    tenant_id: str = ""
    data_subject_id: str = ""

    # Request details
    description: str = ""
    requested_data_categories: List[str] = field(default_factory=list)
    legal_basis: Optional[str] = None

    # Processing
    status: str = "pending"  # pending, in_progress, completed, rejected
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30))
    completed_at: Optional[datetime] = None

    # Response
    response_data: Optional[Dict[str, Any]] = None
    response_format: str = "json"  # json, csv, pdf

    # Verification
    identity_verified: bool = False
    verification_method: Optional[str] = None
    verification_timestamp: Optional[datetime] = None


class PersonalDataProcessor:
    """Handles personal data processing in compliance with GDPR"""

    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)
        self.logger = logger.bind(component="personal_data_processor")

    def encrypt_personal_data(self, data: str) -> str:
        """Encrypt personal data"""
        try:
            encrypted = self.cipher.encrypt(data.encode())
            return encrypted.decode()
        except Exception as e:
            self.logger.error("Failed to encrypt personal data", error=str(e))
            raise

    def decrypt_personal_data(self, encrypted_data: str) -> str:
        """Decrypt personal data"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except Exception as e:
            self.logger.error("Failed to decrypt personal data", error=str(e))
            raise

    def pseudonymize_data(self, data: str, salt: str = "") -> str:
        """Pseudonymize personal data using consistent hashing"""
        hasher = hashlib.sha256()
        hasher.update((data + salt).encode())
        return hasher.hexdigest()

    def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize personal data by removing identifiers"""
        anonymized = data.copy()

        # Remove direct identifiers
        direct_identifiers = [
            'email', 'phone', 'name', 'address', 'ssn', 'passport',
            'driver_license', 'credit_card', 'bank_account'
        ]

        for identifier in direct_identifiers:
            if identifier in anonymized:
                del anonymized[identifier]

        # Generalize quasi-identifiers
        if 'age' in anonymized:
            age = anonymized['age']
            if isinstance(age, (int, float)):
                # Group into age ranges
                if age < 18:
                    anonymized['age_group'] = 'under_18'
                elif age < 30:
                    anonymized['age_group'] = '18_29'
                elif age < 50:
                    anonymized['age_group'] = '30_49'
                else:
                    anonymized['age_group'] = '50_plus'
                del anonymized['age']

        if 'location' in anonymized:
            # Keep only country-level information
            location = anonymized['location']
            if isinstance(location, dict) and 'country' in location:
                anonymized['location'] = {'country': location['country']}
            elif isinstance(location, str):
                # Extract country if possible
                anonymized['location'] = {'region': 'unknown'}

        return anonymized


class ThreatDetectionEngine:
    """AI-powered threat detection system"""

    def __init__(self, rls_manager: RLSManager):
        self.rls_manager = rls_manager
        self.logger = logger.bind(component="threat_detection")

        # Threat patterns
        self.sql_injection_patterns = [
            r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
            r"((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))",
            r"\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
            r"((\%27)|(\'))union",
            r"exec(\s|\+)+(s|x)p\w+",
            r"UNION[^a-zA-Z]*SELECT",
            r"SELECT[^a-zA-Z]*FROM",
            r"INSERT[^a-zA-Z]*INTO",
            r"UPDATE[^a-zA-Z]*SET",
            r"DELETE[^a-zA-Z]*FROM"
        ]

        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
            r"<object[^>]*>.*?</object>",
            r"<embed[^>]*>.*?</embed>",
            r"<link[^>]*>",
            r"<meta[^>]*>"
        ]

        # Rate limiting tracking
        self.request_counts: Dict[str, Dict[str, int]] = {}
        self.failed_login_attempts: Dict[str, List[datetime]] = {}

        # Behavioral baselines
        self.user_behavior_baselines: Dict[str, Dict[str, Any]] = {}

    async def analyze_request(
        self,
        request: Request,
        tenant_context: Optional[EnhancedTenantContext] = None
    ) -> List[SecurityEvent]:
        """Analyze incoming request for threats"""
        events = []

        # Get request details
        source_ip = self.get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")
        endpoint = str(request.url.path)
        method = request.method

        # Check for SQL injection
        if await self.detect_sql_injection(request):
            events.append(SecurityEvent(
                event_type=SecurityEventType.SQL_INJECTION_ATTEMPT,
                severity=ThreatLevel.HIGH,
                description=f"SQL injection attempt detected on {endpoint}",
                source_ip=source_ip,
                user_agent=user_agent,
                endpoint=endpoint,
                request_method=method,
                tenant_id=tenant_context.tenant_id if tenant_context else None,
                metadata={"patterns_matched": "sql_injection"}
            ))

        # Check for XSS
        if await self.detect_xss(request):
            events.append(SecurityEvent(
                event_type=SecurityEventType.XSS_ATTEMPT,
                severity=ThreatLevel.HIGH,
                description=f"XSS attempt detected on {endpoint}",
                source_ip=source_ip,
                user_agent=user_agent,
                endpoint=endpoint,
                request_method=method,
                tenant_id=tenant_context.tenant_id if tenant_context else None,
                metadata={"patterns_matched": "xss"}
            ))

        # Check rate limiting
        if self.check_rate_limit_exceeded(source_ip, endpoint):
            events.append(SecurityEvent(
                event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
                severity=ThreatLevel.MEDIUM,
                description=f"Rate limit exceeded for {endpoint}",
                source_ip=source_ip,
                endpoint=endpoint,
                request_method=method,
                tenant_id=tenant_context.tenant_id if tenant_context else None
            ))

        # Check for suspicious IP
        if await self.is_suspicious_ip(source_ip):
            events.append(SecurityEvent(
                event_type=SecurityEventType.SUSPICIOUS_ACTIVITY,
                severity=ThreatLevel.MEDIUM,
                description=f"Request from suspicious IP: {source_ip}",
                source_ip=source_ip,
                endpoint=endpoint,
                tenant_id=tenant_context.tenant_id if tenant_context else None,
                metadata={"reason": "suspicious_ip"}
            ))

        return events

    async def detect_sql_injection(self, request: Request) -> bool:
        """Detect SQL injection attempts"""
        try:
            # Check query parameters
            for param_value in request.query_params.values():
                for pattern in self.sql_injection_patterns:
                    if re.search(pattern, param_value, re.IGNORECASE):
                        return True

            # Check form data if present
            if hasattr(request, '_body'):
                body = await request.body()
                body_str = body.decode('utf-8', errors='ignore')

                for pattern in self.sql_injection_patterns:
                    if re.search(pattern, body_str, re.IGNORECASE):
                        return True

            return False
        except Exception as e:
            self.logger.error("Error in SQL injection detection", error=str(e))
            return False

    async def detect_xss(self, request: Request) -> bool:
        """Detect XSS attempts"""
        try:
            # Check query parameters
            for param_value in request.query_params.values():
                for pattern in self.xss_patterns:
                    if re.search(pattern, param_value, re.IGNORECASE):
                        return True

            # Check form data if present
            if hasattr(request, '_body'):
                body = await request.body()
                body_str = body.decode('utf-8', errors='ignore')

                for pattern in self.xss_patterns:
                    if re.search(pattern, body_str, re.IGNORECASE):
                        return True

            return False
        except Exception as e:
            self.logger.error("Error in XSS detection", error=str(e))
            return False

    def check_rate_limit_exceeded(self, ip: str, endpoint: str) -> bool:
        """Check if rate limit is exceeded"""
        try:
            current_time = datetime.now(timezone.utc)
            minute_key = current_time.strftime("%Y-%m-%d-%H-%M")

            if ip not in self.request_counts:
                self.request_counts[ip] = {}

            if minute_key not in self.request_counts[ip]:
                self.request_counts[ip][minute_key] = 0

            self.request_counts[ip][minute_key] += 1

            # Clean old entries
            for time_key in list(self.request_counts[ip].keys()):
                if time_key < (current_time - timedelta(minutes=5)).strftime("%Y-%m-%d-%H-%M"):
                    del self.request_counts[ip][time_key]

            # Check limits (can be made configurable)
            rate_limits = {
                "/api/": 100,  # API endpoints
                "/auth/login": 5,  # Login attempts
                "default": 200
            }

            limit = rate_limits.get(endpoint, rate_limits["default"])
            for key in self.request_counts[ip]:
                if key.endswith(minute_key):
                    limit = rate_limits.get(endpoint, rate_limits["default"])
                    break

            return self.request_counts[ip][minute_key] > limit

        except Exception as e:
            self.logger.error("Error in rate limit check", error=str(e))
            return False

    async def is_suspicious_ip(self, ip: str) -> bool:
        """Check if IP is suspicious"""
        try:
            ip_obj = ipaddress.ip_address(ip)

            # Check if IP is in private ranges (generally safe)
            if ip_obj.is_private:
                return False

            # Check against known malicious IP lists (implement external API calls)
            # For now, just check some basic patterns
            suspicious_patterns = [
                # Known bot/scanner patterns
                r"^192\.168\.",  # Should not be public
                r"^10\.",        # Should not be public
                r"^172\.(1[6-9]|2[0-9]|3[0-1])\."  # Should not be public
            ]

            for pattern in suspicious_patterns:
                if re.match(pattern, ip):
                    return True

            return False

        except Exception as e:
            self.logger.error("Error in suspicious IP check", error=str(e))
            return False

    def get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check various headers for real IP
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fallback to direct connection IP
        if hasattr(request, 'client') and request.client:
            return request.client.host

        return "unknown"

    async def analyze_user_behavior(
        self,
        user_id: str,
        tenant_id: str,
        activity_data: Dict[str, Any]
    ) -> List[SecurityEvent]:
        """Analyze user behavior for anomalies"""
        events = []

        try:
            # Get user baseline
            baseline = self.user_behavior_baselines.get(user_id, {})

            # Analyze login patterns
            current_time = datetime.now(timezone.utc)
            login_time = activity_data.get('login_time', current_time)

            if baseline.get('typical_login_hours'):
                login_hour = login_time.hour
                typical_hours = baseline['typical_login_hours']

                if login_hour not in typical_hours:
                    events.append(SecurityEvent(
                        event_type=SecurityEventType.ANOMALOUS_BEHAVIOR,
                        severity=ThreatLevel.LOW,
                        description=f"Unusual login time for user {user_id}",
                        user_id=user_id,
                        tenant_id=tenant_id,
                        metadata={
                            "login_hour": login_hour,
                            "typical_hours": typical_hours
                        }
                    ))

            # Analyze access patterns
            accessed_endpoints = activity_data.get('accessed_endpoints', [])
            if baseline.get('typical_endpoints'):
                unusual_endpoints = set(accessed_endpoints) - set(baseline['typical_endpoints'])

                if unusual_endpoints:
                    events.append(SecurityEvent(
                        event_type=SecurityEventType.ANOMALOUS_BEHAVIOR,
                        severity=ThreatLevel.LOW,
                        description=f"Unusual endpoint access for user {user_id}",
                        user_id=user_id,
                        tenant_id=tenant_id,
                        metadata={
                            "unusual_endpoints": list(unusual_endpoints)
                        }
                    ))

            # Update baseline
            self.update_user_baseline(user_id, activity_data)

        except Exception as e:
            self.logger.error("Error in user behavior analysis", error=str(e))

        return events

    def update_user_baseline(self, user_id: str, activity_data: Dict[str, Any]):
        """Update user behavior baseline"""
        if user_id not in self.user_behavior_baselines:
            self.user_behavior_baselines[user_id] = {
                'typical_login_hours': set(),
                'typical_endpoints': set(),
                'activity_count': 0
            }

        baseline = self.user_behavior_baselines[user_id]

        # Update login hours
        if 'login_time' in activity_data:
            login_hour = activity_data['login_time'].hour
            baseline['typical_login_hours'].add(login_hour)

        # Update typical endpoints
        if 'accessed_endpoints' in activity_data:
            baseline['typical_endpoints'].update(activity_data['accessed_endpoints'])

        baseline['activity_count'] += 1


class ComplianceManager:
    """Manages compliance with various standards"""

    def __init__(self, rls_manager: RLSManager):
        self.rls_manager = rls_manager
        self.personal_data_processor = PersonalDataProcessor(Fernet.generate_key())
        self.logger = logger.bind(component="compliance_manager")

        # Data retention policies (in days)
        self.retention_policies = {
            DataClassification.PUBLIC: 365 * 7,  # 7 years
            DataClassification.INTERNAL: 365 * 5,  # 5 years
            DataClassification.CONFIDENTIAL: 365 * 3,  # 3 years
            DataClassification.PERSONAL: 365 * 2,  # 2 years
            DataClassification.SENSITIVE_PERSONAL: 365 * 1,  # 1 year
        }

    async def process_data_subject_request(
        self,
        request: DataSubjectRequest,
        tenant_context: EnhancedTenantContext
    ) -> DataSubjectRequest:
        """Process GDPR data subject request"""
        try:
            if request.request_type == DataSubjectRight.ACCESS:
                # Collect all personal data for the subject
                personal_data = await self.collect_personal_data(
                    request.data_subject_id,
                    request.tenant_id,
                    request.requested_data_categories
                )

                request.response_data = personal_data
                request.status = "completed"
                request.completed_at = datetime.now(timezone.utc)

            elif request.request_type == DataSubjectRight.ERASURE:
                # Delete personal data (right to be forgotten)
                await self.erase_personal_data(
                    request.data_subject_id,
                    request.tenant_id,
                    request.requested_data_categories
                )

                request.status = "completed"
                request.completed_at = datetime.now(timezone.utc)

            elif request.request_type == DataSubjectRight.RECTIFICATION:
                # Update incorrect personal data
                if request.response_data:
                    await self.update_personal_data(
                        request.data_subject_id,
                        request.tenant_id,
                        request.response_data
                    )

                request.status = "completed"
                request.completed_at = datetime.now(timezone.utc)

            elif request.request_type == DataSubjectRight.DATA_PORTABILITY:
                # Export data in portable format
                portable_data = await self.export_portable_data(
                    request.data_subject_id,
                    request.tenant_id,
                    request.requested_data_categories
                )

                request.response_data = portable_data
                request.response_format = "json"  # Standard portable format
                request.status = "completed"
                request.completed_at = datetime.now(timezone.utc)

            # Save request to database
            await self.save_data_subject_request(request)

            return request

        except Exception as e:
            self.logger.error(
                "Error processing data subject request",
                request_id=request.request_id,
                error=str(e)
            )
            raise

    async def collect_personal_data(
        self,
        data_subject_id: str,
        tenant_id: str,
        categories: List[str]
    ) -> Dict[str, Any]:
        """Collect all personal data for a data subject"""
        personal_data = {}

        try:
            async with self.rls_manager.tenant_context(tenant_id) as conn:
                # Collect from user profiles
                user_data = await conn.fetchrow("""
                    SELECT * FROM user_profiles
                    WHERE user_id = $1 AND tenant_id = $2
                """, data_subject_id, tenant_id)

                if user_data:
                    personal_data['profile'] = dict(user_data)

                # Collect from activity logs
                activity_data = await conn.fetch("""
                    SELECT * FROM audit_logs
                    WHERE user_id = $1 AND tenant_id = $2
                    ORDER BY created_at DESC
                    LIMIT 1000
                """, data_subject_id, tenant_id)

                personal_data['activity_history'] = [dict(row) for row in activity_data]

                # Collect from platform-specific data
                for category in categories:
                    if category == 'marketing_data':
                        marketing_data = await conn.fetch("""
                            SELECT * FROM marketing_interactions
                            WHERE user_id = $1 AND tenant_id = $2
                        """, data_subject_id, tenant_id)
                        personal_data['marketing_data'] = [dict(row) for row in marketing_data]

                    elif category == 'ai_interactions':
                        ai_data = await conn.fetch("""
                            SELECT * FROM ai_conversation_history
                            WHERE user_id = $1 AND tenant_id = $2
                        """, data_subject_id, tenant_id)
                        personal_data['ai_interactions'] = [dict(row) for row in ai_data]

            return personal_data

        except Exception as e:
            self.logger.error(
                "Error collecting personal data",
                data_subject_id=data_subject_id,
                error=str(e)
            )
            raise

    async def erase_personal_data(
        self,
        data_subject_id: str,
        tenant_id: str,
        categories: List[str]
    ):
        """Erase personal data (right to be forgotten)"""
        try:
            async with self.rls_manager.tenant_context(tenant_id) as conn:
                # Anonymize instead of delete to maintain data integrity
                anonymized_id = self.personal_data_processor.pseudonymize_data(
                    data_subject_id, "erasure_salt"
                )

                # Update user profiles
                await conn.execute("""
                    UPDATE user_profiles
                    SET
                        email = $1,
                        first_name = 'ERASED',
                        last_name = 'ERASED',
                        phone = NULL,
                        address = NULL,
                        date_of_birth = NULL,
                        erased_at = CURRENT_TIMESTAMP
                    WHERE user_id = $2 AND tenant_id = $3
                """, anonymized_id, data_subject_id, tenant_id)

                # Anonymize activity logs
                await conn.execute("""
                    UPDATE audit_logs
                    SET
                        user_id = $1,
                        personal_data_removed = TRUE
                    WHERE user_id = $2 AND tenant_id = $3
                """, anonymized_id, data_subject_id, tenant_id)

                # Handle category-specific erasure
                for category in categories:
                    if category == 'marketing_data':
                        await conn.execute("""
                            DELETE FROM marketing_interactions
                            WHERE user_id = $1 AND tenant_id = $2
                        """, data_subject_id, tenant_id)

                    elif category == 'ai_interactions':
                        await conn.execute("""
                            UPDATE ai_conversation_history
                            SET
                                user_id = $1,
                                conversation_data = NULL,
                                personal_data_removed = TRUE
                            WHERE user_id = $2 AND tenant_id = $3
                        """, anonymized_id, data_subject_id, tenant_id)

        except Exception as e:
            self.logger.error(
                "Error erasing personal data",
                data_subject_id=data_subject_id,
                error=str(e)
            )
            raise

    async def update_personal_data(
        self,
        data_subject_id: str,
        tenant_id: str,
        update_data: Dict[str, Any]
    ):
        """Update personal data (rectification)"""
        try:
            async with self.rls_manager.tenant_context(tenant_id) as conn:
                # Build update query dynamically
                set_clauses = []
                values = []
                param_count = 1

                for field, value in update_data.items():
                    # Only update allowed fields
                    allowed_fields = [
                        'email', 'first_name', 'last_name', 'phone',
                        'address', 'date_of_birth', 'preferences'
                    ]

                    if field in allowed_fields:
                        set_clauses.append(f"{field} = ${param_count}")
                        values.append(value)
                        param_count += 1

                if set_clauses:
                    query = f"""
                        UPDATE user_profiles
                        SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = ${param_count} AND tenant_id = ${param_count + 1}
                    """
                    values.extend([data_subject_id, tenant_id])

                    await conn.execute(query, *values)

        except Exception as e:
            self.logger.error(
                "Error updating personal data",
                data_subject_id=data_subject_id,
                error=str(e)
            )
            raise

    async def export_portable_data(
        self,
        data_subject_id: str,
        tenant_id: str,
        categories: List[str]
    ) -> Dict[str, Any]:
        """Export data in portable format"""
        return await self.collect_personal_data(data_subject_id, tenant_id, categories)

    async def save_data_subject_request(self, request: DataSubjectRequest):
        """Save data subject request to database"""
        try:
            async with self.rls_manager.tenant_context(request.tenant_id) as conn:
                await conn.execute("""
                    INSERT INTO data_subject_requests (
                        request_id, request_type, tenant_id, data_subject_id,
                        description, requested_data_categories, legal_basis,
                        status, created_at, due_date, completed_at,
                        response_data, response_format, identity_verified,
                        verification_method, verification_timestamp
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
                    ON CONFLICT (request_id) DO UPDATE SET
                        status = EXCLUDED.status,
                        completed_at = EXCLUDED.completed_at,
                        response_data = EXCLUDED.response_data
                """,
                    request.request_id, request.request_type.value, request.tenant_id,
                    request.data_subject_id, request.description, request.requested_data_categories,
                    request.legal_basis, request.status, request.created_at, request.due_date,
                    request.completed_at, request.response_data, request.response_format,
                    request.identity_verified, request.verification_method, request.verification_timestamp
                )

        except Exception as e:
            self.logger.error(
                "Error saving data subject request",
                request_id=request.request_id,
                error=str(e)
            )
            raise

    async def apply_data_retention_policy(self, tenant_id: str):
        """Apply data retention policies"""
        try:
            current_date = datetime.now(timezone.utc)

            async with self.rls_manager.tenant_context(tenant_id) as conn:
                for classification, retention_days in self.retention_policies.items():
                    cutoff_date = current_date - timedelta(days=retention_days)

                    # Archive or delete old data based on classification
                    if classification == DataClassification.PERSONAL:
                        # Anonymize personal data
                        await conn.execute("""
                            UPDATE audit_logs
                            SET
                                user_id = 'ANONYMIZED_' || LEFT(MD5(user_id), 8),
                                personal_data_removed = TRUE,
                                anonymized_at = CURRENT_TIMESTAMP
                            WHERE tenant_id = $1
                            AND created_at < $2
                            AND personal_data_removed = FALSE
                            AND data_classification = $3
                        """, tenant_id, cutoff_date, classification.value)

                    elif classification == DataClassification.PUBLIC:
                        # Archive public data
                        await conn.execute("""
                            UPDATE public_content
                            SET
                                archived = TRUE,
                                archived_at = CURRENT_TIMESTAMP
                            WHERE tenant_id = $1
                            AND created_at < $2
                            AND archived = FALSE
                        """, tenant_id, cutoff_date)

        except Exception as e:
            self.logger.error(
                "Error applying data retention policy",
                tenant_id=tenant_id,
                error=str(e)
            )
            raise


class SecurityAuditLogger:
    """Handles security event logging and audit trails"""

    def __init__(self, rls_manager: RLSManager):
        self.rls_manager = rls_manager
        self.logger = logger.bind(component="security_audit")

    async def log_security_event(self, event: SecurityEvent):
        """Log a security event to the audit trail"""
        try:
            async with self.rls_manager.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO security_events (
                        event_id, event_type, severity, timestamp, tenant_id,
                        user_id, session_id, platform, description, source_ip,
                        user_agent, endpoint, request_method, metadata, tags,
                        detected_by, response_action, resolution_status
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
                """,
                    event.event_id, event.event_type.value, event.severity.value,
                    event.timestamp, event.tenant_id, event.user_id, event.session_id,
                    event.platform.value if event.platform else None, event.description,
                    event.source_ip, event.user_agent, event.endpoint, event.request_method,
                    event.metadata, event.tags, event.detected_by, event.response_action,
                    event.resolution_status
                )

            # Log to structured logger for real-time monitoring
            self.logger.info(
                "Security event logged",
                event_id=event.event_id,
                event_type=event.event_type.value,
                severity=event.severity.value,
                tenant_id=event.tenant_id,
                user_id=event.user_id,
                description=event.description
            )

        except Exception as e:
            self.logger.error(
                "Error logging security event",
                event_id=event.event_id,
                error=str(e)
            )
            raise

    async def get_security_events(
        self,
        tenant_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        event_types: Optional[List[SecurityEventType]] = None,
        severity_levels: Optional[List[ThreatLevel]] = None,
        limit: int = 100
    ) -> List[SecurityEvent]:
        """Retrieve security events with filters"""
        try:
            conditions = ["tenant_id = $1"]
            params = [tenant_id]
            param_count = 2

            if start_date:
                conditions.append(f"timestamp >= ${param_count}")
                params.append(start_date)
                param_count += 1

            if end_date:
                conditions.append(f"timestamp <= ${param_count}")
                params.append(end_date)
                param_count += 1

            if event_types:
                event_type_values = [et.value for et in event_types]
                conditions.append(f"event_type = ANY(${param_count})")
                params.append(event_type_values)
                param_count += 1

            if severity_levels:
                severity_values = [sl.value for sl in severity_levels]
                conditions.append(f"severity = ANY(${param_count})")
                params.append(severity_values)
                param_count += 1

            query = f"""
                SELECT * FROM security_events
                WHERE {' AND '.join(conditions)}
                ORDER BY timestamp DESC
                LIMIT ${param_count}
            """
            params.append(limit)

            async with self.rls_manager.tenant_context(tenant_id) as conn:
                rows = await conn.fetch(query, *params)

                events = []
                for row in rows:
                    event = SecurityEvent(
                        event_id=row['event_id'],
                        event_type=SecurityEventType(row['event_type']),
                        severity=ThreatLevel(row['severity']),
                        timestamp=row['timestamp'],
                        tenant_id=row['tenant_id'],
                        user_id=row['user_id'],
                        session_id=row['session_id'],
                        platform=PlatformType(row['platform']) if row['platform'] else None,
                        description=row['description'],
                        source_ip=row['source_ip'],
                        user_agent=row['user_agent'],
                        endpoint=row['endpoint'],
                        request_method=row['request_method'],
                        metadata=row['metadata'] or {},
                        tags=row['tags'] or [],
                        detected_by=row['detected_by'],
                        response_action=row['response_action'],
                        resolution_status=row['resolution_status']
                    )
                    events.append(event)

                return events

        except Exception as e:
            self.logger.error(
                "Error retrieving security events",
                tenant_id=tenant_id,
                error=str(e)
            )
            raise


# Global instances
threat_detection_engine: Optional[ThreatDetectionEngine] = None
compliance_manager: Optional[ComplianceManager] = None
security_audit_logger: Optional[SecurityAuditLogger] = None


def initialize_security_framework(rls_manager: RLSManager) -> tuple:
    """Initialize the security and compliance framework"""
    global threat_detection_engine, compliance_manager, security_audit_logger

    threat_detection_engine = ThreatDetectionEngine(rls_manager)
    compliance_manager = ComplianceManager(rls_manager)
    security_audit_logger = SecurityAuditLogger(rls_manager)

    return threat_detection_engine, compliance_manager, security_audit_logger


def get_security_framework() -> tuple:
    """Get the initialized security framework components"""
    if not all([threat_detection_engine, compliance_manager, security_audit_logger]):
        raise RuntimeError("Security framework not initialized")

    return threat_detection_engine, compliance_manager, security_audit_logger