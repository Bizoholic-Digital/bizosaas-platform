"""
Agent Hierarchy System for BizOSaaS AI Crew

This module defines the hierarchical structure of AI agents with Supervisors,
Specialists, and Workers for sophisticated task delegation and execution.
"""

from typing import Dict, List, Any, Optional, Type, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio
import logging
from abc import ABC, abstractmethod

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)

class AgentLevel(Enum):
    """Agent hierarchy levels"""
    SUPERVISOR = "supervisor"
    SPECIALIST = "specialist"
    WORKER = "worker"

class AgentDomain(Enum):
    """Business domain specializations"""
    CRM = "crm"
    ECOMMERCE = "ecommerce"
    ANALYTICS = "analytics"
    BILLING = "billing"
    CMS = "cms"
    INTEGRATIONS = "integrations"
    MARKETING = "marketing"
    OPERATIONS = "operations"

class TaskComplexity(Enum):
    """Task complexity levels for delegation"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"

class AgentStatus(Enum):
    """Agent operational status"""
    IDLE = "idle"
    BUSY = "busy"
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"
    ERROR = "error"

@dataclass
class AgentMetrics:
    """Performance metrics for agents"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    average_execution_time: float = 0.0
    success_rate: float = 0.0
    load_factor: float = 0.0
    last_activity: Optional[datetime] = None
    
    def update_metrics(self, execution_time: float, success: bool):
        """Update agent performance metrics"""
        self.total_tasks += 1
        self.last_activity = datetime.now()
        
        if success:
            self.completed_tasks += 1
        else:
            self.failed_tasks += 1
        
        # Update average execution time
        if self.total_tasks == 1:
            self.average_execution_time = execution_time
        else:
            self.average_execution_time = (
                (self.average_execution_time * (self.total_tasks - 1) + execution_time) 
                / self.total_tasks
            )
        
        # Update success rate
        self.success_rate = self.completed_tasks / self.total_tasks
        
        # Update load factor (simple calculation based on recent activity)
        self.load_factor = min(1.0, self.total_tasks / 100.0)

class BaseAgentConfig(BaseModel):
    """Base configuration for all agents"""
    name: str
    role: str
    goal: str
    backstory: str
    level: AgentLevel
    domain: AgentDomain
    max_execution_time: int = 300  # seconds
    max_iterations: int = 10
    allow_delegation: bool = False
    memory: bool = True
    verbose: bool = True
    tools: List[str] = Field(default_factory=list)
    llm_config: Dict[str, Any] = Field(default_factory=dict)

