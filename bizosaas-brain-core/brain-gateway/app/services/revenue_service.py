from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
from app.models.revenue import PortalRevenue, DomainInventory
from app.models.user import User

class RevenueService:
    def __init__(self, db: Session):
        self.db = db

    async def log_revenue(self, data: Dict[str, Any]) -> PortalRevenue:
        """Log platform revenue from various sources"""
        revenue = PortalRevenue(
            tenant_id=data.get("tenant_id"),
            user_id=data.get("user_id"),
            source_type=data.get("source_type"), # 'domain_purchase', 'affiliate_commission'
            source_id=data.get("source_id"),
            partner_name=data.get("partner_name"),
            amount=data.get("amount"),
            currency=data.get("currency", "USD"),
            commission_amount=data.get("commission_amount", 0.0),
            partner_payout=data.get("partner_payout", 0.0),
            status=data.get("status", "pending"),
            details=data.get("details", {})
        )
        self.db.add(revenue)
        self.db.commit()
        self.db.refresh(revenue)
        return revenue

    async def get_stats(self) -> Dict[str, Any]:
        """Aggregate revenue stats for admin dashboard"""
        total_revenue = self.db.query(func.sum(PortalRevenue.amount)).scalar() or 0.0
        total_commission = self.db.query(func.sum(PortalRevenue.commission_amount)).scalar() or 0.0
        
        # Last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_revenue = self.db.query(func.sum(PortalRevenue.amount)).filter(
            PortalRevenue.created_at >= thirty_days_ago
        ).scalar() or 0.0
        
        # Group by source
        by_source = self.db.query(
            PortalRevenue.source_type, 
            func.sum(PortalRevenue.amount)
        ).group_by(PortalRevenue.source_type).all()
        
        return {
            "total_revenue": total_revenue,
            "total_commission": total_commission,
            "recent_30d_revenue": recent_revenue,
            "sources": {s: a for s, a in by_source}
        }

    async def get_recent_transactions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent revenue transactions with user context"""
        transactions = self.db.query(PortalRevenue).order_by(
            PortalRevenue.created_at.desc()
        ).limit(limit).all()
        
        result = []
        for t in transactions:
            user = self.db.query(User).filter(User.id == t.user_id).first()
            result.append({
                "id": str(t.id),
                "source_type": t.source_type,
                "partner": t.partner_name,
                "amount": t.amount,
                "commission": t.commission_amount,
                "status": t.status,
                "user_email": user.email if user else "Unknown",
                "created_at": t.created_at
            })
        return result

class DomainService:
    def __init__(self, db: Session):
        self.db = db

    async def register_domain(self, data: Dict[str, Any]) -> DomainInventory:
        """Log a new domain registration"""
        domain = DomainInventory(
            tenant_id=data.get("tenant_id"),
            user_id=data.get("user_id"),
            domain_name=data.get("domain_name"),
            registrar=data.get("registrar"),
            expiry_date=data.get("expiry_date"),
            target_service=data.get("target_service"),
            target_slug=data.get("target_slug"),
            status="active"
        )
        self.db.add(domain)
        self.db.commit()
        self.db.refresh(domain)
        return domain

    async def get_all_domains(self) -> List[DomainInventory]:
        """List all domains registered on the platform"""
        return self.db.query(DomainInventory).order_by(DomainInventory.created_at.desc()).all()
