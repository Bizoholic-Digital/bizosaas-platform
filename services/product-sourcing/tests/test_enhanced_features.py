#!/usr/bin/env python3
"""
Enhanced Feature Tests for Product Sourcing Workflow [P8]
Tests new functionality including Indian market optimization, enhanced Amazon integration,
and improved AI scoring algorithms
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Test client
client = TestClient(app)

# Indian Market Optimization Tests
class TestIndianMarketOptimization:
    """Test Indian market optimization functionality"""
    
    def test_indian_market_analysis_endpoint(self):
        """Test Indian market analysis endpoint"""
        payload = {
            "product_title": "Wireless Gaming Mouse",
            "current_price": 3499,
            "category": "electronics"
        }
        
        response = client.post("/api/product-sourcing/indian-market-analysis", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "indian_market_analysis" in data
        assert "optimization_results" in data["indian_market_analysis"]
        assert "analysis_summary" in data["indian_market_analysis"]
        assert "market_viability" in data["indian_market_analysis"]["analysis_summary"]
    
    def test_regional_insights_endpoint(self):
        """Test regional insights endpoint"""
        response = client.get("/api/product-sourcing/indian-market/regional-insights?category=electronics&price_range=mid_range")
        assert response.status_code == 200
        
        data = response.json()
        assert "regional_insights" in data
        assert "regional_demand" in data["regional_insights"]
        assert "target_regions" in data["regional_insights"]
        assert "cultural_considerations" in data["regional_insights"]
    
    def test_festival_calendar_endpoint(self):
        """Test festival calendar endpoint"""
        response = client.get("/api/product-sourcing/festival-calendar")
        assert response.status_code == 200
        
        data = response.json()
        assert "festival_calendar" in data
        assert "major_festivals" in data["festival_calendar"]
        assert "seasonal_trends" in data["festival_calendar"]
        assert "regional_festivals" in data["festival_calendar"]
    
    def test_gst_calculator_endpoint(self):
        """Test GST calculator endpoint"""
        response = client.get("/api/product-sourcing/gst-calculator?price=5000&category=electronics")
        assert response.status_code == 200
        
        data = response.json()
        assert "gst_calculation" in data
        assert "gst_rate" in data["gst_calculation"]
        assert "gst_amount" in data["gst_calculation"]
        assert "total_price_including_gst" in data["gst_calculation"]
    
    @pytest.mark.asyncio
    async def test_indian_market_optimizer_class(self):
        """Test IndianMarketOptimizer class functionality"""
        try:
            from indian_market_optimizer import IndianMarketOptimizer
            
            optimizer = IndianMarketOptimizer()
            
            product_data = {
                "title": "Smart Fitness Watch",
                "price": 8999,
                "category": "electronics",
                "brand": "TechBrand",
                "rating": 4.3,
                "review_count": 750
            }
            
            result = optimizer.optimize_for_indian_market(product_data)
            
            assert "insights" in result
            assert "market_score" in result
            assert "optimized_pricing" in result
            assert "target_regions" in result
            assert "recommendations" in result
        except ImportError:
            pytest.skip("IndianMarketOptimizer not available")
    
    def test_gst_impact_calculation(self):
        """Test GST impact calculation"""
        try:
            from indian_market_optimizer import IndianMarketOptimizer
            
            optimizer = IndianMarketOptimizer()
            
            # Test electronics (18% GST)
            electronics_product = {"category": "electronics", "price": 10000}
            gst_impact = optimizer._calculate_gst_impact(electronics_product)
            assert 0 <= gst_impact <= 100
            assert "gst_analysis" in electronics_product
            assert electronics_product["gst_analysis"]["applicable_rate"] == 18
            
            # Test books (0% GST)
            books_product = {"category": "books", "price": 500}
            gst_impact_books = optimizer._calculate_gst_impact(books_product)
            assert gst_impact_books >= 90  # High score for low/no GST
        except ImportError:
            pytest.skip("IndianMarketOptimizer not available")

# Enhanced Amazon SP-API Tests
class TestEnhancedAmazonIntegration:
    """Test enhanced Amazon SP-API client"""
    
    @pytest.mark.asyncio
    async def test_enhanced_amazon_client_search(self):
        """Test enhanced Amazon client search functionality"""
        try:
            from amazon_sp_api_client import EnhancedAmazonSPAPIClient
            
            client = EnhancedAmazonSPAPIClient()
            
            # Test with mock credentials (should use mock data)
            products = await client.search_products(["gaming mouse"], "electronics", 10)
            
            assert len(products) <= 10
            for product in products:
                assert hasattr(product, 'asin')
                assert hasattr(product, 'title')
                assert hasattr(product, 'price')
                assert hasattr(product, 'currency')
        except ImportError:
            pytest.skip("EnhancedAmazonSPAPIClient not available")
    
    @pytest.mark.asyncio
    async def test_enhanced_amazon_product_details(self):
        """Test enhanced product details retrieval"""
        try:
            from amazon_sp_api_client import EnhancedAmazonSPAPIClient
            
            client_amazon = EnhancedAmazonSPAPIClient()
            
            # Test with mock ASIN
            details = await client_amazon.get_product_details("B08N5WRWNW")
            
            assert "asin" in details
            assert "title" in details
            assert "price" in details
            assert "currency" in details
            assert "specifications" in details
        except ImportError:
            pytest.skip("EnhancedAmazonSPAPIClient not available")
    
    def test_rate_limiter(self):
        """Test rate limiter functionality"""
        try:
            from amazon_sp_api_client import RateLimiter
            import time
            
            limiter = RateLimiter(calls_per_second=2.0)
            
            start_time = time.time()
            
            # Make two calls - second should be delayed
            asyncio.run(limiter.wait_if_needed())
            asyncio.run(limiter.wait_if_needed())
            
            elapsed_time = time.time() - start_time
            assert elapsed_time >= 0.4  # Should wait at least 0.4 seconds
        except ImportError:
            pytest.skip("RateLimiter not available")

# Enhanced Product Scoring Tests
class TestEnhancedProductScoring:
    """Test enhanced product scoring algorithms"""
    
    @pytest.mark.asyncio
    async def test_enhanced_trend_score_calculation(self):
        """Test enhanced trend score calculation"""
        from main import ProductScoringEngine
        
        engine = ProductScoringEngine()
        
        # Product with viral keywords should get trend boost
        viral_product = {
            "title": "Smart Wireless Portable Mini Device",
            "price": 2999,
            "rating": 4.5,
            "review_count": 1000,
            "category": "electronics",
            "keywords": ["smart", "wireless", "portable"]
        }
        
        trend_score = await engine._calculate_trend_score(viral_product)
        assert 0 <= trend_score <= 100
    
    @pytest.mark.asyncio
    async def test_enhanced_profit_score_calculation(self):
        """Test enhanced profit score calculation with Indian market factors"""
        from main import ProductScoringEngine
        
        engine = ProductScoringEngine()
        
        product_data = {
            "price": 5999,
            "category": "electronics",
            "rating": 4.3,
            "review_count": 500,
            "competitor_count": 75
        }
        
        profit_score = await engine._calculate_profit_score(product_data)
        assert 0 <= profit_score <= 100
        assert "profit_analysis" in product_data
        assert "estimated_cost" in product_data["profit_analysis"]
        assert "amazon_fees" in product_data["profit_analysis"]
    
    @pytest.mark.asyncio 
    async def test_enhanced_competition_score_calculation(self):
        """Test enhanced competition score calculation"""
        from main import ProductScoringEngine
        
        engine = ProductScoringEngine()
        
        high_competition_product = {
            "competitor_count": 200,
            "price": 3999,
            "rating": 4.0,
            "review_count": 300,
            "category": "electronics",
            "brand": "Samsung"
        }
        
        competition_score = await engine._calculate_competition_score(high_competition_product)
        assert 0 <= competition_score <= 100
        assert "competitive_analysis" in high_competition_product
        assert "competition_score" in high_competition_product["competitive_analysis"]
    
    @pytest.mark.asyncio
    async def test_enhanced_risk_score_calculation(self):
        """Test enhanced risk score calculation"""
        from main import ProductScoringEngine
        
        engine = ProductScoringEngine()
        
        product_data = {
            "category": "electronics",
            "price": 7999,
            "rating": 3.8,
            "review_count": 150,
            "seller_type": "Third Party",
            "origin_country": "China"
        }
        
        risk_score = await engine._calculate_risk_score(product_data)
        assert 0 <= risk_score <= 100
        assert "risk_analysis" in product_data
        assert "total_risk_score" in product_data["risk_analysis"]
        assert "risk_level" in product_data["risk_analysis"]
        assert "mitigation_strategies" in product_data["risk_analysis"]
    
    def test_enhanced_product_classification(self):
        """Test enhanced product classification with risk consideration"""
        from main import ProductScoringEngine, ProductCategory
        
        engine = ProductScoringEngine()
        
        # High-trend, low-risk product should be HOOK
        hook_category = engine._classify_product(80, 80, 60, 30)
        assert hook_category == ProductCategory.HOOK
        
        # High-profit, low-risk product should be HERO
        hero_category = engine._classify_product(75, 50, 70, 40)
        assert hero_category == ProductCategory.HERO
        
        # High-risk product should be NOT_QUALIFIED regardless of other scores
        high_risk_category = engine._classify_product(80, 75, 70, 80)
        assert high_risk_category == ProductCategory.NOT_QUALIFIED

# Enhanced Trend Analysis Tests  
class TestEnhancedTrendAnalysis:
    """Test enhanced trend analysis with social media integration"""
    
    @pytest.mark.asyncio
    async def test_enhanced_google_trends(self):
        """Test enhanced Google trends analysis"""
        from main import TrendAnalysisService
        
        service = TrendAnalysisService()
        
        result = await service._analyze_google_trends("wireless earbuds", "30d")
        
        assert "score" in result
        assert "search_volume" in result
        assert "related_queries" in result
        assert "regional_interest" in result
        assert "demographics" in result
        assert "seasonal_data" in result
    
    @pytest.mark.asyncio
    async def test_enhanced_tiktok_trends(self):
        """Test enhanced TikTok trends analysis"""
        from main import TrendAnalysisService
        
        service = TrendAnalysisService()
        
        result = await service._analyze_tiktok_trends("gaming setup", "30d")
        
        assert "score" in result
        assert "video_count" in result
        assert "viral_potential" in result
        assert "trending_hashtags" in result
        assert "audience_demographics" in result
        assert "content_types" in result
    
    @pytest.mark.asyncio
    async def test_enhanced_instagram_trends(self):
        """Test enhanced Instagram trends analysis"""
        from main import TrendAnalysisService
        
        service = TrendAnalysisService()
        
        result = await service._analyze_instagram_trends("aesthetic decor", "30d")
        
        assert "score" in result
        assert "post_count" in result
        assert "influencer_mentions" in result
        assert "top_hashtags" in result
        assert "content_categories" in result
        assert "growth_metrics" in result
    
    @pytest.mark.asyncio
    async def test_enhanced_youtube_trends(self):
        """Test enhanced YouTube trends analysis"""
        from main import TrendAnalysisService
        
        service = TrendAnalysisService()
        
        result = await service._analyze_youtube_trends("tech review", "30d")
        
        assert "score" in result
        assert "video_count" in result
        assert "engagement_metrics" in result
        assert "content_types" in result
        assert "trending_keywords" in result
        assert "seasonal_patterns" in result

# Integration Tests
class TestCompleteWorkflow:
    """Test complete product sourcing workflow"""
    
    @pytest.mark.asyncio
    async def test_complete_product_analysis_workflow(self):
        """Test complete product analysis including Indian optimization"""
        payload = {
            "product_title": "Premium Wireless Gaming Headset",
            "current_price": 12999,
            "category": "electronics",
            "deep_analysis": True
        }
        
        with patch('main.amazon_client.get_product_details') as mock_details, \
             patch('main.amazon_client.get_pricing_data') as mock_pricing:
            
            mock_details.return_value = {
                "title": "Premium Wireless Gaming Headset",
                "price": 12999,
                "rating": 4.4,
                "review_count": 2800,
                "brand": "SteelSeries",
                "category": "electronics"
            }
            
            mock_pricing.return_value = {
                "current_price": 12999,
                "currency": "INR",
                "fees_estimate": {"total_fees": 2000}
            }
            
            response = client.post("/api/product-sourcing/analyze", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert "product_analysis" in data
            assert "scoring" in data["product_analysis"]
            assert "indian_market_optimization" in data["product_analysis"]
            assert "recommendations" in data["product_analysis"]
    
    def test_end_to_end_discovery_workflow(self):
        """Test end-to-end product discovery workflow"""
        # Start discovery
        discovery_payload = {
            "keywords": ["wireless mouse", "gaming mouse"],
            "category": "electronics",
            "market_region": "IN",
            "profit_margin_min": 25.0
        }
        
        with patch('main.process_product_discovery.delay') as mock_task:
            mock_task.return_value.id = "test_discovery_task"
            
            # Start discovery task
            discovery_response = client.post("/api/product-sourcing/discover", json=discovery_payload)
            assert discovery_response.status_code == 200
            
            task_id = discovery_response.json()["task_id"]
            
            # Mock task completion
            with patch('main.redis_client.get') as mock_redis:
                mock_redis.return_value = json.dumps({
                    "status": "completed",
                    "progress": 100,
                    "results": {"discovered_products": 15}
                })
                
                # Check task status
                status_response = client.get(f"/api/product-sourcing/discovery/{task_id}/status")
                assert status_response.status_code == 200
                
                status_data = status_response.json()
                assert status_data["status"] == "completed"
                assert status_data["results"]["discovered_products"] == 15

# Performance and Load Tests
class TestPerformanceAndLoad:
    """Test performance and load handling capabilities"""
    
    def test_concurrent_api_requests(self):
        """Test handling concurrent API requests"""
        import threading
        import time
        
        results = []
        
        def make_request():
            try:
                response = client.get("/api/product-sourcing/trends?limit=5")
                results.append(response.status_code)
            except Exception as e:
                results.append(500)
        
        # Create 20 concurrent threads
        threads = []
        start_time = time.time()
        
        for _ in range(20):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # All requests should succeed and complete within reasonable time
        assert all(status == 200 for status in results)
        assert len(results) == 20
        assert end_time - start_time < 10  # Should complete within 10 seconds
    
    def test_large_data_handling(self):
        """Test handling of large data sets"""
        # Test with large keyword list
        large_keywords = [f"keyword_{i}" for i in range(50)]
        
        payload = {
            "keywords": large_keywords,
            "category": "electronics",
            "market_region": "IN"
        }
        
        with patch('main.process_product_discovery.delay') as mock_task:
            mock_task.return_value.id = "test_large_task"
            
            response = client.post("/api/product-sourcing/discover", json=payload)
            # Should handle large lists gracefully
            assert response.status_code in [200, 413]  # 413 if payload too large
    
    def test_memory_usage_stability(self):
        """Test memory usage remains stable during processing"""
        import gc
        import sys
        
        # Get initial memory usage
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Make multiple requests
        for i in range(10):
            response = client.get(f"/api/product-sourcing/trends?limit=5&category=electronics")
            assert response.status_code == 200
        
        # Force garbage collection
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Memory usage should not increase significantly
        object_increase = final_objects - initial_objects
        assert object_increase < 1000  # Allow for some increase but not memory leak

# Error Handling and Edge Cases
class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge case scenarios"""
    
    def test_invalid_api_parameters(self):
        """Test handling of invalid API parameters"""
        # Invalid category
        response = client.get("/api/product-sourcing/trends?category=invalid_category")
        assert response.status_code == 200  # Should handle gracefully
        
        # Invalid price in GST calculator
        response = client.get("/api/product-sourcing/gst-calculator?price=-100&category=electronics")
        assert response.status_code in [200, 400]  # Should handle negative price
        
        # Missing required parameters
        response = client.get("/api/product-sourcing/gst-calculator?price=1000")
        assert response.status_code == 422  # Missing category parameter
    
    def test_api_timeout_handling(self):
        """Test API timeout handling"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Simulate timeout
            mock_get.side_effect = asyncio.TimeoutError()
            
            payload = {
                "product_title": "Test Product",
                "current_price": 1000,
                "category": "electronics"
            }
            
            response = client.post("/api/product-sourcing/analyze", json=payload)
            # Should handle timeout gracefully
            assert response.status_code in [200, 500, 503]
    
    def test_database_connection_failure(self):
        """Test database connection failure handling"""
        with patch('main.get_db_connection') as mock_db:
            mock_db.side_effect = Exception("Database connection failed")
            
            response = client.get("/health")
            assert response.status_code == 200  # Health check should return status
            
            data = response.json()
            assert data["status"] == "unhealthy"
    
    def test_invalid_json_payloads(self):
        """Test handling of invalid JSON payloads"""
        # Malformed JSON
        response = client.post(
            "/api/product-sourcing/analyze",
            data="{'invalid': 'json'}",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        
        # Empty payload
        response = client.post("/api/product-sourcing/analyze", json={})
        assert response.status_code == 422
    
    def test_rate_limiting_behavior(self):
        """Test rate limiting behavior"""
        # Make rapid requests to test rate limiting
        responses = []
        for i in range(100):
            response = client.get("/api/product-sourcing/trends?limit=1")
            responses.append(response.status_code)
        
        # Should handle all requests gracefully (with or without rate limiting)
        assert all(status in [200, 429] for status in responses)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])