from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.database import get_db
from app.dependencies import get_current_user
from app.models.client_task import ClientTask

router = APIRouter(prefix="/client-tasks", tags=["Client Tasks"])

class ClientTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    metadata_json: Optional[dict] = None

class ClientTaskUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

# List Tasks (for Client Portal)
@router.get("/", response_model=List[dict])
def list_client_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Filter by user's tenant
    tasks = db.query(ClientTask).filter(ClientTask.tenant_id == current_user.tenant_id).all()
    return [t.to_dict() for t in tasks]

# Create Task (User or Agent calls this)
@router.post("/", response_model=dict)
def create_client_task(
    task_in: ClientTaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_task = ClientTask(
        tenant_id=current_user.tenant_id,
        title=task_in.title,
        description=task_in.description,
        priority=task_in.priority,
        due_date=task_in.due_date,
        metadata_json=task_in.metadata_json,
        # TODO: If called by Agent, set created_by_agent_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task.to_dict()

# Update Status
@router.patch("/{task_id}", response_model=dict)
def update_client_task(
    task_id: str,
    update_in: ClientTaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(ClientTask).filter(
        ClientTask.id == task_id, 
        ClientTask.tenant_id == current_user.tenant_id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if update_in.status:
        task.status = update_in.status
    if update_in.title:
        task.title = update_in.title
    if update_in.description:
        task.description = update_in.description
        
    db.commit()
    db.refresh(task)
    return task.to_dict()
