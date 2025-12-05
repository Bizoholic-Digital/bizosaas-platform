"""
FastAPI Middleware for Row-Level Security (RLS) Context Management
Automatically manages tenant context for all database operations
"""

import asyncio
import json
import structlog
from typing import Dict, Any, Optional, List, Callable
from uuid import UUID
from fastapi import Request, Response, HTTPException, status
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from enhanced_tenant_context import (
    EnhancedTenantContext,
    TenantContextManager,
    PlatformType
)
from rls_manager import RLSManager, RLSContext, RLSAccessLevel

logger = structlog.get_logger(__name__)


class RLSMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for automatic Row-Level Security context management

    Features:
    - Automatic tenant detection from request headers/tokens
    - Platform-specific access control
    - Database connection context management
    - Request/response logging and auditing
    """

    def __init__(
        self,
        app,
        rls_manager: RLSManager,
        tenant_context_manager: TenantContextManager,
        excluded_paths: Optional[List[str]] = None,
        require_tenant_context: bool = True,
        enable_audit_logging: bool = True
    ):
        super().__init__(app)
        self.rls_manager = rls_manager
        self.tenant_context_manager = tenant_context_manager
        self.excluded_paths = excluded_paths or [
            "/health",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
            "/metrics"
        ]
        self.require_tenant_context = require_tenant_context
        self.enable_audit_logging = enable_audit_logging
        self.logger = logger.bind(component="rls_middleware")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process request with automatic RLS context management
        """
        start_time = asyncio.get_event_loop().time()

        # Skip middleware for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        try:
            # Extract tenant context from request
            tenant_context = await self._extract_tenant_context(request)

            # Validate tenant context if required
            if self.require_tenant_context and not tenant_context:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Tenant context required but not found in request"
                )

            # Set request state for downstream access
            if tenant_context:
                request.state.tenant_context = tenant_context
                request.state.rls_context = await self.rls_manager.create_tenant_context_from_enhanced(
                    tenant_context,
                    user_id=self._extract_user_id(request)
                )

            # Process the request
            response = await call_next(request)

            # Log successful request if audit logging is enabled
            if self.enable_audit_logging and tenant_context:
                await self._log_request_audit(
                    request, response, tenant_context, start_time
                )

            return response

        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            self.logger.error(
                "RLS middleware error",
                path=request.url.path,
                method=request.method,
                error=str(e)
            )

            # Log security event for unexpected errors
            if hasattr(request.state, 'tenant_context'):
                await self._log_security_event(
                    request, "middleware_error", str(e)
                )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during request processing"
            )

    async def _extract_tenant_context(
        self,
        request: Request
    ) -> Optional[EnhancedTenantContext]:
        """
        Extract tenant context from request headers and authentication
        """
        try:
            # Method 1: Extract from Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header:
                tenant_context = await self._extract_from_auth_token(auth_header)
                if tenant_context:
                    return tenant_context

            # Method 2: Extract from custom headers
            tenant_id = request.headers.get("X-Tenant-ID")
            if tenant_id:
                tenant_context = await self.tenant_context_manager.get_context(tenant_id)
                if tenant_context:
                    return tenant_context

            # Method 3: Extract from subdomain
            host = request.headers.get("Host", "")
            tenant_context = await self._extract_from_subdomain(host)
            if tenant_context:
                return tenant_context

            # Method 4: Extract from query parameters (development only)
            if request.query_params.get("tenant_id"):
                tenant_id = request.query_params.get("tenant_id")
                return await self.tenant_context_manager.get_context(tenant_id)

            return None

        except Exception as e:
            self.logger.error(
                "Failed to extract tenant context",
                path=request.url.path,
                error=str(e)
            )
            return None

    async def _extract_from_auth_token(
        self,
        auth_header: str
    ) -> Optional[EnhancedTenantContext]:
        """
        Extract tenant context from JWT token
        """
        try:
            if not auth_header.startswith("Bearer "):
                return None

            token = auth_header[7:]  # Remove "Bearer " prefix

            # Decode JWT token (implement actual JWT verification)
            # For now, using a mock implementation
            if token == "demo_token":
                return await self.tenant_context_manager.get_context("demo_tenant")

            # TODO: Implement actual JWT decoding with tenant claims
            # payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            # tenant_id = payload.get("tenant_id")
            # if tenant_id:
            #     return await self.tenant_context_manager.get_context(tenant_id)

            return None

        except Exception as e:
            self.logger.warning(
                "Failed to extract tenant from auth token",
                error=str(e)
            )
            return None

    async def _extract_from_subdomain(
        self,
        host: str
    ) -> Optional[EnhancedTenantContext]:
        """
        Extract tenant context from subdomain
        """
        try:
            # Parse subdomain from host
            parts = host.split(".")
            if len(parts) >= 3:  # subdomain.domain.tld
                subdomain = parts[0]

                # Skip common subdomains
                if subdomain in ["www", "api", "admin"]:
                    return None

                # Look up tenant by subdomain
                return await self.tenant_context_manager.get_context_by_subdomain(subdomain)

            return None

        except Exception as e:
            self.logger.warning(
                "Failed to extract tenant from subdomain",
                host=host,
                error=str(e)
            )
            return None

    def _extract_user_id(self, request: Request) -> Optional[UUID]:
        """
        Extract user ID from request
        """
        try:
            # Extract from custom header
            user_id_header = request.headers.get("X-User-ID")
            if user_id_header:
                return UUID(user_id_header)

            # Extract from JWT token (implement based on your JWT structure)
            # For now, return a mock user ID
            return UUID("123e4567-e89b-12d3-a456-426614174000")

        except Exception as e:
            self.logger.warning(
                "Failed to extract user ID",
                error=str(e)
            )
            return None

    async def _determine_platform_context(
        self,
        request: Request
    ) -> Optional[PlatformType]:
        """
        Determine which platform is being accessed based on request
        """
        path = request.url.path

        # Platform detection based on API path
        if "/api/brain/bizoholic/" in path:
            return PlatformType.BIZOHOLIC
        elif "/api/brain/coreldove/" in path:
            return PlatformType.CORELDOVE
        elif "/api/brain/business-directory/" in path:
            return PlatformType.BUSINESS_DIRECTORY
        elif "/api/brain/thrillring/" in path:
            return PlatformType.THRILLRING
        elif "/api/brain/quanttrade/" in path:
            return PlatformType.QUANTTRADE

        # Platform detection based on host/subdomain
        host = request.headers.get("Host", "")
        if "bizoholic" in host:
            return PlatformType.BIZOHOLIC
        elif "coreldove" in host:
            return PlatformType.CORELDOVE
        elif "directory" in host:
            return PlatformType.BUSINESS_DIRECTORY
        elif "thrillring" in host:
            return PlatformType.THRILLRING
        elif "quanttrade" in host:
            return PlatformType.QUANTTRADE

        return None

    async def _log_request_audit(
        self,
        request: Request,
        response: Response,
        tenant_context: EnhancedTenantContext,
        start_time: float
    ) -> None:
        """
        Log request for audit purposes
        """
        try:
            end_time = asyncio.get_event_loop().time()
            processing_time = (end_time - start_time) * 1000  # Convert to milliseconds

            platform = await self._determine_platform_context(request)

            audit_data = {
                "tenant_id": tenant_context.tenant_id,
                "user_id": str(getattr(request.state, 'user_id', None)),
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "platform": platform.value if platform else None,
                "response_status": response.status_code,
                "processing_time_ms": round(processing_time, 2),
                "user_agent": request.headers.get("User-Agent"),
                "ip_address": request.client.host if request.client else None
            }

            self.logger.info(
                "Request processed",
                **audit_data
            )

            # Store in database audit log if needed
            async with self.rls_manager.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO security_events (
                        tenant_id, event_type, severity, description,
                        request_data, created_at
                    ) VALUES ($1, $2, $3, $4, $5, CURRENT_TIMESTAMP)
                """,
                    tenant_context.tenant_id,
                    "api_request",
                    "low",
                    f"{request.method} {request.url.path}",
                    audit_data
                )

        except Exception as e:
            self.logger.error(
                "Failed to log request audit",
                error=str(e)
            )

    async def _log_security_event(
        self,
        request: Request,
        event_type: str,
        description: str,
        severity: str = "medium"
    ) -> None:
        """
        Log security events
        """
        try:
            tenant_context = getattr(request.state, 'tenant_context', None)

            security_data = {
                "event_type": event_type,
                "description": description,
                "severity": severity,
                "method": request.method,
                "path": request.url.path,
                "ip_address": request.client.host if request.client else None,
                "user_agent": request.headers.get("User-Agent"),
                "tenant_id": tenant_context.tenant_id if tenant_context else None
            }

            self.logger.warning(
                "Security event",
                **security_data
            )

            # Store in security events table
            async with self.rls_manager.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO security_events (
                        tenant_id, event_type, severity, description,
                        ip_address, user_agent, request_data, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, CURRENT_TIMESTAMP)
                """,
                    security_data["tenant_id"],
                    event_type,
                    severity,
                    description,
                    security_data["ip_address"],
                    security_data["user_agent"],
                    security_data
                )

        except Exception as e:
            self.logger.error(
                "Failed to log security event",
                error=str(e)
            )


