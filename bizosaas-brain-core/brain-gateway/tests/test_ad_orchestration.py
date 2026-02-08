import sys
from unittest.mock import MagicMock

# Mock missing dependencies
sys.modules["razorpay"] = MagicMock()
sys.modules["stripe"] = MagicMock()
sys.modules["pandas"] = MagicMock()
sys.modules["redis"] = MagicMock()
sys.modules["psycopg2"] = MagicMock()
sys.modules["psycopg2.extras"] = MagicMock()
sys.modules["psycopg2.extensions"] = MagicMock()
sys.modules["sqlalchemy.ext.declarative"] = MagicMock()
sys.modules["sqlalchemy.orm"] = MagicMock()
sys.modules["sqlalchemy"] = MagicMock()

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from app.api.dependencies import get_current_user

client = TestClient(app)

# Override the authentication dependency
app.dependency_overrides[get_current_user] = lambda: MagicMock(tenant_id="bizoholic")

@patch("app.api.marketing.Client")
def test_orchestrate_ads(mock_temporal_client):
    # Mock Temporal client
    mock_workflow_handle = MagicMock()
    mock_temporal_client.connect.return_value = MagicMock()
    mock_temporal_client.connect.return_value.start_workflow.return_value = mock_workflow_handle
    
    # Dummy spend data
    current_budgets = {
        "meta": 1000.0,
        "google": 2000.0,
        "meesho": 500.0
    }
    
    response = client.post(
        "/api/marketing/orchestrate-ads",
        json={"current_budgets": current_budgets}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "triggered"
    assert "ad-orchestration-bizoholic" in response.json()["workflow_id"]

def test_ad_optimization_activity():
    from app.activities.marketing import optimize_ad_budgets
    import asyncio
    
    params = {
        "tenant_id": "bizoholic",
        "current_budgets": {
            "meta": 1000.0,
            "google": 2000.0,
            "meesho": 500.0
        }
    }
    
    result = asyncio.run(optimize_ad_budgets(params))
    print(f"\nOptimization Result: {result}")
    
    assert result["status"] == "optimized"
    assert "new_budgets" in result
    assert result["new_budgets"]["meta"] == 1200.0  # Increased by 20% since ROAS 4.2 > 4.0
    assert result["new_budgets"]["google"] == 1600.0 # Decreased by 20% since ROAS 2.1 < 2.5
    assert result["new_budgets"]["meesho"] == 600.0  # Increased by 20% since ROAS 5.8 > 4.0
