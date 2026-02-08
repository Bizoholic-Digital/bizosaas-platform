#!/usr/bin/env python3
"""
Minimal Authentication Service - Compatible with existing database schema
"""

import asyncio
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from aiohttp import web
import aiohttp_cors
import asyncpg
import redis.asyncio as redis
import jwt
import hashlib
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MinimalAuthService:
    """Minimal authentication service that works with existing schema"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_pool = None
        self.redis_client = None
        self.jwt_secret = config.get('jwt_secret', 'default-secret')
        self.session_timeout = config.get('session_timeout', 3600)
    
    async def initialize(self):
        """Initialize service connections"""
        # PostgreSQL connection
        self.db_pool = await asyncpg.create_pool(
            host=self.config.get('postgres_host', 'localhost'),
            port=self.config.get('postgres_port', 5432),
            user=self.config.get('postgres_user', 'postgres'),
            password=self.config.get('postgres_password', ''),
            database=self.config.get('postgres_db', 'bizosaas'),
            min_size=2,
            max_size=10
        )
        
        # Redis connection
        self.redis_client = redis.Redis(
            host=self.config.get('redis_host', 'localhost'),
            port=self.config.get('redis_port', 6379),
            decode_responses=True
        )
        
        # Check existing schema
        await self.check_schema()
        logger.info("Authentication service initialized successfully")
    
    async def check_schema(self):
        """Check existing database schema"""
        async with self.db_pool.acquire() as conn:
            # Check if users table exists and its structure
            users_info = await conn.fetch("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            
            if users_info:
                logger.info(f"Found existing users table with {len(users_info)} columns")
                # Check if we need to add password-related columns
                existing_columns = {row['column_name'] for row in users_info}
                
                missing_auth_columns = {
                    'password_hash': 'VARCHAR(255)',
                    'salt': 'VARCHAR(255)',
                    'role': "VARCHAR(50) DEFAULT 'client'",
                    'failed_login_count': 'INTEGER DEFAULT 0',
                    'last_login_at': 'TIMESTAMP WITH TIME ZONE'
                }
                
                for col_name, col_def in missing_auth_columns.items():
                    if col_name not in existing_columns:
                        try:
                            await conn.execute(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_def}")
                            logger.info(f"Added column {col_name} to users table")
                        except Exception as e:
                            logger.warning(f"Could not add column {col_name}: {e}")
            else:
                logger.error("Users table not found!")
    
    async def hash_password(self, password: str) -> tuple[str, str]:
        """Hash password with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_hash.hex(), salt
    
    async def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash"""
        calculated_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return calculated_hash.hex() == stored_hash
    
    async def create_session(self, user_id: str, user_data: Dict[str, Any]) -> str:
        """Create user session"""
        session_id = secrets.token_urlsafe(32)
        session_data = {
            'user_id': str(user_id),
            'tenant_id': str(user_data.get('tenant_id', '')),
            'role': user_data.get('role', 'client'),
            'email': user_data.get('email', ''),
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(seconds=self.session_timeout)).isoformat()
        }
        
        # Store in Redis
        await self.redis_client.hmset(f"session:{session_id}", session_data)
        await self.redis_client.expire(f"session:{session_id}", self.session_timeout)
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        session_data = await self.redis_client.hgetall(f"session:{session_id}")
        
        if session_data and 'expires_at' in session_data:
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if expires_at > datetime.utcnow():
                return session_data
            else:
                # Session expired, clean up
                await self.redis_client.delete(f"session:{session_id}")
        
        return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user"""
        async with self.db_pool.acquire() as conn:
            # Get user data
            user = await conn.fetchrow("""
                SELECT id, email, password_hash, salt, role, tenant_id, is_active
                FROM users 
                WHERE email = $1 AND is_active = true
            """, email)
            
            if not user:
                logger.warning(f"User not found: {email}")
                return None
            
            # Check if user has password set
            if not user['password_hash'] or not user['salt']:
                logger.warning(f"User has no password set: {email}")
                return None
            
            # Verify password
            if await self.verify_password(password, user['password_hash'], user['salt']):
                # Update last login
                await conn.execute("""
                    UPDATE users 
                    SET last_login_at = NOW(), failed_login_count = 0 
                    WHERE id = $1
                """, user['id'])
                
                return dict(user)
            else:
                # Increment failed login count
                await conn.execute("""
                    UPDATE users 
                    SET failed_login_count = COALESCE(failed_login_count, 0) + 1 
                    WHERE id = $1
                """, user['id'])
                
                logger.warning(f"Invalid password for user: {email}")
                return None


