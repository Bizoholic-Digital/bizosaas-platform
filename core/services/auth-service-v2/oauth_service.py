"""
OAuth 2.0 Service for SSO Integration
Supports: Google, Microsoft/Azure AD, GitHub, Slack, LinkedIn
"""

import os
import secrets
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from urllib.parse import urlencode

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.logging_system import get_logger, LogLevel, LogCategory


class OAuthProvider:
    """Base OAuth provider configuration"""

    def __init__(
        self,
        name: str,
        client_id: str,
        client_secret: str,
        authorize_url: str,
        token_url: str,
        userinfo_url: str,
        scopes: list[str],
        redirect_uri: str
    ):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url
        self.scopes = scopes
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, state: str) -> str:
        """Generate OAuth authorization URL"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(self.scopes),
            'state': state,
        }
        return f"{self.authorize_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri,
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from provider"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.userinfo_url,
                headers={'Authorization': f'Bearer {access_token}'}
            )
            response.raise_for_status()
            return response.json()


class OAuthService:
    """OAuth service for managing SSO providers"""

    def __init__(self):
        self.logger = get_logger()
        self.providers = self._initialize_providers()
        self.state_store: Dict[str, Dict[str, Any]] = {}  # In production, use Redis

    def _initialize_providers(self) -> Dict[str, OAuthProvider]:
        """Initialize OAuth providers from environment variables"""
        base_url = os.getenv('NEXT_PUBLIC_APP_URL', 'https://stg.bizoholic.com/portal')

        providers = {}

        # Google OAuth
        if os.getenv('GOOGLE_CLIENT_ID'):
            providers['google'] = OAuthProvider(
                name='google',
                client_id=os.getenv('GOOGLE_CLIENT_ID'),
                client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
                authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
                token_url='https://oauth2.googleapis.com/token',
                userinfo_url='https://www.googleapis.com/oauth2/v2/userinfo',
                scopes=['openid', 'email', 'profile'],
                redirect_uri=f'{base_url}/auth/callback/google'
            )

        # Microsoft/Azure AD OAuth
        if os.getenv('MICROSOFT_CLIENT_ID'):
            providers['microsoft'] = OAuthProvider(
                name='microsoft',
                client_id=os.getenv('MICROSOFT_CLIENT_ID'),
                client_secret=os.getenv('MICROSOFT_CLIENT_SECRET'),
                authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
                token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
                userinfo_url='https://graph.microsoft.com/v1.0/me',
                scopes=['openid', 'email', 'profile', 'User.Read'],
                redirect_uri=f'{base_url}/auth/callback/microsoft'
            )

        # GitHub OAuth
        if os.getenv('GITHUB_CLIENT_ID'):
            providers['github'] = OAuthProvider(
                name='github',
                client_id=os.getenv('GITHUB_CLIENT_ID'),
                client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
                authorize_url='https://github.com/login/oauth/authorize',
                token_url='https://github.com/login/oauth/access_token',
                userinfo_url='https://api.github.com/user',
                scopes=['read:user', 'user:email'],
                redirect_uri=f'{base_url}/auth/callback/github'
            )

        # Slack OAuth
        if os.getenv('SLACK_CLIENT_ID'):
            providers['slack'] = OAuthProvider(
                name='slack',
                client_id=os.getenv('SLACK_CLIENT_ID'),
                client_secret=os.getenv('SLACK_CLIENT_SECRET'),
                authorize_url='https://slack.com/oauth/v2/authorize',
                token_url='https://slack.com/api/oauth.v2.access',
                userinfo_url='https://slack.com/api/users.identity',
                scopes=['identity.basic', 'identity.email'],
                redirect_uri=f'{base_url}/auth/callback/slack'
            )

        # LinkedIn OAuth
        if os.getenv('LINKEDIN_CLIENT_ID'):
            providers['linkedin'] = OAuthProvider(
                name='linkedin',
                client_id=os.getenv('LINKEDIN_CLIENT_ID'),
                client_secret=os.getenv('LINKEDIN_CLIENT_SECRET'),
                authorize_url='https://www.linkedin.com/oauth/v2/authorization',
                token_url='https://www.linkedin.com/oauth/v2/accessToken',
                userinfo_url='https://api.linkedin.com/v2/me',
                scopes=['r_liteprofile', 'r_emailaddress'],
                redirect_uri=f'{base_url}/auth/callback/linkedin'
            )

        return providers

    def get_provider(self, provider_name: str) -> OAuthProvider:
        """Get OAuth provider by name"""
        provider = self.providers.get(provider_name)
        if not provider:
            raise HTTPException(
                status_code=400,
                detail=f"OAuth provider '{provider_name}' not configured"
            )
        return provider

    def generate_state(self, provider_name: str) -> str:
        """Generate and store CSRF state parameter"""
        state = secrets.token_urlsafe(32)
        self.state_store[state] = {
            'provider': provider_name,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(minutes=5)
        }
        return state

    def verify_state(self, state: str) -> Optional[str]:
        """Verify and consume state parameter"""
        state_data = self.state_store.pop(state, None)

        if not state_data:
            return None

        if datetime.utcnow() > state_data['expires_at']:
            return None

        return state_data['provider']

    async def get_authorization_url(self, provider_name: str) -> Dict[str, str]:
        """Generate OAuth authorization URL with state"""
        provider = self.get_provider(provider_name)
        state = self.generate_state(provider_name)

        await self.logger.log(
            LogLevel.INFO,
            LogCategory.AUTHENTICATION,
            "oauth-service",
            f"OAuth authorization initiated: {provider_name}",
            details={'provider': provider_name, 'state': state}
        )

        authorization_url = provider.get_authorization_url(state)

        return {
            'authorization_url': authorization_url,
            'state': state
        }

    async def handle_callback(
        self,
        provider_name: str,
        code: str,
        state: str
    ) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for user info"""

        # Verify state parameter (CSRF protection)
        verified_provider = self.verify_state(state)
        if not verified_provider or verified_provider != provider_name:
            await self.logger.log(
                LogLevel.ERROR,
                LogCategory.AUTHENTICATION,
                "oauth-service",
                f"OAuth state verification failed: {provider_name}",
                details={'provider': provider_name, 'state': state}
            )
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired OAuth state"
            )

        provider = self.get_provider(provider_name)

        try:
            # Exchange code for access token
            token_data = await provider.exchange_code_for_token(code)
            access_token = token_data.get('access_token')

            if not access_token:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to obtain access token"
                )

            # Get user information
            user_info = await provider.get_user_info(access_token)

            await self.logger.log(
                LogLevel.INFO,
                LogCategory.AUTHENTICATION,
                "oauth-service",
                f"OAuth user info retrieved: {provider_name}",
                details={
                    'provider': provider_name,
                    'email': user_info.get('email', 'N/A')
                }
            )

            # Normalize user data across providers
            normalized_user = self._normalize_user_data(provider_name, user_info)

            return {
                'provider': provider_name,
                'access_token': access_token,
                'refresh_token': token_data.get('refresh_token'),
                'expires_in': token_data.get('expires_in'),
                'user': normalized_user
            }

        except httpx.HTTPError as e:
            await self.logger.log(
                LogLevel.ERROR,
                LogCategory.AUTHENTICATION,
                "oauth-service",
                f"OAuth callback failed: {provider_name}",
                details={'provider': provider_name, 'error': str(e)},
                error=e
            )
            raise HTTPException(
                status_code=400,
                detail=f"OAuth authentication failed: {str(e)}"
            )

    def _normalize_user_data(
        self,
        provider_name: str,
        user_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Normalize user data across different OAuth providers"""

        if provider_name == 'google':
            return {
                'provider_user_id': user_info.get('id'),
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'picture': user_info.get('picture'),
                'email_verified': user_info.get('verified_email', False)
            }

        elif provider_name == 'microsoft':
            return {
                'provider_user_id': user_info.get('id'),
                'email': user_info.get('mail') or user_info.get('userPrincipalName'),
                'name': user_info.get('displayName'),
                'picture': None,  # Requires separate API call
                'email_verified': True  # Azure AD emails are pre-verified
            }

        elif provider_name == 'github':
            return {
                'provider_user_id': str(user_info.get('id')),
                'email': user_info.get('email'),
                'name': user_info.get('name') or user_info.get('login'),
                'picture': user_info.get('avatar_url'),
                'email_verified': user_info.get('email') is not None
            }

        elif provider_name == 'slack':
            user = user_info.get('user', {})
            return {
                'provider_user_id': user.get('id'),
                'email': user.get('email'),
                'name': user.get('name'),
                'picture': user.get('image_192'),
                'email_verified': True  # Slack emails are pre-verified
            }

        elif provider_name == 'linkedin':
            return {
                'provider_user_id': user_info.get('id'),
                'email': None,  # Requires separate API call to emailAddress endpoint
                'name': f"{user_info.get('localizedFirstName', '')} {user_info.get('localizedLastName', '')}".strip(),
                'picture': user_info.get('profilePicture', {}).get('displayImage'),
                'email_verified': True
            }

        return user_info

    def get_available_providers(self) -> list[Dict[str, Any]]:
        """Get list of available OAuth providers"""
        return [
            {
                'name': name,
                'display_name': name.capitalize(),
                'enabled': True
            }
            for name in self.providers.keys()
        ]


# Singleton instance
oauth_service = OAuthService()
