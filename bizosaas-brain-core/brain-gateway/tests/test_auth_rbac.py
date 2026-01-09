import pytest
from fastapi.testclient import TestClient
from main import app
from app.dependencies import get_current_user, require_role
from domain.ports.identity_port import AuthenticatedUser
from uuid import uuid4

client = TestClient(app)

# Helper to create mock users with different roles
def get_mock_user(role: str):
    return AuthenticatedUser(
        id=uuid4(),
        email=f"test-{role.lower().replace(' ', '-')}@example.com",
        tenant_id=uuid4(),
        roles=[role]
    )

@pytest.mark.parametrize("role, endpoint, expected_status", [
    ("Super Admin", "/api/admin/stats", 200),
    ("Admin", "/api/admin/stats", 403),
    ("Client", "/api/admin/stats", 403),
    ("Super Admin", "/api/brain/metrics/aggregation", 200),
    ("Admin", "/api/brain/metrics/aggregation", 200),
    ("Client", "/api/brain/metrics/aggregation", 403),
    ("Partner", "/api/campaigns/", 200), # Assuming GET /api/campaigns exists
])
def test_rbac_access(role, endpoint, expected_status):
    """
    Test Role-Based Access Control for various endpoints.
    """
    mock_user = get_mock_user(role)
    
    # Override dependencies
    app.dependency_overrides[get_current_user] = lambda: mock_user
    # We also need to override require_role because it's a decorator-like factory
    # Actually, require_role(r) returns a dependency function.
    # In our implementation, require_role checks user.roles.
    
    try:
        response = client.get(endpoint)
        assert response.status_code == expected_status
    finally:
        app.dependency_overrides.clear()

def test_unauthenticated_access():
    """
    Test that endpoints requiring auth return 401/403 when no user is present.
    """
    # By default, without override, it might fail or use Clerk.
    # We want to ensure it's protected.
    response = client.get("/api/admin/stats")
    assert response.status_code in [401, 403]
