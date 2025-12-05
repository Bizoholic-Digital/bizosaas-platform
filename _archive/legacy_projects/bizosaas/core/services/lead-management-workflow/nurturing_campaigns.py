"""
Multi-Stage Nurturing Campaigns for BizOSaaS Platform
Automated nurturing with personalized content delivery and follow-up scheduling
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import aioredis
import asyncpg
from pydantic import BaseModel, Field
import httpx
from crewai import Agent, Task, Crew, Process
from langchain.tools import BaseTool
from langchain.llms import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignType(Enum):
    WELCOME_SERIES = "welcome_series"
    EDUCATIONAL = "educational"
    PRODUCT_DEMO = "product_demo"
    CASE_STUDY = "case_study"
    TRIAL_NURTURE = "trial_nurture"
    RE_ENGAGEMENT = "re_engagement"
    UPSELL = "upsell"
    WINBACK = "winback"

class CampaignStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"

class DeliveryChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    SOCIAL_MEDIA = "social_media"
    PHONE_CALL = "phone_call"
    DIRECT_MAIL = "direct_mail"
    RETARGETING_AD = "retargeting_ad"

class TriggerType(Enum):
    TIME_BASED = "time_based"
    BEHAVIOR_BASED = "behavior_based"
    SCORE_BASED = "score_based"
    LIFECYCLE_STAGE = "lifecycle_stage"
    MANUAL = "manual"

@dataclass
class CampaignStep:
    """Individual step in a nurturing campaign"""
    step_id: str
    campaign_id: str
    step_number: int
    name: str
    description: str
    
    # Content and delivery
    content_type: str  # email_template, sms_template, content_piece, task
    content_id: str
    delivery_channel: DeliveryChannel
    
    # Timing and triggers
    delay_hours: int = 0
    delay_days: int = 0
    trigger_type: TriggerType = TriggerType.TIME_BASED
    trigger_conditions: Dict[str, Any] = field(default_factory=dict)
    
    # Personalization
    personalization_rules: Dict[str, Any] = field(default_factory=dict)
    dynamic_content: bool = False
    
    # Goals and tracking
    primary_goal: str = ""
    success_metrics: List[str] = field(default_factory=list)
    
    # Conditional logic
    completion_criteria: Dict[str, Any] = field(default_factory=dict)
    next_step_rules: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    active: bool = True

@dataclass
class NurturingCampaign:
    """Multi-stage nurturing campaign definition"""
    campaign_id: str
    name: str
    description: str
    campaign_type: CampaignType
    
    # Targeting and segmentation
    target_segments: List[str] = field(default_factory=list)
    entry_criteria: Dict[str, Any] = field(default_factory=dict)
    exit_criteria: Dict[str, Any] = field(default_factory=dict)
    
    # Campaign flow
    steps: List[CampaignStep] = field(default_factory=list)
    total_steps: int = 0
    estimated_duration_days: int = 0
    
    # Performance and optimization
    conversion_goals: List[str] = field(default_factory=list)
    success_metrics: Dict[str, str] = field(default_factory=dict)
    a_b_testing: bool = False
    
    # Management
    status: CampaignStatus = CampaignStatus.ACTIVE
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Statistics
    total_enrolled: int = 0
    active_participants: int = 0
    completed_participants: int = 0
    conversion_rate: float = 0.0

@dataclass
class CampaignEnrollment:
    """Lead enrollment in a nurturing campaign"""
    enrollment_id: str
    lead_id: str
    campaign_id: str
    
    # Progress tracking
    current_step: int = 0
    completed_steps: List[int] = field(default_factory=list)
    next_action_date: Optional[datetime] = None
    
    # Status and history
    status: str = "active"  # active, paused, completed, opted_out
    enrolled_at: datetime = field(default_factory=datetime.utcnow)
    last_interaction: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    
    # Personalization data
    personalization_data: Dict[str, Any] = field(default_factory=dict)
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Performance tracking
    engagement_score: float = 0.0
    conversion_achieved: bool = False
    conversion_date: Optional[datetime] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

class ContentPersonalizationEngine:
    """AI-powered content personalization for nurturing campaigns"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(openai_api_key=openai_api_key, temperature=0.3)
        self.personalization_agent = self._create_personalization_agent()
        
    def _create_personalization_agent(self) -> Agent:
        """Create AI agent for content personalization"""
        return Agent(
            role='Content Personalization Specialist',
            goal='Personalize campaign content based on lead characteristics and behavior',
            backstory="""You are an expert in marketing personalization who creates 
            highly targeted and relevant content for different audience segments. You 
            understand how to adapt messaging, tone, and examples based on industry, 
            company size, role, and engagement patterns.""",
            verbose=True,
            tools=[self._create_personalization_tool()],
            llm=self.llm,
            memory=True
        )
    
    def _create_personalization_tool(self) -> BaseTool:
        """Create tool for content personalization"""
        class PersonalizationTool(BaseTool):
            name = "personalize_content"
            description = "Personalize content based on lead data and behavior"
            
            def _run(self, content_template: str, lead_data: str, campaign_context: str) -> str:
                try:
                    lead_info = json.loads(lead_data)
                    context = json.loads(campaign_context)
                    
                    # Extract personalization variables
                    company_name = lead_info.get("company_name", "your company")
                    industry = lead_info.get("industry", "")
                    company_size = lead_info.get("company_size", 0)
                    job_title = lead_info.get("job_title", "")
                    pain_points = lead_info.get("pain_points", [])
                    
                    # Personalize content
                    personalized_content = content_template.replace("{company_name}", company_name)
                    
                    # Industry-specific examples
                    if industry:
                        industry_examples = self._get_industry_examples(industry)
                        personalized_content = personalized_content.replace(
                            "{industry_example}", industry_examples
                        )
                    
                    # Company size appropriate messaging
                    if company_size > 500:
                        size_messaging = "enterprise-level solutions"
                    elif company_size > 50:
                        size_messaging = "mid-market solutions"
                    else:
                        size_messaging = "small business solutions"
                    
                    personalized_content = personalized_content.replace(
                        "{size_messaging}", size_messaging
                    )
                    
                    # Role-specific value propositions
                    if "ceo" in job_title.lower() or "founder" in job_title.lower():
                        role_focus = "strategic growth and competitive advantage"
                    elif "marketing" in job_title.lower():
                        role_focus = "marketing efficiency and ROI"
                    elif "sales" in job_title.lower():
                        role_focus = "sales productivity and pipeline growth"
                    else:
                        role_focus = "operational efficiency"
                    
                    personalized_content = personalized_content.replace(
                        "{role_focus}", role_focus
                    )
                    
                    return personalized_content
                    
                except Exception as e:
                    return f"Personalization error: {str(e)}"
            
            def _get_industry_examples(self, industry: str) -> str:
                """Get industry-specific examples"""
                examples = {
                    "technology": "streamline your software development lifecycle",
                    "healthcare": "improve patient outcomes while reducing costs",
                    "finance": "enhance compliance while accelerating decision-making",
                    "retail": "optimize inventory and enhance customer experience",
                    "manufacturing": "increase operational efficiency and quality control"
                }
                return examples.get(industry.lower(), "achieve your business objectives")
        
        return PersonalizationTool()
    
    async def personalize_content(self, content_template: str, lead_data: Dict[str, Any], 
                                 campaign_context: Dict[str, Any]) -> str:
        """Personalize content using AI agent"""
        try:
            personalization_task = Task(
                description=f"""Personalize the following content template for the specific lead:
                
                Content Template: {content_template}
                
                Lead Data: {json.dumps(lead_data, indent=2)}
                
                Campaign Context: {json.dumps(campaign_context, indent=2)}
                
                Please personalize the content by:
                1. Replacing placeholder variables with actual data
                2. Adapting messaging tone for the industry and role
                3. Including relevant examples and use cases
                4. Ensuring the content feels personal and relevant
                5. Maintaining professional tone while being conversational
                """,
                agent=self.personalization_agent,
                expected_output="Fully personalized content ready for delivery"
            )
            
            crew = Crew(
                agents=[self.personalization_agent],
                tasks=[personalization_task],
                verbose=True,
                process=Process.sequential
            )
            
            result = await asyncio.to_thread(crew.kickoff)
            return result if isinstance(result, str) else str(result)
            
        except Exception as e:
            logger.error(f"Error personalizing content: {e}")
            return content_template  # Fallback to original template

