"""
Campaign Aggregate - Central domain model for marketing campaign management

This aggregate handles campaign lifecycle including:
- Campaign creation and planning
- Budget management and allocation
- Performance tracking and optimization
- Multi-channel campaign coordination
- AI-driven optimization
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, DateTime, Numeric, Text, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from .base import AggregateRoot, DomainEvent, ValueObject, BaseEntity, BusinessRuleViolation


class CampaignType(str, Enum):
    """Types of marketing campaigns"""
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    PAID_SEARCH = "paid_search"
    DISPLAY_ADS = "display_ads"
    CONTENT_MARKETING = "content_marketing"
    WEBINAR = "webinar"
    EVENT = "event"
    INFLUENCER = "influencer"
    AFFILIATE = "affiliate"
    RETARGETING = "retargeting"
    VIDEO_ADS = "video_ads"
    NATIVE_ADS = "native_ads"
    MULTI_CHANNEL = "multi_channel"


class CampaignStatus(str, Enum):
    """Campaign status throughout the lifecycle"""
    DRAFT = "draft"
    PLANNED = "planned"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class CampaignObjective(str, Enum):
    """Campaign objectives"""
    BRAND_AWARENESS = "brand_awareness"
    LEAD_GENERATION = "lead_generation"
    SALES_CONVERSION = "sales_conversion"
    CUSTOMER_RETENTION = "customer_retention"
    WEBSITE_TRAFFIC = "website_traffic"
    ENGAGEMENT = "engagement"
    APP_INSTALLS = "app_installs"
    VIDEO_VIEWS = "video_views"
    REACH = "reach"


class OptimizationGoal(str, Enum):
    """Optimization goals for AI-driven campaigns"""
    MINIMIZE_CPA = "minimize_cpa"  # Cost Per Acquisition
    MAXIMIZE_ROI = "maximize_roi"  # Return on Investment
    MAXIMIZE_REACH = "maximize_reach"
    MAXIMIZE_ENGAGEMENT = "maximize_engagement"
    MINIMIZE_CPC = "minimize_cpc"  # Cost Per Click
    MAXIMIZE_CONVERSIONS = "maximize_conversions"


class ChannelConfig(ValueObject):
    """Value object for channel-specific configuration"""
    
    channel: str  # email, facebook, google_ads, linkedin, etc.
    is_enabled: bool = True
    budget_allocation: Decimal = Decimal('0.00')  # Amount or percentage
    allocation_type: str = "amount"  # amount or percentage
    platform_config: Dict[str, Any] = Field(default_factory=dict)
    targeting_criteria: Dict[str, Any] = Field(default_factory=dict)
    creative_config: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('allocation_type')
    def validate_allocation_type(cls, v):
        if v not in ['amount', 'percentage']:
            raise ValueError('Allocation type must be "amount" or "percentage"')
        return v


class CampaignBudget(ValueObject):
    """Value object for campaign budget management"""
    
    total_budget: Decimal
    spent_amount: Decimal = Decimal('0.00')
    daily_budget: Optional[Decimal] = None
    currency: str = "USD"
    budget_type: str = "total"  # total, daily, monthly
    auto_optimization: bool = False
    
    @property
    def remaining_budget(self) -> Decimal:
        """Get remaining budget"""
        return max(Decimal('0.00'), self.total_budget - self.spent_amount)
    
    @property
    def spend_percentage(self) -> float:
        """Get spend percentage"""
        if self.total_budget == 0:
            return 0.0
        return float((self.spent_amount / self.total_budget) * 100)
    
    @property
    def is_budget_exceeded(self) -> bool:
        """Check if budget is exceeded"""
        return self.spent_amount > self.total_budget
    
    @validator('total_budget', 'spent_amount', 'daily_budget')
    def validate_positive_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError('Budget amounts must be positive')
        return v


class CampaignMetrics(ValueObject):
    """Value object for campaign performance metrics"""
    
    # Reach and Impressions
    impressions: int = 0
    reach: int = 0
    unique_clicks: int = 0
    
    # Engagement Metrics
    clicks: int = 0
    click_through_rate: float = 0.0
    engagement_rate: float = 0.0
    
    # Conversion Metrics
    conversions: int = 0
    conversion_rate: float = 0.0
    cost_per_conversion: Decimal = Decimal('0.00')
    
    # Financial Metrics
    revenue: Decimal = Decimal('0.00')
    roi: float = 0.0  # Return on Investment
    roas: float = 0.0  # Return on Ad Spend
    
    # Cost Metrics
    cost_per_click: Decimal = Decimal('0.00')
    cost_per_impression: Decimal = Decimal('0.00')
    
    # Lead Metrics
    leads_generated: int = 0
    qualified_leads: int = 0
    cost_per_lead: Decimal = Decimal('0.00')
    
    # Quality Metrics
    quality_score: Optional[float] = None
    relevance_score: Optional[float] = None
    
    # Time-based Metrics
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    def calculate_derived_metrics(self, spent_amount: Decimal) -> 'CampaignMetrics':
        """Calculate derived metrics based on spent amount"""
        
        # Calculate rates
        ctr = (self.clicks / self.impressions * 100) if self.impressions > 0 else 0.0
        conv_rate = (self.conversions / self.clicks * 100) if self.clicks > 0 else 0.0
        
        # Calculate costs
        cpc = spent_amount / self.clicks if self.clicks > 0 else Decimal('0.00')
        cpm = spent_amount / self.impressions * 1000 if self.impressions > 0 else Decimal('0.00')
        cpa = spent_amount / self.conversions if self.conversions > 0 else Decimal('0.00')
        cpl = spent_amount / self.leads_generated if self.leads_generated > 0 else Decimal('0.00')
        
        # Calculate ROI and ROAS
        roi_value = ((self.revenue - spent_amount) / spent_amount * 100) if spent_amount > 0 else 0.0
        roas_value = (self.revenue / spent_amount) if spent_amount > 0 else 0.0
        
        return self.copy(update={
            "click_through_rate": ctr,
            "conversion_rate": conv_rate,
            "cost_per_click": cpc,
            "cost_per_impression": cpm,
            "cost_per_conversion": cpa,
            "cost_per_lead": cpl,
            "roi": roi_value,
            "roas": float(roas_value),
            "last_updated": datetime.utcnow()
        })


class CampaignSchedule(ValueObject):
    """Value object for campaign scheduling"""
    
    start_date: datetime
    end_date: Optional[datetime] = None
    timezone: str = "UTC"
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly
    day_parting: Optional[Dict[str, Any]] = None  # Time-of-day targeting
    
    @property
    def is_active_now(self) -> bool:
        """Check if campaign should be active now"""
        now = datetime.utcnow()
        if now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
    
    @property
    def duration_days(self) -> Optional[int]:
        """Get campaign duration in days"""
        if not self.end_date:
            return None
        return (self.end_date - self.start_date).days


class TargetingCriteria(ValueObject):
    """Value object for campaign targeting"""
    
    # Demographic Targeting
    age_range: Optional[Dict[str, int]] = None  # {"min": 18, "max": 65}
    gender: Optional[List[str]] = None
    location: Optional[Dict[str, Any]] = None
    languages: Optional[List[str]] = None
    
    # Interest and Behavior Targeting
    interests: List[str] = Field(default_factory=list)
    behaviors: List[str] = Field(default_factory=list)
    custom_audiences: List[str] = Field(default_factory=list)
    lookalike_audiences: List[str] = Field(default_factory=list)
    
    # Professional Targeting (B2B)
    job_titles: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)
    company_sizes: List[str] = Field(default_factory=list)
    
    # Device and Platform Targeting
    devices: List[str] = Field(default_factory=list)
    operating_systems: List[str] = Field(default_factory=list)
    browsers: List[str] = Field(default_factory=list)
    
    # Advanced Targeting
    keywords: List[str] = Field(default_factory=list)
    exclusion_criteria: Dict[str, Any] = Field(default_factory=dict)


class OptimizationRule(ValueObject):
    """Value object for AI optimization rules"""
    
    rule_id: UUID = Field(default_factory=uuid4)
    rule_type: str  # budget_reallocation, bid_adjustment, audience_expansion, etc.
    condition: Dict[str, Any]  # Condition that triggers the rule
    action: Dict[str, Any]  # Action to take when condition is met
    is_enabled: bool = True
    trigger_threshold: Optional[float] = None
    cooldown_hours: int = 24  # Hours to wait before re-triggering
    last_triggered: Optional[datetime] = None
    
    @property
    def can_trigger(self) -> bool:
        """Check if rule can be triggered (not in cooldown)"""
        if not self.is_enabled:
            return False
        if not self.last_triggered:
            return True
        hours_since_trigger = (datetime.utcnow() - self.last_triggered).total_seconds() / 3600
        return hours_since_trigger >= self.cooldown_hours


# Domain Events
class CampaignCreated(DomainEvent):
    """Event raised when a new campaign is created"""
    event_type: str = "campaign.created"


class CampaignLaunched(DomainEvent):
    """Event raised when a campaign is launched"""
    event_type: str = "campaign.launched"


class CampaignPaused(DomainEvent):
    """Event raised when a campaign is paused"""
    event_type: str = "campaign.paused"


class CampaignCompleted(DomainEvent):
    """Event raised when a campaign completes"""
    event_type: str = "campaign.completed"


class CampaignBudgetExceeded(DomainEvent):
    """Event raised when campaign budget is exceeded"""
    event_type: str = "campaign.budget_exceeded"


class CampaignOptimized(DomainEvent):
    """Event raised when campaign is optimized by AI"""
    event_type: str = "campaign.optimized"


class CampaignMetricsUpdated(DomainEvent):
    """Event raised when campaign metrics are updated"""
    event_type: str = "campaign.metrics_updated"


# Campaign Aggregate Root
class Campaign(AggregateRoot):
    """
    Campaign aggregate root - manages campaign lifecycle and business rules
    """
    
    # Basic Information
    name: str
    description: Optional[str] = None
    campaign_type: CampaignType
    objective: CampaignObjective
    status: CampaignStatus = CampaignStatus.DRAFT
    
    # Budget and Financial
    budget: CampaignBudget
    
    # Scheduling
    schedule: CampaignSchedule
    
    # Targeting and Audience
    targeting: TargetingCriteria = Field(default_factory=TargetingCriteria)
    
    # Channel Configuration
    channels: List[ChannelConfig] = Field(default_factory=list)
    
    # Performance Metrics
    metrics: CampaignMetrics = Field(default_factory=CampaignMetrics)
    
    # AI Optimization
    optimization_goal: Optional[OptimizationGoal] = None
    optimization_rules: List[OptimizationRule] = Field(default_factory=list)
    ai_optimization_enabled: bool = False
    
    # Creative Assets and Content
    creative_assets: Dict[str, Any] = Field(default_factory=dict)
    content_variations: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Attribution and Tracking
    utm_parameters: Dict[str, str] = Field(default_factory=dict)
    tracking_pixels: List[str] = Field(default_factory=list)
    conversion_goals: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Management and Ownership
    owner_id: Optional[UUID] = None
    team_members: List[UUID] = Field(default_factory=list)
    
    # Custom Fields and Tags
    tags: Set[str] = Field(default_factory=set)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    
    # Notes and History
    notes: List[str] = Field(default_factory=list)
    
    def __init__(self, **data):
        super().__init__(**data)
        
        # Auto-generate UTM parameters if not provided
        if not self.utm_parameters:
            self.utm_parameters = {
                "utm_source": "bizosaas",
                "utm_medium": self.campaign_type.value,
                "utm_campaign": self.name.lower().replace(" ", "_"),
                "utm_term": "",
                "utm_content": ""
            }
        
        # Raise creation event
        self.add_domain_event(CampaignCreated(
            aggregate_id=self.id,
            aggregate_type="Campaign",
            tenant_id=self.tenant_id,
            data={
                "campaign_id": str(self.id),
                "name": self.name,
                "campaign_type": self.campaign_type.value,
                "objective": self.objective.value,
                "budget": float(self.budget.total_budget),
                "start_date": self.schedule.start_date.isoformat(),
                "owner_id": str(self.owner_id) if self.owner_id else None
            }
        ))
    
    def launch_campaign(self, user_id: Optional[UUID] = None) -> None:
        """Launch the campaign"""
        
        # Validate campaign readiness
        self._validate_campaign_launch()
        
        # Check if it's time to launch
        if not self.schedule.is_active_now:
            self.status = CampaignStatus.SCHEDULED
        else:
            self.status = CampaignStatus.ACTIVE
        
        self.increment_version()
        
        # Add note about launch
        self.add_note(f"Campaign launched by {user_id or 'system'}")
        
        # Raise launch event
        self.add_domain_event(CampaignLaunched(
            aggregate_id=self.id,
            aggregate_type="Campaign",
            tenant_id=self.tenant_id,
            data={
                "campaign_id": str(self.id),
                "launched_by": str(user_id) if user_id else None,
                "launch_time": datetime.utcnow().isoformat(),
                "scheduled_start": self.schedule.start_date.isoformat()
            }
        ))
    
    def pause_campaign(self, user_id: Optional[UUID] = None, reason: Optional[str] = None) -> None:
        """Pause the campaign"""
        
        if self.status not in [CampaignStatus.ACTIVE, CampaignStatus.SCHEDULED]:
            raise BusinessRuleViolation(f"Cannot pause campaign with status {self.status.value}")
        
        self.status = CampaignStatus.PAUSED
        self.increment_version()
        
        # Add note about pause
        pause_note = f"Campaign paused by {user_id or 'system'}"
        if reason:
            pause_note += f" - Reason: {reason}"
        self.add_note(pause_note)
        
        # Raise pause event
        self.add_domain_event(CampaignPaused(
            aggregate_id=self.id,
            aggregate_type="Campaign",
            tenant_id=self.tenant_id,
            data={
                "campaign_id": str(self.id),
                "paused_by": str(user_id) if user_id else None,
                "pause_time": datetime.utcnow().isoformat(),
                "reason": reason
            }
        ))
    
    def resume_campaign(self, user_id: Optional[UUID] = None) -> None:
        """Resume a paused campaign"""
        
        if self.status != CampaignStatus.PAUSED:
            raise BusinessRuleViolation(f"Cannot resume campaign with status {self.status.value}")
        
        # Check if campaign period is still valid
        if self.schedule.end_date and datetime.utcnow() > self.schedule.end_date:
            self.status = CampaignStatus.COMPLETED
        elif self.schedule.is_active_now:
            self.status = CampaignStatus.ACTIVE
        else:
            self.status = CampaignStatus.SCHEDULED
        
        self.increment_version()
        
        # Add note about resume
        self.add_note(f"Campaign resumed by {user_id or 'system'}")
    
    def complete_campaign(self, user_id: Optional[UUID] = None) -> None:
        """Complete the campaign"""
        
        if self.status in [CampaignStatus.COMPLETED, CampaignStatus.CANCELLED, CampaignStatus.ARCHIVED]:
            return  # Already in final state
        
        self.status = CampaignStatus.COMPLETED
        self.increment_version()
        
        # Add note about completion
        self.add_note(f"Campaign completed by {user_id or 'system'}")
        
        # Raise completion event
        self.add_domain_event(CampaignCompleted(
            aggregate_id=self.id,
            aggregate_type="Campaign",
            tenant_id=self.tenant_id,
            data={
                "campaign_id": str(self.id),
                "completed_by": str(user_id) if user_id else None,
                "completion_time": datetime.utcnow().isoformat(),
                "final_metrics": self.metrics.dict(),
                "total_spent": float(self.budget.spent_amount),
                "roi": self.metrics.roi
            }
        ))
    
    def update_budget(self, new_budget: CampaignBudget, user_id: Optional[UUID] = None) -> None:
        """Update campaign budget"""
        
        old_budget = self.budget.total_budget
        self.budget = new_budget
        self.increment_version()
        
        # Check for budget exceeded
        if new_budget.is_budget_exceeded:
            self.add_domain_event(CampaignBudgetExceeded(
                aggregate_id=self.id,
                aggregate_type="Campaign",
                tenant_id=self.tenant_id,
                data={
                    "campaign_id": str(self.id),
                    "total_budget": float(new_budget.total_budget),
                    "spent_amount": float(new_budget.spent_amount),
                    "overspend": float(new_budget.spent_amount - new_budget.total_budget)
                }
            ))
        
        # Add note about budget update
        self.add_note(f"Budget updated from {old_budget} to {new_budget.total_budget} by {user_id or 'system'}")
    
    def update_metrics(self, new_metrics: CampaignMetrics, user_id: Optional[UUID] = None) -> None:
        """Update campaign performance metrics"""
        
        # Calculate derived metrics
        updated_metrics = new_metrics.calculate_derived_metrics(self.budget.spent_amount)
        
        old_conversions = self.metrics.conversions
        old_roi = self.metrics.roi
        
        self.metrics = updated_metrics
        self.increment_version()
        
        # Trigger AI optimization if enabled and criteria met
        if self.ai_optimization_enabled and self.status == CampaignStatus.ACTIVE:
            self._check_optimization_triggers()
        
        # Raise metrics update event
        self.add_domain_event(CampaignMetricsUpdated(
            aggregate_id=self.id,
            aggregate_type="Campaign",
            tenant_id=self.tenant_id,
            data={
                "campaign_id": str(self.id),
                "new_conversions": updated_metrics.conversions - old_conversions,
                "current_roi": updated_metrics.roi,
                "roi_change": updated_metrics.roi - old_roi,
                "metrics": updated_metrics.dict()
            }
        ))
    
    def add_channel(self, channel_config: ChannelConfig) -> None:
        """Add a channel configuration"""
        
        # Check if channel already exists
        for i, existing_channel in enumerate(self.channels):
            if existing_channel.channel == channel_config.channel:
                # Update existing channel
                self.channels[i] = channel_config
                self.increment_version()
                return
        
        # Add new channel
        self.channels.append(channel_config)
        self.increment_version()
    
    def remove_channel(self, channel_name: str) -> None:
        """Remove a channel configuration"""
        
        self.channels = [c for c in self.channels if c.channel != channel_name]
        self.increment_version()
    
    def enable_ai_optimization(self, optimization_goal: OptimizationGoal, user_id: Optional[UUID] = None) -> None:
        """Enable AI optimization for the campaign"""
        
        self.ai_optimization_enabled = True
        self.optimization_goal = optimization_goal
        self.increment_version()
        
        # Add default optimization rules based on goal
        self._add_default_optimization_rules(optimization_goal)
        
        # Add note about AI optimization
        self.add_note(f"AI optimization enabled with goal: {optimization_goal.value} by {user_id or 'system'}")
    
    def add_optimization_rule(self, rule: OptimizationRule) -> None:
        """Add an optimization rule"""
        
        self.optimization_rules.append(rule)
        self.increment_version()
    
    def remove_optimization_rule(self, rule_id: UUID) -> None:
        """Remove an optimization rule"""
        
        self.optimization_rules = [r for r in self.optimization_rules if r.rule_id != rule_id]
        self.increment_version()
    
    def optimize_campaign(self, optimization_data: Dict[str, Any], user_id: Optional[UUID] = None) -> None:
        """Apply optimization recommendations"""
        
        optimization_actions = []
        
        # Apply budget reallocations
        if "budget_reallocations" in optimization_data:
            for channel_name, new_allocation in optimization_data["budget_reallocations"].items():
                for i, channel in enumerate(self.channels):
                    if channel.channel == channel_name:
                        old_allocation = channel.budget_allocation
                        self.channels[i] = channel.copy(update={"budget_allocation": Decimal(str(new_allocation))})
                        optimization_actions.append(f"Reallocated {channel_name} budget from {old_allocation} to {new_allocation}")
        
        # Apply bid adjustments
        if "bid_adjustments" in optimization_data:
            for channel_name, bid_adjustment in optimization_data["bid_adjustments"].items():
                for i, channel in enumerate(self.channels):
                    if channel.channel == channel_name:
                        channel_config = channel.platform_config.copy()
                        channel_config["bid_adjustment"] = bid_adjustment
                        self.channels[i] = channel.copy(update={"platform_config": channel_config})
                        optimization_actions.append(f"Adjusted {channel_name} bid by {bid_adjustment}%")
        
        # Apply audience expansions
        if "audience_expansions" in optimization_data:
            for audience_type, new_audiences in optimization_data["audience_expansions"].items():
                if audience_type == "interests":
                    self.targeting.interests.extend(new_audiences)
                elif audience_type == "lookalike_audiences":
                    self.targeting.lookalike_audiences.extend(new_audiences)
                optimization_actions.append(f"Expanded {audience_type} targeting")
        
        self.increment_version()
        
        # Add note about optimization
        self.add_note(f"Campaign optimized by AI: {'; '.join(optimization_actions)}")
        
        # Raise optimization event
        self.add_domain_event(CampaignOptimized(
            aggregate_id=self.id,
            aggregate_type="Campaign",
            tenant_id=self.tenant_id,
            data={
                "campaign_id": str(self.id),
                "optimization_actions": optimization_actions,
                "optimization_data": optimization_data,
                "optimized_by": str(user_id) if user_id else "ai_system"
            }
        ))
    
    def add_team_member(self, user_id: UUID) -> None:
        """Add a team member to the campaign"""
        
        if user_id not in self.team_members:
            self.team_members.append(user_id)
            self.increment_version()
    
    def remove_team_member(self, user_id: UUID) -> None:
        """Remove a team member from the campaign"""
        
        if user_id in self.team_members:
            self.team_members.remove(user_id)
            self.increment_version()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the campaign"""
        self.tags.add(tag.lower().strip())
        self.increment_version()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the campaign"""
        self.tags.discard(tag.lower().strip())
        self.increment_version()
    
    def add_note(self, note: str, user_id: Optional[UUID] = None) -> None:
        """Add a note to the campaign"""
        timestamp = datetime.utcnow().isoformat()
        formatted_note = f"[{timestamp}] {note}"
        if user_id:
            formatted_note = f"[{timestamp}] [{user_id}] {note}"
        
        self.notes.append(formatted_note)
        self.increment_version()
    
    def _validate_campaign_launch(self) -> None:
        """Validate that campaign is ready to launch"""
        
        if not self.name.strip():
            raise BusinessRuleViolation("Campaign name is required")
        
        if self.budget.total_budget <= 0:
            raise BusinessRuleViolation("Campaign budget must be greater than 0")
        
        if not self.channels:
            raise BusinessRuleViolation("At least one channel must be configured")
        
        if not any(channel.is_enabled for channel in self.channels):
            raise BusinessRuleViolation("At least one channel must be enabled")
        
        # Validate budget allocation
        total_allocation = sum(channel.budget_allocation for channel in self.channels if channel.is_enabled)
        if total_allocation > self.budget.total_budget:
            raise BusinessRuleViolation("Total channel budget allocation exceeds campaign budget")
    
    def _check_optimization_triggers(self) -> None:
        """Check if any optimization rules should be triggered"""
        
        for rule in self.optimization_rules:
            if rule.can_trigger and self._evaluate_optimization_condition(rule.condition):
                # Mark rule as triggered
                rule.last_triggered = datetime.utcnow()
                
                # Apply optimization action (simplified - would call AI service in real implementation)
                self._apply_optimization_action(rule.action)
    
    def _evaluate_optimization_condition(self, condition: Dict[str, Any]) -> bool:
        """Evaluate if an optimization condition is met"""
        
        # Simplified condition evaluation
        metric_name = condition.get("metric")
        operator = condition.get("operator")
        threshold = condition.get("threshold")
        
        if not all([metric_name, operator, threshold]):
            return False
        
        current_value = getattr(self.metrics, metric_name, 0)
        
        if operator == "less_than":
            return current_value < threshold
        elif operator == "greater_than":
            return current_value > threshold
        elif operator == "equals":
            return current_value == threshold
        
        return False
    
    def _apply_optimization_action(self, action: Dict[str, Any]) -> None:
        """Apply an optimization action"""
        
        # Simplified action application
        action_type = action.get("type")
        
        if action_type == "pause_low_performing_channels":
            for channel in self.channels:
                # Simplified logic - would use real performance data
                if channel.budget_allocation > 0:  # Placeholder condition
                    channel.is_enabled = False
        
        # In a real implementation, this would trigger more sophisticated optimizations
        self.increment_version()
    
    def _add_default_optimization_rules(self, goal: OptimizationGoal) -> None:
        """Add default optimization rules based on the goal"""
        
        if goal == OptimizationGoal.MINIMIZE_CPA:
            # Rule to pause high CPA channels
            rule = OptimizationRule(
                rule_type="pause_high_cpa_channels",
                condition={"metric": "cost_per_conversion", "operator": "greater_than", "threshold": 100},
                action={"type": "pause_channel", "threshold_multiplier": 2.0}
            )
            self.optimization_rules.append(rule)
        
        elif goal == OptimizationGoal.MAXIMIZE_ROI:
            # Rule to increase budget for high ROI channels
            rule = OptimizationRule(
                rule_type="increase_high_roi_budget",
                condition={"metric": "roi", "operator": "greater_than", "threshold": 200},
                action={"type": "increase_budget", "increase_percentage": 20}
            )
            self.optimization_rules.append(rule)
    
    @property
    def days_running(self) -> int:
        """Get number of days campaign has been running"""
        start_date = max(self.schedule.start_date, self.created_at)
        return (datetime.utcnow() - start_date).days
    
    @property
    def is_active(self) -> bool:
        """Check if campaign is currently active"""
        return self.status == CampaignStatus.ACTIVE and self.schedule.is_active_now
    
    @property
    def performance_summary(self) -> Dict[str, Any]:
        """Get a summary of campaign performance"""
        return {
            "impressions": self.metrics.impressions,
            "clicks": self.metrics.clicks,
            "conversions": self.metrics.conversions,
            "spent": float(self.budget.spent_amount),
            "remaining_budget": float(self.budget.remaining_budget),
            "roi": self.metrics.roi,
            "ctr": self.metrics.click_through_rate,
            "conversion_rate": self.metrics.conversion_rate,
            "days_running": self.days_running
        }


# SQLAlchemy Model for Persistence
class CampaignEntity(BaseEntity):
    """SQLAlchemy model for Campaign persistence"""
    
    __tablename__ = "campaigns"
    
    # Basic Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(SQLEnum(CampaignType), nullable=False)
    objective = Column(SQLEnum(CampaignObjective), nullable=False)
    status = Column(SQLEnum(CampaignStatus), nullable=False, default=CampaignStatus.DRAFT)
    
    # Budget and Financial (stored as JSON)
    budget_data = Column(JSON, nullable=False)
    
    # Scheduling (stored as JSON)
    schedule_data = Column(JSON, nullable=False)
    
    # Targeting (stored as JSON)
    targeting_data = Column(JSON)
    
    # Channel Configuration (stored as JSON)
    channels_data = Column(JSON, default=list)
    
    # Performance Metrics (stored as JSON)
    metrics_data = Column(JSON)
    
    # AI Optimization
    optimization_goal = Column(SQLEnum(OptimizationGoal))
    optimization_rules_data = Column(JSON, default=list)
    ai_optimization_enabled = Column(Boolean, default=False)
    
    # Creative Assets and Content (stored as JSON)
    creative_assets = Column(JSON, default=dict)
    content_variations = Column(JSON, default=list)
    
    # Attribution and Tracking (stored as JSON)
    utm_parameters = Column(JSON, default=dict)
    tracking_pixels = Column(JSON, default=list)
    conversion_goals = Column(JSON, default=list)
    
    # Management and Ownership
    owner_id = Column(PGUUID(as_uuid=True))
    team_members = Column(JSON, default=list)
    
    # Custom Fields and Tags
    tags = Column(JSON, default=list)
    custom_fields = Column(JSON, default=dict)
    
    # Notes
    notes = Column(JSON, default=list)
    
    def to_domain(self) -> Campaign:
        """Convert SQLAlchemy model to domain aggregate"""
        
        # Convert JSON data back to value objects
        budget = CampaignBudget(**self.budget_data)
        schedule = CampaignSchedule(**self.schedule_data)
        targeting = TargetingCriteria(**self.targeting_data) if self.targeting_data else TargetingCriteria()
        metrics = CampaignMetrics(**self.metrics_data) if self.metrics_data else CampaignMetrics()
        
        # Convert channels
        channels = [ChannelConfig(**channel_data) for channel_data in (self.channels_data or [])]
        
        # Convert optimization rules
        optimization_rules = [OptimizationRule(**rule_data) for rule_data in (self.optimization_rules_data or [])]
        
        return Campaign(
            id=self.id,
            tenant_id=self.tenant_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            version=self.version,
            name=self.name,
            description=self.description,
            campaign_type=self.campaign_type,
            objective=self.objective,
            status=self.status,
            budget=budget,
            schedule=schedule,
            targeting=targeting,
            channels=channels,
            metrics=metrics,
            optimization_goal=self.optimization_goal,
            optimization_rules=optimization_rules,
            ai_optimization_enabled=self.ai_optimization_enabled,
            creative_assets=self.creative_assets or {},
            content_variations=self.content_variations or [],
            utm_parameters=self.utm_parameters or {},
            tracking_pixels=self.tracking_pixels or [],
            conversion_goals=self.conversion_goals or [],
            owner_id=self.owner_id,
            team_members=[UUID(member_id) for member_id in (self.team_members or [])],
            tags=set(self.tags or []),
            custom_fields=self.custom_fields or {},
            notes=self.notes or []
        )
    
    @classmethod
    def from_domain(cls, domain_campaign: Campaign) -> 'CampaignEntity':
        """Create SQLAlchemy model from domain aggregate"""
        
        return cls(
            id=domain_campaign.id,
            tenant_id=domain_campaign.tenant_id,
            created_at=domain_campaign.created_at,
            updated_at=domain_campaign.updated_at,
            version=domain_campaign.version,
            name=domain_campaign.name,
            description=domain_campaign.description,
            campaign_type=domain_campaign.campaign_type,
            objective=domain_campaign.objective,
            status=domain_campaign.status,
            budget_data=domain_campaign.budget.dict(),
            schedule_data=domain_campaign.schedule.dict(),
            targeting_data=domain_campaign.targeting.dict(),
            channels_data=[channel.dict() for channel in domain_campaign.channels],
            metrics_data=domain_campaign.metrics.dict(),
            optimization_goal=domain_campaign.optimization_goal,
            optimization_rules_data=[rule.dict() for rule in domain_campaign.optimization_rules],
            ai_optimization_enabled=domain_campaign.ai_optimization_enabled,
            creative_assets=domain_campaign.creative_assets,
            content_variations=domain_campaign.content_variations,
            utm_parameters=domain_campaign.utm_parameters,
            tracking_pixels=domain_campaign.tracking_pixels,
            conversion_goals=domain_campaign.conversion_goals,
            owner_id=domain_campaign.owner_id,
            team_members=[str(member_id) for member_id in domain_campaign.team_members],
            tags=list(domain_campaign.tags),
            custom_fields=domain_campaign.custom_fields,
            notes=domain_campaign.notes
        )