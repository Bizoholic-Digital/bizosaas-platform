#!/usr/bin/env python3

"""
Comprehensive Authentication and Access Control System
Enterprise-grade security for BizOSaaS platform with Saleor dashboard protection
"""

import asyncio
import base64
import hashlib
import secrets
import time
import logging
import jwt
import bcrypt
import redis
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
from aiohttp import web
from aiohttp.web_middlewares import middleware
import aiohttp_cors
import aiohttp_session
from aiohttp_session.redis_storage import RedisStorage
from cryptography.fernet import Fernet
from pydantic import BaseModel, EmailStr
import asyncpg
import json
import re
from functools import wraps
import ipaddress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserRole(Enum):
    """User role definitions with hierarchical permissions"""
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    MANAGER = "manager"
    STAFF = "staff"
    CLIENT = "client"

class SecurityEventType(Enum):
    """Security event types for audit logging"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILED = "login_failed"
    LOGIN_BLOCKED = "login_blocked"
    PASSWORD_CHANGED = "password_changed"
    ROLE_CHANGED = "role_changed"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SESSION_HIJACK_ATTEMPT = "session_hijack_attempt"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"

@dataclass
class SecurityEvent:
    """Security event data structure"""
    event_type: SecurityEventType
    user_id: Optional[str]
    tenant_id: Optional[str]
    ip_address: str
    user_agent: str
    timestamp: datetime
    details: Dict[str, Any]
    risk_score: int = 0

@dataclass
class UserSession:
    """User session data structure"""
    session_id: str
    user_id: str
    tenant_id: Optional[str]
    role: UserRole
    permissions: List[str]
    ip_address: str
    user_agent: str
    created_at: datetime
    last_activity: datetime
    expires_at: datetime
    mfa_verified: bool = False
    device_fingerprint: Optional[str] = None

@dataclass
class LoginAttempt:
    """Login attempt tracking"""
    ip_address: str
    user_id: Optional[str]
    timestamp: datetime
    success: bool
    risk_score: int

class PasswordPolicy:
    """Password security policy implementation"""
    
    MIN_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL = True
    MAX_AGE_DAYS = 90
    HISTORY_COUNT = 12
    
    @classmethod
    def validate(cls, password: str) -> Tuple[bool, List[str]]:
        """Validate password against policy"""
        errors = []
        
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must be at least {cls.MIN_LENGTH} characters long")
        
        if cls.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if cls.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if cls.REQUIRE_DIGITS and not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if cls.REQUIRE_SPECIAL and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    @classmethod
    def calculate_strength(cls, password: str) -> int:
        """Calculate password strength score (0-100)"""
        score = 0
        
        # Length bonus
        score += min(len(password) * 2, 30)
        
        # Character variety bonus
        if re.search(r'[a-z]', password): score += 10
        if re.search(r'[A-Z]', password): score += 10
        if re.search(r'\d', password): score += 10
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 10
        
        # Pattern penalties
        if re.search(r'(.)\1{2,}', password): score -= 10  # Repeated characters
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password): score -= 10  # Sequential numbers
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()): score -= 10  # Sequential letters
        
        # Common patterns
        common_patterns = ['password', '123456', 'qwerty', 'admin', 'user']
        for pattern in common_patterns:
            if pattern.lower() in password.lower():
                score -= 20
        
        return max(0, min(100, score))

class AuthenticationService:
    """Comprehensive authentication service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.redis_client = None
        self.db_pool = None
        # Generate or use provided Fernet key (must be 32 url-safe base64-encoded bytes)
        encryption_key = config.get('encryption_key')
        if not encryption_key:
            encryption_key = Fernet.generate_key()
        elif isinstance(encryption_key, str):
            # If it's a string, encode it properly for Fernet
            encryption_key = encryption_key.encode()[:32].ljust(32, b'0')
            encryption_key = base64.urlsafe_b64encode(encryption_key)
        self.cipher_suite = Fernet(encryption_key)
        self.jwt_secret = config.get('jwt_secret', secrets.token_urlsafe(32))
        self.session_timeout = config.get('session_timeout', 3600)  # 1 hour
        self.max_login_attempts = config.get('max_login_attempts', 5)
        self.lockout_duration = config.get('lockout_duration', 900)  # 15 minutes
        self.rate_limits = {
            'login': (5, 300),  # 5 attempts per 5 minutes
            'api': (100, 60),   # 100 requests per minute
            'password_reset': (3, 3600)  # 3 attempts per hour
        }
    
    async def initialize(self):
        """Initialize service connections"""
        # Redis connection for session storage
        self.redis_client = redis.Redis(
            host=self.config.get('redis_host', 'localhost'),
            port=self.config.get('redis_port', 6379),
            decode_responses=True
        )
        
        # PostgreSQL connection for user data
        self.db_pool = await asyncpg.create_pool(
            host=self.config.get('postgres_host', 'localhost'),
            port=self.config.get('postgres_port', 5432),
            user=self.config.get('postgres_user', 'admin'),
            password=self.config.get('postgres_password', 'securepassword'),
            database=self.config.get('postgres_db', 'bizosaas'),
            min_size=5,
            max_size=20
        )
        
        # Create database schema
        await self.create_schema()
    
    async def create_schema(self):
        """Create database schema for authentication - Compatible with existing integer-based schema"""
        async with self.db_pool.acquire() as conn:
            # First, check if core tables already exist and their schema
            existing_tables = await conn.fetch("""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name IN ('users', 'tenants', 'user_sessions')
                ORDER BY table_name, ordinal_position
            """)
            
            # Check if users table exists and what type the id column is
            users_id_type = None
            tenants_id_type = None
            
            for row in existing_tables:
                if row['table_name'] == 'users' and row['column_name'] == 'id':
                    users_id_type = row['data_type']
                elif row['table_name'] == 'tenants' and row['column_name'] == 'id':
                    tenants_id_type = row['data_type']
            
            logger.info(f"Detected schema: users.id={users_id_type}, tenants.id={tenants_id_type}")
            
            # Determine the correct data types based on existing schema
            if users_id_type == 'integer':
                id_type = 'SERIAL PRIMARY KEY'
                ref_type = 'INTEGER'
                tenant_ref = 'INTEGER REFERENCES tenants(id)' if tenants_id_type == 'integer' else 'INTEGER'
                user_ref = 'INTEGER REFERENCES users(id)'
            else:
                id_type = 'UUID PRIMARY KEY DEFAULT gen_random_uuid()'
                ref_type = 'UUID'
                tenant_ref = 'UUID REFERENCES tenants(id)'
                user_ref = 'UUID REFERENCES users(id)'
            
            # Only add missing columns to existing users table if needed
            if users_id_type:  # users table exists
                logger.info("Users table exists, checking for missing auth columns...")
                
                # Add missing columns to existing users table
                missing_columns = [
                    ('password_hash', 'VARCHAR(255)'),
                    ('salt', 'VARCHAR(255)'),
                    ('role', "VARCHAR(50) DEFAULT 'client'"),
                    ('is_verified', 'BOOLEAN DEFAULT false'),
                    ('mfa_enabled', 'BOOLEAN DEFAULT false'),
                    ('mfa_secret', 'VARCHAR(255)'),
                    ('password_changed_at', 'TIMESTAMP WITH TIME ZONE DEFAULT NOW()'),
                    ('last_login_at', 'TIMESTAMP WITH TIME ZONE'),
                    ('failed_login_count', 'INTEGER DEFAULT 0'),
                    ('locked_until', 'TIMESTAMP WITH TIME ZONE'),
                    ('metadata', "JSONB DEFAULT '{}'::jsonb")
                ]
                
                for col_name, col_def in missing_columns:
                    try:
                        await conn.execute(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_def}")
                        logger.info(f"Added column {col_name} to users table")
                    except Exception as e:
                        logger.warning(f"Could not add column {col_name}: {e}")
            
            # Create additional auth tables with compatible schema
            schema_sql = f"""
            -- Password history for policy enforcement
            CREATE TABLE IF NOT EXISTS password_history (
                id {id_type},
                user_id {user_ref} ON DELETE CASCADE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            -- Security events audit log
            CREATE TABLE IF NOT EXISTS security_events (
                id {id_type},
                event_type VARCHAR(50) NOT NULL,
                user_id {ref_type},
                tenant_id {ref_type},
                ip_address INET NOT NULL,
                user_agent TEXT,
                event_data JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                risk_score INTEGER DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            -- Rate limiting table
            CREATE TABLE IF NOT EXISTS rate_limits (
                id {id_type},
                identifier VARCHAR(255) NOT NULL, -- IP or user_id
                action VARCHAR(50) NOT NULL,
                count INTEGER DEFAULT 1,
                window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                UNIQUE(identifier, action, window_start)
            );
            
            -- API keys for service-to-service communication
            CREATE TABLE IF NOT EXISTS api_keys (
                id {id_type},
                key_id VARCHAR(255) UNIQUE NOT NULL,
                key_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                tenant_id {ref_type},
                permissions JSONB NOT NULL DEFAULT '[]'::jsonb,
                is_active BOOLEAN DEFAULT true,
                expires_at TIMESTAMP WITH TIME ZONE,
                last_used_at TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            -- Create indexes for performance
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_users_tenant ON users(tenant_id);
            CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);
            CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);
            CREATE INDEX IF NOT EXISTS idx_security_events_user ON security_events(user_id);
            CREATE INDEX IF NOT EXISTS idx_security_events_created ON security_events(created_at);
            CREATE INDEX IF NOT EXISTS idx_rate_limits_identifier ON rate_limits(identifier, action);
            
            -- Add foreign key constraints for security_events if using integers
            """ + (f"""
            DO $$
            BEGIN
                -- Add foreign keys only if they don't exist
                IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'security_events_user_id_fkey') THEN
                    ALTER TABLE security_events ADD CONSTRAINT security_events_user_id_fkey 
                        FOREIGN KEY (user_id) REFERENCES users(id);
                END IF;
                
                IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'security_events_tenant_id_fkey') THEN
                    ALTER TABLE security_events ADD CONSTRAINT security_events_tenant_id_fkey 
                        FOREIGN KEY (tenant_id) REFERENCES tenants(id);
                END IF;
                
                IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'api_keys_tenant_id_fkey') THEN
                    ALTER TABLE api_keys ADD CONSTRAINT api_keys_tenant_id_fkey 
                        FOREIGN KEY (tenant_id) REFERENCES tenants(id);
                END IF;
            END $$;
            """ if users_id_type == 'integer' else """")
            
            try:
                await conn.execute(schema_sql)
                logger.info("Auth schema created/updated successfully")
            except Exception as e:
                logger.error(f"Schema creation failed: {e}")
                # Continue anyway - the service can work with existing tables
    
    async def hash_password(self, password: str) -> Tuple[str, str]:
        """Hash password with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return password_hash.hex(), salt
    
    async def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        calculated_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return calculated_hash.hex() == password_hash
    
    async def generate_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': str(user_data['id']),
            'tenant_id': str(user_data.get('tenant_id')),
            'role': user_data['role'],
            'exp': datetime.utcnow() + timedelta(seconds=self.session_timeout),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    async def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
    
    async def check_rate_limit(self, identifier: str, action: str) -> Tuple[bool, int]:
        """Check if action is rate limited"""
        if action not in self.rate_limits:
            return True, 0
        
        limit, window = self.rate_limits[action]
        
        # Use Redis for real-time rate limiting
        key = f"rate_limit:{identifier}:{action}"
        current_time = int(time.time())
        window_start = current_time - (current_time % window)
        
        pipe = self.redis_client.pipeline()
        pipe.zremrangebyscore(key, 0, current_time - window)
        pipe.zcard(key)
        pipe.zadd(key, {str(current_time): current_time})
        pipe.expire(key, window)
        results = pipe.execute()
        
        current_count = results[1]
        
        if current_count >= limit:
            return False, limit - current_count
        
        return True, limit - current_count
    
    async def log_security_event(self, event: SecurityEvent):
        """Log security event to database"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO security_events 
                (event_type, user_id, tenant_id, ip_address, user_agent, event_data, risk_score)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, 
            event.event_type.value,
            event.user_id,
            event.tenant_id,
            event.ip_address,
            event.user_agent,
            json.dumps(event.details),
            event.risk_score
            )
    
    async def authenticate_user(self, email: str, password: str, ip_address: str, user_agent: str) -> Optional[UserSession]:
        """Authenticate user and create session"""
        
        # Check rate limiting
        allowed, remaining = await self.check_rate_limit(ip_address, 'login')
        if not allowed:
            await self.log_security_event(SecurityEvent(
                event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
                user_id=None,
                tenant_id=None,
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.utcnow(),
                details={'action': 'login'},
                risk_score=30
            ))
            return None
        
        async with self.db_pool.acquire() as conn:
            # Get user data
            user = await conn.fetchrow("""
                SELECT * FROM users WHERE email = $1 AND is_active = true
            """, email)
            
            if not user:
                await self.log_security_event(SecurityEvent(
                    event_type=SecurityEventType.LOGIN_FAILED,
                    user_id=None,
                    tenant_id=None,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    timestamp=datetime.utcnow(),
                    details={'reason': 'user_not_found', 'email': email},
                    risk_score=20
                ))
                return None
            
            # Check if account is locked
            if user['locked_until'] and user['locked_until'] > datetime.utcnow():
                await self.log_security_event(SecurityEvent(
                    event_type=SecurityEventType.LOGIN_BLOCKED,
                    user_id=str(user['id']),
                    tenant_id=str(user.get('tenant_id')),
                    ip_address=ip_address,
                    user_agent=user_agent,
                    timestamp=datetime.utcnow(),
                    details={'reason': 'account_locked'},
                    risk_score=50
                ))
                return None
            
            # Verify password
            password_valid = await self.verify_password(password, user['password_hash'], user['salt'])
            
            if not password_valid:
                # Increment failed login count
                failed_count = user['failed_login_count'] + 1
                locked_until = None
                
                if failed_count >= self.max_login_attempts:
                    locked_until = datetime.utcnow() + timedelta(seconds=self.lockout_duration)
                
                await conn.execute("""
                    UPDATE users 
                    SET failed_login_count = $1, locked_until = $2 
                    WHERE id = $3
                """, failed_count, locked_until, user['id'])
                
                await self.log_security_event(SecurityEvent(
                    event_type=SecurityEventType.LOGIN_FAILED,
                    user_id=str(user['id']),
                    tenant_id=str(user.get('tenant_id')),
                    ip_address=ip_address,
                    user_agent=user_agent,
                    timestamp=datetime.utcnow(),
                    details={'reason': 'invalid_password', 'failed_count': failed_count},
                    risk_score=25
                ))
                return None
            
            # Reset failed login count on successful authentication
            await conn.execute("""
                UPDATE users 
                SET failed_login_count = 0, locked_until = NULL, last_login_at = NOW()
                WHERE id = $1
            """, user['id'])
            
            # Create session
            session = await self.create_user_session(user, ip_address, user_agent)
            
            await self.log_security_event(SecurityEvent(
                event_type=SecurityEventType.LOGIN_SUCCESS,
                user_id=str(user['id']),
                tenant_id=str(user.get('tenant_id')),
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.utcnow(),
                details={'session_id': session.session_id},
                risk_score=0
            ))
            
            return session
    
    async def create_user_session(self, user: Dict[str, Any], ip_address: str, user_agent: str) -> UserSession:
        """Create a new user session"""
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(seconds=self.session_timeout)
        
        # Get user permissions based on role
        permissions = await self.get_role_permissions(UserRole(user['role']))
        
        session = UserSession(
            session_id=session_id,
            user_id=str(user['id']),
            tenant_id=str(user.get('tenant_id')) if user.get('tenant_id') else None,
            role=UserRole(user['role']),
            permissions=permissions,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            expires_at=expires_at,
            mfa_verified=not user['mfa_enabled']  # If MFA not enabled, consider verified
        )
        
        # Store session in database
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_sessions 
                (session_id, user_id, tenant_id, ip_address, user_agent, expires_at, mfa_verified)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            """, 
            session.session_id, session.user_id, session.tenant_id,
            session.ip_address, session.user_agent, session.expires_at, session.mfa_verified
            )
        
        # Store session in Redis for fast access
        await self.store_session_redis(session)
        
        return session
    
    async def store_session_redis(self, session: UserSession):
        """Store session in Redis"""
        session_data = {
            'user_id': session.user_id,
            'tenant_id': session.tenant_id,
            'role': session.role.value,
            'permissions': session.permissions,
            'ip_address': session.ip_address,
            'created_at': session.created_at.isoformat(),
            'last_activity': session.last_activity.isoformat(),
            'expires_at': session.expires_at.isoformat(),
            'mfa_verified': session.mfa_verified
        }
        
        # Set session with expiration
        self.redis_client.hset(f"session:{session.session_id}", mapping=session_data)
        self.redis_client.expire(f"session:{session.session_id}", self.session_timeout)
    
    async def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get session by ID"""
        # Try Redis first for performance
        session_data = self.redis_client.hgetall(f"session:{session_id}")
        
        if session_data:
            return UserSession(
                session_id=session_id,
                user_id=session_data['user_id'],
                tenant_id=session_data.get('tenant_id'),
                role=UserRole(session_data['role']),
                permissions=json.loads(session_data['permissions']) if isinstance(session_data['permissions'], str) else session_data['permissions'],
                ip_address=session_data['ip_address'],
                user_agent=session_data.get('user_agent', ''),
                created_at=datetime.fromisoformat(session_data['created_at']),
                last_activity=datetime.fromisoformat(session_data['last_activity']),
                expires_at=datetime.fromisoformat(session_data['expires_at']),
                mfa_verified=session_data.get('mfa_verified', False)
            )
        
        # Fallback to database
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT s.*, u.role FROM user_sessions s 
                JOIN users u ON s.user_id = u.id 
                WHERE s.session_id = $1 AND s.is_active = true AND s.expires_at > NOW()
            """, session_id)
            
            if row:
                permissions = await self.get_role_permissions(UserRole(row['role']))
                return UserSession(
                    session_id=session_id,
                    user_id=str(row['user_id']),
                    tenant_id=str(row['tenant_id']) if row['tenant_id'] else None,
                    role=UserRole(row['role']),
                    permissions=permissions,
                    ip_address=row['ip_address'],
                    user_agent=row['user_agent'] or '',
                    created_at=row['created_at'],
                    last_activity=row['last_activity'],
                    expires_at=row['expires_at'],
                    mfa_verified=row['mfa_verified']
                )
        
        return None
    
    async def get_role_permissions(self, role: UserRole) -> List[str]:
        """Get permissions for a role"""
        role_permissions = {
            UserRole.SUPER_ADMIN: [
                'admin:*', 'tenant:*', 'user:*', 'saleor:*', 'system:*'
            ],
            UserRole.TENANT_ADMIN: [
                'tenant:read', 'tenant:write', 'user:read', 'user:write',
                'saleor:read', 'saleor:write', 'dashboard:access'
            ],
            UserRole.MANAGER: [
                'tenant:read', 'user:read', 'saleor:read', 'saleor:manage_products',
                'saleor:manage_orders', 'dashboard:access'
            ],
            UserRole.STAFF: [
                'tenant:read', 'saleor:read', 'dashboard:limited'
            ],
            UserRole.CLIENT: [
                'tenant:read_own', 'dashboard:client'
            ]
        }
        
        return role_permissions.get(role, [])
    
    async def validate_session(self, session_id: str, ip_address: str, user_agent: str) -> Optional[UserSession]:
        """Validate session and check for suspicious activity"""
        session = await self.get_session(session_id)
        
        if not session:
            return None
        
        # Check if session expired
        if session.expires_at < datetime.utcnow():
            await self.invalidate_session(session_id)
            return None
        
        # Check for session hijacking attempts
        if session.ip_address != ip_address:
            await self.log_security_event(SecurityEvent(
                event_type=SecurityEventType.SESSION_HIJACK_ATTEMPT,
                user_id=session.user_id,
                tenant_id=session.tenant_id,
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.utcnow(),
                details={
                    'original_ip': session.ip_address,
                    'new_ip': ip_address,
                    'session_id': session_id
                },
                risk_score=80
            ))
            await self.invalidate_session(session_id)
            return None
        
        # Update last activity
        session.last_activity = datetime.utcnow()
        await self.update_session_activity(session)
        
        return session
    
    async def update_session_activity(self, session: UserSession):
        """Update session last activity"""
        # Update Redis
        self.redis_client.hset(f"session:{session.session_id}", 
                              'last_activity', session.last_activity.isoformat())
        
        # Update database
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE user_sessions SET last_activity = $1 WHERE session_id = $2
            """, session.last_activity, session.session_id)
    
    async def invalidate_session(self, session_id: str):
        """Invalidate a session"""
        # Remove from Redis
        self.redis_client.delete(f"session:{session_id}")
        
        # Mark as inactive in database
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE user_sessions SET is_active = false WHERE session_id = $1
            """, session_id)
    
    async def create_api_key(self, name: str, tenant_id: Optional[str], permissions: List[str]) -> Tuple[str, str]:
        """Create API key for service-to-service authentication"""
        key_id = f"bizo_{secrets.token_urlsafe(16)}"
        secret = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(f"{key_id}:{secret}".encode()).hexdigest()
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO api_keys (key_id, key_hash, name, tenant_id, permissions)
                VALUES ($1, $2, $3, $4, $5)
            """, key_id, key_hash, name, tenant_id, json.dumps(permissions))
        
        return key_id, secret
    
    async def validate_api_key(self, key_id: str, secret: str) -> Optional[Dict[str, Any]]:
        """Validate API key"""
        key_hash = hashlib.sha256(f"{key_id}:{secret}".encode()).hexdigest()
        
        async with self.db_pool.acquire() as conn:
            key_data = await conn.fetchrow("""
                SELECT * FROM api_keys 
                WHERE key_id = $1 AND key_hash = $2 AND is_active = true
                AND (expires_at IS NULL OR expires_at > NOW())
            """, key_id, key_hash)
            
            if key_data:
                # Update last used timestamp
                await conn.execute("""
                    UPDATE api_keys SET last_used_at = NOW() WHERE id = $1
                """, key_data['id'])
                
                return {
                    'key_id': key_data['key_id'],
                    'name': key_data['name'],
                    'tenant_id': key_data['tenant_id'],
                    'permissions': json.loads(key_data['permissions'])
                }
        
        return None

class AuthMiddleware:
    """Authentication middleware for web applications"""
    
    def __init__(self, auth_service: AuthenticationService, protected_paths: List[str] = None):
        self.auth_service = auth_service
        self.protected_paths = protected_paths or ['/api/', '/admin/', '/dashboard/']
    
    @middleware
    async def middleware(self, request, handler):
        """Authentication middleware"""
        path = request.path
        
        # Skip authentication for public paths
        if not any(path.startswith(p) for p in self.protected_paths):
            return await handler(request)
        
        # Get session ID from cookie or header
        session_id = None
        
        # Try session cookie
        if 'session_id' in request.cookies:
            session_id = request.cookies['session_id']
        
        # Try Authorization header
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            # Try JWT token
            payload = await self.auth_service.verify_jwt_token(token)
            if payload:
                # Create temporary session from JWT
                request['user'] = {
                    'user_id': payload['user_id'],
                    'tenant_id': payload.get('tenant_id'),
                    'role': payload['role']
                }
                return await handler(request)
            else:
                session_id = token
        
        # Try API key authentication
        if auth_header.startswith('ApiKey '):
            api_key_parts = auth_header[7:].split(':', 1)
            if len(api_key_parts) == 2:
                key_id, secret = api_key_parts
                api_key_data = await self.auth_service.validate_api_key(key_id, secret)
                if api_key_data:
                    request['api_key'] = api_key_data
                    return await handler(request)
        
        if not session_id:
            return web.json_response({
                'error': 'Authentication required',
                'code': 'AUTH_REQUIRED'
            }, status=401)
        
        # Validate session
        ip_address = request.remote
        user_agent = request.headers.get('User-Agent', '')
        
        session = await self.auth_service.validate_session(session_id, ip_address, user_agent)
        
        if not session:
            return web.json_response({
                'error': 'Invalid or expired session',
                'code': 'SESSION_INVALID'
            }, status=401)
        
        # Add session to request
        request['session'] = session
        request['user'] = {
            'user_id': session.user_id,
            'tenant_id': session.tenant_id,
            'role': session.role,
            'permissions': session.permissions
        }
        
        return await handler(request)

class SaleorDashboardProxy:
    """Security proxy for Saleor dashboard with authentication"""
    
    def __init__(self, auth_service: AuthenticationService, saleor_url: str):
        self.auth_service = auth_service
        self.saleor_url = saleor_url
        self.required_permissions = ['saleor:read', 'dashboard:access']
    
    async def proxy_request(self, request):
        """Proxy request to Saleor with authentication"""
        
        # Check permissions
        session = request.get('session')
        if not session:
            return web.json_response({
                'error': 'Authentication required for Saleor dashboard',
                'code': 'SALEOR_AUTH_REQUIRED'
            }, status=401)
        
        # Check if user has required permissions
        user_permissions = session.permissions
        has_permission = any(
            perm in user_permissions or 'admin:*' in user_permissions 
            for perm in self.required_permissions
        )
        
        if not has_permission:
            await self.auth_service.log_security_event(SecurityEvent(
                event_type=SecurityEventType.UNAUTHORIZED_ACCESS,
                user_id=session.user_id,
                tenant_id=session.tenant_id,
                ip_address=session.ip_address,
                user_agent=request.headers.get('User-Agent', ''),
                timestamp=datetime.utcnow(),
                details={
                    'attempted_resource': 'saleor_dashboard',
                    'required_permissions': self.required_permissions,
                    'user_permissions': user_permissions
                },
                risk_score=40
            ))
            
            return web.json_response({
                'error': 'Insufficient permissions for Saleor dashboard',
                'code': 'SALEOR_PERMISSION_DENIED'
            }, status=403)
        
        # Proxy the request to Saleor
        async with aiohttp.ClientSession() as client_session:
            # Forward the request to Saleor
            url = f"{self.saleor_url.rstrip('/')}{request.path_qs}"
            
            headers = dict(request.headers)
            # Remove hop-by-hop headers
            for h in ['connection', 'upgrade', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding']:
                headers.pop(h, None)
            
            # Add authentication headers for Saleor
            headers['X-User-ID'] = session.user_id
            headers['X-Tenant-ID'] = session.tenant_id or ''
            
            try:
                if request.method == 'GET':
                    async with client_session.get(url, headers=headers) as response:
                        content = await response.read()
                        return web.Response(
                            body=content,
                            status=response.status,
                            headers=response.headers
                        )
                elif request.method == 'POST':
                    data = await request.read()
                    async with client_session.post(url, data=data, headers=headers) as response:
                        content = await response.read()
                        return web.Response(
                            body=content,
                            status=response.status,
                            headers=response.headers
                        )
                else:
                    return web.json_response({
                        'error': 'Method not allowed',
                        'code': 'METHOD_NOT_ALLOWED'
                    }, status=405)
                    
            except aiohttp.ClientError as e:
                logger.error(f"Saleor proxy error: {e}")
                return web.json_response({
                    'error': 'Saleor service unavailable',
                    'code': 'SALEOR_UNAVAILABLE'
                }, status=503)
