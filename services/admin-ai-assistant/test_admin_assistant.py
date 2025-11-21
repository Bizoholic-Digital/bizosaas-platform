#!/usr/bin/env python3
"""
Test Suite for BizOSaaS Admin AI Assistant [P10]
Comprehensive testing for platform monitoring and operations service
"""

import pytest
import asyncio
import json
import httpx
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app, PlatformIntelligenceEngine, AdminChatAssistant, PlatformMonitoringEngine, PlatformMetrics

@pytest.fixture
def client():
    """Create test client"""
    return httpx.AsyncClient(app=app, base_url="http://test")

@pytest.fixture
def sample_metrics():
    """Sample platform metrics for testing"""
    return PlatformMetrics(
        timestamp=datetime.utcnow(),
        cpu_usage=45.0,
        memory_usage=65.0,
        disk_usage=30.0,
        network_io={"bytes_sent": 1000, "bytes_recv": 2000},
        active_connections=50,
        total_requests=1000,
        error_rate=0.02,
        response_time=1.5
    )

class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test basic health check endpoint"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Admin AI Assistant [P10]"
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_platform_health(self, client):
        """Test platform health endpoint"""
        with patch('main.monitoring_engine.check_all_services') as mock_check:
            mock_check.return_value = {
                "brain-api": Mock(status="healthy", response_time=0.5),
                "product-sourcing": Mock(status="healthy", response_time=0.8)
            }
            
            response = await client.get("/api/platform/health")
            assert response.status_code == 200
            data = response.json()
            assert "overall_status" in data
            assert "healthy_services" in data
            assert "total_services" in data

class TestMetricsEndpoints:
    """Test metrics collection and retrieval"""
    
    @pytest.mark.asyncio
    async def test_current_metrics(self, client, sample_metrics):
        """Test current metrics endpoint"""
        with patch('main.monitoring_engine.collect_platform_metrics') as mock_collect:
            mock_collect.return_value = sample_metrics
            
            response = await client.get("/api/platform/metrics")
            assert response.status_code == 200
            data = response.json()
            assert data["cpu_usage"] == 45.0
            assert data["memory_usage"] == 65.0
            assert data["error_rate"] == 0.02

    @pytest.mark.asyncio
    async def test_metrics_history(self, client):
        """Test metrics history endpoint"""
        with patch('main.redis_client.get') as mock_redis:
            mock_redis.return_value = json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_usage": 50.0,
                "memory_usage": 70.0
            })
            
            response = await client.get("/api/platform/metrics/history?hours=1")
            assert response.status_code == 200
            data = response.json()
            assert "metrics" in data
            assert "period" in data

class TestAIAnalysis:
    """Test AI intelligence engine functionality"""
    
    def test_platform_intelligence_engine_init(self):
        """Test AI engine initialization"""
        engine = PlatformIntelligenceEngine()
        assert engine.anomaly_detector is not None
        assert engine.scaler is not None
        assert not engine.is_trained

    @pytest.mark.asyncio
    async def test_health_score_calculation(self, sample_metrics):
        """Test health score calculation"""
        engine = PlatformIntelligenceEngine()
        health_score = engine._calculate_health_score(sample_metrics)
        assert isinstance(health_score, float)
        assert 0 <= health_score <= 100

    @pytest.mark.asyncio
    async def test_anomaly_detection_insufficient_data(self):
        """Test anomaly detection with insufficient data"""
        engine = PlatformIntelligenceEngine()
        metrics_history = [PlatformMetrics(
            timestamp=datetime.utcnow(),
            cpu_usage=50.0,
            memory_usage=60.0,
            disk_usage=30.0,
            network_io={},
            active_connections=10,
            total_requests=100,
            error_rate=0.01,
            response_time=1.0
        )]
        
        analysis = await engine.analyze_platform_health(metrics_history)
        assert analysis["status"] == "insufficient_data"

    def test_health_status_classification(self):
        """Test health status classification"""
        engine = PlatformIntelligenceEngine()
        
        assert engine._get_health_status(95.0) == "excellent"
        assert engine._get_health_status(80.0) == "good"
        assert engine._get_health_status(65.0) == "warning"
        assert engine._get_health_status(45.0) == "poor"
        assert engine._get_health_status(25.0) == "critical"

