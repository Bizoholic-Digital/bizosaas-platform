import pytest
import os
from app.adapters.temporal_adapter import TemporalAdapter

@pytest.mark.asyncio
async def test_temporal_adapter_interface():
    """
    Test TemporalAdapter. 
    Requires TEMPORAL_HOST to be set for real integration.
    """
    temporal_host = os.getenv("TEMPORAL_HOST")
    
    if not temporal_host:
        # Mock test
        from unittest.mock import MagicMock, AsyncMock
        with pytest.MonkeyPatch.context() as mp:
            mock_client = AsyncMock()
            mp.setattr("temporalio.client.Client.connect", AsyncMock(return_value=mock_client))
            
            adapter = TemporalAdapter(temporal_host="localhost:7233")
            # We need to manually set the client since connect is called inside methods
            adapter._client = mock_client
            
            # Test get_workflow_status
            mock_handle = MagicMock()
            mock_handle.describe = AsyncMock()
            mock_client.get_workflow_handle.return_value = mock_handle
            
            status = await adapter.get_workflow_status("test-id")
            assert status is not None
    else:
        # Real integration test (very basic connectivity)
        try:
            adapter = TemporalAdapter(temporal_host=temporal_host)
            # Try to connect
            await adapter._get_client()
            assert adapter._client is not None
        except Exception as e:
            pytest.skip(f"Temporal not reachable at {temporal_host}: {e}")
