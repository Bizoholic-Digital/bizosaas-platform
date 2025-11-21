"""
Sales Funnel Builder - BizoholicSaaS
Advanced drag-and-drop sales funnel builder with Mautic integration
"""

import uuid
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class FunnelStageType(str, Enum):
    """Types of funnel stages"""
    LEAD_MAGNET = "lead_magnet"
    WELCOME_SEQUENCE = "welcome_sequence" 
    NURTURE_SEQUENCE = "nurture_sequence"
    SALES_SEQUENCE = "sales_sequence"
    RETENTION_SEQUENCE = "retention_sequence"
    WIN_BACK_SEQUENCE = "win_back_sequence"
    UPSELL_SEQUENCE = "upsell_sequence"

class TriggerType(str, Enum):
    """Types of automation triggers"""
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    LINK_CLICKED = "link_clicked"
    FORM_SUBMITTED = "form_submitted"
    PAGE_VISITED = "page_visited"
    TIME_DELAY = "time_delay"
    LEAD_SCORE = "lead_score"
    TAG_ADDED = "tag_added"
    SEGMENT_JOINED = "segment_joined"

class ActionType(str, Enum):
    """Types of automation actions"""
    SEND_EMAIL = "send_email"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    ADD_TO_SEGMENT = "add_to_segment"
    REMOVE_FROM_SEGMENT = "remove_from_segment"
    UPDATE_FIELD = "update_field"
    ADD_POINTS = "add_points"
    SUBTRACT_POINTS = "subtract_points"
    CHANGE_STAGE = "change_stage"
    SEND_NOTIFICATION = "send_notification"
    WEBHOOK = "webhook"

class FunnelTemplate(str, Enum):
    """Pre-built funnel templates"""
    SAAS_TRIAL = "saas_trial"
    LEAD_GENERATION = "lead_generation"
    E_COMMERCE = "e_commerce"
    WEBINAR = "webinar"
    CONSULTATION = "consultation"
    NEWSLETTER = "newsletter"
    PRODUCT_LAUNCH = "product_launch"
    ABANDONED_CART = "abandoned_cart"

# Pydantic Models
class FunnelStageConfig(BaseModel):
    """Configuration for a single funnel stage"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    stage_type: FunnelStageType
    description: Optional[str] = None
    position: int = 0
    is_active: bool = True
    
    # Email configuration
    email_templates: List[Dict[str, Any]] = []
    delay_before_action: Optional[int] = None  # minutes
    
    # Conditions and triggers
    entry_conditions: List[Dict[str, Any]] = []
    exit_conditions: List[Dict[str, Any]] = []
    
    # Actions to perform
    actions: List[Dict[str, Any]] = []
    
    # Analytics
    conversion_goals: Dict[str, Any] = {}

class AutomationRule(BaseModel):
    """Automation rule configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    trigger: TriggerType
    trigger_config: Dict[str, Any] = {}
    conditions: List[Dict[str, Any]] = []
    actions: List[ActionType]
    action_configs: List[Dict[str, Any]] = []
    is_active: bool = True
    priority: int = 0

