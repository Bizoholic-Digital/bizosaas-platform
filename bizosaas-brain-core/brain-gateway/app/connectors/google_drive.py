import httpx
import os
from typing import Dict, Any, Optional, List
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .oauth_mixin import OAuthMixin
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class GoogleDriveConnector(BaseConnector, OAuthMixin):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-drive",
            name="Google Drive",
            type=ConnectorType.OTHER,
            description="Access and manage files in Google Drive.",
            icon="google-drive",
            version="1.0.0",
            auth_schema={
                "access_token": {"type": "string", "label": "Access Token", "format": "password"},
                "refresh_token": {"type": "string", "label": "Refresh Token", "format": "password", "help": "Required for offline access"},
                "expires_at": {"type": "number", "label": "Expires At (timestamp)"}
            }
        )

    async def _get_access_token(self) -> str:
        """
        Retrieves a valid access token. 
        If a refresh_token is present, it will attempt to refresh the access token.
        """
        # Simple case for testing or if token is explicitly managed
        if self.credentials.get("access_token") and not self.credentials.get("expires_at"):
             return self.credentials.get("access_token")

        # Refresh token flow if refresh_token and client_id/secret are available
        if self.credentials.get("refresh_token"):
            try:
                # Check for environment variables (standard BizOSaaS pattern)
                client_id = os.getenv("GOOGLE_DRIVE_CLIENT_ID") or os.getenv("GOOGLE_CLIENT_ID")
                client_secret = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET") or os.getenv("GOOGLE_CLIENT_SECRET")
                
                if client_id and client_secret:
                    token_data = await self.refresh_token(self.credentials.get("refresh_token"))
                    self.credentials["access_token"] = token_data.get("access_token")
                    if "expires_in" in token_data:
                        import time
                        self.credentials["expires_at"] = int(time.time()) + token_data["expires_in"]
                    return self.credentials["access_token"]
            except Exception as e:
                self.logger.error(f"Failed to refresh Google Drive access token: {e}")
        
        if self.credentials.get("access_token"):
            return self.credentials.get("access_token")

        raise ValueError("No valid access_token or refresh_token found in credentials.")

    async def validate_credentials(self) -> bool:
        try:
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/drive/v3/about?fields=user",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch data from Google Drive.
        resource_type: 'files', 'folders'
        """
        token = await self._get_access_token()
        params = params or {}
        
        # Google Drive API v3
        url = "https://www.googleapis.com/drive/v3/files"
        
        if resource_type.lower() == 'folders':
             # If q is already provided, we might want to append to it
            q = "mimeType = 'application/vnd.google-apps.folder'"
            if params.get("q"):
                params["q"] = f"({params['q']}) and {q}"
            else:
                params["q"] = q
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "data": data.get("files", []),
                "meta": {
                    "nextPageToken": data.get("nextPageToken"),
                    "kind": data.get("kind")
                }
            }

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute actions on Google Drive.
        action: 'create_folder', 'upload_file'
        """
        token = await self._get_access_token()
        
        if action == "create_folder":
            name = payload.get("name")
            parent_id = payload.get("parent_id")
            
            if not name:
                raise ValueError("Folder name is required")
                
            metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder"
            }
            if parent_id:
                metadata["parents"] = [parent_id]
                
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://www.googleapis.com/drive/v3/files",
                    headers={"Authorization": f"Bearer {token}"},
                    json=metadata,
                    timeout=30.0
                )
                response.raise_for_status()
                return {"status": "success", "data": response.json()}

        if action == "upload_file":
            # This is a basic implementation. For large files, we'd need resumable uploads.
            name = payload.get("name")
            content = payload.get("content") # Base64 or string
            parent_id = payload.get("parent_id")
            mime_type = payload.get("mime_type", "application/octet-stream")
            
            if not name or not content:
                raise ValueError("Name and content are required")
                
            # Multipart upload
            metadata = {"name": name}
            if parent_id:
                metadata["parents"] = [parent_id]
                
            # For simplicity in this direct connector, we'll assume content is small
            # and passed directly. Real production use would use formal file objects.
            files = {
                'metadata': (None, bytes(str(metadata), 'utf-8'), 'application/json'),
                'file': (name, content, mime_type)
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                    headers={"Authorization": f"Bearer {token}"},
                    files=files,
                    timeout=60.0
                )
                response.raise_for_status()
                return {"status": "success", "data": response.json()}
                
        raise NotImplementedError(f"Action {action} not implemented for Google Drive")

    # OAuthMixin Implementation
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        scope = "https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata.readonly"
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}&"
            f"state={state}&"
            f"access_type=offline&"
            f"prompt=consent"
        )
    
    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data)
            resp.raise_for_status()
            return resp.json()
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "refresh_token": refresh_token,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "grant_type": "refresh_token"
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, data=data)
            resp.raise_for_status()
            return resp.json()
