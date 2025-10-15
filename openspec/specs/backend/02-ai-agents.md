# AI Agents Service - Backend Service (DDD)

## Service Identity
- **Name**: AI Agents Service
- **Type**: Backend - AI Orchestration & Autonomous Decision-Making
- **Container**: `bizosaas-ai-agents-staging`
- **Image**: `bizosaas/ai-agents:latest`
- **Port**: `8008:8000` (external:internal)
- **Status**: ✅ Running (19+ hours uptime)

## Purpose
Orchestrate 93 specialized CrewAI + LangChain agents across 40+ API integrations providing autonomous decision-making for marketing campaigns, e-commerce operations, and business automation.

## Domain-Driven Design Architecture

### Bounded Context
**AI Agents Context** - Autonomous agent orchestration and decision-making

```
AI Agents Bounded Context
├── Domain Layer
│   ├── Aggregates: AgentCrew, AgentTask, Integration
│   ├── Entities: Agent, Task, ExecutionContext
│   ├── Value Objects: AgentPattern, IntegrationCategory, TaskStatus
│   ├── Domain Events: CrewExecutionStarted, TaskCompleted, IntegrationActivated
│   ├── Domain Services: CrewOrchestrator, TaskRouter, CredentialManager
│   └── Repository Interfaces: ICrewRepository, ITaskRepository
├── Application Layer
│   ├── Commands: ExecuteCrewCommand, CreateTaskCommand
│   ├── Queries: GetTaskStatusQuery, ListAgentsQuery
│   ├── Handlers: CrewExecutionHandler, TaskStatusHandler
│   └── DTOs: CrewExecutionDTO, TaskResultDTO
├── Infrastructure Layer
│   ├── CrewAI Engine Integration
│   ├── LangChain Framework Integration
│   ├── External API Adapters (40+ integrations)
│   ├── Vault Credentials Provider
│   └── Redis Task Queue
└── API Layer
    ├── REST Endpoints (FastAPI)
    ├── WebSocket (real-time updates)
    └── Agent Management API
```

### Core Aggregates

#### AgentCrew Aggregate
```python
from typing import List, Optional
from enum import Enum
from uuid import UUID, uuid4
from dataclasses import dataclass, field
from datetime import datetime

class AgentPattern(Enum):
    FOUR_AGENT = "4-agent"      # Complex integrations
    THREE_AGENT = "3-agent"     # Medium integrations
    TWO_AGENT = "2-agent"       # Standard integrations
    SINGLE_AGENT = "single"     # Simple integrations

class CrewStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class AgentCrew:
    """
    Aggregate root for AI agent crew
    
    Invariants:
    - Crew must have at least one agent
    - All agents must belong to same integration category
    - Crew pattern must match number of agents
    """
    def __init__(
        self,
        id: UUID,
        name: str,
        pattern: AgentPattern,
        integration: str,
        tenant_id: UUID
    ):
        self.id = id
        self.name = name
        self.pattern = pattern
        self.integration = integration
        self.tenant_id = tenant_id
        self.agents: List[Agent] = []
        self.tasks: List[AgentTask] = []
        self.status = CrewStatus.IDLE
        self.execution_context: Optional[ExecutionContext] = None
        self._domain_events: List[DomainEvent] = []

    def add_agent(self, agent: Agent):
        """Add agent to crew"""
        if len(self.agents) >= self._max_agents_for_pattern():
            raise ValueError(f"Crew pattern {self.pattern} allows max {self._max_agents_for_pattern()} agents")
        
        self.agents.append(agent)

    def execute(self, context: ExecutionContext) -> UUID:
        """Start crew execution"""
        if self.status == CrewStatus.RUNNING:
            raise ValueError("Crew already running")
        
        if not self.agents:
            raise ValueError("Crew has no agents")
        
        self.execution_context = context
        self.status = CrewStatus.RUNNING
        
        # Create execution ID
        execution_id = uuid4()
        
        self._add_domain_event(CrewExecutionStartedEvent(
            crew_id=self.id,
            execution_id=execution_id,
            integration=self.integration,
            tenant_id=self.tenant_id
        ))
        
        return execution_id

    def complete_execution(self, result: dict):
        """Mark execution as completed"""
        self.status = CrewStatus.COMPLETED
        
        self._add_domain_event(CrewExecutionCompletedEvent(
            crew_id=self.id,
            result=result,
            tenant_id=self.tenant_id
        ))

    def fail_execution(self, error: str):
        """Mark execution as failed"""
        self.status = CrewStatus.FAILED
        
        self._add_domain_event(CrewExecutionFailedEvent(
            crew_id=self.id,
            error=error,
            tenant_id=self.tenant_id
        ))

    def _max_agents_for_pattern(self) -> int:
        return {
            AgentPattern.FOUR_AGENT: 4,
            AgentPattern.THREE_AGENT: 3,
            AgentPattern.TWO_AGENT: 2,
            AgentPattern.SINGLE_AGENT: 1
        }[self.pattern]

    def _add_domain_event(self, event: DomainEvent):
        self._domain_events.append(event)
```

