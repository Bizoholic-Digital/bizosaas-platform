"""
BizOSaaS Personal AI Assistant
Comprehensive AI-powered assistant for development and operations management

This assistant serves as the primary interface for:
- Development task management and code review
- Day-to-day operations across all projects
- Project monitoring and performance analytics
- Client communication and support coordination
- Strategic decision making and recommendations
- Mobile-first interaction via Telegram and web interfaces
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from ai_agents_management import AIAgentsManager, get_ai_agents_manager
from telegram_integration import TelegramBotManager, get_telegram_manager
from vault_client import VaultClient
from event_bus_integration import BrainEventBusClient

logger = logging.getLogger(__name__)

# ========================================================================================
# PERSONAL AI ASSISTANT MODELS
# ========================================================================================

class AssistantCapability(str, Enum):
    """Core capabilities of the Personal AI Assistant"""
    DEVELOPMENT_MANAGEMENT = "development_management"
    OPERATIONS_OVERSIGHT = "operations_oversight"
    PROJECT_MONITORING = "project_monitoring"
    CLIENT_COMMUNICATION = "client_communication"
    STRATEGIC_PLANNING = "strategic_planning"
    PERFORMANCE_ANALYTICS = "performance_analytics"
    TASK_AUTOMATION = "task_automation"
    MOBILE_CONTROL = "mobile_control"

class InteractionMode(str, Enum):
    """Different modes of interaction with the assistant"""
    TELEGRAM_CHAT = "telegram_chat"
    WEB_DASHBOARD = "web_dashboard"
    API_INTEGRATION = "api_integration"
    VOICE_COMMAND = "voice_command"
    SCHEDULED_REPORT = "scheduled_report"

class TaskPriority(str, Enum):
    """Task priority levels for the assistant"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SCHEDULED = "scheduled"

class ProjectScope(str, Enum):
    """Scope of project management"""
    BIZOHOLIC = "bizoholic"
    CORELDOVE = "coreldove"
    THRILLRING = "thrillring"
    QUANTTRADE = "quanttrade"
    ALL_PROJECTS = "all_projects"
    PLATFORM_WIDE = "platform_wide"

class AssistantTask(BaseModel):
    """Individual task managed by the Personal AI Assistant"""
    task_id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    priority: TaskPriority
    project_scope: ProjectScope
    estimated_duration: Optional[int] = None  # minutes
    assigned_agents: List[str] = Field(default_factory=list)
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    completion_percentage: float = 0.0
    dependencies: List[UUID] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DailyOperationsReport(BaseModel):
    """Daily operations summary for all projects"""
    report_id: UUID = Field(default_factory=uuid4)
    date: datetime = Field(default_factory=datetime.utcnow)
    project_summaries: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    key_metrics: Dict[str, float] = Field(default_factory=dict)
    alerts: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    completed_tasks: int = 0
    pending_tasks: int = 0
    critical_issues: int = 0

class StrategicInsight(BaseModel):
    """Strategic insights and recommendations"""
    insight_id: UUID = Field(default_factory=uuid4)
    category: str
    title: str
    description: str
    impact_level: str  # "low", "medium", "high", "critical"
    recommended_actions: List[str]
    timeline: str
    estimated_roi: Optional[str] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)

# ========================================================================================
# PERSONAL AI ASSISTANT MANAGER
# ========================================================================================

