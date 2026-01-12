from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class AuthenticatedUser:
    """Domain Entity for authenticated user."""
    id: str
    email: str
    name: str  # Display name
    roles: List[str] = field(default_factory=list)  # Maps to Groups
    tenant_id: Optional[str] = None
    permissions: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict) # Extra profile data
    
    @property
    def role(self) -> str:
        """Helper to get primary role as a standardized string for backward compatibility."""
        if not self.roles:
            return "user"
        # Standardize: "Super Admin" -> "super_admin", "Admin" -> "admin"
        return self.roles[0].lower().replace(" ", "_")

class IdentityPort(ABC):
    """Port (Interface) for Identity operations.
    
    The Domain Core depends ONLY on this interface.
    Adapters (Authentik, Keycloak, etc.) implement this.
    """
    
    @abstractmethod
    async def validate_token(self, token: str) -> bool:
        """Validate if a token is valid, active, and not expired."""
        pass
    
    @abstractmethod
    async def get_user_from_token(self, token: str) -> Optional[AuthenticatedUser]:
        """Extract user information from a valid token using Introspection or UserInfo."""
        pass
    
    @abstractmethod
    async def has_permission(self, user: AuthenticatedUser, permission: str) -> bool:
        """Check if user has a specific permission (RBAC/ABAC)."""
        pass
    
    @abstractmethod
    async def update_user_metadata(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """Update user's public metadata."""
        pass
