"""
Health Checker
Performs health checks for all registered integrations
"""

import asyncio
import aiohttp
import logging
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from urllib.parse import urlparse
import ssl

from config.settings import settings

logger = logging.getLogger(__name__)


class HealthChecker:
    """
    Performs health checks on integration endpoints
    Supports multiple authentication methods and health check patterns
    """
    
    def __init__(self):
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.active_checks: Dict[str, asyncio.Task] = {}
        
        # Health check statistics
        self.check_stats = {
            'total_checks': 0,
            'successful_checks': 0,
            'failed_checks': 0,
            'average_response_time': 0.0,
            'checks_by_integration': {}
        }
        
        logger.info("Health Checker initialized")
    
    async def initialize(self):
        """Initialize the health checker"""
        try:
            # Create HTTP session with optimized settings
            connector = aiohttp.TCPConnector(
                limit=100,  # Total connection pool size
                limit_per_host=30,  # Connections per host
                ttl_dns_cache=300,  # DNS cache TTL
                use_dns_cache=True,
                keepalive_timeout=30,
                enable_cleanup_closed=True
            )
            
            timeout = aiohttp.ClientTimeout(
                total=settings.HEALTH_CHECK_TIMEOUT,
                connect=5,
                sock_read=10
            )
            
            self.http_session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    'User-Agent': 'BizOSaaS-Integration-Monitor/1.0',
                    'Accept': 'application/json, text/plain, */*'
                }
            )
            
            logger.info("Health Checker initialized with HTTP session")
            
        except Exception as e:
            logger.error(f"Failed to initialize Health Checker: {e}")
            raise
    
    async def check_health(self, integration: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform health check for a specific integration
        
        Args:
            integration: Integration configuration
            
        Returns:
            Dict containing health check results
        """
        integration_name = integration['name']
        health_endpoint = integration.get('health_check_endpoint', {})
        
        if not health_endpoint:
            logger.warning(f"No health check endpoint configured for {integration_name}")
            return {
                'success': False,
                'status_code': 0,
                'response_time': 0.0,
                'error': 'No health check endpoint configured',
                'metadata': {}
            }
        
        start_time = time.time()
        
        try:
            # Increment stats
            self.check_stats['total_checks'] += 1
            integration_stats = self.check_stats['checks_by_integration'].get(integration_name, 0)
            self.check_stats['checks_by_integration'][integration_name] = integration_stats + 1
            
            # Perform the health check
            result = await self._perform_health_check(integration_name, health_endpoint)
            
            # Calculate response time
            response_time = time.time() - start_time
            result['response_time'] = response_time
            
            # Update statistics
            if result['success']:
                self.check_stats['successful_checks'] += 1
            else:
                self.check_stats['failed_checks'] += 1
            
            # Update average response time
            total_checks = self.check_stats['total_checks']
            current_avg = self.check_stats['average_response_time']
            self.check_stats['average_response_time'] = (current_avg * (total_checks - 1) + response_time) / total_checks
            
            logger.debug(f"Health check completed for {integration_name}: {result['success']} ({response_time:.3f}s)")
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"Health check failed for {integration_name}: {e}")
            
            self.check_stats['failed_checks'] += 1
            
            return {
                'success': False,
                'status_code': 0,
                'response_time': response_time,
                'error': str(e),
                'metadata': {'exception_type': type(e).__name__}
            }
    
    async def _perform_health_check(self, integration_name: str, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Perform the actual health check HTTP request"""
        
        url = endpoint.get('url', '')
        method = endpoint.get('method', 'GET').upper()
        headers = endpoint.get('headers', {}).copy()
        timeout = endpoint.get('timeout', settings.HEALTH_CHECK_TIMEOUT)
        expected_status = endpoint.get('expected_status', [200])
        auth_config = endpoint.get('authentication', {})
        
        # Handle URL templating (basic substitution)
        url = self._substitute_url_variables(url, integration_name)
        
        # Add authentication headers
        headers = await self._add_authentication(headers, auth_config, integration_name)
        
        # Prepare request body for POST/PUT requests
        data = None
        if method in ['POST', 'PUT']:
            data = await self._prepare_health_check_body(integration_name, endpoint)
        
        try:
            # Make HTTP request
            async with self.http_session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=timeout),
                ssl=False if url.startswith('http://') else True
            ) as response:
                
                status_code = response.status
                success = status_code in expected_status
                
                # Read response body (limited size)
                try:
                    if response.content_type == 'application/json':
                        response_data = await response.json()
                    else:
                        response_text = await response.text()
                        response_data = response_text[:1000]  # Limit response size
                except:
                    response_data = None
                
                # Additional health checks based on response content
                content_health = await self._validate_response_content(
                    integration_name, response_data, status_code
                )
                
                return {
                    'success': success and content_health,
                    'status_code': status_code,
                    'response_data': response_data,
                    'headers': dict(response.headers),
                    'url': str(response.url),
                    'metadata': {
                        'method': method,
                        'content_type': response.content_type,
                        'content_length': response.headers.get('content-length'),
                        'server': response.headers.get('server'),
                        'cache_control': response.headers.get('cache-control'),
                        'content_health': content_health
                    }
                }
                
        except asyncio.TimeoutError:
            return {
                'success': False,
                'status_code': 0,
                'error': f'Request timeout after {timeout}s',
                'metadata': {'timeout': timeout, 'url': url}
            }
        except aiohttp.ClientConnectorError as e:
            return {
                'success': False,
                'status_code': 0,
                'error': f'Connection error: {str(e)}',
                'metadata': {'connection_error': True, 'url': url}
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': 0,
                'error': f'Unexpected error: {str(e)}',
                'metadata': {'exception_type': type(e).__name__, 'url': url}
            }
    
    def _substitute_url_variables(self, url: str, integration_name: str) -> str:
        """Substitute URL variables with actual values"""
        
        # Common substitutions for health checks
        substitutions = {
            'stripe': {
                '{customer_id}': 'cus_test',
                '{payment_intent_id}': 'pi_test'
            },
            'paypal': {
                '{account_sid}': 'test_account'
            },
            'google_ads': {
                '{customer_id}': '1234567890'
            },
            'facebook_ads': {
                '{account_id}': '123456789',
                '{campaign_id}': 'test_campaign'
            },
            'google_analytics': {
                '{property_id}': '123456789'
            },
            'facebook_pixel': {
                '{pixel_id}': '123456789'
            },
            'aws_s3': {
                '{bucket}': 'test-bucket',
                '{key}': 'health-check.txt'
            },
            'cloudflare': {
                '{zone_id}': 'test_zone'
            },
            'whatsapp_business': {
                '{phone_number_id}': '123456789'
            },
            'twilio_sms': {
                '{account_sid}': 'test_account'
            }
        }
        
        integration_substitutions = substitutions.get(integration_name, {})
        
        for placeholder, value in integration_substitutions.items():
            url = url.replace(placeholder, value)
        
        return url
    
    async def _add_authentication(self, headers: Dict[str, str], auth_config: Dict[str, Any], integration_name: str) -> Dict[str, str]:
        """Add authentication headers based on configuration"""
        
        auth_type = auth_config.get('type', 'none')
        auth_header = auth_config.get('header', 'Authorization')
        
        if auth_type == 'none':
            return headers
        
        # Get authentication credentials (would come from vault in production)
        credentials = await self._get_integration_credentials(integration_name)
        
        if not credentials:
            logger.warning(f"No credentials available for {integration_name}")
            return headers
        
        try:
            if auth_type == 'bearer':
                token = credentials.get('access_token') or credentials.get('api_key')
                if token:
                    headers[auth_header] = f'Bearer {token}'
            
            elif auth_type == 'basic':
                username = credentials.get('username') or credentials.get('client_id')
                password = credentials.get('password') or credentials.get('client_secret')
                if username and password:
                    import base64
                    auth_string = base64.b64encode(f'{username}:{password}'.encode()).decode()
                    headers[auth_header] = f'Basic {auth_string}'
            
            elif auth_type == 'x-api-key':
                api_key = credentials.get('api_key')
                if api_key:
                    headers[auth_header] = api_key
            
            elif auth_type == 'oauth2':
                access_token = credentials.get('access_token')
                if access_token:
                    headers[auth_header] = f'Bearer {access_token}'
            
            elif auth_type == 'aws_sig4':
                # AWS Signature V4 would be implemented here
                # For health checks, we'll use a simpler approach
                access_key = credentials.get('aws_access_key_id')
                if access_key:
                    headers['x-amz-content-sha256'] = 'UNSIGNED-PAYLOAD'
            
        except Exception as e:
            logger.error(f"Failed to add authentication for {integration_name}: {e}")
        
        return headers
    
    async def _get_integration_credentials(self, integration_name: str) -> Dict[str, Any]:
        """Get integration credentials from secure storage"""
        
        # In production, this would fetch from Vault or encrypted storage
        # For development/testing, return mock credentials
        mock_credentials = {
            'stripe': {
                'api_key': 'sk_test_mock_key'
            },
            'paypal': {
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret'
            },
            'google_ads': {
                'access_token': 'mock_access_token',
                'developer_token': 'mock_developer_token'
            },
            'facebook_ads': {
                'access_token': 'mock_access_token'
            },
            'openai': {
                'api_key': 'sk-mock_api_key'
            },
            'anthropic': {
                'api_key': 'mock_anthropic_key'
            },
            'aws_s3': {
                'aws_access_key_id': 'mock_access_key',
                'aws_secret_access_key': 'mock_secret_key'
            },
            'cloudflare': {
                'api_key': 'mock_cloudflare_key'
            }
        }
        
        return mock_credentials.get(integration_name, {})
    
    async def _prepare_health_check_body(self, integration_name: str, endpoint: Dict[str, Any]) -> Optional[str]:
        """Prepare request body for health check POST requests"""
        
        # Integration-specific health check bodies
        health_check_bodies = {
            'google_analytics': {
                'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                'metrics': [{'name': 'sessions'}],
                'dimensions': [{'name': 'date'}]
            },
            'facebook_pixel': {
                'data': [{
                    'event_name': 'PageView',
                    'event_time': int(time.time()),
                    'action_source': 'website'
                }],
                'test_event_code': 'TEST12345'
            },
            'anthropic': {
                'model': 'claude-3-haiku-20240307',
                'max_tokens': 10,
                'messages': [{'role': 'user', 'content': 'Hi'}]
            }
        }
        
        body_data = health_check_bodies.get(integration_name)
        if body_data:
            return json.dumps(body_data)
        
        return None
    
    async def _validate_response_content(self, integration_name: str, response_data: Any, status_code: int) -> bool:
        """Validate response content for additional health indicators"""
        
        if status_code >= 500:
            return False
        
        if not response_data:
            return True  # Empty response is acceptable for some health checks
        
        try:
            # Integration-specific content validation
            if integration_name == 'stripe':
                if isinstance(response_data, dict):
                    return 'object' in response_data or 'id' in response_data
            
            elif integration_name == 'paypal':
                if isinstance(response_data, dict):
                    return 'access_token' in response_data or 'token_type' in response_data
            
            elif integration_name == 'google_ads':
                if isinstance(response_data, dict):
                    return 'results' in response_data or 'fieldMask' in response_data
            
            elif integration_name == 'facebook_ads':
                if isinstance(response_data, dict):
                    return 'id' in response_data or 'name' in response_data
            
            elif integration_name == 'openai':
                if isinstance(response_data, dict):
                    return 'data' in response_data or 'object' in response_data
            
            elif integration_name == 'aws_s3':
                # For S3, success status is sufficient
                return True
            
            elif integration_name == 'cloudflare':
                if isinstance(response_data, dict):
                    return response_data.get('success', False)
            
            # Default: check for common error indicators
            if isinstance(response_data, dict):
                error_indicators = ['error', 'errors', 'message', 'detail']
                has_error = any(indicator in response_data for indicator in error_indicators)
                return not has_error
            
            return True
            
        except Exception as e:
            logger.debug(f"Content validation error for {integration_name}: {e}")
            return True  # Don't fail health check due to validation errors
    
    async def check_multiple_integrations(self, integrations: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Perform health checks for multiple integrations concurrently"""
        
        tasks = {}
        for integration in integrations:
            integration_name = integration['name']
            task = asyncio.create_task(self.check_health(integration))
            tasks[integration_name] = task
        
        # Wait for all health checks to complete
        results = {}
        for integration_name, task in tasks.items():
            try:
                results[integration_name] = await task
            except Exception as e:
                logger.error(f"Health check task failed for {integration_name}: {e}")
                results[integration_name] = {
                    'success': False,
                    'status_code': 0,
                    'response_time': 0.0,
                    'error': f'Task execution failed: {str(e)}',
                    'metadata': {}
                }
        
        return results
    
    async def continuous_health_check(self, integration: Dict[str, Any], interval: int = 60):
        """Run continuous health checks for an integration"""
        integration_name = integration['name']
        
        logger.info(f"Starting continuous health check for {integration_name} (interval: {interval}s)")
        
        while True:
            try:
                result = await self.check_health(integration)
                
                if not result['success']:
                    logger.warning(f"Health check failed for {integration_name}: {result.get('error', 'Unknown error')}")
                else:
                    logger.debug(f"Health check passed for {integration_name}")
                
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                logger.info(f"Continuous health check cancelled for {integration_name}")
                break
            except Exception as e:
                logger.error(f"Continuous health check error for {integration_name}: {e}")
                await asyncio.sleep(interval)
    
    # Public API methods
    
    async def get_health_statistics(self) -> Dict[str, Any]:
        """Get health check statistics"""
        total = self.check_stats['total_checks']
        success_rate = (self.check_stats['successful_checks'] / total * 100) if total > 0 else 0
        
        return {
            **self.check_stats,
            'success_rate': success_rate,
            'failure_rate': 100 - success_rate,
            'active_checks': len(self.active_checks)
        }
    
    async def get_integration_health_history(self, integration_name: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get health check history for specific integration"""
        # This would query the database in a real implementation
        # For now, return mock data
        return []
    
    async def force_health_check(self, integration: Dict[str, Any]) -> Dict[str, Any]:
        """Force immediate health check for integration"""
        return await self.check_health(integration)
    
    async def cleanup(self):
        """Cleanup resources"""
        # Cancel all active checks
        for integration_name, task in self.active_checks.items():
            task.cancel()
            logger.info(f"Cancelled continuous health check for {integration_name}")
        
        # Close HTTP session
        if self.http_session:
            await self.http_session.close()
        
        logger.info("Health Checker cleaned up")