# HTTP Handlers
async def health_check(request):
    """Health check endpoint"""
    return web.json_response({'status': 'healthy', 'service': 'BizOSaaS Auth'})


async def login(request):
    """User login endpoint"""
    try:
        data = await request.json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return web.json_response({
                'error': 'Email and password required'
            }, status=400)
        
        auth_service = request.app['auth_service']
        user = await auth_service.authenticate_user(email, password)
        
        if user:
            session_id = await auth_service.create_session(user['id'], user)
            
            response = web.json_response({
                'success': True,
                'user': {
                    'id': str(user['id']),
                    'email': user['email'],
                    'role': user['role'],
                    'tenant_id': str(user['tenant_id']) if user['tenant_id'] else None
                },
                'session_id': session_id
            })
            
            # Set session cookie
            response.set_cookie(
                'session_id', 
                session_id, 
                max_age=auth_service.session_timeout,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite='Lax'
            )
            
            return response
        else:
            return web.json_response({
                'error': 'Invalid credentials'
            }, status=401)
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return web.json_response({
            'error': 'Internal server error'
        }, status=500)


async def logout(request):
    """User logout endpoint"""
    session_id = request.cookies.get('session_id')
    if session_id:
        auth_service = request.app['auth_service']
        await auth_service.redis_client.delete(f"session:{session_id}")
    
    response = web.json_response({'success': True, 'message': 'Logged out'})
    response.del_cookie('session_id')
    return response


async def profile(request):
    """Get user profile - requires authentication"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        return web.json_response({'error': 'Authentication required'}, status=401)
    
    auth_service = request.app['auth_service']
    session = await auth_service.get_session(session_id)
    
    if not session:
        return web.json_response({'error': 'Invalid or expired session'}, status=401)
    
    return web.json_response({
        'user': {
            'id': session['user_id'],
            'email': session['email'],
            'role': session['role'],
            'tenant_id': session['tenant_id'] if session['tenant_id'] else None
        }
    })


async def create_app():
    """Create aiohttp application"""
    app = web.Application()
    
    # Configure CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_post('/api/auth/login', login)
    app.router.add_post('/api/auth/logout', logout)
    app.router.add_get('/api/auth/profile', profile)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        if hasattr(route, 'method') and route.method != '*':
            cors.add(route)
    
    return app


async def main():
    """Main application entry point"""
    # Load configuration
    config = {
        'postgres_host': os.getenv('POSTGRES_HOST', 'localhost'),
        'postgres_port': int(os.getenv('POSTGRES_PORT', 5432)),
        'postgres_user': os.getenv('POSTGRES_USER', 'postgres'),
        'postgres_password': os.getenv('POSTGRES_PASSWORD', ''),
        'postgres_db': os.getenv('POSTGRES_DB', 'bizosaas'),
        'redis_host': os.getenv('REDIS_HOST', 'localhost'),
        'redis_port': int(os.getenv('REDIS_PORT', 6379)),
        'jwt_secret': os.getenv('JWT_SECRET', 'default-secret'),
        'session_timeout': int(os.getenv('SESSION_TIMEOUT', 3600))
    }
    
    port = int(os.getenv('PORT', 8003))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("🚀 Starting BizOSaaS Minimal Authentication Service...")
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print("🔐 Features:")
    print("   - Compatible with existing integer-based schema")
    print("   - Session-based authentication")
    print("   - Redis session storage")
    print("   - Automatic schema compatibility checks")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Create and initialize auth service
    auth_service = MinimalAuthService(config)
    await auth_service.initialize()
    
    # Create application
    app = await create_app()
    app['auth_service'] = auth_service
    
    # Start server
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, host, port)
    await site.start()
    
    print(f"✅ BizOSaaS Authentication Service started on port {port}")
    print("💡 API Endpoints:")
    print(f"   POST http://{host}:{port}/api/auth/login")
    print(f"   POST http://{host}:{port}/api/auth/logout")
    print(f"   GET  http://{host}:{port}/api/auth/profile")
    print(f"   GET  http://{host}:{port}/health")
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