"""
Content Marketing HITL (Human-in-the-Loop) Approval Workflows
Advanced approval workflow system for content marketing automation with progressive automation levels

This module implements sophisticated HITL approval workflows that balance automation efficiency
with human oversight, supporting progressive automation levels and conservative estimation.

Key Features:
- Progressive automation levels (Level 1-5)
- Risk-based approval routing
- Automated escalation workflows
- Performance-based approval confidence
- Conservative estimation with safety buffers
- Learning and optimization from approval patterns
- Multi-stakeholder approval workflows
- Crisis management escalation
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field
import uuid
import structlog

# Temporal imports for workflow orchestration
from temporal import activity, workflow
from temporal.workflow import WorkflowHandle

# Import content marketing models
from app.models.content_marketing_models import (
    ContentType, ContentStatus, ContentPlatform, HITLApprovalType, AutomationLevel,
    HITLApprovalWorkflow, ContentPiece, ContentStrategy
)

# Set up structured logging
logger = structlog.get_logger(__name__)

class ApprovalDecision(Enum):
    """Approval decision types"""
    APPROVED = "approved"
    REJECTED = "rejected"
    APPROVED_WITH_MODIFICATIONS = "approved_with_modifications"
    ESCALATED = "escalated"
    PENDING_REVIEW = "pending_review"
    AUTO_APPROVED = "auto_approved"

class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ApprovalPriority(Enum):
    """Approval priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

@dataclass
class ApprovalContext:
    """Context for approval decisions"""
    tenant_id: str
    content_id: Optional[str] = None
    workflow_id: Optional[str] = None
    approval_type: HITLApprovalType = HITLApprovalType.CONTENT_STRATEGY
    automation_level: AutomationLevel = AutomationLevel.LEVEL_2_ASSISTED
    risk_level: RiskLevel = RiskLevel.MEDIUM
    priority: ApprovalPriority = ApprovalPriority.MEDIUM
    requester_id: str = ""
    business_impact: str = "medium"
    deadline: Optional[datetime] = None
    escalation_rules: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ApprovalCriteria:
    """Criteria for approval evaluation"""
    brand_compliance_threshold: float = 0.85
    quality_score_threshold: float = 0.8
    risk_tolerance_level: RiskLevel = RiskLevel.MEDIUM
    ai_confidence_threshold: float = 0.75
    performance_prediction_threshold: float = 0.7
    legal_review_required: bool = False
    executive_approval_required: bool = False
    technical_review_required: bool = False

@dataclass
class ApprovalResult:
    """Result of approval evaluation"""
    decision: ApprovalDecision
    confidence_score: float
    reasoning: List[str]
    modifications_required: Dict[str, Any] = field(default_factory=dict)
    escalation_path: List[str] = field(default_factory=list)
    estimated_approval_time: Optional[timedelta] = None
    reviewer_assignments: List[str] = field(default_factory=list)
    follow_up_actions: List[str] = field(default_factory=list)

