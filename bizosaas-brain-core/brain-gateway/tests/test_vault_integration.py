import pytest
import os
import hvac
from app.adapters.vault_adapter import VaultAdapter

@pytest.mark.asyncio
async def test_vault_adapter_interface():
    """
    Test VaultAdapter with a mock client to verify internal logic.
    For a real integration test, set VAULT_ADDR and VAULT_TOKEN.
    """
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    
    if not vault_addr or not vault_token:
        # Mock test if no real vault
        from unittest.mock import MagicMock
        with pytest.MonkeyPatch.context() as mp:
            mock_hvac = MagicMock()
            mp.setattr("hvac.Client", lambda url: mock_hvac)
            mock_hvac.is_authenticated.return_value = True
            
            adapter = VaultAdapter(vault_url="http://mock:8200", vault_token="test")
            
            # Test store
            mock_hvac.secrets.kv.v2.create_or_update_secret.return_value = {}
            success = await adapter.store_secret("test/path", {"key": "value"})
            assert success is True
            
            # Test get
            mock_hvac.secrets.kv.v2.read_secret_version.return_value = {"data": {"data": {"key": "value"}}}
            secret = await adapter.get_secret("test/path")
            assert secret == {"key": "value"}
    else:
        # Real integration test
        adapter = VaultAdapter(vault_url=vault_addr, vault_token=vault_token)
        
        test_path = "test/integration-test"
        test_data = {"foo": "bar"}
        
        try:
            # Store
            success = await adapter.store_secret(test_path, test_data)
            assert success is True
            
            # Get
            retrieved = await adapter.get_secret(test_path)
            assert retrieved == test_data
            
            # List
            prefix = "test"
            keys = await adapter.list_secrets(prefix)
            assert "integration-test" in keys
            
            # Delete
            deleted = await adapter.delete_secret(test_path)
            assert deleted is True
            
        except Exception as e:
            pytest.fail(f"Vault integration failed: {e}")
