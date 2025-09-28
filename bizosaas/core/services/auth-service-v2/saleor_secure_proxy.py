#!/usr/bin/env python3

"""
Secure Saleor Dashboard Proxy
Provides authenticated access to Saleor dashboard at localhost:9020
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any
from aiohttp import web, ClientSession
import aiohttp_cors
from urllib.parse import urljoin, urlparse

from auth_security import AuthenticationService, AuthMiddleware, SecurityEvent, SecurityEventType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureSaleorProxy:
    """Secure proxy for Saleor dashboard with comprehensive authentication"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth_service = AuthenticationService(config)
        self.saleor_api_url = config.get('saleor_api_url', 'http://localhost:8024')
        self.saleor_dashboard_url = config.get('saleor_dashboard_url', 'http://localhost:9020')
        self.allowed_origins = config.get('allowed_origins', ['http://localhost:3000'])
        
        # Security configuration
        self.rate_limits = {
            'api': (100, 60),      # 100 API calls per minute
            'admin': (50, 60),     # 50 admin actions per minute
            'graphql': (200, 60)   # 200 GraphQL queries per minute
        }
        
        # Required permissions for different endpoints
        self.endpoint_permissions = {
            '/dashboard/': ['saleor:read', 'dashboard:access'],
            '/api/': ['saleor:api'],
            '/graphql/': ['saleor:graphql'],
            '/admin/': ['saleor:admin'],
            '/media/': ['saleor:media'],
            '/static/': []  # Static files don't require authentication
        }
    
    async def initialize(self):
        """Initialize the proxy service"""
        await self.auth_service.initialize()
        logger.info("Secure Saleor proxy initialized")
    
    def get_required_permissions(self, path: str) -> list:
        """Get required permissions for a path"""
        for endpoint, permissions in self.endpoint_permissions.items():
            if path.startswith(endpoint):
                return permissions
        return ['saleor:read']  # Default permission
    
    async def check_access_permissions(self, request, required_permissions: list) -> bool:
        """Check if user has required permissions"""
        session = request.get('session')
        api_key = request.get('api_key')
        
        if not session and not api_key:
            return False
        
        # Get user permissions
        permissions = []
        if session:
            permissions = session.permissions
        elif api_key:
            permissions = api_key.get('permissions', [])
        
        # Check permissions
        for required in required_permissions:
            if required in permissions or 'admin:*' in permissions:
                continue
            # Check wildcard permissions
            if any(perm.endswith('*') and required.startswith(perm[:-1]) for perm in permissions):
                continue
            return False
        
        return True
    
    async def check_rate_limit(self, request, action: str) -> bool:
        """Check rate limiting for actions"""
        if action not in self.rate_limits:
            return True
        
        session = request.get('session')
        identifier = session.user_id if session else request.remote
        
        return await self.auth_service.check_rate_limit(identifier, action)
    
    async def log_access_attempt(self, request, success: bool, details: Dict[str, Any] = None):
        """Log access attempt for security monitoring"""
        session = request.get('session')
        
        if session:
            event_type = SecurityEventType.LOGIN_SUCCESS if success else SecurityEventType.UNAUTHORIZED_ACCESS
            risk_score = 0 if success else 40
            
            await self.auth_service.log_security_event(SecurityEvent(
                event_type=event_type,
                user_id=session.user_id,
                tenant_id=session.tenant_id,
                ip_address=request.remote,
                user_agent=request.headers.get('User-Agent', ''),
                timestamp=datetime.utcnow(),
                details=details or {'path': request.path},
                risk_score=risk_score
            ))
    
    async def handle_dashboard_request(self, request):
        """Handle dashboard requests with authentication"""
        path = request.path
        method = request.method
        
        logger.info(f"Dashboard request: {method} {path}")
        
        # Check if static files (allow without authentication)
        if path.startswith('/static/') or path.startswith('/media/'):
            return await self.proxy_to_saleor(request, self.saleor_dashboard_url)
        
        # Get required permissions
        required_permissions = self.get_required_permissions(path)
        
        # Check authentication for protected resources
        if required_permissions:
            if not await self.check_access_permissions(request, required_permissions):
                await self.log_access_attempt(request, False, {
                    'reason': 'insufficient_permissions',
                    'required': required_permissions,
                    'path': path
                })
                
                return web.json_response({
                    'error': 'Insufficient permissions for Saleor dashboard',
                    'required_permissions': required_permissions,
                    'code': 'SALEOR_PERMISSION_DENIED'
                }, status=403)
        
        # Check rate limiting
        action = 'admin' if '/admin/' in path else 'api'
        allowed, remaining = await self.check_rate_limit(request, action)
        
        if not allowed:
            await self.log_access_attempt(request, False, {
                'reason': 'rate_limit_exceeded',
                'action': action,
                'path': path
            })
            
            return web.json_response({
                'error': 'Rate limit exceeded',
                'retry_after': 60,
                'code': 'RATE_LIMIT_EXCEEDED'
            }, status=429)
        
        # Log successful access
        await self.log_access_attempt(request, True, {'action': action, 'path': path})
        
        # Proxy to Saleor dashboard
        return await self.proxy_to_saleor(request, self.saleor_dashboard_url)
    
    async def handle_api_request(self, request):
        """Handle API requests with authentication"""
        path = request.path
        
        # Check permissions
        required_permissions = self.get_required_permissions(path)
        
        if not await self.check_access_permissions(request, required_permissions):
            return web.json_response({
                'error': 'Insufficient permissions for API access',
                'required_permissions': required_permissions,
                'code': 'API_PERMISSION_DENIED'
            }, status=403)
        
        # Check rate limiting
        allowed, remaining = await self.check_rate_limit(request, 'api')
        
        if not allowed:
            return web.json_response({
                'error': 'API rate limit exceeded',
                'retry_after': 60,
                'code': 'RATE_LIMIT_EXCEEDED'
            }, status=429)
        
        # Proxy to Saleor API
        return await self.proxy_to_saleor(request, self.saleor_api_url)
    
    async def handle_graphql_request(self, request):
        """Handle GraphQL requests with authentication and query analysis"""
        # Check permissions
        required_permissions = ['saleor:graphql']
        
        if not await self.check_access_permissions(request, required_permissions):
            return web.json_response({
                'error': 'Insufficient permissions for GraphQL access',
                'code': 'GRAPHQL_PERMISSION_DENIED'
            }, status=403)
        
        # Check rate limiting
        allowed, remaining = await self.check_rate_limit(request, 'graphql')
        
        if not allowed:
            return web.json_response({
                'error': 'GraphQL rate limit exceeded',
                'retry_after': 60,
                'code': 'RATE_LIMIT_EXCEEDED'
            }, status=429)
        
        # Analyze GraphQL query for security
        if request.method == 'POST':
            try:
                data = await request.json()
                query = data.get('query', '')
                
                # Check for potentially dangerous operations
                dangerous_operations = ['mutation', 'subscription']
                if any(op in query.lower() for op in dangerous_operations):
                    # Require higher permissions for mutations
                    if not await self.check_access_permissions(request, ['saleor:write']):
                        return web.json_response({
                            'error': 'Insufficient permissions for GraphQL mutations',
                            'code': 'GRAPHQL_WRITE_DENIED'
                        }, status=403)
                
                # Log GraphQL operations
                session = request.get('session')
                if session:
                    await self.auth_service.log_security_event(SecurityEvent(
                        event_type=SecurityEventType.LOGIN_SUCCESS,
                        user_id=session.user_id,
                        tenant_id=session.tenant_id,
                        ip_address=request.remote,
                        user_agent=request.headers.get('User-Agent', ''),
                        timestamp=datetime.utcnow(),
                        details={'action': 'graphql_query', 'query_type': 'mutation' if 'mutation' in query.lower() else 'query'},
                        risk_score=10 if 'mutation' in query.lower() else 0
                    ))
                
            except Exception as e:
                logger.warning(f"Failed to parse GraphQL request: {e}")
        
        # Proxy to Saleor GraphQL API
        return await self.proxy_to_saleor(request, f"{self.saleor_api_url.rstrip('/')}/graphql/")
    
    async def proxy_to_saleor(self, request, target_url: str):
        """Proxy request to Saleor service"""
        # Construct target URL
        path = request.path_qs
        if path.startswith('/saleor'):
            path = path[7:]  # Remove /saleor prefix
        
        url = urljoin(target_url.rstrip('/'), path.lstrip('/'))
        
        # Prepare headers
        headers = dict(request.headers)
        
        # Remove hop-by-hop headers
        hop_by_hop = [
            'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
            'te', 'trailers', 'transfer-encoding', 'upgrade'
        ]
        for header in hop_by_hop:
            headers.pop(header, None)
        
        # Add authentication context
        session = request.get('session')
        if session:
            headers['X-User-ID'] = session.user_id
            headers['X-Tenant-ID'] = session.tenant_id or ''
            headers['X-User-Role'] = session.role.value
            headers['X-User-Permissions'] = ','.join(session.permissions)
        
        api_key = request.get('api_key')
        if api_key:
            headers['X-API-Key-ID'] = api_key['key_id']
            headers['X-API-Key-Tenant'] = api_key.get('tenant_id', '')
        
        # Proxy the request
        try:
            async with ClientSession(timeout=ClientSession.timeout(total=30)) as session:
                if request.method == 'GET':
                    async with session.get(url, headers=headers) as resp:
                        content = await resp.read()
                        
                        # Create response
                        response = web.Response(
                            body=content,
                            status=resp.status,
                            headers=resp.headers
                        )
                        
                        # Add security headers
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        response.headers['X-Frame-Options'] = 'DENY'
                        response.headers['X-XSS-Protection'] = '1; mode=block'
                        
                        return response
                
                elif request.method == 'POST':
                    data = await request.read()
                    async with session.post(url, data=data, headers=headers) as resp:
                        content = await resp.read()
                        
                        response = web.Response(
                            body=content,
                            status=resp.status,
                            headers=resp.headers
                        )
                        
                        # Add security headers
                        response.headers['X-Content-Type-Options'] = 'nosniff'
                        response.headers['X-Frame-Options'] = 'DENY'
                        response.headers['X-XSS-Protection'] = '1; mode=block'
                        
                        return response
                
                else:
                    # Handle other HTTP methods
                    async with session.request(
                        request.method, url, 
                        data=await request.read(), 
                        headers=headers
                    ) as resp:
                        content = await resp.read()
                        return web.Response(
                            body=content,
                            status=resp.status,
                            headers=resp.headers
                        )
        
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            return web.json_response({
                'error': 'Saleor service unavailable',
                'code': 'SALEOR_UNAVAILABLE',
                'details': str(e)
            }, status=503)
    
    async def health_check(self, request):
        """Health check endpoint"""
        try:
            # Check Saleor connectivity
            async with ClientSession() as session:
                async with session.get(f"{self.saleor_api_url}/health/", timeout=10) as resp:
                    saleor_status = resp.status == 200
        except:
            saleor_status = False
        
        status_code = 200 if saleor_status else 503
        
        return web.json_response({
            'status': 'healthy' if saleor_status else 'degraded',
            'service': 'saleor-secure-proxy',
            'version': '1.0.0',
            'saleor_connectivity': saleor_status,
            'timestamp': datetime.utcnow().isoformat()
        }, status=status_code)

