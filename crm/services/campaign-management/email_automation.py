"""
Email Automation Workflows - BizoholicSaaS
Advanced email automation with behavioral triggers and multi-tenant isolation
"""

import uuid
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import logging
import json
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class EmailTriggerType(str, Enum):
    """Types of email automation triggers"""
    TIME_DELAY = "time_delay"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    LINK_CLICKED = "link_clicked"
    FORM_SUBMITTED = "form_submitted"
    PAGE_VISITED = "page_visited"
    PURCHASE_MADE = "purchase_made"
    CART_ABANDONED = "cart_abandoned"
    LOGIN_ACTIVITY = "login_activity"
    SUBSCRIPTION_CHANGED = "subscription_changed"
    LEAD_SCORE_REACHED = "lead_score_reached"
    TAG_ADDED = "tag_added"
    SEGMENT_JOINED = "segment_joined"
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"

class EmailActionType(str, Enum):
    """Types of email automation actions"""
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    ADD_TO_LIST = "add_to_list"
    REMOVE_FROM_LIST = "remove_from_list"
    UPDATE_CONTACT_FIELD = "update_contact_field"
    ADD_LEAD_SCORE = "add_lead_score"
    SUBTRACT_LEAD_SCORE = "subtract_lead_score"
    MOVE_TO_SEGMENT = "move_to_segment"
    CREATE_TASK = "create_task"
    SEND_WEBHOOK = "send_webhook"
    PAUSE_AUTOMATION = "pause_automation"
    RESTART_AUTOMATION = "restart_automation"

class AutomationStatus(str, Enum):
    """Automation workflow status"""
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"
    DRAFT = "draft"
    ERROR = "error"

class ContactStatus(str, Enum):
    """Contact status in automation"""
    ENTERED = "entered"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXITED = "exited"
    ERROR = "error"

# Pydantic Models
class EmailTrigger(BaseModel):
    """Email automation trigger configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: EmailTriggerType
    conditions: Dict[str, Any] = {}
    delay_minutes: int = 0
    delay_unit: str = "minutes"  # minutes, hours, days
    is_active: bool = True

class EmailAction(BaseModel):
    """Email automation action configuration"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: EmailActionType
    config: Dict[str, Any] = {}
    delay_after_trigger: int = 0
    success_conditions: Dict[str, Any] = {}
    failure_conditions: Dict[str, Any] = {}

