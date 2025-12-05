import jwt
import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)

class BizOSaaSJWTAuthentication(BaseAuthentication):
    """
    Custom authentication class that validates JWT tokens from BizOSaaS
    and creates/updates local Wagtail users accordingly
    """
    
    def authenticate(self, request):
        auth_header = self.get_authorization_header(request)
        
        if not auth_header:
            return None
            
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != 'bearer':
                return None
                
        except ValueError:
            return None
            
        return self.authenticate_credentials(token)
    
    def get_authorization_header(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            return None
        return auth.encode('iso-8859-1')
    
    def authenticate_credentials(self, token):
        try:
            # Validate token with BizOSaaS
            payload = jwt.decode(
                token, 
                settings.BIZOSAAS_JWT_SECRET, 
                algorithms=['HS256']
            )
            
            user_id = payload.get('user_id')
            tenant_id = payload.get('tenant_id')
            
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')
            
            # Get or create local user
            user = self.get_or_create_user(payload)
            
            # Attach tenant information for multi-tenancy
            user.current_tenant_id = tenant_id
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationFailed('Authentication failed')
    
    def get_or_create_user(self, payload):
        """
        Get or create a local Wagtail user based on BizOSaaS user data
        """
        user_id = payload.get('user_id')
        email = payload.get('email')
        username = payload.get('username', email)
        first_name = payload.get('first_name', '')
        last_name = payload.get('last_name', '')
        is_admin = payload.get('is_admin', False)
        
        try:
            # Try to find user by email first
            user = User.objects.get(email=email)
            
            # Update user information
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_admin
            user.is_superuser = is_admin
            user.save()
            
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_admin,
                is_superuser=is_admin
            )
            
            logger.info(f"Created new Wagtail user: {email}")
        
        return user

class BizOSaaSUserSync:
    """
    Service for syncing users between BizOSaaS and Wagtail
    """
    
    @staticmethod
    def sync_user_from_bizosaas(user_data):
        """
        Sync a user from BizOSaaS to Wagtail
        """
        try:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data.get('username', user_data['email']),
                    'first_name': user_data.get('first_name', ''),
                    'last_name': user_data.get('last_name', ''),
                    'is_staff': user_data.get('is_admin', False),
                    'is_superuser': user_data.get('is_admin', False),
                }
            )
            
            if not created:
                # Update existing user
                user.username = user_data.get('username', user_data['email'])
                user.first_name = user_data.get('first_name', '')
                user.last_name = user_data.get('last_name', '')
                user.is_staff = user_data.get('is_admin', False)
                user.is_superuser = user_data.get('is_admin', False)
                user.save()
            
            return user, created
            
        except Exception as e:
            logger.error(f"Error syncing user {user_data.get('email')}: {str(e)}")
            raise
    
    @staticmethod
    def validate_bizosaas_session(token):
        """
        Validate session with BizOSaaS backend
        """
        try:
            response = requests.get(
                f"{settings.BIZOSAAS_API_URL}/api/v1/auth/validate",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error validating BizOSaaS session: {str(e)}")
            return None