class RLSRequestHelper:
    """
    Helper class for accessing RLS context within request handlers
    """

    @staticmethod
    def get_tenant_context(request: Request) -> Optional[EnhancedTenantContext]:
        """Get tenant context from request state"""
        return getattr(request.state, 'tenant_context', None)

    @staticmethod
    def get_rls_context(request: Request) -> Optional[RLSContext]:
        """Get RLS context from request state"""
        return getattr(request.state, 'rls_context', None)

    @staticmethod
    def require_tenant_context(request: Request) -> EnhancedTenantContext:
        """Get tenant context or raise exception if not found"""
        context = RLSRequestHelper.get_tenant_context(request)
        if not context:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tenant context required"
            )
        return context

    @staticmethod
    def require_rls_context(request: Request) -> RLSContext:
        """Get RLS context or raise exception if not found"""
        context = RLSRequestHelper.get_rls_context(request)
        if not context:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="RLS context required"
            )
        return context

    @staticmethod
    async def validate_platform_access(
        request: Request,
        platform: PlatformType,
        operation: str = "read"
    ) -> bool:
        """
        Validate platform access for current request
        """
        tenant_context = RLSRequestHelper.get_tenant_context(request)
        if not tenant_context:
            return False

        platform_access = tenant_context.platform_access.get(platform)
        if not platform_access or not platform_access.enabled:
            return False

        # Check operation-specific permissions
        if operation == "write" and not platform_access.features.get("write_access", True):
            return False
        elif operation == "admin" and not platform_access.features.get("admin_access", False):
            return False

        return True

    @staticmethod
    async def require_platform_access(
        request: Request,
        platform: PlatformType,
        operation: str = "read"
    ) -> None:
        """
        Require platform access or raise exception
        """
        has_access = await RLSRequestHelper.validate_platform_access(
            request, platform, operation
        )

        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied to {platform.value} platform for {operation} operation"
            )


