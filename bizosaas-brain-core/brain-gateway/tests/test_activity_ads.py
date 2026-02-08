import pytest
import asyncio
from unittest.mock import MagicMock
import sys

# Mock what's needed for the activity if it imports anything heavy
sys.modules["app.connectors.registry"] = MagicMock()

from app.activities.marketing import optimize_ad_budgets

@pytest.mark.asyncio
async def test_ad_optimization_logic():
    params = {
        "tenant_id": "bizoholic",
        "current_budgets": {
            "meta": 1000.0,
            "google": 2000.0,
            "meesho": 500.0
        }
    }
    
    result = await optimize_ad_budgets(params)
    
    print(f"\nOptimization Result: {result}")
    
    assert result["status"] == "optimized"
    assert "new_budgets" in result
    assert result["new_budgets"]["meta"] == 1200.0  # Increased by 20% since ROAS 4.2 > 4.0
    assert result["new_budgets"]["google"] == 1600.0 # Decreased by 20% since ROAS 2.1 < 2.5
    assert result["new_budgets"]["meesho"] == 600.0  # Increased by 20% since ROAS 5.8 > 4.0
    assert "recommendations" in result
    assert len(result["recommendations"]) == 3