class CampaignExecutionEngine:
    """Engine for executing nurturing campaign steps"""
    
    def __init__(self, db_config: Dict[str, str], redis_config: Dict[str, str]):
        self.db_config = db_config
        self.redis_config = redis_config
        self.execution_queue = asyncio.Queue()
        self.delivery_handlers = {}
        
    async def initialize(self):
        """Initialize execution engine"""
        try:
            # Initialize database connection
            self.db_pool = await asyncpg.create_pool(**self.db_config)
            
            # Initialize Redis connection
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config['host']}:{self.redis_config['port']}"
            )
            
            # Register delivery handlers
            self._register_delivery_handlers()
            
            # Start execution worker
            asyncio.create_task(self._execution_worker())
            
            logger.info("Campaign execution engine initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize execution engine: {e}")
            raise
    
    def _register_delivery_handlers(self):
        """Register handlers for different delivery channels"""
        self.delivery_handlers = {
            DeliveryChannel.EMAIL: self._send_email,
            DeliveryChannel.SMS: self._send_sms,
            DeliveryChannel.SOCIAL_MEDIA: self._post_social_media,
            DeliveryChannel.PHONE_CALL: self._schedule_phone_call,
            DeliveryChannel.RETARGETING_AD: self._create_retargeting_campaign
        }
    
    async def execute_campaign_step(self, enrollment: CampaignEnrollment, 
                                   step: CampaignStep, campaign: NurturingCampaign) -> bool:
        """Execute a specific campaign step for a lead"""
        try:
            # Get lead data
            lead_data = await self._get_lead_data(enrollment.lead_id)
            if not lead_data:
                logger.error(f"Lead data not found for {enrollment.lead_id}")
                return False
            
            # Check trigger conditions
            if not await self._check_trigger_conditions(step, lead_data, enrollment):
                logger.info(f"Trigger conditions not met for step {step.step_id}")
                return False
            
            # Get and personalize content
            content = await self._get_step_content(step, lead_data, campaign)
            if not content:
                logger.error(f"Content not found for step {step.step_id}")
                return False
            
            # Execute delivery
            delivery_handler = self.delivery_handlers.get(step.delivery_channel)
            if not delivery_handler:
                logger.error(f"No handler for delivery channel {step.delivery_channel}")
                return False
            
            success = await delivery_handler(enrollment, step, content, lead_data)
            
            if success:
                # Update enrollment progress
                await self._update_enrollment_progress(enrollment, step)
                
                # Track interaction
                await self._track_interaction(enrollment, step, "delivered")
                
                # Schedule next step
                await self._schedule_next_step(enrollment, campaign)
                
                logger.info(f"Successfully executed step {step.step_id} for lead {enrollment.lead_id}")
                return True
            else:
                logger.error(f"Failed to execute step {step.step_id} for lead {enrollment.lead_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing campaign step {step.step_id}: {e}")
            return False
    
    async def _check_trigger_conditions(self, step: CampaignStep, lead_data: Dict[str, Any], 
                                      enrollment: CampaignEnrollment) -> bool:
        """Check if trigger conditions are met for step execution"""
        try:
            if step.trigger_type == TriggerType.TIME_BASED:
                # Time-based triggers are handled by scheduler
                return True
            
            elif step.trigger_type == TriggerType.BEHAVIOR_BASED:
                # Check behavioral conditions
                conditions = step.trigger_conditions
                for condition_type, condition_value in conditions.items():
                    if condition_type == "website_visits":
                        if lead_data.get("website_visits", 0) < condition_value:
                            return False
                    elif condition_type == "email_opens":
                        if lead_data.get("email_opens", 0) < condition_value:
                            return False
                    elif condition_type == "content_downloads":
                        if lead_data.get("content_downloads", 0) < condition_value:
                            return False
                
                return True
            
            elif step.trigger_type == TriggerType.SCORE_BASED:
                # Check lead score conditions
                required_score = step.trigger_conditions.get("min_score", 0)
                current_score = lead_data.get("total_score", 0)
                return current_score >= required_score
            
            elif step.trigger_type == TriggerType.LIFECYCLE_STAGE:
                # Check lifecycle stage
                required_stage = step.trigger_conditions.get("stage")
                current_stage = lead_data.get("lifecycle_stage")
                return current_stage == required_stage
            
            else:
                return True
                
        except Exception as e:
            logger.error(f"Error checking trigger conditions: {e}")
            return False
    
    async def _get_step_content(self, step: CampaignStep, lead_data: Dict[str, Any], 
                               campaign: NurturingCampaign) -> Optional[Dict[str, Any]]:
        """Get and personalize content for campaign step"""
        try:
            # Get base content
            async with self.db_pool.acquire() as conn:
                content_row = await conn.fetchrow("""
                    SELECT * FROM campaign_content 
                    WHERE content_id = $1 AND content_type = $2
                """, step.content_id, step.content_type)
                
                if not content_row:
                    return None
                
                base_content = {
                    "subject": content_row.get("subject", ""),
                    "body": content_row.get("body", ""),
                    "template_variables": json.loads(content_row.get("template_variables", "{}")),
                    "attachments": json.loads(content_row.get("attachments", "[]"))
                }
            
            # Apply personalization if enabled
            if step.dynamic_content:
                personalization_engine = ContentPersonalizationEngine(
                    openai_api_key="your-openai-api-key"  # Get from config
                )
                
                campaign_context = {
                    "campaign_type": campaign.campaign_type.value,
                    "step_number": step.step_number,
                    "campaign_goal": campaign.conversion_goals
                }
                
                if base_content["subject"]:
                    base_content["subject"] = await personalization_engine.personalize_content(
                        base_content["subject"], lead_data, campaign_context
                    )
                
                if base_content["body"]:
                    base_content["body"] = await personalization_engine.personalize_content(
                        base_content["body"], lead_data, campaign_context
                    )
            
            # Apply template variables
            for var_name, var_value in base_content["template_variables"].items():
                if var_name in lead_data:
                    placeholder = f"{{{var_name}}}"
                    base_content["subject"] = base_content["subject"].replace(placeholder, str(lead_data[var_name]))
                    base_content["body"] = base_content["body"].replace(placeholder, str(lead_data[var_name]))
            
            return base_content
            
        except Exception as e:
            logger.error(f"Error getting step content: {e}")
            return None
    
    async def _send_email(self, enrollment: CampaignEnrollment, step: CampaignStep, 
                         content: Dict[str, Any], lead_data: Dict[str, Any]) -> bool:
        """Send email through delivery service"""
        try:
            email_data = {
                "to": lead_data["email"],
                "subject": content["subject"],
                "body": content["body"],
                "template_id": step.content_id,
                "campaign_id": enrollment.campaign_id,
                "lead_id": enrollment.lead_id,
                "step_id": step.step_id,
                "attachments": content.get("attachments", [])
            }
            
            # Send to email service queue
            await self.redis.lpush("email_delivery_queue", json.dumps(email_data))
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    async def _send_sms(self, enrollment: CampaignEnrollment, step: CampaignStep, 
                       content: Dict[str, Any], lead_data: Dict[str, Any]) -> bool:
        """Send SMS through delivery service"""
        try:
            phone_number = lead_data.get("phone_number")
            if not phone_number:
                logger.warning(f"No phone number for lead {enrollment.lead_id}")
                return False
            
            sms_data = {
                "to": phone_number,
                "message": content["body"][:160],  # SMS length limit
                "campaign_id": enrollment.campaign_id,
                "lead_id": enrollment.lead_id,
                "step_id": step.step_id
            }
            
            # Send to SMS service queue
            await self.redis.lpush("sms_delivery_queue", json.dumps(sms_data))
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
    
    async def _post_social_media(self, enrollment: CampaignEnrollment, step: CampaignStep, 
                                content: Dict[str, Any], lead_data: Dict[str, Any]) -> bool:
        """Create social media engagement"""
        try:
            # Get social media profiles
            social_profiles = lead_data.get("social_profiles", {})
            if not social_profiles:
                return False
            
            social_data = {
                "profiles": social_profiles,
                "content": content["body"],
                "campaign_id": enrollment.campaign_id,
                "lead_id": enrollment.lead_id,
                "step_id": step.step_id,
                "action_type": "engage"  # like, comment, follow, etc.
            }
            
            # Send to social media service queue
            await self.redis.lpush("social_media_queue", json.dumps(social_data))
            
            return True
            
        except Exception as e:
            logger.error(f"Error posting social media: {e}")
            return False
    
    async def _schedule_phone_call(self, enrollment: CampaignEnrollment, step: CampaignStep, 
                                  content: Dict[str, Any], lead_data: Dict[str, Any]) -> bool:
        """Schedule phone call task"""
        try:
            # Create task for sales rep
            task_data = {
                "type": "phone_call",
                "lead_id": enrollment.lead_id,
                "campaign_id": enrollment.campaign_id,
                "step_id": step.step_id,
                "priority": "medium",
                "due_date": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
                "description": content["body"],
                "assigned_rep": lead_data.get("assigned_rep_id")
            }
            
            # Create task in CRM system
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO tasks (task_id, type, lead_id, assigned_rep_id, priority, 
                                     due_date, description, campaign_id, created_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, 
                    f"call_{enrollment.lead_id}_{step.step_id}",
                    task_data["type"],
                    task_data["lead_id"],
                    task_data["assigned_rep"],
                    task_data["priority"],
                    task_data["due_date"],
                    task_data["description"],
                    task_data["campaign_id"],
                    datetime.utcnow()
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling phone call: {e}")
            return False
    
    async def _create_retargeting_campaign(self, enrollment: CampaignEnrollment, step: CampaignStep, 
                                         content: Dict[str, Any], lead_data: Dict[str, Any]) -> bool:
        """Create retargeting advertising campaign"""
        try:
            retargeting_data = {
                "lead_email": lead_data["email"],
                "campaign_content": content["body"],
                "target_platforms": ["facebook", "google", "linkedin"],
                "budget": 50,  # Daily budget
                "duration_days": 7,
                "campaign_id": enrollment.campaign_id,
                "lead_id": enrollment.lead_id,
                "step_id": step.step_id
            }
            
            # Send to advertising service queue
            await self.redis.lpush("retargeting_queue", json.dumps(retargeting_data))
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating retargeting campaign: {e}")
            return False
    
    async def _update_enrollment_progress(self, enrollment: CampaignEnrollment, step: CampaignStep):
        """Update enrollment progress after step execution"""
        try:
            enrollment.completed_steps.append(step.step_number)
            enrollment.current_step = step.step_number + 1
            enrollment.last_interaction = datetime.utcnow()
            
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE campaign_enrollments SET
                        current_step = $1,
                        completed_steps = $2,
                        last_interaction = $3
                    WHERE enrollment_id = $4
                """, 
                    enrollment.current_step,
                    json.dumps(enrollment.completed_steps),
                    enrollment.last_interaction,
                    enrollment.enrollment_id
                )
                
        except Exception as e:
            logger.error(f"Error updating enrollment progress: {e}")
    
    async def _track_interaction(self, enrollment: CampaignEnrollment, step: CampaignStep, 
                               interaction_type: str):
        """Track campaign interaction for analytics"""
        try:
            interaction_data = {
                "enrollment_id": enrollment.enrollment_id,
                "lead_id": enrollment.lead_id,
                "campaign_id": enrollment.campaign_id,
                "step_id": step.step_id,
                "interaction_type": interaction_type,
                "delivery_channel": step.delivery_channel.value,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store interaction
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO campaign_interactions (
                        enrollment_id, lead_id, campaign_id, step_id, 
                        interaction_type, delivery_channel, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                    interaction_data["enrollment_id"],
                    interaction_data["lead_id"],
                    interaction_data["campaign_id"],
                    interaction_data["step_id"],
                    interaction_data["interaction_type"],
                    interaction_data["delivery_channel"],
                    datetime.utcnow()
                )
            
            # Update Redis for real-time analytics
            await self.redis.lpush("campaign_analytics", json.dumps(interaction_data))
            
        except Exception as e:
            logger.error(f"Error tracking interaction: {e}")
    
    async def _schedule_next_step(self, enrollment: CampaignEnrollment, campaign: NurturingCampaign):
        """Schedule the next step in the campaign"""
        try:
            if enrollment.current_step >= len(campaign.steps):
                # Campaign completed
                await self._complete_enrollment(enrollment)
                return
            
            next_step = campaign.steps[enrollment.current_step]
            
            # Calculate next execution time
            delay_hours = next_step.delay_hours + (next_step.delay_days * 24)
            next_execution_time = datetime.utcnow() + timedelta(hours=delay_hours)
            
            # Schedule next step execution
            schedule_data = {
                "enrollment_id": enrollment.enrollment_id,
                "campaign_id": enrollment.campaign_id,
                "step_id": next_step.step_id,
                "execution_time": next_execution_time.isoformat()
            }
            
            await self.redis.zadd(
                "campaign_execution_schedule",
                {json.dumps(schedule_data): next_execution_time.timestamp()}
            )
            
            # Update enrollment next action date
            enrollment.next_action_date = next_execution_time
            
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE campaign_enrollments SET
                        next_action_date = $1
                    WHERE enrollment_id = $2
                """, next_execution_time, enrollment.enrollment_id)
                
        except Exception as e:
            logger.error(f"Error scheduling next step: {e}")
    
    async def _complete_enrollment(self, enrollment: CampaignEnrollment):
        """Complete campaign enrollment"""
        try:
            enrollment.status = "completed"
            enrollment.completion_date = datetime.utcnow()
            
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE campaign_enrollments SET
                        status = 'completed',
                        completion_date = $1
                    WHERE enrollment_id = $2
                """, enrollment.completion_date, enrollment.enrollment_id)
            
            logger.info(f"Completed campaign enrollment {enrollment.enrollment_id}")
            
        except Exception as e:
            logger.error(f"Error completing enrollment: {e}")
    
    async def _get_lead_data(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive lead data"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT l.*, ls.total_score, ls.qualification_level
                    FROM leads l
                    LEFT JOIN lead_scores ls ON l.lead_id = ls.lead_id
                    WHERE l.lead_id = $1
                """, lead_id)
                
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            logger.error(f"Error getting lead data: {e}")
            return None
    
    async def _execution_worker(self):
        """Background worker for campaign execution"""
        while True:
            try:
                # Check for scheduled executions
                current_time = datetime.utcnow().timestamp()
                
                # Get due executions from Redis sorted set
                due_executions = await self.redis.zrangebyscore(
                    "campaign_execution_schedule", 
                    0, 
                    current_time,
                    withscores=True
                )
                
                for execution_data, score in due_executions:
                    try:
                        execution_info = json.loads(execution_data)
                        
                        # Remove from schedule
                        await self.redis.zrem("campaign_execution_schedule", execution_data)
                        
                        # Execute step
                        await self._process_scheduled_execution(execution_info)
                        
                    except Exception as e:
                        logger.error(f"Error processing scheduled execution: {e}")
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in execution worker: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _process_scheduled_execution(self, execution_info: Dict[str, Any]):
        """Process a scheduled campaign execution"""
        try:
            # Get enrollment data
            async with self.db_pool.acquire() as conn:
                enrollment_row = await conn.fetchrow("""
                    SELECT * FROM campaign_enrollments WHERE enrollment_id = $1
                """, execution_info["enrollment_id"])
                
                if not enrollment_row:
                    logger.error(f"Enrollment not found: {execution_info['enrollment_id']}")
                    return
                
                # Get campaign data
                campaign_row = await conn.fetchrow("""
                    SELECT * FROM nurturing_campaigns WHERE campaign_id = $1
                """, execution_info["campaign_id"])
                
                if not campaign_row:
                    logger.error(f"Campaign not found: {execution_info['campaign_id']}")
                    return
                
                # Get step data
                step_row = await conn.fetchrow("""
                    SELECT * FROM campaign_steps WHERE step_id = $1
                """, execution_info["step_id"])
                
                if not step_row:
                    logger.error(f"Step not found: {execution_info['step_id']}")
                    return
            
            # Convert to objects
            enrollment = CampaignEnrollment(
                enrollment_id=enrollment_row["enrollment_id"],
                lead_id=enrollment_row["lead_id"],
                campaign_id=enrollment_row["campaign_id"],
                current_step=enrollment_row["current_step"],
                completed_steps=json.loads(enrollment_row["completed_steps"]),
                status=enrollment_row["status"],
                enrolled_at=enrollment_row["enrolled_at"],
                last_interaction=enrollment_row["last_interaction"]
            )
            
            step = CampaignStep(
                step_id=step_row["step_id"],
                campaign_id=step_row["campaign_id"],
                step_number=step_row["step_number"],
                name=step_row["name"],
                description=step_row["description"],
                content_type=step_row["content_type"],
                content_id=step_row["content_id"],
                delivery_channel=DeliveryChannel(step_row["delivery_channel"]),
                delay_hours=step_row["delay_hours"],
                delay_days=step_row["delay_days"],
                trigger_type=TriggerType(step_row["trigger_type"]),
                trigger_conditions=json.loads(step_row["trigger_conditions"]),
                dynamic_content=step_row["dynamic_content"]
            )
            
            campaign = NurturingCampaign(
                campaign_id=campaign_row["campaign_id"],
                name=campaign_row["name"],
                description=campaign_row["description"],
                campaign_type=CampaignType(campaign_row["campaign_type"]),
                conversion_goals=json.loads(campaign_row["conversion_goals"])
            )
            
            # Execute the step
            await self.execute_campaign_step(enrollment, step, campaign)
            
        except Exception as e:
            logger.error(f"Error processing scheduled execution: {e}")