# Utility functions for FastAPI dependency injection
def get_tenant_context(request: Request) -> EnhancedTenantContext:
    """FastAPI dependency for tenant context"""
    return RLSRequestHelper.require_tenant_context(request)


def get_rls_context(request: Request) -> RLSContext:
    """FastAPI dependency for RLS context"""
    return RLSRequestHelper.require_rls_context(request)


async def require_bizoholic_access(request: Request) -> None:
    """FastAPI dependency for Bizoholic platform access"""
    await RLSRequestHelper.require_platform_access(
        request, PlatformType.BIZOHOLIC
    )


async def require_coreldove_access(request: Request) -> None:
    """FastAPI dependency for CoreLDove platform access"""
    await RLSRequestHelper.require_platform_access(
        request, PlatformType.CORELDOVE
    )


async def require_directory_access(request: Request) -> None:
    """FastAPI dependency for Business Directory platform access"""
    await RLSRequestHelper.require_platform_access(
        request, PlatformType.BUSINESS_DIRECTORY
    )


async def require_thrillring_access(request: Request) -> None:
    """FastAPI dependency for ThrillRing platform access"""
    await RLSRequestHelper.require_platform_access(
        request, PlatformType.THRILLRING
    )


async def require_quanttrade_access(request: Request) -> None:
    """FastAPI dependency for QuantTrade platform access"""
    await RLSRequestHelper.require_platform_access(
        request, PlatformType.QUANTTRADE
    )


# Example usage in FastAPI routes:
"""
from fastapi import Depends

@app.get("/api/brain/bizoholic/leads")
async def get_leads(
    request: Request,
    tenant_context: EnhancedTenantContext = Depends(get_tenant_context),
    _: None = Depends(require_bizoholic_access)
):
    # This endpoint automatically has:
    # 1. Tenant context validation
    # 2. Bizoholic platform access validation
    # 3. Database RLS context set

    rls_context = RLSRequestHelper.get_rls_context(request)
    async with rls_manager.tenant_session(rls_context) as conn:
        leads = await conn.fetch("SELECT * FROM bizoholic_leads")
        return {"leads": [dict(lead) for lead in leads]}
"""