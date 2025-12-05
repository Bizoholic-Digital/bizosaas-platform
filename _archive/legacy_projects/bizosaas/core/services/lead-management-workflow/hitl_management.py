"""
Human-in-the-Loop (HITL) Management System for Lead Management Workflow
Provides manual oversight, intervention capabilities, and quality control for automated processes
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import aioredis
import asyncpg
from pydantic import BaseModel, Field
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InterventionType(Enum):
    SCORE_OVERRIDE = "score_override"
    ASSIGNMENT_OVERRIDE = "assignment_override"
    CAMPAIGN_APPROVAL = "campaign_approval"
    QUALITY_REVIEW = "quality_review"
    ESCALATION_HANDLING = "escalation_handling"
    MANUAL_REASSIGNMENT = "manual_reassignment"
    CONTENT_APPROVAL = "content_approval"
    STRATEGY_OVERRIDE = "strategy_override"

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    EXPIRED = "expired"

class ReviewPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class UserRole(Enum):
    SALES_REP = "sales_rep"
    SALES_MANAGER = "sales_manager"
    MARKETING_MANAGER = "marketing_manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

@dataclass
class HITLRequest:
    """Human intervention request"""
    request_id: str
    intervention_type: InterventionType
    priority: ReviewPriority
    
    # Request details
    subject: str
    description: str
    context_data: Dict[str, Any] = field(default_factory=dict)
    
    # Assignment and approval
    requested_by: str = ""
    assigned_to: Optional[str] = None
    required_role: UserRole = UserRole.SALES_MANAGER
    
    # Status tracking
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    
    # Response data
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    response_data: Dict[str, Any] = field(default_factory=dict)
    
    # Escalation
    escalated_to: Optional[str] = None
    escalated_at: Optional[datetime] = None
    escalation_reason: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class QualityReview:
    """Quality review record for automated decisions"""
    review_id: str
    review_type: str  # lead_scoring, assignment, campaign_execution
    entity_id: str    # lead_id, assignment_id, campaign_id
    
    # Review criteria
    automated_decision: Dict[str, Any] = field(default_factory=dict)
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Review results
    reviewer_id: str = ""
    review_status: str = "pending"  # pending, approved, needs_improvement, rejected
    feedback: str = ""
    corrective_actions: List[str] = field(default_factory=list)
    
    # Scoring
    accuracy_score: Optional[float] = None
    confidence_score: Optional[float] = None
    human_override: bool = False
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None
    
    # Learning data
    learning_feedback: Dict[str, Any] = field(default_factory=dict)

class ApprovalWorkflow:
    """Manages approval workflows for different intervention types"""
    
    def __init__(self):
        self.approval_rules = {
            InterventionType.SCORE_OVERRIDE: {
                "required_role": UserRole.SALES_MANAGER,
                "approval_timeout_hours": 24,
                "auto_escalate": True,
                "escalation_role": UserRole.ADMIN
            },
            InterventionType.ASSIGNMENT_OVERRIDE: {
                "required_role": UserRole.SALES_MANAGER,
                "approval_timeout_hours": 4,
                "auto_escalate": True,
                "escalation_role": UserRole.ADMIN
            },
            InterventionType.CAMPAIGN_APPROVAL: {
                "required_role": UserRole.MARKETING_MANAGER,
                "approval_timeout_hours": 48,
                "auto_escalate": False,
                "escalation_role": UserRole.ADMIN
            },
            InterventionType.QUALITY_REVIEW: {
                "required_role": UserRole.SALES_MANAGER,
                "approval_timeout_hours": 72,
                "auto_escalate": False,
                "escalation_role": UserRole.ADMIN
            },
            InterventionType.ESCALATION_HANDLING: {
                "required_role": UserRole.ADMIN,
                "approval_timeout_hours": 2,
                "auto_escalate": True,
                "escalation_role": UserRole.SUPER_ADMIN
            }
        }
    
    def get_approval_requirements(self, intervention_type: InterventionType) -> Dict[str, Any]:
        """Get approval requirements for intervention type"""
        return self.approval_rules.get(intervention_type, {
            "required_role": UserRole.SALES_MANAGER,
            "approval_timeout_hours": 24,
            "auto_escalate": False,
            "escalation_role": UserRole.ADMIN
        })
    
    def calculate_due_date(self, intervention_type: InterventionType, 
                          priority: ReviewPriority) -> datetime:
        """Calculate due date based on type and priority"""
        rules = self.get_approval_requirements(intervention_type)
        base_hours = rules["approval_timeout_hours"]
        
        # Adjust based on priority
        priority_multipliers = {
            ReviewPriority.URGENT: 0.25,
            ReviewPriority.HIGH: 0.5,
            ReviewPriority.MEDIUM: 1.0,
            ReviewPriority.LOW: 2.0
        }
        
        adjusted_hours = base_hours * priority_multipliers[priority]
        return datetime.utcnow() + timedelta(hours=adjusted_hours)

class HITLManagementSystem:
    """Main Human-in-the-Loop management system"""
    
    def __init__(self, db_config: Dict[str, str], redis_config: Dict[str, str]):
        self.db_config = db_config
        self.redis_config = redis_config
        self.approval_workflow = ApprovalWorkflow()
        
        # User management
        self.user_roles = {}
        self.user_permissions = {}
        
        # Quality control metrics
        self.quality_metrics = {
            "total_reviews": 0,
            "accuracy_score": 0.0,
            "human_intervention_rate": 0.0,
            "approval_rate": 0.0
        }
        
        # Active requests tracking
        self.pending_requests = {}
        self.active_reviews = {}
    
    async def initialize(self):
        """Initialize HITL management system"""
        try:
            # Initialize database connection
            self.db_pool = await asyncpg.create_pool(**self.db_config)
            
            # Initialize Redis connection
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config['host']}:{self.redis_config['port']}"
            )
            
            # Load user roles and permissions
            await self._load_user_management()
            
            # Start background tasks
            asyncio.create_task(self._approval_monitor())
            asyncio.create_task(self._quality_review_scheduler())
            asyncio.create_task(self._escalation_processor())
            
            logger.info("HITL management system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize HITL management system: {e}")
            raise
    
    async def _load_user_management(self):
        """Load user roles and permissions"""
        try:
            async with self.db_pool.acquire() as conn:
                # Load user roles
                user_rows = await conn.fetch("""
                    SELECT user_id, role, permissions, team, active FROM users WHERE active = true
                """)
                
                for row in user_rows:
                    self.user_roles[row["user_id"]] = {
                        "role": UserRole(row["role"]),
                        "permissions": json.loads(row["permissions"]) if row["permissions"] else [],
                        "team": row["team"],
                        "active": row["active"]
                    }
                
                logger.info(f"Loaded {len(self.user_roles)} user profiles")
                
        except Exception as e:
            logger.error(f"Error loading user management: {e}")
            # Create default admin user for testing
            self.user_roles["admin"] = {
                "role": UserRole.ADMIN,
                "permissions": ["all"],
                "team": "admin",
                "active": True
            }
    
    async def request_intervention(self, intervention_type: InterventionType,
                                 context_data: Dict[str, Any],
                                 requested_by: str,
                                 priority: ReviewPriority = ReviewPriority.MEDIUM,
                                 subject: str = "",
                                 description: str = "") -> HITLRequest:
        """Request human intervention for automated process"""
        try:
            # Generate request ID
            request_id = f"hitl_{intervention_type.value}_{uuid.uuid4().hex[:8]}"
            
            # Get approval requirements
            approval_rules = self.approval_workflow.get_approval_requirements(intervention_type)
            
            # Calculate due date
            due_date = self.approval_workflow.calculate_due_date(intervention_type, priority)
            
            # Create HITL request
            request = HITLRequest(
                request_id=request_id,
                intervention_type=intervention_type,
                priority=priority,
                subject=subject or f"{intervention_type.value.replace('_', ' ').title()} Request",
                description=description,
                context_data=context_data,
                requested_by=requested_by,
                required_role=approval_rules["required_role"],
                due_date=due_date
            )
            
            # Assign to appropriate reviewer
            assigned_reviewer = await self._assign_reviewer(request)
            if assigned_reviewer:
                request.assigned_to = assigned_reviewer
            
            # Store request in database
            await self._store_hitl_request(request)
            
            # Add to pending requests
            self.pending_requests[request_id] = request
            
            # Send notification to assigned reviewer
            await self._notify_reviewer(request)
            
            # Cache for quick access
            await self._cache_request(request)
            
            logger.info(f"Created HITL request {request_id} for {intervention_type.value}")
            
            return request
            
        except Exception as e:
            logger.error(f"Error creating HITL request: {e}")
            raise
    
    async def _assign_reviewer(self, request: HITLRequest) -> Optional[str]:
        """Assign request to appropriate reviewer based on role and workload"""
        try:
            required_role = request.required_role
            
            # Find eligible reviewers
            eligible_reviewers = []
            for user_id, user_data in self.user_roles.items():
                if (user_data["role"] == required_role or 
                    self._has_higher_role(user_data["role"], required_role)):
                    eligible_reviewers.append(user_id)
            
            if not eligible_reviewers:
                logger.warning(f"No eligible reviewers found for role {required_role}")
                return None
            
            # Get workload for each reviewer
            reviewer_workloads = {}
            for reviewer in eligible_reviewers:
                workload = await self._get_reviewer_workload(reviewer)
                reviewer_workloads[reviewer] = workload
            
            # Assign to reviewer with lowest workload
            assigned_reviewer = min(reviewer_workloads.items(), key=lambda x: x[1])[0]
            
            return assigned_reviewer
            
        except Exception as e:
            logger.error(f"Error assigning reviewer: {e}")
            return None
    
    def _has_higher_role(self, user_role: UserRole, required_role: UserRole) -> bool:
        """Check if user role has higher permissions than required role"""
        role_hierarchy = {
            UserRole.SALES_REP: 1,
            UserRole.SALES_MANAGER: 2,
            UserRole.MARKETING_MANAGER: 2,
            UserRole.ADMIN: 3,
            UserRole.SUPER_ADMIN: 4
        }
        
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)
    
    async def _get_reviewer_workload(self, reviewer_id: str) -> int:
        """Get current workload for reviewer"""
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.fetchval("""
                    SELECT COUNT(*) FROM hitl_requests 
                    WHERE assigned_to = $1 AND status = 'pending'
                """, reviewer_id)
                
                return result or 0
                
        except Exception as e:
            logger.error(f"Error getting reviewer workload: {e}")
            return 0
    
    async def approve_request(self, request_id: str, approved_by: str,
                            response_data: Dict[str, Any] = None,
                            comments: str = "") -> bool:
        """Approve a HITL request"""
        try:
            # Get request
            request = await self._get_hitl_request(request_id)
            if not request:
                logger.error(f"HITL request {request_id} not found")
                return False
            
            # Check if user has permission to approve
            if not await self._can_approve(approved_by, request):
                logger.error(f"User {approved_by} not authorized to approve request {request_id}")
                return False
            
            # Update request status
            request.status = ApprovalStatus.APPROVED
            request.approved_by = approved_by
            request.approved_at = datetime.utcnow()
            request.response_data = response_data or {}
            request.metadata["comments"] = comments
            
            # Update in database
            await self._update_hitl_request(request)
            
            # Execute approved action
            await self._execute_approved_action(request)
            
            # Remove from pending requests
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
            
            # Send confirmation notification
            await self._notify_approval_result(request, approved=True)
            
            # Update quality metrics
            await self._update_quality_metrics("approval", True)
            
            logger.info(f"Approved HITL request {request_id} by {approved_by}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error approving request {request_id}: {e}")
            return False
    
    async def reject_request(self, request_id: str, rejected_by: str,
                           rejection_reason: str, comments: str = "") -> bool:
        """Reject a HITL request"""
        try:
            # Get request
            request = await self._get_hitl_request(request_id)
            if not request:
                return False
            
            # Check if user has permission to reject
            if not await self._can_approve(rejected_by, request):
                return False
            
            # Update request status
            request.status = ApprovalStatus.REJECTED
            request.approved_by = rejected_by
            request.approved_at = datetime.utcnow()
            request.rejection_reason = rejection_reason
            request.metadata["comments"] = comments
            
            # Update in database
            await self._update_hitl_request(request)
            
            # Remove from pending requests
            if request_id in self.pending_requests:
                del self.pending_requests[request_id]
            
            # Send rejection notification
            await self._notify_approval_result(request, approved=False)
            
            # Update quality metrics
            await self._update_quality_metrics("approval", False)
            
            logger.info(f"Rejected HITL request {request_id} by {rejected_by}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error rejecting request {request_id}: {e}")
            return False
    
    async def create_quality_review(self, review_type: str, entity_id: str,
                                  automated_decision: Dict[str, Any],
                                  quality_metrics: Dict[str, float] = None) -> QualityReview:
        """Create a quality review for an automated decision"""
        try:
            review_id = f"qr_{review_type}_{entity_id}_{uuid.uuid4().hex[:8]}"
            
            review = QualityReview(
                review_id=review_id,
                review_type=review_type,
                entity_id=entity_id,
                automated_decision=automated_decision,
                quality_metrics=quality_metrics or {}
            )
            
            # Store in database
            await self._store_quality_review(review)
            
            # Add to active reviews
            self.active_reviews[review_id] = review
            
            # Schedule for review if quality score is below threshold
            quality_score = self._calculate_quality_score(quality_metrics or {})
            if quality_score < 0.8:  # Threshold for manual review
                await self._schedule_manual_review(review)
            
            logger.info(f"Created quality review {review_id} for {review_type}")
            
            return review
            
        except Exception as e:
            logger.error(f"Error creating quality review: {e}")
            raise
    
    def _calculate_quality_score(self, quality_metrics: Dict[str, float]) -> float:
        """Calculate overall quality score from metrics"""
        if not quality_metrics:
            return 0.5  # Neutral score
        
        # Weight different quality metrics
        weights = {
            "accuracy": 0.4,
            "confidence": 0.3,
            "completeness": 0.2,
            "consistency": 0.1
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for metric, value in quality_metrics.items():
            weight = weights.get(metric, 0.1)
            weighted_score += value * weight
            total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0.5
    
    async def manual_score_override(self, lead_id: str, override_data: Dict[str, Any],
                                  override_by: str, reason: str) -> bool:
        """Handle manual lead score override"""
        try:
            # Create HITL request for score override
            context_data = {
                "lead_id": lead_id,
                "original_score": override_data.get("original_score"),
                "new_score": override_data.get("new_score"),
                "score_breakdown": override_data.get("score_breakdown", {}),
                "reason": reason
            }
            
            request = await self.request_intervention(
                InterventionType.SCORE_OVERRIDE,
                context_data,
                override_by,
                ReviewPriority.HIGH,
                f"Score Override Request for Lead {lead_id}",
                f"Requesting manual override of lead score from {override_data.get('original_score')} to {override_data.get('new_score')}. Reason: {reason}"
            )
            
            # For urgent cases, auto-approve if requester has sufficient permissions
            if self._can_auto_approve(override_by, request):
                return await self.approve_request(request.request_id, override_by, override_data)
            
            return True  # Request created, pending approval
            
        except Exception as e:
            logger.error(f"Error in manual score override: {e}")
            return False
    
    async def manual_assignment_override(self, lead_id: str, new_rep_id: str,
                                       override_by: str, reason: str) -> bool:
        """Handle manual lead assignment override"""
        try:
            context_data = {
                "lead_id": lead_id,
                "new_rep_id": new_rep_id,
                "reason": reason,
                "override_timestamp": datetime.utcnow().isoformat()
            }
            
            request = await self.request_intervention(
                InterventionType.ASSIGNMENT_OVERRIDE,
                context_data,
                override_by,
                ReviewPriority.HIGH,
                f"Assignment Override Request for Lead {lead_id}",
                f"Requesting manual reassignment of lead to {new_rep_id}. Reason: {reason}"
            )
            
            # For urgent cases or manager override, process immediately
            if self._can_auto_approve(override_by, request):
                return await self.approve_request(request.request_id, override_by, context_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in manual assignment override: {e}")
            return False
    
    async def campaign_approval_request(self, campaign_data: Dict[str, Any],
                                      requested_by: str) -> HITLRequest:
        """Request approval for high-value campaign"""
        try:
            context_data = {
                "campaign_id": campaign_data["campaign_id"],
                "campaign_type": campaign_data["campaign_type"],
                "target_value": campaign_data.get("target_value", 0),
                "estimated_reach": campaign_data.get("estimated_reach", 0),
                "budget": campaign_data.get("budget", 0),
                "campaign_details": campaign_data
            }
            
            # Determine priority based on campaign value
            priority = ReviewPriority.HIGH if campaign_data.get("target_value", 0) > 100000 else ReviewPriority.MEDIUM
            
            request = await self.request_intervention(
                InterventionType.CAMPAIGN_APPROVAL,
                context_data,
                requested_by,
                priority,
                f"Campaign Approval: {campaign_data.get('name', 'Unnamed Campaign')}",
                f"Requesting approval for {campaign_data['campaign_type']} campaign targeting {campaign_data.get('estimated_reach', 0)} leads"
            )
            
            return request
            
        except Exception as e:
            logger.error(f"Error requesting campaign approval: {e}")
            raise
    
    def _can_auto_approve(self, user_id: str, request: HITLRequest) -> bool:
        """Check if user can auto-approve specific request types"""
        user_data = self.user_roles.get(user_id)
        if not user_data:
            return False
        
        # Admin and Super Admin can auto-approve most requests
        if user_data["role"] in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            return True
        
        # Managers can auto-approve their own overrides in some cases
        if (request.intervention_type == InterventionType.ASSIGNMENT_OVERRIDE and
            user_data["role"] == UserRole.SALES_MANAGER):
            return True
        
        return False
    
    async def _can_approve(self, user_id: str, request: HITLRequest) -> bool:
        """Check if user can approve a specific request"""
        user_data = self.user_roles.get(user_id)
        if not user_data:
            return False
        
        # Check role hierarchy
        return self._has_higher_role(user_data["role"], request.required_role)
    
    async def _execute_approved_action(self, request: HITLRequest):
        """Execute the approved action based on intervention type"""
        try:
            if request.intervention_type == InterventionType.SCORE_OVERRIDE:
                await self._execute_score_override(request)
            elif request.intervention_type == InterventionType.ASSIGNMENT_OVERRIDE:
                await self._execute_assignment_override(request)
            elif request.intervention_type == InterventionType.CAMPAIGN_APPROVAL:
                await self._execute_campaign_approval(request)
            
            logger.info(f"Executed approved action for request {request.request_id}")
            
        except Exception as e:
            logger.error(f"Error executing approved action: {e}")
    
    async def _execute_score_override(self, request: HITLRequest):
        """Execute manual score override"""
        try:
            context = request.context_data
            lead_id = context["lead_id"]
            new_score = context["new_score"]
            
            # Update lead score in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE lead_scores SET
                        total_score = $1,
                        manual_override = true,
                        override_by = $2,
                        override_at = $3,
                        override_reason = $4
                    WHERE lead_id = $5
                """, 
                    new_score,
                    request.approved_by,
                    request.approved_at,
                    context.get("reason", ""),
                    lead_id
                )
            
            # Trigger re-assignment if needed
            await self._trigger_reassignment_check(lead_id)
            
        except Exception as e:
            logger.error(f"Error executing score override: {e}")
    
    async def _execute_assignment_override(self, request: HITLRequest):
        """Execute manual assignment override"""
        try:
            context = request.context_data
            lead_id = context["lead_id"]
            new_rep_id = context["new_rep_id"]
            
            # Update assignment in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE lead_assignments SET
                        rep_id = $1,
                        manual_override = true,
                        override_by = $2,
                        override_at = $3,
                        override_reason = $4
                    WHERE lead_id = $5 AND status = 'active'
                """,
                    new_rep_id,
                    request.approved_by,
                    request.approved_at,
                    context.get("reason", ""),
                    lead_id
                )
            
            # Send notification to new rep
            await self._notify_new_assignment(lead_id, new_rep_id)
            
        except Exception as e:
            logger.error(f"Error executing assignment override: {e}")
    
    async def _execute_campaign_approval(self, request: HITLRequest):
        """Execute campaign approval"""
        try:
            context = request.context_data
            campaign_id = context["campaign_id"]
            
            # Update campaign status to approved
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE nurturing_campaigns SET
                        status = 'approved',
                        approved_by = $1,
                        approved_at = $2
                    WHERE campaign_id = $3
                """,
                    request.approved_by,
                    request.approved_at,
                    campaign_id
                )
            
            # Trigger campaign activation
            await self._trigger_campaign_activation(campaign_id)
            
        except Exception as e:
            logger.error(f"Error executing campaign approval: {e}")
    
    async def _approval_monitor(self):
        """Background task to monitor approval timeouts and escalations"""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                current_time = datetime.utcnow()
                
                # Check for expired requests
                expired_requests = []
                for request_id, request in self.pending_requests.items():
                    if request.due_date and current_time > request.due_date:
                        expired_requests.append(request)
                
                # Handle expired requests
                for request in expired_requests:
                    await self._handle_expired_request(request)
                
            except Exception as e:
                logger.error(f"Error in approval monitor: {e}")
                await asyncio.sleep(60)
    
    async def _handle_expired_request(self, request: HITLRequest):
        """Handle expired approval request"""
        try:
            approval_rules = self.approval_workflow.get_approval_requirements(request.intervention_type)
            
            if approval_rules.get("auto_escalate", False):
                # Escalate to higher role
                escalation_role = approval_rules.get("escalation_role", UserRole.ADMIN)
                await self._escalate_request(request, escalation_role, "Approval timeout")
            else:
                # Mark as expired
                request.status = ApprovalStatus.EXPIRED
                await self._update_hitl_request(request)
                
                # Remove from pending
                if request.request_id in self.pending_requests:
                    del self.pending_requests[request.request_id]
                
                # Notify requester
                await self._notify_request_expired(request)
            
            logger.info(f"Handled expired request {request.request_id}")
            
        except Exception as e:
            logger.error(f"Error handling expired request: {e}")
    
    async def _escalate_request(self, request: HITLRequest, escalation_role: UserRole, reason: str):
        """Escalate request to higher authority"""
        try:
            # Find escalation target
            escalation_target = await self._find_escalation_target(escalation_role)
            if not escalation_target:
                logger.error(f"No escalation target found for role {escalation_role}")
                return
            
            # Update request
            request.status = ApprovalStatus.ESCALATED
            request.escalated_to = escalation_target
            request.escalated_at = datetime.utcnow()
            request.escalation_reason = reason
            request.assigned_to = escalation_target
            
            # Extend due date
            request.due_date = datetime.utcnow() + timedelta(hours=24)
            
            # Update in database
            await self._update_hitl_request(request)
            
            # Notify escalation target
            await self._notify_escalation(request)
            
            logger.info(f"Escalated request {request.request_id} to {escalation_target}")
            
        except Exception as e:
            logger.error(f"Error escalating request: {e}")
    
    async def _find_escalation_target(self, required_role: UserRole) -> Optional[str]:
        """Find appropriate escalation target"""
        eligible_users = []
        for user_id, user_data in self.user_roles.items():
            if self._has_higher_role(user_data["role"], required_role):
                eligible_users.append(user_id)
        
        if not eligible_users:
            return None
        
        # Find user with lowest workload
        min_workload = float('inf')
        target_user = None
        
        for user_id in eligible_users:
            workload = await self._get_reviewer_workload(user_id)
            if workload < min_workload:
                min_workload = workload
                target_user = user_id
        
        return target_user
    
    async def _quality_review_scheduler(self):
        """Background task to schedule quality reviews"""
        while True:
            try:
                await asyncio.sleep(3600)  # Check every hour
                
                # Schedule random quality reviews
                await self._schedule_random_quality_reviews()
                
                # Review quality metrics and adjust automation confidence
                await self._review_quality_metrics()
                
            except Exception as e:
                logger.error(f"Error in quality review scheduler: {e}")
                await asyncio.sleep(600)
    
    async def _schedule_random_quality_reviews(self):
        """Schedule random quality reviews for sampling"""
        try:
            # Sample recent automated decisions for review
            review_rate = 0.05  # Review 5% of decisions
            
            async with self.db_pool.acquire() as conn:
                # Get recent lead scores for review
                recent_scores = await conn.fetch("""
                    SELECT lead_id, total_score, qualification_level, scored_at
                    FROM lead_scores 
                    WHERE scored_at > NOW() - INTERVAL '24 hours'
                    AND manual_override = false
                    ORDER BY RANDOM()
                    LIMIT 10
                """)
                
                for score_record in recent_scores:
                    if random.random() < review_rate:
                        automated_decision = {
                            "total_score": score_record["total_score"],
                            "qualification_level": score_record["qualification_level"],
                            "scored_at": score_record["scored_at"].isoformat()
                        }
                        
                        await self.create_quality_review(
                            "lead_scoring",
                            score_record["lead_id"],
                            automated_decision
                        )
                
                # Get recent assignments for review
                recent_assignments = await conn.fetch("""
                    SELECT assignment_id, lead_id, rep_id, assignment_score, assigned_at
                    FROM lead_assignments
                    WHERE assigned_at > NOW() - INTERVAL '24 hours'
                    AND manual_override = false
                    ORDER BY RANDOM()
                    LIMIT 5
                """)
                
                for assignment_record in recent_assignments:
                    if random.random() < review_rate:
                        automated_decision = {
                            "rep_id": assignment_record["rep_id"],
                            "assignment_score": assignment_record["assignment_score"],
                            "assigned_at": assignment_record["assigned_at"].isoformat()
                        }
                        
                        await self.create_quality_review(
                            "assignment",
                            assignment_record["assignment_id"],
                            automated_decision
                        )
            
        except Exception as e:
            logger.error(f"Error scheduling random quality reviews: {e}")
    
    async def _escalation_processor(self):
        """Background task to process escalations"""
        while True:
            try:
                await asyncio.sleep(600)  # Check every 10 minutes
                
                # Process pending escalations
                escalated_requests = [
                    req for req in self.pending_requests.values() 
                    if req.status == ApprovalStatus.ESCALATED
                ]
                
                for request in escalated_requests:
                    await self._process_escalated_request(request)
                
            except Exception as e:
                logger.error(f"Error in escalation processor: {e}")
                await asyncio.sleep(300)
    
    async def _process_escalated_request(self, request: HITLRequest):
        """Process an escalated request"""
        try:
            # Check if escalation has been handled
            if request.escalated_at:
                time_since_escalation = datetime.utcnow() - request.escalated_at
                
                # If escalation is older than 4 hours and still pending, alert super admin
                if time_since_escalation > timedelta(hours=4):
                    await self._alert_super_admin(request)
            
        except Exception as e:
            logger.error(f"Error processing escalated request: {e}")
    
    async def get_pending_requests(self, user_id: str, role_filter: Optional[UserRole] = None) -> List[HITLRequest]:
        """Get pending requests for a user"""
        try:
            user_data = self.user_roles.get(user_id)
            if not user_data:
                return []
            
            pending_requests = []
            for request in self.pending_requests.values():
                # Check if user can handle this request
                if (request.assigned_to == user_id or 
                    self._has_higher_role(user_data["role"], request.required_role)):
                    
                    if role_filter is None or request.required_role == role_filter:
                        pending_requests.append(request)
            
            # Sort by priority and due date
            pending_requests.sort(
                key=lambda x: (x.priority.value, x.due_date or datetime.max)
            )
            
            return pending_requests
            
        except Exception as e:
            logger.error(f"Error getting pending requests: {e}")
            return []
    
    async def get_quality_dashboard(self) -> Dict[str, Any]:
        """Get quality control dashboard data"""
        try:
            async with self.db_pool.acquire() as conn:
                # Get quality review statistics
                quality_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_reviews,
                        AVG(accuracy_score) as avg_accuracy,
                        COUNT(CASE WHEN human_override = true THEN 1 END) as human_overrides,
                        COUNT(CASE WHEN review_status = 'approved' THEN 1 END) as approved_reviews
                    FROM quality_reviews
                    WHERE created_at > NOW() - INTERVAL '30 days'
                """)
                
                # Get HITL request statistics
                hitl_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_requests,
                        COUNT(CASE WHEN status = 'approved' THEN 1 END) as approved_requests,
                        COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected_requests,
                        COUNT(CASE WHEN status = 'escalated' THEN 1 END) as escalated_requests,
                        AVG(EXTRACT(EPOCH FROM (approved_at - created_at))/3600) as avg_approval_time_hours
                    FROM hitl_requests
                    WHERE created_at > NOW() - INTERVAL '30 days'
                """)
            
            dashboard_data = {
                "quality_metrics": {
                    "total_reviews": quality_stats["total_reviews"] or 0,
                    "average_accuracy": float(quality_stats["avg_accuracy"] or 0),
                    "human_intervention_rate": (quality_stats["human_overrides"] or 0) / max(1, quality_stats["total_reviews"] or 1),
                    "approval_rate": (quality_stats["approved_reviews"] or 0) / max(1, quality_stats["total_reviews"] or 1)
                },
                "hitl_metrics": {
                    "total_requests": hitl_stats["total_requests"] or 0,
                    "approval_rate": (hitl_stats["approved_requests"] or 0) / max(1, hitl_stats["total_requests"] or 1),
                    "rejection_rate": (hitl_stats["rejected_requests"] or 0) / max(1, hitl_stats["total_requests"] or 1),
                    "escalation_rate": (hitl_stats["escalated_requests"] or 0) / max(1, hitl_stats["total_requests"] or 1),
                    "avg_approval_time_hours": float(hitl_stats["avg_approval_time_hours"] or 0)
                },
                "pending_summary": {
                    "total_pending": len(self.pending_requests),
                    "by_priority": self._get_pending_by_priority(),
                    "by_type": self._get_pending_by_type()
                }
            }
            
            return dashboard_data
            
        except Exception as e:
            logger.error(f"Error getting quality dashboard: {e}")
            return {}
    
    def _get_pending_by_priority(self) -> Dict[str, int]:
        """Get pending requests grouped by priority"""
        priority_counts = {priority.value: 0 for priority in ReviewPriority}
        
        for request in self.pending_requests.values():
            priority_counts[request.priority.value] += 1
        
        return priority_counts
    
    def _get_pending_by_type(self) -> Dict[str, int]:
        """Get pending requests grouped by intervention type"""
        type_counts = {intervention.value: 0 for intervention in InterventionType}
        
        for request in self.pending_requests.values():
            type_counts[request.intervention_type.value] += 1
        
        return type_counts
    
    # Database operations
    
    async def _store_hitl_request(self, request: HITLRequest):
        """Store HITL request in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO hitl_requests (
                        request_id, intervention_type, priority, subject, description,
                        context_data, requested_by, assigned_to, required_role, status,
                        created_at, due_date, metadata
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
                    request.request_id, request.intervention_type.value, request.priority.value,
                    request.subject, request.description, json.dumps(request.context_data),
                    request.requested_by, request.assigned_to, request.required_role.value,
                    request.status.value, request.created_at, request.due_date,
                    json.dumps(request.metadata)
                )
                
        except Exception as e:
            logger.error(f"Error storing HITL request: {e}")
    
    async def _update_hitl_request(self, request: HITLRequest):
        """Update HITL request in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE hitl_requests SET
                        status = $1, approved_by = $2, approved_at = $3,
                        rejection_reason = $4, response_data = $5,
                        escalated_to = $6, escalated_at = $7, escalation_reason = $8,
                        metadata = $9
                    WHERE request_id = $10
                """,
                    request.status.value, request.approved_by, request.approved_at,
                    request.rejection_reason, json.dumps(request.response_data),
                    request.escalated_to, request.escalated_at, request.escalation_reason,
                    json.dumps(request.metadata), request.request_id
                )
                
        except Exception as e:
            logger.error(f"Error updating HITL request: {e}")
    
    async def _get_hitl_request(self, request_id: str) -> Optional[HITLRequest]:
        """Get HITL request from database"""
        try:
            # Check cache first
            if request_id in self.pending_requests:
                return self.pending_requests[request_id]
            
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM hitl_requests WHERE request_id = $1
                """, request_id)
                
                if row:
                    return HITLRequest(
                        request_id=row["request_id"],
                        intervention_type=InterventionType(row["intervention_type"]),
                        priority=ReviewPriority(row["priority"]),
                        subject=row["subject"],
                        description=row["description"],
                        context_data=json.loads(row["context_data"]),
                        requested_by=row["requested_by"],
                        assigned_to=row["assigned_to"],
                        required_role=UserRole(row["required_role"]),
                        status=ApprovalStatus(row["status"]),
                        created_at=row["created_at"],
                        due_date=row["due_date"],
                        approved_by=row["approved_by"],
                        approved_at=row["approved_at"],
                        rejection_reason=row["rejection_reason"],
                        response_data=json.loads(row["response_data"]) if row["response_data"] else {},
                        escalated_to=row["escalated_to"],
                        escalated_at=row["escalated_at"],
                        escalation_reason=row["escalation_reason"],
                        metadata=json.loads(row["metadata"]) if row["metadata"] else {}
                    )
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting HITL request: {e}")
            return None
    
    async def _store_quality_review(self, review: QualityReview):
        """Store quality review in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO quality_reviews (
                        review_id, review_type, entity_id, automated_decision,
                        quality_metrics, reviewer_id, review_status, feedback,
                        corrective_actions, accuracy_score, confidence_score,
                        human_override, created_at, learning_feedback
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                """,
                    review.review_id, review.review_type, review.entity_id,
                    json.dumps(review.automated_decision), json.dumps(review.quality_metrics),
                    review.reviewer_id, review.review_status, review.feedback,
                    json.dumps(review.corrective_actions), review.accuracy_score,
                    review.confidence_score, review.human_override, review.created_at,
                    json.dumps(review.learning_feedback)
                )
                
        except Exception as e:
            logger.error(f"Error storing quality review: {e}")
    
    # Notification methods (placeholders - integrate with notification service)
    
    async def _notify_reviewer(self, request: HITLRequest):
        """Send notification to assigned reviewer"""
        notification_data = {
            "type": "hitl_request_assigned",
            "request_id": request.request_id,
            "priority": request.priority.value,
            "subject": request.subject,
            "due_date": request.due_date.isoformat() if request.due_date else None
        }
        
        await self.redis.lpush("notification_queue", json.dumps(notification_data))
    
    async def _notify_approval_result(self, request: HITLRequest, approved: bool):
        """Send notification about approval result"""
        notification_data = {
            "type": "hitl_request_completed",
            "request_id": request.request_id,
            "approved": approved,
            "approved_by": request.approved_by
        }
        
        await self.redis.lpush("notification_queue", json.dumps(notification_data))
    
    async def _notify_escalation(self, request: HITLRequest):
        """Send escalation notification"""
        notification_data = {
            "type": "hitl_request_escalated",
            "request_id": request.request_id,
            "escalated_to": request.escalated_to,
            "escalation_reason": request.escalation_reason
        }
        
        await self.redis.lpush("urgent_notifications", json.dumps(notification_data))
    
    # Utility methods
    
    async def _cache_request(self, request: HITLRequest):
        """Cache request for quick access"""
        cache_key = f"hitl_request:{request.request_id}"
        cache_data = {
            "request_id": request.request_id,
            "status": request.status.value,
            "priority": request.priority.value,
            "assigned_to": request.assigned_to,
            "due_date": request.due_date.isoformat() if request.due_date else None
        }
        
        await self.redis.setex(cache_key, 3600, json.dumps(cache_data, default=str))
    
    async def _update_quality_metrics(self, metric_type: str, success: bool):
        """Update quality control metrics"""
        if metric_type == "approval":
            self.quality_metrics["total_reviews"] += 1
            if success:
                # Update approval rate
                current_rate = self.quality_metrics["approval_rate"]
                total = self.quality_metrics["total_reviews"]
                self.quality_metrics["approval_rate"] = (current_rate * (total - 1) + 1) / total
    
    async def cleanup(self):
        """Cleanup HITL management system"""
        try:
            if hasattr(self, 'db_pool'):
                await self.db_pool.close()
            if hasattr(self, 'redis'):
                await self.redis.close()
            logger.info("HITL management system cleanup completed")
        except Exception as e:
            logger.error(f"Error during HITL cleanup: {e}")

# Example usage
async def main():
    """Example usage of HITL management system"""
    
    # Configuration
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "bizosaas",
        "user": "postgres",
        "password": "password"
    }
    
    redis_config = {
        "host": "localhost",
        "port": 6379
    }
    
    # Initialize HITL system
    hitl_system = HITLManagementSystem(db_config, redis_config)
    await hitl_system.initialize()
    
    try:
        # Example: Request manual score override
        override_success = await hitl_system.manual_score_override(
            "lead_123",
            {"original_score": 65, "new_score": 85},
            "sales_manager_1",
            "Lead showed strong interest in demo call"
        )
        print(f"Score override request successful: {override_success}")
        
        # Example: Get pending requests for user
        pending_requests = await hitl_system.get_pending_requests("sales_manager_1")
        print(f"Pending requests: {len(pending_requests)}")
        
        # Example: Get quality dashboard
        dashboard = await hitl_system.get_quality_dashboard()
        print(f"Quality dashboard: {json.dumps(dashboard, indent=2, default=str)}")
        
    finally:
        await hitl_system.cleanup()

if __name__ == "__main__":
    asyncio.run(main())