"""
JWT Authentication for Django CRM
Multi-tenant JWT authentication with BizOSaaS integration
"""
import jwt
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def get_user_model_safe():
    """Lazy import of User model to avoid AppRegistryNotReady"""
    return get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JWT Token authentication for multi-tenant CRM
    Integrates with BizOSaaS auth service
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return (user, auth) tuple
        """
        token = self.get_token_from_request(request)
        if not token:
            return None
            
        try:
            payload = self.decode_token(token)
            user = self.get_user_from_payload(payload)
            
            # Set tenant context if available
            if 'tenant_id' in payload:
                request.tenant_id = payload['tenant_id']
            
            return (user, token)
            
        except (jwt.InvalidTokenError, get_user_model_safe().DoesNotExist) as e:
            logger.warning(f"Authentication failed: {e}")
            raise exceptions.AuthenticationFailed('Invalid token')
    
    def get_token_from_request(self, request):
        """Extract JWT token from request headers"""
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
            
        try:
            auth_type, token = auth_header.split(' ', 1)
            if auth_type.lower() != 'bearer':
                return None
            return token
        except ValueError:
            return None
    
    def decode_token(self, token):
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # Check token expiration
            if 'exp' in payload:
                exp_timestamp = payload['exp']
                if datetime.utcnow().timestamp() > exp_timestamp:
                    raise jwt.ExpiredSignatureError('Token has expired')
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')
    
    def get_user_from_payload(self, payload):
        """Get user from JWT payload"""
        User = get_user_model_safe()
        try:
            user_id = payload.get('user_id')
            email = payload.get('email')

            if user_id:
                return User.objects.get(id=user_id)
            elif email:
                return User.objects.get(email=email)
            else:
                raise User.DoesNotExist('No user identifier in token')

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')


class TokenManager:
    """JWT token management utilities"""
    
    @staticmethod
    def generate_token(user, tenant_id=None, expires_in=None):
        """Generate JWT token for user"""
        if expires_in is None:
            expires_in = settings.JWT_EXPIRATION_DELTA
        
        payload = {
            'user_id': str(user.id),
            'email': user.email,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow(),
        }
        
        if tenant_id:
            payload['tenant_id'] = str(tenant_id)
        
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return token
    
    @staticmethod
    def refresh_token(token):
        """Refresh JWT token if valid"""
        User = get_user_model_safe()
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={'verify_exp': False}  # Don't verify expiration for refresh
            )

            user = User.objects.get(id=payload['user_id'])
            tenant_id = payload.get('tenant_id')

            return TokenManager.generate_token(user, tenant_id)

        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid refresh token')
    
    @staticmethod
    def validate_token(token):
        """Validate token without authentication"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return True, payload
        except jwt.InvalidTokenError as e:
            return False, str(e)


def require_tenant(view_func):
    """Decorator to require tenant context"""
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'tenant_id'):
            return Response(
                {'error': 'Tenant context required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return view_func(request, *args, **kwargs)
    return wrapper