class BaseHierarchicalAgent(ABC):
    """Abstract base class for hierarchical agents"""
    
    def __init__(self, config: BaseAgentConfig):
        self.config = config
        self.status = AgentStatus.IDLE
        self.metrics = AgentMetrics()
        self.subordinates: List['BaseHierarchicalAgent'] = []
        self.supervisor: Optional['BaseHierarchicalAgent'] = None
        self.tools: List[BaseTool] = []
        self.agent: Optional[Agent] = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the CrewAI agent"""
        llm_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.1,
            **self.config.llm_config
        }
        
        llm = ChatOpenAI(**llm_config)
        
        self.agent = Agent(
            role=self.config.role,
            goal=self.config.goal,
            backstory=self.config.backstory,
            verbose=self.config.verbose,
            allow_delegation=self.config.allow_delegation,
            tools=self.tools,
            llm=llm,
            memory=self.config.memory,
            max_execution_time=self.config.max_execution_time,
            max_iter=self.config.max_iterations
        )
    
    @abstractmethod
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Check if agent can handle the given task"""
        pass
    
    def add_subordinate(self, agent: 'BaseHierarchicalAgent'):
        """Add a subordinate agent"""
        self.subordinates.append(agent)
        agent.supervisor = self
    
    def remove_subordinate(self, agent: 'BaseHierarchicalAgent'):
        """Remove a subordinate agent"""
        if agent in self.subordinates:
            self.subordinates.remove(agent)
            agent.supervisor = None
    
    def get_available_subordinates(self) -> List['BaseHierarchicalAgent']:
        """Get list of available subordinate agents"""
        return [
            agent for agent in self.subordinates 
            if agent.status == AgentStatus.AVAILABLE
        ]
    
    async def delegate_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate task to appropriate subordinate"""
        available_agents = self.get_available_subordinates()
        
        # Find best agent for the task
        best_agent = None
        best_score = 0
        
        for agent in available_agents:
            if agent.can_handle_task(task_data):
                # Simple scoring based on success rate and load
                score = agent.metrics.success_rate * (1 - agent.metrics.load_factor)
                if score > best_score:
                    best_score = score
                    best_agent = agent
        
        if best_agent:
            logger.info(f"Delegating task to {best_agent.config.name}")
            return await best_agent.execute_task(task_data)
        else:
            raise Exception(f"No available subordinate can handle task: {task_data.get('type', 'unknown')}")

class SupervisorAgent(BaseHierarchicalAgent):
    """High-level supervisor agents that coordinate and delegate tasks"""
    
    def __init__(self, config: BaseAgentConfig):
        config.level = AgentLevel.SUPERVISOR
        config.allow_delegation = True
        super().__init__(config)
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task through delegation and coordination"""
        start_time = datetime.now()
        
        try:
            self.status = AgentStatus.BUSY
            
            # Analyze task complexity
            complexity = self._analyze_task_complexity(task_data)
            
            if complexity in [TaskComplexity.COMPLEX, TaskComplexity.EXPERT]:
                # For complex tasks, create a crew with multiple specialists
                return await self._execute_complex_task(task_data)
            else:
                # For simpler tasks, delegate to single specialist
                return await self.delegate_task(task_data)
        
        except Exception as e:
            logger.error(f"Supervisor task execution failed: {str(e)}")
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics.update_metrics(execution_time, False)
            raise
        
        finally:
            self.status = AgentStatus.AVAILABLE
    
    def _analyze_task_complexity(self, task_data: Dict[str, Any]) -> TaskComplexity:
        """Analyze task complexity to determine execution strategy"""
        
        # Simple heuristics for complexity analysis
        task_type = task_data.get('type', '')
        requires_multiple_domains = task_data.get('multi_domain', False)
        data_volume = task_data.get('data_volume', 0)
        
        if requires_multiple_domains or 'workflow' in task_type:
            return TaskComplexity.EXPERT
        elif data_volume > 10000 or 'analysis' in task_type:
            return TaskComplexity.COMPLEX
        elif 'optimization' in task_type or 'recommendation' in task_type:
            return TaskComplexity.MODERATE
        else:
            return TaskComplexity.SIMPLE
    
    async def _execute_complex_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complex task using crew coordination"""
        
        # Identify required specialists
        required_domains = task_data.get('required_domains', [])
        specialist_agents = []
        
        for domain in required_domains:
            domain_specialists = [
                agent for agent in self.subordinates 
                if agent.config.domain.value == domain
                and agent.status == AgentStatus.AVAILABLE
            ]
            if domain_specialists:
                specialist_agents.append(domain_specialists[0])  # Pick best available
        
        if not specialist_agents:
            # Fallback to single agent delegation
            return await self.delegate_task(task_data)
        
        # Create collaborative crew
        tasks = []
        for i, agent in enumerate(specialist_agents):
            task_description = f"Handle {agent.config.domain.value} aspects of: {task_data.get('description', '')}"
            
            task = Task(
                description=task_description,
                agent=agent.agent,
                expected_output=f"Processed {agent.config.domain.value} results"
            )
            tasks.append(task)
        
        # Create and execute crew
        crew = Crew(
            agents=[agent.agent for agent in specialist_agents],
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        result = crew.kickoff(task_data)
        
        return {
            'status': 'success',
            'result': result,
            'agents_used': [agent.config.name for agent in specialist_agents],
            'execution_type': 'crew_collaboration'
        }
    
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Supervisor can handle any task through delegation"""
        return True

