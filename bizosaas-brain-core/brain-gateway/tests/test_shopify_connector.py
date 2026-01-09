import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.connectors.shopify import ShopifyConnector

@pytest.fixture
def shopify_credentials():
    return {
        "shop_url": "test-shop.myshopify.com",
        "access_token": "shpat_test_token_123"
    }

@pytest.fixture
def connector(shopify_credentials):
    return ShopifyConnector("tenant_1", shopify_credentials)

@pytest.mark.asyncio
async def test_shopify_validate_credentials_success(connector):
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_instance
        
        assert await connector.validate_credentials() is True

@pytest.mark.asyncio
async def test_shopify_validate_credentials_failure(connector):
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_instance
        
        assert await connector.validate_credentials() is False

@pytest.mark.asyncio
async def test_shopify_sync_products(connector):
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"products": [{"id": 1, "title": "Test Product"}]}
        mock_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_instance
        
        result = await connector.sync_data("products")
        assert len(result["data"]) == 1
        assert result["data"][0]["title"] == "Test Product"

@pytest.mark.asyncio
async def test_shopify_create_product(connector):
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"product": {"id": 123, "title": "New Product"}}
        mock_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_instance
        
        result = await connector.perform_action("create_product", {"title": "New Product"})
        assert result["product"]["id"] == 123
        assert result["product"]["title"] == "New Product"

@pytest.mark.asyncio
async def test_shopify_unsupported_action(connector):
    with pytest.raises(ValueError, match="Unsupported action"):
        await connector.perform_action("unsupported_action", {})
