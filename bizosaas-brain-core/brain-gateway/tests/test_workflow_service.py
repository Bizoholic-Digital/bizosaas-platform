import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.services.workflow_service import WorkflowService
from app.models.workflow import Workflow

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_workflow_port():
    return AsyncMock()

@pytest.fixture
def service(mock_db, mock_workflow_port):
    return WorkflowService(db=mock_db, workflow_port=mock_workflow_port)

@pytest.mark.asyncio
async def test_create_workflow(service, mock_db):
    data = {
        "name": "Test Workflow",
        "description": "A test workflow",
        "type": "Test",
        "status": "paused"
    }
    tenant_id = "tenant123"
    
    workflow = await service.create_workflow(tenant_id, data)
    
    assert workflow.name == "Test Workflow"
    assert workflow.tenant_id == tenant_id
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_update_config(service, mock_db):
    workflow = Workflow(id="wf1", tenant_id="t1", config={"retries": 1})
    mock_db.query.return_value.filter.return_value.first.return_value = workflow
    
    success = await service.update_config("t1", "wf1", {"retries": 3, "priority": "high"})
    
    assert success is True
    assert workflow.config["retries"] == 3
    assert workflow.config["priority"] == "high"
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_toggle_status(service, mock_db):
    workflow = Workflow(id="wf1", tenant_id="t1", status="paused")
    mock_db.query.return_value.filter.return_value.first.return_value = workflow
    
    new_status = await service.toggle_status("t1", "wf1")
    
    assert new_status == "running"
    assert workflow.status == "running"
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_trigger_workflow_success(service, mock_workflow_port, mock_db):
    workflow = Workflow(id="wf1", tenant_id="t1", name="Sync")
    mock_db.query.return_value.filter.return_value.first.return_value = workflow
    mock_workflow_port.start_workflow.return_value = "run123"
    
    result = await service.trigger_workflow("t1", "wf1", {"key": "val"})
    
    assert result["status"] == "started"
    assert result["run_id"] == "run123"
    mock_workflow_port.start_workflow.assert_called_once_with(
        workflow_name="Sync",
        workflow_id="t1-wf1",
        task_queue="queue-t1",
        args=[{"key": "val"}]
    )

@pytest.mark.asyncio
async def test_trigger_workflow_no_port(mock_db):
    # Service without port
    service_no_port = WorkflowService(db=mock_db, workflow_port=None)
    workflow = Workflow(id="wf1", tenant_id="t1", name="Sync")
    mock_db.query.return_value.filter.return_value.first.return_value = workflow
    
    result = await service_no_port.trigger_workflow("t1", "wf1")
    
    assert result["status"] == "simulated"
