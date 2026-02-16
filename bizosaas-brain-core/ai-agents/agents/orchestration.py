"""
Centralized Orchestration for BizOSaas Core
Advanced orchestration engine for multi-agent workflows and business processes
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Type
from enum import Enum
import logging

from crewai import Agent, Task, Crew, Process

from .base_agent import BaseAgent, AgentRole, AgentTaskRequest, AgentTaskResponse
from .marketing_agents import *
from .ecommerce_agents import *
from .analytics_agents import *
from .operations_agents import *
from .workflow_crews import *
from .crm_agents import *
from .impact_analysis_agent import ImpactAnalysisAgent
from .documentation_agent import DocumentationAgent

logger = logging.getLogger(__name__)

class OrchestrationMode(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    ADAPTIVE = "adaptive"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class WorkflowDefinition:
    """Defines a complete business workflow with agents, tasks, and dependencies"""
    
    def __init__(
        self,
        workflow_id: str,
        name: str,
        description: str,
        agent_sequence: List[str],
        orchestration_mode: OrchestrationMode = OrchestrationMode.SEQUENTIAL,
        priority: WorkflowPriority = WorkflowPriority.MEDIUM,
        timeout_minutes: int = 60,
        retry_attempts: int = 3
    ):
        self.workflow_id = workflow_id
        self.name = name
        self.description = description
        self.agent_sequence = agent_sequence
        self.orchestration_mode = orchestration_mode
        self.priority = priority
        self.timeout_minutes = timeout_minutes
        self.retry_attempts = retry_attempts
        self.created_at = datetime.now(timezone.utc)

class WorkflowExecution:
    """Tracks the execution of a workflow instance"""
    
    def __init__(self, workflow_def: WorkflowDefinition, tenant_id: str, user_id: str):
        self.execution_id = str(uuid.uuid4())
        self.workflow_def = workflow_def
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.status = WorkflowStatus.PENDING
        self.started_at = None
        self.completed_at = None
        self.current_step = 0
        self.results = {}
        self.errors = []
        self.performance_metrics = {
            "total_duration": 0,
            "agent_durations": {},
            "success_rate": 0
        }

class HierarchicalCrewOrchestrator:
    """Advanced orchestrator for hierarchical multi-agent workflows"""
    
    def __init__(self):
        self.agent_registry = {}
        self.workflow_definitions = {}
        self.active_executions = {}
        self._initialize_agents()
        self._initialize_workflows()
    
    def _initialize_agents(self):
        """Initialize all available agents in the registry"""
        agent_classes = [
            # Marketing Agents
            MarketingStrategistAgent, ContentCreatorAgent, SEOSpecialistAgent,
            SocialMediaSpecialistAgent, EmailMarketingAgent, PaidAdvertisingAgent,
            InfluencerMarketingAgent, MarketingAutomationAgent, BrandingSpecialistAgent,
            
            # E-commerce Agents
            ProductSourcingAgent, EcommerceAgent, PriceOptimizationAgent,
            InventoryManagementAgent, SupplierRelationsAgent, FraudDetectionAgent,
            CustomerSegmentationAgent, SalesForecastingAgent, ASOAgent,
            AmazonOptimizationAgent, EcommercePlatformIntegrationAgent,
            ReviewManagementAgent, ConversionRateOptimizationAgent,
            
            # Analytics Agents
            DigitalPresenceAuditAgent, PerformanceAnalyticsAgent, ReportGeneratorAgent,
            DataVisualizationAgent, ROIAnalysisAgent, TrendAnalysisAgent,
            InsightSynthesisAgent, PredictiveAnalyticsAgent,
            
            # Operations Agents
            CustomerSupportAgent, ComplianceAuditAgent, WorkflowOptimizationAgent,
            ResourcePlanningAgent, QualityAssuranceAgent, IncidentManagementAgent,
            KnowledgeManagementAgent, ProcessAutomationAgent,
            
            # Advanced CRM Agents
            ContactIntelligenceAgent, LeadScoringAgent, SalesAssistantAgent,
            SentimentAnalysisAgent, EscalationPredictorAgent, PersonalizationAgent,
            PipelineManagementAgent,
            
            # Workflow Crews
            DigitalAuditCrew, CampaignLaunchCrew, ProductLaunchCrew,
            CompetitorAnalysisCrew, MarketResearchCrew, ContentStrategyCrew,
            ReputationManagementCrew, LeadQualificationCrew,
            ImpactAnalysisAgent,
            DocumentationAgent
        ]
        
        for agent_class in agent_classes:
            try:
                agent_instance = agent_class()
                self.agent_registry[agent_instance.agent_name] = agent_instance
                logger.info(f"Registered agent: {agent_instance.agent_name}")
            except Exception as e:
                logger.error(f"Failed to initialize agent {agent_class.__name__}: {e}")
    
    def _initialize_workflows(self):
        """Initialize predefined workflow definitions"""
        self.workflow_definitions = {
            "comprehensive_digital_audit": WorkflowDefinition(
                workflow_id="comprehensive_digital_audit",
                name="Comprehensive Digital Audit",
                description="Complete digital presence analysis with actionable recommendations",
                agent_sequence=[
                    "digital_audit_crew",
                    "performance_analytics_specialist",
                    "report_generator_specialist"
                ],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.HIGH,
                timeout_minutes=120
            ),
            "product_launch_campaign": WorkflowDefinition(
                workflow_id="product_launch_campaign",
                name="Product Launch Campaign",
                description="End-to-end product launch with marketing and e-commerce optimization",
                agent_sequence=[
                    "product_sourcing_specialist",
                    "marketing_strategist",
                    "content_creator",
                    "campaign_launch_crew"
                ],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.HIGH,
                timeout_minutes=180
            ),
            "competitor_intelligence": WorkflowDefinition(
                workflow_id="competitor_intelligence",
                name="Competitor Intelligence Analysis",
                description="Comprehensive competitive analysis and positioning recommendations",
                agent_sequence=[
                    "competitor_analysis_crew",
                    "market_research_crew",
                    "insight_synthesis_specialist"
                ],
                orchestration_mode=OrchestrationMode.PARALLEL,
                priority=WorkflowPriority.MEDIUM,
                timeout_minutes=90
            ),
            "customer_journey_optimization": WorkflowDefinition(
                workflow_id="customer_journey_optimization",
                name="Customer Journey Optimization",
                description="Optimize complete customer journey from awareness to conversion",
                agent_sequence=[
                    "customer_segmentation_specialist",
                    "conversion_optimization_specialist",
                    "email_marketing_specialist",
                    "performance_analytics_specialist"
                ],
                orchestration_mode=OrchestrationMode.HIERARCHICAL,
                priority=WorkflowPriority.HIGH,
                timeout_minutes=150
            ),
            "impact_analysis": WorkflowDefinition(
                workflow_id="impact_analysis",
                name="Impact Analysis workflow",
                description="Monitors and predicts impact of marketing configurations",
                agent_sequence=["impact_analysis"],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.MEDIUM,
                timeout_minutes=30
            ),
            "amazon_product_sourcing": WorkflowDefinition(
                workflow_id="amazon_product_sourcing",
                name="Amazon Product Sourcing",
                description="Intelligent discovery and validation of products on Amazon",
                agent_sequence=[
                    "product_sourcing_specialist",
                    "amazon_optimization_specialist",
                    "price_optimization_specialist"
                ],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.HIGH,
                timeout_minutes=90
            ),
            "ecommerce_listing_optimization": WorkflowDefinition(
                workflow_id="ecommerce_listing_optimization",
                name="E-commerce Listing & SEO",
                description="Automated high-converting, search-ready product listings",
                agent_sequence=[
                    "content_creator",
                    "seo_specialist",
                    "ecommerce_specialist"
                ],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.MEDIUM,
                timeout_minutes=60
            ),
            "automated_order_fulfillment": WorkflowDefinition(
                workflow_id="automated_order_fulfillment",
                name="Automated Order Fulfillment",
                description="End-to-end order processing, fraud detection, and inventory sync",
                agent_sequence=[
                    "fraud_detection_specialist",
                    "ecommerce_specialist",
                    "inventory_management_specialist"
                ],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.HIGH,
                timeout_minutes=45
            ),
            "campaign_launch": WorkflowDefinition(
                workflow_id="campaign_launch",
                name="Multi-Channel Campaign Launch",
                description="Comprehensive marketing campaign creation and launch",
                agent_sequence=["campaign_launch_crew"],
                orchestration_mode=OrchestrationMode.SEQUENTIAL,
                priority=WorkflowPriority.HIGH,
                timeout_minutes=60
            )
        }
    
    async def execute_workflow(
        self,
        workflow_id: str,
        input_data: Dict[str, Any],
        tenant_id: str,
        user_id: str,
        custom_agents: Optional[List[str]] = None
    ) -> WorkflowExecution:
        """Execute a complete business workflow"""
        
        # Get workflow definition
        if workflow_id not in self.workflow_definitions:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow_def = self.workflow_definitions[workflow_id]
        
        # Override agent sequence if custom agents provided
        if custom_agents:
            workflow_def.agent_sequence = custom_agents
        
        # Create workflow execution
        execution = WorkflowExecution(workflow_def, tenant_id, user_id)
        execution.status = WorkflowStatus.RUNNING
        execution.started_at = datetime.now(timezone.utc)
        
        self.active_executions[execution.execution_id] = execution
        
        try:
            # Execute workflow based on orchestration mode
            if workflow_def.orchestration_mode == OrchestrationMode.SEQUENTIAL:
                await self._execute_sequential(execution, input_data)
            elif workflow_def.orchestration_mode == OrchestrationMode.PARALLEL:
                await self._execute_parallel(execution, input_data)
            elif workflow_def.orchestration_mode == OrchestrationMode.HIERARCHICAL:
                await self._execute_hierarchical(execution, input_data)
            else:
                await self._execute_adaptive(execution, input_data)
            
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.now(timezone.utc)
            execution.performance_metrics["total_duration"] = (
                execution.completed_at - execution.started_at
            ).total_seconds()
            
            logger.info(f"Workflow {workflow_id} completed successfully")
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.errors.append(str(e))
            execution.completed_at = datetime.now(timezone.utc)
            logger.error(f"Workflow {workflow_id} failed: {e}")
        
        return execution
    
    async def _execute_sequential(self, execution: WorkflowExecution, input_data: Dict[str, Any]):
        """Execute agents sequentially, passing results between agents"""
        current_data = input_data.copy()
        
        for i, agent_name in enumerate(execution.workflow_def.agent_sequence):
            if agent_name not in self.agent_registry:
                raise ValueError(f"Agent {agent_name} not found in registry")
            
            agent = self.agent_registry[agent_name]
            execution.current_step = i
            
            # Create task request
            task_request = AgentTaskRequest(
                tenant_id=execution.tenant_id,
                user_id=execution.user_id,
                task_type="workflow_execution",
                input_data=current_data,
                context={
                    "workflow_id": execution.workflow_def.workflow_id,
                    "execution_id": execution.execution_id,
                    "step": i,
                    "previous_results": execution.results
                }
            )
            
            # Execute agent task
            start_time = datetime.now(timezone.utc)
            result = await agent.execute_task(task_request)
            end_time = datetime.now(timezone.utc)
            
            # Store results and metrics
            execution.results[agent_name] = result.result
            execution.performance_metrics["agent_durations"][agent_name] = (
                end_time - start_time
            ).total_seconds()
            
            # Pass results to next agent
            if result.status == "completed":
                current_data.update(result.result)
            else:
                raise Exception(f"Agent {agent_name} failed: {result.error}")
    
    async def _execute_parallel(self, execution: WorkflowExecution, input_data: Dict[str, Any]):
        """Execute agents in parallel and aggregate results"""
        tasks = []
        
        for agent_name in execution.workflow_def.agent_sequence:
            if agent_name not in self.agent_registry:
                raise ValueError(f"Agent {agent_name} not found in registry")
            
            agent = self.agent_registry[agent_name]
            
            task_request = AgentTaskRequest(
                tenant_id=execution.tenant_id,
                user_id=execution.user_id,
                task_type="workflow_execution",
                input_data=input_data,
                context={
                    "workflow_id": execution.workflow_def.workflow_id,
                    "execution_id": execution.execution_id,
                    "mode": "parallel"
                }
            )
            
            tasks.append(agent.execute_task(task_request))
        
        # Execute all agents concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, (agent_name, result) in enumerate(zip(execution.workflow_def.agent_sequence, results)):
            if isinstance(result, Exception):
                raise result
            
            execution.results[agent_name] = result.result
    
    async def _execute_hierarchical(self, execution: WorkflowExecution, input_data: Dict[str, Any]):
        """Execute agents in hierarchical order with dependency resolution"""
        # For now, implement as sequential with enhanced coordination
        await self._execute_sequential(execution, input_data)
    
    async def _execute_adaptive(self, execution: WorkflowExecution, input_data: Dict[str, Any]):
        """Execute agents with adaptive routing based on results"""
        # For now, implement as sequential with basic adaptation
        await self._execute_sequential(execution, input_data)
    
    def get_workflow_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get the current status of a workflow execution"""
        return self.active_executions.get(execution_id)
    
    def list_available_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflow definitions"""
        return [
            {
                "workflow_id": wf.workflow_id,
                "name": wf.name,
                "description": wf.description,
                "agents": wf.agent_sequence,
                "mode": wf.orchestration_mode,
                "priority": wf.priority
            }
            for wf in self.workflow_definitions.values()
        ]
    
    def list_available_agents(self) -> List[Dict[str, Any]]:
        """List all available agents"""
        return [
            {
                "agent_name": agent.agent_name,
                "role": agent.agent_role,
                "description": agent.description,
                "version": agent.version
            }
            for agent in self.agent_registry.values()
        ]

class WorkflowEngine:
    """Main workflow engine for BizOSaas business processes"""
    
    def __init__(self):
        self.orchestrator = HierarchicalCrewOrchestrator()
        self.execution_history = {}
    
    async def execute_business_workflow(
        self,
        workflow_type: str,
        business_data: Dict[str, Any],
        tenant_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Execute a complete business workflow"""
        
        try:
            execution = await self.orchestrator.execute_workflow(
                workflow_id=workflow_type,
                input_data=business_data,
                tenant_id=tenant_id,
                user_id=user_id
            )
            
            # Store execution history
            self.execution_history[execution.execution_id] = execution
            
            return {
                "execution_id": execution.execution_id,
                "status": execution.status,
                "results": execution.results,
                "performance_metrics": execution.performance_metrics,
                "started_at": execution.started_at.isoformat() if execution.started_at else None,
                "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
                "errors": execution.errors
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                "execution_id": None,
                "status": WorkflowStatus.FAILED,
                "error": str(e),
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow execution"""
        execution = self.orchestrator.get_workflow_status(execution_id)
        
        if not execution:
            execution = self.execution_history.get(execution_id)
        
        if not execution:
            return None
        
        return {
            "execution_id": execution.execution_id,
            "workflow_name": execution.workflow_def.name,
            "status": execution.status,
            "current_step": execution.current_step,
            "total_steps": len(execution.workflow_def.agent_sequence),
            "progress": execution.current_step / len(execution.workflow_def.agent_sequence) * 100,
            "started_at": execution.started_at.isoformat() if execution.started_at else None,
            "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
            "performance_metrics": execution.performance_metrics,
            "errors": execution.errors
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available business workflows"""
        return self.orchestrator.list_available_workflows()
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all available AI agents"""
        return self.orchestrator.list_available_agents()