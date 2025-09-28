#!/usr/bin/env python3
"""
BizOSaaS Admin AI Assistant [P10] - Platform Monitoring and Operations
Comprehensive AI-Powered Platform Administration and Monitoring System

This service provides comprehensive platform administration capabilities including:
- Real-time health monitoring and system status tracking
- AI-powered insights and recommendations for platform optimization
- User management and analytics dashboard
- Automated operations and incident response assistance
- Performance optimization and resource management
- Cross-service coordination and monitoring
- Intelligent alerting and notification system

Author: BizOSaaS Platform Team
Version: 1.0.0
Port: 8028 (Admin AI Assistant Service)
"""

import asyncio
import aiohttp
import asyncpg
import json
import logging
import os
import redis
import uuid
import numpy as np
import psutil
import websockets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import requests
from textblob import TextBlob
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BizOSaaS Admin AI Assistant [P10]",
    description="Comprehensive AI-Powered Platform Administration and Monitoring System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/bizosaas")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
BRAIN_API_URL = os.getenv("BRAIN_API_URL", "http://localhost:8001")
INTEGRATION_MONITOR_URL = os.getenv("INTEGRATION_MONITOR_URL", "http://localhost:8025")
PRODUCT_SOURCING_URL = os.getenv("PRODUCT_SOURCING_URL", "http://localhost:8026")
SUPPLIER_VALIDATION_URL = os.getenv("SUPPLIER_VALIDATION_URL", "http://localhost:8027")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin-key-123")

# Redis client
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Database connection
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# WebSocket connection manager
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
        
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if self.active_connections:
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                self.disconnect(connection)

websocket_manager = WebSocketManager()

# Enums
class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    UNHEALTHY = "unhealthy"
    DOWN = "down"

class MetricType(str, Enum):
    GAUGE = "gauge"
    COUNTER = "counter"
    HISTOGRAM = "histogram"
    RATE = "rate"

class OperationType(str, Enum):
    RESTART_SERVICE = "restart_service"
    SCALE_SERVICE = "scale_service"
    CLEAR_CACHE = "clear_cache"
    BACKUP_DATABASE = "backup_database"
    OPTIMIZE_PERFORMANCE = "optimize_performance"

# Pydantic models
class ServiceHealthCheck(BaseModel):
    service_name: str
    url: str
    expected_status: int = 200
    timeout: int = 30
    critical: bool = True

class AlertRule(BaseModel):
    name: str
    condition: str
    threshold: float
    severity: AlertSeverity
    enabled: bool = True
    service_filter: Optional[str] = None

class AutomationRule(BaseModel):
    name: str
    trigger_condition: str
    action: OperationType
    parameters: Dict[str, Any]
    enabled: bool = True

class PerformanceMetric(BaseModel):
    metric_name: str
    service_name: str
    value: float
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

# Data classes
@dataclass
class ServiceHealth:
    service_name: str
    status: ServiceStatus
    response_time: float
    last_check: datetime
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class PlatformMetrics:
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    active_connections: int
    total_requests: int
    error_rate: float
    response_time: float

@dataclass
class Alert:
    id: str
    title: str
    description: str
    severity: AlertSeverity
    service_name: str
    triggered_at: datetime
    resolved_at: Optional[datetime] = None
    acknowledged: bool = False
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Recommendation:
    id: str
    title: str
    description: str
    category: str
    impact: str
    effort: str
    confidence: float
    created_at: datetime
    implemented: bool = False

