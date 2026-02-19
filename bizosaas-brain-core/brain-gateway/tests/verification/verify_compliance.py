"""
Verification script for Phase 9: Compliance & Trust.
Tests ComplianceService functions and ComplianceAgent prompt routing.
"""
import asyncio
import logging
from unittest.mock import MagicMock, patch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def make_mock_db(user=None, audit_logs=None, user_count=5):
    """Create a mock SQLAlchemy Session."""
    db = MagicMock()

    mock_user_query = MagicMock()
    mock_user_query.filter.return_value.first.return_value = user
    mock_user_query.count.return_value = user_count

    mock_log_query = MagicMock()
    mock_log_query.filter.return_value.order_by.return_value.limit.return_value.all.return_value = audit_logs or []
    mock_log_query.order_by.return_value.limit.return_value.first.return_value = (audit_logs or [None])[0]

    def query_side_effect(model):
        from app.models.user import User, AuditLog
        if model is User:
            return mock_user_query
        return mock_log_query

    db.query.side_effect = query_side_effect
    return db


async def test_gdpr_export():
    print("\n1. Testing GDPR Data Export...")
    from app.services.compliance_service import ComplianceService
    from app.models.user import User
    import uuid

    service = ComplianceService()
    user_id = str(uuid.uuid4())

    mock_user = MagicMock(spec=User)
    mock_user.id = uuid.UUID(user_id)
    mock_user.email = "test@example.com"
    mock_user.first_name = "Test"
    mock_user.last_name = "User"
    mock_user.role = "tenant_admin"
    mock_user.created_at = None
    mock_user.platform_preferences = {"theme": "dark"}
    mock_user.permissions = ["read", "write"]

    db = make_mock_db(user=mock_user, audit_logs=[])

    result = await service.export_user_data(user_id, db)
    assert "error" not in result, f"Export failed: {result}"
    assert result["profile"]["email"] == "test@example.com"
    assert result.get("gdpr_basis"), "Missing gdpr_basis in export"
    print(f"   ✅ GDPR export OK for user {user_id[:8]}...")


async def test_gdpr_anonymize():
    print("\n2. Testing GDPR Anonymization (Right to be Forgotten)...")
    from app.services.compliance_service import ComplianceService
    from app.models.user import User
    import uuid

    service = ComplianceService()
    user_id = str(uuid.uuid4())

    mock_user = MagicMock(spec=User)
    mock_user.id = uuid.UUID(user_id)
    mock_user.email = "test@example.com"

    db = make_mock_db(user=mock_user, audit_logs=[])

    result = await service.anonymize_user_data(user_id, db)
    assert "error" not in result, f"Anonymize failed: {result}"
    assert result["status"] == "success"
    assert "anon_" in result["anonymized_id"]
    assert mock_user.email.endswith("@deleted.bizosaas.com")
    print(f"   ✅ User anonymized → {mock_user.email}")


async def test_regulatory_status():
    print("\n3. Testing Regulatory Status Check...")
    from app.services.compliance_service import ComplianceService

    service = ComplianceService()
    db = make_mock_db(audit_logs=[MagicMock()], user_count=42)

    status = await service.get_regulatory_status(db)
    assert status["GDPR"]["status"] == "compliant"
    assert status["SOC2"]["completion_pct"] >= 75
    assert status["HIPAA"]["status"] == "not_applicable"
    print(f"   ✅ GDPR: {status['GDPR']['status']}, SOC2: {status['SOC2']['completion_pct']}%, HIPAA: {status['HIPAA']['status']}")


async def test_compliance_prompt_routing():
    print("\n4. Testing ComplianceAgent Prompt Routing...")
    from app.core.prompt_enhancer import PromptEnhancer
    enhancer = PromptEnhancer.__new__(PromptEnhancer)

    # Mock the DB to return no template (to trigger fallback)
    mock_session = MagicMock()
    query_mock = MagicMock()
    query_mock.filter.return_value.order_by.return_value.first.return_value = None
    query_mock.filter.return_value.first.return_value = None
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)
    mock_session.query.return_value = query_mock

    enhancer.Session = MagicMock(return_value=mock_session)

    template = await enhancer._find_template("compliance_specialist", "test_tenant")
    assert template is not None, "Compliance template not found"
    assert "GDPR" in template.template_text
    assert "SOC2" in template.template_text
    print("   ✅ ComplianceAgent prompt loaded via fallback routing")


async def test_gitignore_covers_env():
    print("\n5. Testing .gitignore coverage for .env files...")
    import subprocess
    result = subprocess.run(
        ["git", "check-ignore", "-v", "bizosaas-brain-core/brain-gateway/.env"],
        capture_output=True, text=True,
        cwd="/home/alagiri/projects/bizosaas-platform"
    )
    assert result.returncode == 0, f".env is NOT ignored by git! ({result.stdout.strip()})"
    print(f"   ✅ .env is ignored: {result.stdout.strip()}")


async def main():
    print("\n" + "="*55)
    print("  Phase 9: Compliance & Trust — Verification Suite")
    print("="*55)
    await test_gdpr_export()
    await test_gdpr_anonymize()
    await test_regulatory_status()
    await test_compliance_prompt_routing()
    await test_gitignore_covers_env()
    print("\n🎉 All Phase 9 Compliance checks passed!")
    print("="*55)

if __name__ == "__main__":
    asyncio.run(main())