class ContentMarketingHITLWorkflows:
    """Main HITL workflow orchestrator for content marketing"""
    
    def __init__(self):
        self.approval_queue = {}
        self.approval_history = {}
        self.automation_learning = {}
        self.performance_metrics = {
            "total_approvals": 0,
            "auto_approval_rate": 0.0,
            "average_approval_time": 0.0,
            "escalation_rate": 0.0,
            "rejection_rate": 0.0
        }
        self.logger = structlog.get_logger(__name__)
    
    async def initiate_approval_workflow(
        self,
        context: ApprovalContext,
        content_data: Dict[str, Any],
        criteria: ApprovalCriteria
    ) -> str:
        """Initiate HITL approval workflow"""
        
        approval_id = str(uuid.uuid4())
        
        try:
            # Perform initial risk assessment
            risk_assessment = await self._assess_content_risk(content_data, context)
            
            # Determine approval path based on automation level and risk
            approval_path = await self._determine_approval_path(
                context, risk_assessment, criteria
            )
            
            # Create approval workflow entry
            approval_workflow = {
                "approval_id": approval_id,
                "context": context.__dict__,
                "content_data": content_data,
                "criteria": criteria.__dict__,
                "risk_assessment": risk_assessment,
                "approval_path": approval_path,
                "status": "initiated",
                "created_at": datetime.now(),
                "timeline": []
            }
            
            self.approval_queue[approval_id] = approval_workflow
            
            # Execute approval workflow based on path
            if approval_path["auto_approval_eligible"]:
                result = await self._execute_auto_approval(approval_id)
            else:
                result = await self._execute_manual_approval(approval_id)
            
            self.logger.info(
                f"Approval workflow initiated",
                approval_id=approval_id,
                tenant_id=context.tenant_id,
                approval_type=context.approval_type.value,
                automation_level=context.automation_level.value
            )
            
            return approval_id
            
        except Exception as e:
            self.logger.error(f"Approval workflow initiation failed", 
                            approval_id=approval_id, error=str(e))
            raise
    
    async def _assess_content_risk(
        self,
        content_data: Dict[str, Any],
        context: ApprovalContext
    ) -> Dict[str, Any]:
        """Assess risk level of content for approval routing"""
        
        risk_factors = {
            "brand_sensitivity": 0.0,
            "legal_compliance": 0.0,
            "business_impact": 0.0,
            "technical_complexity": 0.0,
            "audience_sensitivity": 0.0
        }
        
        # Brand sensitivity assessment
        brand_keywords = ["CEO", "executive", "crisis", "controversy", "legal"]
        content_text = str(content_data.get("content", "")).lower()
        brand_sensitivity = sum(1 for keyword in brand_keywords if keyword in content_text) / len(brand_keywords)
        risk_factors["brand_sensitivity"] = brand_sensitivity
        
        # Legal compliance assessment
        legal_keywords = ["claim", "guarantee", "medical", "financial", "lawsuit"]
        legal_risk = sum(1 for keyword in legal_keywords if keyword in content_text) / len(legal_keywords)
        risk_factors["legal_compliance"] = legal_risk
        
        # Business impact assessment
        business_impact_map = {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
            "critical": 1.0
        }
        risk_factors["business_impact"] = business_impact_map.get(context.business_impact, 0.5)
        
        # Technical complexity assessment
        technical_indicators = content_data.get("technical_requirements", [])
        risk_factors["technical_complexity"] = min(len(technical_indicators) / 5, 1.0)
        
        # Audience sensitivity assessment
        sensitive_topics = ["politics", "religion", "health", "finance", "personal"]
        audience_risk = sum(1 for topic in sensitive_topics if topic in content_text) / len(sensitive_topics)
        risk_factors["audience_sensitivity"] = audience_risk
        
        # Calculate overall risk score
        overall_risk = sum(risk_factors.values()) / len(risk_factors)
        
        # Determine risk level
        if overall_risk < 0.3:
            risk_level = RiskLevel.LOW
        elif overall_risk < 0.6:
            risk_level = RiskLevel.MEDIUM
        elif overall_risk < 0.8:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
        
        return {
            "risk_factors": risk_factors,
            "overall_risk_score": overall_risk,
            "risk_level": risk_level.value,
            "risk_reasoning": self._generate_risk_reasoning(risk_factors),
            "recommended_approvers": self._recommend_approvers(risk_level, context)
        }
    
    def _generate_risk_reasoning(self, risk_factors: Dict[str, float]) -> List[str]:
        """Generate human-readable risk reasoning"""
        reasoning = []
        
        if risk_factors["brand_sensitivity"] > 0.5:
            reasoning.append("Content contains brand-sensitive keywords requiring review")
        
        if risk_factors["legal_compliance"] > 0.3:
            reasoning.append("Potential legal compliance concerns detected")
        
        if risk_factors["business_impact"] > 0.7:
            reasoning.append("High business impact content requires senior review")
        
        if risk_factors["technical_complexity"] > 0.6:
            reasoning.append("Technical complexity requires specialist review")
        
        if risk_factors["audience_sensitivity"] > 0.4:
            reasoning.append("Audience-sensitive topics require careful review")
        
        if not reasoning:
            reasoning.append("Low risk content suitable for standard approval process")
        
        return reasoning
    
    def _recommend_approvers(
        self,
        risk_level: RiskLevel,
        context: ApprovalContext
    ) -> List[str]:
        """Recommend appropriate approvers based on risk level"""
        
        approvers = []
        
        if risk_level == RiskLevel.LOW:
            approvers = ["content_manager"]
        elif risk_level == RiskLevel.MEDIUM:
            approvers = ["content_manager", "marketing_lead"]
        elif risk_level == RiskLevel.HIGH:
            approvers = ["marketing_lead", "brand_manager", "legal_review"]
        else:  # CRITICAL
            approvers = ["marketing_director", "brand_manager", "legal_counsel", "executive_team"]
        
        # Add specialized approvers based on content type
        if context.approval_type == HITLApprovalType.LEGAL_COMPLIANCE:
            approvers.append("legal_counsel")
        elif context.approval_type == HITLApprovalType.EXECUTIVE_CONTENT:
            approvers.append("executive_assistant")
        elif context.approval_type == HITLApprovalType.CRISIS_MANAGEMENT:
            approvers = ["crisis_manager", "pr_lead", "executive_team"]
        
        return list(set(approvers))  # Remove duplicates
    
    async def _determine_approval_path(
        self,
        context: ApprovalContext,
        risk_assessment: Dict[str, Any],
        criteria: ApprovalCriteria
    ) -> Dict[str, Any]:
        """Determine the appropriate approval path"""
        
        auto_approval_eligible = False
        approval_path = {
            "auto_approval_eligible": False,
            "required_approvers": risk_assessment["recommended_approvers"],
            "parallel_approval": False,
            "escalation_triggers": [],
            "estimated_duration": timedelta(hours=24)
        }
        
        # Check auto-approval eligibility based on automation level
        if context.automation_level in [AutomationLevel.LEVEL_4_AUTO_REVIEW, AutomationLevel.LEVEL_5_AUTONOMOUS]:
            if (risk_assessment["risk_level"] == RiskLevel.LOW.value and
                context.priority.value <= ApprovalPriority.MEDIUM.value):
                auto_approval_eligible = True
        
        # Override auto-approval for specific conditions
        if (context.approval_type in [HITLApprovalType.CRISIS_MANAGEMENT, HITLApprovalType.LEGAL_COMPLIANCE] or
            criteria.executive_approval_required or
            criteria.legal_review_required):
            auto_approval_eligible = False
        
        approval_path["auto_approval_eligible"] = auto_approval_eligible
        
        # Determine if parallel approval is beneficial
        if len(approval_path["required_approvers"]) > 2 and context.priority.value >= ApprovalPriority.HIGH.value:
            approval_path["parallel_approval"] = True
            approval_path["estimated_duration"] = timedelta(hours=12)
        
        # Set escalation triggers
        escalation_triggers = []
        if context.deadline:
            deadline_buffer = (context.deadline - datetime.now()).total_seconds() / 3600  # hours
            if deadline_buffer < 6:
                escalation_triggers.append("urgent_deadline")
        
        if context.priority == ApprovalPriority.CRITICAL:
            escalation_triggers.append("critical_priority")
        
        approval_path["escalation_triggers"] = escalation_triggers
        
        return approval_path
    
    async def _execute_auto_approval(self, approval_id: str) -> ApprovalResult:
        """Execute automated approval workflow"""
        
        approval_workflow = self.approval_queue[approval_id]
        content_data = approval_workflow["content_data"]
        criteria = approval_workflow["criteria"]
        
        # Perform automated quality checks
        quality_checks = await self._perform_quality_checks(content_data, criteria)
        
        # Make approval decision based on checks
        if all(check["passed"] for check in quality_checks["checks"]):
            decision = ApprovalDecision.AUTO_APPROVED
            confidence_score = quality_checks["overall_score"]
            reasoning = ["All automated quality checks passed"]
        else:
            decision = ApprovalDecision.PENDING_REVIEW
            confidence_score = quality_checks["overall_score"]
            reasoning = [check["reason"] for check in quality_checks["checks"] if not check["passed"]]
        
        # Update approval workflow
        approval_workflow["status"] = decision.value
        approval_workflow["auto_approval_result"] = quality_checks
        approval_workflow["timeline"].append({
            "timestamp": datetime.now(),
            "event": "auto_approval_completed",
            "decision": decision.value
        })
        
        result = ApprovalResult(
            decision=decision,
            confidence_score=confidence_score,
            reasoning=reasoning,
            estimated_approval_time=timedelta(minutes=5)  # Auto approval is fast
        )
        
        # Log approval decision
        self.logger.info(
            f"Auto approval completed",
            approval_id=approval_id,
            decision=decision.value,
            confidence_score=confidence_score
        )
        
        return result
    
    async def _execute_manual_approval(self, approval_id: str) -> ApprovalResult:
        """Execute manual approval workflow"""
        
        approval_workflow = self.approval_queue[approval_id]
        context = ApprovalContext(**approval_workflow["context"])
        approval_path = approval_workflow["approval_path"]
        
        # Assign to appropriate reviewers
        reviewer_assignments = await self._assign_reviewers(
            approval_id, 
            approval_path["required_approvers"]
        )
        
        # Create approval tasks
        approval_tasks = await self._create_approval_tasks(approval_id, reviewer_assignments)
        
        # Update approval workflow
        approval_workflow["status"] = "pending_review"
        approval_workflow["reviewer_assignments"] = reviewer_assignments
        approval_workflow["approval_tasks"] = approval_tasks
        approval_workflow["timeline"].append({
            "timestamp": datetime.now(),
            "event": "manual_approval_initiated",
            "reviewers": reviewer_assignments
        })
        
        # Estimate approval time based on reviewers and priority
        estimated_time = self._estimate_approval_time(
            len(reviewer_assignments),
            context.priority,
            approval_path["parallel_approval"]
        )
        
        result = ApprovalResult(
            decision=ApprovalDecision.PENDING_REVIEW,
            confidence_score=0.0,  # Will be updated when reviews complete
            reasoning=["Manual review required based on risk assessment"],
            reviewer_assignments=reviewer_assignments,
            estimated_approval_time=estimated_time
        )
        
        # Set up monitoring and escalation
        await self._setup_approval_monitoring(approval_id)
        
        self.logger.info(
            f"Manual approval initiated",
            approval_id=approval_id,
            reviewers=reviewer_assignments,
            estimated_time=estimated_time
        )
        
        return result
    
    async def _perform_quality_checks(
        self,
        content_data: Dict[str, Any],
        criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform automated quality checks"""
        
        checks = []
        
        # Brand compliance check
        brand_score = content_data.get("brand_compliance_score", 0.85)
        checks.append({
            "name": "brand_compliance",
            "passed": brand_score >= criteria.get("brand_compliance_threshold", 0.85),
            "score": brand_score,
            "reason": f"Brand compliance score: {brand_score:.2f}"
        })
        
        # Quality score check
        quality_score = content_data.get("quality_score", 0.8)
        checks.append({
            "name": "quality_score",
            "passed": quality_score >= criteria.get("quality_score_threshold", 0.8),
            "score": quality_score,
            "reason": f"Quality score: {quality_score:.2f}"
        })
        
        # AI confidence check
        ai_confidence = content_data.get("ai_confidence", 0.75)
        checks.append({
            "name": "ai_confidence",
            "passed": ai_confidence >= criteria.get("ai_confidence_threshold", 0.75),
            "score": ai_confidence,
            "reason": f"AI confidence: {ai_confidence:.2f}"
        })
        
        # Performance prediction check
        performance_prediction = content_data.get("performance_prediction", {}).get("engagement_rate", 0.7)
        checks.append({
            "name": "performance_prediction",
            "passed": performance_prediction >= criteria.get("performance_prediction_threshold", 0.7),
            "score": performance_prediction,
            "reason": f"Performance prediction: {performance_prediction:.2f}"
        })
        
        # Calculate overall score
        overall_score = sum(check["score"] for check in checks) / len(checks)
        
        return {
            "checks": checks,
            "overall_score": overall_score,
            "passed_checks": sum(1 for check in checks if check["passed"]),
            "total_checks": len(checks)
        }
    
    async def _assign_reviewers(
        self,
        approval_id: str,
        required_approvers: List[str]
    ) -> List[str]:
        """Assign specific reviewers to approval workflow"""
        
        # This would integrate with user management system
        # For now, using role-based assignments
        
        reviewer_assignments = []
        
        role_to_user_map = {
            "content_manager": "user_content_manager_1",
            "marketing_lead": "user_marketing_lead_1", 
            "brand_manager": "user_brand_manager_1",
            "legal_review": "user_legal_counsel_1",
            "marketing_director": "user_marketing_director_1",
            "crisis_manager": "user_crisis_manager_1",
            "executive_team": "user_executive_1"
        }
        
        for role in required_approvers:
            if role in role_to_user_map:
                reviewer_assignments.append(role_to_user_map[role])
        
        return reviewer_assignments
    
    async def _create_approval_tasks(
        self,
        approval_id: str,
        reviewer_assignments: List[str]
    ) -> List[Dict[str, Any]]:
        """Create approval tasks for reviewers"""
        
        approval_workflow = self.approval_queue[approval_id]
        
        tasks = []
        for reviewer in reviewer_assignments:
            task = {
                "task_id": str(uuid.uuid4()),
                "approval_id": approval_id,
                "reviewer_id": reviewer,
                "status": "assigned",
                "assigned_at": datetime.now(),
                "due_date": datetime.now() + timedelta(hours=24),
                "task_data": {
                    "content_summary": approval_workflow["content_data"].get("title", "Content Review"),
                    "approval_type": approval_workflow["context"]["approval_type"],
                    "priority": approval_workflow["context"]["priority"],
                    "risk_level": approval_workflow["risk_assessment"]["risk_level"]
                }
            }
            tasks.append(task)
        
        return tasks
    
    def _estimate_approval_time(
        self,
        num_reviewers: int,
        priority: ApprovalPriority,
        parallel_approval: bool
    ) -> timedelta:
        """Estimate approval completion time"""
        
        base_time_hours = {
            ApprovalPriority.LOW: 48,
            ApprovalPriority.MEDIUM: 24,
            ApprovalPriority.HIGH: 12,
            ApprovalPriority.URGENT: 6,
            ApprovalPriority.CRITICAL: 2
        }
        
        base_time = base_time_hours.get(priority, 24)
        
        if parallel_approval:
            # Parallel approval doesn't scale with reviewers
            estimated_hours = base_time
        else:
            # Sequential approval scales with reviewers
            estimated_hours = base_time * min(num_reviewers, 3)  # Cap at 3x
        
        # Add conservative buffer
        conservative_buffer = 1.4  # 40% buffer
        final_hours = estimated_hours * conservative_buffer
        
        return timedelta(hours=final_hours)
    
    async def _setup_approval_monitoring(self, approval_id: str):
        """Set up monitoring and escalation for approval workflow"""
        
        # This would set up monitoring tasks in Temporal or similar
        # For now, just logging the setup
        
        approval_workflow = self.approval_queue[approval_id]
        context = ApprovalContext(**approval_workflow["context"])
        
        monitoring_config = {
            "approval_id": approval_id,
            "check_interval": timedelta(hours=4),
            "escalation_triggers": approval_workflow["approval_path"]["escalation_triggers"],
            "deadline": context.deadline,
            "priority": context.priority.value
        }
        
        self.logger.info(
            f"Approval monitoring configured",
            approval_id=approval_id,
            monitoring_config=monitoring_config
        )
    
    async def process_approval_decision(
        self,
        approval_id: str,
        reviewer_id: str,
        decision: ApprovalDecision,
        comments: Optional[str] = None,
        modifications: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process reviewer's approval decision"""
        
        if approval_id not in self.approval_queue:
            raise ValueError(f"Approval workflow {approval_id} not found")
        
        approval_workflow = self.approval_queue[approval_id]
        
        # Record the decision
        decision_record = {
            "reviewer_id": reviewer_id,
            "decision": decision.value,
            "timestamp": datetime.now(),
            "comments": comments,
            "modifications": modifications
        }
        
        if "decisions" not in approval_workflow:
            approval_workflow["decisions"] = []
        
        approval_workflow["decisions"].append(decision_record)
        
        # Update timeline
        approval_workflow["timeline"].append({
            "timestamp": datetime.now(),
            "event": "reviewer_decision",
            "reviewer": reviewer_id,
            "decision": decision.value
        })
        
        # Check if all required approvals are complete
        completion_result = await self._check_approval_completion(approval_id)
        
        # Update performance metrics
        await self._update_approval_metrics(approval_id, decision)
        
        self.logger.info(
            f"Approval decision processed",
            approval_id=approval_id,
            reviewer_id=reviewer_id,
            decision=decision.value,
            completion_status=completion_result["status"]
        )
        
        return {
            "approval_id": approval_id,
            "decision_recorded": True,
            "completion_status": completion_result["status"],
            "final_decision": completion_result.get("final_decision"),
            "next_steps": completion_result.get("next_steps", [])
        }
    
    async def _check_approval_completion(self, approval_id: str) -> Dict[str, Any]:
        """Check if approval workflow is complete"""
        
        approval_workflow = self.approval_queue[approval_id]
        decisions = approval_workflow.get("decisions", [])
        required_approvers = approval_workflow["approval_path"]["required_approvers"]
        
        # Count decisions by type
        decision_counts = {}
        for decision in decisions:
            decision_type = decision["decision"]
            decision_counts[decision_type] = decision_counts.get(decision_type, 0) + 1
        
        # Determine completion status
        total_decisions = len(decisions)
        required_decisions = len(required_approvers)
        
        if total_decisions < required_decisions:
            return {
                "status": "pending",
                "progress": f"{total_decisions}/{required_decisions} decisions received"
            }
        
        # Determine final decision
        rejections = decision_counts.get("rejected", 0)
        approvals = decision_counts.get("approved", 0)
        modifications = decision_counts.get("approved_with_modifications", 0)
        
        if rejections > 0:
            final_decision = "rejected"
            next_steps = ["Review rejection feedback", "Revise content", "Resubmit for approval"]
        elif modifications > 0:
            final_decision = "approved_with_modifications"
            next_steps = ["Implement requested modifications", "Proceed with publication"]
        else:
            final_decision = "approved"
            next_steps = ["Proceed with publication", "Set up performance monitoring"]
        
        # Update workflow status
        approval_workflow["status"] = "completed"
        approval_workflow["final_decision"] = final_decision
        approval_workflow["completed_at"] = datetime.now()
        
        return {
            "status": "completed",
            "final_decision": final_decision,
            "decision_breakdown": decision_counts,
            "next_steps": next_steps
        }
    
    async def _update_approval_metrics(self, approval_id: str, decision: ApprovalDecision):
        """Update approval performance metrics"""
        
        approval_workflow = self.approval_queue[approval_id]
        
        # Update total approvals
        self.performance_metrics["total_approvals"] += 1
        
        # Update auto-approval rate
        if approval_workflow.get("auto_approval_result"):
            auto_approvals = sum(1 for w in self.approval_queue.values() 
                               if w.get("auto_approval_result"))
            self.performance_metrics["auto_approval_rate"] = auto_approvals / self.performance_metrics["total_approvals"]
        
        # Update average approval time
        if approval_workflow["status"] == "completed":
            start_time = approval_workflow["created_at"]
            end_time = approval_workflow.get("completed_at", datetime.now())
            approval_time = (end_time - start_time).total_seconds() / 3600  # hours
            
            current_avg = self.performance_metrics["average_approval_time"]
            total_approvals = self.performance_metrics["total_approvals"]
            self.performance_metrics["average_approval_time"] = (
                (current_avg * (total_approvals - 1) + approval_time) / total_approvals
            )
        
        # Update rejection rate
        if decision == ApprovalDecision.REJECTED:
            rejections = sum(1 for w in self.approval_queue.values()
                           if w.get("final_decision") == "rejected")
            self.performance_metrics["rejection_rate"] = rejections / self.performance_metrics["total_approvals"]
    
    async def get_approval_status(self, approval_id: str) -> Dict[str, Any]:
        """Get current status of approval workflow"""
        
        if approval_id not in self.approval_queue:
            raise ValueError(f"Approval workflow {approval_id} not found")
        
        approval_workflow = self.approval_queue[approval_id]
        
        # Calculate progress
        decisions = approval_workflow.get("decisions", [])
        required_approvers = approval_workflow["approval_path"]["required_approvers"]
        progress = len(decisions) / len(required_approvers) * 100
        
        # Estimate remaining time
        if approval_workflow["status"] in ["pending_review", "initiated"]:
            estimated_completion = approval_workflow["created_at"] + approval_workflow["approval_path"]["estimated_duration"]
        else:
            estimated_completion = None
        
        return {
            "approval_id": approval_id,
            "status": approval_workflow["status"],
            "progress": progress,
            "decisions_received": len(decisions),
            "required_decisions": len(required_approvers),
            "estimated_completion": estimated_completion,
            "timeline": approval_workflow["timeline"],
            "risk_assessment": approval_workflow["risk_assessment"],
            "current_reviewers": approval_workflow.get("reviewer_assignments", [])
        }
    
    async def get_approval_dashboard(self, tenant_id: str) -> Dict[str, Any]:
        """Get approval dashboard for tenant"""
        
        # Filter approvals for tenant
        tenant_approvals = {
            aid: workflow for aid, workflow in self.approval_queue.items()
            if workflow["context"]["tenant_id"] == tenant_id
        }
        
        # Calculate metrics
        total_approvals = len(tenant_approvals)
        pending_approvals = len([w for w in tenant_approvals.values() if w["status"] in ["initiated", "pending_review"]])
        completed_approvals = len([w for w in tenant_approvals.values() if w["status"] == "completed"])
        auto_approvals = len([w for w in tenant_approvals.values() if w.get("auto_approval_result")])
        
        # Calculate average approval time for completed workflows
        completed_workflows = [w for w in tenant_approvals.values() if w["status"] == "completed" and "completed_at" in w]
        if completed_workflows:
            avg_approval_time = sum(
                (w["completed_at"] - w["created_at"]).total_seconds() / 3600 
                for w in completed_workflows
            ) / len(completed_workflows)
        else:
            avg_approval_time = 0
        
        return {
            "total_approvals": total_approvals,
            "pending_approvals": pending_approvals,
            "completed_approvals": completed_approvals,
            "auto_approval_rate": auto_approvals / total_approvals if total_approvals > 0 else 0,
            "average_approval_time_hours": avg_approval_time,
            "approval_queue": [
                {
                    "approval_id": aid,
                    "approval_type": w["context"]["approval_type"],
                    "status": w["status"],
                    "priority": w["context"]["priority"],
                    "created_at": w["created_at"],
                    "estimated_completion": w["created_at"] + w["approval_path"]["estimated_duration"]
                }
                for aid, w in tenant_approvals.items()
                if w["status"] in ["initiated", "pending_review"]
            ]
        }

# Global HITL workflow instance
content_marketing_hitl = ContentMarketingHITLWorkflows()