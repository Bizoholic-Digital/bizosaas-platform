from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from domain.ports.identity_port import AuthenticatedUser
from app.models.support import Ticket
from pydantic import BaseModel
from typing import List, Optional
import uuid

router = APIRouter(prefix="/api/support", tags=["support"])

class TicketCreate(BaseModel):
    subject: str
    description: str
    category: Optional[str] = None
    priority: str = "medium"

@router.post("/tickets")
async def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Create a new support ticket."""
    ticket = Ticket(
        tenant_id=user.tenant_id,
        creator_id=user.id,
        subject=ticket_in.subject,
        description=ticket_in.description,
        category=ticket_in.category,
        priority=ticket_in.priority
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # TODO: Trigger AI agent for auto-triage
    
    return ticket

@router.get("/tickets")
async def list_tickets(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List tickets for the current tenant or assigned to the partner."""
    # If user is a client, show their tenant's tickets
    if user.role == "client" or user.role == "user":
        return db.query(Ticket).filter(Ticket.tenant_id == user.tenant_id).all()
    
    # If user is a partner, show tickets assigned to them
    if user.role == "partner":
        return db.query(Ticket).filter(Ticket.assigned_partner_id == user.id).all()
        
    return []

@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == uuid.UUID(ticket_id)).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
