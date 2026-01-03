# Standalone E2E Test Script
from fastapi.testclient import TestClient
from domain.ports.identity_port import AuthenticatedUser

# Mock User
MOCK_USER = AuthenticatedUser(
    id="user_123",
    email="test@bizos.com",
    name="Test User",
    tenant_id="tenant_abc",
    roles=["admin"]
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependencies import get_db, get_current_user
from app.middleware.auth import get_current_user as auth_get_current_user
from app.models import Base
from app.models.onboarding_session import OnboardingSession
from app.models.billing_event import BillingEvent
from app.models.strategy_validation import StrategyValidation
from app.models.user import User, Tenant

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import UUID

# Fix UUID for SQLite
@compiles(UUID, "sqlite")
def compile_uuid_sqlite(type_, compiler, **kw):
    return "CHAR(32)"

from sqlalchemy.pool import StaticPool
# Setup In-memory DB for Testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in memory
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return MOCK_USER

from main import app as fastapi_app
from app.dependencies import get_db, get_current_user
from app.middleware.auth import get_current_user as auth_get_current_user
from app.models import Base

# Monkeypatch for direct calls in activities/services
import app.dependencies as deps
deps.get_db = override_get_db
deps.SessionLocal = TestingSessionLocal

fastapi_app.dependency_overrides[get_db] = override_get_db
fastapi_app.dependency_overrides[get_current_user] = override_get_current_user
fastapi_app.dependency_overrides[auth_get_current_user] = override_get_current_user

client = TestClient(fastapi_app)

def test_full_onboarding_to_compliance_e2e():
    """
    E2E Test Case:
    1. User starts onboarding by saving business profile.
    2. User triggers digital presence detection.
    3. User triggers magic discovery for external services.
    4. User completes onboarding.
    5. User verifies GDPR compliance features (data export).
    """
    print("\n[E2E] Starting Onboarding flow...")

    # Step 1: Business Profile
    profile_data = {
        "companyName": "Test Corp",
        "industry": "Technology",
        "location": "San Francisco",
        "website": "https://testcorp.io"
    }
    response = client.post("/api/onboarding/business-profile", json=profile_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    session_id = response.json()["sessionId"]
    print(f"[E2E] Profile saved. Session: {session_id}")

    # Step 2: Digital Presence Detection
    presence_data = {
        "websiteDetected": True,
        "cmsType": "wordpress",
        "crmType": "fluent-crm",
        "hasTracking": True
    }
    response = client.post("/api/onboarding/digital-presence", json=presence_data)
    assert response.status_code == 200
    print("[E2E] Digital presence data updated.")

    # Step 3: Magic Discovery (New Feature)
    response = client.get("/api/onboarding/magic-discovery")
    assert response.status_code == 200
    discovered = response.json()
    assert "google" in discovered
    assert discovered["google"]["detected"] is True
    print(f"[E2E] Magic Discovery found: {list(discovered.keys())}")

    # Step 4: Complete Onboarding
    complete_payload = {
        "currentStep": 8,
        "profile": profile_data,
        "digitalPresence": presence_data,
        "analytics": {"GAId": "UA-12345", "setupLater": False},
        "socialMedia": {"platforms": ["facebook", "linkedin"]},
        "goals": {
            "primaryGoal": "lead_gen",
            "monthlyBudget": 5000,
            "targetAudience": {"ageRange": "25-45", "interests": ["tech", "ai"]}
        },
        "tools": {"selectedMcps": ["google-ads", "hubspot"]},
        "agent": {"persona": "aggressive", "name": "Titan"},
        "isComplete": True
    }
    response = client.post("/api/onboarding/complete", json=complete_payload)
    assert response.status_code == 200
    print("[E2E] Onboarding complete. Redirecting to dashboard.")

    # Step 5: Verify GDPR Compliance (Sprint 3)
    print("[E2E] Testing GDPR data export...")
    export_payload = {
        "format": "json",
        "include_connectors": True,
        "include_campaigns": True,
        "include_conversations": True
    }
    response = client.post("/api/privacy/export", json=export_payload)
    assert response.status_code == 200
    export_data = response.json()
    assert export_data["status"] == "accepted"
    assert "export_id" in export_data
    print(f"[E2E] GDPR Export request accepted. ID: {export_data['export_id']}")

    # Step 6: Verify Strategy Validation Trigger (Sprint 2)
    print("[E2E] Testing AI Strategy Validation...")
    validation_req = {
        "goal": "lead_gen",
        "budget": 2500.0,
        "platforms": ["google-ads", "facebook-ads"],
        "industry": "Real Estate"
    }
    response = client.post("/api/campaigns/validate-strategy", json=validation_req)
    assert response.status_code == 200
    assert "validation_id" in response.json()
    print("[E2E] AI Strategy validation workflow triggered.")

    print("\n[E2E] ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_onboarding_to_compliance_e2e()
