import pytest
from unittest.mock import AsyncMock, patch
from app.connectors.llm import OpenAIConnector, AnthropicConnector, OpenRouterConnector, GoogleAIConnector
from app.connectors.base import ConnectorStatus

@pytest.mark.asyncio
async def test_openai_connector_validation():
    credentials = {"api_key": "sk-test-key"}
    connector = OpenAIConnector(tenant_id="test", credentials=credentials)
    
    with patch("httpx.AsyncClient.get") as mock_get:
        # Mock success
        mock_get.return_value = AsyncMock(status_code=200)
        assert await connector.validate_credentials() is True
        
        # Mock failure
        mock_get.return_value = AsyncMock(status_code=401)
        assert await connector.validate_credentials() is False

@pytest.mark.asyncio
async def test_anthropic_connector_validation():
    credentials = {"api_key": "sk-ant-test-key"}
    connector = AnthropicConnector(tenant_id="test", credentials=credentials)
    
    with patch("httpx.AsyncClient.post") as mock_post:
        # Mock success
        mock_post.return_value = AsyncMock(status_code=200)
        assert await connector.validate_credentials() is True
        
        # Mock failure
        mock_post.return_value = AsyncMock(status_code=401)
        assert await connector.validate_credentials() is False

@pytest.mark.asyncio
async def test_openrouter_connector_validation():
    credentials = {"api_key": "sk-or-test-key"}
    connector = OpenRouterConnector(tenant_id="test", credentials=credentials)
    
    with patch("httpx.AsyncClient.get") as mock_get:
        # Mock success
        mock_get.return_value = AsyncMock(status_code=200)
        assert await connector.validate_credentials() is True
        
        # Mock failure
        mock_get.return_value = AsyncMock(status_code=401)
        assert await connector.validate_credentials() is False

@pytest.mark.asyncio
async def test_google_ai_connector_validation():
    credentials = {"api_key": "test-google-key"}
    connector = GoogleAIConnector(tenant_id="test", credentials=credentials)
    
    with patch("httpx.AsyncClient.get") as mock_get:
        # Mock success
        mock_get.return_value = AsyncMock(status_code=200)
        assert await connector.validate_credentials() is True
        
        # Mock failure
        mock_get.return_value = AsyncMock(status_code=401)
        assert await connector.validate_credentials() is False

@pytest.mark.asyncio
async def test_llm_connector_status():
    credentials = {"api_key": "test"}
    connector = OpenAIConnector(tenant_id="test", credentials=credentials)
    
    with patch.object(OpenAIConnector, "validate_credentials", return_value=AsyncMock(return_value=True)):
        # Wait, validate_credentials is an async method, so it should return True directly if mocked with AsyncMock return_value
        connector.validate_credentials = AsyncMock(return_value=True)
        status = await connector.get_status()
        assert status == ConnectorStatus.CONNECTED
        
        connector.validate_credentials = AsyncMock(return_value=False)
        status = await connector.get_status()
        assert status == ConnectorStatus.ERROR