async def create_app(config: Dict[str, Any]) -> web.Application:
    """Create and configure the proxy application"""
    
    proxy = SecureSaleorProxy(config)
    await proxy.initialize()
    
    # Create application
    app = web.Application()
    
    # Configure CORS
    cors = aiohttp_cors.setup(app, defaults={
        origin: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        ) for origin in proxy.allowed_origins
    })
    
    # Add authentication middleware
    auth_middleware = AuthMiddleware(
        proxy.auth_service,
        protected_paths=['/saleor/', '/api/', '/graphql/', '/dashboard/']
    )
    app.middlewares.append(auth_middleware.middleware)
    
    # Health check (no auth required)
    app.router.add_get('/health', proxy.health_check)
    
    # Saleor dashboard routes (authentication required)
    app.router.add_route('*', '/saleor/dashboard/{path:.*}', proxy.handle_dashboard_request)
    app.router.add_route('*', '/dashboard/{path:.*}', proxy.handle_dashboard_request)
    
    # API routes (authentication required)
    app.router.add_route('*', '/saleor/api/{path:.*}', proxy.handle_api_request)
    app.router.add_route('*', '/api/{path:.*}', proxy.handle_api_request)
    
    # GraphQL routes (authentication required)
    app.router.add_route('*', '/saleor/graphql/{path:.*}', proxy.handle_graphql_request)
    app.router.add_route('*', '/graphql/{path:.*}', proxy.handle_graphql_request)
    
    # Default Saleor routes
    app.router.add_route('*', '/saleor/{path:.*}', proxy.handle_dashboard_request)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def main():
    """Main application entry point"""
    
    # Load configuration
    config = {
        'postgres_host': os.getenv('POSTGRES_HOST', 'host.docker.internal'),
        'postgres_port': int(os.getenv('POSTGRES_PORT', 5432)),
        'postgres_user': os.getenv('POSTGRES_USER', 'admin'),
        'postgres_password': os.getenv('POSTGRES_PASSWORD', 'securepassword'),
        'postgres_db': os.getenv('POSTGRES_DB', 'bizosaas'),
        'redis_host': os.getenv('REDIS_HOST', 'host.docker.internal'),
        'redis_port': int(os.getenv('REDIS_PORT', 6379)),
        'jwt_secret': os.getenv('JWT_SECRET', 'your-super-secret-jwt-key-here-change-in-production'),
        'saleor_api_url': os.getenv('SALEOR_API_URL', 'http://localhost:8024'),
        'saleor_dashboard_url': os.getenv('SALEOR_DASHBOARD_URL', 'http://localhost:9020'),
        'allowed_origins': os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001').split(','),
        'session_timeout': int(os.getenv('SESSION_TIMEOUT', 3600))
    }
    
    port = int(os.getenv('PROXY_PORT', 9021))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("🛡️  Starting Secure Saleor Dashboard Proxy...")
    print(f"🌐 Proxy server will be available at: http://{host}:{port}")
    print(f"🔗 Saleor API: {config['saleor_api_url']}")
    print(f"🔗 Saleor Dashboard: {config['saleor_dashboard_url']}")
    print("🔐 Security features enabled:")
    print("   - Authentication and authorization")
    print("   - Role-based access control")
    print("   - Rate limiting per user/action")
    print("   - GraphQL query analysis")
    print("   - Comprehensive audit logging")
    print("   - Security headers injection")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    app = await create_app(config)
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    print(f"✅ Secure Saleor Proxy started on port {port}")
    print("💡 Access points:")
    print(f"   Dashboard: http://{host}:{port}/saleor/dashboard/")
    print(f"   API:       http://{host}:{port}/saleor/api/")
    print(f"   GraphQL:   http://{host}:{port}/saleor/graphql/")
    print(f"   Health:    http://{host}:{port}/health")
    print("🛑 Press Ctrl+C to stop the proxy")
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Secure Saleor Proxy...")
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProxy stopped.")