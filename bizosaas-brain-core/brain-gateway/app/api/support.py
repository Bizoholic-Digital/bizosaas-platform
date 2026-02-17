from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.domain.ports.identity_port import AuthenticatedUser
from app.models.support import SupportTicket
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.models.support import SupportTicket, TicketMessage
from app.core.intelligence import call_ai_agent_with_rag
from app.api.agents import AGENTS
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/support", tags=["support"])

class TicketCreate(BaseModel):
    subject: str
    description: str
    category: Optional[str] = None
    priority: str = "medium"

class TicketMessageCreate(BaseModel):
    content: str

@router.post("/tickets")
async def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Create a new support ticket."""
    ticket = SupportTicket(
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
    
    # ticket is already added/committed above
    
    # 1. Create Initial User Message
    user_msg = TicketMessage(
        ticket_id=ticket.id,
        sender_id=user.id,
        sender_type="user",
        content=ticket_in.description
    )
    db.add(user_msg)
    
    # 2. Trigger AI Agent for Auto-Triage
    try:
        # specific agent for support
        agent_id = "customer-support"
        
        # Construct context
        context = {
            "ticket_id": str(ticket.id),
            "subject": ticket.subject,
            "category": ticket.category,
            "priority": ticket.priority,
            "user_role": user.role
        }

        result = await call_ai_agent_with_rag(
            agent_type=agent_id,
            task_description=ticket_in.description,
            payload=context,
            tenant_id=str(user.tenant_id),
            agent_id=str(user.id),
            priority="high",
            use_rag=True
        )
        
        ai_response = result.get("response")
        
        if ai_response:
            # 3. Create AI Response Message
            ai_msg = TicketMessage(
                ticket_id=ticket.id,
                sender_id=None, # System/AI
                sender_type="ai",
                content=ai_response
            )
            db.add(ai_msg)
            
            # Update ticket status if AI thinks it resolved it? 
            # For now, keep open but maybe tag as "replied"
            
    except Exception as e:
        logger.error(f"Failed to trigger support agent: {e}")
        # Non-blocking failure
        
    db.commit()
    db.refresh(ticket)
    
    return ticket

@router.post("/tickets/{ticket_id}/reply")
async def reply_ticket(
    ticket_id: str,
    message_in: TicketMessageCreate,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Add a reply to a ticket (User or Partner)"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == uuid.UUID(ticket_id)).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    # Permission check (User owns ticket OR is Partner)
    if user.role not in ["partner", "admin"] and ticket.tenant_id != user.tenant_id:
         raise HTTPException(status_code=403, detail="Not authorized")

    # Add Message
    msg = TicketMessage(
        ticket_id=ticket.id,
        sender_id=user.id,
        sender_type="user" if user.role == "client" else "agent",
        content=message_in.content
    )
    db.add(msg)
    
    # If user replied, triggering AI again could be annoying unless specifically requested.
    # For now, just save the message.
    
    db.commit()
    return msg

@router.get("/tickets")
async def list_tickets(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List tickets for the current tenant or assigned to the partner."""
    # If user is a client, show their tenant's tickets
    if user.role == "client" or user.role == "user":
        return db.query(SupportTicket).filter(SupportTicket.tenant_id == user.tenant_id).all()
    
    # If user is a partner, show tickets assigned to them
    if user.role == "partner":
        return db.query(SupportTicket).filter(SupportTicket.assigned_partner_id == user.id).all()
        
    return []

@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == uuid.UUID(ticket_id)).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
