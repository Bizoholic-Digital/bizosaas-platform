"""
Security utilities for order processing workflow
Authentication, authorization, and security validation
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)

# Security configuration
SECURITY_CONFIG = {
    "jwt_secret": "your-secret-key-change-in-production",
    "jwt_algorithm": "HS256",
    "jwt_expiration_hours": 24,
    "api_key_header": "X-API-Key",
    "rate_limit_per_minute": 100,
    "require_https": False,  # Set to True in production
    "password_min_length": 8
}

# Initialize security scheme
security_scheme = HTTPBearer()

# API keys (in production, store in secure database)
API_KEYS = {
    "test-api-key-123": {
        "name": "Test Client",
        "permissions": ["orders:read", "orders:write", "inventory:read"],
        "rate_limit": 1000,
        "active": True
    },
    "admin-api-key-456": {
        "name": "Admin Client",
        "permissions": ["*"],  # All permissions
        "rate_limit": 10000,
        "active": True
    }
}

# User roles and permissions
ROLE_PERMISSIONS = {
    "admin": [
        "orders:*",
        "inventory:*",
        "payments:*",
        "fulfillment:*",
        "analytics:*",
        "users:*"
    ],
    "manager": [
        "orders:read",
        "orders:write",
        "inventory:read",
        "inventory:write",
        "payments:read",
        "fulfillment:read",
        "fulfillment:write",
        "analytics:read"
    ],
    "operator": [
        "orders:read",
        "orders:write",
        "inventory:read",
        "fulfillment:read",
        "fulfillment:write"
    ],
    "customer": [
        "orders:read",
        "orders:write"
    ],
    "readonly": [
        "orders:read",
        "inventory:read",
        "analytics:read"
    ]
}


class AuthenticationError(Exception):
    """Authentication failed"""
    pass


class AuthorizationError(Exception):
    """Authorization failed"""
    pass


class SecurityValidator:
    """Security validation utilities"""
    
    def __init__(self):
        self.failed_attempts = {}  # Track failed authentication attempts
        
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        
        issues = []
        score = 0
        
        # Length check
        if len(password) < SECURITY_CONFIG["password_min_length"]:
            issues.append(f"Password must be at least {SECURITY_CONFIG['password_min_length']} characters long")
        else:
            score += 1
        
        # Character variety checks
        if any(c.islower() for c in password):
            score += 1
        else:
            issues.append("Password must contain lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            issues.append("Password must contain uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            issues.append("Password must contain numbers")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            issues.append("Password must contain special characters")
        
        # Determine strength
        if score >= 4:
            strength = "strong"
        elif score >= 3:
            strength = "medium"
        elif score >= 2:
            strength = "weak"
        else:
            strength = "very_weak"
        
        return {
            "valid": len(issues) == 0,
            "strength": strength,
            "score": score,
            "issues": issues
        }
    
    def validate_order_access(self, user: Dict[str, Any], order: Dict[str, Any]) -> bool:
        """Validate if user can access specific order"""
        
        user_role = user.get("role", "customer")
        user_id = user.get("user_id")
        
        # Admins and managers can access all orders
        if user_role in ["admin", "manager"]:
            return True
        
        # Customers can only access their own orders
        if user_role == "customer":
            return order.get("customer_id") == user_id
        
        # Operators can access orders they're assigned to or all if no specific assignment
        if user_role == "operator":
            assigned_orders = user.get("assigned_orders", [])
            if not assigned_orders:  # No specific assignment means access to all
                return True
            return order.get("id") in assigned_orders
        
        return False
    
    def validate_ip_whitelist(self, client_ip: str, whitelist: List[str]) -> bool:
        """Validate client IP against whitelist"""
        
        if not whitelist:
            return True  # No whitelist means all IPs allowed
        
        # Simple IP validation (in production, use proper CIDR matching)
        return client_ip in whitelist
    
    def check_rate_limit(self, identifier: str, limit_per_minute: int = None) -> bool:
        """Check if request is within rate limit"""
        
        if limit_per_minute is None:
            limit_per_minute = SECURITY_CONFIG["rate_limit_per_minute"]
        
        current_time = datetime.utcnow()
        
        # Simple in-memory rate limiting (use Redis in production)
        if not hasattr(self, 'rate_limit_data'):
            self.rate_limit_data = {}
        
        if identifier not in self.rate_limit_data:
            self.rate_limit_data[identifier] = []
        
        # Remove old entries (older than 1 minute)
        cutoff_time = current_time - timedelta(minutes=1)
        self.rate_limit_data[identifier] = [
            timestamp for timestamp in self.rate_limit_data[identifier]
            if timestamp > cutoff_time
        ]
        
        # Check if under limit
        if len(self.rate_limit_data[identifier]) >= limit_per_minute:
            return False
        
        # Add current request
        self.rate_limit_data[identifier].append(current_time)
        return True


# Security utilities
security_validator = SecurityValidator()


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_jwt_token(user_data: Dict[str, Any]) -> str:
    """Create JWT token for user"""
    
    payload = {
        "user_id": user_data["user_id"],
        "email": user_data["email"],
        "role": user_data["role"],
        "permissions": user_data.get("permissions", []),
        "exp": datetime.utcnow() + timedelta(hours=SECURITY_CONFIG["jwt_expiration_hours"]),
        "iat": datetime.utcnow(),
        "iss": "order-processing-workflow"
    }
    
    token = jwt.encode(
        payload, 
        SECURITY_CONFIG["jwt_secret"], 
        algorithm=SECURITY_CONFIG["jwt_algorithm"]
    )
    
    return token


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token"""
    
    try:
        payload = jwt.decode(
            token,
            SECURITY_CONFIG["jwt_secret"],
            algorithms=[SECURITY_CONFIG["jwt_algorithm"]]
        )
        
        return payload
        
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")


