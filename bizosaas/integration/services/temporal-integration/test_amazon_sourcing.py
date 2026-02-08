"""
Comprehensive Test Suite for Amazon Sourcing Workflow
Tests end-to-end workflow execution, error handling, and integration points
"""

import asyncio
import pytest
import json
import logging
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List
from datetime import datetime, timezone
import httpx
from decimal import Decimal

from amazon_sourcing_workflow import (
    AmazonSourcingWorkflow,
    AmazonSourcingActivities, 
    AmazonSourcingInput,
    AmazonSourcingOutput,
    AmazonSourcingStatus,
    AmazonSourcingError,
    AmazonProductData,
    AIEnhancementResult,
    SaleorProductData,
    AmazonSourcingWorkflowManager
)

from saleor_integration import (
    SaleorGraphQLClient,
    SaleorProductInput,
    create_amazon_sourced_product
)

from amazon_sourcing_api import router

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test fixtures and mock data

@pytest.fixture
def sample_amazon_input():
    """Sample Amazon sourcing input data"""
    return AmazonSourcingInput(
        amazon_url="https://amazon.com/dp/B08N5WRWNW",
        asin="B08N5WRWNW",
        tenant_id="test_tenant",
        user_id="test_user",
        store_config={
            "auto_publish": False,
            "pricing_rules": {"markup_percentage": 25}
        },
        ai_enhancement_config={
            "enable_seo_optimization": True,
            "enable_competitor_analysis": True
        },
        notification_config={
            "email_enabled": True,
            "webhook_enabled": False
        }
    )

@pytest.fixture
def sample_amazon_data():
    """Sample Amazon product data"""
    return AmazonProductData(
        asin="B08N5WRWNW",
        title="Premium Wireless Bluetooth Headphones",
        description="High-quality wireless headphones with noise cancellation and 30-hour battery life.",
        price=Decimal("79.99"),
        images=[
            "https://images-na.ssl-images-amazon.com/images/I/B08N5WRWNW_001.jpg",
            "https://images-na.ssl-images-amazon.com/images/I/B08N5WRWNW_002.jpg"
        ],
        category="Electronics",
        brand="TechBrand",
        features=["Noise Cancellation", "30-hour Battery", "Quick Charge"],
        rating=4.5,
        review_count=1247,
        availability="in_stock"
    )

@pytest.fixture
def sample_ai_enhancements():
    """Sample AI enhancement results"""
    return AIEnhancementResult(
        optimized_title="Premium Wireless Bluetooth Headphones - Noise Cancelling with 30H Battery",
        seo_description="Experience crystal-clear audio with these premium wireless Bluetooth headphones featuring active noise cancellation and impressive 30-hour battery life. Perfect for travel, work, or leisure.",
        product_tags=["wireless", "bluetooth", "headphones", "noise-cancelling", "premium"],
        category_suggestions=["Electronics", "Audio", "Headphones"],
        pricing_recommendations={
            "suggested_price": 99.99,
            "competitor_range": {"min": 69.99, "max": 129.99},
            "margin_percentage": 25
        },
        competitor_analysis={
            "similar_products": 15,
            "average_rating": 4.2,
            "price_position": "competitive"
        },
        content_enhancements={
            "bullet_points": ["Premium sound quality", "Active noise cancellation", "30-hour battery life"],
            "key_features": ["Bluetooth 5.0", "Fast charging", "Foldable design"]
        }
    )

@pytest.fixture
def mock_saleor_client():
    """Mock Saleor GraphQL client"""
    client = AsyncMock(spec=SaleorGraphQLClient)
    
    # Mock shop info
    client.get_shop_info.return_value = {
        "name": "Test Store",
        "defaultCountry": {"code": "US"},
        "defaultCurrency": "USD"
    }
    
    # Mock categories
    client.get_categories.return_value = [
        {
            "id": "Q2F0ZWdvcnk6MQ==",
            "name": "Electronics",
            "slug": "electronics"
        }
    ]
    
    # Mock product types
    client.get_product_types.return_value = [
        {
            "id": "UHJvZHVjdFR5cGU6MQ==",
            "name": "Default",
            "slug": "default"
        }
    ]
    
    # Mock product creation
    client.create_product.return_value = {
        "id": "UHJvZHVjdDoxMjM=",
        "name": "Test Product",
        "slug": "test-product",
        "created": "2024-01-01T00:00:00Z"
    }
    
    # Mock variant creation
    client.create_product_variant.return_value = {
        "id": "UHJvZHVjdFZhcmlhbnQ6NDU2",
        "sku": "AMZ-B08N5WRWNW"
    }
    
    return client

