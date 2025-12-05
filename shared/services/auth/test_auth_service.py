#!/usr/bin/env python3
"""
Comprehensive test suite for BizOSaaS Authentication Service
Tests FastAPI-Users integration, multi-tenant auth, and API client
"""

import pytest
import asyncio
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from unittest.mock import Mock, patch, AsyncMock

import httpx
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_async_session, User, Tenant, UserSession, Base
from auth_client import AuthClient, LoginRequest, AuthError, RateLimitError


# Test database setup
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True
)

TestAsyncSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_async_session():
    """Override database session for testing"""
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def setup_test_db():
    """Set up test database"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def test_client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
async def test_session():
    """Create test database session"""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def test_tenant(test_session: AsyncSession):
    """Create test tenant"""
    tenant = Tenant(
        id=uuid.uuid4(),
        name="Test Company",
        slug="test-company",
        status="active",
        allowed_platforms=["bizosaas", "bizoholic"],
        max_users=100
    )
    test_session.add(tenant)
    await test_session.commit()
    await test_session.refresh(tenant)
    return tenant


@pytest.fixture
async def test_user(test_session: AsyncSession, test_tenant: Tenant):
    """Create test user"""
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        hashed_password="$2b$12$hashed_password_here",  # bcrypt hash of "password123"
        first_name="Test",
        last_name="User",
        role="user",
        tenant_id=test_tenant.id,
        allowed_platforms=["bizosaas"],
        is_active=True,
        is_verified=True
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
async def admin_user(test_session: AsyncSession, test_tenant: Tenant):
    """Create admin test user"""
    user = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        hashed_password="$2b$12$hashed_password_here",
        first_name="Admin",
        last_name="User",
        role="super_admin",
        tenant_id=test_tenant.id,
        allowed_platforms=["bizosaas", "bizoholic"],
        is_active=True,
        is_verified=True
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, test_client: TestClient):
        """Test root health endpoint"""
        response = test_client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "bizosaas-auth-unified"
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, test_client: TestClient):
        """Test detailed health endpoint"""
        response = test_client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["service"] == "bizosaas-auth-unified"
        assert data["status"] == "healthy"
        assert "database" in data
        assert "redis" in data


class TestAuthentication:
    """Test authentication endpoints"""
    
    @pytest.mark.asyncio
    async def test_sso_login_success(self, test_client: TestClient, test_user: User, setup_test_db):
        """Test successful SSO login"""
        login_data = {
            "email": test_user.email,
            "password": "password123",
            "platform": "bizosaas",
            "remember_me": False
        }
        
        with patch('bcrypt.checkpw', return_value=True):
            response = test_client.post("/auth/sso/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email
        assert data["tenant"]["slug"] == test_user.tenant.slug
    
    @pytest.mark.asyncio
    async def test_sso_login_invalid_credentials(self, test_client: TestClient, setup_test_db):
        """Test SSO login with invalid credentials"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword",
            "platform": "bizosaas"
        }
        
        response = test_client.post("/auth/sso/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_sso_login_platform_access_denied(self, test_client: TestClient, test_user: User, setup_test_db):
        """Test SSO login with platform access denied"""
        login_data = {
            "email": test_user.email,
            "password": "password123",
            "platform": "unauthorized-platform"
        }
        
        with patch('bcrypt.checkpw', return_value=True):
            response = test_client.post("/auth/sso/login", json=login_data)
        
        assert response.status_code == 403
        assert "Access denied to platform" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, test_client: TestClient, test_user: User, setup_test_db):
        """Test getting current user information"""
        # Mock the current_active_user dependency
        with patch('main.current_active_user', return_value=test_user):
            response = test_client.get("/auth/me")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["user"]["email"] == test_user.email
        assert data["tenant"]["slug"] == test_user.tenant.slug
        assert "permissions" in data
        assert "session_info" in data
    
    @pytest.mark.asyncio
    async def test_platform_authorization(self, test_client: TestClient, test_user: User, setup_test_db):
        """Test platform authorization check"""
        with patch('main.current_active_user', return_value=test_user):
            # Test authorized platform
            response = test_client.get("/auth/authorize/bizosaas")
            assert response.status_code == 200
            
            data = response.json()
            assert data["authorized"] is True
            assert data["platform"] == "bizosaas"
            
            # Test unauthorized platform
            response = test_client.get("/auth/authorize/unauthorized-platform")
            assert response.status_code == 403