class EmailTemplate(BaseModel):
    """Email template with dynamic content"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    html_content: str
    text_content: Optional[str] = None
    personalization_fields: List[str] = []
    dynamic_content: List[Dict[str, Any]] = []
    tracking_enabled: bool = True
    open_tracking: bool = True
    click_tracking: bool = True

class AutomationWorkflow(BaseModel):
    """Complete email automation workflow"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    tenant_id: str
    funnel_id: Optional[str] = None
    trigger: EmailTrigger
    actions: List[EmailAction]
    entry_conditions: List[Dict[str, Any]] = []
    exit_conditions: List[Dict[str, Any]] = []
    status: AutomationStatus = AutomationStatus.DRAFT
    is_multi_step: bool = False
    max_executions_per_contact: int = 1
    cooldown_period_days: int = 30
    priority: int = 0
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContactAutomationExecution(BaseModel):
    """Track contact's progress through automation"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    contact_id: str
    tenant_id: str
    current_step: int = 0
    status: ContactStatus = ContactStatus.ENTERED
    data: Dict[str, Any] = {}
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    next_action_at: Optional[datetime] = None
    execution_count: int = 1
    error_message: Optional[str] = None

class BehavioralTriggerConfig(BaseModel):
    """Configuration for behavioral triggers"""
    trigger_name: str
    conditions: List[Dict[str, Any]]
    time_window: int = 24  # hours
    min_occurrences: int = 1
    max_occurrences: Optional[int] = None
    reset_period: Optional[int] = None  # days

@dataclass
class EmailMetrics:
    """Email performance metrics"""
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    bounced: int = 0
    unsubscribed: int = 0
    complained: int = 0
    conversion: int = 0

class EmailAutomationEngine:
    """Advanced Email Automation Engine with Behavioral Triggers"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.active_workflows: Dict[str, AutomationWorkflow] = {}
        self.contact_executions: Dict[str, List[ContactAutomationExecution]] = {}
    
    def create_behavioral_trigger_workflow(self, config: Dict[str, Any]) -> AutomationWorkflow:
        """Create a sophisticated behavioral trigger workflow"""
        
        # Parse trigger configuration
        trigger_config = BehavioralTriggerConfig(**config["trigger"])
        
        # Create trigger
        trigger = EmailTrigger(
            type=EmailTriggerType(config["trigger"]["type"]),
            conditions=config["trigger"]["conditions"],
            delay_minutes=config["trigger"].get("delay_minutes", 0)
        )
        
        # Create actions
        actions = []
        for action_config in config["actions"]:
            action = EmailAction(
                type=EmailActionType(action_config["type"]),
                config=action_config["config"],
                delay_after_trigger=action_config.get("delay_after_trigger", 0)
            )
            actions.append(action)
        
        # Create workflow
        workflow = AutomationWorkflow(
            name=config["name"],
            description=config.get("description"),
            tenant_id=self.tenant_id,
            funnel_id=config.get("funnel_id"),
            trigger=trigger,
            actions=actions,
            entry_conditions=config.get("entry_conditions", []),
            exit_conditions=config.get("exit_conditions", []),
            is_multi_step=config.get("is_multi_step", False),
            max_executions_per_contact=config.get("max_executions_per_contact", 1),
            cooldown_period_days=config.get("cooldown_period_days", 30),
            priority=config.get("priority", 0),
            tags=config.get("tags", [])
        )
        
        return workflow
    
    def create_drip_campaign_workflow(self, config: Dict[str, Any]) -> AutomationWorkflow:
        """Create a time-based drip email campaign"""
        
        # Create time-delay trigger
        trigger = EmailTrigger(
            type=EmailTriggerType.TIME_DELAY,
            conditions={"start_immediately": True},
            delay_minutes=config.get("initial_delay_minutes", 0)
        )
        
        # Create sequence of email actions with delays
        actions = []
        for i, email_config in enumerate(config["emails"]):
            action = EmailAction(
                type=EmailActionType.SEND_EMAIL,
                config={
                    "email_template_id": email_config["template_id"],
                    "subject": email_config["subject"],
                    "personalize": email_config.get("personalize", True),
                    "tracking": email_config.get("tracking", True)
                },
                delay_after_trigger=email_config.get("delay_hours", 0) * 60  # Convert to minutes
            )
            actions.append(action)
        
        workflow = AutomationWorkflow(
            name=config["name"],
            description=config.get("description", "Automated drip email campaign"),
            tenant_id=self.tenant_id,
            funnel_id=config.get("funnel_id"),
            trigger=trigger,
            actions=actions,
            is_multi_step=True,
            max_executions_per_contact=1,
            tags=["drip_campaign"]
        )
        
        return workflow
    
    def create_abandoned_cart_workflow(self, config: Dict[str, Any]) -> AutomationWorkflow:
        """Create abandoned cart recovery workflow"""
        
        trigger = EmailTrigger(
            type=EmailTriggerType.CART_ABANDONED,
            conditions={
                "cart_value_min": config.get("min_cart_value", 0),
                "cart_items_min": config.get("min_cart_items", 1),
                "time_since_abandonment_hours": config.get("trigger_delay_hours", 1)
            },
            delay_minutes=config.get("trigger_delay_hours", 1) * 60
        )
        
        actions = []
        
        # First reminder email
        actions.append(EmailAction(
            type=EmailActionType.SEND_EMAIL,
            config={
                "email_template_id": config["templates"]["first_reminder"],
                "subject": "You left something in your cart!",
                "include_cart_items": True,
                "discount_code": config.get("discount_code")
            },
            delay_after_trigger=0
        ))
        
        # Second reminder with urgency
        if len(config["templates"]) > 1:
            actions.append(EmailAction(
                type=EmailActionType.SEND_EMAIL,
                config={
                    "email_template_id": config["templates"]["second_reminder"],
                    "subject": "Don't miss out - complete your order",
                    "include_cart_items": True,
                    "add_urgency": True,
                    "discount_code": config.get("discount_code")
                },
                delay_after_trigger=24 * 60  # 24 hours later
            ))
        
        # Final reminder with special offer
        if len(config["templates"]) > 2:
            actions.append(EmailAction(
                type=EmailActionType.SEND_EMAIL,
                config={
                    "email_template_id": config["templates"]["final_reminder"],
                    "subject": "Last chance - your cart expires soon",\n                    \"include_cart_items\": True,\n                    \"special_offer\": True,\n                    \"discount_code\": config.get(\"final_discount_code\")\n                },\n                delay_after_trigger=72 * 60  # 72 hours later\n            ))\n        \n        workflow = AutomationWorkflow(\n            name=\"Abandoned Cart Recovery\",\n            description=\"Recover abandoned carts with timed email sequence\",\n            tenant_id=self.tenant_id,\n            trigger=trigger,\n            actions=actions,\n            is_multi_step=True,\n            max_executions_per_contact=3,  # Allow multiple cart abandonment recoveries\n            cooldown_period_days=7,\n            tags=[\"e-commerce\", \"cart_recovery\"]\n        )\n        \n        return workflow\n    \n    def create_welcome_series_workflow(self, config: Dict[str, Any]) -> AutomationWorkflow:\n        \"\"\"Create welcome email series for new subscribers\"\"\"\n        \n        trigger = EmailTrigger(\n            type=EmailTriggerType.FORM_SUBMITTED,\n            conditions={\n                \"form_id\": config.get(\"signup_form_id\"),\n                \"list_id\": config.get(\"list_id\"),\n                \"immediate_trigger\": True\n            },\n            delay_minutes=0\n        )\n        \n        actions = []\n        \n        # Welcome email (immediate)\n        actions.append(EmailAction(\n            type=EmailActionType.SEND_EMAIL,\n            config={\n                \"email_template_id\": config[\"templates\"][\"welcome\"],\n                \"subject\": config.get(\"welcome_subject\", \"Welcome to our community!\"),\n                \"personalize\": True,\n                \"send_immediately\": True\n            },\n            delay_after_trigger=0\n        ))\n        \n        # Add welcome tag\n        actions.append(EmailAction(\n            type=EmailActionType.ADD_TAG,\n            config={\"tag\": \"new_subscriber\"},\n            delay_after_trigger=0\n        ))\n        \n        # Follow-up emails\n        if \"follow_up_templates\" in config:\n            for i, template_config in enumerate(config[\"follow_up_templates\"]):\n                delay_days = template_config.get(\"delay_days\", i + 1)\n                actions.append(EmailAction(\n                    type=EmailActionType.SEND_EMAIL,\n                    config={\n                        \"email_template_id\": template_config[\"template_id\"],\n                        \"subject\": template_config[\"subject\"],\n                        \"personalize\": True\n                    },\n                    delay_after_trigger=delay_days * 24 * 60  # Convert days to minutes\n                ))\n        \n        workflow = AutomationWorkflow(\n            name=\"Welcome Email Series\",\n            description=\"Onboard new subscribers with welcome email sequence\",\n            tenant_id=self.tenant_id,\n            trigger=trigger,\n            actions=actions,\n            is_multi_step=True,\n            max_executions_per_contact=1,\n            tags=[\"welcome\", \"onboarding\"]\n        )\n        \n        return workflow\n    \n    def create_re_engagement_workflow(self, config: Dict[str, Any]) -> AutomationWorkflow:\n        \"\"\"Create re-engagement campaign for inactive contacts\"\"\"\n        \n        trigger = EmailTrigger(\n            type=EmailTriggerType.LOGIN_ACTIVITY,\n            conditions={\n                \"days_since_last_activity\": config.get(\"inactivity_days\", 30),\n                \"exclude_tags\": [\"unsubscribed\", \"bounced\"],\n                \"min_engagement_score\": config.get(\"min_engagement_score\", 10)\n            },\n            delay_minutes=0\n        )\n        \n        actions = []\n        \n        # First re-engagement email\n        actions.append(EmailAction(\n            type=EmailActionType.SEND_EMAIL,\n            config={\n                \"email_template_id\": config[\"templates\"][\"first_attempt\"],\n                \"subject\": \"We miss you! Here's what you've been missing\",\n                \"include_recent_content\": True,\n                \"special_offer\": config.get(\"include_offer\", False)\n            },\n            delay_after_trigger=0\n        ))\n        \n        # Tag as re-engagement candidate\n        actions.append(EmailAction(\n            type=EmailActionType.ADD_TAG,\n            config={\"tag\": \"re_engagement_campaign\"},\n            delay_after_trigger=0\n        ))\n        \n        # Second attempt if no response\n        if \"second_attempt_template\" in config[\"templates\"]:\n            actions.append(EmailAction(\n                type=EmailActionType.SEND_EMAIL,\n                config={\n                    \"email_template_id\": config[\"templates\"][\"second_attempt\"],\n                    \"subject\": \"One more try - we have something special for you\",\n                    \"conditions\": {\n                        \"no_email_opens\": {\"days\": 7},\n                        \"no_website_visits\": {\"days\": 7}\n                    }\n                },\n                delay_after_trigger=7 * 24 * 60  # 7 days\n            ))\n        \n        # Final attempt - win-back offer\n        if \"final_attempt_template\" in config[\"templates\"]:\n            actions.append(EmailAction(\n                type=EmailActionType.SEND_EMAIL,\n                config={\n                    \"email_template_id\": config[\"templates\"][\"final_attempt\"],\n                    \"subject\": \"Last chance - here's our best offer\",\n                    \"win_back_offer\": True,\n                    \"discount_percentage\": config.get(\"win_back_discount\", 25)\n                },\n                delay_after_trigger=14 * 24 * 60  # 14 days\n            ))\n        \n        workflow = AutomationWorkflow(\n            name=\"Re-engagement Campaign\",\n            description=\"Re-engage inactive contacts with targeted email sequence\",\n            tenant_id=self.tenant_id,\n            trigger=trigger,\n            actions=actions,\n            is_multi_step=True,\n            max_executions_per_contact=2,  # Allow retry after 6 months\n            cooldown_period_days=180,\n            tags=[\"re_engagement\", \"retention\"]\n        )\n        \n        return workflow\n    \n    def create_lead_scoring_workflow(self, config: Dict[str, Any]) -> AutomationWorkflow:\n        \"\"\"Create lead scoring automation workflow\"\"\"\n        \n        trigger = EmailTrigger(\n            type=EmailTriggerType.LEAD_SCORE_REACHED,\n            conditions={\n                \"score_threshold\": config.get(\"score_threshold\", 100),\n                \"score_change\": config.get(\"score_change\", \"increased\"),\n                \"time_period\": config.get(\"time_period\", \"24_hours\")\n            },\n            delay_minutes=0\n        )\n        \n        actions = []\n        \n        # Notify sales team for high-scoring leads\n        if config.get(\"notify_sales\", True):\n            actions.append(EmailAction(\n                type=EmailActionType.CREATE_TASK,\n                config={\n                    \"task_type\": \"sales_follow_up\",\n                    \"assign_to\": config.get(\"sales_team_id\"),\n                    \"priority\": \"high\",\n                    \"due_date\": \"24_hours\"\n                },\n                delay_after_trigger=0\n            ))\n        \n        # Send personalized content to high-scoring leads\n        actions.append(EmailAction(\n            type=EmailActionType.SEND_EMAIL,\n            config={\n                \"email_template_id\": config[\"templates\"][\"high_score_nurture\"],\n                \"subject\": \"Exclusive insights for our most engaged subscribers\",\n                \"personalize\": True,\n                \"premium_content\": True\n            },\n            delay_after_trigger=30  # 30 minutes delay\n        ))\n        \n        # Add to high-value segment\n        actions.append(EmailAction(\n            type=EmailActionType.MOVE_TO_SEGMENT,\n            config={\"segment_id\": config.get(\"high_value_segment_id\")},\n            delay_after_trigger=0\n        ))\n        \n        workflow = AutomationWorkflow(\n            name=\"Lead Scoring Automation\",\n            description=\"Automated actions for high-scoring leads\",\n            tenant_id=self.tenant_id,\n            trigger=trigger,\n            actions=actions,\n            max_executions_per_contact=999,  # Allow multiple executions as score changes\n            cooldown_period_days=1,  # Short cooldown\n            priority=1,  # High priority\n            tags=[\"lead_scoring\", \"sales_qualified\"]\n        )\n        \n        return workflow\n    \n    async def execute_workflow(self, workflow: AutomationWorkflow, contact_id: str, trigger_data: Dict[str, Any] = {}) -> ContactAutomationExecution:\n        \"\"\"Execute an automation workflow for a specific contact\"\"\"\n        \n        try:\n            # Check if contact is eligible for this workflow\n            if not await self._is_contact_eligible(contact_id, workflow):\n                logger.info(f\"Contact {contact_id} not eligible for workflow {workflow.id}\")\n                return None\n            \n            # Create execution record\n            execution = ContactAutomationExecution(\n                workflow_id=workflow.id,\n                contact_id=contact_id,\n                tenant_id=self.tenant_id,\n                data=trigger_data\n            )\n            \n            # Execute actions in sequence\n            for i, action in enumerate(workflow.actions):\n                try:\n                    # Calculate delay\n                    delay_minutes = action.delay_after_trigger\n                    if delay_minutes > 0:\n                        execution.next_action_at = datetime.utcnow() + timedelta(minutes=delay_minutes)\n                        execution.status = ContactStatus.IN_PROGRESS\n                        # In real implementation, this would be scheduled\n                        await asyncio.sleep(1)  # Simulate delay\n                    \n                    # Execute action\n                    action_result = await self._execute_action(action, contact_id, trigger_data)\n                    \n                    if action_result[\"success\"]:\n                        execution.current_step = i + 1\n                        execution.data[f\"action_{i}_result\"] = action_result\n                    else:\n                        execution.status = ContactStatus.ERROR\n                        execution.error_message = action_result.get(\"error\")\n                        break\n                        \n                except Exception as action_error:\n                    logger.error(f\"Action execution error: {action_error}\")\n                    execution.status = ContactStatus.ERROR\n                    execution.error_message = str(action_error)\n                    break\n            \n            # Mark as completed if all actions succeeded\n            if execution.current_step == len(workflow.actions):\n                execution.status = ContactStatus.COMPLETED\n                execution.completed_at = datetime.utcnow()\n            \n            # Store execution record\n            if contact_id not in self.contact_executions:\n                self.contact_executions[contact_id] = []\n            self.contact_executions[contact_id].append(execution)\n            \n            return execution\n            \n        except Exception as e:\n            logger.error(f\"Workflow execution error: {e}\")\n            return ContactAutomationExecution(\n                workflow_id=workflow.id,\n                contact_id=contact_id,\n                tenant_id=self.tenant_id,\n                status=ContactStatus.ERROR,\n                error_message=str(e)\n            )\n    \n    async def _is_contact_eligible(self, contact_id: str, workflow: AutomationWorkflow) -> bool:\n        \"\"\"Check if contact is eligible for workflow execution\"\"\"\n        \n        # Check execution count limit\n        contact_executions = self.contact_executions.get(contact_id, [])\n        workflow_executions = [exec for exec in contact_executions if exec.workflow_id == workflow.id]\n        \n        if len(workflow_executions) >= workflow.max_executions_per_contact:\n            # Check cooldown period\n            last_execution = max(workflow_executions, key=lambda x: x.started_at)\n            cooldown_end = last_execution.started_at + timedelta(days=workflow.cooldown_period_days)\n            \n            if datetime.utcnow() < cooldown_end:\n                return False\n        \n        # Check entry conditions\n        for condition in workflow.entry_conditions:\n            if not await self._evaluate_condition(contact_id, condition):\n                return False\n        \n        return True\n    \n    async def _execute_action(self, action: EmailAction, contact_id: str, data: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Execute a single automation action\"\"\"\n        \n        try:\n            if action.type == EmailActionType.SEND_EMAIL:\n                return await self._send_email(action.config, contact_id, data)\n            elif action.type == EmailActionType.ADD_TAG:\n                return await self._add_tag(action.config, contact_id)\n            elif action.type == EmailActionType.ADD_LEAD_SCORE:\n                return await self._add_lead_score(action.config, contact_id)\n            elif action.type == EmailActionType.MOVE_TO_SEGMENT:\n                return await self._move_to_segment(action.config, contact_id)\n            else:\n                # Simulate other actions\n                await asyncio.sleep(0.1)\n                return {\n                    \"success\": True,\n                    \"action_type\": action.type,\n                    \"message\": f\"Action {action.type} executed successfully\"\n                }\n                \n        except Exception as e:\n            return {\n                \"success\": False,\n                \"error\": str(e),\n                \"action_type\": action.type\n            }\n    \n    async def _send_email(self, config: Dict[str, Any], contact_id: str, data: Dict[str, Any]) -> Dict[str, Any]:\n        \"\"\"Send email action implementation\"\"\"\n        \n        # In real implementation, this would integrate with Mautic API\n        await asyncio.sleep(0.5)  # Simulate API call\n        \n        return {\n            \"success\": True,\n            \"email_sent\": True,\n            \"template_id\": config.get(\"email_template_id\"),\n            \"contact_id\": contact_id,\n            \"subject\": config.get(\"subject\"),\n            \"sent_at\": datetime.utcnow().isoformat()\n        }\n    \n    async def _add_tag(self, config: Dict[str, Any], contact_id: str) -> Dict[str, Any]:\n        \"\"\"Add tag action implementation\"\"\"\n        \n        await asyncio.sleep(0.1)\n        \n        return {\n            \"success\": True,\n            \"tag_added\": config.get(\"tag\"),\n            \"contact_id\": contact_id\n        }\n    \n    async def _add_lead_score(self, config: Dict[str, Any], contact_id: str) -> Dict[str, Any]:\n        \"\"\"Add lead score action implementation\"\"\"\n        \n        await asyncio.sleep(0.1)\n        \n        return {\n            \"success\": True,\n            \"points_added\": config.get(\"points\", 10),\n            \"contact_id\": contact_id\n        }\n    \n    async def _move_to_segment(self, config: Dict[str, Any], contact_id: str) -> Dict[str, Any]:\n        \"\"\"Move to segment action implementation\"\"\"\n        \n        await asyncio.sleep(0.1)\n        \n        return {\n            \"success\": True,\n            \"moved_to_segment\": config.get(\"segment_id\"),\n            \"contact_id\": contact_id\n        }\n    \n    async def _evaluate_condition(self, contact_id: str, condition: Dict[str, Any]) -> bool:\n        \"\"\"Evaluate a workflow condition\"\"\"\n        \n        # In real implementation, this would check contact data against condition\n        # For now, always return True\n        return True\n    \n    def get_workflow_metrics(self, workflow_id: str) -> Dict[str, Any]:\n        \"\"\"Get performance metrics for a workflow\"\"\"\n        \n        # Get all executions for this workflow\n        all_executions = []\n        for contact_executions in self.contact_executions.values():\n            workflow_executions = [exec for exec in contact_executions if exec.workflow_id == workflow_id]\n            all_executions.extend(workflow_executions)\n        \n        if not all_executions:\n            return {\"total_executions\": 0}\n        \n        # Calculate metrics\n        total = len(all_executions)\n        completed = len([exec for exec in all_executions if exec.status == ContactStatus.COMPLETED])\n        in_progress = len([exec for exec in all_executions if exec.status == ContactStatus.IN_PROGRESS])\n        errors = len([exec for exec in all_executions if exec.status == ContactStatus.ERROR])\n        \n        completion_rate = (completed / total * 100) if total > 0 else 0\n        \n        # Average completion time for completed executions\n        completed_executions = [exec for exec in all_executions if exec.completed_at]\n        avg_completion_time = None\n        \n        if completed_executions:\n            total_time = sum([\n                (exec.completed_at - exec.started_at).total_seconds() / 3600  # Convert to hours\n                for exec in completed_executions\n            ])\n            avg_completion_time = total_time / len(completed_executions)\n        \n        return {\n            \"workflow_id\": workflow_id,\n            \"total_executions\": total,\n            \"completed\": completed,\n            \"in_progress\": in_progress,\n            \"errors\": errors,\n            \"completion_rate\": round(completion_rate, 2),\n            \"average_completion_time_hours\": round(avg_completion_time, 2) if avg_completion_time else None,\n            \"last_execution\": max(all_executions, key=lambda x: x.started_at).started_at.isoformat() if all_executions else None\n        }\n    \n    def get_contact_journey(self, contact_id: str) -> List[Dict[str, Any]]:\n        \"\"\"Get complete automation journey for a contact\"\"\"\n        \n        contact_executions = self.contact_executions.get(contact_id, [])\n        \n        journey = []\n        for execution in sorted(contact_executions, key=lambda x: x.started_at):\n            journey.append({\n                \"workflow_id\": execution.workflow_id,\n                \"status\": execution.status,\n                \"started_at\": execution.started_at.isoformat(),\n                \"completed_at\": execution.completed_at.isoformat() if execution.completed_at else None,\n                \"current_step\": execution.current_step,\n                \"data\": execution.data,\n                \"error\": execution.error_message\n            })\n        \n        return journey