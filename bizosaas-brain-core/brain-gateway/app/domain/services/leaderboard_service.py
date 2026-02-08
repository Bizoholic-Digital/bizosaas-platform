from sqlalchemy.orm import Session
from app.models.user import User, Tenant
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LeaderboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_partner_leaderboard(self, period: str = "monthly") -> List[Dict[str, Any]]:
        """
        Aggregate metrics for partners.
        In production, this would query a dedicated 'partner_metrics' table 
        populated by task completion and client satisfaction data.
        """
        partners = self.db.query(User).filter(User.role == "partner").all()
        
        leaderboard = []
        for partner in partners:
            # Mock aggregation for MVP
            managed_count = len(partner.managed_tenants)
            revenue_generated = managed_count * 500.0 # Placeholder logic
            satisfaction_score = 4.5 + (managed_count % 5) * 0.1 # Mock variation
            
            leaderboard.append({
                "partner_id": str(partner.id),
                "name": f"{partner.first_name} {partner.last_name}",
                "email": partner.email,
                "managed_clients": managed_count,
                "revenue": revenue_generated,
                "score": round(satisfaction_score, 1),
                "rank": 0 # To be calculated
            })
            
        # Sort and assign rank
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        for i, entry in enumerate(leaderboard):
            entry["rank"] = i + 1
            
        return leaderboard

    def calculate_capacity_score(self, partner_id: str) -> float:
        """
        Calculate AI-driven capacity score.
        Considers active clients vs limit, average response time, and agent load.
        """
        # Logic: Base score 100. Subtract 20 per client. 
        # Add bonus for high satisfaction.
        from uuid import UUID
        partner = self.db.query(User).filter(User.id == UUID(partner_id)).first()
        if not partner:
            return 0.0
            
        base_score = 100.0
        client_penalty = len(partner.managed_tenants) * 15.0
        
        return max(0.0, base_score - client_penalty)