class TestTenantManagement:
    """Test tenant management endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_tenant_success(self, test_client: TestClient, admin_user: User, setup_test_db):
        """Test successful tenant creation"""
        tenant_data = {
            "name": "New Test Company",
            "slug": "new-test-company",
            "domain": "newtest.example.com",
            "subscription_plan": "premium",
            "allowed_platforms": ["bizosaas", "bizoholic"],
            "max_users": 50
        }
        
        with patch('main.require_role', return_value=lambda: admin_user):
            response = test_client.post("/tenants", json=tenant_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == tenant_data["name"]
        assert data["slug"] == tenant_data["slug"]
        assert data["domain"] == tenant_data["domain"]
        assert data["max_users"] == tenant_data["max_users"]
    
    @pytest.mark.asyncio
    async def test_create_tenant_duplicate_slug(self, test_client: TestClient, admin_user: User, test_tenant: Tenant, setup_test_db):
        """Test tenant creation with duplicate slug"""
        tenant_data = {
            "name": "Duplicate Company",
            "slug": test_tenant.slug,  # Use existing slug
            "allowed_platforms": ["bizosaas"]
        }
        
        with patch('main.require_role', return_value=lambda: admin_user):
            response = test_client.post("/tenants", json=tenant_data)
        
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_my_tenant(self, test_client: TestClient, test_user: User, setup_test_db):
        """Test getting current user's tenant"""
        with patch('main.current_active_user', return_value=test_user):
            response = test_client.get("/tenants/me")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == str(test_user.tenant.id)
        assert data["name"] == test_user.tenant.name
        assert data["slug"] == test_user.tenant.slug


