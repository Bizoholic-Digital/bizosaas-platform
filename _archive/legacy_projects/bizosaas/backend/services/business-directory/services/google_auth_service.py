"""
Google Authentication Service
Handles OAuth 2.0 flow for Google Business Profile API access
"""

import os
import json
import secrets
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from urllib.parse import urlencode, parse_qs, urlparse

import httpx
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.exceptions import RefreshError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from cryptography.fernet import Fernet

from ..models.google_integration import GoogleAccount, GoogleAccountStatus
from ..core.config import settings
from ..core.database import get_async_session

logger = logging.getLogger(__name__)


class GoogleAuthService:
    """
    Service for managing Google OAuth 2.0 authentication and token management
    """
    
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scopes = settings.GOOGLE_SCOPES.split(',') if hasattr(settings, 'GOOGLE_SCOPES') else [
            'https://www.googleapis.com/auth/business.manage'
        ]
        
        # Initialize encryption for storing tokens securely
        if not hasattr(settings, 'ENCRYPTION_KEY'):
            # Generate a key for development - in production, this should be set via environment
            settings.ENCRYPTION_KEY = Fernet.generate_key()
        
        self.cipher = Fernet(settings.ENCRYPTION_KEY if isinstance(settings.ENCRYPTION_KEY, bytes) 
                           else settings.ENCRYPTION_KEY.encode())
    
    def get_authorization_url(self, tenant_id: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate Google OAuth authorization URL
        
        Args:
            tenant_id: Tenant ID for multi-tenant isolation
            state: Optional state parameter for CSRF protection
            
        Returns:
            Dictionary containing authorization URL and state
        """
        try:
            # Create OAuth flow
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            # Generate state if not provided
            if not state:
                state = secrets.token_urlsafe(32)
            
            # Include tenant_id in state for security
            secure_state = f"{tenant_id}:{state}"
            
            # Generate authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=secure_state,
                prompt='consent'  # Force consent screen to get refresh token
            )
            
            logger.info(f"Generated Google auth URL for tenant {tenant_id}")
            
            return {
                "authorization_url": auth_url,
                "state": secure_state,
                "scopes": self.scopes
            }
            
        except Exception as e:
            logger.error(f"Error generating authorization URL: {str(e)}")
            raise ValueError(f"Failed to generate authorization URL: {str(e)}")
    
    async def handle_oauth_callback(
        self, 
        code: str, 
        state: str, 
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle OAuth callback and exchange code for tokens
        
        Args:
            code: Authorization code from Google
            state: State parameter for CSRF protection
            error: Error parameter if OAuth failed
            
        Returns:
            Dictionary containing account information and success status
        """
        if error:
            logger.error(f"OAuth callback error: {error}")
            raise ValueError(f"OAuth authorization failed: {error}")
        
        try:
            # Extract tenant_id from state
            if ':' not in state:
                raise ValueError("Invalid state parameter")
            
            tenant_id, original_state = state.split(':', 1)
            
            # Create OAuth flow
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes,
                state=state
            )
            flow.redirect_uri = self.redirect_uri
            
            # Exchange code for tokens
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            # Get user info from Google
            user_info = await self._get_user_info(credentials.token)
            
            # Save or update Google account
            account = await self._save_google_account(
                tenant_id=tenant_id,
                credentials=credentials,
                user_info=user_info
            )
            
            logger.info(f"Successfully authenticated Google account {user_info['email']} for tenant {tenant_id}")
            
            return {
                "success": True,
                "account_id": str(account.id),
                "email": user_info['email'],
                "display_name": user_info.get('name'),
                "granted_scopes": credentials.granted_scopes,
                "tenant_id": tenant_id
            }
            
        except Exception as e:
            logger.error(f"Error handling OAuth callback: {str(e)}")
            raise ValueError(f"Failed to process OAuth callback: {str(e)}")
    
    async def refresh_access_token(self, account: GoogleAccount) -> bool:
        """
        Refresh access token for a Google account
        
        Args:
            account: GoogleAccount instance
            
        Returns:
            True if refresh successful, False otherwise
        """
        try:
            if not account.refresh_token:
                logger.error(f"No refresh token available for account {account.email}")
                return False
            
            # Decrypt refresh token
            refresh_token = self.cipher.decrypt(account.refresh_token.encode()).decode()
            
            # Create credentials object
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes
            )
            
            # Refresh the token
            request = Request()
            credentials.refresh(request)
            
            # Update account with new token
            async with get_async_session() as session:
                encrypted_token = self.cipher.encrypt(credentials.token.encode()).decode()
                
                await session.execute(
                    update(GoogleAccount)
                    .where(GoogleAccount.id == account.id)
                    .values(
                        access_token=encrypted_token,
                        token_expires_at=credentials.expiry,
                        status=GoogleAccountStatus.CONNECTED.value,
                        error_count=0,
                        last_error=None
                    )
                )
                await session.commit()
            
            logger.info(f"Successfully refreshed token for account {account.email}")
            return True
            
        except RefreshError as e:
            logger.error(f"Refresh token expired or invalid for account {account.email}: {str(e)}")
            await self._mark_account_expired(account)
            return False
        except Exception as e:
            logger.error(f"Error refreshing token for account {account.email}: {str(e)}")
            account.mark_error(f"Token refresh failed: {str(e)}")
            return False
    
    async def get_valid_credentials(self, account: GoogleAccount) -> Optional[Credentials]:
        """
        Get valid credentials for a Google account, refreshing if necessary
        
        Args:
            account: GoogleAccount instance
            
        Returns:
            Valid Credentials object or None if unable to get valid credentials
        """
        try:
            if not account.is_active:
                logger.warning(f"Account {account.email} is not active")
                return None
            
            # Decrypt access token
            access_token = self.cipher.decrypt(account.access_token.encode()).decode()
            refresh_token = None
            
            if account.refresh_token:
                refresh_token = self.cipher.decrypt(account.refresh_token.encode()).decode()
            
            # Create credentials object
            credentials = Credentials(
                token=access_token,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes,
                expiry=account.token_expires_at
            )
            
            # Check if token needs refresh
            if account.is_token_expired and refresh_token:
                logger.info(f"Access token expired for {account.email}, refreshing...")
                if await self.refresh_access_token(account):
                    # Get updated credentials after refresh
                    return await self.get_valid_credentials(account)
                else:
                    return None
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error getting valid credentials for account {account.email}: {str(e)}")
            account.mark_error(f"Failed to get valid credentials: {str(e)}")
            return None
    
    async def disconnect_account(self, account_id: str, tenant_id: str) -> bool:
        """
        Disconnect a Google account and revoke access
        
        Args:
            account_id: Google account ID to disconnect
            tenant_id: Tenant ID for security
            
        Returns:
            True if disconnection successful
        """
        try:
            async with get_async_session() as session:
                # Get account
                result = await session.execute(
                    select(GoogleAccount)
                    .where(
                        GoogleAccount.id == account_id,
                        GoogleAccount.tenant_id == tenant_id
                    )
                )
                account = result.scalar_one_or_none()
                
                if not account:
                    raise ValueError("Account not found")
                
                # Get valid credentials to revoke token
                credentials = await self.get_valid_credentials(account)
                
                if credentials and credentials.token:
                    # Revoke the token with Google
                    try:
                        async with httpx.AsyncClient() as client:
                            response = await client.post(
                                "https://oauth2.googleapis.com/revoke",
                                params={"token": credentials.token},
                                headers={"Content-Type": "application/x-www-form-urlencoded"}
                            )
                            if response.status_code != 200:
                                logger.warning(f"Failed to revoke token with Google: {response.text}")
                    except Exception as e:
                        logger.warning(f"Error revoking token with Google: {str(e)}")
                
                # Update account status
                await session.execute(
                    update(GoogleAccount)
                    .where(GoogleAccount.id == account_id)
                    .values(
                        status=GoogleAccountStatus.DISCONNECTED.value,
                        access_token=None,
                        refresh_token=None,
                        token_expires_at=None
                    )
                )
                await session.commit()
                
                logger.info(f"Successfully disconnected Google account {account.email}")
                return True
                
        except Exception as e:
            logger.error(f"Error disconnecting Google account: {str(e)}")
            raise ValueError(f"Failed to disconnect account: {str(e)}")
    
    async def get_account_status(self, tenant_id: str) -> List[Dict[str, Any]]:
        """
        Get status of all Google accounts for a tenant
        
        Args:
            tenant_id: Tenant ID
            
        Returns:
            List of account status dictionaries
        """
        try:
            async with get_async_session() as session:
                result = await session.execute(
                    select(GoogleAccount)
                    .where(GoogleAccount.tenant_id == tenant_id)
                    .order_by(GoogleAccount.created_at.desc())
                )
                accounts = result.scalars().all()
                
                status_list = []
                for account in accounts:
                    status_list.append({
                        "id": str(account.id),
                        "email": account.email,
                        "display_name": account.display_name,
                        "status": account.status,
                        "last_sync_at": account.last_sync_at.isoformat() if account.last_sync_at else None,
                        "connected_at": account.connected_at.isoformat(),
                        "is_token_expired": account.is_token_expired,
                        "error_count": account.error_count,
                        "last_error": account.last_error,
                        "granted_scopes": account.granted_scopes,
                        "location_count": len(account.locations) if hasattr(account, 'locations') else 0
                    })
                
                return status_list
                
        except Exception as e:
            logger.error(f"Error getting account status for tenant {tenant_id}: {str(e)}")
            raise ValueError(f"Failed to get account status: {str(e)}")
    
    async def _get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting user info from Google: {str(e)}")
            raise ValueError(f"Failed to get user info: {str(e)}")
    
    async def _save_google_account(
        self, 
        tenant_id: str, 
        credentials: Credentials, 
        user_info: Dict[str, Any]
    ) -> GoogleAccount:
        """Save or update Google account in database"""
        try:
            async with get_async_session() as session:
                # Check if account already exists
                result = await session.execute(
                    select(GoogleAccount)
                    .where(
                        GoogleAccount.tenant_id == tenant_id,
                        GoogleAccount.google_account_id == user_info['id']
                    )
                )
                account = result.scalar_one_or_none()
                
                # Encrypt tokens
                encrypted_access_token = self.cipher.encrypt(credentials.token.encode()).decode()
                encrypted_refresh_token = None
                if credentials.refresh_token:
                    encrypted_refresh_token = self.cipher.encrypt(credentials.refresh_token.encode()).decode()
                
                if account:
                    # Update existing account
                    account.access_token = encrypted_access_token
                    account.refresh_token = encrypted_refresh_token
                    account.token_expires_at = credentials.expiry
                    account.status = GoogleAccountStatus.CONNECTED.value
                    account.granted_scopes = list(credentials.granted_scopes) if credentials.granted_scopes else []
                    account.error_count = 0
                    account.last_error = None
                    account.email = user_info['email']
                    account.display_name = user_info.get('name')
                else:
                    # Create new account
                    account = GoogleAccount(
                        tenant_id=tenant_id,
                        google_account_id=user_info['id'],
                        email=user_info['email'],
                        display_name=user_info.get('name'),
                        access_token=encrypted_access_token,
                        refresh_token=encrypted_refresh_token,
                        token_expires_at=credentials.expiry,
                        status=GoogleAccountStatus.CONNECTED.value,
                        granted_scopes=list(credentials.granted_scopes) if credentials.granted_scopes else []
                    )
                    session.add(account)
                
                await session.commit()
                await session.refresh(account)
                return account
                
        except Exception as e:
            logger.error(f"Error saving Google account: {str(e)}")
            raise ValueError(f"Failed to save account: {str(e)}")
    
    async def _mark_account_expired(self, account: GoogleAccount):
        """Mark account as expired"""
        try:
            async with get_async_session() as session:
                await session.execute(
                    update(GoogleAccount)
                    .where(GoogleAccount.id == account.id)
                    .values(
                        status=GoogleAccountStatus.EXPIRED.value,
                        last_error="Refresh token expired or invalid"
                    )
                )
                await session.commit()
        except Exception as e:
            logger.error(f"Error marking account as expired: {str(e)}")


# Service instance
google_auth_service = GoogleAuthService()