"""
Admin Prime Copilot
High-level orchestration agent that assists the platform owner in managing
the entire BizOSaaS ecosystem through intelligent analysis and recommendations.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

logger = logging.getLogger(__name__)


class AdminPrimeCopilot:
    """
    AI-powered copilot that provides intelligent insights and recommendations
    to the platform administrator for managing the entire ecosystem.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.agent_id = "admin_prime_v1"
    
    async def generate_daily_brief(self) -> Dict[str, Any]:
        """
        Generate a comprehensive daily briefing for the platform admin.
        """
        logger.info("Generating daily brief...")
        
        # Gather data from all subsystems
        tenant_summary = await self._analyze_tenant_health()
        workflow_summary = await self._analyze_workflow_performance()
        discovery_summary = await self._analyze_discovery_activity()
        financial_summary = await self._analyze_financial_metrics()
        system_health = await self._analyze_system_health()
        
        # Generate AI-powered insights
        insights = await self._generate_insights({
            "tenants": tenant_summary,
            "workflows": workflow_summary,
            "discovery": discovery_summary,
            "financials": financial_summary,
            "system": system_health
        })
        
        # Prioritize action items
        action_items = await self._prioritize_action_items(insights)
        
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "tenants": tenant_summary,
                "workflows": workflow_summary,
                "discovery": discovery_summary,
                "financials": financial_summary,
                "system_health": system_health
            },
            "insights": insights,
            "action_items": action_items,
            "recommendations": await self._generate_recommendations(insights)
        }
    
    async def _analyze_tenant_health(self) -> Dict[str, Any]:
        """
        Analyze overall tenant health and engagement.
        """
        from app.models.user import User
        from app.models.onboarding import OnboardingSession
        
        # Total tenants
        total_tenants = self.db.query(User).filter(User.role == "tenant").count()
        
        # Active tenants (logged in within 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        active_tenants = self.db.query(User).filter(
            User.role == "tenant",
            User.last_login >= seven_days_ago
        ).count()
        
        # Onboarding completion rate
        total_sessions = self.db.query(OnboardingSession).count()
        completed_sessions = self.db.query(OnboardingSession).filter(
            OnboardingSession.completed == True
        ).count()
        
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Churn risk (tenants who haven't logged in for 30+ days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        at_risk = self.db.query(User).filter(
            User.role == "tenant",
            User.last_login < thirty_days_ago
        ).count()
        
        return {
            "total_tenants": total_tenants,
            "active_tenants": active_tenants,
            "activity_rate": round((active_tenants / total_tenants * 100) if total_tenants > 0 else 0, 2),
            "onboarding_completion_rate": round(completion_rate, 2),
            "at_risk_count": at_risk,
            "health_score": self._calculate_tenant_health_score(active_tenants, total_tenants, at_risk)
        }
    
    async def _analyze_workflow_performance(self) -> Dict[str, Any]:
        """
        Analyze workflow execution performance.
        """
        from app.services.workflow_monitor import WorkflowMonitor
        
        monitor = WorkflowMonitor(self.db)
        metrics = await monitor.get_aggregated_metrics(time_range_hours=24)
        
        return {
            "total_executions_24h": metrics.total_executions,
            "success_rate": round(metrics.success_rate, 2),
            "average_duration": round(metrics.average_duration_seconds, 2),
            "total_cost_24h": round(metrics.total_cost, 2),
            "top_failing_workflows": metrics.top_failing_workflows[:3],
            "performance_score": self._calculate_workflow_performance_score(metrics)
        }
    
    async def _analyze_discovery_activity(self) -> Dict[str, Any]:
        """
        Analyze workflow discovery agent activity.
        """
        from app.models.workflow_proposal import WorkflowProposal
        
        # Proposals in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_proposals = self.db.query(WorkflowProposal).filter(
            WorkflowProposal.created_at >= seven_days_ago
        ).count()
        
        # Pending approvals
        pending = self.db.query(WorkflowProposal).filter(
            WorkflowProposal.status == "proposed"
        ).count()
        
        # Approval rate
        total_proposals = self.db.query(WorkflowProposal).count()
        approved = self.db.query(WorkflowProposal).filter(
            WorkflowProposal.status == "approved"
        ).count()
        
        approval_rate = (approved / total_proposals * 100) if total_proposals > 0 else 0
        
        return {
            "proposals_last_7_days": recent_proposals,
            "pending_approvals": pending,
            "total_proposals": total_proposals,
            "approval_rate": round(approval_rate, 2),
            "discovery_health": "active" if recent_proposals > 0 else "idle"
        }
    
    async def _analyze_financial_metrics(self) -> Dict[str, Any]:
        """
        Analyze financial performance (placeholder for Lago integration).
        """
        # TODO: Integrate with Lago for real financial data
        return {
            "mrr": 0,  # Monthly Recurring Revenue
            "arr": 0,  # Annual Recurring Revenue
            "churn_rate": 0,
            "ltv": 0,  # Lifetime Value
            "cac": 0,  # Customer Acquisition Cost
            "note": "Financial metrics integration pending"
        }
    
    async def _analyze_system_health(self) -> Dict[str, Any]:
        """
        Analyze overall system health.
        """
        from app.services.workflow_monitor import WorkflowMonitor
        
        monitor = WorkflowMonitor(self.db)
        last_hour = await monitor.get_aggregated_metrics(time_range_hours=1)
        
        # Determine health status
        if last_hour.success_rate >= 95:
            status = "excellent"
        elif last_hour.success_rate >= 80:
            status = "good"
        elif last_hour.success_rate >= 50:
            status = "degraded"
        else:
            status = "critical"
        
        return {
            "status": status,
            "workflow_success_rate_1h": round(last_hour.success_rate, 2),
            "active_workflows": self.db.query(func.count()).select_from(
                self.db.query(func.distinct(self.db.query(WorkflowProposal).filter(
                    WorkflowProposal.status == "approved"
                ).subquery().c.id)).subquery()
            ).scalar() or 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _generate_insights(self, data: Dict[str, Any]) -> List[str]:
        """
        Generate AI-powered insights from the data.
        """
        insights = []
        
        # Tenant insights
        if data["tenants"]["activity_rate"] < 50:
            insights.append(f"⚠️ Tenant activity rate is low at {data['tenants']['activity_rate']}%. Consider engagement campaigns.")
        
        if data["tenants"]["at_risk_count"] > 0:
            insights.append(f"🚨 {data['tenants']['at_risk_count']} tenants at risk of churn. Immediate outreach recommended.")
        
        # Workflow insights
        if data["workflows"]["success_rate"] < 90:
            insights.append(f"⚠️ Workflow success rate at {data['workflows']['success_rate']}%. Review top failing workflows.")
        
        if len(data["workflows"]["top_failing_workflows"]) > 0:
            top_failure = data["workflows"]["top_failing_workflows"][0]
            insights.append(f"🔧 '{top_failure['workflow_name']}' has {top_failure['failure_count']} failures. Requires attention.")
        
        # Discovery insights
        if data["discovery"]["pending_approvals"] > 5:
            insights.append(f"📋 {data['discovery']['pending_approvals']} workflow proposals awaiting review. Approval backlog detected.")
        
        if data["discovery"]["discovery_health"] == "idle":
            insights.append("💤 Discovery agent idle. No new proposals in 7 days. System may be missing optimization opportunities.")
        
        # System health insights
        if data["system"]["status"] in ["degraded", "critical"]:
            insights.append(f"🚨 System health is {data['system']['status'].upper()}. Immediate investigation required.")
        
        return insights
    
    async def _prioritize_action_items(self, insights: List[str]) -> List[Dict[str, Any]]:
        """
        Convert insights into prioritized action items.
        """
        action_items = []
        
        for insight in insights:
            priority = "high" if "🚨" in insight else ("medium" if "⚠️" in insight else "low")
            
            action_items.append({
                "priority": priority,
                "insight": insight,
                "category": self._categorize_insight(insight),
                "suggested_action": self._suggest_action(insight)
            })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        action_items.sort(key=lambda x: priority_order[x["priority"]])
        
        return action_items
    
    async def _generate_recommendations(self, insights: List[str]) -> List[str]:
        """
        Generate strategic recommendations based on insights.
        """
        recommendations = []
        
        if any("churn" in i.lower() for i in insights):
            recommendations.append("Implement automated re-engagement workflows for at-risk tenants")
        
        if any("approval backlog" in i.lower() for i in insights):
            recommendations.append("Schedule dedicated time for workflow proposal reviews")
        
        if any("failing" in i.lower() for i in insights):
            recommendations.append("Enable auto-pause for workflows with >50% failure rate")
        
        if any("idle" in i.lower() for i in insights):
            recommendations.append("Review discovery agent configuration and data sources")
        
        return recommendations
    
    def _calculate_tenant_health_score(self, active: int, total: int, at_risk: int) -> float:
        """Calculate overall tenant health score (0-100)."""
        if total == 0:
            return 0
        
        activity_score = (active / total) * 60  # 60% weight
        churn_penalty = (at_risk / total) * 40  # 40% penalty
        
        return max(0, min(100, activity_score - churn_penalty))
    
    def _calculate_workflow_performance_score(self, metrics) -> float:
        """Calculate workflow performance score (0-100)."""
        success_weight = 0.7
        efficiency_weight = 0.3
        
        success_score = metrics.success_rate * success_weight
        
        # Efficiency based on average duration (lower is better, assume 30s is ideal)
        ideal_duration = 30
        efficiency_score = max(0, 100 - (metrics.average_duration_seconds - ideal_duration)) * efficiency_weight
        
        return min(100, success_score + efficiency_score)
    
    def _categorize_insight(self, insight: str) -> str:
        """Categorize an insight."""
        if "tenant" in insight.lower() or "churn" in insight.lower():
            return "tenant_management"
        elif "workflow" in insight.lower():
            return "workflow_operations"
        elif "discovery" in insight.lower() or "proposal" in insight.lower():
            return "agentic_operations"
        elif "system" in insight.lower():
            return "infrastructure"
        else:
            return "general"
    
    def _suggest_action(self, insight: str) -> str:
        """Suggest an action based on the insight."""
        if "churn" in insight.lower():
            return "Review tenant engagement metrics and initiate outreach campaign"
        elif "failing" in insight.lower():
            return "Investigate workflow logs and consider pausing until fixed"
        elif "approval" in insight.lower():
            return "Review pending proposals in Admin Portal > Workflows > HITL tab"
        elif "idle" in insight.lower():
            return "Check discovery agent logs and verify data source connections"
        elif "degraded" in insight.lower() or "critical" in insight.lower():
            return "Check system logs and infrastructure metrics immediately"
        else:
            return "Monitor situation and review in next daily brief"


async def get_admin_prime_copilot(db: Session) -> AdminPrimeCopilot:
    """Helper to get Admin Prime Copilot instance."""
    return AdminPrimeCopilot(db)