#### AgentTask Aggregate
```python
class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentTask:
    """
    Aggregate for agent tasks
    
    Manages:
    - Task execution lifecycle
    - Input/output data
    - Dependencies between tasks
    - Human-in-the-loop (HITL) approval
    """
    def __init__(
        self,
        id: UUID,
        description: str,
        agent_id: UUID,
        priority: TaskPriority,
        tenant_id: UUID
    ):
        self.id = id
        self.description = description
        self.agent_id = agent_id
        self.priority = priority
        self.tenant_id = tenant_id
        self.status = TaskStatus.PENDING
        self.input_data: dict = {}
        self.output_data: Optional[dict] = None
        self.requires_hitl = False
        self.hitl_approved = False
        self.dependencies: List[UUID] = []
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self._domain_events: List[DomainEvent] = []

    def start_execution(self):
        """Start task execution"""
        if self.status != TaskStatus.PENDING:
            raise ValueError(f"Cannot start task with status {self.status}")
        
        if not self._dependencies_completed():
            raise ValueError("Task dependencies not completed")
        
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()
        
        self._add_domain_event(TaskStartedEvent(
            task_id=self.id,
            agent_id=self.agent_id,
            tenant_id=self.tenant_id
        ))

    def complete(self, output: dict):
        """Complete task with output"""
        if self.requires_hitl and not self.hitl_approved:
            raise ValueError("Task requires HITL approval")
        
        self.status = TaskStatus.COMPLETED
        self.output_data = output
        self.completed_at = datetime.utcnow()
        
        self._add_domain_event(TaskCompletedEvent(
            task_id=self.id,
            output=output,
            execution_time=(self.completed_at - self.started_at).total_seconds(),
            tenant_id=self.tenant_id
        ))

    def request_hitl_approval(self, data: dict):
        """Request human-in-the-loop approval"""
        self.requires_hitl = True
        self.status = TaskStatus.PENDING
        
        self._add_domain_event(HITLApprovalRequestedEvent(
            task_id=self.id,
            data=data,
            tenant_id=self.tenant_id
        ))

    def approve_hitl(self):
        """Approve task via HITL"""
        self.hitl_approved = True
        
        self._add_domain_event(HITLApprovedEvent(
            task_id=self.id,
            tenant_id=self.tenant_id
        ))

    def _dependencies_completed(self) -> bool:
        # Check if all dependent tasks are completed
        return True  # Implementation checks task repository
```

### Value Objects

```python
@dataclass(frozen=True)
class IntegrationCategory:
    """Integration category classification"""
    name: str  # e.g., "social_media", "ai_providers", "ecommerce"
    
    def __post_init__(self):
        valid_categories = [
            "social_media", "ai_providers", "ecommerce", 
            "business_ops", "search_engines"
        ]
        if self.name not in valid_categories:
            raise ValueError(f"Invalid category: {self.name}")

@dataclass(frozen=True)
class AgentRole:
    """Agent role within crew"""
    title: str
    responsibilities: List[str]
    
    def __post_init__(self):
        if not self.responsibilities:
            raise ValueError("Agent must have at least one responsibility")
```

### Domain Events

```python
@dataclass
class CrewExecutionStartedEvent:
    crew_id: UUID
    execution_id: UUID
    integration: str
    tenant_id: UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class TaskCompletedEvent:
    task_id: UUID
    output: dict
    execution_time: float
    tenant_id: UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class HITLApprovalRequestedEvent:
    task_id: UUID
    data: dict
    tenant_id: UUID
    timestamp: datetime = field(default_factory=datetime.utcnow)
```

