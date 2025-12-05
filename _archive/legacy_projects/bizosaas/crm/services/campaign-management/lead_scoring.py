"""
Lead Scoring and Qualification System - BizoholicSaaS
Advanced lead scoring with behavioral tracking, qualification automation, and sales handoff
"""

import uuid
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import logging
import json
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

class LeadStatus(str, Enum):
    """Lead qualification status"""
    UNQUALIFIED = "unqualified"
    MARKETING_QUALIFIED = "marketing_qualified" 
    SALES_QUALIFIED = "sales_qualified"
    SALES_ACCEPTED = "sales_accepted"
    OPPORTUNITY = "opportunity"
    CUSTOMER = "customer"
    LOST = "lost"

class ScoreCategory(str, Enum):
    """Categories for lead scoring"""
    DEMOGRAPHIC = "demographic"
    BEHAVIORAL = "behavioral"
    ENGAGEMENT = "engagement"
    INTEREST = "interest"
    TIMING = "timing"
    AUTHORITY = "authority"
    NEED = "need"
    BUDGET = "budget"

class ActivityType(str, Enum):
    """Types of lead activities that can be scored"""
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    WEBSITE_VISIT = "website_visit"
    FORM_SUBMITTED = "form_submitted"
    CONTENT_DOWNLOADED = "content_downloaded"
    WEBINAR_ATTENDED = "webinar_attended"
    DEMO_REQUESTED = "demo_requested"
    TRIAL_STARTED = "trial_started"
    PRICING_PAGE_VIEWED = "pricing_page_viewed"
    FEATURE_USED = "feature_used"
    SUPPORT_TICKET = "support_ticket"
    PHONE_CALL = "phone_call"
    MEETING_SCHEDULED = "meeting_scheduled"

class QualificationCriteria(BaseModel):
    """Qualification criteria configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    min_score: int
    max_score: Optional[int] = None
    required_attributes: List[str] = []
    required_activities: List[Dict[str, Any]] = []
    disqualifying_attributes: List[str] = []
    priority: int = 0

class ScoringRule(BaseModel):
    """Individual scoring rule"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: ScoreCategory
    trigger: Dict[str, Any]  # Conditions that trigger this rule
    points: int  # Points to add/subtract
    max_frequency: Optional[int] = None  # Maximum times this rule can apply
    time_window: Optional[int] = None  # Time window in hours for frequency limit
    decay_rate: Optional[float] = None  # Points decay over time
    conditions: List[Dict[str, Any]] = []  # Additional conditions
    is_active: bool = True

class LeadScore(BaseModel):
    """Lead scoring model"""
    lead_id: str
    tenant_id: str
    total_score: int = 0
    category_scores: Dict[ScoreCategory, int] = Field(default_factory=dict)
    qualification_status: LeadStatus = LeadStatus.UNQUALIFIED
    last_activity: Optional[datetime] = None
    last_score_change: Optional[datetime] = None
    score_history: List[Dict[str, Any]] = Field(default_factory=list)
    activities: List[Dict[str, Any]] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LeadActivity(BaseModel):
    """Individual lead activity"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    lead_id: str
    activity_type: ActivityType
    activity_data: Dict[str, Any]
    points_awarded: int = 0
    scoring_rules_applied: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HandoffConfiguration(BaseModel):
    """Configuration for sales handoff"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    name: str
    trigger_score: int
    trigger_status: LeadStatus
    sales_team_assignment: str  # How to assign leads
    notification_methods: List[str] = ["email", "slack", "crm"]
    handoff_template: Dict[str, str] = {}
    sla_hours: int = 24  # Response SLA
    auto_follow_up: bool = True
    escalation_rules: List[Dict[str, Any]] = []

@dataclass
class LeadQualificationResult:
    """Result of lead qualification process"""
    lead_id: str
    previous_status: LeadStatus
    new_status: LeadStatus
    score_change: int
    qualifying_activities: List[str]
    next_actions: List[Dict[str, Any]]
    handoff_triggered: bool = False
    handoff_data: Optional[Dict[str, Any]] = None

