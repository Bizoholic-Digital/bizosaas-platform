from sqlalchemy.orm import Session
from app.models.agent import Agent, AgentOptimization
from datetime import datetime
import uuid

class AgentService:
    @staticmethod
    def get_agent_optimizations(db: Session, agent_id: str = None):
        query = db.query(AgentOptimization)
        if agent_id:
            query = query.filter(AgentOptimization.agent_id == agent_id)
        return query.order_by(AgentOptimization.suggested_at.desc()).all()

    @staticmethod
    def approve_optimization(db: Session, optimization_id: str):
        opt = db.query(AgentOptimization).filter(AgentOptimization.id == optimization_id).first()
        if opt:
            opt.status = "approved"
            db.commit()
            return opt
        return None

    @staticmethod
    def toggle_auto_execute(db: Session, optimization_id: str, enabled: bool):
        opt = db.query(AgentOptimization).filter(AgentOptimization.id == optimization_id).first()
        if opt:
            opt.auto_execute = enabled
            db.commit()
            return opt
        return None

    @staticmethod
    def create_mock_optimizations(db: Session, agent_id: str):
        """Helper for demo purposes to populate optimizations."""
        mocks = [
            {
                "type": "prompt",
                "description": "Redundant greeting in system prompt",
                "improvement": "Remove 'Hello, I am your assistant' from the start to save tokens.",
                "impact": "Low"
            },
            {
                "type": "performance",
                "description": "High latency on customer queries",
                "improvement": "Use gpt-4o-mini for simple classification tasks before hitting main model.",
                "impact": "High"
            },
            {
                "type": "cost",
                "description": "Expensive model used for summarization",
                "improvement": "Switch summarization steps to Claude 3 Haiku.",
                "impact": "Medium"
            }
        ]
        
        created = []
        for mock in mocks:
            opt = AgentOptimization(
                agent_id=agent_id,
                **mock
            )
            db.add(opt)
            created.append(opt)
        
        db.commit()
        return created