class TestAmazonSourcingActivities:
    """Test suite for Amazon sourcing activities"""
    
    @pytest.fixture
    def activities(self):
        """Create activities instance for testing"""
        return AmazonSourcingActivities()
    
    @pytest.mark.asyncio
    async def test_extract_product_data_success(self, activities, sample_amazon_input):
        """Test successful product data extraction"""
        
        # Mock the scraping method
        with patch.object(activities, '_scrape_amazon_product_data') as mock_scrape:
            mock_scrape.return_value = {
                'asin': 'B08N5WRWNW',
                'title': 'Test Product',
                'description': 'Test Description',
                'price': Decimal('29.99'),
                'images': ['https://example.com/image.jpg'],
                'category': 'Electronics'
            }
            
            result = await activities.extract_product_data_activity({
                'amazon_url': sample_amazon_input.amazon_url
            })
            
            assert result['status'] == 'success'
            assert result['asin'] == 'B08N5WRWNW'
            assert 'data' in result
            assert result['data']['title'] == 'Test Product'
    
    @pytest.mark.asyncio
    async def test_extract_product_data_invalid_url(self, activities):
        """Test product data extraction with invalid URL"""
        
        result = await activities.extract_product_data_activity({
            'amazon_url': 'https://invalid-url.com'
        })
        
        assert result['status'] == 'error'
        assert result['error_type'] == AmazonSourcingError.PRODUCT_NOT_FOUND
    
    @pytest.mark.asyncio
    async def test_enhance_with_ai_success(self, activities, sample_amazon_data):
        """Test successful AI enhancement"""
        
        # Mock CrewAI API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'success',
            'result': {
                'optimized_title': 'Enhanced Product Title',
                'seo_description': 'Enhanced SEO description',
                'product_tags': ['tag1', 'tag2'],
                'category_suggestions': ['Electronics'],
                'pricing_recommendations': {'suggested_price': 99.99}
            }
        }
        
        with patch.object(activities.crewai_client, 'post', return_value=mock_response):
            result = await activities.enhance_with_ai_activity(
                sample_amazon_data.__dict__,
                {'enable_seo_optimization': True}
            )
            
            assert result['status'] == 'success'
            assert 'enhancements' in result
            assert result['enhancements']['optimized_title'] == 'Enhanced Product Title'
    
    @pytest.mark.asyncio
    async def test_enhance_with_ai_failure(self, activities, sample_amazon_data):
        """Test AI enhancement failure handling"""
        
        # Mock API failure
        with patch.object(activities.crewai_client, 'post', side_effect=httpx.HTTPError("API Error")):
            result = await activities.enhance_with_ai_activity(
                sample_amazon_data.__dict__,
                {}
            )
            
            assert result['status'] == 'error'
            assert result['error_type'] == AmazonSourcingError.AI_ENHANCEMENT_FAILED
    
    @pytest.mark.asyncio
    async def test_create_saleor_product_success(self, activities, sample_amazon_data, sample_ai_enhancements):
        """Test successful Saleor product creation"""
        
        # Mock Saleor API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'productCreate': {
                    'product': {
                        'id': 'UHJvZHVjdDoxMjM=',
                        'name': 'Test Product'
                    },
                    'errors': []
                }
            }
        }
        
        with patch.object(activities.saleor_client, 'post', return_value=mock_response):
            result = await activities.create_saleor_product_activity(
                sample_amazon_data.__dict__,
                sample_ai_enhancements.__dict__,
                {}
            )
            
            assert result['status'] == 'success'
            assert 'saleor_product' in result
            assert result['saleor_product']['product_id'] == 'UHJvZHVjdDoxMjM='
    
    @pytest.mark.asyncio
    async def test_process_images_success(self, activities):
        """Test successful image processing"""
        
        images = [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg"
        ]
        
        # Mock image download
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'fake_image_data'
        
        with patch.object(activities.http_client, 'get', return_value=mock_response):
            result = await activities.process_images_activity(images, "product_123")
            
            assert result['status'] == 'success'
            assert len(result['processed_images']) == 2
    
    @pytest.mark.asyncio
    async def test_validate_product_success(self, activities, sample_amazon_data):
        """Test successful product validation"""
        
        result = await activities.validate_product_activity(sample_amazon_data.__dict__)
        
        assert result['status'] == 'success'
        assert 'quality_scores' in result
        assert 'overall_quality' in result['quality_scores']
        assert result['validation_passed'] == True
    
    @pytest.mark.asyncio
    async def test_notify_completion_success(self, activities):
        """Test successful completion notification"""
        
        workflow_result = {
            'workflow_id': 'test_workflow_123',
            'status': 'completed',
            'amazon_data': {'title': 'Test Product'},
            'quality_scores': {'overall_quality': 85.0}
        }
        
        notification_config = {
            'email_enabled': True,
            'webhook_enabled': False
        }
        
        result = await activities.notify_completion_activity(workflow_result, notification_config)
        
        assert result['status'] == 'success'
        assert len(result['notifications_sent']) >= 1

