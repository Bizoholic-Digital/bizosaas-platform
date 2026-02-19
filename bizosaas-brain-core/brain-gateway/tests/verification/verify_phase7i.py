"""
Verification for Phase 7I: Cron Job System + AI Safety
Tests CronJob model, API, and SafetyMonitorAgent.
"""
import asyncio
import logging
from unittest.mock import MagicMock
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def make_mock_db(logs=None, user_count=10, agent_count=5):
    db = MagicMock()
    mock_audit_query = MagicMock()
    mock_audit_query.filter.return_value.all.return_value = logs or []
    mock_audit_query.filter.return_value.count.return_value = len(logs or [])
    mock_audit_query.filter.return_value.order_by.return_value.limit.return_value.first.return_value = None

    mock_user_query = MagicMock()
    mock_user_query.count.return_value = user_count

    mock_agent_query = MagicMock()
    mock_agent_query.count.return_value = agent_count

    mock_cron_query = MagicMock()
    mock_cron_query.filter.return_value.first.return_value = None
    mock_cron_query.order_by.return_value.all.return_value = []

    def query_side(model):
        from app.models.user import AuditLog, User
        try:
            from app.models.agent import Agent
            if model is Agent:
                return mock_agent_query
        except Exception:
            pass
        if model is AuditLog:
            return mock_audit_query
        if model is User:
            return mock_user_query
        return mock_cron_query

    db.query.side_effect = query_side
    return db


async def test_cron_job_model():
    print("\n1. Testing CronJob model import...")
    from app.models.cron_job import CronJob, CronJobType, CronJobStatus
    import uuid
    job = CronJob(
        id=uuid.uuid4(),
        name="test-cleanup",
        job_type=CronJobType.cleanup,
        schedule="0 2 * * *",
        status=CronJobStatus.active,
        is_system=True,
    )
    assert job.name == "test-cleanup"
    assert job.job_type == CronJobType.cleanup
    assert job.status == CronJobStatus.active
    print("   ✅ CronJob model: OK")


async def test_default_cron_jobs_defined():
    print("\n2. Testing DEFAULT_CRON_JOBS definition...")
    from app.temporal_workflows.cron_workflow import DEFAULT_CRON_JOBS, CronJobWorkflow
    assert len(DEFAULT_CRON_JOBS) == 5
    names = [j["name"] for j in DEFAULT_CRON_JOBS]
    assert "daily-cleanup" in names
    assert "hourly-security-scan" in names
    assert "health-check" in names
    assert "weekly-optimization" in names
    assert "daily-compliance-check" in names
    print(f"   ✅ {len(DEFAULT_CRON_JOBS)} default system cron jobs defined: {names}")


async def test_safety_monitor_scan():
    print("\n3. Testing SafetyMonitorAgent scan (no anomalies)...")
    from app.core.agents.safety_monitor_agent import SafetyMonitorAgent
    agent = SafetyMonitorAgent()
    db = make_mock_db(logs=[])
    report = await agent.scan_recent_outputs(db, hours=1)
    assert report["violations_found"] == 0
    print(f"   ✅ Clean scan: {report['logs_checked']} logs checked, 0 violations")


async def test_safety_monitor_detects_anomaly():
    print("\n4. Testing SafetyMonitorAgent anomaly detection...")
    from app.core.agents.safety_monitor_agent import SafetyMonitorAgent
    from app.models.user import AuditLog
    import uuid

    agent = SafetyMonitorAgent()

    # Mock log with dangerous keyword
    suspicious_log = MagicMock(spec=AuditLog)
    suspicious_log.id = uuid.uuid4()
    suspicious_log.user_id = uuid.uuid4()
    suspicious_log.action = "agent_response"
    suspicious_log.details = "output: drop table users; try rm -rf /data"
    suspicious_log.created_at = datetime.utcnow()

    db = make_mock_db(logs=[suspicious_log])
    report = await agent.scan_recent_outputs(db, hours=1)
    assert report["violations_found"] >= 1
    print(f"   ✅ Anomaly detected: {report['violations_found']} violation(s) flagged")


async def test_safety_monitor_health_check():
    print("\n5. Testing SafetyMonitorAgent health check...")
    from app.core.agents.safety_monitor_agent import SafetyMonitorAgent
    agent = SafetyMonitorAgent()
    db = make_mock_db()
    result = await agent.run_health_check(db)
    assert result["status"] == "healthy"
    print(f"   ✅ Health check: {result['metrics']}")


async def test_tenant_isolation():
    print("\n6. Testing tenant isolation enforcement...")
    from app.core.agents.safety_monitor_agent import SafetyMonitorAgent
    agent = SafetyMonitorAgent()

    # Matching tenant — no breach
    clean = await agent.enforce_tenant_isolation("tenant-A", {"tenant_id": "tenant-A", "data": "ok"})
    assert not clean["breach"]

    # Mismatched tenant — breach!
    breach = await agent.enforce_tenant_isolation("tenant-A", {"tenant_id": "tenant-B", "data": "secret"})
    assert breach["breach"]
    print("   ✅ Isolation: clean pass OK, breach detected and blocked OK")


async def test_gha_workflows_exist():
    print("\n7. Testing GHA workflow files exist...")
    import os
    base = "/home/alagiri/projects/bizosaas-platform/.github/workflows"
    required = [
        "_reusable-deploy.yml",
        "deploy-admin-portal.yml",
        "deploy-business-directory.yml",
        "deploy-wagtail.yml",
        "deploy-docs.yml",
    ]
    for f in required:
        path = os.path.join(base, f)
        assert os.path.exists(path), f"Missing: {path}"
        print(f"   ✅ {f}")


async def main():
    print("\n" + "="*55)
    print("  Phase 7I: Cron Jobs + AI Safety — Verification")
    print("="*55)
    await test_cron_job_model()
    await test_default_cron_jobs_defined()
    await test_safety_monitor_scan()
    await test_safety_monitor_detects_anomaly()
    await test_safety_monitor_health_check()
    await test_tenant_isolation()
    await test_gha_workflows_exist()
    print("\n🎉 All Phase 7I checks passed!")
    print("="*55)


if __name__ == "__main__":
    asyncio.run(main())
