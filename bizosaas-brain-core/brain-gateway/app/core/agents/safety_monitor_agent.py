"""
SafetyMonitorAgent — continuous safety and tenant isolation enforcement.
Runs as a scheduled cron job, scanning recent agent outputs for anomalies.
"""
import logging
import re
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SafetyMonitorAgent:
    """
    Scans the platform for safety violations and tenant isolation breaches.
    Works alongside GovernanceAgent (real-time) as a periodic auditor.
    """

    # Patterns that flag cross-tenant data leakage
    ISOLATION_PATTERNS = [
        r"tenant_id\s*[:=]\s*['\"](?!{expected})",   # references unexpected tenant
        r"SELECT.*FROM.*WHERE(?!.*tenant_id)",          # query missing tenant filter
        r"Authorization:.*Bearer\s+[A-Za-z0-9._-]{20,}", # raw JWT in output
    ]

    # Keywords that suggest an anomaly
    ANOMALY_KEYWORDS = [
        "drop table", "truncate", "delete from users",
        "rm -rf", "sudo", "chmod 777",
        "os.system", "subprocess.call", "eval(",
    ]

    def __init__(self):
        self.violations: List[Dict[str, Any]] = []

    # ─────────────────────────────────────────────────────────────────────────
    # Core scan methods
    # ─────────────────────────────────────────────────────────────────────────

    async def scan_recent_outputs(
        self, db, hours: int = 1
    ) -> Dict[str, Any]:
        """
        Scans AuditLog entries from the last N hours for safety anomalies.
        Returns a report with flagged entries.
        """
        from app.models.user import AuditLog
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        recent_logs = (
            db.query(AuditLog)
            .filter(AuditLog.created_at >= cutoff)
            .all()
        )

        flagged = []
        for log in recent_logs:
            details_str = str(log.details or "").lower()
            issues = self._check_for_anomalies(details_str)
            if issues:
                flagged.append({
                    "log_id": str(log.id),
                    "user_id": str(log.user_id),
                    "action": log.action,
                    "timestamp": log.created_at.isoformat(),
                    "issues": issues,
                })

        self.violations = flagged
        logger.info(
            f"SafetyMonitorAgent scan complete: {len(recent_logs)} logs checked, "
            f"{len(flagged)} flagged."
        )
        return {
            "scanned_at": datetime.utcnow().isoformat(),
            "period_hours": hours,
            "logs_checked": len(recent_logs),
            "violations_found": len(flagged),
            "flagged_entries": flagged,
        }

    async def enforce_tenant_isolation(
        self, requesting_tenant_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validates that data in a response belongs only to the requesting tenant.
        Returns sanitized data or raises an isolation breach warning.
        """
        if "tenant_id" in data and str(data["tenant_id"]) != requesting_tenant_id:
            logger.error(
                f"ISOLATION BREACH: tenant {requesting_tenant_id} received "
                f"data for tenant {data['tenant_id']}"
            )
            return {
                "breach": True,
                "message": "Tenant isolation violation detected and blocked.",
                "requesting_tenant": requesting_tenant_id,
            }
        return {"breach": False, "data": data}

    async def run_health_check(self, db) -> Dict[str, Any]:
        """
        Basic platform health metrics for the scheduled health-check cron job.
        """
        from app.models.user import User, AuditLog
        from app.models.agent import Agent

        user_count = db.query(User).count()
        agent_count = db.query(Agent).count()
        log_count = (
            db.query(AuditLog)
            .filter(AuditLog.created_at >= datetime.utcnow() - timedelta(hours=24))
            .count()
        )

        return {
            "checked_at": datetime.utcnow().isoformat(),
            "status": "healthy",
            "metrics": {
                "total_users": user_count,
                "total_agents": agent_count,
                "audit_events_24h": log_count,
            },
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _check_for_anomalies(self, text: str) -> List[str]:
        issues = []
        for keyword in self.ANOMALY_KEYWORDS:
            if keyword in text:
                issues.append(f"Suspicious keyword detected: '{keyword}'")
        return issues


# Singleton
safety_monitor_agent = SafetyMonitorAgent()
