"""
BizoSaaS Agent Orchestration Service - Focused Microservice
Coordinates AI agent tasks and maintains task state
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(str, Enum):
    MARKETING_STRATEGIST = "marketing_strategist"
    CONTENT_CREATOR = "content_creator"
    SEO_ANALYZER = "seo_analyzer"
    LEAD_SCORER = "lead_scorer"
    REPORT_GENERATOR = "report_generator"

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskRequest(BaseModel):
    tenant_id: int
    agent_type: AgentType
    task_description: str
    parameters: Dict[str, Any] = {}
    priority: str = "normal"

class TaskResponse(BaseModel):
    task_id: str
    tenant_id: int
    agent_type: AgentType
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

# In-memory task storage (use Redis/DB in production)
tasks: Dict[str, TaskResponse] = {}

app = FastAPI(
    title="BizoSaaS Agent Orchestration Service",
    description="Coordinates AI agent tasks and maintains state",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "agent-orchestration"}

@app.get("/")
async def root():
    return {
        "service": "BizoSaaS Agent Orchestration Service",
        "version": "1.0.0",
        "status": "running",
        "capabilities": [
            "Task coordination",
            "State management",
            "Agent routing"
        ]
    }

@app.post("/orchestrate", response_model=TaskResponse)
async def orchestrate_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Create and coordinate an AI agent task"""
    task_id = str(uuid.uuid4())
    
    task = TaskResponse(
        task_id=task_id,
        tenant_id=request.tenant_id,
        agent_type=request.agent_type,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )
    
    tasks[task_id] = task
    
    # Add background task to route to appropriate service
    background_tasks.add_task(route_to_agent_service, task_id, request)
    
    return task

async def route_to_agent_service(task_id: str, request: TaskRequest):
    """Route task to appropriate specialized AI service"""
    try:
        tasks[task_id].status = TaskStatus.PROCESSING
        
        # Route to specialized services based on agent type
        service_map = {
            AgentType.MARKETING_STRATEGIST: "http://bizosaas-marketing-ai:8007",
            AgentType.CONTENT_CREATOR: "http://bizosaas-marketing-ai:8007", 
            AgentType.SEO_ANALYZER: "http://bizosaas-analytics-ai:8008",
            AgentType.LEAD_SCORER: "http://bizosaas-analytics-ai:8008",
            AgentType.REPORT_GENERATOR: "http://bizosaas-analytics-ai:8008"
        }
        
        target_service = service_map.get(request.agent_type)
        if not target_service:
            raise ValueError(f"No service found for agent type: {request.agent_type}")
        
        logger.info(f"Routing task {task_id} to {target_service}")
        
        # Mock successful completion (replace with actual service call)
        tasks[task_id].status = TaskStatus.COMPLETED
        tasks[task_id].completed_at = datetime.now()
        tasks[task_id].result = {
            "routed_to": target_service,
            "agent_type": request.agent_type,
            "message": "Task routed successfully"
        }
        
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        tasks[task_id].status = TaskStatus.FAILED
        tasks[task_id].error = str(e)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return tasks[task_id]

@app.get("/tasks")
async def list_tasks(tenant_id: Optional[int] = None, status: Optional[TaskStatus] = None):
    """List tasks with optional filtering"""
    filtered_tasks = tasks.values()
    
    if tenant_id:
        filtered_tasks = [t for t in filtered_tasks if t.tenant_id == tenant_id]
    
    if status:
        filtered_tasks = [t for t in filtered_tasks if t.status == status]
    
    return {"tasks": list(filtered_tasks)}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks[task_id]
    return {"message": f"Task {task_id} deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)