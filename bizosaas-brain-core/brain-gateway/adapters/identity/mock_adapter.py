from typing import Optional, Dict
from domain.ports.identity_port import IdentityPort, AuthenticatedUser

class MockIdentityAdapter(IdentityPort):
    """
    Mock Identity Adapter for local development or when Auth is disabled.
    """
    async def validate_token(self, token: str) -> bool:
        return True

    async def get_user_from_token(self, token: str) -> Optional[AuthenticatedUser]:
        return AuthenticatedUser(
            id="dev-user-id",
            email="dev@bizoholic.net",
            name="dev_admin",
            roles=["Super Admin", "Admin"],
            tenant_id="default_tenant"
        )

    async def has_permission(self, user: AuthenticatedUser, permission: str) -> bool:
        """Mock permission check - always returns True for admin roles"""
        if "Admin" in user.roles or "Super Admin" in user.roles:
            return True
        return permission in user.permissions

    async def get_login_url(self, state: str) -> str:
        return "http://localhost:3000/mock-login"

    async def exchange_code(self, code: str) -> Dict:
        return {"access_token": "mock-token", "id_token": "mock-id-token"}