# AI-Powered Platform Intelligence Engine
class PlatformIntelligenceEngine:
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    async def analyze_platform_health(self, metrics_history: List[PlatformMetrics]) -> Dict[str, Any]:
        """Analyze platform health using AI algorithms"""
        try:
            if len(metrics_history) < 10:
                return {"status": "insufficient_data", "recommendations": []}
            
            # Convert metrics to DataFrame for analysis
            metrics_data = []
            for metric in metrics_history:
                metrics_data.append({
                    'timestamp': metric.timestamp,
                    'cpu_usage': metric.cpu_usage,
                    'memory_usage': metric.memory_usage,
                    'disk_usage': metric.disk_usage,
                    'active_connections': metric.active_connections,
                    'error_rate': metric.error_rate,
                    'response_time': metric.response_time
                })
            
            df = pd.DataFrame(metrics_data)
            
            # Detect anomalies
            features = ['cpu_usage', 'memory_usage', 'disk_usage', 'error_rate', 'response_time']
            X = df[features].values
            
            if not self.is_trained and len(X) >= 50:
                X_scaled = self.scaler.fit_transform(X)
                self.anomaly_detector.fit(X_scaled)
                self.is_trained = True
            
            anomalies = []
            if self.is_trained:
                X_scaled = self.scaler.transform(X)
                anomaly_scores = self.anomaly_detector.decision_function(X_scaled)
                anomaly_flags = self.anomaly_detector.predict(X_scaled)
                
                for i, (score, flag) in enumerate(zip(anomaly_scores, anomaly_flags)):
                    if flag == -1:  # Anomaly detected
                        anomalies.append({
                            'timestamp': metrics_history[i].timestamp.isoformat(),
                            'anomaly_score': float(score),
                            'affected_metrics': features
                        })
            
            # Generate health score
            latest_metrics = metrics_history[-1]
            health_score = self._calculate_health_score(latest_metrics)
            
            # Generate trends
            trends = self._analyze_trends(df, features)
            
            # Generate recommendations
            recommendations = await self._generate_health_recommendations(latest_metrics, trends, anomalies)
            
            return {
                "health_score": health_score,
                "status": self._get_health_status(health_score),
                "anomalies": anomalies,
                "trends": trends,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in platform health analysis: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def _calculate_health_score(self, metrics: PlatformMetrics) -> float:
        """Calculate overall platform health score"""
        # Scoring factors (lower is better for most metrics)
        cpu_score = max(0, 100 - metrics.cpu_usage)
        memory_score = max(0, 100 - metrics.memory_usage)
        disk_score = max(0, 100 - metrics.disk_usage)
        error_score = max(0, 100 - (metrics.error_rate * 100))
        response_score = max(0, 100 - min(metrics.response_time * 10, 100))
        
        # Weighted average
        weights = {
            'cpu': 0.2,
            'memory': 0.25,
            'disk': 0.15,
            'error': 0.25,
            'response': 0.15
        }
        
        health_score = (
            cpu_score * weights['cpu'] +
            memory_score * weights['memory'] +
            disk_score * weights['disk'] +
            error_score * weights['error'] +
            response_score * weights['response']
        )
        
        return round(health_score, 2)
    
    def _get_health_status(self, health_score: float) -> str:
        """Get health status based on score"""
        if health_score >= 90:
            return "excellent"
        elif health_score >= 75:
            return "good"
        elif health_score >= 60:
            return "warning"
        elif health_score >= 40:
            return "poor"
        else:
            return "critical"
    
    def _analyze_trends(self, df: pd.DataFrame, features: List[str]) -> Dict[str, Any]:
        """Analyze trends in metrics"""
        trends = {}
        
        for feature in features:
            if len(df) >= 5:
                # Calculate trend direction
                recent_values = df[feature].tail(5).values
                if len(recent_values) >= 2:
                    slope = np.polyfit(range(len(recent_values)), recent_values, 1)[0]
                    
                    if slope > 0.1:
                        direction = "increasing"
                    elif slope < -0.1:
                        direction = "decreasing"
                    else:
                        direction = "stable"
                    
                    trends[feature] = {
                        "direction": direction,
                        "slope": float(slope),
                        "current_value": float(recent_values[-1]),
                        "change_rate": float(slope / recent_values[0] * 100) if recent_values[0] != 0 else 0
                    }
        
        return trends
    
    async def _generate_health_recommendations(self, metrics: PlatformMetrics, trends: Dict[str, Any], anomalies: List[Dict]) -> List[Dict[str, Any]]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        # CPU-based recommendations
        if metrics.cpu_usage > 80:
            recommendations.append({
                "title": "High CPU Usage Detected",
                "description": f"CPU usage is at {metrics.cpu_usage:.1f}%. Consider scaling up or optimizing resource-intensive processes.",
                "category": "performance",
                "priority": "high",
                "suggested_actions": [
                    "Scale up compute resources",
                    "Identify and optimize CPU-intensive processes",
                    "Implement caching to reduce computation load"
                ]
            })
        
        # Memory-based recommendations
        if metrics.memory_usage > 85:
            recommendations.append({
                "title": "High Memory Usage",
                "description": f"Memory usage is at {metrics.memory_usage:.1f}%. Memory leak or insufficient resources suspected.",
                "category": "performance",
                "priority": "high",
                "suggested_actions": [
                    "Investigate potential memory leaks",
                    "Increase available memory",
                    "Optimize data structures and caching"
                ]
            })
        
        # Error rate recommendations
        if metrics.error_rate > 0.05:  # 5% error rate
            recommendations.append({
                "title": "Elevated Error Rate",
                "description": f"Error rate is {metrics.error_rate:.2%}. Service reliability may be compromised.",
                "category": "reliability",
                "priority": "critical",
                "suggested_actions": [
                    "Review error logs for patterns",
                    "Implement circuit breakers",
                    "Check downstream service dependencies"
                ]
            })
        
        # Response time recommendations
        if metrics.response_time > 5.0:  # 5 seconds
            recommendations.append({
                "title": "Slow Response Times",
                "description": f"Average response time is {metrics.response_time:.2f}s. User experience may be impacted.",
                "category": "performance",
                "priority": "medium",
                "suggested_actions": [
                    "Optimize database queries",
                    "Implement response caching",
                    "Review API performance bottlenecks"
                ]
            })
        
        # Trend-based recommendations
        if trends.get('error_rate', {}).get('direction') == 'increasing':
            recommendations.append({
                "title": "Increasing Error Rate Trend",
                "description": "Error rate has been trending upward. Proactive investigation recommended.",
                "category": "reliability",
                "priority": "medium",
                "suggested_actions": [
                    "Set up enhanced monitoring",
                    "Review recent deployments",
                    "Implement error rate alerts"
                ]
            })
        
        # Anomaly-based recommendations
        if anomalies:
            recommendations.append({
                "title": "Anomalous Behavior Detected",
                "description": f"AI detected {len(anomalies)} anomalous patterns in the last monitoring period.",
                "category": "monitoring",
                "priority": "medium",
                "suggested_actions": [
                    "Review anomaly details",
                    "Correlate with recent changes",
                    "Set up automated anomaly alerts"
                ]
            })
        
        return recommendations

# Platform Monitoring Engine
class PlatformMonitoringEngine:
    def __init__(self):
        self.services = {
            "brain-api": {"url": BRAIN_API_URL, "port": 8001},
            "integration-monitor": {"url": INTEGRATION_MONITOR_URL, "port": 8025},
            "product-sourcing": {"url": PRODUCT_SOURCING_URL, "port": 8026},
            "supplier-validation": {"url": SUPPLIER_VALIDATION_URL, "port": 8027}
        }
        self.intelligence_engine = PlatformIntelligenceEngine()
        
    async def check_all_services(self) -> Dict[str, ServiceHealth]:
        """Check health of all platform services"""
        health_results = {}
        
        for service_name, config in self.services.items():
            health = await self._check_service_health(service_name, config["url"])
            health_results[service_name] = health
            
        return health_results
    
    async def _check_service_health(self, service_name: str, base_url: str) -> ServiceHealth:
        """Check health of individual service"""
        start_time = datetime.utcnow()
        
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"{base_url}/health") as response:
                    response_time = (datetime.utcnow() - start_time).total_seconds()
                    
                    if response.status == 200:
                        data = await response.json()
                        return ServiceHealth(
                            service_name=service_name,
                            status=ServiceStatus.HEALTHY,
                            response_time=response_time,
                            last_check=datetime.utcnow(),
                            metadata=data
                        )
                    else:
                        return ServiceHealth(
                            service_name=service_name,
                            status=ServiceStatus.WARNING,
                            response_time=response_time,
                            last_check=datetime.utcnow(),
                            error_message=f"HTTP {response.status}"
                        )
                        
        except asyncio.TimeoutError:
            return ServiceHealth(
                service_name=service_name,
                status=ServiceStatus.DOWN,
                response_time=10.0,
                last_check=datetime.utcnow(),
                error_message="Connection timeout"
            )
        except Exception as e:
            return ServiceHealth(
                service_name=service_name,
                status=ServiceStatus.UNHEALTHY,
                response_time=(datetime.utcnow() - start_time).total_seconds(),
                last_check=datetime.utcnow(),
                error_message=str(e)
            )
    
    async def collect_platform_metrics(self) -> PlatformMetrics:
        """Collect comprehensive platform metrics"""
        try:
            # System metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Redis metrics for connections and requests
            redis_info = redis_client.info()
            active_connections = redis_info.get('connected_clients', 0)
            total_requests = redis_info.get('total_commands_processed', 0)
            
            # Calculate error rate from service health checks
            service_health = await self.check_all_services()
            healthy_services = sum(1 for h in service_health.values() if h.status == ServiceStatus.HEALTHY)
            total_services = len(service_health)
            error_rate = 1 - (healthy_services / total_services) if total_services > 0 else 0
            
            # Average response time
            response_times = [h.response_time for h in service_health.values()]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            return PlatformMetrics(
                timestamp=datetime.utcnow(),
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                disk_usage=(disk.used / disk.total) * 100,
                network_io={
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                active_connections=active_connections,
                total_requests=total_requests,
                error_rate=error_rate,
                response_time=avg_response_time
            )
            
        except Exception as e:
            logger.error(f"Error collecting platform metrics: {str(e)}")
            return PlatformMetrics(
                timestamp=datetime.utcnow(),
                cpu_usage=0,
                memory_usage=0,
                disk_usage=0,
                network_io={},
                active_connections=0,
                total_requests=0,
                error_rate=1.0,
                response_time=999.0
            )

# AI Chat Assistant
class AdminChatAssistant:
    def __init__(self):
        self.monitoring_engine = PlatformMonitoringEngine()
        
    async def process_chat_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process chat message and provide AI-powered responses"""
        try:
            message_lower = message.lower()
            
            # Health check requests
            if any(keyword in message_lower for keyword in ['health', 'status', 'check', 'monitor']):
                return await self._handle_health_inquiry(message, context)
            
            # Performance requests
            elif any(keyword in message_lower for keyword in ['performance', 'slow', 'cpu', 'memory', 'disk']):
                return await self._handle_performance_inquiry(message, context)
            
            # Error and troubleshooting
            elif any(keyword in message_lower for keyword in ['error', 'issue', 'problem', 'fail', 'down']):
                return await self._handle_troubleshooting_inquiry(message, context)
            
            # Recommendations
            elif any(keyword in message_lower for keyword in ['recommend', 'suggest', 'optimize', 'improve']):
                return await self._handle_recommendation_inquiry(message, context)
            
            # General help
            else:
                return await self._handle_general_inquiry(message, context)
                
        except Exception as e:
            logger.error(f"Error processing chat message: {str(e)}")
            return {
                "response": "I encountered an error processing your request. Please try again or contact support.",
                "type": "error",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _handle_health_inquiry(self, message: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle health-related inquiries"""
        service_health = await self.monitoring_engine.check_all_services()
        
        healthy_count = sum(1 for h in service_health.values() if h.status == ServiceStatus.HEALTHY)
        total_count = len(service_health)
        
        response = f"Platform Health Summary:\n\n"
        response += f"✅ {healthy_count}/{total_count} services are healthy\n\n"
        
        for service_name, health in service_health.items():
            status_emoji = "✅" if health.status == ServiceStatus.HEALTHY else "⚠️" if health.status == ServiceStatus.WARNING else "❌"
            response += f"{status_emoji} {service_name}: {health.status.value} ({health.response_time:.2f}s)\n"
        
        if healthy_count < total_count:
            response += f"\n🔍 Issues detected. Would you like me to help troubleshoot?"
        
        return {
            "response": response,
            "type": "health_check",
            "data": {
                "service_health": {name: asdict(health) for name, health in service_health.items()},
                "summary": {
                    "healthy_services": healthy_count,
                    "total_services": total_count,
                    "overall_status": "healthy" if healthy_count == total_count else "degraded"
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _handle_performance_inquiry(self, message: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle performance-related inquiries"""
        metrics = await self.monitoring_engine.collect_platform_metrics()
        
        response = f"Platform Performance Summary:\n\n"
        response += f"🖥️ CPU Usage: {metrics.cpu_usage:.1f}%\n"
        response += f"💾 Memory Usage: {metrics.memory_usage:.1f}%\n"
        response += f"💿 Disk Usage: {metrics.disk_usage:.1f}%\n"
        response += f"⚡ Average Response Time: {metrics.response_time:.2f}s\n"
        response += f"❌ Error Rate: {metrics.error_rate:.2%}\n"
        response += f"🔗 Active Connections: {metrics.active_connections}\n"
        
        # Performance assessment
        if metrics.cpu_usage > 80:
            response += f"\n⚠️ High CPU usage detected. Consider scaling up."
        if metrics.memory_usage > 85:
            response += f"\n⚠️ High memory usage. Check for memory leaks."
        if metrics.response_time > 5:
            response += f"\n⚠️ Slow response times. Optimization needed."
        
        return {
            "response": response,
            "type": "performance_check",
            "data": asdict(metrics),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _handle_troubleshooting_inquiry(self, message: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle troubleshooting inquiries"""
        service_health = await self.monitoring_engine.check_all_services()
        
        issues = []
        for service_name, health in service_health.items():
            if health.status != ServiceStatus.HEALTHY:
                issues.append({
                    "service": service_name,
                    "status": health.status.value,
                    "error": health.error_message,
                    "response_time": health.response_time
                })
        
        if not issues:
            response = "Great news! All services are currently healthy. No issues detected."
        else:
            response = f"I found {len(issues)} issue(s):\n\n"
            for issue in issues:
                response += f"❌ {issue['service']}: {issue['status']}\n"
                if issue['error']:
                    response += f"   Error: {issue['error']}\n"
                response += f"   Response time: {issue['response_time']:.2f}s\n\n"
            
            response += "Suggested troubleshooting steps:\n"
            response += "1. Check service logs for detailed error information\n"
            response += "2. Verify database and Redis connections\n"
            response += "3. Restart unhealthy services if needed\n"
            response += "4. Monitor resource usage (CPU, memory, disk)\n"
        
        return {
            "response": response,
            "type": "troubleshooting",
            "data": {"issues": issues},
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _handle_recommendation_inquiry(self, message: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle recommendation inquiries"""
        # Get recent metrics for analysis
        metrics = await self.monitoring_engine.collect_platform_metrics()
        
        # Generate AI recommendations
        recommendations = []
        
        if metrics.cpu_usage > 70:
            recommendations.append({
                "title": "CPU Optimization",
                "description": "Consider implementing CPU-efficient algorithms or scaling horizontally",
                "priority": "medium"
            })
        
        if metrics.memory_usage > 80:
            recommendations.append({
                "title": "Memory Management",
                "description": "Implement memory pooling and garbage collection optimization",
                "priority": "high"
            })
        
        if metrics.error_rate > 0.01:
            recommendations.append({
                "title": "Error Rate Reduction",
                "description": "Implement circuit breakers and retry mechanisms",
                "priority": "high"
            })
        
        if metrics.response_time > 3:
            recommendations.append({
                "title": "Response Time Optimization",
                "description": "Add caching layers and optimize database queries",
                "priority": "medium"
            })
        
        # Security recommendations
        recommendations.append({
            "title": "Security Enhancement",
            "description": "Regular security audits and dependency updates",
            "priority": "medium"
        })
        
        response = "Here are my AI-powered recommendations:\n\n"
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
            response += f"{i}. {priority_emoji} {rec['title']}\n"
            response += f"   {rec['description']}\n\n"
        
        if not recommendations:
            response = "Your platform is performing well! No immediate optimizations needed."
        
        return {
            "response": response,
            "type": "recommendations",
            "data": {"recommendations": recommendations},
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _handle_general_inquiry(self, message: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle general inquiries"""
        response = """Hello! I'm your BizOSaaS Admin AI Assistant. I can help you with:

🔍 **Platform Monitoring**
- Check service health and status
- Monitor performance metrics
- Track system resources

🔧 **Troubleshooting**
- Identify and diagnose issues
- Provide resolution steps
- Monitor error rates

📊 **Analytics & Insights**
- Generate performance reports
- Provide optimization recommendations
- Track usage patterns

🤖 **Automated Operations**
- Restart services
- Clear caches
- Optimize resources

Try asking me:
- "What's the platform health status?"
- "How is performance looking?"
- "Any issues I should know about?"
- "What optimizations do you recommend?"

How can I assist you today?"""

        return {
            "response": response,
            "type": "general_help",
            "timestamp": datetime.utcnow().isoformat()
        }

# Initialize global instances
monitoring_engine = PlatformMonitoringEngine()
chat_assistant = AdminChatAssistant()

# Background monitoring task
async def continuous_monitoring():
    """Continuous platform monitoring task"""
    while True:
        try:
            # Collect metrics
            metrics = await monitoring_engine.collect_platform_metrics()
            
            # Store metrics in Redis with TTL
            metrics_key = f"platform_metrics:{int(metrics.timestamp.timestamp())}"
            redis_client.setex(metrics_key, 3600, json.dumps(asdict(metrics), default=str))
            
            # Check for alerts
            alerts = await check_alert_conditions(metrics)
            
            # Broadcast real-time updates
            await websocket_manager.broadcast({
                "type": "metrics_update",
                "data": asdict(metrics),
                "alerts": alerts,
                "timestamp": metrics.timestamp.isoformat()
            })
            
            # Sleep for 30 seconds
            await asyncio.sleep(30)
            
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {str(e)}")
            await asyncio.sleep(60)  # Wait longer on error

async def check_alert_conditions(metrics: PlatformMetrics) -> List[Dict[str, Any]]:
    """Check if any alert conditions are met"""
    alerts = []
    
    # CPU alert
    if metrics.cpu_usage > 85:
        alerts.append({
            "severity": "critical",
            "title": "High CPU Usage",
            "message": f"CPU usage is {metrics.cpu_usage:.1f}%",
            "timestamp": metrics.timestamp.isoformat()
        })
    
    # Memory alert
    if metrics.memory_usage > 90:
        alerts.append({
            "severity": "critical",
            "title": "High Memory Usage",
            "message": f"Memory usage is {metrics.memory_usage:.1f}%",
            "timestamp": metrics.timestamp.isoformat()
        })
    
    # Error rate alert
    if metrics.error_rate > 0.1:  # 10% error rate
        alerts.append({
            "severity": "high",
            "title": "High Error Rate",
            "message": f"Error rate is {metrics.error_rate:.2%}",
            "timestamp": metrics.timestamp.isoformat()
        })
    
    return alerts

# Database operations
async def get_db_connection():
    """Get database connection"""
    return await asyncpg.connect(DATABASE_URL)

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    # Simple API key authentication for admin
    if credentials.credentials != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "id": "admin-user",
        "role": "admin",
        "email": "admin@bizosaas.com"
    }

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Admin AI Assistant [P10]",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Admin dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_redirect(request: Request):
    """Dashboard redirect"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/platform/health")
async def get_platform_health():
    """Get comprehensive platform health status"""
    try:
        service_health = await monitoring_engine.check_all_services()
        
        # Calculate overall status
        healthy_count = sum(1 for h in service_health.values() if h.status == ServiceStatus.HEALTHY)
        total_count = len(service_health)
        
        overall_status = "healthy" if healthy_count == total_count else "degraded" if healthy_count > 0 else "down"
        
        return {
            "overall_status": overall_status,
            "healthy_services": healthy_count,
            "total_services": total_count,
            "services": {name: asdict(health) for name, health in service_health.items()},
            "last_check": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting platform health: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get platform health: {str(e)}")

@app.get("/api/platform/metrics")
async def get_platform_metrics():
    """Get current platform metrics"""
    try:
        metrics = await monitoring_engine.collect_platform_metrics()
        return asdict(metrics)
        
    except Exception as e:
        logger.error(f"Error getting platform metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get platform metrics: {str(e)}")

@app.get("/api/platform/metrics/history")
async def get_metrics_history(
    hours: int = Query(24, ge=1, le=168),  # Last 1-168 hours
    interval: int = Query(300, ge=60, le=3600)  # 1-60 minute intervals
):
    """Get historical platform metrics"""
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Get metrics from Redis
        metrics_data = []
        current_time = start_time
        
        while current_time <= end_time:
            metrics_key = f"platform_metrics:{int(current_time.timestamp())}"
            metrics_json = redis_client.get(metrics_key)
            
            if metrics_json:
                try:
                    metrics_dict = json.loads(metrics_json)
                    metrics_data.append(metrics_dict)
                except:
                    pass
            
            current_time += timedelta(seconds=interval)
        
        return {
            "metrics": metrics_data,
            "period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "hours": hours,
                "interval_seconds": interval
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get metrics history: {str(e)}")

@app.get("/api/platform/analysis")
async def get_platform_analysis():
    """Get AI-powered platform analysis"""
    try:
        # Get recent metrics history
        metrics_data = []
        for i in range(100):  # Last 100 data points
            timestamp = datetime.utcnow() - timedelta(minutes=i*5)
            metrics_key = f"platform_metrics:{int(timestamp.timestamp())}"
            metrics_json = redis_client.get(metrics_key)
            
            if metrics_json:
                try:
                    metrics_dict = json.loads(metrics_json)
                    metrics_data.append(PlatformMetrics(
                        timestamp=datetime.fromisoformat(metrics_dict['timestamp']),
                        cpu_usage=metrics_dict['cpu_usage'],
                        memory_usage=metrics_dict['memory_usage'],
                        disk_usage=metrics_dict['disk_usage'],
                        network_io=metrics_dict['network_io'],
                        active_connections=metrics_dict['active_connections'],
                        total_requests=metrics_dict['total_requests'],
                        error_rate=metrics_dict['error_rate'],
                        response_time=metrics_dict['response_time']
                    ))
                except:
                    pass
        
        if not metrics_data:
            # Generate current metrics if no history
            current_metrics = await monitoring_engine.collect_platform_metrics()
            metrics_data = [current_metrics]
        
        # Perform AI analysis
        analysis = await monitoring_engine.intelligence_engine.analyze_platform_health(metrics_data)
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error getting platform analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get platform analysis: {str(e)}")

@app.post("/api/chat")
async def chat_with_assistant(message: ChatMessage):
    """Chat with the AI assistant"""
    try:
        response = await chat_assistant.process_chat_message(message.message, message.context)
        return response
        
    except Exception as e:
        logger.error(f"Error in chat processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@app.get("/api/dashboard/analytics")
async def get_dashboard_analytics():
    """Get comprehensive dashboard analytics"""
    try:
        # Service health summary
        service_health = await monitoring_engine.check_all_services()
        healthy_count = sum(1 for h in service_health.values() if h.status == ServiceStatus.HEALTHY)
        
        # Current metrics
        current_metrics = await monitoring_engine.collect_platform_metrics()
        
        # Get metrics history for trends
        metrics_history = []
        for i in range(24):  # Last 24 hours
            timestamp = datetime.utcnow() - timedelta(hours=i)
            metrics_key = f"platform_metrics:{int(timestamp.timestamp())}"
            metrics_json = redis_client.get(metrics_key)
            
            if metrics_json:
                try:
                    metrics_dict = json.loads(metrics_json)
                    metrics_history.append(metrics_dict)
                except:
                    pass
        
        # Calculate trends
        cpu_trend = "stable"
        memory_trend = "stable"
        if len(metrics_history) >= 2:
            cpu_values = [m.get('cpu_usage', 0) for m in metrics_history[-10:]]
            if len(cpu_values) >= 2:
                cpu_slope = np.polyfit(range(len(cpu_values)), cpu_values, 1)[0]
                cpu_trend = "increasing" if cpu_slope > 1 else "decreasing" if cpu_slope < -1 else "stable"
            
            memory_values = [m.get('memory_usage', 0) for m in metrics_history[-10:]]
            if len(memory_values) >= 2:
                memory_slope = np.polyfit(range(len(memory_values)), memory_values, 1)[0]
                memory_trend = "increasing" if memory_slope > 1 else "decreasing" if memory_slope < -1 else "stable"
        
        return {
            "summary": {
                "total_services": len(service_health),
                "healthy_services": healthy_count,
                "service_availability": (healthy_count / len(service_health)) * 100 if service_health else 0,
                "overall_health_score": monitoring_engine.intelligence_engine._calculate_health_score(current_metrics)
            },
            "current_metrics": asdict(current_metrics),
            "service_health": {name: asdict(health) for name, health in service_health.items()},
            "trends": {
                "cpu_usage": cpu_trend,
                "memory_usage": memory_trend,
                "data_points": len(metrics_history)
            },
            "alerts": await check_alert_conditions(current_metrics),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard analytics: {str(e)}")

@app.post("/api/operations/restart-service")
async def restart_service(
    service_name: str,
    current_user = Depends(get_current_user)
):
    """Restart a specific service"""
    try:
        if service_name not in monitoring_engine.services:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # In a real implementation, this would trigger service restart
        # For now, we'll simulate the operation
        
        # Log the operation
        operation_id = str(uuid.uuid4())
        redis_client.setex(
            f"operation:{operation_id}",
            3600,
            json.dumps({
                "type": "restart_service",
                "service_name": service_name,
                "initiated_by": current_user["id"],
                "timestamp": datetime.utcnow().isoformat(),
                "status": "completed"
            })
        )
        
        return {
            "operation_id": operation_id,
            "message": f"Service {service_name} restart initiated",
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error restarting service: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to restart service: {str(e)}")

@app.post("/api/operations/clear-cache")
async def clear_cache(
    cache_type: str = "all",
    current_user = Depends(get_current_user)
):
    """Clear Redis cache"""
    try:
        cleared_keys = 0
        
        if cache_type == "all":
            # Clear all keys except persistent data
            keys = redis_client.keys("cache:*")
            if keys:
                cleared_keys = redis_client.delete(*keys)
        elif cache_type == "metrics":
            keys = redis_client.keys("platform_metrics:*")
            if keys:
                cleared_keys = redis_client.delete(*keys)
        elif cache_type == "operations":
            keys = redis_client.keys("operation:*")
            if keys:
                cleared_keys = redis_client.delete(*keys)
        
        return {
            "message": f"Cache cleared successfully",
            "cache_type": cache_type,
            "keys_cleared": cleared_keys,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong", "timestamp": datetime.utcnow().isoformat()}))
            elif message.get("type") == "subscribe":
                # Handle subscription to specific data streams
                await websocket.send_text(json.dumps({"type": "subscribed", "stream": message.get("stream")}))
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    logger.info("Starting Admin AI Assistant [P10]")
    
    # Initialize database tables if needed
    await create_database_tables()
    
    # Start background monitoring
    asyncio.create_task(continuous_monitoring())
    
    logger.info("Admin AI Assistant [P10] started successfully")
    logger.info(f"Dashboard available at: http://localhost:8028/dashboard")
    logger.info(f"API Documentation: http://localhost:8028/docs")

async def create_database_tables():
    """Create database tables for admin operations"""
    try:
        conn = await get_db_connection()
        try:
            # Create platform_metrics table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS platform_metrics (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    cpu_usage DECIMAL(5,2) NOT NULL,
                    memory_usage DECIMAL(5,2) NOT NULL,
                    disk_usage DECIMAL(5,2) NOT NULL,
                    network_io JSONB NOT NULL,
                    active_connections INTEGER NOT NULL DEFAULT 0,
                    total_requests BIGINT NOT NULL DEFAULT 0,
                    error_rate DECIMAL(5,4) NOT NULL DEFAULT 0,
                    response_time DECIMAL(8,3) NOT NULL DEFAULT 0
                )
            """)
            
            # Create admin_operations table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS admin_operations (
                    id VARCHAR(36) PRIMARY KEY,
                    operation_type VARCHAR(50) NOT NULL,
                    service_name VARCHAR(100),
                    parameters JSONB,
                    initiated_by VARCHAR(36) NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'pending',
                    result JSONB,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    completed_at TIMESTAMP WITH TIME ZONE
                )
            """)
            
            # Create platform_alerts table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS platform_alerts (
                    id VARCHAR(36) PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    severity VARCHAR(20) NOT NULL,
                    service_name VARCHAR(100),
                    triggered_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    resolved_at TIMESTAMP WITH TIME ZONE,
                    acknowledged BOOLEAN DEFAULT FALSE,
                    acknowledged_by VARCHAR(36),
                    metadata JSONB
                )
            """)
            
            # Create indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_platform_metrics_timestamp ON platform_metrics(timestamp)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_admin_operations_created_at ON admin_operations(created_at)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_platform_alerts_triggered_at ON platform_alerts(triggered_at)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_platform_alerts_severity ON platform_alerts(severity)")
            
            logger.info("Database tables created successfully")
            
        finally:
            await conn.close()
            
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Admin AI Assistant [P10] starting on port 8028")
    logger.info("Dashboard available at: http://localhost:8028/dashboard")
    logger.info("API Documentation: http://localhost:8028/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8028,
        reload=True,
        log_level="info"
    )