class EmailTemplate(BaseModel):
    """Email template configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    personalization_fields: List[str] = []
    dynamic_content_rules: List[Dict[str, Any]] = []

class FunnelAnalytics(BaseModel):
    """Funnel performance analytics"""
    total_entries: int = 0
    total_completions: int = 0
    completion_rate: float = 0.0
    average_time_to_complete: Optional[float] = None
    stage_conversion_rates: Dict[str, float] = {}
    revenue_generated: float = 0.0
    cost_per_conversion: Optional[float] = None

class AdvancedFunnelBuilder:
    """Advanced Sales Funnel Builder with Mautic Integration"""
    
    def __init__(self, tenant_id: str, user_id: str):
        self.tenant_id = tenant_id
        self.user_id = user_id
    
    def get_funnel_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get pre-built funnel templates"""
        
        templates = {
            FunnelTemplate.SAAS_TRIAL: {
                "name": "SaaS Free Trial Funnel",
                "description": "Convert trial users to paid subscribers",
                "stages": [
                    {
                        "name": "Trial Welcome",
                        "stage_type": FunnelStageType.WELCOME_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "Welcome & Getting Started",
                                "subject": "Welcome to {company_name}! Let's get you started",
                                "delay_hours": 0
                            }
                        ]
                    },
                    {
                        "name": "Feature Education",
                        "stage_type": FunnelStageType.NURTURE_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "Key Features Tour",
                                "subject": "5 features that will transform your workflow",
                                "delay_hours": 24
                            },
                            {
                                "name": "Success Stories",
                                "subject": "How {customer_name} increased productivity by 40%",
                                "delay_hours": 72
                            }
                        ]
                    },
                    {
                        "name": "Trial Ending Reminder",
                        "stage_type": FunnelStageType.SALES_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "3 Days Left",
                                "subject": "Your trial expires in 3 days - Save 20%",
                                "delay_hours": 168  # 7 days after start
                            },
                            {
                                "name": "Last Day",
                                "subject": "Last chance to save 20% on your subscription",
                                "delay_hours": 216  # 9 days after start
                            }
                        ]
                    }
                ],
                "automation_rules": [
                    {
                        "name": "Feature Usage Trigger",
                        "trigger": TriggerType.PAGE_VISITED,
                        "trigger_config": {"page": "/dashboard"},
                        "actions": [ActionType.ADD_TAG],
                        "action_configs": [{"tag": "active_user"}]
                    }
                ]
            },
            
            FunnelTemplate.LEAD_GENERATION: {
                "name": "Lead Generation Funnel",
                "description": "Capture and nurture leads with valuable content",
                "stages": [
                    {
                        "name": "Lead Magnet Delivery",
                        "stage_type": FunnelStageType.LEAD_MAGNET,
                        "email_templates": [
                            {
                                "name": "Download Your Free Guide",
                                "subject": "Your free guide is ready for download",
                                "delay_hours": 0
                            }
                        ]
                    },
                    {
                        "name": "Value Nurture Series",
                        "stage_type": FunnelStageType.NURTURE_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "Pro Tip #1",
                                "subject": "The #1 mistake most businesses make",
                                "delay_hours": 24
                            },
                            {
                                "name": "Case Study",
                                "subject": "How we helped {industry} business grow 200%",
                                "delay_hours": 72
                            },
                            {
                                "name": "Advanced Strategy",
                                "subject": "Advanced strategy most competitors don't know",
                                "delay_hours": 120
                            }
                        ]
                    },
                    {
                        "name": "Consultation Offer",
                        "stage_type": FunnelStageType.SALES_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "Free Consultation",
                                "subject": "Ready for a custom growth strategy?",
                                "delay_hours": 168
                            }
                        ]
                    }
                ]
            },
            
            FunnelTemplate.E_COMMERCE: {
                "name": "E-commerce Sales Funnel",
                "description": "Convert browsers to buyers with abandoned cart recovery",
                "stages": [
                    {
                        "name": "Welcome New Subscribers",
                        "stage_type": FunnelStageType.WELCOME_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "Welcome + First Purchase Discount",
                                "subject": "Welcome! Here's 15% off your first order",
                                "delay_hours": 0
                            }
                        ]
                    },
                    {
                        "name": "Product Education",
                        "stage_type": FunnelStageType.NURTURE_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "Best Sellers Showcase",
                                "subject": "Our customers' favorite products this month",
                                "delay_hours": 48
                            },
                            {
                                "name": "How-To Guide",
                                "subject": "Get the most out of your purchase",
                                "delay_hours": 96
                            }
                        ]
                    },
                    {
                        "name": "Cart Abandonment Recovery",
                        "stage_type": FunnelStageType.SALES_SEQUENCE,
                        "email_templates": [
                            {
                                "name": "You Left Something Behind",
                                "subject": "Your cart is waiting for you",
                                "delay_hours": 1
                            },
                            {
                                "name": "Limited Time Offer",
                                "subject": "Don't miss out - 10% off expires soon",
                                "delay_hours": 24
                            },
                            {
                                "name": "Last Chance",
                                "subject": "Last chance to complete your order",
                                "delay_hours": 72
                            }
                        ]
                    }
                ],
                "automation_rules": [
                    {
                        "name": "Cart Abandonment Trigger",
                        "trigger": TriggerType.PAGE_VISITED,
                        "trigger_config": {"page": "/cart", "time_on_page_min": 30},
                        "actions": [ActionType.ADD_TO_SEGMENT],
                        "action_configs": [{"segment": "cart_abandoners"}]
                    }
                ]
            }
        }
        
        return templates
    
    def create_funnel_from_template(self, template: FunnelTemplate, customizations: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Create a new funnel from a template with customizations"""
        
        templates = self.get_funnel_templates()
        base_template = templates.get(template)
        
        if not base_template:
            raise ValueError(f"Template {template} not found")
        
        # Apply customizations
        funnel_config = base_template.copy()
        
        # Apply basic customizations
        if "name" in customizations:
            funnel_config["name"] = customizations["name"]
        
        if "description" in customizations:
            funnel_config["description"] = customizations["description"]
        
        # Customize stages
        if "stage_customizations" in customizations:
            stage_customizations = customizations["stage_customizations"]
            
            for i, stage in enumerate(funnel_config["stages"]):
                if i < len(stage_customizations):
                    stage_custom = stage_customizations[i]
                    stage.update(stage_custom)
        
        # Add funnel metadata
        funnel_config["template_used"] = template
        funnel_config["created_at"] = datetime.utcnow().isoformat()
        funnel_config["created_by"] = self.user_id
        funnel_config["tenant_id"] = self.tenant_id
        
        return funnel_config
    
    def build_custom_funnel(self, funnel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Build a custom funnel from scratch"""
        
        stages = []
        
        for stage_config in funnel_config.get("stages", []):
            stage = FunnelStageConfig(
                name=stage_config["name"],
                stage_type=FunnelStageType(stage_config["stage_type"]),
                description=stage_config.get("description"),
                position=stage_config.get("position", len(stages)),
                email_templates=stage_config.get("email_templates", []),
                delay_before_action=stage_config.get("delay_before_action"),
                entry_conditions=stage_config.get("entry_conditions", []),
                exit_conditions=stage_config.get("exit_conditions", []),
                actions=stage_config.get("actions", []),
                conversion_goals=stage_config.get("conversion_goals", {})
            )
            stages.append(stage.dict())
        
        # Build automation rules
        automation_rules = []
        for rule_config in funnel_config.get("automation_rules", []):
            rule = AutomationRule(
                name=rule_config["name"],
                trigger=TriggerType(rule_config["trigger"]),
                trigger_config=rule_config.get("trigger_config", {}),
                conditions=rule_config.get("conditions", []),
                actions=[ActionType(action) for action in rule_config.get("actions", [])],
                action_configs=rule_config.get("action_configs", []),
                is_active=rule_config.get("is_active", True),
                priority=rule_config.get("priority", 0)
            )
            automation_rules.append(rule.dict())
        
        return {
            "id": str(uuid.uuid4()),
            "name": funnel_config["name"],
            "description": funnel_config.get("description"),
            "funnel_type": funnel_config.get("funnel_type", "custom"),
            "stages": stages,
            "automation_rules": automation_rules,
            "conversion_goals": funnel_config.get("conversion_goals", {}),
            "tenant_id": self.tenant_id,
            "created_by": self.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }
    
    async def sync_funnel_to_mautic(self, funnel_config: Dict[str, Any], mautic_integration_config: Dict[str, Any]) -> Dict[str, Any]:
        """Sync funnel configuration to Mautic"""
        
        try:
            from ..integration.mautic_integration import MauticIntegration, MauticConfig, MauticCampaign, MauticEmail
            
            # Create Mautic configuration
            mautic_config = MauticConfig(**mautic_integration_config)
            
            async with MauticIntegration(mautic_config) as mautic:
                # Authenticate
                auth_result = await mautic.authenticate()
                if not auth_result["success"]:
                    return {"success": False, "error": auth_result["error"]}
                
                # Create main campaign in Mautic
                campaign_events = []
                email_mappings = {}
                
                # Create email templates for each stage
                for stage in funnel_config["stages"]:
                    for email_template in stage.get("email_templates", []):
                        
                        # Create email in Mautic
                        mautic_email = MauticEmail(
                            name=f"{funnel_config['name']} - {email_template['name']}",
                            subject=email_template.get("subject", ""),
                            html_content=email_template.get("html_content", ""),
                            text_content=email_template.get("text_content"),
                            email_type="template",
                            is_published=True
                        )
                        
                        email_result = await mautic.create_email(mautic_email)
                        
                        if email_result["success"]:
                            email_mappings[email_template.get("id", str(uuid.uuid4()))] = email_result["email_id"]
                            
                            # Create campaign event for email
                            campaign_events.append({
                                "name": f"Send {email_template['name']}",
                                "type": "email.send",
                                "eventType": "action",
                                "properties": {
                                    "email": email_result["email_id"],
                                    "email_type": "transactional"
                                },
                                "triggerInterval": email_template.get("delay_hours", 0),
                                "triggerIntervalUnit": "h"
                            })
                
                # Create main campaign
                mautic_campaign = MauticCampaign(
                    name=funnel_config["name"],
                    description=funnel_config.get("description", ""),
                    is_published=True,
                    allow_restart=True,
                    events=campaign_events
                )
                
                campaign_result = await mautic.create_campaign(mautic_campaign)
                
                if campaign_result["success"]:
                    return {
                        "success": True,
                        "mautic_campaign_id": campaign_result["campaign_id"],
                        "email_mappings": email_mappings,
                        "sync_timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    return {"success": False, "error": campaign_result["error"]}
                    
        except Exception as e:
            logger.error(f"Mautic sync error: {e}")
            return {"success": False, "error": str(e)}
    
    def validate_funnel_config(self, funnel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate funnel configuration"""
        
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ["name", "stages"]
        for field in required_fields:
            if field not in funnel_config:
                errors.append(f"Missing required field: {field}")
        
        # Validate stages
        if "stages" in funnel_config:
            stages = funnel_config["stages"]
            
            if not stages:
                errors.append("Funnel must have at least one stage")
            
            # Check stage positions
            positions = [stage.get("position", 0) for stage in stages]
            if len(set(positions)) != len(positions):
                warnings.append("Duplicate stage positions detected")
            
            # Validate email templates
            for i, stage in enumerate(stages):
                email_templates = stage.get("email_templates", [])
                for j, template in enumerate(email_templates):
                    if not template.get("subject"):
                        errors.append(f"Stage {i}, Email {j}: Missing subject line")
                    
                    if not template.get("html_content"):
                        warnings.append(f"Stage {i}, Email {j}: No HTML content provided")
        
        # Validate automation rules
        if "automation_rules" in funnel_config:
            for i, rule in enumerate(funnel_config["automation_rules"]):
                if not rule.get("name"):
                    errors.append(f"Automation rule {i}: Missing name")
                
                if not rule.get("trigger"):
                    errors.append(f"Automation rule {i}: Missing trigger")
                
                if not rule.get("actions"):
                    warnings.append(f"Automation rule {i}: No actions defined")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validation_timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_funnel_analytics(self, funnel_id: str, performance_data: Dict[str, Any]) -> FunnelAnalytics:
        """Generate funnel performance analytics"""
        
        # Calculate basic metrics
        total_entries = performance_data.get("total_entries", 0)
        total_completions = performance_data.get("total_completions", 0)
        completion_rate = (total_completions / total_entries * 100) if total_entries > 0 else 0
        
        # Calculate stage conversion rates
        stage_conversion_rates = {}
        stage_data = performance_data.get("stage_data", [])
        
        for i, stage in enumerate(stage_data):
            if i == 0:
                # First stage conversion rate
                stage_conversion_rates[stage["stage_id"]] = 100.0
            else:
                prev_stage_entries = stage_data[i-1].get("completions", 1)
                current_stage_entries = stage.get("entries", 0)
                conversion_rate = (current_stage_entries / prev_stage_entries * 100) if prev_stage_entries > 0 else 0
                stage_conversion_rates[stage["stage_id"]] = round(conversion_rate, 2)
        
        # Calculate revenue metrics
        revenue_generated = performance_data.get("revenue_generated", 0.0)
        cost_per_conversion = None
        
        if total_completions > 0 and "total_cost" in performance_data:
            cost_per_conversion = performance_data["total_cost"] / total_completions
        
        return FunnelAnalytics(
            total_entries=total_entries,
            total_completions=total_completions,
            completion_rate=round(completion_rate, 2),
            average_time_to_complete=performance_data.get("average_completion_time"),
            stage_conversion_rates=stage_conversion_rates,
            revenue_generated=revenue_generated,
            cost_per_conversion=cost_per_conversion
        )
    
    def optimize_funnel_performance(self, funnel_analytics: FunnelAnalytics, funnel_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimization recommendations based on analytics"""
        
        recommendations = []
        
        # Low completion rate optimization
        if funnel_analytics.completion_rate < 10:
            recommendations.append({
                "type": "completion_rate",
                "priority": "high",
                "issue": f"Low completion rate ({funnel_analytics.completion_rate}%)",
                "recommendation": "Consider reducing the number of stages or improving email content quality",
                "expected_improvement": "15-30% increase in completions"
            })
        
        # Stage-specific optimizations
        for stage_id, conversion_rate in funnel_analytics.stage_conversion_rates.items():
            if conversion_rate < 50:
                recommendations.append({
                    "type": "stage_optimization",
                    "priority": "medium",
                    "stage_id": stage_id,
                    "issue": f"Low stage conversion rate ({conversion_rate}%)",
                    "recommendation": "Review email content, timing, and audience targeting for this stage",
                    "expected_improvement": "10-25% improvement in stage conversion"
                })
        
        # Cost optimization
        if funnel_analytics.cost_per_conversion and funnel_analytics.cost_per_conversion > 50:
            recommendations.append({
                "type": "cost_optimization",
                "priority": "medium",
                "issue": f"High cost per conversion (${funnel_analytics.cost_per_conversion:.2f})",
                "recommendation": "Optimize targeting and reduce funnel length to improve efficiency",
                "expected_improvement": "20-40% reduction in acquisition costs"
            })
        
        # Revenue optimization
        if funnel_analytics.revenue_generated > 0:
            revenue_per_completion = funnel_analytics.revenue_generated / funnel_analytics.total_completions if funnel_analytics.total_completions > 0 else 0
            
            if revenue_per_completion < 100:
                recommendations.append({
                    "type": "revenue_optimization",
                    "priority": "high",
                    "issue": f"Low revenue per conversion (${revenue_per_completion:.2f})",
                    "recommendation": "Add upsell sequences or increase price points",
                    "expected_improvement": "25-50% increase in revenue per customer"
                })
        
        return {
            "recommendations": recommendations,
            "optimization_score": self._calculate_optimization_score(funnel_analytics),
            "next_review_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
    
    def _calculate_optimization_score(self, analytics: FunnelAnalytics) -> float:
        """Calculate overall funnel optimization score (0-100)"""
        
        score = 0
        
        # Completion rate score (40% weight)
        if analytics.completion_rate >= 20:
            score += 40
        elif analytics.completion_rate >= 15:
            score += 30
        elif analytics.completion_rate >= 10:
            score += 20
        elif analytics.completion_rate >= 5:
            score += 10
        
        # Stage conversion rates score (30% weight)
        if analytics.stage_conversion_rates:
            avg_conversion = sum(analytics.stage_conversion_rates.values()) / len(analytics.stage_conversion_rates)
            if avg_conversion >= 70:
                score += 30
            elif avg_conversion >= 50:
                score += 20
            elif avg_conversion >= 30:
                score += 15
            else:
                score += 5
        
        # Revenue efficiency score (20% weight)
        if analytics.cost_per_conversion:
            if analytics.cost_per_conversion <= 25:
                score += 20
            elif analytics.cost_per_conversion <= 50:
                score += 15
            elif analytics.cost_per_conversion <= 100:
                score += 10
            else:
                score += 5
        else:
            score += 10  # No cost data available
        
        # Completion time score (10% weight)
        if analytics.average_time_to_complete:
            # Optimal completion time is 7-14 days
            if 7 <= analytics.average_time_to_complete <= 14:
                score += 10
            elif 3 <= analytics.average_time_to_complete <= 21:
                score += 7
            else:
                score += 3
        else:
            score += 5  # No time data available
        
        return min(score, 100)  # Cap at 100