def verify_api_key(api_key: str) -> Dict[str, Any]:
    """Verify API key and return client info"""
    
    if api_key not in API_KEYS:
        raise AuthenticationError("Invalid API key")
    
    client_info = API_KEYS[api_key]
    
    if not client_info["active"]:
        raise AuthenticationError("API key is inactive")
    
    return client_info


def check_permission(user_permissions: List[str], required_permission: str) -> bool:
    """Check if user has required permission"""
    
    # Check for wildcard permission
    if "*" in user_permissions:
        return True
    
    # Check for exact permission
    if required_permission in user_permissions:
        return True
    
    # Check for wildcard in permission category
    permission_parts = required_permission.split(":")
    if len(permission_parts) == 2:
        category_wildcard = f"{permission_parts[0]}:*"
        if category_wildcard in user_permissions:
            return True
    
    return False


def require_permission(required_permission: str):
    """Decorator to require specific permission"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This would be used with dependency injection in FastAPI
            # For now, it's a placeholder
            return func(*args, **kwargs)
        return wrapper
    return decorator


# FastAPI dependency functions

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> Dict[str, Any]:
    """Get current authenticated user from JWT token"""
    
    try:
        token = credentials.credentials
        payload = decode_jwt_token(token)
        
        # In production, you might want to validate user still exists in database
        user_data = {
            "user_id": payload["user_id"],
            "email": payload["email"],
            "role": payload["role"],
            "permissions": payload.get("permissions", [])
        }
        
        return user_data
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_api_client(api_key: str) -> Dict[str, Any]:
    """Get API client info from API key"""
    
    try:
        client_info = verify_api_key(api_key)
        return client_info
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


def require_permissions(required_permissions: List[str]):
    """Dependency to require specific permissions"""
    
    def permission_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_permissions = current_user.get("permissions", [])
        
        for required_permission in required_permissions:
            if not check_permission(user_permissions, required_permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {required_permission}"
                )
        
        return current_user
    
    return permission_checker


def validate_order_access_permission(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency to validate order access permissions"""
    
    required_permissions = ["orders:read", "orders:write"]
    
    user_permissions = current_user.get("permissions", [])
    
    has_permission = any(
        check_permission(user_permissions, perm) 
        for perm in required_permissions
    )
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Order access permission required"
        )
    
    return current_user