class TestChatAssistant:
    """Test AI chat assistant functionality"""
    
    @pytest.mark.asyncio
    async def test_chat_assistant_init(self):
        """Test chat assistant initialization"""
        assistant = AdminChatAssistant()
        assert assistant.monitoring_engine is not None

    @pytest.mark.asyncio
    async def test_health_inquiry(self):
        """Test health-related chat inquiries"""
        assistant = AdminChatAssistant()
        
        with patch.object(assistant.monitoring_engine, 'check_all_services') as mock_check:
            mock_check.return_value = {
                "brain-api": Mock(status="healthy", response_time=0.5),
                "test-service": Mock(status="warning", response_time=2.0)
            }
            
            response = await assistant.process_chat_message("What's the platform health?")
            assert response["type"] == "health_check"
            assert "data" in response
            assert "service_health" in response["data"]

    @pytest.mark.asyncio
    async def test_performance_inquiry(self):
        """Test performance-related chat inquiries"""
        assistant = AdminChatAssistant()
        
        with patch.object(assistant.monitoring_engine, 'collect_platform_metrics') as mock_collect:
            mock_collect.return_value = PlatformMetrics(
                timestamp=datetime.utcnow(),
                cpu_usage=75.0,
                memory_usage=80.0,
                disk_usage=40.0,
                network_io={},
                active_connections=25,
                total_requests=500,
                error_rate=0.03,
                response_time=2.0
            )
            
            response = await assistant.process_chat_message("How is performance?")
            assert response["type"] == "performance_check"
            assert "CPU Usage: 75.0%" in response["response"]

    @pytest.mark.asyncio
    async def test_general_help_inquiry(self):
        """Test general help inquiries"""
        assistant = AdminChatAssistant()
        
        response = await assistant.process_chat_message("Hello, what can you do?")
        assert response["type"] == "general_help"
        assert "Platform Monitoring" in response["response"]

class TestMonitoringEngine:
    """Test platform monitoring engine"""
    
    @pytest.mark.asyncio
    async def test_monitoring_engine_init(self):
        """Test monitoring engine initialization"""
        engine = PlatformMonitoringEngine()
        assert "brain-api" in engine.services
        assert "product-sourcing" in engine.services
        assert "supplier-validation" in engine.services

    @pytest.mark.asyncio
    async def test_service_health_check_success(self):
        """Test successful service health check"""
        engine = PlatformMonitoringEngine()
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={"status": "healthy"})
            mock_get.return_value.__aenter__.return_value = mock_response
            
            health = await engine._check_service_health("test-service", "http://localhost:8000")
            assert health.status.value == "healthy"
            assert health.service_name == "test-service"

    @pytest.mark.asyncio
    async def test_service_health_check_failure(self):
        """Test failed service health check"""
        engine = PlatformMonitoringEngine()
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Connection refused")
            
            health = await engine._check_service_health("test-service", "http://localhost:8000")
            assert health.status.value == "unhealthy"
            assert "Connection refused" in health.error_message