class NurturingCampaignManager:
    """Main manager for nurturing campaigns"""
    
    def __init__(self, db_config: Dict[str, str], redis_config: Dict[str, str], 
                 openai_api_key: str):
        self.db_config = db_config
        self.redis_config = redis_config
        self.execution_engine = CampaignExecutionEngine(db_config, redis_config)
        self.personalization_engine = ContentPersonalizationEngine(openai_api_key)
        
        # Campaign templates
        self.campaign_templates = {}
        
        # Performance metrics
        self.performance_metrics = {
            "total_campaigns": 0,
            "active_enrollments": 0,
            "completion_rate": 0.0,
            "average_engagement": 0.0
        }
    
    async def initialize(self):
        """Initialize campaign manager"""
        try:
            # Initialize database connection
            self.db_pool = await asyncpg.create_pool(**self.db_config)
            
            # Initialize Redis connection
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config['host']}:{self.redis_config['port']}"
            )
            
            # Initialize execution engine
            await self.execution_engine.initialize()
            
            # Load campaign templates
            await self._load_campaign_templates()
            
            logger.info("Nurturing campaign manager initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize campaign manager: {e}")
            raise
    
    async def create_campaign(self, campaign_data: Dict[str, Any]) -> NurturingCampaign:
        """Create a new nurturing campaign"""
        try:
            campaign = NurturingCampaign(
                campaign_id=f"campaign_{int(datetime.utcnow().timestamp())}",
                name=campaign_data["name"],
                description=campaign_data["description"],
                campaign_type=CampaignType(campaign_data["campaign_type"]),
                target_segments=campaign_data.get("target_segments", []),
                entry_criteria=campaign_data.get("entry_criteria", {}),
                exit_criteria=campaign_data.get("exit_criteria", {}),
                conversion_goals=campaign_data.get("conversion_goals", []),
                created_by=campaign_data.get("created_by", "system")
            )
            
            # Store campaign in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO nurturing_campaigns (
                        campaign_id, name, description, campaign_type, target_segments,
                        entry_criteria, exit_criteria, conversion_goals, status, created_by, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """,
                    campaign.campaign_id, campaign.name, campaign.description,
                    campaign.campaign_type.value, json.dumps(campaign.target_segments),
                    json.dumps(campaign.entry_criteria), json.dumps(campaign.exit_criteria),
                    json.dumps(campaign.conversion_goals), campaign.status.value,
                    campaign.created_by, campaign.created_at
                )
            
            logger.info(f"Created campaign {campaign.campaign_id}: {campaign.name}")
            return campaign
            
        except Exception as e:
            logger.error(f"Error creating campaign: {e}")
            raise
    
    async def enroll_lead(self, lead_id: str, campaign_id: str, 
                         enrollment_data: Optional[Dict[str, Any]] = None) -> CampaignEnrollment:
        """Enroll a lead in a nurturing campaign"""
        try:
            # Check if lead is already enrolled
            async with self.db_pool.acquire() as conn:
                existing = await conn.fetchrow("""
                    SELECT * FROM campaign_enrollments 
                    WHERE lead_id = $1 AND campaign_id = $2 AND status = 'active'
                """, lead_id, campaign_id)
                
                if existing:
                    logger.warning(f"Lead {lead_id} already enrolled in campaign {campaign_id}")
                    return None
                
                # Check entry criteria
                lead_data = await self._get_lead_data(lead_id)
                campaign_data = await conn.fetchrow("""
                    SELECT * FROM nurturing_campaigns WHERE campaign_id = $1
                """, campaign_id)
                
                if not self._check_entry_criteria(lead_data, json.loads(campaign_data["entry_criteria"])):
                    logger.info(f"Lead {lead_id} does not meet entry criteria for campaign {campaign_id}")
                    return None
            
            # Create enrollment
            enrollment = CampaignEnrollment(
                enrollment_id=f"enroll_{lead_id}_{campaign_id}_{int(datetime.utcnow().timestamp())}",
                lead_id=lead_id,
                campaign_id=campaign_id,
                personalization_data=enrollment_data or {}
            )
            
            # Store enrollment
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO campaign_enrollments (
                        enrollment_id, lead_id, campaign_id, current_step, completed_steps,
                        status, enrolled_at, personalization_data
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                    enrollment.enrollment_id, enrollment.lead_id, enrollment.campaign_id,
                    enrollment.current_step, json.dumps(enrollment.completed_steps),
                    enrollment.status, enrollment.enrolled_at,
                    json.dumps(enrollment.personalization_data)
                )
            
            # Schedule first step
            await self._schedule_first_step(enrollment, campaign_id)
            
            logger.info(f"Enrolled lead {lead_id} in campaign {campaign_id}")
            return enrollment
            
        except Exception as e:
            logger.error(f"Error enrolling lead {lead_id} in campaign {campaign_id}: {e}")
            raise
    
    async def _check_entry_criteria(self, lead_data: Dict[str, Any], 
                                   entry_criteria: Dict[str, Any]) -> bool:
        """Check if lead meets campaign entry criteria"""
        try:
            for field, criteria in entry_criteria.items():
                lead_value = lead_data.get(field)
                
                if isinstance(criteria, dict):
                    operator = criteria.get("operator", "equals")
                    value = criteria.get("value")
                    
                    if operator == "equals" and lead_value != value:
                        return False
                    elif operator == "greater_than" and (not lead_value or lead_value <= value):
                        return False
                    elif operator == "less_than" and (not lead_value or lead_value >= value):
                        return False
                    elif operator == "contains" and value not in str(lead_value).lower():
                        return False
                    elif operator == "in" and lead_value not in value:
                        return False
                else:
                    if lead_value != criteria:
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking entry criteria: {e}")
            return False
    
    async def _schedule_first_step(self, enrollment: CampaignEnrollment, campaign_id: str):
        """Schedule the first step of a campaign"""
        try:
            # Get first step
            async with self.db_pool.acquire() as conn:
                first_step = await conn.fetchrow("""
                    SELECT * FROM campaign_steps 
                    WHERE campaign_id = $1 
                    ORDER BY step_number ASC 
                    LIMIT 1
                """, campaign_id)
                
                if first_step:
                    # Schedule immediate or delayed execution
                    delay_hours = first_step["delay_hours"] + (first_step["delay_days"] * 24)
                    execution_time = datetime.utcnow() + timedelta(hours=delay_hours)
                    
                    schedule_data = {
                        "enrollment_id": enrollment.enrollment_id,
                        "campaign_id": enrollment.campaign_id,
                        "step_id": first_step["step_id"],
                        "execution_time": execution_time.isoformat()
                    }
                    
                    await self.redis.zadd(
                        "campaign_execution_schedule",
                        {json.dumps(schedule_data): execution_time.timestamp()}
                    )
                
        except Exception as e:
            logger.error(f"Error scheduling first step: {e}")
    
    async def get_campaign_analytics(self, campaign_id: str, 
                                   date_range: Optional[Tuple[datetime, datetime]] = None) -> Dict[str, Any]:
        """Get comprehensive campaign analytics"""
        try:
            if not date_range:
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=30)
            else:
                start_date, end_date = date_range
            
            async with self.db_pool.acquire() as conn:
                # Basic campaign metrics
                campaign_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total_enrollments,
                        COUNT(CASE WHEN status = 'active' THEN 1 END) as active_enrollments,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_enrollments,
                        COUNT(CASE WHEN conversion_achieved = true THEN 1 END) as conversions,
                        AVG(engagement_score) as avg_engagement_score
                    FROM campaign_enrollments
                    WHERE campaign_id = $1 AND enrolled_at BETWEEN $2 AND $3
                """, campaign_id, start_date, end_date)
                
                # Step performance
                step_performance = await conn.fetch("""
                    SELECT 
                        cs.step_number,
                        cs.name,
                        COUNT(ci.*) as interactions,
                        COUNT(CASE WHEN ci.interaction_type = 'delivered' THEN 1 END) as deliveries,
                        COUNT(CASE WHEN ci.interaction_type = 'opened' THEN 1 END) as opens,
                        COUNT(CASE WHEN ci.interaction_type = 'clicked' THEN 1 END) as clicks
                    FROM campaign_steps cs
                    LEFT JOIN campaign_interactions ci ON cs.step_id = ci.step_id
                    WHERE cs.campaign_id = $1 AND ci.created_at BETWEEN $2 AND $3
                    GROUP BY cs.step_id, cs.step_number, cs.name
                    ORDER BY cs.step_number
                """, campaign_id, start_date, end_date)
                
                # Channel performance
                channel_performance = await conn.fetch("""
                    SELECT 
                        delivery_channel,
                        COUNT(*) as total_interactions,
                        COUNT(CASE WHEN interaction_type = 'opened' THEN 1 END) as opens,
                        COUNT(CASE WHEN interaction_type = 'clicked' THEN 1 END) as clicks
                    FROM campaign_interactions
                    WHERE campaign_id = $1 AND created_at BETWEEN $2 AND $3
                    GROUP BY delivery_channel
                """, campaign_id, start_date, end_date)
            
            # Calculate metrics
            total_enrollments = campaign_stats["total_enrollments"] or 0
            conversions = campaign_stats["conversions"] or 0
            conversion_rate = (conversions / total_enrollments) if total_enrollments > 0 else 0
            
            return {
                "campaign_id": campaign_id,
                "date_range": {"start": start_date.isoformat(), "end": end_date.isoformat()},
                "overview": {
                    "total_enrollments": total_enrollments,
                    "active_enrollments": campaign_stats["active_enrollments"] or 0,
                    "completed_enrollments": campaign_stats["completed_enrollments"] or 0,
                    "conversion_rate": conversion_rate,
                    "avg_engagement_score": float(campaign_stats["avg_engagement_score"] or 0)
                },
                "step_performance": [
                    {
                        "step_number": row["step_number"],
                        "name": row["name"],
                        "deliveries": row["deliveries"] or 0,
                        "opens": row["opens"] or 0,
                        "clicks": row["clicks"] or 0,
                        "open_rate": (row["opens"] / max(1, row["deliveries"])) if row["deliveries"] else 0,
                        "click_rate": (row["clicks"] / max(1, row["opens"])) if row["opens"] else 0
                    }
                    for row in step_performance
                ],
                "channel_performance": [
                    {
                        "channel": row["delivery_channel"],
                        "interactions": row["total_interactions"],
                        "opens": row["opens"] or 0,
                        "clicks": row["clicks"] or 0,
                        "engagement_rate": ((row["opens"] + row["clicks"]) / max(1, row["total_interactions"]))
                    }
                    for row in channel_performance
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting campaign analytics: {e}")
            return {}
    
    async def _load_campaign_templates(self):
        """Load predefined campaign templates"""
        try:
            # Define standard campaign templates
            self.campaign_templates = {
                "welcome_series": {
                    "name": "Welcome Series",
                    "description": "Onboard new leads with educational content",
                    "steps": [
                        {"delay_days": 0, "content_type": "email", "subject": "Welcome to {company_name}"},
                        {"delay_days": 3, "content_type": "email", "subject": "Getting started guide"},
                        {"delay_days": 7, "content_type": "phone_call", "description": "Introduction call"},
                        {"delay_days": 14, "content_type": "email", "subject": "Case study: Success story"}
                    ]
                },
                "trial_nurture": {
                    "name": "Trial Nurturing",
                    "description": "Convert trial users to paid customers",
                    "steps": [
                        {"delay_days": 1, "content_type": "email", "subject": "Your trial is active"},
                        {"delay_days": 7, "content_type": "email", "subject": "Getting the most from your trial"},
                        {"delay_days": 14, "content_type": "phone_call", "description": "Trial check-in call"},
                        {"delay_days": 21, "content_type": "email", "subject": "Trial ending soon - upgrade now"}
                    ]
                }
            }
            
            logger.info(f"Loaded {len(self.campaign_templates)} campaign templates")
            
        except Exception as e:
            logger.error(f"Error loading campaign templates: {e}")
    
    async def _get_lead_data(self, lead_id: str) -> Dict[str, Any]:
        """Get lead data for campaign processing"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT l.*, ls.total_score, ls.qualification_level
                    FROM leads l
                    LEFT JOIN lead_scores ls ON l.lead_id = ls.lead_id
                    WHERE l.lead_id = $1
                """, lead_id)
                
                return dict(row) if row else {}
                
        except Exception as e:
            logger.error(f"Error getting lead data: {e}")
            return {}
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            if hasattr(self, 'db_pool'):
                await self.db_pool.close()
            if hasattr(self, 'redis'):
                await self.redis.close()
            logger.info("Nurturing campaign manager cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Example usage
async def main():
    """Example usage of nurturing campaigns"""
    
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
    
    # Initialize manager
    campaign_manager = NurturingCampaignManager(db_config, redis_config, "your-openai-api-key")
    await campaign_manager.initialize()
    
    try:
        # Create a welcome series campaign
        campaign_data = {
            "name": "New Lead Welcome Series",
            "description": "Nurture new leads with educational content",
            "campaign_type": "welcome_series",
            "target_segments": ["new_leads", "qualified_leads"],
            "entry_criteria": {
                "total_score": {"operator": "greater_than", "value": 50}
            },
            "conversion_goals": ["demo_scheduled", "trial_started"]
        }
        
        campaign = await campaign_manager.create_campaign(campaign_data)
        print(f"Created campaign: {campaign.name}")
        
        # Enroll a lead
        enrollment = await campaign_manager.enroll_lead("lead_123", campaign.campaign_id)
        if enrollment:
            print(f"Enrolled lead in campaign: {enrollment.enrollment_id}")
        
        # Get analytics
        analytics = await campaign_manager.get_campaign_analytics(campaign.campaign_id)
        print(f"Campaign analytics: {json.dumps(analytics, indent=2, default=str)}")
        
    finally:
        await campaign_manager.cleanup()

if __name__ == "__main__":
    asyncio.run(main())