"""
Cost Optimization API
Exposes cost-saving recommendations to the Admin Portal.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, require_role
from app.services.cost_optimization import CostOptimizationEngine
from app.domain.ports.identity_port import AuthenticatedUser

router = APIRouter(prefix="/api/admin/billing/optimization", tags=["cost-optimization"])


@router.get("/recommendations")
async def get_cost_recommendations(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """
    Get a list of cost optimization recommendations.
    """
    optimizer = CostOptimizationEngine(db)
    recommendations = await optimizer.generate_recommendations()
    
    return {
        "status": "success",
        "total_recommendations": len(recommendations),
        "potential_monthly_savings": sum(r["potential_savings"] for r in recommendations) * 30, # Estimated
        "recommendations": recommendations
    }