## 93 AI Agents Implementation

### Agent Pattern Distribution

#### 4-Agent Pattern (6 integrations)
**Complex APIs requiring 4 specialized agents**:
- Facebook/Meta, Amazon SP-API, Amazon Advertising, Stripe, PayPal, PayU

```python
class FourAgentCrew:
    """4-Agent pattern for complex integrations"""
    
    def __init__(self, integration: str):
        self.management_agent = Agent(
            role="Management Agent",
            goal="Coordinate overall strategy and resource allocation",
            backstory="Expert project manager with deep integration knowledge"
        )
        
        self.analytics_agent = Agent(
            role="Analytics Agent",
            goal="Analyze performance data and provide insights",
            backstory="Data scientist specializing in marketing analytics"
        )
        
        self.content_agent = Agent(
            role="Content/Operations Agent",
            goal="Handle content creation and operational tasks",
            backstory="Content strategist with operations expertise"
        )
        
        self.performance_agent = Agent(
            role="Performance Agent",
            goal="Optimize campaigns and monitor KPIs",
            backstory="Performance marketing specialist"
        )
    
    async def execute(self, task: dict) -> dict:
        """Execute 4-agent workflow"""
        # Management agent plans strategy
        strategy = await self.management_agent.execute(task)
        
        # Content agent creates/configures
        content = await self.content_agent.execute(strategy)
        
        # Performance agent optimizes
        optimization = await self.performance_agent.execute(content)
        
        # Analytics agent analyzes results
        insights = await self.analytics_agent.execute(optimization)
        
        return {
            "strategy": strategy,
            "content": content,
            "optimization": optimization,
            "insights": insights
        }
```

#### 3-Agent Pattern (8 integrations)
**Medium complexity**: Instagram, LinkedIn, YouTube, Google Search Console, Google Ads, Google Analytics, OpenAI, Anthropic Claude

```python
class ThreeAgentCrew:
    """3-Agent pattern for medium integrations"""
    
    def __init__(self, integration: str):
        self.management_agent = Agent(
            role="Management Agent",
            goal="Strategic planning and coordination"
        )
        
        self.optimization_agent = Agent(
            role="Optimization Agent",
            goal="Improve performance and efficiency"
        )
        
        self.analytics_agent = Agent(
            role="Analytics Agent",
            goal="Track metrics and generate insights"
        )
```

#### 2-Agent Pattern (12 integrations)
**Standard complexity**: Twitter/X, TikTok, Pinterest, Google My Business, Bing, Facebook Ads, Razorpay, Amazon SES, SendGrid, Twilio, HubSpot, Calendly

```python
class TwoAgentCrew:
    """2-Agent pattern for standard integrations"""
    
    def __init__(self, integration: str):
        self.operations_agent = Agent(
            role="Operations Agent",
            goal="Execute core functionality"
        )
        
        self.analytics_agent = Agent(
            role="Analytics Agent",
            goal="Monitor and report"
        )
```

#### Single Agent (14 integrations)
**Simple APIs**: Yandex, Baidu, DuckDuckGo, various Amazon APIs, Brevo, Mailchimp, ElevenLabs, Deepgram, Slack

```python
class SingleAgentCrew:
    """Single agent for simple integrations"""
    
    def __init__(self, integration: str):
        self.unified_agent = Agent(
            role="Unified Agent",
            goal="Handle all integration functionality"
        )
```

## API Layer

### Execute Agent Crew
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/agents", tags=["AI Agents"])

class CrewExecutionRequest(BaseModel):
    integration: str
    action: str
    data: dict