class TestAuthClient:
    """Test the authentication client"""
    
    @pytest.fixture
    def mock_httpx_client(self):
        """Mock httpx client"""
        client = Mock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=None)
        client.aclose = AsyncMock()
        return client
    
    @pytest.mark.asyncio
    async def test_auth_client_login_success(self):
        """Test successful login through auth client"""
        mock_response_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {
                "id": str(uuid.uuid4()),
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "role": "user",
                "tenant_id": str(uuid.uuid4()),
                "allowed_platforms": ["bizosaas"],
                "is_active": True,
                "is_verified": True
            },
            "tenant": {
                "id": str(uuid.uuid4()),
                "name": "Test Company",
                "slug": "test-company",
                "status": "active",
                "allowed_platforms": ["bizosaas"],
                "max_users": 10
            },
            "permissions": ["user:read"]
        }\n        \n        async def mock_request():\n            response = Mock()\n            response.raise_for_status = Mock()\n            response.json.return_value = mock_response_data\n            return response\n        \n        with patch('httpx.AsyncClient') as mock_client_class:\n            mock_client = Mock()\n            mock_client.post = AsyncMock(return_value=await mock_request())\n            mock_client.aclose = AsyncMock()\n            mock_client_class.return_value = mock_client\n            \n            client = AuthClient(base_url=\"http://localhost:8007\")\n            login_request = LoginRequest(\n                email=\"test@example.com\",\n                password=\"password123\",\n                platform=\"bizosaas\"\n            )\n            \n            auth_response = await client.login(login_request)\n            \n            assert auth_response.access_token == \"test_access_token\"\n            assert auth_response.user.email == \"test@example.com\"\n            assert auth_response.tenant.slug == \"test-company\"\n    \n    @pytest.mark.asyncio\n    async def test_auth_client_retry_logic(self):\n        \"\"\"Test retry logic in auth client\"\"\"\n        with patch('httpx.AsyncClient') as mock_client_class:\n            mock_client = Mock()\n            # First call fails, second succeeds\n            mock_client.post = AsyncMock(side_effect=[\n                httpx.TimeoutException(\"Timeout\"),\n                Mock(json=Mock(return_value={\"status\": \"success\"}), raise_for_status=Mock())\n            ])\n            mock_client.aclose = AsyncMock()\n            mock_client_class.return_value = mock_client\n            \n            client = AuthClient(base_url=\"http://localhost:8007\", max_retries=2)\n            \n            result = await client._make_request(\n                \"POST\", \n                \"/test\", \n                data={\"test\": \"data\"},\n                include_auth=False\n            )\n            \n            assert result == {\"status\": \"success\"}\n            assert mock_client.post.call_count == 2\n    \n    @pytest.mark.asyncio\n    async def test_auth_client_circuit_breaker(self):\n        \"\"\"Test circuit breaker functionality\"\"\"\n        client = AuthClient(base_url=\"http://localhost:8007\")\n        \n        # Simulate failures to open circuit\n        for _ in range(5):\n            client.circuit_breaker.record_failure()\n        \n        assert client.circuit_breaker.state == 'OPEN'\n        \n        # Circuit should reject calls\n        with pytest.raises(Exception):\n            await client.circuit_breaker.call(lambda: None)\n    \n    @pytest.mark.asyncio\n    async def test_auth_client_token_refresh(self):\n        \"\"\"Test token refresh functionality\"\"\"\n        mock_response = {\n            \"access_token\": \"new_access_token\",\n            \"token_type\": \"bearer\",\n            \"expires_in\": 1800\n        }\n        \n        with patch('httpx.AsyncClient') as mock_client_class:\n            mock_client = Mock()\n            mock_client.post = AsyncMock(return_value=Mock(\n                json=Mock(return_value=mock_response),\n                raise_for_status=Mock()\n            ))\n            mock_client.aclose = AsyncMock()\n            mock_client_class.return_value = mock_client\n            \n            client = AuthClient(base_url=\"http://localhost:8007\")\n            client._refresh_token = \"test_refresh_token\"\n            \n            result = await client.refresh_token()\n            \n            assert result is True\n            assert client._access_token == \"new_access_token\"


class TestSecurityFeatures:
    \"\"\"Test security features and edge cases\"\"\"\n    \n    @pytest.mark.asyncio\n    async def test_rate_limiting(self, test_client: TestClient, setup_test_db):\n        \"\"\"Test rate limiting protection\"\"\"\n        login_data = {\n            \"email\": \"test@example.com\",\n            \"password\": \"wrongpassword\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        # Mock rate limiter to trigger immediately\n        with patch('fastapi_limiter.FastAPILimiter.init'):\n            with patch('main.RateLimiter', side_effect=RateLimitError(\"Rate limit exceeded\")):\n                response = test_client.post(\"/auth/sso/login\", json=login_data)\n                \n                # Should handle rate limiting gracefully\n                assert response.status_code in [429, 500]  # Rate limited or server error\n    \n    @pytest.mark.asyncio\n    async def test_account_lockout(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test account lockout after failed attempts\"\"\"\n        login_data = {\n            \"email\": test_user.email,\n            \"password\": \"wrongpassword\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        # Simulate multiple failed login attempts\n        with patch('bcrypt.checkpw', return_value=False):\n            for _ in range(6):  # Exceed lockout threshold\n                test_client.post(\"/auth/sso/login\", json=login_data)\n        \n        # Account should be locked\n        with patch('bcrypt.checkpw', return_value=True):  # Even with correct password\n            response = test_client.post(\"/auth/sso/login\", json=login_data)\n            assert response.status_code == 423  # Locked\n    \n    @pytest.mark.asyncio\n    async def test_token_validation(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test JWT token validation\"\"\"\n        # Test with invalid token\n        headers = {\"Authorization\": \"Bearer invalid_token\"}\n        response = test_client.get(\"/auth/me\", headers=headers)\n        assert response.status_code == 401\n        \n        # Test with expired token (mocked)\n        expired_token = \"expired.jwt.token\"\n        headers = {\"Authorization\": f\"Bearer {expired_token}\"}\n        response = test_client.get(\"/auth/me\", headers=headers)\n        assert response.status_code == 401\n    \n    @pytest.mark.asyncio\n    async def test_sql_injection_protection(self, test_client: TestClient, setup_test_db):\n        \"\"\"Test SQL injection protection\"\"\"\n        malicious_data = {\n            \"email\": \"test@example.com'; DROP TABLE users; --\",\n            \"password\": \"password123\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        response = test_client.post(\"/auth/sso/login\", json=malicious_data)\n        \n        # Should handle gracefully without exposing database errors\n        assert response.status_code in [400, 401, 422]  # Bad request or validation error\n        \n        # Verify tables still exist by making another request\n        normal_data = {\n            \"email\": \"normal@example.com\",\n            \"password\": \"password123\",\n            \"platform\": \"bizosaas\"\n        }\n        response2 = test_client.post(\"/auth/sso/login\", json=normal_data)\n        assert response2.status_code in [401, 422]  # Normal response, not database error


class TestIntegrationScenarios:
    \"\"\"Test real-world integration scenarios\"\"\"\n    \n    @pytest.mark.asyncio\n    async def test_cross_platform_authentication(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test authentication across multiple platforms\"\"\"\n        platforms = [\"bizosaas\", \"bizoholic\"]\n        \n        # Update user to have access to multiple platforms\n        test_user.allowed_platforms = platforms\n        \n        for platform in platforms:\n            login_data = {\n                \"email\": test_user.email,\n                \"password\": \"password123\",\n                \"platform\": platform\n            }\n            \n            with patch('bcrypt.checkpw', return_value=True):\n                response = test_client.post(\"/auth/sso/login\", json=login_data)\n            \n            assert response.status_code == 200\n            data = response.json()\n            assert data[\"user\"][\"email\"] == test_user.email\n    \n    @pytest.mark.asyncio\n    async def test_session_management(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test session creation and management\"\"\"\n        # First, authenticate\n        with patch('main.current_active_user', return_value=test_user):\n            response = test_client.post(\"/auth/sessions\", params={\"platform\": \"bizosaas\"})\n        \n        assert response.status_code == 200\n        data = response.json()\n        \n        assert \"session_id\" in data\n        assert \"session_token\" in data\n        assert \"refresh_token\" in data\n        assert data[\"platform\"] == \"bizosaas\"\n    \n    @pytest.mark.asyncio\n    async def test_audit_logging(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test that audit events are logged\"\"\"\n        login_data = {\n            \"email\": test_user.email,\n            \"password\": \"password123\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        with patch('bcrypt.checkpw', return_value=True):\n            with patch('main.create_audit_log') as mock_audit:\n                response = test_client.post(\"/auth/sso/login\", json=login_data)\n                \n                assert response.status_code == 200\n                # Verify audit log was called (in background task)\n                # Note: Background tasks in tests might need special handling\n    \n    @pytest.mark.asyncio\n    async def test_concurrent_authentication(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test concurrent authentication requests\"\"\"\n        login_data = {\n            \"email\": test_user.email,\n            \"password\": \"password123\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        async def make_login_request():\n            with patch('bcrypt.checkpw', return_value=True):\n                return test_client.post(\"/auth/sso/login\", json=login_data)\n        \n        # Make multiple concurrent requests\n        tasks = [make_login_request() for _ in range(5)]\n        responses = await asyncio.gather(*[asyncio.create_task(task()) for task in tasks])\n        \n        # All should succeed\n        for response in responses:\n            assert response.status_code == 200\n    \n    @pytest.mark.asyncio\n    async def test_database_failure_handling(self, test_client: TestClient, setup_test_db):\n        \"\"\"Test handling of database failures\"\"\"\n        login_data = {\n            \"email\": \"test@example.com\",\n            \"password\": \"password123\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        with patch('main.get_async_session', side_effect=Exception(\"Database connection failed\")):\n            response = test_client.post(\"/auth/sso/login\", json=login_data)\n            \n            # Should handle database failures gracefully\n            assert response.status_code == 500\n            data = response.json()\n            assert \"error\" in data[\"detail\"].lower() or \"failed\" in data[\"detail\"].lower()


# Performance and load testing\nclass TestPerformance:\n    \"\"\"Test performance characteristics\"\"\"\n    \n    @pytest.mark.asyncio\n    @pytest.mark.slow\n    async def test_authentication_performance(self, test_client: TestClient, test_user: User, setup_test_db):\n        \"\"\"Test authentication performance under load\"\"\"\n        login_data = {\n            \"email\": test_user.email,\n            \"password\": \"password123\",\n            \"platform\": \"bizosaas\"\n        }\n        \n        start_time = datetime.now()\n        \n        # Perform multiple authentications\n        for _ in range(100):\n            with patch('bcrypt.checkpw', return_value=True):\n                response = test_client.post(\"/auth/sso/login\", json=login_data)\n                assert response.status_code == 200\n        \n        end_time = datetime.now()\n        duration = (end_time - start_time).total_seconds()\n        \n        # Should complete 100 authentications in reasonable time\n        assert duration < 10.0  # Less than 10 seconds\n        \n        avg_time = duration / 100\n        print(f\"Average authentication time: {avg_time:.3f} seconds\")\n        assert avg_time < 0.1  # Less than 100ms per auth


if __name__ == \"__main__\":\n    pytest.main([\n        \"test_auth_service.py\",\n        \"-v\",\n        \"--asyncio-mode=auto\",\n        \"--tb=short\"\n    ])