class LeadScoringEngine:
    """Advanced Lead Scoring and Qualification Engine"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.scoring_rules: Dict[str, ScoringRule] = {}
        self.qualification_criteria: Dict[LeadStatus, QualificationCriteria] = {}
        self.handoff_configs: List[HandoffConfiguration] = []
        self.lead_scores: Dict[str, LeadScore] = {}
    
    def initialize_default_scoring_rules(self) -> None:
        """Initialize default lead scoring rules"""
        
        default_rules = [
            # Demographic Scoring
            ScoringRule(
                name="Company Size - Enterprise",
                category=ScoreCategory.DEMOGRAPHIC,
                trigger={"attribute": "company_size", "operator": "in", "values": ["1000+", "enterprise"]},
                points=25,
                conditions=[]
            ),
            ScoringRule(
                name="Job Title - Decision Maker",
                category=ScoreCategory.DEMOGRAPHIC,
                trigger={"attribute": "job_title", "operator": "contains", "values": ["ceo", "founder", "president", "director", "manager"]},
                points=20,
                conditions=[]
            ),
            ScoringRule(
                name="Industry Match",
                category=ScoreCategory.DEMOGRAPHIC,
                trigger={"attribute": "industry", "operator": "in", "values": ["saas", "technology", "marketing", "ecommerce"]},
                points=15,
                conditions=[]
            ),
            
            # Behavioral Scoring
            ScoringRule(
                name="Pricing Page Visit",
                category=ScoreCategory.BEHAVIORAL,
                trigger={"activity": "website_visit", "page_type": "pricing"},
                points=30,
                max_frequency=3,
                time_window=24
            ),
            ScoringRule(
                name="Demo Request",
                category=ScoreCategory.BEHAVIORAL,
                trigger={"activity": "demo_requested"},
                points=50,
                max_frequency=1
            ),
            ScoringRule(
                name="Trial Started",
                category=ScoreCategory.BEHAVIORAL,
                trigger={"activity": "trial_started"},
                points=40,
                max_frequency=1
            ),
            ScoringRule(
                name="Feature Usage - High Value",
                category=ScoreCategory.BEHAVIORAL,
                trigger={"activity": "feature_used", "feature_tier": "premium"},
                points=25,
                max_frequency=10,
                time_window=168  # 1 week
            ),
            
            # Engagement Scoring
            ScoringRule(
                name="Email Engagement - High",
                category=ScoreCategory.ENGAGEMENT,
                trigger={"activity": "email_clicked", "engagement_score": ">80"},
                points=15,
                max_frequency=5,
                time_window=24
            ),
            ScoringRule(
                name="Content Download",
                category=ScoreCategory.ENGAGEMENT,
                trigger={"activity": "content_downloaded", "content_type": "whitepaper"},
                points=20,
                max_frequency=3
            ),
            ScoringRule(
                name="Webinar Attendance",
                category=ScoreCategory.ENGAGEMENT,
                trigger={"activity": "webinar_attended", "attendance_percentage": ">75"},
                points=35,
                max_frequency=2
            ),
            
            # Interest Scoring
            ScoringRule(
                name="Multiple Page Views",
                category=ScoreCategory.INTEREST,
                trigger={"activity": "website_visit", "page_count": ">5", "session_duration": ">300"},
                points=20,
                max_frequency=3,
                time_window=72
            ),
            ScoringRule(
                name="Return Visitor",
                category=ScoreCategory.INTEREST,
                trigger={"activity": "website_visit", "visitor_type": "returning", "frequency": ">3"},
                points=15,
                decay_rate=0.1  # 10% decay per week
            ),
            
            # Timing Scoring
            ScoringRule(
                name="Recent Activity",
                category=ScoreCategory.TIMING,
                trigger={"activity": "any", "recency": "<24"},
                points=10,
                decay_rate=0.2  # 20% decay per week
            ),
            
            # Negative Scoring
            ScoringRule(
                name="Competitor",
                category=ScoreCategory.DEMOGRAPHIC,
                trigger={"attribute": "company_type", "operator": "equals", "value": "competitor"},
                points=-50,
                max_frequency=1
            ),
            ScoringRule(
                name="Unsubscribed",
                category=ScoreCategory.ENGAGEMENT,
                trigger={"activity": "email_unsubscribed"},
                points=-25,
                max_frequency=1
            ),
            ScoringRule(
                name="Low Budget",
                category=ScoreCategory.BUDGET,
                trigger={"attribute": "budget_range", "operator": "in", "values": ["<$1000", "no_budget"]},
                points=-20,
                max_frequency=1
            )
        ]
        
        for rule in default_rules:
            self.scoring_rules[rule.id] = rule
    
    def initialize_qualification_criteria(self) -> None:
        """Initialize default qualification criteria"""
        
        self.qualification_criteria = {
            LeadStatus.MARKETING_QUALIFIED: QualificationCriteria(
                name="Marketing Qualified Lead (MQL)",
                description="Lead shows sufficient engagement and intent",
                min_score=50,
                max_score=99,
                required_activities=[
                    {"activity": "email_clicked", "frequency": ">2"},
                    {"activity": "website_visit", "frequency": ">3"}
                ],
                required_attributes=["email", "company"]
            ),
            
            LeadStatus.SALES_QUALIFIED: QualificationCriteria(
                name="Sales Qualified Lead (SQL)",
                description="Lead meets criteria for sales engagement",
                min_score=100,
                required_activities=[
                    {"activity": "demo_requested", "frequency": ">0"},
                    {"activity": "pricing_page_viewed", "frequency": ">1"}
                ],
                required_attributes=["email", "company", "job_title"],
                disqualifying_attributes=["competitor_flag"]
            ),
            
            LeadStatus.SALES_ACCEPTED: QualificationCriteria(
                name="Sales Accepted Lead (SAL)",
                description="Sales team has accepted and engaged with lead",
                min_score=120,
                required_activities=[
                    {"activity": "phone_call", "frequency": ">0"},
                    {"activity": "meeting_scheduled", "frequency": ">0"}
                ]
            ),
            
            LeadStatus.OPPORTUNITY: QualificationCriteria(
                name="Sales Opportunity",
                description="Active sales opportunity with defined next steps",
                min_score=150,
                required_activities=[
                    {"activity": "demo_requested", "frequency": ">0"},
                    {"activity": "proposal_requested", "frequency": ">0"}
                ]
            )
        }
    
    async def score_lead_activity(self, lead_id: str, activity: LeadActivity) -> LeadQualificationResult:
        """Score a new lead activity and update qualification status"""
        
        try:
            # Get or create lead score record
            if lead_id not in self.lead_scores:
                self.lead_scores[lead_id] = LeadScore(
                    lead_id=lead_id,
                    tenant_id=self.tenant_id
                )
            
            lead_score = self.lead_scores[lead_id]
            previous_status = lead_score.qualification_status
            total_points_added = 0
            
            # Apply scoring rules
            applicable_rules = await self._find_applicable_rules(activity)
            
            for rule in applicable_rules:
                # Check if rule can be applied (frequency limits, etc.)
                if await self._can_apply_rule(lead_score, rule, activity):
                    points = await self._calculate_rule_points(rule, activity, lead_score)
                    
                    if points != 0:
                        # Update scores
                        lead_score.total_score += points
                        total_points_added += points
                        
                        # Update category score
                        if rule.category not in lead_score.category_scores:
                            lead_score.category_scores[rule.category] = 0
                        lead_score.category_scores[rule.category] += points
                        
                        # Record in activity
                        activity.points_awarded += points
                        activity.scoring_rules_applied.append(rule.id)
                        
                        # Record in history
                        lead_score.score_history.append({
                            "timestamp": datetime.utcnow().isoformat(),
                            "rule_id": rule.id,
                            "rule_name": rule.name,
                            "points_change": points,
                            "new_total": lead_score.total_score,
                            "activity_id": activity.id,
                            "activity_type": activity.activity_type.value
                        })
            
            # Add activity to lead record
            lead_score.activities.append({
                "id": activity.id,
                "type": activity.activity_type.value,
                "data": activity.activity_data,
                "points": activity.points_awarded,
                "timestamp": activity.timestamp.isoformat()
            })
            
            # Update timestamps
            lead_score.last_activity = activity.timestamp
            lead_score.last_score_change = datetime.utcnow()
            lead_score.updated_at = datetime.utcnow()
            
            # Check for qualification status change
            new_status = await self._determine_qualification_status(lead_score)
            
            if new_status != previous_status:
                lead_score.qualification_status = new_status
                
                # Check if handoff should be triggered
                handoff_triggered, handoff_data = await self._check_handoff_triggers(lead_score, new_status)
                
                return LeadQualificationResult(
                    lead_id=lead_id,
                    previous_status=previous_status,
                    new_status=new_status,
                    score_change=total_points_added,
                    qualifying_activities=[activity.id],
                    next_actions=await self._generate_next_actions(lead_score, new_status),
                    handoff_triggered=handoff_triggered,
                    handoff_data=handoff_data
                )
            
            return LeadQualificationResult(
                lead_id=lead_id,
                previous_status=previous_status,
                new_status=new_status,
                score_change=total_points_added,
                qualifying_activities=[activity.id],
                next_actions=await self._generate_next_actions(lead_score, new_status)
            )
            
        except Exception as e:
            logger.error(f"Error scoring lead activity: {e}")
            raise
    
    async def bulk_score_activities(self, activities: List[LeadActivity]) -> List[LeadQualificationResult]:
        """Score multiple activities efficiently"""
        
        results = []
        
        # Group activities by lead_id for efficient processing
        activities_by_lead = {}
        for activity in activities:
            if activity.lead_id not in activities_by_lead:
                activities_by_lead[activity.lead_id] = []
            activities_by_lead[activity.lead_id].append(activity)
        
        # Process each lead's activities
        for lead_id, lead_activities in activities_by_lead.items():
            for activity in sorted(lead_activities, key=lambda x: x.timestamp):
                result = await self.score_lead_activity(lead_id, activity)
                results.append(result)
        
        return results
    
    async def recalculate_lead_score(self, lead_id: str, include_decay: bool = True) -> LeadScore:
        """Recalculate a lead's total score from scratch"""
        
        try:
            if lead_id not in self.lead_scores:
                raise ValueError(f"Lead {lead_id} not found")
            
            lead_score = self.lead_scores[lead_id]
            
            # Reset scores
            lead_score.total_score = 0
            lead_score.category_scores = {}
            
            # Recalculate from all activities
            for activity_data in lead_score.activities:
                activity = LeadActivity(
                    id=activity_data["id"],
                    lead_id=lead_id,
                    activity_type=ActivityType(activity_data["type"]),
                    activity_data=activity_data["data"],
                    timestamp=datetime.fromisoformat(activity_data["timestamp"])
                )
                
                # Apply scoring rules
                applicable_rules = await self._find_applicable_rules(activity)
                
                for rule in applicable_rules:
                    if await self._can_apply_rule(lead_score, rule, activity):
                        points = await self._calculate_rule_points(rule, activity, lead_score, include_decay)
                        
                        lead_score.total_score += points
                        
                        if rule.category not in lead_score.category_scores:
                            lead_score.category_scores[rule.category] = 0
                        lead_score.category_scores[rule.category] += points
            
            # Update qualification status
            lead_score.qualification_status = await self._determine_qualification_status(lead_score)
            lead_score.updated_at = datetime.utcnow()
            
            return lead_score
            
        except Exception as e:
            logger.error(f"Error recalculating lead score: {e}")
            raise
    
    async def get_lead_insights(self, lead_id: str) -> Dict[str, Any]:
        """Generate actionable insights for a lead"""
        
        if lead_id not in self.lead_scores:
            return {"error": "Lead not found"}
        
        lead_score = self.lead_scores[lead_id]
        
        insights = {
            "lead_id": lead_id,
            "current_score": lead_score.total_score,
            "qualification_status": lead_score.qualification_status.value,
            "category_breakdown": dict(lead_score.category_scores),
            "recent_activities": lead_score.activities[-10:] if lead_score.activities else [],
            "score_trend": await self._calculate_score_trend(lead_score),
            "next_best_actions": await self._generate_next_actions(lead_score, lead_score.qualification_status),
            "qualification_gaps": await self._identify_qualification_gaps(lead_score),
            "engagement_level": await self._calculate_engagement_level(lead_score),
            "risk_factors": await self._identify_risk_factors(lead_score),
            "recommended_content": await self._recommend_content(lead_score),
            "optimal_contact_time": await self._predict_optimal_contact_time(lead_score)
        }
        
        return insights
    
    async def _find_applicable_rules(self, activity: LeadActivity) -> List[ScoringRule]:
        """Find scoring rules applicable to an activity"""
        
        applicable_rules = []
        
        for rule in self.scoring_rules.values():
            if not rule.is_active:
                continue
            
            # Check if rule trigger matches activity
            if await self._rule_matches_activity(rule, activity):
                applicable_rules.append(rule)
        
        return applicable_rules
    
    async def _rule_matches_activity(self, rule: ScoringRule, activity: LeadActivity) -> bool:
        """Check if a scoring rule matches an activity"""
        
        trigger = rule.trigger
        
        # Activity-based triggers
        if "activity" in trigger:
            if trigger["activity"] == "any":
                return True
            elif trigger["activity"] == activity.activity_type.value:
                # Check additional activity conditions
                for key, condition in trigger.items():
                    if key == "activity":
                        continue
                    
                    if key in activity.activity_data:
                        if not await self._evaluate_condition(activity.activity_data[key], condition):
                            return False
                
                return True
        
        # Attribute-based triggers will be checked separately
        return False
    
    async def _can_apply_rule(self, lead_score: LeadScore, rule: ScoringRule, activity: LeadActivity) -> bool:
        """Check if a rule can be applied (frequency limits, etc.)"""
        
        # Check frequency limits
        if rule.max_frequency:
            # Count how many times this rule has been applied
            rule_applications = [
                h for h in lead_score.score_history
                if h["rule_id"] == rule.id
            ]
            
            if rule.time_window:
                # Count only within time window
                cutoff_time = datetime.utcnow() - timedelta(hours=rule.time_window)
                rule_applications = [
                    h for h in rule_applications
                    if datetime.fromisoformat(h["timestamp"]) > cutoff_time
                ]
            
            if len(rule_applications) >= rule.max_frequency:
                return False
        
        # Check additional conditions
        for condition in rule.conditions:
            if not await self._evaluate_condition_on_lead(condition, lead_score, activity):
                return False
        
        return True
    
    async def _calculate_rule_points(self, rule: ScoringRule, activity: LeadActivity, lead_score: LeadScore, include_decay: bool = True) -> int:
        """Calculate points for a rule application, including decay"""
        
        base_points = rule.points
        
        # Apply decay if configured
        if include_decay and rule.decay_rate and lead_score.last_activity:
            weeks_since_last_activity = (activity.timestamp - lead_score.last_activity).days / 7
            decay_factor = (1 - rule.decay_rate) ** weeks_since_last_activity
            base_points = int(base_points * decay_factor)
        
        return base_points
    
    async def _determine_qualification_status(self, lead_score: LeadScore) -> LeadStatus:
        """Determine the appropriate qualification status for a lead"""
        
        current_status = lead_score.qualification_status
        
        # Check each qualification criteria in order of progression
        status_order = [
            LeadStatus.SALES_QUALIFIED,
            LeadStatus.MARKETING_QUALIFIED,
            LeadStatus.UNQUALIFIED
        ]
        
        for status in status_order:
            if status in self.qualification_criteria:
                criteria = self.qualification_criteria[status]
                
                if await self._meets_qualification_criteria(lead_score, criteria):
                    return status
        
        return LeadStatus.UNQUALIFIED
    
    async def _meets_qualification_criteria(self, lead_score: LeadScore, criteria: QualificationCriteria) -> bool:
        """Check if a lead meets specific qualification criteria"""
        
        # Check score requirements
        if lead_score.total_score < criteria.min_score:
            return False
        
        if criteria.max_score and lead_score.total_score > criteria.max_score:
            return False
        
        # Check required attributes
        for attr in criteria.required_attributes:
            if attr not in lead_score.attributes or not lead_score.attributes[attr]:
                return False
        
        # Check disqualifying attributes
        for attr in criteria.disqualifying_attributes:
            if attr in lead_score.attributes and lead_score.attributes[attr]:
                return False
        
        # Check required activities
        for activity_requirement in criteria.required_activities:
            if not await self._has_required_activity(lead_score, activity_requirement):
                return False
        
        return True
    
    async def _has_required_activity(self, lead_score: LeadScore, requirement: Dict[str, Any]) -> bool:
        """Check if lead has required activity"""
        
        activity_type = requirement["activity"]
        frequency_requirement = requirement.get("frequency", ">0")
        
        # Count activities of this type
        matching_activities = [
            a for a in lead_score.activities
            if a["type"] == activity_type
        ]
        
        count = len(matching_activities)
        
        # Parse frequency requirement
        if frequency_requirement.startswith(">"):
            required_count = int(frequency_requirement[1:])
            return count > required_count
        elif frequency_requirement.startswith(">="):
            required_count = int(frequency_requirement[2:])
            return count >= required_count
        elif frequency_requirement.startswith("="):
            required_count = int(frequency_requirement[1:])
            return count == required_count
        else:
            required_count = int(frequency_requirement)
            return count >= required_count
    
    async def _check_handoff_triggers(self, lead_score: LeadScore, new_status: LeadStatus) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Check if sales handoff should be triggered"""
        
        for config in self.handoff_configs:
            if (lead_score.total_score >= config.trigger_score and 
                new_status == config.trigger_status):
                
                handoff_data = {
                    "config_id": config.id,
                    "lead_score": lead_score.total_score,
                    "qualification_status": new_status.value,
                    "assignment_method": config.sales_team_assignment,
                    "sla_hours": config.sla_hours,
                    "notification_methods": config.notification_methods,
                    "handoff_template": config.handoff_template,
                    "lead_insights": await self.get_lead_insights(lead_score.lead_id)
                }
                
                return True, handoff_data
        
        return False, None
    
    async def _generate_next_actions(self, lead_score: LeadScore, status: LeadStatus) -> List[Dict[str, Any]]:
        """Generate recommended next actions for a lead"""
        
        actions = []
        
        if status == LeadStatus.UNQUALIFIED:
            actions.extend([
                {
                    "action": "send_nurture_email",
                    "priority": "medium",
                    "description": "Send educational content to build engagement"
                },
                {
                    "action": "track_website_behavior",
                    "priority": "low",
                    "description": "Monitor website visits for buying signals"
                }
            ])
        
        elif status == LeadStatus.MARKETING_QUALIFIED:
            actions.extend([
                {
                    "action": "send_product_demo_invite",
                    "priority": "high",
                    "description": "Invite to product demo or trial"
                },
                {
                    "action": "score_increase_campaign",
                    "priority": "medium",
                    "description": "Engage with high-value content"
                }
            ])
        
        elif status == LeadStatus.SALES_QUALIFIED:
            actions.extend([
                {
                    "action": "assign_to_sales_rep",
                    "priority": "urgent",
                    "description": "Assign to appropriate sales representative"
                },
                {
                    "action": "schedule_discovery_call",
                    "priority": "high",
                    "description": "Schedule initial discovery call"
                }
            ])
        
        return actions
    
    async def _identify_qualification_gaps(self, lead_score: LeadScore) -> List[Dict[str, Any]]:
        """Identify what's preventing lead from advancing to next status"""
        
        gaps = []
        current_status = lead_score.qualification_status
        
        # Check next level criteria
        next_statuses = {
            LeadStatus.UNQUALIFIED: LeadStatus.MARKETING_QUALIFIED,
            LeadStatus.MARKETING_QUALIFIED: LeadStatus.SALES_QUALIFIED,
            LeadStatus.SALES_QUALIFIED: LeadStatus.SALES_ACCEPTED
        }
        
        if current_status in next_statuses:
            next_status = next_statuses[current_status]
            
            if next_status in self.qualification_criteria:
                criteria = self.qualification_criteria[next_status]
                
                # Check score gap
                if lead_score.total_score < criteria.min_score:
                    gaps.append({
                        "type": "score",
                        "description": f"Need {criteria.min_score - lead_score.total_score} more points",
                        "current": lead_score.total_score,
                        "required": criteria.min_score
                    })
                
                # Check missing attributes
                for attr in criteria.required_attributes:
                    if attr not in lead_score.attributes:
                        gaps.append({
                            "type": "attribute",
                            "description": f"Missing required attribute: {attr}",
                            "attribute": attr
                        })
                
                # Check missing activities
                for activity_req in criteria.required_activities:
                    if not await self._has_required_activity(lead_score, activity_req):
                        gaps.append({
                            "type": "activity",
                            "description": f"Missing required activity: {activity_req['activity']}",
                            "activity": activity_req
                        })
        
        return gaps
    
    async def _calculate_engagement_level(self, lead_score: LeadScore) -> str:
        """Calculate overall engagement level"""
        
        if not lead_score.activities:
            return "none"
        
        # Calculate engagement based on recent activity
        recent_cutoff = datetime.utcnow() - timedelta(days=30)
        recent_activities = [
            a for a in lead_score.activities
            if datetime.fromisoformat(a["timestamp"]) > recent_cutoff
        ]
        
        engagement_score = lead_score.category_scores.get(ScoreCategory.ENGAGEMENT, 0)
        
        if engagement_score >= 50:
            return "high"
        elif engagement_score >= 20:
            return "medium"
        elif engagement_score > 0:
            return "low"
        else:
            return "none"
    
    async def _identify_risk_factors(self, lead_score: LeadScore) -> List[str]:
        """Identify risk factors that might prevent conversion"""
        
        risks = []
        
        # Check for negative scoring indicators
        if lead_score.category_scores.get(ScoreCategory.BUDGET, 0) < 0:
            risks.append("Budget constraints indicated")
        
        # Check for recent inactivity
        if lead_score.last_activity:
            days_inactive = (datetime.utcnow() - lead_score.last_activity).days
            if days_inactive > 14:
                risks.append(f"No activity for {days_inactive} days")
        
        # Check for disengagement signals
        unsubscribe_activities = [
            a for a in lead_score.activities
            if a["type"] == "email_unsubscribed"
        ]
        if unsubscribe_activities:
            risks.append("Email unsubscribe detected")
        
        return risks
    
    async def _recommend_content(self, lead_score: LeadScore) -> List[Dict[str, str]]:
        """Recommend content based on lead profile and behavior"""
        
        recommendations = []
        
        status = lead_score.qualification_status
        
        if status == LeadStatus.UNQUALIFIED:
            recommendations.extend([
                {"type": "blog_post", "title": "Getting Started Guide", "reason": "Educational content for awareness"},
                {"type": "ebook", "title": "Industry Best Practices", "reason": "Value-driven content to build trust"}
            ])
        
        elif status == LeadStatus.MARKETING_QUALIFIED:
            recommendations.extend([
                {"type": "case_study", "title": "Customer Success Story", "reason": "Social proof for consideration"},
                {"type": "demo_video", "title": "Product Overview Demo", "reason": "Product education for evaluation"}
            ])
        
        elif status == LeadStatus.SALES_QUALIFIED:
            recommendations.extend([
                {"type": "roi_calculator", "title": "ROI Assessment Tool", "reason": "Quantify business value"},
                {"type": "comparison_guide", "title": "Feature Comparison", "reason": "Competitive differentiation"}
            ])
        
        return recommendations
    
    async def _predict_optimal_contact_time(self, lead_score: LeadScore) -> Dict[str, Any]:
        """Predict optimal time to contact lead"""
        
        # Analyze activity patterns
        activity_hours = []
        activity_days = []
        
        for activity in lead_score.activities:
            timestamp = datetime.fromisoformat(activity["timestamp"])
            activity_hours.append(timestamp.hour)
            activity_days.append(timestamp.weekday())
        
        if not activity_hours:
            return {
                "recommended_hour": 14,  # 2 PM default
                "recommended_day": "Tuesday",
                "confidence": "low"
            }
        
        # Find most common hour and day
        from collections import Counter
        hour_counter = Counter(activity_hours)
        day_counter = Counter(activity_days)
        
        optimal_hour = hour_counter.most_common(1)[0][0]
        optimal_day_num = day_counter.most_common(1)[0][0]
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        optimal_day = days[optimal_day_num]
        
        confidence = "high" if len(activity_hours) >= 10 else "medium" if len(activity_hours) >= 5 else "low"
        
        return {
            "recommended_hour": optimal_hour,
            "recommended_day": optimal_day,
            "confidence": confidence
        }
    
    async def _calculate_score_trend(self, lead_score: LeadScore) -> Dict[str, Any]:
        """Calculate score trend over time"""
        
        if len(lead_score.score_history) < 2:
            return {"trend": "insufficient_data"}
        
        # Get scores from last 30 days
        recent_cutoff = datetime.utcnow() - timedelta(days=30)
        recent_history = [
            h for h in lead_score.score_history
            if datetime.fromisoformat(h["timestamp"]) > recent_cutoff
        ]
        
        if len(recent_history) < 2:
            return {"trend": "stable", "change": 0}
        
        # Calculate trend
        first_score = recent_history[0]["new_total"]
        last_score = recent_history[-1]["new_total"]
        change = last_score - first_score
        
        if change > 10:
            trend = "increasing"
        elif change < -10:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "change": change,
            "period_days": 30
        }
    
    async def _evaluate_condition(self, value: Any, condition: str) -> bool:
        """Evaluate a condition against a value"""
        
        if condition.startswith(">"):
            threshold = float(condition[1:])
            return float(value) > threshold
        elif condition.startswith("<"):
            threshold = float(condition[1:])
            return float(value) < threshold
        elif condition.startswith(">="):
            threshold = float(condition[2:])
            return float(value) >= threshold
        elif condition.startswith("<="):
            threshold = float(condition[2:])
            return float(value) <= threshold
        elif condition.startswith("="):
            return str(value) == condition[1:]
        else:
            return str(value) == condition
    
    async def _evaluate_condition_on_lead(self, condition: Dict[str, Any], lead_score: LeadScore, activity: LeadActivity) -> bool:
        """Evaluate a complex condition on lead data"""
        
        # Implementation would check various lead attributes and activity patterns
        # For now, return True as placeholder
        return True
    
    def export_configuration(self) -> Dict[str, Any]:
        """Export scoring configuration for backup or replication"""
        
        return {
            "tenant_id": self.tenant_id,
            "scoring_rules": {rule_id: rule.dict() for rule_id, rule in self.scoring_rules.items()},
            "qualification_criteria": {status.value: criteria.dict() for status, criteria in self.qualification_criteria.items()},
            "handoff_configs": [config.dict() for config in self.handoff_configs]
        }
    
    def import_configuration(self, config: Dict[str, Any]) -> None:
        """Import scoring configuration"""
        
        # Import scoring rules
        if "scoring_rules" in config:
            self.scoring_rules = {}
            for rule_id, rule_data in config["scoring_rules"].items():
                self.scoring_rules[rule_id] = ScoringRule(**rule_data)
        
        # Import qualification criteria
        if "qualification_criteria" in config:
            self.qualification_criteria = {}
            for status_str, criteria_data in config["qualification_criteria"].items():
                status = LeadStatus(status_str)
                self.qualification_criteria[status] = QualificationCriteria(**criteria_data)
        
        # Import handoff configs
        if "handoff_configs" in config:
            self.handoff_configs = []
            for config_data in config["handoff_configs"]:
                self.handoff_configs.append(HandoffConfiguration(**config_data))