@router.post("/execute")
async def execute_crew(
    request: CrewExecutionRequest,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """
    Execute AI agent crew for specific integration
    
    Example:
    POST /agents/execute
    {
        "integration": "facebook",
        "action": "create_campaign",
        "data": {
            "name": "Summer Sale 2025",
            "budget": 5000,
            "target_audience": {...}
        }
    }
    """
    # Determine agent pattern
    pattern = determine_agent_pattern(request.integration)
    
    # Load crew configuration
    crew_config = await crew_repository.get_by_integration(
        request.integration, 
        tenant_id
    )
    
    if not crew_config:
        raise HTTPException(status_code=404, detail="Crew not found")
    
    # Create execution context
    context = ExecutionContext(
        tenant_id=tenant_id,
        integration=request.integration,
        action=request.action,
        data=request.data
    )
    
    # Execute crew
    execution_id = crew_config.execute(context)
    
    # Publish domain events
    for event in crew_config.domain_events:
        await event_bus.publish(event)
    
    return {
        "execution_id": str(execution_id),
        "status": "started",
        "pattern": pattern.value,
        "agents": len(crew_config.agents)
    }

@router.get("/execution/{execution_id}")
async def get_execution_status(
    execution_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Get crew execution status"""
    execution = await execution_repository.get_by_id(execution_id)
    
    if not execution or execution.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return {
        "execution_id": str(execution_id),
        "status": execution.status.value,
        "progress": execution.calculate_progress(),
        "tasks_completed": len([t for t in execution.tasks if t.status == TaskStatus.COMPLETED]),
        "tasks_total": len(execution.tasks),
        "result": execution.result if execution.status == CrewStatus.COMPLETED else None
    }
```

### Human-in-the-Loop (HITL) Endpoints
```python
@router.get("/hitl/pending")
async def get_pending_hitl_tasks(
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Get tasks requiring HITL approval"""
    tasks = await task_repository.get_pending_hitl(tenant_id)
    
    return {
        "tasks": [
            {
                "task_id": str(task.id),
                "description": task.description,
                "data": task.input_data,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]
    }

@router.post("/hitl/{task_id}/approve")
async def approve_hitl_task(
    task_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant)
):
    """Approve HITL task"""
    task = await task_repository.get_by_id(task_id)
    
    if not task or task.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.approve_hitl()
    await task_repository.save(task)
    
    # Resume task execution
    await task_executor.resume(task_id)
    
    return {"status": "approved"}
```

## Integration Management

### Vault Credentials Integration
```python
class CredentialManager:
    """Manage API credentials from Vault"""
    
    def __init__(self, vault_client):
        self.vault = vault_client
    
    async def get_integration_credentials(
        self,
        integration: str,
        tenant_id: UUID
    ) -> dict:
        """Get credentials for integration from Vault"""
        path = f"secret/tenant/{tenant_id}/integrations/{integration}"
        
        try:
            credentials = await self.vault.get_secret(path)
            return credentials
        except Exception as e:
            raise ValueError(f"Failed to get credentials for {integration}: {e}")
    
    async def validate_credentials(
        self,
        integration: str,
        credentials: dict
    ) -> bool:
        """Validate credentials by making test API call"""
        adapter = get_integration_adapter(integration)
        return await adapter.test_connection(credentials)
```

## Configuration

```bash
# AI Agents Service
AI_AGENTS_HOST=0.0.0.0
AI_AGENTS_PORT=8000
LOG_LEVEL=info

# CrewAI Configuration
CREWAI_MAX_CONCURRENT_CREWS=10
CREWAI_TASK_TIMEOUT=3600  # 1 hour

# LangChain Configuration
LANGCHAIN_TRACING=true
LANGCHAIN_ENDPOINT=http://langchain-server:8000

# AI Providers (from Vault)
OPENAI_API_KEY=vault:secret/apis/openai#api_key
ANTHROPIC_API_KEY=vault:secret/apis/anthropic#api_key

# Database
DATABASE_URL=postgresql://postgres:password@bizosaas-postgres-staging:5432/bizosaas_platform

# Redis (task queue)
REDIS_URL=redis://bizosaas-redis-staging:6379/1

# Vault
VAULT_ADDR=http://bizosaas-vault-staging:8200
VAULT_TOKEN=${VAULT_TOKEN}
```

## Deployment Checklist
- [x] AI Agents container deployed
- [x] CrewAI framework configured
- [x] LangChain integration active
- [x] Vault credentials accessible
- [x] Redis task queue configured
- [x] All 93 agents registered
- [x] HITL workflows implemented
- [ ] Integration tests passing (needs validation)

---
**Status**: ✅ Running (needs validation)
**Last Updated**: October 15, 2025
**Owner**: Backend Team
