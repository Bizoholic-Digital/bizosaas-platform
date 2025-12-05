"""
Security Middleware for BizOSaaS Platform
Integrates threat detection, compliance monitoring, and audit logging
"""

import asyncio
import json
import structlog
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
from uuid import uuid4

from fastapi import Request, Response, HTTPException, status
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import JSONResponse

from enhanced_tenant_context import EnhancedTenantContext
from shared.rls_middleware import RLSRequestHelper
from compliance_framework import (
    SecurityEvent,
    SecurityEventType,
    ThreatLevel,
    ThreatDetectionEngine,
    SecurityAuditLogger,
    ComplianceManager,
    get_security_framework
)

logger = structlog.get_logger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive security middleware for threat detection and compliance
    """

    def __init__(
        self,
        app,
        enable_threat_detection: bool = True,
        enable_audit_logging: bool = True,
        enable_compliance_monitoring: bool = True,
        excluded_paths: Optional[List[str]] = None,
        rate_limiting_enabled: bool = True,
        auto_block_suspicious_ips: bool = False
    ):
        super().__init__(app)

        # Configuration
        self.enable_threat_detection = enable_threat_detection
        self.enable_audit_logging = enable_audit_logging
        self.enable_compliance_monitoring = enable_compliance_monitoring
        self.rate_limiting_enabled = rate_limiting_enabled
        self.auto_block_suspicious_ips = auto_block_suspicious_ips

        # Excluded paths from security scanning
        self.excluded_paths = excluded_paths or [
            "/health",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
            "/metrics",
            "/static/"
        ]

        # Security components
        self.threat_detection_engine: Optional[ThreatDetectionEngine] = None
        self.security_audit_logger: Optional[SecurityAuditLogger] = None
        self.compliance_manager: Optional[ComplianceManager] = None

        # Blocked IPs (in production, use Redis or database)
        self.blocked_ips: set = set()

        self.logger = logger.bind(component="security_middleware")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Main middleware dispatch method
        """
        start_time = asyncio.get_event_loop().time()
        request_id = str(uuid4())

        # Initialize security components if not already done
        if not self.threat_detection_engine:
            try:
                (
                    self.threat_detection_engine,
                    self.compliance_manager,
                    self.security_audit_logger
                ) = get_security_framework()
            except RuntimeError:
                # Security framework not initialized - continue without security features
                self.logger.warning("Security framework not initialized")

        # Skip security processing for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        # Get client information
        client_ip = self.get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")

        # Check for blocked IPs
        if client_ip in self.blocked_ips:
            self.logger.warning(
                "Blocked IP attempted access",
                ip=client_ip,
                path=request.url.path,
                request_id=request_id
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"error": "Access denied", "request_id": request_id}
            )

        # Get tenant context
        tenant_context = RLSRequestHelper.get_tenant_context(request)

        security_events = []
        audit_event = None

        try:
            # Threat detection
            if self.enable_threat_detection and self.threat_detection_engine:
                threat_events = await self.threat_detection_engine.analyze_request(
                    request, tenant_context
                )
                security_events.extend(threat_events)

                # Handle critical threats
                critical_events = [e for e in threat_events if e.severity == ThreatLevel.CRITICAL]
                if critical_events and self.auto_block_suspicious_ips:
                    self.blocked_ips.add(client_ip)
                    self.logger.critical(
                        "Critical threat detected - IP blocked",
                        ip=client_ip,
                        events=[e.event_type.value for e in critical_events],
                        request_id=request_id
                    )
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"error": "Security threat detected", "request_id": request_id}
                    )

            # Prepare audit event
            if self.enable_audit_logging:
                audit_event = self.create_audit_event(
                    request, tenant_context, request_id, start_time
                )

            # Process the request
            response = await call_next(request)

            # Update audit event with response information
            if audit_event:
                audit_event.response_status = response.status_code
                audit_event.duration_ms = int(
                    (asyncio.get_event_loop().time() - start_time) * 1000
                )

            # Log successful security events
            if self.security_audit_logger:
                for event in security_events:
                    await self.security_audit_logger.log_security_event(event)

                if audit_event:
                    await self.log_audit_event(audit_event)

            # Compliance monitoring
            if self.enable_compliance_monitoring and self.compliance_manager:
                await self.monitor_compliance(request, response, tenant_context)

            return response

        except HTTPException as e:
            # Log HTTP exceptions as security events
            if e.status_code >= 400:
                security_event = SecurityEvent(
                    event_type=SecurityEventType.ACCESS_DENIED,
                    severity=ThreatLevel.MEDIUM if e.status_code < 500 else ThreatLevel.HIGH,
                    description=f"HTTP {e.status_code}: {e.detail}",
                    source_ip=client_ip,
                    user_agent=user_agent,
                    endpoint=request.url.path,
                    request_method=request.method,
                    tenant_id=tenant_context.tenant_id if tenant_context else None,
                    metadata={"status_code": e.status_code, "detail": e.detail}
                )

                if self.security_audit_logger:
                    await self.security_audit_logger.log_security_event(security_event)

            raise

        except Exception as e:
            # Log unexpected errors as security events
            security_event = SecurityEvent(
                event_type=SecurityEventType.SYSTEM_ERROR,
                severity=ThreatLevel.HIGH,
                description=f"Unexpected error in security middleware: {str(e)}",
                source_ip=client_ip,
                user_agent=user_agent,
                endpoint=request.url.path,
                request_method=request.method,
                tenant_id=tenant_context.tenant_id if tenant_context else None,
                metadata={"error_type": type(e).__name__, "error_message": str(e)}
            )

            if self.security_audit_logger:
                await self.security_audit_logger.log_security_event(security_event)

            self.logger.error(
                "Security middleware error",
                error=str(e),
                request_id=request_id,
                path=request.url.path
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal security error"
            )

    def create_audit_event(
        self,
        request: Request,
        tenant_context: Optional[EnhancedTenantContext],
        request_id: str,
        start_time: float
    ) -> Dict[str, Any]:
        """
        Create audit event for request
        """
        return {
            "log_id": str(uuid4()),
            "tenant_id": tenant_context.tenant_id if tenant_context else None,
            "user_id": getattr(request.state, 'user_id', None),
            "session_id": request.headers.get("x-session-id"),
            "action": f"{request.method} {request.url.path}",
            "resource_type": self.extract_resource_type(request.url.path),
            "resource_id": self.extract_resource_id(request.url.path),
            "platform": tenant_context.primary_platform.value if tenant_context else None,
            "source_ip": self.get_client_ip(request),
            "user_agent": request.headers.get("user-agent"),
            "endpoint": request.url.path,
            "request_method": request.method,
            "request_data": self.extract_request_data(request),
            "response_status": None,  # Will be updated after response
            "created_at": datetime.now(timezone.utc),
            "duration_ms": None,  # Will be calculated
            "data_classification": self.classify_data(request.url.path),
            "contains_personal_data": self.contains_personal_data(request),
            "business_context": self.extract_business_context(request.url.path),
            "risk_level": self.assess_risk_level(request),
            "compliance_relevant": self.is_compliance_relevant(request.url.path),
            "metadata": {
                "request_id": request_id,
                "headers": dict(request.headers),
                "query_params": dict(request.query_params)
            }
        }

    async def log_audit_event(self, audit_event: Dict[str, Any]):
        """
        Log audit event to database
        """
        if not self.security_audit_logger:
            return

        try:
            # Convert to database format and save
            # This would integrate with the audit_logs table
            pass  # Implementation would go here
        except Exception as e:
            self.logger.error("Failed to log audit event", error=str(e))

    async def monitor_compliance(
        self,
        request: Request,
        response: Response,
        tenant_context: Optional[EnhancedTenantContext]
    ):
        """
        Monitor compliance-related activities
        """
        if not tenant_context or not self.compliance_manager:
            return

        # Monitor for personal data access
        if self.contains_personal_data(request):
            security_event = SecurityEvent(
                event_type=SecurityEventType.PERSONAL_DATA_ACCESS,
                severity=ThreatLevel.LOW,
                description="Personal data accessed",
                source_ip=self.get_client_ip(request),
                endpoint=request.url.path,
                request_method=request.method,
                tenant_id=tenant_context.tenant_id,
                user_id=getattr(request.state, 'user_id', None),
                metadata={
                    "data_type": "personal",
                    "response_status": response.status_code
                }
            )

            await self.security_audit_logger.log_security_event(security_event)

        # Monitor for data export activities
        if self.is_data_export(request):
            security_event = SecurityEvent(
                event_type=SecurityEventType.DATA_EXPORT,
                severity=ThreatLevel.MEDIUM,
                description="Data export activity detected",
                source_ip=self.get_client_ip(request),
                endpoint=request.url.path,
                request_method=request.method,
                tenant_id=tenant_context.tenant_id,
                user_id=getattr(request.state, 'user_id', None),
                metadata={
                    "export_type": "api",
                    "response_status": response.status_code
                }
            )

            await self.security_audit_logger.log_security_event(security_event)

    def get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request
        """
        # Check various headers for real IP
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        if hasattr(request, 'client') and request.client:
            return request.client.host

        return "unknown"

    def extract_resource_type(self, path: str) -> str:
        """
        Extract resource type from URL path
        """
        path_parts = path.strip("/").split("/")

        if len(path_parts) >= 2:
            if path_parts[0] == "api":
                return path_parts[1] if len(path_parts) > 1 else "api"
            else:
                return path_parts[0]

        return "unknown"

    def extract_resource_id(self, path: str) -> Optional[str]:
        """
        Extract resource ID from URL path
        """
        path_parts = path.strip("/").split("/")

        # Look for UUID-like patterns or numeric IDs
        for part in path_parts:
            if (len(part) == 36 and part.count("-") == 4) or part.isdigit():
                return part

        return None

    def extract_request_data(self, request: Request) -> Dict[str, Any]:
        """
        Extract relevant request data for auditing
        """
        data = {
            "query_params": dict(request.query_params),
            "path_params": getattr(request, "path_params", {}),
        }

        # Add content type if available
        content_type = request.headers.get("content-type")
        if content_type:
            data["content_type"] = content_type

        return data

    def classify_data(self, path: str) -> str:
        """
        Classify the data sensitivity level based on the endpoint
        """
        if any(keyword in path.lower() for keyword in ["personal", "profile", "user", "contact"]):
            return "personal"
        elif any(keyword in path.lower() for keyword in ["payment", "billing", "credit", "financial"]):
            return "sensitive_personal"
        elif any(keyword in path.lower() for keyword in ["internal", "admin", "management"]):
            return "confidential"
        elif any(keyword in path.lower() for keyword in ["public", "docs", "health"]):
            return "public"
        else:
            return "internal"

    def contains_personal_data(self, request: Request) -> bool:
        """
        Check if the request involves personal data
        """
        path = request.url.path.lower()
        personal_data_indicators = [
            "user", "profile", "contact", "personal", "email", "phone",
            "address", "name", "identification", "preferences"
        ]

        return any(indicator in path for indicator in personal_data_indicators)

    def extract_business_context(self, path: str) -> str:
        """
        Extract business context from the request path
        """
        if "/api/brain/" in path:
            return "ai_operations"
        elif "/api/auth/" in path:
            return "authentication"
        elif "/api/payment/" in path:
            return "financial"
        elif "/api/admin/" in path:
            return "administration"
        elif "/api/tenant/" in path:
            return "tenant_management"
        else:
            return "general"

    def assess_risk_level(self, request: Request) -> str:
        """
        Assess risk level of the request
        """
        path = request.url.path.lower()
        method = request.method.upper()

        # High risk operations
        if method in ["DELETE"] or "delete" in path:
            return "high"
        elif "admin" in path or "management" in path:
            return "high"
        elif method in ["POST", "PUT", "PATCH"]:
            return "medium"
        elif self.contains_personal_data(request):
            return "medium"
        else:
            return "low"

    def is_compliance_relevant(self, path: str) -> bool:
        """
        Check if the request is relevant for compliance monitoring
        """
        compliance_paths = [
            "/api/user", "/api/profile", "/api/personal", "/api/consent",
            "/api/data", "/api/export", "/api/delete", "/api/privacy"
        ]

        return any(comp_path in path.lower() for comp_path in compliance_paths)

    def is_data_export(self, request: Request) -> bool:
        """
        Check if the request is for data export
        """
        path = request.url.path.lower()
        export_indicators = ["export", "download", "backup", "dump", "extract"]

        return any(indicator in path for indicator in export_indicators)


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware with intelligent threat detection
    """

    def __init__(
        self,
        app,
        default_rate_limit: int = 100,  # requests per minute
        burst_limit: int = 200,  # burst allowance
        window_size: int = 60,  # seconds
        enabled: bool = True
    ):
        super().__init__(app)
        self.default_rate_limit = default_rate_limit
        self.burst_limit = burst_limit
        self.window_size = window_size
        self.enabled = enabled

        # Rate limiting data (in production, use Redis)
        self.request_counts: Dict[str, List[datetime]] = {}
        self.burst_counts: Dict[str, int] = {}

        self.logger = logger.bind(component="rate_limiting")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Apply rate limiting
        """
        if not self.enabled:
            return await call_next(request)

        client_ip = self.get_client_ip(request)
        current_time = datetime.now(timezone.utc)

        # Clean old entries
        self.cleanup_old_entries(client_ip, current_time)

        # Check rate limits
        if self.is_rate_limited(client_ip, current_time):
            # Log rate limit exceeded event
            await self.log_rate_limit_event(request, client_ip)

            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.default_rate_limit} requests per minute allowed",
                    "retry_after": self.window_size
                },
                headers={"Retry-After": str(self.window_size)}
            )

        # Record the request
        self.record_request(client_ip, current_time)

        return await call_next(request)

    def get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        if hasattr(request, 'client') and request.client:
            return request.client.host

        return "unknown"

    def cleanup_old_entries(self, client_ip: str, current_time: datetime):
        """Remove old entries outside the window"""
        if client_ip in self.request_counts:
            cutoff_time = current_time - timedelta(seconds=self.window_size)
            self.request_counts[client_ip] = [
                req_time for req_time in self.request_counts[client_ip]
                if req_time > cutoff_time
            ]

    def is_rate_limited(self, client_ip: str, current_time: datetime) -> bool:
        """Check if the client has exceeded rate limits"""
        if client_ip not in self.request_counts:
            return False

        request_count = len(self.request_counts[client_ip])

        # Check regular rate limit
        if request_count >= self.default_rate_limit:
            return True

        # Check burst limit
        burst_count = self.burst_counts.get(client_ip, 0)
        if burst_count >= self.burst_limit:
            return True

        return False

    def record_request(self, client_ip: str, current_time: datetime):
        """Record a request for rate limiting"""
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []

        self.request_counts[client_ip].append(current_time)

        # Update burst count
        self.burst_counts[client_ip] = self.burst_counts.get(client_ip, 0) + 1

        # Reset burst count periodically
        if len(self.request_counts[client_ip]) % 10 == 0:
            self.burst_counts[client_ip] = max(0, self.burst_counts[client_ip] - 5)

    async def log_rate_limit_event(self, request: Request, client_ip: str):
        """Log rate limiting event"""
        try:
            threat_detection_engine, _, security_audit_logger = get_security_framework()

            security_event = SecurityEvent(
                event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
                severity=ThreatLevel.MEDIUM,
                description=f"Rate limit exceeded for IP {client_ip}",
                source_ip=client_ip,
                user_agent=request.headers.get("user-agent"),
                endpoint=request.url.path,
                request_method=request.method,
                metadata={
                    "rate_limit": self.default_rate_limit,
                    "window_size": self.window_size
                }
            )

            await security_audit_logger.log_security_event(security_event)

        except RuntimeError:
            # Security framework not initialized
            self.logger.warning("Rate limit exceeded but security framework not available")


# Utility functions for middleware setup
def setup_security_middleware(app, **kwargs):
    """
    Setup security middleware with configuration
    """
    app.add_middleware(SecurityMiddleware, **kwargs)
    return app


def setup_rate_limiting_middleware(app, **kwargs):
    """
    Setup rate limiting middleware with configuration
    """
    app.add_middleware(RateLimitingMiddleware, **kwargs)
    return app


def setup_comprehensive_security(app, config: Dict[str, Any] = None):
    """
    Setup comprehensive security middleware stack
    """
    config = config or {}

    # Rate limiting (first layer)
    app.add_middleware(
        RateLimitingMiddleware,
        default_rate_limit=config.get("rate_limit", 100),
        burst_limit=config.get("burst_limit", 200),
        enabled=config.get("rate_limiting_enabled", True)
    )

    # Security middleware (second layer)
    app.add_middleware(
        SecurityMiddleware,
        enable_threat_detection=config.get("threat_detection_enabled", True),
        enable_audit_logging=config.get("audit_logging_enabled", True),
        enable_compliance_monitoring=config.get("compliance_monitoring_enabled", True),
        auto_block_suspicious_ips=config.get("auto_block_suspicious_ips", False)
    )

    return app