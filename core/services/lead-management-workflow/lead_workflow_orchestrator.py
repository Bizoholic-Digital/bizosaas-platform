"""
Lead Management Workflow Orchestrator
Main orchestration service that coordinates all lead management components
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
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
import uvicorn

# Import our components
from lead_scoring_engine import LeadScoringEngine, LeadData, LeadScoringModel
from assignment_system import LeadAssignmentSystem, LeadAssignment, AssignmentStrategy
from nurturing_campaigns import NurturingCampaignManager, CampaignEnrollment, CampaignType
from platform_integrations import PlatformIntegrationManager
from hitl_management import HITLManagementSystem, InterventionType, ReviewPriority

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class EventType(Enum):
    LEAD_CREATED = "lead_created"
    LEAD_UPDATED = "lead_updated"
    LEAD_SCORED = "lead_scored"
    LEAD_ASSIGNED = "lead_assigned"
    CAMPAIGN_ENROLLED = "campaign_enrolled"
    CAMPAIGN_COMPLETED = "campaign_completed"
    ESCALATION_TRIGGERED = "escalation_triggered"
    MANUAL_INTERVENTION = "manual_intervention"

@dataclass
class WorkflowEvent:
    """Workflow event for processing"""
    event_id: str
    event_type: EventType
    entity_id: str  # lead_id, assignment_id, etc.
    event_data: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1-10, 1 is highest priority
    created_at: datetime = field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3

# Pydantic models for API
class LeadCreateRequest(BaseModel):
    email: str
    company_name: str
    company_size: Optional[int] = None
    industry: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    service_requirements: List[str] = Field(default_factory=list)
    website_visits: int = 0
    email_opens: int = 0
    content_downloads: int = 0
    referral_source: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LeadUpdateRequest(BaseModel):
    company_size: Optional[int] = None
    industry: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    service_requirements: Optional[List[str]] = None
    website_visits: Optional[int] = None
    email_opens: Optional[int] = None
    content_downloads: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class ScoreOverrideRequest(BaseModel):
    new_score: float
    reason: str
    override_by: str

class AssignmentOverrideRequest(BaseModel):
    new_rep_id: str
    reason: str
    override_by: str

class CampaignEnrollmentRequest(BaseModel):
    campaign_id: str
    enrollment_data: Dict[str, Any] = Field(default_factory=dict)

class WorkflowResponse(BaseModel):
    status: str
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)

class LeadWorkflowOrchestrator:
    """Main orchestrator for lead management workflow"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.status = WorkflowStatus.ACTIVE
        
        # Core components
        self.scoring_engine = None
        self.assignment_system = None
        self.campaign_manager = None
        self.integration_manager = None
        self.hitl_system = None
        
        # Event processing
        self.event_queue = asyncio.Queue()
        self.event_processors = {}
        self.processing_stats = {
            "total_events": 0,
            "processed_events": 0,
            "failed_events": 0,
            "average_processing_time": 0.0
        }
        
        # Workflow rules
        self.workflow_rules = {}
        
        # Performance monitoring
        self.performance_metrics = {
            "leads_processed": 0,
            "assignments_created": 0,
            "campaigns_enrolled": 0,
            "integrations_synced": 0,
            "errors_encountered": 0
        }
    
    async def initialize(self):
        """Initialize the workflow orchestrator"""
        try:
            logger.info("Initializing Lead Workflow Orchestrator...")
            
            # Initialize database and Redis connections
            self.db_pool = await asyncpg.create_pool(**self.config["database"])
            self.redis = await aioredis.from_url(
                f"redis://{self.config['redis']['host']}:{self.config['redis']['port']}"
            )
            
            # Initialize core components
            await self._initialize_components()
            
            # Load workflow rules
            await self._load_workflow_rules()
            
            # Start event processors
            await self._start_event_processors()
            
            # Start monitoring tasks
            asyncio.create_task(self._performance_monitor())
            asyncio.create_task(self._health_checker())
            
            self.status = WorkflowStatus.ACTIVE
            logger.info("Lead Workflow Orchestrator initialized successfully")
            
        except Exception as e:
            self.status = WorkflowStatus.ERROR
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise
    
    async def _initialize_components(self):
        """Initialize all workflow components"""
        try:
            # Initialize Lead Scoring Engine
            self.scoring_engine = LeadScoringEngine(
                self.config["database"],
                self.config["redis"],
                self.config["openai_api_key"]
            )
            await self.scoring_engine.initialize()
            
            # Initialize Assignment System
            self.assignment_system = LeadAssignmentSystem(
                self.config["database"],
                self.config["redis"]
            )
            await self.assignment_system.initialize()
            
            # Initialize Campaign Manager
            self.campaign_manager = NurturingCampaignManager(
                self.config["database"],
                self.config["redis"],
                self.config["openai_api_key"]
            )
            await self.campaign_manager.initialize()
            
            # Initialize Platform Integrations
            self.integration_manager = PlatformIntegrationManager(
                self.config["database"],
                self.config["redis"]
            )
            await self.integration_manager.initialize()
            
            # Initialize HITL System
            self.hitl_system = HITLManagementSystem(
                self.config["database"],
                self.config["redis"]
            )
            await self.hitl_system.initialize()
            
            logger.info("All workflow components initialized")
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
    
    async def _load_workflow_rules(self):
        """Load workflow automation rules"""
        try:
            async with self.db_pool.acquire() as conn:
                rules = await conn.fetch("""
                    SELECT rule_id, rule_name, conditions, actions, priority, enabled
                    FROM workflow_rules WHERE enabled = true
                    ORDER BY priority DESC
                """)
                
                for rule in rules:
                    self.workflow_rules[rule["rule_id"]] = {
                        "name": rule["rule_name"],
                        "conditions": json.loads(rule["conditions"]),
                        "actions": json.loads(rule["actions"]),
                        "priority": rule["priority"],
                        "enabled": rule["enabled"]
                    }
                
                logger.info(f"Loaded {len(self.workflow_rules)} workflow rules")
                
        except Exception as e:
            logger.error(f"Error loading workflow rules: {e}")
            # Create default rules
            await self._create_default_rules()
    
    async def _create_default_rules(self):
        """Create default workflow rules"""
        default_rules = {
            "auto_assign_high_score": {
                "name": "Auto-assign high-scoring leads",
                "conditions": {"total_score": {"operator": "greater_than", "value": 80}},
                "actions": {"assign_lead": True, "strategy": "performance_weighted"},
                "priority": 10
            },
            "enroll_qualified_leads": {
                "name": "Enroll qualified leads in nurturing",
                "conditions": {"qualification_level": {"operator": "in", "value": ["warm", "hot"]}},
                "actions": {"enroll_campaign": True, "campaign_type": "welcome_series"},
                "priority": 8
            },
            "escalate_urgent_leads": {
                "name": "Escalate urgent high-value leads",
                "conditions": {
                    "total_score": {"operator": "greater_than", "value": 90},
                    "budget": {"operator": "greater_than", "value": 100000}
                },
                "actions": {"escalate": True, "notify_manager": True},
                "priority": 15
            }
        }
        
        self.workflow_rules.update(default_rules)
    
    async def _start_event_processors(self):
        """Start event processing workers"""
        try:
            # Register event processors
            self.event_processors = {
                EventType.LEAD_CREATED: self._process_lead_created,
                EventType.LEAD_UPDATED: self._process_lead_updated,
                EventType.LEAD_SCORED: self._process_lead_scored,
                EventType.LEAD_ASSIGNED: self._process_lead_assigned,
                EventType.CAMPAIGN_ENROLLED: self._process_campaign_enrolled,
                EventType.ESCALATION_TRIGGERED: self._process_escalation_triggered
            }
            
            # Start worker tasks
            for i in range(3):  # 3 worker processes
                asyncio.create_task(self._event_worker(f"worker_{i}"))
            
            logger.info("Event processors started")
            
        except Exception as e:
            logger.error(f"Error starting event processors: {e}")
            raise
    
    async def _event_worker(self, worker_id: str):
        """Background worker for processing events"""
        logger.info(f"Event worker {worker_id} started")
        
        while self.status == WorkflowStatus.ACTIVE:
            try:
                # Get event from queue with timeout
                try:
                    event = await asyncio.wait_for(self.event_queue.get(), timeout=5.0)
                except asyncio.TimeoutError:
                    continue
                
                # Process event
                start_time = datetime.utcnow()
                success = await self._process_event(event)
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                
                # Update statistics
                self.processing_stats["total_events"] += 1
                if success:
                    self.processing_stats["processed_events"] += 1
                    event.processed_at = datetime.utcnow()
                else:
                    self.processing_stats["failed_events"] += 1
                    event.retry_count += 1
                    
                    # Retry if not exceeded max retries
                    if event.retry_count <= event.max_retries:
                        await asyncio.sleep(2 ** event.retry_count)  # Exponential backoff
                        await self.event_queue.put(event)
                
                # Update average processing time
                total_processed = self.processing_stats["processed_events"]
                current_avg = self.processing_stats["average_processing_time"]
                self.processing_stats["average_processing_time"] = (
                    (current_avg * (total_processed - 1) + processing_time) / total_processed
                ) if total_processed > 0 else processing_time
                
                # Mark task as done
                self.event_queue.task_done()
                
            except Exception as e:
                logger.error(f"Error in event worker {worker_id}: {e}")
                await asyncio.sleep(5)
        
        logger.info(f"Event worker {worker_id} stopped")
    
    async def _process_event(self, event: WorkflowEvent) -> bool:
        """Process a workflow event"""
        try:
            processor = self.event_processors.get(event.event_type)
            if not processor:
                logger.warning(f"No processor found for event type {event.event_type}")
                return False
            
            result = await processor(event)
            
            if result:
                logger.info(f"Successfully processed event {event.event_id}")
                
                # Store event in database for audit
                await self._store_event_log(event, success=True)
                
                return True
            else:
                logger.error(f"Failed to process event {event.event_id}")
                await self._store_event_log(event, success=False)
                return False
                
        except Exception as e:
            logger.error(f"Error processing event {event.event_id}: {e}")
            await self._store_event_log(event, success=False, error_message=str(e))
            return False
    
    # Event processors
    
    async def _process_lead_created(self, event: WorkflowEvent) -> bool:
        """Process lead creation event"""
        try:
            lead_data = event.event_data
            lead_id = event.entity_id
            
            # Create LeadData object
            lead = LeadData(
                lead_id=lead_id,
                email=lead_data["email"],
                company_name=lead_data["company_name"],
                company_size=lead_data.get("company_size"),
                industry=lead_data.get("industry"),
                job_title=lead_data.get("job_title"),
                location=lead_data.get("location"),
                budget=lead_data.get("budget"),
                timeline=lead_data.get("timeline"),
                service_requirements=lead_data.get("service_requirements", []),
                website_visits=lead_data.get("website_visits", 0),
                email_opens=lead_data.get("email_opens", 0),
                content_downloads=lead_data.get("content_downloads", 0),
                referral_source=lead_data.get("referral_source")
            )
            
            # Score the lead
            scoring_result = await self.scoring_engine.score_lead(lead, use_ai=True)
            
            # Sync to CRM
            await self.integration_manager.sync_lead_to_crm(lead_data)
            
            # Send analytics data
            await self.integration_manager.send_analytics_data("lead_metrics", {
                "lead_id": lead_id,
                "total_score": scoring_result.total_score,
                "qualification_level": scoring_result.qualification_level,
                "company_size": lead.company_size or 0,
                "industry": lead.industry or "",
                "referral_source": lead.referral_source or "unknown"
            })
            
            # Trigger lead scored event
            await self._trigger_event(EventType.LEAD_SCORED, lead_id, {
                "scoring_result": scoring_result.dict()
            })
            
            self.performance_metrics["leads_processed"] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error processing lead created: {e}")
            return False
    
    async def _process_lead_updated(self, event: WorkflowEvent) -> bool:
        """Process lead update event"""
        try:
            lead_id = event.entity_id
            update_data = event.event_data
            
            # Get current lead data
            current_lead_data = await self._get_lead_data(lead_id)
            if not current_lead_data:
                return False
            
            # Update lead data
            current_lead_data.update(update_data)
            
            # Re-score if significant changes
            if self._should_rescore(update_data):
                lead = self._dict_to_lead_data(current_lead_data)
                scoring_result = await self.scoring_engine.score_lead(lead, use_ai=False)
                
                # Trigger scored event
                await self._trigger_event(EventType.LEAD_SCORED, lead_id, {
                    "scoring_result": scoring_result.dict(),
                    "trigger": "update"
                })
            
            # Sync to CRM
            await self.integration_manager.sync_lead_to_crm(current_lead_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing lead updated: {e}")
            return False
    
    async def _process_lead_scored(self, event: WorkflowEvent) -> bool:
        """Process lead scoring event"""
        try:
            lead_id = event.entity_id
            scoring_data = event.event_data["scoring_result"]
            
            # Apply workflow rules
            await self._apply_workflow_rules(lead_id, scoring_data)
            
            # Sync score to CRM
            await self.integration_manager.sync_score_to_crm(lead_id, scoring_data)
            
            # Check for assignment
            lead_data = await self._get_lead_data(lead_id)
            if lead_data and scoring_data["total_score"] >= 60:  # Qualified threshold
                
                # Auto-assign if rules indicate
                if await self._should_auto_assign(scoring_data):
                    assignment = await self.assignment_system.assign_lead(
                        lead_id, 
                        lead_data,
                        strategy=self._determine_assignment_strategy(scoring_data)
                    )
                    
                    if assignment:
                        await self._trigger_event(EventType.LEAD_ASSIGNED, lead_id, {
                            "assignment": {
                                "assignment_id": assignment.assignment_id,
                                "rep_id": assignment.rep_id,
                                "strategy": assignment.strategy_used.value,
                                "score": assignment.assignment_score
                            }
                        })
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing lead scored: {e}")
            return False
    
    async def _process_lead_assigned(self, event: WorkflowEvent) -> bool:
        """Process lead assignment event"""
        try:
            lead_id = event.entity_id
            assignment_data = event.event_data["assignment"]
            
            # Sync assignment to CRM
            await self.integration_manager.sync_assignment_to_crm(assignment_data)
            
            # Send assignment analytics
            await self.integration_manager.send_analytics_data("assignment_metrics", assignment_data)
            
            # Send notification
            lead_data = await self._get_lead_data(lead_id)
            rep_data = await self._get_rep_data(assignment_data["rep_id"])
            
            await self.integration_manager.send_notification("lead_assignment", {
                "assignment_data": {**assignment_data, **lead_data},
                "rep_data": rep_data
            })
            
            # Check for campaign enrollment
            if await self._should_enroll_in_campaign(lead_data):
                campaign_id = await self._determine_campaign(lead_data)
                if campaign_id:
                    enrollment = await self.campaign_manager.enroll_lead(lead_id, campaign_id)
                    if enrollment:
                        await self._trigger_event(EventType.CAMPAIGN_ENROLLED, lead_id, {
                            "enrollment": {
                                "enrollment_id": enrollment.enrollment_id,
                                "campaign_id": campaign_id
                            }
                        })
            
            self.performance_metrics["assignments_created"] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error processing lead assigned: {e}")
            return False
    
    async def _process_campaign_enrolled(self, event: WorkflowEvent) -> bool:
        """Process campaign enrollment event"""
        try:
            lead_id = event.entity_id
            enrollment_data = event.event_data["enrollment"]
            
            # Send campaign analytics
            await self.integration_manager.send_analytics_data("campaign_metrics", {
                "campaign_id": enrollment_data["campaign_id"],
                "lead_id": lead_id,
                "enrollment_date": datetime.utcnow().isoformat(),
                "enrollment_type": "automatic"
            })
            
            self.performance_metrics["campaigns_enrolled"] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error processing campaign enrolled: {e}")
            return False
    
    async def _process_escalation_triggered(self, event: WorkflowEvent) -> bool:
        """Process escalation event"""
        try:
            escalation_data = event.event_data
            
            # Create HITL request for escalation
            request = await self.hitl_system.request_intervention(
                InterventionType.ESCALATION_HANDLING,
                escalation_data,
                "system",
                ReviewPriority.URGENT,
                f"Escalation: {escalation_data.get('type', 'Unknown')}",
                escalation_data.get("description", "")
            )
            
            # Send urgent notification
            await self.integration_manager.send_notification("escalation", escalation_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing escalation: {e}")
            return False
    
    # Workflow rule processing
    
    async def _apply_workflow_rules(self, lead_id: str, scoring_data: Dict[str, Any]):
        """Apply workflow rules based on lead data and scoring"""
        try:
            lead_data = await self._get_lead_data(lead_id)
            combined_data = {**lead_data, **scoring_data}
            
            for rule_id, rule in self.workflow_rules.items():
                if self._evaluate_conditions(rule["conditions"], combined_data):
                    await self._execute_rule_actions(rule["actions"], lead_id, combined_data)
                    logger.info(f"Applied workflow rule {rule_id} to lead {lead_id}")
            
        except Exception as e:
            logger.error(f"Error applying workflow rules: {e}")
    
    def _evaluate_conditions(self, conditions: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Evaluate workflow rule conditions"""
        try:
            for field, condition in conditions.items():
                value = data.get(field)
                
                if isinstance(condition, dict):
                    operator = condition.get("operator", "equals")
                    expected_value = condition.get("value")
                    
                    if operator == "equals" and value != expected_value:
                        return False
                    elif operator == "greater_than" and (value is None or value <= expected_value):
                        return False
                    elif operator == "less_than" and (value is None or value >= expected_value):
                        return False
                    elif operator == "in" and value not in expected_value:
                        return False
                    elif operator == "contains" and expected_value not in str(value).lower():
                        return False
                else:
                    if value != condition:
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error evaluating conditions: {e}")
            return False
    
    async def _execute_rule_actions(self, actions: Dict[str, Any], lead_id: str, data: Dict[str, Any]):
        """Execute workflow rule actions"""
        try:
            for action_type, action_config in actions.items():
                if action_type == "assign_lead" and action_config:
                    strategy = AssignmentStrategy(actions.get("strategy", "round_robin"))
                    await self.assignment_system.assign_lead(lead_id, data, strategy=strategy)
                
                elif action_type == "enroll_campaign" and action_config:
                    campaign_type = actions.get("campaign_type", "welcome_series")
                    campaign_id = await self._find_campaign_by_type(campaign_type)
                    if campaign_id:
                        await self.campaign_manager.enroll_lead(lead_id, campaign_id)
                
                elif action_type == "escalate" and action_config:
                    await self._trigger_event(EventType.ESCALATION_TRIGGERED, lead_id, {
                        "type": "workflow_rule",
                        "rule_triggered": True,
                        "data": data
                    })
                
                elif action_type == "notify_manager" and action_config:
                    await self._notify_manager(lead_id, data)
            
        except Exception as e:
            logger.error(f"Error executing rule actions: {e}")
    
    # API Methods (for external integration)
    
    async def create_lead(self, lead_data: LeadCreateRequest) -> WorkflowResponse:
        """Create a new lead and trigger workflow"""
        try:
            # Generate lead ID
            lead_id = f"lead_{int(datetime.utcnow().timestamp())}_{lead_data.email.split('@')[0]}"
            
            # Store lead in database
            await self._store_lead(lead_id, lead_data.dict())
            
            # Trigger workflow
            await self._trigger_event(EventType.LEAD_CREATED, lead_id, lead_data.dict())
            
            return WorkflowResponse(
                status="success",
                message="Lead created and workflow triggered",
                data={"lead_id": lead_id}
            )
            
        except Exception as e:
            logger.error(f"Error creating lead: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def update_lead(self, lead_id: str, update_data: LeadUpdateRequest) -> WorkflowResponse:
        """Update lead and trigger workflow if needed"""
        try:
            # Update lead in database
            update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
            await self._update_lead(lead_id, update_dict)
            
            # Trigger workflow
            await self._trigger_event(EventType.LEAD_UPDATED, lead_id, update_dict)
            
            return WorkflowResponse(
                status="success",
                message="Lead updated and workflow triggered",
                data={"lead_id": lead_id}
            )
            
        except Exception as e:
            logger.error(f"Error updating lead: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def override_score(self, lead_id: str, override_data: ScoreOverrideRequest) -> WorkflowResponse:
        """Request manual score override"""
        try:
            current_score = await self._get_current_score(lead_id)
            
            success = await self.hitl_system.manual_score_override(
                lead_id,
                {
                    "original_score": current_score,
                    "new_score": override_data.new_score
                },
                override_data.override_by,
                override_data.reason
            )
            
            return WorkflowResponse(
                status="success" if success else "error",
                message="Score override request submitted" if success else "Failed to submit override request",
                data={"lead_id": lead_id, "requested_score": override_data.new_score}
            )
            
        except Exception as e:
            logger.error(f"Error overriding score: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def override_assignment(self, lead_id: str, override_data: AssignmentOverrideRequest) -> WorkflowResponse:
        """Request manual assignment override"""
        try:
            success = await self.hitl_system.manual_assignment_override(
                lead_id,
                override_data.new_rep_id,
                override_data.override_by,
                override_data.reason
            )
            
            return WorkflowResponse(
                status="success" if success else "error",
                message="Assignment override request submitted" if success else "Failed to submit override request",
                data={"lead_id": lead_id, "new_rep_id": override_data.new_rep_id}
            )
            
        except Exception as e:
            logger.error(f"Error overriding assignment: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def enroll_in_campaign(self, lead_id: str, enrollment_data: CampaignEnrollmentRequest) -> WorkflowResponse:
        """Manually enroll lead in campaign"""
        try:
            enrollment = await self.campaign_manager.enroll_lead(
                lead_id,
                enrollment_data.campaign_id,
                enrollment_data.enrollment_data
            )
            
            if enrollment:
                await self._trigger_event(EventType.CAMPAIGN_ENROLLED, lead_id, {
                    "enrollment": {
                        "enrollment_id": enrollment.enrollment_id,
                        "campaign_id": enrollment_data.campaign_id
                    }
                })
                
                return WorkflowResponse(
                    status="success",
                    message="Lead enrolled in campaign",
                    data={"enrollment_id": enrollment.enrollment_id}
                )
            else:
                return WorkflowResponse(
                    status="error",
                    message="Failed to enroll lead in campaign"
                )
            
        except Exception as e:
            logger.error(f"Error enrolling in campaign: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_lead_status(self, lead_id: str) -> WorkflowResponse:
        """Get comprehensive lead status"""
        try:
            # Get lead data
            lead_data = await self._get_lead_data(lead_id)
            if not lead_data:
                raise HTTPException(status_code=404, detail="Lead not found")
            
            # Get scoring data
            scoring_data = await self.scoring_engine.get_lead_score(lead_id)
            
            # Get assignment data
            assignment_data = await self._get_lead_assignment(lead_id)
            
            # Get campaign enrollments
            campaigns = await self._get_lead_campaigns(lead_id)
            
            # Get HITL requests
            hitl_requests = await self._get_lead_hitl_requests(lead_id)
            
            return WorkflowResponse(
                status="success",
                message="Lead status retrieved",
                data={
                    "lead_data": lead_data,
                    "scoring": scoring_data.dict() if scoring_data else None,
                    "assignment": assignment_data,
                    "campaigns": campaigns,
                    "hitl_requests": hitl_requests
                }
            )
            
        except Exception as e:
            logger.error(f"Error getting lead status: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_workflow_analytics(self) -> WorkflowResponse:
        """Get workflow performance analytics"""
        try:
            analytics_data = {
                "performance_metrics": self.performance_metrics,
                "processing_stats": self.processing_stats,
                "system_status": self.status.value,
                "component_status": {
                    "scoring_engine": "active",
                    "assignment_system": "active", 
                    "campaign_manager": "active",
                    "integration_manager": "active",
                    "hitl_system": "active"
                },
                "queue_status": {
                    "pending_events": self.event_queue.qsize(),
                    "active_workers": 3
                }
            }
            
            # Get component-specific analytics
            assignment_analytics = await self.assignment_system.get_assignment_analytics()
            scoring_metrics = await self.scoring_engine.get_scoring_metrics()
            quality_dashboard = await self.hitl_system.get_quality_dashboard()
            integration_status = await self.integration_manager.get_integration_status()
            
            analytics_data.update({
                "assignment_analytics": assignment_analytics,
                "scoring_metrics": scoring_metrics,
                "quality_dashboard": quality_dashboard,
                "integration_status": integration_status
            })
            
            return WorkflowResponse(
                status="success",
                message="Workflow analytics retrieved",
                data=analytics_data
            )
            
        except Exception as e:
            logger.error(f"Error getting workflow analytics: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # Utility methods
    
    async def _trigger_event(self, event_type: EventType, entity_id: str, 
                           event_data: Dict[str, Any], priority: int = 5):
        """Trigger a workflow event"""
        try:
            event = WorkflowEvent(
                event_id=f"{event_type.value}_{entity_id}_{int(datetime.utcnow().timestamp())}",
                event_type=event_type,
                entity_id=entity_id,
                event_data=event_data,
                priority=priority
            )
            
            await self.event_queue.put(event)
            logger.info(f"Triggered event {event.event_id}")
            
        except Exception as e:
            logger.error(f"Error triggering event: {e}")
    
    async def _get_lead_data(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get lead data from database"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow("SELECT * FROM leads WHERE lead_id = $1", lead_id)
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting lead data: {e}")
            return None
    
    async def _store_lead(self, lead_id: str, lead_data: Dict[str, Any]):
        """Store lead in database"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO leads (
                        lead_id, email, company_name, company_size, industry, job_title,
                        location, budget, timeline, service_requirements, website_visits,
                        email_opens, content_downloads, referral_source, metadata, created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
                """,
                    lead_id, lead_data["email"], lead_data["company_name"],
                    lead_data.get("company_size"), lead_data.get("industry"),
                    lead_data.get("job_title"), lead_data.get("location"),
                    lead_data.get("budget"), lead_data.get("timeline"),
                    json.dumps(lead_data.get("service_requirements", [])),
                    lead_data.get("website_visits", 0), lead_data.get("email_opens", 0),
                    lead_data.get("content_downloads", 0), lead_data.get("referral_source"),
                    json.dumps(lead_data.get("metadata", {})), datetime.utcnow()
                )
        except Exception as e:
            logger.error(f"Error storing lead: {e}")
            raise
    
    async def _store_event_log(self, event: WorkflowEvent, success: bool, error_message: str = None):
        """Store event processing log"""
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO workflow_event_logs (
                        event_id, event_type, entity_id, event_data, success,
                        error_message, processing_time, created_at, processed_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                    event.event_id, event.event_type.value, event.entity_id,
                    json.dumps(event.event_data), success, error_message,
                    (event.processed_at - event.created_at).total_seconds() if event.processed_at else 0,
                    event.created_at, event.processed_at
                )
        except Exception as e:
            logger.error(f"Error storing event log: {e}")
    
    # Monitoring tasks
    
    async def _performance_monitor(self):
        """Monitor system performance"""
        while self.status == WorkflowStatus.ACTIVE:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes
                
                # Log performance metrics
                logger.info(f"Performance metrics: {self.performance_metrics}")
                logger.info(f"Processing stats: {self.processing_stats}")
                
                # Check queue health
                queue_size = self.event_queue.qsize()
                if queue_size > 100:
                    logger.warning(f"Event queue size high: {queue_size}")
                
                # Check error rates
                total_events = self.processing_stats["total_events"]
                if total_events > 0:
                    error_rate = self.processing_stats["failed_events"] / total_events
                    if error_rate > 0.1:  # 10% error rate threshold
                        logger.warning(f"High error rate detected: {error_rate:.2%}")
                
            except Exception as e:
                logger.error(f"Error in performance monitor: {e}")
                await asyncio.sleep(60)
    
    async def _health_checker(self):
        """Check component health"""
        while self.status == WorkflowStatus.ACTIVE:
            try:
                await asyncio.sleep(600)  # Check every 10 minutes
                
                # Check database connection
                async with self.db_pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")
                
                # Check Redis connection
                await self.redis.ping()
                
                # Check component health
                # This would include health checks for all components
                
                logger.info("Health check passed")
                
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                self.status = WorkflowStatus.ERROR
                await asyncio.sleep(60)
    
    async def cleanup(self):
        """Cleanup orchestrator resources"""
        try:
            self.status = WorkflowStatus.MAINTENANCE
            
            # Wait for event queue to empty
            await self.event_queue.join()
            
            # Cleanup components
            if self.scoring_engine:
                await self.scoring_engine.cleanup()
            if self.assignment_system:
                await self.assignment_system.cleanup()
            if self.campaign_manager:
                await self.campaign_manager.cleanup()
            if self.integration_manager:
                await self.integration_manager.cleanup()
            if self.hitl_system:
                await self.hitl_system.cleanup()
            
            # Close connections
            if hasattr(self, 'db_pool'):
                await self.db_pool.close()
            if hasattr(self, 'redis'):
                await self.redis.close()
            
            logger.info("Lead workflow orchestrator cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# FastAPI application
def create_app(config: Dict[str, Any]) -> FastAPI:
    """Create FastAPI application with workflow orchestrator"""
    
    app = FastAPI(
        title="Lead Management Workflow API",
        description="Comprehensive lead management workflow with AI-powered scoring and automation",
        version="1.0.0"
    )
    
    # Initialize orchestrator
    orchestrator = LeadWorkflowOrchestrator(config)
    
    @app.on_event("startup")
    async def startup_event():
        await orchestrator.initialize()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        await orchestrator.cleanup()
    
    # API Routes
    
    @app.post("/leads", response_model=WorkflowResponse)
    async def create_lead(lead_data: LeadCreateRequest):
        return await orchestrator.create_lead(lead_data)
    
    @app.put("/leads/{lead_id}", response_model=WorkflowResponse)
    async def update_lead(lead_id: str, update_data: LeadUpdateRequest):
        return await orchestrator.update_lead(lead_id, update_data)
    
    @app.get("/leads/{lead_id}/status", response_model=WorkflowResponse)
    async def get_lead_status(lead_id: str):
        return await orchestrator.get_lead_status(lead_id)
    
    @app.post("/leads/{lead_id}/score-override", response_model=WorkflowResponse)
    async def override_score(lead_id: str, override_data: ScoreOverrideRequest):
        return await orchestrator.override_score(lead_id, override_data)
    
    @app.post("/leads/{lead_id}/assignment-override", response_model=WorkflowResponse)
    async def override_assignment(lead_id: str, override_data: AssignmentOverrideRequest):
        return await orchestrator.override_assignment(lead_id, override_data)
    
    @app.post("/leads/{lead_id}/enroll-campaign", response_model=WorkflowResponse)
    async def enroll_in_campaign(lead_id: str, enrollment_data: CampaignEnrollmentRequest):
        return await orchestrator.enroll_in_campaign(lead_id, enrollment_data)
    
    @app.get("/analytics", response_model=WorkflowResponse)
    async def get_workflow_analytics():
        return await orchestrator.get_workflow_analytics()
    
    @app.get("/health")
    async def health_check():
        return {
            "status": orchestrator.status.value,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    return app

# Example configuration and startup
if __name__ == "__main__":
    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "database": "bizosaas",
            "user": "postgres",
            "password": "password"
        },
        "redis": {
            "host": "localhost",
            "port": 6379
        },
        "openai_api_key": "your-openai-api-key"
    }
    
    app = create_app(config)
    uvicorn.run(app, host="0.0.0.0", port=8000)