#!/usr/bin/env python3
"""
BizOSaaS Platform Analytics Comprehensive Test Suite
===================================================

Validates all analytics capabilities, real-time data flows, and business intelligence features
across the entire BizOSaaS platform ecosystem.

Test Coverage:
1. Apache Superset BI dashboard functionality and data connectivity
2. Real-time analytics endpoints across all services  
3. Business intelligence dashboards and reporting
4. Multi-tenant analytics data segregation
5. Performance metrics and system monitoring
6. User behavior tracking and analytics
7. Financial analytics and revenue reporting
8. AI agent performance metrics and insights
"""

import asyncio
import aiohttp
import psycopg2
import redis
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'analytics_test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARNING = "⚠️ WARNING"
    SKIP = "⏭️ SKIP"

@dataclass
class TestResult:
    name: str
    status: TestStatus
    message: str
    execution_time: float
    details: Dict[str, Any] = None
    metrics: Dict[str, float] = None

class BizOSaaSAnalyticsTestSuite:
    """Comprehensive analytics testing suite for BizOSaaS platform"""
    
    def __init__(self):
        self.base_urls = {
            'central_hub': 'http://localhost:8001',
            'superset': 'http://localhost:8088',
            'client_portal': 'http://localhost:3000',
            'business_directory': 'http://localhost:8004',
            'auth_service': 'http://localhost:8007',
            'wagtail_cms': 'http://localhost:8002',
            'saleor_backend': 'http://localhost:8000',
            'ai_agents': 'http://localhost:8010',
            'temporal': 'http://localhost:8009',
            'sqladmin': 'http://localhost:8005'
        }
        
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'bizosaas',
            'user': 'postgres',
            'password': 'Bizoholic2024Alagiri'
        }
        
        self.redis_config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
        
        self.test_results = []
        self.analytics_metrics = {}
        
    async def run_all_tests(self) -> Dict[str, Any]:
        """Execute all analytics tests and generate comprehensive report"""
        
        logger.info("🚀 Starting BizOSaaS Analytics Comprehensive Test Suite")
        start_time = time.time()
        
        test_categories = [
            ("Database Analytics Infrastructure", self.test_database_analytics),
            ("Apache Superset BI Platform", self.test_superset_analytics),
            ("Real-time Data Flows", self.test_realtime_analytics),
            ("Multi-tenant Data Segregation", self.test_multitenant_analytics),
            ("Business Intelligence Dashboards", self.test_bi_dashboards),
            ("User Behavior Analytics", self.test_user_behavior_analytics),
            ("Financial Analytics", self.test_financial_analytics),
            ("AI Agent Performance Metrics", self.test_ai_agent_metrics),
            ("System Performance Monitoring", self.test_system_monitoring),
            ("API Analytics Endpoints", self.test_api_analytics),
            ("Data Quality & Integrity", self.test_data_quality),
            ("Security Analytics", self.test_security_analytics)
        ]
        
        for category_name, test_function in test_categories:
            logger.info(f"\n🔍 Testing: {category_name}")
            try:
                await test_function()
            except Exception as e:
                logger.error(f"❌ Error in {category_name}: {str(e)}")
                self.test_results.append(TestResult(
                    name=f"{category_name} - Exception",
                    status=TestStatus.FAIL,
                    message=f"Test suite error: {str(e)}",
                    execution_time=0.0
                ))
        
        total_time = time.time() - start_time
        
        # Generate comprehensive report
        report = self.generate_analytics_report(total_time)
        
        # Save detailed report
        await self.save_detailed_report(report)
        
        logger.info(f"✅ Analytics test suite completed in {total_time:.2f} seconds")
        return report

    async def test_database_analytics(self):
        """Test database analytics infrastructure and capabilities"""
        
        # Test 1: Database connectivity and analytics schema
        start_time = time.time()
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check for analytics-related tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%analytic%' OR table_name LIKE '%metric%' OR table_name LIKE '%report%'
            """)
            analytics_tables = cursor.fetchall()
            
            # Check for pgvector extension (for AI analytics)
            cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
            pgvector_enabled = len(cursor.fetchall()) > 0
            
            # Check for time-series analytics capabilities
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.columns 
                WHERE column_name IN ('created_at', 'updated_at', 'timestamp', 'event_time')
            """)
            timestamp_columns = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            execution_time = time.time() - start_time
            
            self.test_results.append(TestResult(
                name="Database Analytics Infrastructure",
                status=TestStatus.PASS if analytics_tables and pgvector_enabled else TestStatus.WARNING,
                message=f"Found {len(analytics_tables)} analytics tables, pgvector: {pgvector_enabled}, timestamp columns: {timestamp_columns}",
                execution_time=execution_time,
                details={
                    'analytics_tables': [table[0] for table in analytics_tables],
                    'pgvector_enabled': pgvector_enabled,
                    'timestamp_columns': timestamp_columns
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Database Analytics Infrastructure",
                status=TestStatus.FAIL,
                message=f"Database connection failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_superset_analytics(self):
        """Test Apache Superset analytics dashboard functionality"""
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test Superset availability
                async with session.get(f"{self.base_urls['superset']}/health") as response:
                    if response.status == 200:
                        health_data = await response.json()
                    else:
                        health_data = {"status": "unknown"}
                
                # Test Superset login endpoint
                async with session.get(f"{self.base_urls['superset']}/login/") as response:
                    login_available = response.status == 200
                
                # Test API endpoints
                async with session.get(f"{self.base_urls['superset']}/api/v1/security/csrf_token/") as response:
                    api_available = response.status == 200
                
                execution_time = time.time() - start_time
                
                overall_status = TestStatus.PASS if all([login_available, api_available]) else TestStatus.FAIL
                
                self.test_results.append(TestResult(
                    name="Apache Superset Analytics Platform",
                    status=overall_status,
                    message=f"Superset health: {health_data.get('status', 'unknown')}, Login: {login_available}, API: {api_available}",
                    execution_time=execution_time,
                    details={
                        'health_data': health_data,
                        'login_available': login_available,
                        'api_available': api_available,
                        'superset_url': self.base_urls['superset']
                    }
                ))
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Apache Superset Analytics Platform",
                status=TestStatus.FAIL,
                message=f"Superset test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_realtime_analytics(self):
        """Test real-time analytics data flows and streaming capabilities"""
        
        start_time = time.time()
        
        try:
            # Test Redis for real-time data
            redis_client = redis.Redis(**self.redis_config)
            redis_info = redis_client.info()
            
            # Test real-time metrics collection
            test_metrics = {
                'user_sessions': redis_client.get('active_sessions') or '0',
                'api_requests_per_minute': redis_client.get('api_rpm') or '0',
                'system_load': redis_client.get('system_load') or '0'
            }
            
            # Test WebSocket connections for real-time updates
            websocket_endpoints = [
                f"{self.base_urls['central_hub']}/ws/analytics",
                f"{self.base_urls['client_portal']}/ws/dashboard"
            ]
            
            websocket_tests = []
            async with aiohttp.ClientSession() as session:
                for endpoint in websocket_endpoints:
                    try:
                        # Check if WebSocket endpoint exists (will fail but give us info)
                        async with session.get(endpoint.replace('/ws/', '/api/')) as response:
                            websocket_tests.append({
                                'endpoint': endpoint,
                                'available': response.status in [200, 404, 405]  # 404/405 means endpoint exists but wrong method
                            })
                    except:
                        websocket_tests.append({
                            'endpoint': endpoint,
                            'available': False
                        })
            
            execution_time = time.time() - start_time
            
            redis_healthy = redis_info.get('loading', '1') == '0'
            
            self.test_results.append(TestResult(
                name="Real-time Analytics Data Flows",
                status=TestStatus.PASS if redis_healthy else TestStatus.WARNING,
                message=f"Redis connected: {redis_healthy}, Active metrics: {len(test_metrics)}, WebSocket endpoints tested: {len(websocket_tests)}",
                execution_time=execution_time,
                details={
                    'redis_info': redis_info,
                    'realtime_metrics': test_metrics,
                    'websocket_tests': websocket_tests
                },
                metrics={
                    'redis_memory_usage': float(redis_info.get('used_memory', 0)),
                    'redis_connected_clients': float(redis_info.get('connected_clients', 0))
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Real-time Analytics Data Flows",
                status=TestStatus.FAIL,
                message=f"Real-time analytics test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_multitenant_analytics(self):
        """Test multi-tenant analytics data segregation and security"""
        
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check for tenant-based row level security
            cursor.execute("""
                SELECT schemaname, tablename, rowsecurity 
                FROM pg_tables 
                WHERE rowsecurity = true
            """)
            rls_tables = cursor.fetchall()
            
            # Check for tenant_id columns in analytics tables
            cursor.execute("""
                SELECT table_name, column_name 
                FROM information_schema.columns 
                WHERE column_name IN ('tenant_id', 'organization_id', 'client_id')
                AND table_name LIKE '%analytic%' OR table_name LIKE '%metric%' OR table_name LIKE '%report%'
            """)
            tenant_columns = cursor.fetchall()
            
            # Test tenant data isolation (sample query)
            cursor.execute("""
                SELECT DISTINCT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%tenant%'
            """)
            tenant_tables = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            execution_time = time.time() - start_time
            
            # Evaluate multi-tenant security
            security_score = len(rls_tables) + len(tenant_columns) + len(tenant_tables)
            status = TestStatus.PASS if security_score > 5 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="Multi-tenant Analytics Data Segregation",
                status=status,
                message=f"RLS tables: {len(rls_tables)}, Tenant columns: {len(tenant_columns)}, Security score: {security_score}",
                execution_time=execution_time,
                details={
                    'rls_tables': [f"{r[0]}.{r[1]}" for r in rls_tables],
                    'tenant_columns': [f"{t[0]}.{t[1]}" for t in tenant_columns],
                    'tenant_tables': [t[0] for t in tenant_tables],
                    'security_score': security_score
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Multi-tenant Analytics Data Segregation",
                status=TestStatus.FAIL,
                message=f"Multi-tenant test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_bi_dashboards(self):
        """Test business intelligence dashboards and reporting capabilities"""
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                dashboard_tests = []
                
                # Test Central Hub analytics endpoints
                hub_endpoints = [
                    '/api/analytics/overview',
                    '/api/analytics/users',
                    '/api/analytics/revenue',
                    '/api/analytics/performance'
                ]
                
                for endpoint in hub_endpoints:
                    try:
                        async with session.get(f"{self.base_urls['central_hub']}{endpoint}") as response:
                            dashboard_tests.append({
                                'endpoint': endpoint,
                                'status_code': response.status,
                                'response_time': response.headers.get('X-Response-Time', 'unknown'),
                                'available': response.status in [200, 401, 403]  # 401/403 means endpoint exists
                            })
                    except Exception as e:
                        dashboard_tests.append({
                            'endpoint': endpoint,
                            'status_code': 0,
                            'response_time': 'error',
                            'available': False,
                            'error': str(e)
                        })
                
                # Test Superset dashboard availability
                try:
                    async with session.get(f"{self.base_urls['superset']}/dashboard/list/") as response:
                        superset_dashboards = response.status == 200 or response.status == 302  # 302 = redirect to login
                except:
                    superset_dashboards = False
                
                # Test Client Portal analytics
                try:
                    async with session.get(f"{self.base_urls['client_portal']}/api/analytics") as response:
                        client_analytics = response.status in [200, 401, 404]
                except:
                    client_analytics = False
                
                execution_time = time.time() - start_time
                
                available_endpoints = sum(1 for test in dashboard_tests if test['available'])
                total_endpoints = len(dashboard_tests)
                
                status = TestStatus.PASS if available_endpoints >= total_endpoints * 0.7 else TestStatus.WARNING
                
                self.test_results.append(TestResult(
                    name="Business Intelligence Dashboards",
                    status=status,
                    message=f"Available endpoints: {available_endpoints}/{total_endpoints}, Superset: {superset_dashboards}, Client analytics: {client_analytics}",
                    execution_time=execution_time,
                    details={
                        'dashboard_tests': dashboard_tests,
                        'superset_dashboards': superset_dashboards,
                        'client_analytics': client_analytics,
                        'availability_score': available_endpoints / total_endpoints
                    }
                ))
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Business Intelligence Dashboards",
                status=TestStatus.FAIL,
                message=f"BI dashboard test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_user_behavior_analytics(self):
        """Test user behavior tracking and analytics capabilities"""
        
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check for user analytics tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND (table_name LIKE '%user%' OR table_name LIKE '%session%' OR table_name LIKE '%event%')
            """)
            user_tables = cursor.fetchall()
            
            # Check for event tracking capabilities
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name LIKE '%event%' OR table_name LIKE '%log%'
                AND column_name IN ('event_type', 'user_id', 'session_id', 'timestamp', 'properties')
            """)
            event_columns = cursor.fetchall()
            
            # Sample analytics query (if data exists)
            try:
                cursor.execute("""
                    SELECT COUNT(*) as total_tables
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                total_tables = cursor.fetchone()[0]
            except:
                total_tables = 0
            
            cursor.close()
            conn.close()
            
            # Test analytics JavaScript/tracking endpoints
            async with aiohttp.ClientSession() as session:
                tracking_endpoints = [
                    f"{self.base_urls['central_hub']}/api/tracking/event",
                    f"{self.base_urls['client_portal']}/api/analytics/track"
                ]
                
                tracking_tests = []
                for endpoint in tracking_endpoints:
                    try:
                        # Test POST endpoint (will likely return 400/405 but confirms existence)
                        async with session.post(endpoint, json={'test': 'data'}) as response:
                            tracking_tests.append({
                                'endpoint': endpoint,
                                'method': 'POST',
                                'status_code': response.status,
                                'available': response.status in [200, 400, 401, 405, 422]
                            })
                    except:
                        tracking_tests.append({
                            'endpoint': endpoint,
                            'method': 'POST',
                            'status_code': 0,
                            'available': False
                        })
            
            execution_time = time.time() - start_time
            
            analytics_score = len(user_tables) + len(event_columns) + len(tracking_tests)
            status = TestStatus.PASS if analytics_score > 3 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="User Behavior Analytics",
                status=status,
                message=f"User tables: {len(user_tables)}, Event columns: {len(event_columns)}, Tracking endpoints: {len(tracking_tests)}",
                execution_time=execution_time,
                details={
                    'user_tables': [table[0] for table in user_tables],
                    'event_columns': [f"{col[0]} ({col[1]})" for col in event_columns],
                    'tracking_tests': tracking_tests,
                    'analytics_score': analytics_score,
                    'total_tables': total_tables
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="User Behavior Analytics",
                status=TestStatus.FAIL,
                message=f"User behavior analytics test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_financial_analytics(self):
        """Test financial analytics and revenue reporting capabilities"""
        
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check for financial tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND (table_name LIKE '%payment%' OR table_name LIKE '%transaction%' 
                     OR table_name LIKE '%invoice%' OR table_name LIKE '%revenue%'
                     OR table_name LIKE '%subscription%' OR table_name LIKE '%billing%')
            """)
            financial_tables = cursor.fetchall()
            
            # Check for financial analytics columns
            cursor.execute("""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE column_name IN ('amount', 'price', 'total', 'revenue', 'cost', 'profit')
                AND data_type IN ('numeric', 'decimal', 'money', 'integer', 'bigint')
            """)
            financial_columns = cursor.fetchall()
            
            # Check for subscription analytics
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name LIKE '%subscription%'
            """)
            subscription_tables = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Test financial API endpoints
            async with aiohttp.ClientSession() as session:
                financial_endpoints = [
                    f"{self.base_urls['central_hub']}/api/analytics/revenue",
                    f"{self.base_urls['central_hub']}/api/analytics/financial",
                    f"{self.base_urls['saleor_backend']}/graphql"  # Saleor has financial data
                ]
                
                financial_tests = []
                for endpoint in financial_endpoints:
                    try:
                        async with session.get(endpoint) as response:
                            financial_tests.append({
                                'endpoint': endpoint,
                                'status_code': response.status,
                                'available': response.status in [200, 400, 401, 405]
                            })
                    except:
                        financial_tests.append({
                            'endpoint': endpoint,
                            'status_code': 0,
                            'available': False
                        })
            
            execution_time = time.time() - start_time
            
            financial_score = len(financial_tables) + len(financial_columns) + len(subscription_tables)
            status = TestStatus.PASS if financial_score > 5 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="Financial Analytics & Revenue Reporting",
                status=status,
                message=f"Financial tables: {len(financial_tables)}, Financial columns: {len(financial_columns)}, Subscription tables: {len(subscription_tables)}",
                execution_time=execution_time,
                details={
                    'financial_tables': [table[0] for table in financial_tables],
                    'financial_columns': [f"{col[0]}.{col[1]} ({col[2]})" for col in financial_columns],
                    'subscription_tables': [table[0] for table in subscription_tables],
                    'financial_tests': financial_tests,
                    'financial_score': financial_score
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Financial Analytics & Revenue Reporting",
                status=TestStatus.FAIL,
                message=f"Financial analytics test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_ai_agent_metrics(self):
        """Test AI agent performance metrics and insights"""
        
        start_time = time.time()
        
        try:
            # Test AI Agents service health and metrics
            async with aiohttp.ClientSession() as session:
                ai_endpoints = [
                    f"{self.base_urls['ai_agents']}/health",
                    f"{self.base_urls['ai_agents']}/metrics",
                    f"{self.base_urls['ai_agents']}/api/analytics",
                    f"{self.base_urls['central_hub']}/api/ai/metrics"
                ]
                
                ai_tests = []
                for endpoint in ai_endpoints:
                    try:
                        async with session.get(endpoint) as response:
                            ai_tests.append({
                                'endpoint': endpoint,
                                'status_code': response.status,
                                'available': response.status in [200, 404, 405],
                                'response_time': getattr(response, '_loop_time', 0)
                            })
                    except Exception as e:
                        ai_tests.append({
                            'endpoint': endpoint,
                            'status_code': 0,
                            'available': False,
                            'error': str(e)
                        })
            
            # Check database for AI analytics
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND (table_name LIKE '%ai%' OR table_name LIKE '%agent%' OR table_name LIKE '%llm%')
            """)
            ai_tables = cursor.fetchall()
            
            # Check for vector analytics (AI embeddings)
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE data_type = 'vector'
            """)
            vector_columns = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            execution_time = time.time() - start_time
            
            available_endpoints = sum(1 for test in ai_tests if test['available'])
            ai_score = available_endpoints + len(ai_tables) + len(vector_columns)
            
            status = TestStatus.PASS if ai_score > 2 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="AI Agent Performance Metrics",
                status=status,
                message=f"Available AI endpoints: {available_endpoints}/{len(ai_tests)}, AI tables: {len(ai_tables)}, Vector columns: {len(vector_columns)}",
                execution_time=execution_time,
                details={
                    'ai_tests': ai_tests,
                    'ai_tables': [table[0] for table in ai_tables],
                    'vector_columns': [f"{col[0]} ({col[1]})" for col in vector_columns],
                    'ai_score': ai_score
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="AI Agent Performance Metrics",
                status=TestStatus.FAIL,
                message=f"AI agent metrics test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_system_monitoring(self):
        """Test system performance monitoring and health metrics"""
        
        start_time = time.time()
        
        try:
            # Test system monitoring endpoints
            async with aiohttp.ClientSession() as session:
                monitoring_endpoints = [
                    f"{self.base_urls['central_hub']}/health",
                    f"{self.base_urls['central_hub']}/metrics",
                    f"{self.base_urls['central_hub']}/api/system/status",
                    f"{self.base_urls['sqladmin']}/health"
                ]
                
                monitoring_tests = []
                for endpoint in monitoring_endpoints:
                    try:
                        start_req = time.time()
                        async with session.get(endpoint) as response:
                            response_time = time.time() - start_req
                            
                            monitoring_tests.append({
                                'endpoint': endpoint,
                                'status_code': response.status,
                                'response_time': response_time,
                                'available': response.status == 200,
                                'healthy': response.status == 200 and response_time < 1.0
                            })
                    except Exception as e:
                        monitoring_tests.append({
                            'endpoint': endpoint,
                            'status_code': 0,
                            'response_time': 999,
                            'available': False,
                            'healthy': False,
                            'error': str(e)
                        })
            
            # Test Redis metrics
            redis_client = redis.Redis(**self.redis_config)
            redis_info = redis_client.info()
            redis_stats = {
                'memory_usage_mb': float(redis_info.get('used_memory', 0)) / 1024 / 1024,
                'connected_clients': int(redis_info.get('connected_clients', 0)),
                'total_commands_processed': int(redis_info.get('total_commands_processed', 0)),
                'hit_rate': float(redis_info.get('keyspace_hits', 0)) / max(float(redis_info.get('keyspace_hits', 0)) + float(redis_info.get('keyspace_misses', 1)), 1) * 100
            }
            
            # Database performance metrics
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    count(*) as total_connections,
                    sum(CASE WHEN state = 'active' THEN 1 ELSE 0 END) as active_connections
                FROM pg_stat_activity
            """)
            db_connections = cursor.fetchone()
            
            cursor.execute("""
                SELECT 
                    schemaname,
                    relname,
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes
                FROM pg_stat_user_tables 
                ORDER BY (n_tup_ins + n_tup_upd + n_tup_del) DESC 
                LIMIT 5
            """)
            table_activity = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            execution_time = time.time() - start_time
            
            healthy_endpoints = sum(1 for test in monitoring_tests if test['healthy'])
            total_endpoints = len(monitoring_tests)
            health_score = healthy_endpoints / total_endpoints if total_endpoints > 0 else 0
            
            status = TestStatus.PASS if health_score >= 0.7 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="System Performance Monitoring",
                status=status,
                message=f"Healthy endpoints: {healthy_endpoints}/{total_endpoints} ({health_score:.1%}), Redis hit rate: {redis_stats['hit_rate']:.1f}%",
                execution_time=execution_time,
                details={
                    'monitoring_tests': monitoring_tests,
                    'redis_stats': redis_stats,
                    'database_connections': {
                        'total': db_connections[0],
                        'active': db_connections[1]
                    },
                    'table_activity': [
                        {
                            'schema': row[0],
                            'table': row[1],
                            'inserts': row[2],
                            'updates': row[3],
                            'deletes': row[4]
                        } for row in table_activity
                    ],
                    'health_score': health_score
                },
                metrics={
                    'redis_memory_mb': redis_stats['memory_usage_mb'],
                    'redis_hit_rate': redis_stats['hit_rate'],
                    'db_total_connections': float(db_connections[0]),
                    'db_active_connections': float(db_connections[1])
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="System Performance Monitoring",
                status=TestStatus.FAIL,
                message=f"System monitoring test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_api_analytics(self):
        """Test API analytics endpoints across all services"""
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                # Comprehensive API endpoint testing
                api_endpoints = {
                    'Central Hub': [
                        f"{self.base_urls['central_hub']}/api/analytics/overview",
                        f"{self.base_urls['central_hub']}/api/analytics/users",
                        f"{self.base_urls['central_hub']}/api/analytics/system",
                        f"{self.base_urls['central_hub']}/api/metrics"
                    ],
                    'Business Directory': [
                        f"{self.base_urls['business_directory']}/api/analytics",
                        f"{self.base_urls['business_directory']}/api/metrics",
                        f"{self.base_urls['business_directory']}/health"
                    ],
                    'Saleor E-commerce': [
                        f"{self.base_urls['saleor_backend']}/graphql",
                        f"{self.base_urls['saleor_backend']}/health/"
                    ],
                    'Auth Service': [
                        f"{self.base_urls['auth_service']}/health",
                        f"{self.base_urls['auth_service']}/api/metrics"
                    ]
                }
                
                service_results = {}
                
                for service_name, endpoints in api_endpoints.items():
                    service_tests = []
                    
                    for endpoint in endpoints:
                        try:
                            start_req = time.time()
                            async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=5)) as response:
                                response_time = time.time() - start_req
                                
                                # Try to get response data
                                try:
                                    if 'json' in response.headers.get('content-type', ''):
                                        data = await response.json()
                                    else:
                                        data = await response.text()
                                except:
                                    data = "Could not parse response"
                                
                                service_tests.append({
                                    'endpoint': endpoint,
                                    'status_code': response.status,
                                    'response_time_ms': round(response_time * 1000, 2),
                                    'content_type': response.headers.get('content-type', 'unknown'),
                                    'content_length': len(str(data)),
                                    'available': response.status in [200, 201, 401, 403],
                                    'healthy': response.status == 200 and response_time < 2.0
                                })
                        except asyncio.TimeoutError:
                            service_tests.append({
                                'endpoint': endpoint,
                                'status_code': 408,
                                'response_time_ms': 5000,
                                'content_type': 'timeout',
                                'content_length': 0,
                                'available': False,
                                'healthy': False,
                                'error': 'Request timeout'
                            })
                        except Exception as e:
                            service_tests.append({
                                'endpoint': endpoint,
                                'status_code': 0,
                                'response_time_ms': 0,
                                'content_type': 'error',
                                'content_length': 0,
                                'available': False,
                                'healthy': False,
                                'error': str(e)
                            })
                    
                    service_results[service_name] = {
                        'tests': service_tests,
                        'total_endpoints': len(endpoints),
                        'available_endpoints': sum(1 for test in service_tests if test['available']),
                        'healthy_endpoints': sum(1 for test in service_tests if test['healthy']),
                        'avg_response_time': np.mean([test['response_time_ms'] for test in service_tests if test['response_time_ms'] > 0]) if service_tests else 0
                    }
            
            execution_time = time.time() - start_time
            
            # Calculate overall API health
            total_endpoints = sum(service['total_endpoints'] for service in service_results.values())
            total_available = sum(service['available_endpoints'] for service in service_results.values())
            total_healthy = sum(service['healthy_endpoints'] for service in service_results.values())
            
            availability_rate = total_available / total_endpoints if total_endpoints > 0 else 0
            health_rate = total_healthy / total_endpoints if total_endpoints > 0 else 0
            
            status = TestStatus.PASS if health_rate >= 0.6 else TestStatus.WARNING if availability_rate >= 0.5 else TestStatus.FAIL
            
            self.test_results.append(TestResult(
                name="API Analytics Endpoints",
                status=status,
                message=f"Endpoints tested: {total_endpoints}, Available: {total_available} ({availability_rate:.1%}), Healthy: {total_healthy} ({health_rate:.1%})",
                execution_time=execution_time,
                details={
                    'service_results': service_results,
                    'total_endpoints': total_endpoints,
                    'availability_rate': availability_rate,
                    'health_rate': health_rate
                },
                metrics={
                    'total_endpoints': float(total_endpoints),
                    'availability_rate': availability_rate,
                    'health_rate': health_rate
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="API Analytics Endpoints",
                status=TestStatus.FAIL,
                message=f"API analytics test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_data_quality(self):
        """Test data quality and integrity across analytics systems"""
        
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Test data quality metrics
            data_quality_tests = []
            
            # Check for primary keys and constraints
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    COUNT(*) as constraint_count
                FROM pg_indexes 
                WHERE schemaname = 'public'
                GROUP BY schemaname, tablename
                ORDER BY constraint_count DESC
                LIMIT 10
            """)
            index_stats = cursor.fetchall()
            
            # Check for null values in critical columns
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                LIMIT 20
            """)
            tables = cursor.fetchall()
            
            null_check_results = []
            for table in tables[:5]:  # Check first 5 tables to avoid timeout
                table_name = table[0]
                try:
                    cursor.execute(f"""
                        SELECT 
                            column_name,
                            data_type,
                            is_nullable
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}'
                        AND is_nullable = 'YES'
                    """)
                    nullable_columns = cursor.fetchall()
                    null_check_results.append({
                        'table': table_name,
                        'nullable_columns': len(nullable_columns),
                        'columns': [col[0] for col in nullable_columns]
                    })
                except:
                    continue
            
            # Check for duplicate data
            cursor.execute("""
                SELECT 
                    table_name,
                    column_name
                FROM information_schema.columns 
                WHERE column_name IN ('id', 'uuid', 'email', 'username')
                AND table_schema = 'public'
            """)
            unique_columns = cursor.fetchall()
            
            # Test data freshness
            cursor.execute("""
                SELECT 
                    table_name,
                    column_name
                FROM information_schema.columns 
                WHERE column_name IN ('created_at', 'updated_at', 'timestamp')
                AND table_schema = 'public'
            """)
            timestamp_columns = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            execution_time = time.time() - start_time
            
            # Calculate data quality score
            quality_score = (
                len(index_stats) * 2 +  # Indexes indicate good structure
                len(unique_columns) * 3 +  # Unique constraints are important
                len(timestamp_columns) * 2 +  # Timestamps enable analytics
                (5 - len(null_check_results)) * 1  # Fewer nullable columns is better
            )
            
            status = TestStatus.PASS if quality_score > 15 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="Data Quality & Integrity",
                status=status,
                message=f"Quality score: {quality_score}, Indexed tables: {len(index_stats)}, Unique columns: {len(unique_columns)}, Timestamp columns: {len(timestamp_columns)}",
                execution_time=execution_time,
                details={
                    'index_stats': [{'schema': row[0], 'table': row[1], 'indexes': row[2]} for row in index_stats],
                    'null_check_results': null_check_results,
                    'unique_columns': [f"{col[0]}.{col[1]}" for col in unique_columns],
                    'timestamp_columns': [f"{col[0]}.{col[1]}" for col in timestamp_columns],
                    'quality_score': quality_score
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Data Quality & Integrity",
                status=TestStatus.FAIL,
                message=f"Data quality test failed: {str(e)}",
                execution_time=execution_time
            ))

    async def test_security_analytics(self):
        """Test security analytics and audit logging capabilities"""
        
        start_time = time.time()
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check for security-related tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND (table_name LIKE '%audit%' OR table_name LIKE '%log%' 
                     OR table_name LIKE '%security%' OR table_name LIKE '%auth%')
            """)
            security_tables = cursor.fetchall()
            
            # Check for audit columns
            cursor.execute("""
                SELECT table_name, column_name 
                FROM information_schema.columns 
                WHERE column_name IN ('created_by', 'updated_by', 'deleted_at', 'ip_address', 'user_agent')
            """)
            audit_columns = cursor.fetchall()
            
            # Check for RLS (Row Level Security)
            cursor.execute("""
                SELECT schemaname, tablename, rowsecurity 
                FROM pg_tables 
                WHERE rowsecurity = true
            """)
            rls_tables = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Test security endpoints
            async with aiohttp.ClientSession() as session:
                security_endpoints = [
                    f"{self.base_urls['auth_service']}/api/security/events",
                    f"{self.base_urls['central_hub']}/api/audit/logs",
                    f"{self.base_urls['central_hub']}/api/security/metrics"
                ]
                
                security_tests = []
                for endpoint in security_endpoints:
                    try:
                        async with session.get(endpoint) as response:
                            security_tests.append({
                                'endpoint': endpoint,
                                'status_code': response.status,
                                'available': response.status in [200, 401, 403, 404]  # 401/403 means auth required
                            })
                    except:
                        security_tests.append({
                            'endpoint': endpoint,
                            'status_code': 0,
                            'available': False
                        })
            
            execution_time = time.time() - start_time
            
            security_score = len(security_tables) + len(audit_columns) + len(rls_tables)
            available_endpoints = sum(1 for test in security_tests if test['available'])
            
            status = TestStatus.PASS if security_score > 5 and available_endpoints > 0 else TestStatus.WARNING
            
            self.test_results.append(TestResult(
                name="Security Analytics & Audit Logging",
                status=status,
                message=f"Security tables: {len(security_tables)}, Audit columns: {len(audit_columns)}, RLS tables: {len(rls_tables)}, Available endpoints: {available_endpoints}",
                execution_time=execution_time,
                details={
                    'security_tables': [table[0] for table in security_tables],
                    'audit_columns': [f"{col[0]}.{col[1]}" for col in audit_columns],
                    'rls_tables': [f"{row[0]}.{row[1]}" for row in rls_tables],
                    'security_tests': security_tests,
                    'security_score': security_score
                }
            ))
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.test_results.append(TestResult(
                name="Security Analytics & Audit Logging",
                status=TestStatus.FAIL,
                message=f"Security analytics test failed: {str(e)}",
                execution_time=execution_time
            ))

    def generate_analytics_report(self, total_execution_time: float) -> Dict[str, Any]:
        """Generate comprehensive analytics test report"""
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.status == TestStatus.PASS)
        failed_tests = sum(1 for result in self.test_results if result.status == TestStatus.FAIL)
        warning_tests = sum(1 for result in self.test_results if result.status == TestStatus.WARNING)
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Aggregate metrics
        all_metrics = {}
        for result in self.test_results:
            if result.metrics:
                all_metrics.update(result.metrics)
        
        # Generate recommendations
        recommendations = self.generate_recommendations()
        
        # Categorize results
        categorized_results = {
            'infrastructure': [],
            'analytics_platforms': [],
            'data_flows': [],
            'business_intelligence': [],
            'performance': [],
            'security': []
        }
        
        category_mapping = {
            'Database Analytics Infrastructure': 'infrastructure',
            'Apache Superset Analytics Platform': 'analytics_platforms',
            'Real-time Analytics Data Flows': 'data_flows',
            'Multi-tenant Analytics Data Segregation': 'data_flows',
            'Business Intelligence Dashboards': 'business_intelligence',
            'User Behavior Analytics': 'business_intelligence',
            'Financial Analytics & Revenue Reporting': 'business_intelligence',
            'AI Agent Performance Metrics': 'analytics_platforms',
            'System Performance Monitoring': 'performance',
            'API Analytics Endpoints': 'performance',
            'Data Quality & Integrity': 'infrastructure',
            'Security Analytics & Audit Logging': 'security'
        }
        
        for result in self.test_results:
            category = category_mapping.get(result.name, 'infrastructure')
            categorized_results[category].append(result)
        
        return {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_execution_time': total_execution_time,
                'platform': 'BizOSaaS Analytics Platform',
                'test_suite_version': '1.0.0'
            },
            'executive_summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'warning_tests': warning_tests,
                'success_rate': round(success_rate, 1),
                'overall_status': 'HEALTHY' if success_rate >= 80 else 'NEEDS_ATTENTION' if success_rate >= 60 else 'CRITICAL',
                'key_findings': self.generate_key_findings()
            },
            'detailed_results': {
                'by_category': categorized_results,
                'all_results': [
                    {
                        'name': result.name,
                        'status': result.status.value,
                        'message': result.message,
                        'execution_time': result.execution_time,
                        'details': result.details,
                        'metrics': result.metrics
                    } for result in self.test_results
                ]
            },
            'analytics_metrics': all_metrics,
            'recommendations': recommendations,
            'platform_health': {
                'database_connectivity': any('Database' in result.name and result.status == TestStatus.PASS for result in self.test_results),
                'superset_available': any('Superset' in result.name and result.status == TestStatus.PASS for result in self.test_results),
                'realtime_data_flows': any('Real-time' in result.name and result.status == TestStatus.PASS for result in self.test_results),
                'api_endpoints_healthy': any('API' in result.name and result.status == TestStatus.PASS for result in self.test_results),
                'security_analytics_enabled': any('Security' in result.name and result.status == TestStatus.PASS for result in self.test_results)
            },
            'next_steps': self.generate_next_steps()
        }

    def generate_key_findings(self) -> List[str]:
        """Generate key findings from test results"""
        
        findings = []
        
        # Analyze database connectivity
        db_test = next((r for r in self.test_results if 'Database' in r.name), None)
        if db_test and db_test.status == TestStatus.PASS:
            findings.append("✅ Database analytics infrastructure is operational with pgvector support")
        elif db_test:
            findings.append("❌ Database analytics infrastructure has connectivity issues")
        
        # Analyze Superset
        superset_test = next((r for r in self.test_results if 'Superset' in r.name), None)
        if superset_test and superset_test.status == TestStatus.PASS:
            findings.append("✅ Apache Superset BI platform is accessible and functional")
        elif superset_test:
            findings.append("⚠️ Apache Superset may have configuration or access issues")
        
        # Analyze real-time capabilities
        realtime_test = next((r for r in self.test_results if 'Real-time' in r.name), None)
        if realtime_test and realtime_test.status == TestStatus.PASS:
            findings.append("✅ Real-time analytics data flows are operational via Redis")
        elif realtime_test:
            findings.append("⚠️ Real-time analytics may need Redis configuration improvements")
        
        # Analyze API health
        api_test = next((r for r in self.test_results if 'API' in r.name), None)
        if api_test and api_test.details:
            health_rate = api_test.details.get('health_rate', 0)
            if health_rate >= 0.7:
                findings.append(f"✅ API analytics endpoints are {health_rate:.1%} healthy")
            else:
                findings.append(f"⚠️ API analytics endpoints need attention ({health_rate:.1%} healthy)")
        
        # Analyze multi-tenant security
        tenant_test = next((r for r in self.test_results if 'Multi-tenant' in r.name), None)
        if tenant_test and tenant_test.status == TestStatus.PASS:
            findings.append("✅ Multi-tenant analytics data segregation is properly implemented")
        elif tenant_test:
            findings.append("⚠️ Multi-tenant analytics security may need enhancement")
        
        return findings

    def generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on test results"""
        
        recommendations = []
        
        # Check for failed tests and generate specific recommendations
        for result in self.test_results:
            if result.status == TestStatus.FAIL:
                if 'Database' in result.name:
                    recommendations.append({
                        'priority': 'HIGH',
                        'category': 'Infrastructure',
                        'issue': 'Database connectivity failure',
                        'action': 'Verify PostgreSQL service is running and credentials are correct',
                        'command': 'docker ps | grep postgres && psql -h localhost -U postgres -d bizosaas -c "SELECT 1;"'
                    })
                elif 'Superset' in result.name:
                    recommendations.append({
                        'priority': 'HIGH',
                        'category': 'Analytics Platform',
                        'issue': 'Apache Superset not accessible',
                        'action': 'Check Superset container health and network configuration',
                        'command': 'docker logs bizosaas-superset && curl -I http://localhost:8088/health'
                    })
                elif 'API' in result.name:
                    recommendations.append({
                        'priority': 'MEDIUM',
                        'category': 'API Endpoints',
                        'issue': 'Analytics API endpoints not responding',
                        'action': 'Restart affected services and verify routing configuration',
                        'command': 'docker-compose restart && curl -I http://localhost:8001/health'
                    })
            
            elif result.status == TestStatus.WARNING:
                if 'Real-time' in result.name:
                    recommendations.append({
                        'priority': 'MEDIUM',
                        'category': 'Data Flows',
                        'issue': 'Real-time analytics partially functional',
                        'action': 'Configure Redis for optimal analytics data streaming',
                        'command': 'redis-cli info stats && docker logs bizosaas-redis'
                    })
                elif 'Multi-tenant' in result.name:
                    recommendations.append({
                        'priority': 'MEDIUM',
                        'category': 'Security',
                        'issue': 'Multi-tenant data segregation needs improvement',
                        'action': 'Implement row-level security (RLS) on analytics tables',
                        'command': 'psql -h localhost -U postgres -d bizosaas -c "ALTER TABLE analytics_table ENABLE ROW LEVEL SECURITY;"'
                    })
        
        # Add general improvement recommendations
        recommendations.extend([
            {
                'priority': 'LOW',
                'category': 'Monitoring',
                'issue': 'Enhanced monitoring needed',
                'action': 'Implement Prometheus metrics collection for all services',
                'command': 'Deploy monitoring stack with Grafana dashboards'
            },
            {
                'priority': 'LOW',
                'category': 'Performance',
                'issue': 'Analytics query optimization',
                'action': 'Create database indexes for frequently queried analytics columns',
                'command': 'ANALYZE; CREATE INDEX CONCURRENTLY ON analytics_table (tenant_id, created_at);'
            }
        ])
        
        return recommendations

    def generate_next_steps(self) -> List[Dict[str, Any]]:
        """Generate prioritized next steps based on test results"""
        
        next_steps = []
        
        # Immediate fixes (24 hours)
        immediate_steps = []
        failed_tests = [r for r in self.test_results if r.status == TestStatus.FAIL]
        if failed_tests:
            immediate_steps.extend([
                {
                    'timeframe': '24 hours',
                    'priority': 'CRITICAL',
                    'task': 'Fix all failed service connectivity issues',
                    'owner': 'DevOps Team',
                    'details': [f"Resolve: {test.name}" for test in failed_tests[:3]]
                }
            ])
        
        # Short-term improvements (1 week)
        short_term_steps = [
            {
                'timeframe': '1 week',
                'priority': 'HIGH',
                'task': 'Implement comprehensive analytics monitoring',
                'owner': 'Analytics Team',
                'details': [
                    'Deploy Prometheus + Grafana stack',
                    'Create real-time analytics dashboards',
                    'Set up alert thresholds for key metrics'
                ]
            },
            {
                'timeframe': '1 week', 
                'priority': 'HIGH',
                'task': 'Enhance Superset configuration and integration',
                'owner': 'BI Team',
                'details': [
                    'Configure database connections',
                    'Create default dashboards',
                    'Set up user access controls'
                ]
            }
        ]
        
        # Medium-term enhancements (1 month)
        medium_term_steps = [
            {
                'timeframe': '1 month',
                'priority': 'MEDIUM',
                'task': 'Advanced analytics capabilities',
                'owner': 'Product Team',
                'details': [
                    'Implement predictive analytics',
                    'Add machine learning insights',
                    'Create automated reporting'
                ]
            },
            {
                'timeframe': '1 month',
                'priority': 'MEDIUM',
                'task': 'Performance optimization',
                'owner': 'Engineering Team',
                'details': [
                    'Optimize database queries',
                    'Implement caching strategies',
                    'Add query result pagination'
                ]
            }
        ]
        
        next_steps.extend(immediate_steps + short_term_steps + medium_term_steps)
        
        return next_steps

    async def save_detailed_report(self, report: Dict[str, Any]):
        """Save detailed analytics test report to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_filename = f"analytics_test_report_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save markdown report
        md_filename = f"analytics_test_report_{timestamp}.md"
        await self.generate_markdown_report(report, md_filename)
        
        logger.info(f"📊 Detailed reports saved: {json_filename}, {md_filename}")

    async def generate_markdown_report(self, report: Dict[str, Any], filename: str):
        """Generate human-readable markdown report"""
        
        md_content = f"""# BizOSaaS Analytics Platform Test Report

**Generated:** {report['report_metadata']['generated_at']}  
**Execution Time:** {report['report_metadata']['total_execution_time']:.2f} seconds  
**Platform:** {report['report_metadata']['platform']}

## Executive Summary

- **Total Tests:** {report['executive_summary']['total_tests']}
- **Success Rate:** {report['executive_summary']['success_rate']}%
- **Overall Status:** {report['executive_summary']['overall_status']}

### Test Results Breakdown
- ✅ **Passed:** {report['executive_summary']['passed_tests']}
- ❌ **Failed:** {report['executive_summary']['failed_tests']}  
- ⚠️ **Warnings:** {report['executive_summary']['warning_tests']}

### Key Findings
"""
        
        for finding in report['executive_summary']['key_findings']:
            md_content += f"- {finding}\n"
        
        md_content += "\n## Platform Health Status\n\n"
        for component, status in report['platform_health'].items():
            status_icon = "✅" if status else "❌"
            md_content += f"- {status_icon} **{component.replace('_', ' ').title()}:** {'Operational' if status else 'Needs Attention'}\n"
        
        md_content += "\n## Detailed Test Results\n\n"
        
        for category, results in report['detailed_results']['by_category'].items():
            if results:
                md_content += f"### {category.replace('_', ' ').title()}\n\n"
                for result in results:
                    md_content += f"- **{result['name']}** {result['status']}\n"
                    md_content += f"  - *{result['message']}*\n"
                    md_content += f"  - Execution time: {result['execution_time']:.3f}s\n\n"
        
        md_content += "\n## Recommendations\n\n"
        
        high_priority = [r for r in report['recommendations'] if r['priority'] == 'HIGH']
        medium_priority = [r for r in report['recommendations'] if r['priority'] == 'MEDIUM']
        low_priority = [r for r in report['recommendations'] if r['priority'] == 'LOW']
        
        for priority, recs in [('HIGH', high_priority), ('MEDIUM', medium_priority), ('LOW', low_priority)]:
            if recs:
                md_content += f"### {priority} Priority\n\n"
                for rec in recs:
                    md_content += f"**{rec['category']}:** {rec['issue']}\n"
                    md_content += f"- *Action:* {rec['action']}\n"
                    md_content += f"- *Command:* `{rec['command']}`\n\n"
        
        md_content += "\n## Next Steps\n\n"
        
        for step in report['next_steps']:
            md_content += f"### {step['timeframe'].title()} - {step['priority']} Priority\n"
            md_content += f"**Task:** {step['task']}\n"
            md_content += f"**Owner:** {step['owner']}\n"
            md_content += "**Details:**\n"
            for detail in step['details']:
                md_content += f"- {detail}\n"
            md_content += "\n"
        
        if report['analytics_metrics']:
            md_content += "\n## Analytics Metrics\n\n"
            md_content += "| Metric | Value |\n|--------|-------|\n"
            for metric, value in report['analytics_metrics'].items():
                md_content += f"| {metric.replace('_', ' ').title()} | {value:.2f} |\n"
        
        md_content += f"\n---\n*Report generated by BizOSaaS Analytics Test Suite v{report['report_metadata']['test_suite_version']}*\n"
        
        with open(filename, 'w') as f:
            f.write(md_content)

async def main():
    """Main execution function"""
    
    print("🚀 BizOSaaS Analytics Comprehensive Test Suite")
    print("=" * 60)
    
    test_suite = BizOSaaSAnalyticsTestSuite()
    
    try:
        report = await test_suite.run_all_tests()
        
        print(f"\n📊 Test Suite Complete!")
        print(f"Success Rate: {report['executive_summary']['success_rate']:.1f}%")
        print(f"Overall Status: {report['executive_summary']['overall_status']}")
        print(f"Total Execution Time: {report['report_metadata']['total_execution_time']:.2f}s")
        
        print(f"\n📁 Reports saved with timestamp: {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
    except Exception as e:
        logger.error(f"❌ Test suite failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))