class SpecialistAgent(BaseHierarchicalAgent):
    """Domain-specific specialist agents"""
    
    def __init__(self, config: BaseAgentConfig):
        config.level = AgentLevel.SPECIALIST
        config.allow_delegation = True  # Can delegate to workers
        super().__init__(config)
        self._initialize_domain_tools()
    
    def _initialize_domain_tools(self):
        """Initialize domain-specific tools"""
        domain_tools = {
            AgentDomain.CRM: self._create_crm_tools(),
            AgentDomain.ECOMMERCE: self._create_ecommerce_tools(),
            AgentDomain.ANALYTICS: self._create_analytics_tools(),
            AgentDomain.BILLING: self._create_billing_tools(),
            AgentDomain.CMS: self._create_cms_tools(),
            AgentDomain.INTEGRATIONS: self._create_integration_tools()
        }
        
        self.tools = domain_tools.get(self.config.domain, [])
    
    def _create_crm_tools(self) -> List[BaseTool]:
        """Create CRM-specific tools"""
        # Implementation for CRM tools
        return []
    
    def _create_ecommerce_tools(self) -> List[BaseTool]:
        """Create E-commerce specific tools"""
        # Implementation for E-commerce tools
        return []
    
    def _create_analytics_tools(self) -> List[BaseTool]:
        """Create Analytics specific tools"""
        # Implementation for Analytics tools
        return []
    
    def _create_billing_tools(self) -> List[BaseTool]:
        """Create Billing specific tools"""
        # Implementation for Billing tools
        return []
    
    def _create_cms_tools(self) -> List[BaseTool]:
        """Create CMS specific tools"""
        # Implementation for CMS tools
        return []
    
    def _create_integration_tools(self) -> List[BaseTool]:
        """Create Integration specific tools"""
        # Implementation for Integration tools
        return []
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute domain-specific task"""
        start_time = datetime.now()
        
        try:
            self.status = AgentStatus.BUSY
            
            # Check if we can handle this ourselves or need to delegate
            if self._requires_worker_delegation(task_data):
                return await self.delegate_task(task_data)
            else:
                return await self._execute_specialist_task(task_data)
        
        except Exception as e:
            logger.error(f"Specialist task execution failed: {str(e)}")
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics.update_metrics(execution_time, False)
            raise
        
        finally:
            self.status = AgentStatus.AVAILABLE
    
    def _requires_worker_delegation(self, task_data: Dict[str, Any]) -> bool:
        """Check if task requires delegation to worker agents"""
        # Simple heuristics for delegation decision
        data_processing_intensive = task_data.get('data_intensive', False)
        repetitive_task = task_data.get('repetitive', False)
        bulk_operation = task_data.get('bulk_operation', False)
        
        return data_processing_intensive or repetitive_task or bulk_operation
    
    async def _execute_specialist_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task using specialist knowledge"""
        
        # Create a task for the agent
        task_description = task_data.get('description', 'Execute specialist task')
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="Completed specialist analysis and recommendations"
        )
        
        # Execute the task
        result = task.execute()
        
        return {
            'status': 'success',
            'result': result,
            'agent': self.config.name,
            'domain': self.config.domain.value,
            'execution_type': 'specialist_direct'
        }
    
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Check if specialist can handle the task based on domain"""
        task_domain = task_data.get('domain')
        if task_domain:
            return task_domain == self.config.domain.value
        
        # Check for domain-specific keywords
        description = task_data.get('description', '').lower()
        domain_keywords = {
            AgentDomain.CRM: ['lead', 'customer', 'contact', 'sales', 'pipeline'],
            AgentDomain.ECOMMERCE: ['product', 'inventory', 'order', 'catalog', 'pricing'],
            AgentDomain.ANALYTICS: ['report', 'analysis', 'metric', 'dashboard', 'insight'],
            AgentDomain.BILLING: ['invoice', 'payment', 'subscription', 'revenue', 'billing'],
            AgentDomain.CMS: ['content', 'page', 'article', 'media', 'publishing'],
            AgentDomain.INTEGRATIONS: ['api', 'sync', 'webhook', 'connection', 'integration']
        }
        
        keywords = domain_keywords.get(self.config.domain, [])
        return any(keyword in description for keyword in keywords)

class WorkerAgent(BaseHierarchicalAgent):
    """Low-level worker agents for specific operations"""
    
    def __init__(self, config: BaseAgentConfig):
        config.level = AgentLevel.WORKER
        config.allow_delegation = False  # Workers don't delegate
        super().__init__(config)
    
    async def execute_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific operational task"""
        start_time = datetime.now()
        
        try:
            self.status = AgentStatus.BUSY
            
            # Workers execute tasks directly
            result = await self._execute_worker_task(task_data)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics.update_metrics(execution_time, True)
            
            return result
        
        except Exception as e:
            logger.error(f"Worker task execution failed: {str(e)}")
            execution_time = (datetime.now() - start_time).total_seconds()
            self.metrics.update_metrics(execution_time, False)
            raise
        
        finally:
            self.status = AgentStatus.AVAILABLE
    
    async def _execute_worker_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual worker task"""
        
        task_description = task_data.get('description', 'Execute worker task')
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="Completed worker operation"
        )
        
        result = task.execute()
        
        return {
            'status': 'success',
            'result': result,
            'agent': self.config.name,
            'domain': self.config.domain.value,
            'execution_type': 'worker_direct'
        }
    
    def can_handle_task(self, task_data: Dict[str, Any]) -> bool:
        """Check if worker can handle specific task type"""
        task_type = task_data.get('type', '')
        worker_tasks = task_data.get('worker_tasks', [])
        
        # Check if this specific worker type can handle the task
        return (
            task_type in worker_tasks or
            self.config.name.lower() in task_type.lower()
        )

class AgentHierarchy:
    """Manages the hierarchical structure of agents"""
    
    def __init__(self):
        self.agents: Dict[str, BaseHierarchicalAgent] = {}
        self.supervisors: List[SupervisorAgent] = []
        self.specialists: Dict[AgentDomain, List[SpecialistAgent]] = {}
        self.workers: Dict[AgentDomain, List[WorkerAgent]] = {}
        self._initialize_default_hierarchy()
    
    def _initialize_default_hierarchy(self):
        """Initialize the default agent hierarchy"""
        
        # Create Master Business Supervisor
        master_supervisor_config = BaseAgentConfig(
            name="master_business_supervisor",
            role="Master Business Operations Supervisor",
            goal="Coordinate all business operations and ensure optimal task execution across domains",
            backstory="""You are the master supervisor overseeing all business operations. 
            You excel at understanding complex business requirements, coordinating multiple teams, 
            and ensuring tasks are executed efficiently across all domains.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.OPERATIONS,
            allow_delegation=True
        )
        
        master_supervisor = SupervisorAgent(master_supervisor_config)
        self.add_agent(master_supervisor)
        
        # Create domain supervisors
        domain_supervisors = {
            AgentDomain.CRM: self._create_crm_supervisor(),
            AgentDomain.ECOMMERCE: self._create_ecommerce_supervisor(),
            AgentDomain.ANALYTICS: self._create_analytics_supervisor(),
            AgentDomain.BILLING: self._create_billing_supervisor(),
            AgentDomain.CMS: self._create_cms_supervisor(),
            AgentDomain.INTEGRATIONS: self._create_integrations_supervisor()
        }
        
        # Add domain supervisors as subordinates to master supervisor
        for domain, supervisor in domain_supervisors.items():
            self.add_agent(supervisor)
            master_supervisor.add_subordinate(supervisor)
        
        # Create specialists and workers for each domain
        for domain in AgentDomain:
            specialists = self._create_domain_specialists(domain)
            workers = self._create_domain_workers(domain)
            
            domain_supervisor = domain_supervisors.get(domain)
            
            for specialist in specialists:
                self.add_agent(specialist)
                if domain_supervisor:
                    domain_supervisor.add_subordinate(specialist)
            
            for worker in workers:
                self.add_agent(worker)
                # Assign workers to relevant specialists
                for specialist in specialists:
                    specialist.add_subordinate(worker)
    
    def _create_crm_supervisor(self) -> SupervisorAgent:
        """Create CRM domain supervisor"""
        config = BaseAgentConfig(
            name="crm_supervisor",
            role="CRM Operations Supervisor",
            goal="Oversee all customer relationship management operations",
            backstory="""You are an expert CRM supervisor with deep understanding of 
            customer lifecycle management, sales processes, and relationship optimization.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.CRM
        )
        return SupervisorAgent(config)
    
    def _create_ecommerce_supervisor(self) -> SupervisorAgent:
        """Create E-commerce domain supervisor"""
        config = BaseAgentConfig(
            name="ecommerce_supervisor",
            role="E-commerce Operations Supervisor",
            goal="Manage all e-commerce operations including inventory, orders, and catalog management",
            backstory="""You are an experienced e-commerce supervisor who understands 
            online retail operations, inventory management, and customer shopping experiences.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.ECOMMERCE
        )
        return SupervisorAgent(config)
    
    def _create_analytics_supervisor(self) -> SupervisorAgent:
        """Create Analytics domain supervisor"""
        config = BaseAgentConfig(
            name="analytics_supervisor", 
            role="Analytics Operations Supervisor",
            goal="Coordinate all analytics and reporting operations",
            backstory="""You are an analytics expert who specializes in data-driven insights, 
            performance monitoring, and business intelligence across all platform operations.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.ANALYTICS
        )
        return SupervisorAgent(config)
    
    def _create_billing_supervisor(self) -> SupervisorAgent:
        """Create Billing domain supervisor"""
        config = BaseAgentConfig(
            name="billing_supervisor",
            role="Billing Operations Supervisor", 
            goal="Oversee all billing, payment, and subscription management operations",
            backstory="""You are a billing operations expert who understands subscription management, 
            payment processing, revenue optimization, and financial compliance.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.BILLING
        )
        return SupervisorAgent(config)
    
    def _create_cms_supervisor(self) -> SupervisorAgent:
        """Create CMS domain supervisor"""
        config = BaseAgentConfig(
            name="cms_supervisor",
            role="Content Management Supervisor",
            goal="Coordinate all content management and publishing operations",
            backstory="""You are a content management expert who understands content strategy, 
            publishing workflows, SEO optimization, and digital content lifecycle management.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.CMS
        )
        return SupervisorAgent(config)
    
    def _create_integrations_supervisor(self) -> SupervisorAgent:
        """Create Integrations domain supervisor"""
        config = BaseAgentConfig(
            name="integrations_supervisor",
            role="Integrations Operations Supervisor",
            goal="Manage all third-party integrations and data synchronization",
            backstory="""You are an integration specialist who excels at connecting disparate systems, 
            managing API relationships, and ensuring seamless data flow across platforms.""",
            level=AgentLevel.SUPERVISOR,
            domain=AgentDomain.INTEGRATIONS
        )
        return SupervisorAgent(config)
    
    def _create_domain_specialists(self, domain: AgentDomain) -> List[SpecialistAgent]:
        """Create specialist agents for a domain"""
        
        specialist_configs = {
            AgentDomain.CRM: [
                {
                    "name": f"crm_lead_specialist",
                    "role": "Lead Management Specialist",
                    "goal": "Optimize lead scoring, nurturing, and conversion processes",
                    "backstory": "Expert in lead qualification and conversion optimization"
                },
                {
                    "name": f"crm_customer_specialist", 
                    "role": "Customer Relationship Specialist",
                    "goal": "Enhance customer relationships and retention strategies",
                    "backstory": "Specialist in customer lifecycle management and retention"
                }
            ],
            AgentDomain.ECOMMERCE: [
                {
                    "name": f"ecommerce_inventory_specialist",
                    "role": "Inventory Optimization Specialist", 
                    "goal": "Optimize inventory levels and product availability",
                    "backstory": "Expert in inventory management and demand forecasting"
                },
                {
                    "name": f"ecommerce_product_specialist",
                    "role": "Product Recommendation Specialist",
                    "goal": "Generate intelligent product recommendations and optimize catalogs",
                    "backstory": "Specialist in product analytics and recommendation systems"
                }
            ],
            AgentDomain.ANALYTICS: [
                {
                    "name": f"analytics_reporting_specialist",
                    "role": "Report Generation Specialist",
                    "goal": "Create comprehensive business reports and insights",
                    "backstory": "Expert in data analysis and business intelligence reporting"
                },
                {
                    "name": f"analytics_insights_specialist",
                    "role": "Business Insights Specialist", 
                    "goal": "Generate actionable business insights from data patterns",
                    "backstory": "Specialist in pattern recognition and predictive analytics"
                }
            ],
            AgentDomain.BILLING: [
                {
                    "name": f"billing_subscription_specialist",
                    "role": "Subscription Management Specialist",
                    "goal": "Optimize subscription lifecycle and revenue management",
                    "backstory": "Expert in subscription business models and revenue optimization"
                },
                {
                    "name": f"billing_revenue_specialist",
                    "role": "Revenue Optimization Specialist",
                    "goal": "Analyze and optimize revenue streams and pricing strategies",
                    "backstory": "Specialist in pricing strategies and revenue analytics"
                }
            ],
            AgentDomain.CMS: [
                {
                    "name": f"cms_content_specialist",
                    "role": "Content Optimization Specialist",
                    "goal": "Optimize content for engagement and SEO performance", 
                    "backstory": "Expert in content strategy and search engine optimization"
                },
                {
                    "name": f"cms_seo_specialist",
                    "role": "SEO Recommendation Specialist",
                    "goal": "Provide SEO recommendations and content optimization strategies",
                    "backstory": "Specialist in technical SEO and content optimization"
                }
            ],
            AgentDomain.INTEGRATIONS: [
                {
                    "name": f"integrations_sync_specialist",
                    "role": "Data Synchronization Specialist",
                    "goal": "Ensure seamless data synchronization across platforms",
                    "backstory": "Expert in data integration and synchronization strategies"
                },
                {
                    "name": f"integrations_error_specialist",
                    "role": "Integration Error Handler",
                    "goal": "Handle integration errors and implement recovery strategies",
                    "backstory": "Specialist in troubleshooting and error recovery for integrations"
                }
            ]
        }
        
        specialists = []
        configs = specialist_configs.get(domain, [])
        
        for config_data in configs:
            config = BaseAgentConfig(
                **config_data,
                level=AgentLevel.SPECIALIST,
                domain=domain
            )
            specialists.append(SpecialistAgent(config))
        
        return specialists
    
    def _create_domain_workers(self, domain: AgentDomain) -> List[WorkerAgent]:
        """Create worker agents for a domain"""
        
        worker_configs = {
            AgentDomain.CRM: [
                {
                    "name": f"crm_data_processor",
                    "role": "CRM Data Processing Worker",
                    "goal": "Process CRM data updates and maintenance tasks",
                    "backstory": "Specialized in CRM data processing and cleanup operations"
                },
                {
                    "name": f"crm_email_worker",
                    "role": "CRM Email Automation Worker", 
                    "goal": "Execute email campaigns and automated communications",
                    "backstory": "Expert in email automation and customer communications"
                }
            ],
            AgentDomain.ECOMMERCE: [
                {
                    "name": f"ecommerce_price_worker",
                    "role": "Price Update Worker",
                    "goal": "Execute price updates and inventory adjustments",
                    "backstory": "Specialized in product pricing and inventory operations"
                },
                {
                    "name": f"ecommerce_order_worker",
                    "role": "Order Processing Worker",
                    "goal": "Process orders and handle fulfillment operations",
                    "backstory": "Expert in order processing and fulfillment workflows"
                }
            ],
            AgentDomain.ANALYTICS: [
                {
                    "name": f"analytics_data_worker",
                    "role": "Data Collection Worker",
                    "goal": "Collect and prepare data for analysis",
                    "backstory": "Specialized in data collection and preparation tasks"
                },
                {
                    "name": f"analytics_calc_worker",
                    "role": "Calculation Worker",
                    "goal": "Perform calculations and statistical operations",
                    "backstory": "Expert in mathematical calculations and data processing"
                }
            ],
            AgentDomain.BILLING: [
                {
                    "name": f"billing_invoice_worker",
                    "role": "Invoice Generation Worker",
                    "goal": "Generate and process invoices automatically",
                    "backstory": "Specialized in invoice generation and billing operations"
                },
                {
                    "name": f"billing_payment_worker", 
                    "role": "Payment Processing Worker",
                    "goal": "Process payments and handle payment reconciliation",
                    "backstory": "Expert in payment processing and reconciliation"
                }
            ],
            AgentDomain.CMS: [
                {
                    "name": f"cms_publish_worker",
                    "role": "Content Publishing Worker",
                    "goal": "Execute content publishing and updates",
                    "backstory": "Specialized in content publishing and distribution"
                },
                {
                    "name": f"cms_seo_worker",
                    "role": "SEO Implementation Worker",
                    "goal": "Implement SEO recommendations and optimizations",
                    "backstory": "Expert in implementing technical SEO changes"
                }
            ],
            AgentDomain.INTEGRATIONS: [
                {
                    "name": f"integrations_api_worker",
                    "role": "API Call Worker",
                    "goal": "Execute API calls and data transfers",
                    "backstory": "Specialized in API operations and data exchange"
                },
                {
                    "name": f"integrations_monitor_worker",
                    "role": "Integration Monitoring Worker",
                    "goal": "Monitor integration health and performance",
                    "backstory": "Expert in monitoring and alerting for integrations"
                }
            ]
        }
        
        workers = []
        configs = worker_configs.get(domain, [])
        
        for config_data in configs:
            config = BaseAgentConfig(
                **config_data,
                level=AgentLevel.WORKER,
                domain=domain
            )
            workers.append(WorkerAgent(config))
        
        return workers
    
    def add_agent(self, agent: BaseHierarchicalAgent):
        """Add an agent to the hierarchy"""
        self.agents[agent.config.name] = agent
        
        if agent.config.level == AgentLevel.SUPERVISOR:
            self.supervisors.append(agent)
        elif agent.config.level == AgentLevel.SPECIALIST:
            domain_specialists = self.specialists.setdefault(agent.config.domain, [])
            domain_specialists.append(agent)
        elif agent.config.level == AgentLevel.WORKER:
            domain_workers = self.workers.setdefault(agent.config.domain, [])
            domain_workers.append(agent)
    
    def get_agent(self, name: str) -> Optional[BaseHierarchicalAgent]:
        """Get agent by name"""
        return self.agents.get(name)
    
    def get_agents_by_domain(self, domain: AgentDomain) -> List[BaseHierarchicalAgent]:
        """Get all agents for a specific domain"""
        agents = []
        agents.extend(self.specialists.get(domain, []))
        agents.extend(self.workers.get(domain, []))
        return agents
    
    def get_available_agents(self) -> List[BaseHierarchicalAgent]:
        """Get all currently available agents"""
        return [
            agent for agent in self.agents.values()
            if agent.status == AgentStatus.AVAILABLE
        ]
    
    def get_hierarchy_status(self) -> Dict[str, Any]:
        """Get comprehensive hierarchy status"""
        status = {
            'total_agents': len(self.agents),
            'supervisors': len(self.supervisors),
            'specialists': sum(len(specs) for specs in self.specialists.values()),
            'workers': sum(len(workers) for workers in self.workers.values()),
            'available_agents': len(self.get_available_agents()),
            'domain_breakdown': {}
        }
        
        for domain in AgentDomain:
            domain_agents = self.get_agents_by_domain(domain)
            status['domain_breakdown'][domain.value] = {
                'total': len(domain_agents),
                'available': len([a for a in domain_agents if a.status == AgentStatus.AVAILABLE])
            }
        
        return status
    
    async def route_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route task to appropriate agent in hierarchy"""
        
        # Start with master supervisor for complex coordination
        master_supervisor = next(
            (agent for agent in self.supervisors 
             if agent.config.name == "master_business_supervisor"), 
            None
        )
        
        if master_supervisor:
            return await master_supervisor.execute_task(task_data)
        else:
            # Fallback to domain-specific routing
            task_domain = task_data.get('domain')
            if task_domain:
                domain_enum = AgentDomain(task_domain)
                domain_agents = self.get_agents_by_domain(domain_enum)
                
                # Find best available agent
                for agent in domain_agents:
                    if (agent.status == AgentStatus.AVAILABLE and 
                        agent.can_handle_task(task_data)):
                        return await agent.execute_task(task_data)
            
            raise Exception(f"No suitable agent found for task: {task_data.get('type', 'unknown')}")

# Global instance
agent_hierarchy = AgentHierarchy()