class TestAPIEndpoints:
    """Test API endpoints functionality"""
    
    @pytest.mark.asyncio
    async def test_dashboard_analytics(self, client):
        """Test dashboard analytics endpoint"""
        with patch('main.monitoring_engine.check_all_services') as mock_services, \
             patch('main.monitoring_engine.collect_platform_metrics') as mock_metrics, \
             patch('main.redis_client.get') as mock_redis:
            
            mock_services.return_value = {
                "brain-api": Mock(status="healthy", response_time=0.5)
            }
            mock_metrics.return_value = PlatformMetrics(
                timestamp=datetime.utcnow(),
                cpu_usage=45.0,
                memory_usage=65.0,
                disk_usage=30.0,
                network_io={},
                active_connections=20,
                total_requests=300,
                error_rate=0.01,
                response_time=1.2
            )
            mock_redis.return_value = None
            
            response = await client.get("/api/dashboard/analytics")
            assert response.status_code == 200
            data = response.json()
            assert "summary" in data
            assert "current_metrics" in data
            assert "service_health" in data

    @pytest.mark.asyncio
    async def test_chat_endpoint(self, client):
        """Test chat endpoint"""
        with patch('main.chat_assistant.process_chat_message') as mock_chat:
            mock_chat.return_value = {
                "response": "Test response",
                "type": "general_help",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = await client.post("/api/chat", json={
                "message": "Test message",
                "context": {}
            })
            assert response.status_code == 200
            data = response.json()
            assert data["response"] == "Test response"

    @pytest.mark.asyncio
    async def test_restart_service_operation(self, client):
        """Test restart service operation"""
        with patch('main.redis_client.setex') as mock_redis:
            mock_redis.return_value = True
            
            response = await client.post(
                "/api/operations/restart-service?service_name=brain-api",
                headers={"Authorization": "Bearer admin-key-123"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "operation_id" in data
            assert data["status"] == "completed"

    @pytest.mark.asyncio
    async def test_clear_cache_operation(self, client):
        """Test clear cache operation"""
        with patch('main.redis_client.delete') as mock_delete:
            mock_delete.return_value = 5
            
            response = await client.post(
                "/api/operations/clear-cache",
                headers={"Authorization": "Bearer admin-key-123"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["keys_cleared"] == 5

class TestAlertSystem:
    """Test alert system functionality"""
    
    @pytest.mark.asyncio
    async def test_alert_conditions_critical_cpu(self):
        """Test critical CPU alert condition"""
        from main import check_alert_conditions
        
        metrics = PlatformMetrics(
            timestamp=datetime.utcnow(),
            cpu_usage=95.0,  # Critical level
            memory_usage=50.0,
            disk_usage=30.0,
            network_io={},
            active_connections=10,
            total_requests=100,
            error_rate=0.01,
            response_time=1.0
        )
        
        alerts = await check_alert_conditions(metrics)
        cpu_alerts = [a for a in alerts if "CPU" in a["title"]]
        assert len(cpu_alerts) > 0
        assert cpu_alerts[0]["severity"] == "critical"

    @pytest.mark.asyncio
    async def test_alert_conditions_high_error_rate(self):
        """Test high error rate alert condition"""
        from main import check_alert_conditions
        
        metrics = PlatformMetrics(
            timestamp=datetime.utcnow(),
            cpu_usage=50.0,
            memory_usage=60.0,
            disk_usage=30.0,
            network_io={},
            active_connections=10,
            total_requests=100,
            error_rate=0.15,  # 15% error rate
            response_time=1.0
        )
        
        alerts = await check_alert_conditions(metrics)
        error_alerts = [a for a in alerts if "Error Rate" in a["title"]]
        assert len(error_alerts) > 0
        assert error_alerts[0]["severity"] == "high"

class TestDataModels:
    """Test data models and validation"""
    
    def test_platform_metrics_creation(self):
        """Test platform metrics data class"""
        metrics = PlatformMetrics(
            timestamp=datetime.utcnow(),
            cpu_usage=45.0,
            memory_usage=65.0,
            disk_usage=30.0,
            network_io={"sent": 1000, "received": 2000},
            active_connections=25,
            total_requests=500,
            error_rate=0.02,
            response_time=1.5
        )
        
        assert metrics.cpu_usage == 45.0
        assert metrics.memory_usage == 65.0
        assert isinstance(metrics.timestamp, datetime)

    def test_service_health_creation(self):
        """Test service health data class"""
        from main import ServiceHealth, ServiceStatus
        
        health = ServiceHealth(
            service_name="test-service",
            status=ServiceStatus.HEALTHY,
            response_time=0.5,
            last_check=datetime.utcnow()
        )
        
        assert health.service_name == "test-service"
        assert health.status == ServiceStatus.HEALTHY
        assert health.response_time == 0.5

class TestUtilityFunctions:
    """Test utility functions"""
    
    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Test database connection function"""
        with patch('asyncpg.connect') as mock_connect:
            mock_connect.return_value = AsyncMock()
            
            from main import get_db_connection
            conn = await get_db_connection()
            assert conn is not None

class TestWebSocketFunctionality:
    """Test WebSocket functionality"""
    
    def test_websocket_manager_init(self):
        """Test WebSocket manager initialization"""
        from main import WebSocketManager
        
        manager = WebSocketManager()
        assert manager.active_connections == []

    @pytest.mark.asyncio
    async def test_websocket_broadcast(self):
        """Test WebSocket message broadcasting"""
        from main import WebSocketManager
        
        manager = WebSocketManager()
        
        # Mock WebSocket connections
        mock_ws1 = AsyncMock()
        mock_ws2 = AsyncMock()
        manager.active_connections = [mock_ws1, mock_ws2]
        
        await manager.broadcast({"type": "test", "data": "test_data"})
        
        mock_ws1.send_text.assert_called_once()
        mock_ws2.send_text.assert_called_once()

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    @pytest.mark.asyncio
    async def test_metrics_collection_error(self):
        """Test metrics collection with error"""
        engine = PlatformMonitoringEngine()
        
        with patch('psutil.cpu_percent', side_effect=Exception("System error")):
            metrics = await engine.collect_platform_metrics()
            assert metrics.error_rate == 1.0  # Should indicate error state

    @pytest.mark.asyncio
    async def test_chat_assistant_error(self):
        """Test chat assistant error handling"""
        assistant = AdminChatAssistant()
        
        with patch.object(assistant, '_handle_health_inquiry', side_effect=Exception("Test error")):
            response = await assistant.process_chat_message("health check")
            assert response["type"] == "error"
            assert "encountered an error" in response["response"]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])