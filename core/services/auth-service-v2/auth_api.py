#!/usr/bin/env python3

"""
BizOSaaS Authentication API Server
Comprehensive authentication and authorization service for the platform
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from aiohttp import web, ClientSession
import aiohttp_cors
import aiohttp_session
from aiohttp_session.redis_storage import RedisStorage
import redis.asyncio as redis
from pydantic import BaseModel, EmailStr, ValidationError
import qrcode
import pyotp
import io
import base64

from auth_security import (
    AuthenticationService, AuthMiddleware, SaleorDashboardProxy,
    UserRole, SecurityEventType, SecurityEvent, PasswordPolicy
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API validation
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None
    tenant_id: Optional[str] = None
    role: str = "client"

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class MFASetupRequest(BaseModel):
    user_id: str

class MFAVerifyRequest(BaseModel):
    token: str
    backup_code: Optional[str] = None

class APIKeyCreateRequest(BaseModel):
    name: str
    tenant_id: Optional[str] = None
    permissions: List[str]
    expires_days: Optional[int] = None

class BizOSaaSAuthAPI:
    """Main authentication API service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth_service = AuthenticationService(config)
        self.saleor_proxy = None
        
        # Initialize Saleor proxy if configured
        saleor_url = config.get('saleor_api_url')
        if saleor_url:
            self.saleor_proxy = SaleorDashboardProxy(self.auth_service, saleor_url)
    
    async def initialize(self):
        """Initialize the service"""
        await self.auth_service.initialize()
        logger.info("Authentication service initialized")
    
    async def login(self, request):
        """User login endpoint"""
        try:
            data = await request.json()
            login_data = LoginRequest(**data)
            
            ip_address = request.remote
            user_agent = request.headers.get('User-Agent', '')
            
            # Authenticate user
            session = await self.auth_service.authenticate_user(
                login_data.email, 
                login_data.password, 
                ip_address, 
                user_agent
            )
            
            if not session:
                return web.json_response({
                    'error': 'Invalid credentials or account locked',
                    'code': 'AUTH_FAILED'
                }, status=401)
            
            # Generate JWT token
            user_data = {
                'id': session.user_id,
                'tenant_id': session.tenant_id,
                'role': session.role.value
            }
            jwt_token = await self.auth_service.generate_jwt_token(user_data)
            
            # Set session cookie
            response = web.json_response({
                'success': True,
                'user': {
                    'id': session.user_id,
                    'tenant_id': session.tenant_id,
                    'role': session.role.value,
                    'permissions': session.permissions,
                    'mfa_required': not session.mfa_verified
                },
                'token': jwt_token,
                'session_id': session.session_id
            })
            
            # Set secure session cookie
            max_age = 86400 if login_data.remember_me else None  # 24 hours or session
            response.set_cookie(
                'session_id',
                session.session_id,
                max_age=max_age,
                secure=True,
                httponly=True,
                samesite='Strict'
            )
            
            return response
            
        except ValidationError as e:
            return web.json_response({
                'error': 'Invalid request data',
                'details': e.errors()
            }, status=400)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return web.json_response({
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }, status=500)
    
    async def logout(self, request):
        """User logout endpoint"""
        session = request.get('session')
        if session:
            await self.auth_service.invalidate_session(session.session_id)
        
        response = web.json_response({'success': True})
        response.del_cookie('session_id')
        return response
    
    async def register(self, request):
        """User registration endpoint"""
        try:
            data = await request.json()
            register_data = RegisterRequest(**data)
            
            # Validate password
            is_valid, errors = PasswordPolicy.validate(register_data.password)
            if not is_valid:
                return web.json_response({
                    'error': 'Password does not meet policy requirements',
                    'details': errors
                }, status=400)
            
            # Hash password
            password_hash, salt = await self.auth_service.hash_password(register_data.password)
            
            # Create user
            async with self.auth_service.db_pool.acquire() as conn:
                # Check if user already exists
                existing_user = await conn.fetchrow(
                    "SELECT id FROM users WHERE email = $1", 
                    register_data.email
                )
                
                if existing_user:
                    return web.json_response({
                        'error': 'User with this email already exists',
                        'code': 'USER_EXISTS'
                    }, status=409)
                
                # Insert new user
                user_id = await conn.fetchval("""
                    INSERT INTO users (email, username, password_hash, salt, role, tenant_id)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                """, 
                register_data.email,
                register_data.username or register_data.email.split('@')[0],
                password_hash,
                salt,
                register_data.role,
                register_data.tenant_id
                )
            
            # Log security event
            ip_address = request.remote
            user_agent = request.headers.get('User-Agent', '')
            
            await self.auth_service.log_security_event(SecurityEvent(
                event_type=SecurityEventType.LOGIN_SUCCESS,
                user_id=str(user_id),
                tenant_id=register_data.tenant_id,
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.utcnow(),
                details={'action': 'registration'},
                risk_score=0
            ))
            
            return web.json_response({
                'success': True,
                'user_id': str(user_id),
                'message': 'User registered successfully'
            })
            
        except ValidationError as e:
            return web.json_response({
                'error': 'Invalid request data',
                'details': e.errors()
            }, status=400)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return web.json_response({
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }, status=500)
    
    async def change_password(self, request):
        """Change user password endpoint"""
        try:
            session = request.get('session')
            if not session:
                return web.json_response({
                    'error': 'Authentication required',
                    'code': 'AUTH_REQUIRED'
                }, status=401)
            
            data = await request.json()
            change_data = ChangePasswordRequest(**data)
            
            # Validate new password
            is_valid, errors = PasswordPolicy.validate(change_data.new_password)
            if not is_valid:
                return web.json_response({
                    'error': 'New password does not meet policy requirements',
                    'details': errors
                }, status=400)
            
            async with self.auth_service.db_pool.acquire() as conn:
                # Get current user data
                user = await conn.fetchrow(
                    "SELECT password_hash, salt FROM users WHERE id = $1",
                    session.user_id
                )
                
                if not user:
                    return web.json_response({
                        'error': 'User not found',
                        'code': 'USER_NOT_FOUND'
                    }, status=404)
                
                # Verify current password
                password_valid = await self.auth_service.verify_password(
                    change_data.current_password, 
                    user['password_hash'], 
                    user['salt']
                )
                
                if not password_valid:
                    return web.json_response({
                        'error': 'Current password is incorrect',
                        'code': 'INVALID_PASSWORD'
                    }, status=400)
                
                # Hash new password
                new_password_hash, new_salt = await self.auth_service.hash_password(
                    change_data.new_password
                )
                
                # Update password
                await conn.execute("""
                    UPDATE users 
                    SET password_hash = $1, salt = $2, password_changed_at = NOW()
                    WHERE id = $3
                """, new_password_hash, new_salt, session.user_id)
                
                # Add to password history
                await conn.execute("""
                    INSERT INTO password_history (user_id, password_hash)
                    VALUES ($1, $2)
                """, session.user_id, new_password_hash)
            
            # Log security event
            await self.auth_service.log_security_event(SecurityEvent(
                event_type=SecurityEventType.PASSWORD_CHANGED,
                user_id=session.user_id,
                tenant_id=session.tenant_id,
                ip_address=session.ip_address,
                user_agent=request.headers.get('User-Agent', ''),
                timestamp=datetime.utcnow(),
                details={},
                risk_score=0
            ))
            
            return web.json_response({'success': True})
            
        except ValidationError as e:
            return web.json_response({
                'error': 'Invalid request data',
                'details': e.errors()
            }, status=400)
        except Exception as e:
            logger.error(f"Password change error: {e}")
            return web.json_response({
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }, status=500)
    
    async def setup_mfa(self, request):
        """Setup multi-factor authentication"""
        try:
            session = request.get('session')
            if not session:
                return web.json_response({
                    'error': 'Authentication required',
                    'code': 'AUTH_REQUIRED'
                }, status=401)
            
            # Generate MFA secret
            secret = pyotp.random_base32()
            
            # Create TOTP URL for QR code
            async with self.auth_service.db_pool.acquire() as conn:
                user = await conn.fetchrow(
                    "SELECT email FROM users WHERE id = $1",
                    session.user_id
                )
                
                if not user:
                    return web.json_response({
                        'error': 'User not found',
                        'code': 'USER_NOT_FOUND'
                    }, status=404)
                
                totp_url = pyotp.totp.TOTP(secret).provisioning_uri(
                    name=user['email'],
                    issuer_name="BizOSaaS Platform"
                )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(totp_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            qr_code_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            # Store temporary secret (not activated until verified)
            self.auth_service.redis_client.setex(
                f"mfa_setup:{session.user_id}", 
                300,  # 5 minutes
                secret
            )
            
            return web.json_response({
                'success': True,
                'secret': secret,
                'qr_code': f"data:image/png;base64,{qr_code_base64}",
                'manual_entry_key': secret,
                'instructions': "Scan the QR code with your authenticator app or enter the manual key"
            })
            
        except Exception as e:
            logger.error(f"MFA setup error: {e}")
            return web.json_response({
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }, status=500)
    
    async def verify_mfa_setup(self, request):
        """Verify MFA setup with token"""
        try:
            session = request.get('session')
            if not session:
                return web.json_response({
                    'error': 'Authentication required',
                    'code': 'AUTH_REQUIRED'
                }, status=401)
            
            data = await request.json()
            verify_data = MFAVerifyRequest(**data)
            
            # Get temporary secret
            secret = self.auth_service.redis_client.get(f"mfa_setup:{session.user_id}")
            if not secret:
                return web.json_response({
                    'error': 'MFA setup session expired',
                    'code': 'MFA_SETUP_EXPIRED'
                }, status=400)
            
            # Verify token
            totp = pyotp.TOTP(secret)
            if not totp.verify(verify_data.token):
                return web.json_response({
                    'error': 'Invalid MFA token',
                    'code': 'INVALID_MFA_TOKEN'
                }, status=400)
            
            # Activate MFA for user
            async with self.auth_service.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE users 
                    SET mfa_enabled = true, mfa_secret = $1
                    WHERE id = $2
                """, secret, session.user_id)
            
            # Clean up temporary secret
            self.auth_service.redis_client.delete(f"mfa_setup:{session.user_id}")
            
            # Log security event
            await self.auth_service.log_security_event(SecurityEvent(
                event_type=SecurityEventType.MFA_ENABLED,
                user_id=session.user_id,
                tenant_id=session.tenant_id,
                ip_address=session.ip_address,
                user_agent=request.headers.get('User-Agent', ''),
                timestamp=datetime.utcnow(),
                details={},
                risk_score=0
            ))
            
            return web.json_response({
                'success': True,
                'message': 'MFA enabled successfully'
            })
            
        except ValidationError as e:
            return web.json_response({
                'error': 'Invalid request data',
                'details': e.errors()
            }, status=400)
        except Exception as e:
            logger.error(f"MFA verification error: {e}")
            return web.json_response({
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }, status=500)
    
    async def create_api_key(self, request):
        """Create API key for service-to-service authentication"""
        try:
            session = request.get('session')
            if not session:
                return web.json_response({
                    'error': 'Authentication required',
                    'code': 'AUTH_REQUIRED'
                }, status=401)
            
            # Check permissions
            if session.role not in [UserRole.SUPER_ADMIN, UserRole.TENANT_ADMIN]:
                return web.json_response({
                    'error': 'Insufficient permissions',
                    'code': 'PERMISSION_DENIED'
                }, status=403)
            
            data = await request.json()
            api_key_data = APIKeyCreateRequest(**data)
            
            key_id, secret = await self.auth_service.create_api_key(
                api_key_data.name,
                api_key_data.tenant_id or session.tenant_id,
                api_key_data.permissions
            )
            
            return web.json_response({
                'success': True,
                'key_id': key_id,
                'secret': secret,
                'warning': 'Store the secret securely. It will not be shown again.'
            })
            
        except ValidationError as e:
            return web.json_response({
                'error': 'Invalid request data',
                'details': e.errors()
            }, status=400)
        except Exception as e:
            logger.error(f"API key creation error: {e}")
            return web.json_response({
                'error': 'Internal server error',
                'code': 'INTERNAL_ERROR'
            }, status=500)
    
    async def get_user_profile(self, request):
        """Get current user profile"""
        session = request.get('session')
        if not session:
            return web.json_response({
                'error': 'Authentication required',
                'code': 'AUTH_REQUIRED'
            }, status=401)
        
        async with self.auth_service.db_pool.acquire() as conn:
            user = await conn.fetchrow("""
                SELECT id, email, username, role, is_active, mfa_enabled, 
                       last_login_at, created_at, metadata
                FROM users WHERE id = $1
            """, session.user_id)
            
            if not user:
                return web.json_response({
                    'error': 'User not found',
                    'code': 'USER_NOT_FOUND'
                }, status=404)
        
        return web.json_response({
            'success': True,
            'user': {
                'id': str(user['id']),
                'email': user['email'],
                'username': user['username'],
                'role': user['role'],
                'is_active': user['is_active'],
                'mfa_enabled': user['mfa_enabled'],
                'last_login_at': user['last_login_at'].isoformat() if user['last_login_at'] else None,
                'created_at': user['created_at'].isoformat(),
                'metadata': user['metadata'] or {}
            }
        })
    
    async def get_security_events(self, request):
        """Get security events for user"""
        session = request.get('session')
        if not session:
            return web.json_response({
                'error': 'Authentication required',
                'code': 'AUTH_REQUIRED'
            }, status=401)
        
        # Parse query parameters
        limit = int(request.query.get('limit', 50))
        offset = int(request.query.get('offset', 0))
        
        async with self.auth_service.db_pool.acquire() as conn:
            events = await conn.fetch("""
                SELECT event_type, ip_address, event_data, risk_score, created_at
                FROM security_events 
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
            """, session.user_id, limit, offset)
        
        return web.json_response({
            'success': True,
            'events': [
                {
                    'event_type': event['event_type'],
                    'ip_address': event['ip_address'],
                    'details': json.loads(event['event_data']),
                    'risk_score': event['risk_score'],
                    'timestamp': event['created_at'].isoformat()
                }
                for event in events
            ]
        })
    
    async def health_check(self, request):
        """Health check endpoint"""
        try:
            # Test database connection
            async with self.auth_service.db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
            
            # Test Redis connection
            self.auth_service.redis_client.ping()
            
            return web.json_response({
                'status': 'healthy',
                'service': 'bizosaas-auth-service',
                'version': '2.0.0',
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return web.json_response({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }, status=503)
    
    async def saleor_dashboard_access(self, request):
        """Protected access to Saleor dashboard"""
        if not self.saleor_proxy:
            return web.json_response({
                'error': 'Saleor dashboard not configured',
                'code': 'SALEOR_NOT_CONFIGURED'
            }, status=503)
        
        return await self.saleor_proxy.proxy_request(request)

async def create_app(config: Dict[str, Any]) -> web.Application:
    """Create and configure the web application"""
    
    # Initialize authentication service
    auth_api = BizOSaaSAuthAPI(config)
    await auth_api.initialize()
    
    # Create application
    app = web.Application()
    
    # Configure Redis session storage (async)
    redis_client = redis.Redis.from_url(
        f"redis://{config.get('redis_host', 'localhost')}:{config.get('redis_port', 6379)}"
    )
    
    aiohttp_session.setup(
        app, 
        RedisStorage(redis_client, max_age=86400)  # 24 hours
    )
    
    # Configure CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add middleware
    auth_middleware = AuthMiddleware(
        auth_api.auth_service,
        protected_paths=['/api/', '/dashboard/', '/saleor/']
    )
    app.middlewares.append(auth_middleware.middleware)
    
    # Public routes (no authentication required)
    app.router.add_post('/api/auth/login', auth_api.login)
    app.router.add_post('/api/auth/register', auth_api.register)
    app.router.add_get('/health', auth_api.health_check)
    
    # Protected routes (authentication required)
    app.router.add_post('/api/auth/logout', auth_api.logout)
    app.router.add_post('/api/auth/change-password', auth_api.change_password)
    app.router.add_post('/api/auth/mfa/setup', auth_api.setup_mfa)
    app.router.add_post('/api/auth/mfa/verify', auth_api.verify_mfa_setup)
    app.router.add_post('/api/auth/api-keys', auth_api.create_api_key)
    app.router.add_get('/api/auth/profile', auth_api.get_user_profile)
    app.router.add_get('/api/auth/security-events', auth_api.get_security_events)
    
    # Add CORS to specific routes (exclude wildcard routes to avoid conflicts)
    for route in list(app.router.routes()):
        # Skip wildcard routes that will conflict with CORS preflight handlers
        if hasattr(route, 'method') and route.method != '*':
            cors.add(route)
    
    # Saleor dashboard proxy routes (added after CORS to avoid conflicts)
    app.router.add_route('*', '/saleor/{path:.*}', auth_api.saleor_dashboard_access)
    app.router.add_route('*', '/dashboard/saleor/{path:.*}', auth_api.saleor_dashboard_access)
    
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
        'encryption_key': os.getenv('ENCRYPTION_KEY', 'your-32-byte-base64-encoded-key'),
        'saleor_api_url': os.getenv('SALEOR_API_URL', 'http://localhost:8024'),
        'session_timeout': int(os.getenv('SESSION_TIMEOUT', 3600)),
        'max_login_attempts': int(os.getenv('MAX_LOGIN_ATTEMPTS', 5)),
        'lockout_duration': int(os.getenv('LOCKOUT_DURATION', 900))
    }
    
    port = int(os.getenv('PORT', 8003))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("🚀 Starting BizOSaaS Authentication Service...")
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print("🔐 Security features enabled:")
    print("   - Multi-factor authentication (TOTP)")
    print("   - Role-based access control (RBAC)")
    print("   - Password policy enforcement")
    print("   - Rate limiting and brute force protection")
    print("   - Session hijacking prevention")
    print("   - Comprehensive audit logging")
    print("   - Saleor dashboard proxy with authentication")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    app = await create_app(config)
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    print(f"✅ BizOSaaS Authentication Service started on port {port}")
    print("💡 API Endpoints:")
    print(f"   POST http://{host}:{port}/api/auth/login")
    print(f"   POST http://{host}:{port}/api/auth/register")
    print(f"   GET  http://{host}:{port}/health")
    print(f"   Saleor Dashboard: http://{host}:{port}/saleor/")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down BizOSaaS Authentication Service...")
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")