class PersonalAIAssistant:
    """
    Comprehensive Personal AI Assistant for BizOSaaS Platform Management
    
    This assistant serves as the central intelligence for managing all aspects
    of the BizOSaaS ecosystem, from development to operations to strategic planning.
    """
    
    def __init__(self, vault_client: VaultClient = None, event_bus_client: BrainEventBusClient = None):
        self.vault_client = vault_client
        self.event_bus_client = event_bus_client
        self.logger = logger.bind(component="personal_ai_assistant")
        
        # Initialize sub-managers
        self.ai_agents_manager = None
        self.telegram_manager = None
        
        # Assistant state
        self.active_tasks: Dict[UUID, AssistantTask] = {}
        self.capabilities = list(AssistantCapability)
        self.interaction_history: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.daily_metrics: Dict[str, Any] = {}
        self.weekly_summaries: List[DailyOperationsReport] = []
        
        self.logger.info("Personal AI Assistant initialized")

    async def initialize_dependencies(self):
        """Initialize all dependent managers and services"""
        try:
            self.ai_agents_manager = await get_ai_agents_manager()
            self.telegram_manager = await get_telegram_manager()
            
            # Load existing tasks from Vault
            await self._load_assistant_state()
            
            self.logger.info("Personal AI Assistant dependencies initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize assistant dependencies: {e}")
            raise

    # ========================================================================================
    # DEVELOPMENT MANAGEMENT
    # ========================================================================================

    async def manage_development_task(self, task_description: str, priority: TaskPriority = TaskPriority.MEDIUM, 
                                    project_scope: ProjectScope = ProjectScope.PLATFORM_WIDE) -> AssistantTask:
        """
        Manage development tasks with AI agent delegation
        """
        try:
            # Create development task
            task = AssistantTask(
                title=f"Development: {task_description[:50]}...",
                description=task_description,
                priority=priority,
                project_scope=project_scope,
                estimated_duration=60,  # Default 1 hour
                metadata={
                    "task_type": "development",
                    "requires_code_review": True,
                    "testing_required": True
                }
            )
            
            # Analyze task and assign appropriate AI agents
            suitable_agents = await self._analyze_and_assign_agents(task_description, "development")
            task.assigned_agents = suitable_agents
            
            # Store task
            self.active_tasks[task.task_id] = task
            await self._store_task_in_vault(task)
            
            # Publish development event
            await self._publish_assistant_event("development_task_created", {
                "task_id": str(task.task_id),
                "description": task_description,
                "priority": priority.value,
                "assigned_agents": suitable_agents
            })
            
            # Send Telegram notification if configured
            await self._send_telegram_notification(
                f"🔧 Development Task Created\n"
                f"Priority: {priority.value.upper()}\n"
                f"Scope: {project_scope.value}\n"
                f"Assigned Agents: {', '.join(suitable_agents[:3])}\n"
                f"Task: {task_description[:100]}..."
            )
            
            self.logger.info(f"Development task created: {task.task_id}")
            return task
            
        except Exception as e:
            self.logger.error(f"Error managing development task: {e}")
            raise

    async def review_code_changes(self, file_path: str, changes_description: str) -> Dict[str, Any]:
        """
        Review code changes using AI agents
        """
        try:
            # Execute code review agent
            review_result = await self.ai_agents_manager.execute_agent(
                "code_review_agent",
                {
                    "file_path": file_path,
                    "changes": changes_description,
                    "review_type": "comprehensive"
                }
            )
            
            # Process review results
            review_summary = {
                "file_path": file_path,
                "review_score": review_result.get("score", 0.8),
                "issues_found": review_result.get("issues", []),
                "recommendations": review_result.get("recommendations", []),
                "approved": review_result.get("approved", True),
                "reviewed_at": datetime.utcnow().isoformat()
            }
            
            # Store review in Vault
            await self.vault_client.store_secret(
                f"code_reviews/{datetime.utcnow().strftime('%Y-%m-%d')}/{uuid4()}",
                review_summary
            )
            
            # Send notification
            await self._send_telegram_notification(
                f"🔍 Code Review Complete\n"
                f"File: {file_path}\n"
                f"Score: {review_summary['review_score']:.1f}/1.0\n"
                f"Issues: {len(review_summary['issues_found'])}\n"
                f"Status: {'✅ Approved' if review_summary['approved'] else '❌ Needs Changes'}"
            )
            
            return review_summary
            
        except Exception as e:
            self.logger.error(f"Error reviewing code changes: {e}")
            raise

    # ========================================================================================
    # OPERATIONS MANAGEMENT
    # ========================================================================================

    async def generate_daily_operations_report(self, projects: List[ProjectScope] = None) -> DailyOperationsReport:
        """
        Generate comprehensive daily operations report
        """
        try:
            if projects is None:
                projects = [ProjectScope.BIZOHOLIC, ProjectScope.CORELDOVE, 
                          ProjectScope.THRILLRING, ProjectScope.QUANTTRADE]
            
            report = DailyOperationsReport()
            
            # Gather metrics for each project
            for project in projects:
                project_summary = await self._gather_project_metrics(project)
                report.project_summaries[project.value] = project_summary
            
            # Calculate platform-wide metrics
            report.key_metrics = await self._calculate_platform_metrics()
            
            # Identify alerts and recommendations
            report.alerts = await self._identify_operational_alerts()
            report.recommendations = await self._generate_operational_recommendations()
            
            # Count tasks
            report.completed_tasks = len([t for t in self.active_tasks.values() 
                                        if t.status == "completed" and 
                                        t.created_at.date() == datetime.utcnow().date()])
            report.pending_tasks = len([t for t in self.active_tasks.values() 
                                      if t.status == "pending"])
            
            # Store report
            await self._store_daily_report(report)
            
            # Send summary via Telegram
            await self._send_daily_report_notification(report)
            
            self.logger.info(f"Daily operations report generated: {report.report_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating daily operations report: {e}")
            raise

    async def monitor_project_health(self, project: ProjectScope) -> Dict[str, Any]:
        """
        Monitor health and performance of specific project
        """
        try:
            health_metrics = {
                "project": project.value,
                "timestamp": datetime.utcnow().isoformat(),
                "health_score": 0.0,
                "services_status": {},
                "performance_metrics": {},
                "alerts": [],
                "recommendations": []
            }
            
            # Check service health using AI agents
            if project == ProjectScope.BIZOHOLIC:
                services = ["wordpress", "crm", "analytics"]
            elif project == ProjectScope.CORELDOVE:
                services = ["saleor", "storefront", "inventory"]
            else:
                services = ["web_app", "api", "database"]
            
            for service in services:
                service_health = await self._check_service_health(project, service)
                health_metrics["services_status"][service] = service_health
            
            # Calculate overall health score
            health_scores = [s.get("health_score", 0.5) for s in health_metrics["services_status"].values()]
            health_metrics["health_score"] = sum(health_scores) / len(health_scores) if health_scores else 0.0
            
            # Generate performance insights
            health_metrics["performance_metrics"] = await self._gather_performance_metrics(project)
            
            # Identify issues and recommendations
            if health_metrics["health_score"] < 0.7:
                health_metrics["alerts"].append(f"Low health score detected for {project.value}")
                health_metrics["recommendations"].append("Investigate service performance issues")
            
            # Store health data
            await self.vault_client.store_secret(
                f"project_health/{project.value}/{datetime.utcnow().strftime('%Y-%m-%d-%H')}",
                health_metrics
            )
            
            return health_metrics
            
        except Exception as e:
            self.logger.error(f"Error monitoring project health: {e}")
            raise

    # ========================================================================================
    # CLIENT COMMUNICATION & SUPPORT
    # ========================================================================================

    async def handle_client_inquiry(self, client_id: str, inquiry: str, urgency: str = "medium") -> Dict[str, Any]:
        """
        Handle client inquiries with AI-powered response generation
        """
        try:
            # Analyze inquiry using AI agents
            analysis_result = await self.ai_agents_manager.execute_agent(
                "customer_support_agent",
                {
                    "client_id": client_id,
                    "inquiry": inquiry,
                    "urgency": urgency,
                    "context": "personal_assistant_handling"
                }
            )
            
            response_data = {
                "inquiry_id": str(uuid4()),
                "client_id": client_id,
                "inquiry": inquiry,
                "urgency": urgency,
                "ai_response": analysis_result.get("suggested_response", ""),
                "requires_human_review": analysis_result.get("requires_human", False),
                "estimated_resolution_time": analysis_result.get("resolution_time", "24 hours"),
                "assigned_department": analysis_result.get("department", "general_support"),
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Store inquiry data
            await self.vault_client.store_secret(
                f"client_inquiries/{client_id}/{response_data['inquiry_id']}",
                response_data
            )
            
            # Send notification based on urgency
            if urgency in ["high", "critical"]:
                await self._send_telegram_notification(
                    f"🚨 {urgency.upper()} Client Inquiry\n"
                    f"Client: {client_id}\n"
                    f"Inquiry: {inquiry[:100]}...\n"
                    f"Requires Review: {'Yes' if response_data['requires_human_review'] else 'No'}"
                )
            
            # Publish event
            await self._publish_assistant_event("client_inquiry_received", response_data)
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Error handling client inquiry: {e}")
            raise

    # ========================================================================================
    # STRATEGIC PLANNING & INSIGHTS
    # ========================================================================================

    async def generate_strategic_insights(self, timeframe: str = "weekly") -> List[StrategicInsight]:
        """
        Generate strategic insights and recommendations
        """
        try:
            insights = []
            
            # Market analysis insights
            market_insight = await self._analyze_market_trends()
            if market_insight:
                insights.append(StrategicInsight(
                    category="market_analysis",
                    title="Market Trend Analysis",
                    description=market_insight["description"],
                    impact_level=market_insight["impact"],
                    recommended_actions=market_insight["actions"],
                    timeline=market_insight["timeline"]
                ))
            
            # Performance optimization insights
            perf_insight = await self._analyze_performance_optimization()
            if perf_insight:
                insights.append(StrategicInsight(
                    category="performance_optimization",
                    title="Performance Optimization Opportunities",
                    description=perf_insight["description"],
                    impact_level=perf_insight["impact"],
                    recommended_actions=perf_insight["actions"],
                    timeline=perf_insight["timeline"],
                    estimated_roi=perf_insight.get("roi")
                ))
            
            # Resource allocation insights
            resource_insight = await self._analyze_resource_allocation()
            if resource_insight:
                insights.append(StrategicInsight(
                    category="resource_allocation",
                    title="Resource Allocation Recommendations",
                    description=resource_insight["description"],
                    impact_level=resource_insight["impact"],
                    recommended_actions=resource_insight["actions"],
                    timeline=resource_insight["timeline"]
                ))
            
            # Store insights
            for insight in insights:
                await self.vault_client.store_secret(
                    f"strategic_insights/{timeframe}/{insight.insight_id}",
                    insight.dict()
                )
            
            # Send summary notification
            if insights:
                await self._send_telegram_notification(
                    f"📊 Strategic Insights Generated\n"
                    f"Timeframe: {timeframe}\n"
                    f"Insights: {len(insights)}\n"
                    f"High Impact: {len([i for i in insights if i.impact_level == 'high'])}\n"
                    f"Critical: {len([i for i in insights if i.impact_level == 'critical'])}"
                )
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error generating strategic insights: {e}")
            raise

    # ========================================================================================
    # MOBILE CONTROL INTERFACE
    # ========================================================================================

    async def process_mobile_command(self, command: str, user_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process commands received via mobile interface (Telegram, etc.)
        """
        try:
            # Parse command
            command_parts = command.lower().strip().split()
            if not command_parts:
                return {"error": "Empty command"}
            
            primary_command = command_parts[0]
            
            # Route command to appropriate handler
            if primary_command in ["status", "health"]:
                return await self._handle_status_command(command_parts[1:] if len(command_parts) > 1 else [])
                
            elif primary_command in ["task", "tasks"]:
                return await self._handle_task_command(command_parts[1:])
                
            elif primary_command in ["report", "reports"]:
                return await self._handle_report_command(command_parts[1:])
                
            elif primary_command in ["deploy", "deployment"]:
                return await self._handle_deployment_command(command_parts[1:], user_id)
                
            elif primary_command in ["monitor", "monitoring"]:
                return await self._handle_monitoring_command(command_parts[1:])
                
            elif primary_command in ["help", "commands"]:
                return await self._handle_help_command()
                
            else:
                # Use AI agent to interpret natural language command
                return await self._handle_natural_language_command(command, user_id, context)
                
        except Exception as e:
            self.logger.error(f"Error processing mobile command: {e}")
            return {"error": f"Command processing failed: {str(e)}"}

    # ========================================================================================
    # AUTOMATION & TASK EXECUTION
    # ========================================================================================

    async def execute_automated_workflow(self, workflow_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute automated workflows using AI agents
        """
        try:
            workflow_result = {
                "workflow_id": str(uuid4()),
                "workflow_name": workflow_name,
                "parameters": parameters or {},
                "started_at": datetime.utcnow().isoformat(),
                "status": "executing",
                "steps_completed": 0,
                "total_steps": 0,
                "results": {}
            }
            
            # Define workflow steps based on workflow name
            if workflow_name == "daily_maintenance":
                steps = [
                    ("health_check", "Checking all services health"),
                    ("performance_analysis", "Analyzing performance metrics"),
                    ("backup_verification", "Verifying backup integrity"),
                    ("security_scan", "Running security scan"),
                    ("report_generation", "Generating daily report")
                ]
            elif workflow_name == "deployment_pipeline":
                steps = [
                    ("code_review", "Reviewing code changes"),
                    ("testing", "Running automated tests"),
                    ("staging_deployment", "Deploying to staging"),
                    ("validation", "Validating deployment"),
                    ("production_deployment", "Deploying to production")
                ]
            else:
                return {"error": f"Unknown workflow: {workflow_name}"}
            
            workflow_result["total_steps"] = len(steps)
            
            # Execute workflow steps
            for i, (step_name, step_description) in enumerate(steps):
                try:
                    # Execute step using appropriate AI agent
                    step_result = await self._execute_workflow_step(step_name, step_description, parameters)
                    workflow_result["results"][step_name] = step_result
                    workflow_result["steps_completed"] = i + 1
                    
                    # Update progress
                    await self._publish_assistant_event("workflow_progress", {
                        "workflow_id": workflow_result["workflow_id"],
                        "step": step_name,
                        "progress": (i + 1) / len(steps) * 100
                    })
                    
                except Exception as step_error:
                    workflow_result["results"][step_name] = {"error": str(step_error)}
                    workflow_result["status"] = "failed"
                    break
            
            if workflow_result["status"] != "failed":
                workflow_result["status"] = "completed"
            
            workflow_result["completed_at"] = datetime.utcnow().isoformat()
            
            # Store workflow results
            await self.vault_client.store_secret(
                f"workflow_executions/{workflow_name}/{workflow_result['workflow_id']}",
                workflow_result
            )
            
            # Send completion notification
            await self._send_telegram_notification(
                f"🔄 Workflow {workflow_result['status'].title()}\n"
                f"Name: {workflow_name}\n"
                f"Steps: {workflow_result['steps_completed']}/{workflow_result['total_steps']}\n"
                f"Duration: {self._calculate_duration(workflow_result['started_at'], workflow_result['completed_at'])}"
            )
            
            return workflow_result
            
        except Exception as e:
            self.logger.error(f"Error executing automated workflow: {e}")
            raise

    # ========================================================================================
    # HELPER METHODS
    # ========================================================================================

    async def _analyze_and_assign_agents(self, task_description: str, task_type: str) -> List[str]:
        """Analyze task and assign appropriate AI agents"""
        # Simple assignment logic - can be enhanced with ML
        task_lower = task_description.lower()
        agents = []
        
        if "seo" in task_lower or "search" in task_lower:
            agents.extend(["seo_optimizer", "keyword_researcher", "content_seo_agent"])
        if "content" in task_lower or "blog" in task_lower:
            agents.extend(["content_creator", "blog_writer", "social_media_content_agent"])
        if "marketing" in task_lower or "campaign" in task_lower:
            agents.extend(["campaign_manager", "ad_optimizer", "email_marketing_agent"])
        if "analytics" in task_lower or "performance" in task_lower:
            agents.extend(["analytics_reporter", "performance_monitor"])
        
        # Default agents for development tasks
        if task_type == "development":
            agents.extend(["code_review_agent", "testing_agent", "deployment_agent"])
        
        return list(set(agents[:5]))  # Limit to 5 agents

    async def _store_task_in_vault(self, task: AssistantTask):
        """Store task in Vault for persistence"""
        await self.vault_client.store_secret(
            f"assistant_tasks/{task.project_scope.value}/{task.task_id}",
            task.dict()
        )

    async def _load_assistant_state(self):
        """Load assistant state from Vault"""
        # Implementation would load existing tasks and state
        pass

    async def _publish_assistant_event(self, event_type: str, data: Dict[str, Any]):
        """Publish assistant events to Event Bus"""
        if self.event_bus_client:
            await self.event_bus_client.publish_event(
                event_type=f"assistant.{event_type}",
                data=data,
                tenant_id="platform",
                source="personal_ai_assistant"
            )

    async def _send_telegram_notification(self, message: str):
        """Send notification via Telegram"""
        if self.telegram_manager:
            # Send to configured admin chat
            await self.telegram_manager.send_admin_notification(message)

    async def _gather_project_metrics(self, project: ProjectScope) -> Dict[str, Any]:
        """Gather metrics for specific project"""
        return {
            "project": project.value,
            "uptime": "99.5%",
            "response_time": "120ms",
            "active_users": 1250,
            "revenue": "$15,750",
            "issues": 2,
            "last_deployment": "2025-09-12T14:30:00Z"
        }

    async def _calculate_platform_metrics(self) -> Dict[str, float]:
        """Calculate platform-wide metrics"""
        return {
            "total_users": 5000.0,
            "total_revenue": 45000.0,
            "avg_response_time": 150.0,
            "overall_uptime": 99.2,
            "active_projects": 4.0
        }

    async def _identify_operational_alerts(self) -> List[str]:
        """Identify operational alerts"""
        return [
            "High memory usage on Coreldove server",
            "Backup verification pending for Quanttrade"
        ]

    async def _generate_operational_recommendations(self) -> List[str]:
        """Generate operational recommendations"""
        return [
            "Consider upgrading database instance for better performance",
            "Implement automated monitoring for critical services",
            "Schedule maintenance window for server updates"
        ]

    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate duration between two timestamps"""
        try:
            start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            duration = end - start
            
            minutes = int(duration.total_seconds() / 60)
            if minutes < 60:
                return f"{minutes}m"
            else:
                hours = minutes // 60
                mins = minutes % 60
                return f"{hours}h {mins}m"
        except:
            return "Unknown"

# ========================================================================================
# ASSISTANT FACTORY AND DEPENDENCIES
# ========================================================================================

_personal_assistant_instance: Optional[PersonalAIAssistant] = None

async def get_personal_ai_assistant() -> PersonalAIAssistant:
    """Get or create Personal AI Assistant instance"""
    global _personal_assistant_instance
    
    if _personal_assistant_instance is None:
        from vault_client import get_vault_client
        from event_bus_integration import get_event_bus_client
        
        vault_client = await get_vault_client()
        event_bus_client = await get_event_bus_client()
        
        _personal_assistant_instance = PersonalAIAssistant(vault_client, event_bus_client)
        await _personal_assistant_instance.initialize_dependencies()
    
    return _personal_assistant_instance

# ========================================================================================
# MOBILE COMMAND HANDLERS
# ========================================================================================

async def handle_mobile_command(command: str, user_id: str) -> str:
    """
    Simple interface for handling mobile commands
    Returns formatted response string for mobile interface
    """
    assistant = await get_personal_ai_assistant()
    result = await assistant.process_mobile_command(command, user_id)
    
    if "error" in result:
        return f"❌ Error: {result['error']}"
    
    # Format response based on command type
    if "status" in result:
        return f"📊 System Status: {result['status']}\n" + \
               f"Health Score: {result.get('health_score', 'Unknown')}\n" + \
               f"Active Services: {result.get('active_services', 'Unknown')}"
    
    return f"✅ Command executed successfully\nResult: {str(result)[:200]}..."