class SecurityMiddleware:
    """Security middleware for additional protection"""
    
    def __init__(self):
        self.blocked_ips = set()
        self.suspicious_activity = {}
    
    def check_request_security(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check request for security issues"""
        
        security_check = {
            "passed": True,
            "warnings": [],
            "blocked": False,
            "risk_score": 0
        }
        
        client_ip = request_data.get("client_ip", "unknown")
        user_agent = request_data.get("user_agent", "")
        
        # Check blocked IPs
        if client_ip in self.blocked_ips:
            security_check["passed"] = False
            security_check["blocked"] = True
            security_check["warnings"].append("IP address is blocked")
            return security_check
        
        # Check for suspicious user agents
        suspicious_agents = ["bot", "crawler", "scanner", "hack"]
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            security_check["risk_score"] += 20
            security_check["warnings"].append("Suspicious user agent detected")
        
        # Check request frequency
        if not security_validator.check_rate_limit(client_ip):
            security_check["risk_score"] += 50
            security_check["warnings"].append("Rate limit exceeded")
        
        # Determine if request should be blocked
        if security_check["risk_score"] >= 70:
            security_check["passed"] = False
            security_check["blocked"] = True
        
        return security_check
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security event"""
        
        logger.warning(f"Security event: {event_type} - {details}")
        
        # In production, this would send to security monitoring system


# Input validation utilities

def validate_order_input(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate order input data for security"""
    
    validation_result = {
        "valid": True,
        "errors": [],
        "sanitized_data": order_data.copy()
    }
    
    # Validate required fields
    required_fields = ["customer_id", "items", "billing_address", "shipping_address"]
    for field in required_fields:
        if field not in order_data:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Missing required field: {field}")
    
    # Validate email addresses
    email_fields = ["billing_address.email", "shipping_address.email"]
    for field_path in email_fields:
        email = _get_nested_value(order_data, field_path)
        if email and not _is_valid_email(email):
            validation_result["valid"] = False
            validation_result["errors"].append(f"Invalid email format: {field_path}")
    
    # Validate amounts
    if "items" in order_data:
        for i, item in enumerate(order_data["items"]):
            if "unit_price" in item:
                try:
                    price = float(item["unit_price"])
                    if price < 0:
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"Item {i}: negative price not allowed")
                    if price > 10000:  # Reasonable upper limit
                        validation_result["warnings"] = validation_result.get("warnings", [])
                        validation_result["warnings"].append(f"Item {i}: unusually high price")
                except (ValueError, TypeError):
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Item {i}: invalid price format")
    
    # Sanitize string inputs
    _sanitize_strings(validation_result["sanitized_data"])
    
    return validation_result


def _get_nested_value(data: Dict[str, Any], path: str) -> Any:
    """Get nested value from dictionary using dot notation"""
    
    keys = path.split(".")
    value = data
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None
    
    return value


def _is_valid_email(email: str) -> bool:
    """Basic email validation"""
    
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def _sanitize_strings(data: Any):
    """Sanitize string inputs to prevent injection attacks"""
    
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = _sanitize_strings(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            data[i] = _sanitize_strings(item)
    elif isinstance(data, str):
        # Basic sanitization - remove potentially dangerous characters
        dangerous_chars = ["<", ">", "\"", "'", "&", ";", "(", ")", "script"]
        sanitized = data
        for char in dangerous_chars:
            if char in sanitized.lower():
                sanitized = sanitized.replace(char, "")
        return sanitized
    
    return data


# Encryption utilities (for sensitive data)

def encrypt_sensitive_data(data: str, key: Optional[str] = None) -> str:
    """Encrypt sensitive data (basic implementation)"""
    
    # In production, use proper encryption like Fernet
    # This is a placeholder implementation
    import base64
    
    if key is None:
        key = SECURITY_CONFIG["jwt_secret"]
    
    # Simple XOR encryption (NOT secure for production)
    encrypted = ""
    for i, char in enumerate(data):
        encrypted += chr(ord(char) ^ ord(key[i % len(key)]))
    
    return base64.b64encode(encrypted.encode()).decode()


def decrypt_sensitive_data(encrypted_data: str, key: Optional[str] = None) -> str:
    """Decrypt sensitive data"""
    
    import base64
    
    if key is None:
        key = SECURITY_CONFIG["jwt_secret"]
    
    try:
        decoded = base64.b64decode(encrypted_data.encode()).decode()
        
        decrypted = ""
        for i, char in enumerate(decoded):
            decrypted += chr(ord(char) ^ ord(key[i % len(key)]))
        
        return decrypted
        
    except Exception:
        raise ValueError("Failed to decrypt data")


# Security audit utilities

def audit_access(user: Dict[str, Any], action: str, resource: str, success: bool):
    """Audit user access for compliance"""
    
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user.get("user_id", "unknown"),
        "user_email": user.get("email", "unknown"),
        "action": action,
        "resource": resource,
        "success": success,
        "ip_address": "unknown"  # Would be populated from request context
    }
    
    logger.info(f"AUDIT: {audit_entry}")
    
    # In production, this would be sent to audit logging system


def generate_security_report() -> Dict[str, Any]:
    """Generate security status report"""
    
    return {
        "total_api_keys": len(API_KEYS),
        "active_api_keys": len([k for k in API_KEYS.values() if k["active"]]),
        "blocked_ips": len(getattr(security_validator, 'blocked_ips', [])),
        "rate_limit_violations": 0,  # Would track actual violations
        "failed_authentications": len(getattr(security_validator, 'failed_attempts', {})),
        "last_security_scan": datetime.utcnow().isoformat(),
        "security_level": "medium"  # Would be calculated based on actual metrics
    }