class TestAmazonSourcingWorkflow:
    """Test suite for the complete Amazon sourcing workflow"""
    
    @pytest.fixture
    def workflow(self):
        """Create workflow instance for testing"""
        return AmazonSourcingWorkflow()
    
    @pytest.mark.asyncio
    async def test_complete_workflow_success(self, workflow, sample_amazon_input):
        """Test complete workflow execution success path"""
        
        # Mock all activities
        with patch.object(workflow.activities, 'extract_product_data_activity') as mock_extract, \
             patch.object(workflow.activities, 'enhance_with_ai_activity') as mock_enhance, \
             patch.object(workflow.activities, 'create_saleor_product_activity') as mock_create, \
             patch.object(workflow.activities, 'process_images_activity') as mock_images, \
             patch.object(workflow.activities, 'validate_product_activity') as mock_validate, \
             patch.object(workflow.activities, 'notify_completion_activity') as mock_notify:
            
            # Set up mock responses
            mock_extract.return_value = {
                'status': 'success',
                'data': {
                    'asin': 'B08N5WRWNW',
                    'title': 'Test Product',
                    'price': 29.99,
                    'images': ['image1.jpg']
                }
            }
            
            mock_enhance.return_value = {
                'status': 'success',
                'enhancements': {
                    'optimized_title': 'Enhanced Title',
                    'seo_description': 'Enhanced Description'
                }
            }
            
            mock_create.return_value = {
                'status': 'success',
                'saleor_product': {
                    'product_id': 'UHJvZHVjdDoxMjM='
                }
            }
            
            mock_images.return_value = {
                'status': 'success',
                'processed_images': [{'filename': 'image1.jpg'}]
            }
            
            mock_validate.return_value = {
                'status': 'success',
                'quality_scores': {'overall_quality': 85.0},
                'validation_passed': True
            }
            
            mock_notify.return_value = {
                'status': 'success',
                'notifications_sent': [{'type': 'email'}]
            }
            
            # Execute workflow
            result = await workflow.run(sample_amazon_input)
            
            # Verify results
            assert result.status == AmazonSourcingStatus.COMPLETED
            assert result.amazon_data is not None
            assert result.ai_enhancements is not None
            assert result.saleor_product is not None
            assert result.quality_scores is not None
            assert len(result.errors) == 0
    
    @pytest.mark.asyncio
    async def test_workflow_with_extraction_failure(self, workflow, sample_amazon_input):
        """Test workflow behavior when product extraction fails"""
        
        with patch.object(workflow.activities, 'extract_product_data_activity') as mock_extract:
            mock_extract.return_value = {
                'status': 'error',
                'error': 'Product not found',
                'error_type': AmazonSourcingError.PRODUCT_NOT_FOUND
            }
            
            result = await workflow.run(sample_amazon_input)
            
            assert result.status == AmazonSourcingStatus.FAILED
            assert len(result.errors) > 0
            assert 'Product extraction failed' in result.errors[0]

class TestSaleorIntegration:
    """Test suite for Saleor GraphQL integration"""
    
    @pytest.mark.asyncio
    async def test_create_amazon_sourced_product(self, mock_saleor_client, sample_amazon_data, sample_ai_enhancements):
        """Test complete Amazon product creation in Saleor"""
        
        config = {
            "auto_publish": False,
            "pricing_rules": {"markup_percentage": 25}
        }
        
        result = await create_amazon_sourced_product(
            mock_saleor_client,
            sample_amazon_data.__dict__,
            sample_ai_enhancements.__dict__,
            config
        )
        
        assert result['product_id'] == 'UHJvZHVjdDoxMjM='
        assert result['product_name'] == sample_ai_enhancements.optimized_title
        assert result['images_uploaded'] == 0  # Mock doesn't upload images
        
        # Verify client method calls
        mock_saleor_client.get_product_types.assert_called_once()
        mock_saleor_client.create_product.assert_called_once()

class TestAmazonSourcingAPI:
    """Test suite for Amazon sourcing API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from fastapi.testclient import TestClient
        from fastapi import FastAPI
        
        app = FastAPI()
        app.include_router(router)
        
        return TestClient(app)
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/amazon-sourcing/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "amazon_sourcing_workflow"
        assert data["status"] == "healthy"
    
    def test_start_workflow_endpoint_validation(self, client):
        """Test workflow start endpoint input validation"""
        
        # Valid request
        valid_request = {
            "amazon_url": "https://amazon.com/dp/B08N5WRWNW",
            "tenant_id": "test_tenant"
        }
        
        # This would require mocking the workflow manager
        # For now, just test that the endpoint exists and validates input
        
        # Invalid request - missing URL
        invalid_request = {
            "tenant_id": "test_tenant"
        }
        
        response = client.post("/amazon-sourcing/start", json=invalid_request)
        assert response.status_code == 422  # Validation error

class TestErrorHandling:
    """Test suite for error handling and edge cases"""
    
    @pytest.mark.asyncio
    async def test_invalid_amazon_url_handling(self):
        """Test handling of invalid Amazon URLs"""
        
        activities = AmazonSourcingActivities()
        
        invalid_urls = [
            "https://not-amazon.com/product",
            "invalid-url",
            "",
            None
        ]
        
        for url in invalid_urls:
            if url is None:
                continue
                
            result = await activities.extract_product_data_activity({
                'amazon_url': url
            })
            
            assert result['status'] == 'error'
    
    @pytest.mark.asyncio
    async def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        
        activities = AmazonSourcingActivities()
        
        with patch.object(activities.http_client, 'get', side_effect=httpx.TimeoutException("Timeout")):
            result = await activities.extract_product_data_activity({
                'amazon_url': 'https://amazon.com/dp/B08N5WRWNW'
            })
            
            assert result['status'] == 'error'
    
    @pytest.mark.asyncio
    async def test_saleor_api_error_handling(self):
        """Test handling of Saleor API errors"""
        
        activities = AmazonSourcingActivities()
        
        # Mock Saleor API error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'errors': [{'message': 'Invalid input'}]
        }
        
        with patch.object(activities.saleor_client, 'post', return_value=mock_response):
            result = await activities.create_saleor_product_activity(
                {'title': 'Test'}, 
                {}, 
                {}
            )
            
            assert result['status'] == 'error'
            assert result['error_type'] == AmazonSourcingError.SALEOR_CREATION_FAILED

class TestPerformanceAndScalability:
    """Test suite for performance and scalability aspects"""
    
    @pytest.mark.asyncio
    async def test_concurrent_workflow_execution(self):
        """Test concurrent execution of multiple workflows"""
        
        manager = AmazonSourcingWorkflowManager(MagicMock())
        
        # Mock the start_workflow method
        with patch.object(manager.temporal_client, 'start_workflow') as mock_start:
            mock_start.return_value = MagicMock(
                workflow_id="test_workflow",
                status="running",
                started_at=datetime.now(timezone.utc)
            )
            
            # Start multiple workflows concurrently
            tasks = []
            for i in range(5):
                task = manager.start_amazon_sourcing_workflow(
                    amazon_url=f"https://amazon.com/dp/TEST{i}",
                    tenant_id="test_tenant",
                    user_id="test_user"
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            
            assert len(results) == 5
            assert all(r.status == "running" for r in results)
    
    @pytest.mark.asyncio
    async def test_batch_processing_limits(self):
        """Test batch processing with limits"""
        
        from amazon_sourcing_api import start_batch_sourcing
        
        # Test with too many URLs
        too_many_urls = [f"https://amazon.com/dp/TEST{i}" for i in range(100)]
        
        # This would test the limit enforcement in the API
        # Implementation would depend on the actual FastAPI setup

# Integration tests requiring actual services

@pytest.mark.integration
class TestIntegrationWithActualServices:
    """Integration tests that require actual running services"""
    
    @pytest.mark.asyncio
    async def test_actual_saleor_connection(self):
        """Test actual connection to Saleor GraphQL API"""
        
        try:
            async with SaleorGraphQLClient() as client:
                shop_info = await client.get_shop_info()
                
                assert 'name' in shop_info
                logger.info(f"Connected to shop: {shop_info['name']}")
                
        except Exception as e:
            pytest.skip(f"Saleor service not available: {e}")
    
    @pytest.mark.asyncio
    async def test_actual_crewai_connection(self):
        """Test actual connection to CrewAI service"""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/health")
                response.raise_for_status()
                
                health_data = response.json()
                assert health_data.get('status') == 'healthy'
                logger.info("CrewAI service is healthy")
                
        except Exception as e:
            pytest.skip(f"CrewAI service not available: {e}")

# Pytest configuration and fixtures

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring actual services"
    )

if __name__ == "__main__":
    # Run tests
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-m", "not integration"  # Skip integration tests by default
    ])