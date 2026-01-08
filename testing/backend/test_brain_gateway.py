"""
Brain Gateway API Unit Tests - Optimized for Hexagonal Architecture
Tests: UNIT-001 through UNIT-007
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from uuid import uuid4, UUID
from datetime import datetime, timedelta

# Import domain ports and entities
from domain.ports.identity_port import AuthenticatedUser, IdentityPort
from app.models.campaign import Campaign, CampaignStatus
from app.models.user import User

class TestIdentityPort:
    """UNIT-001: Identity Port and Adapter tests"""
    
    @pytest.mark.asyncio
    async def test_mock_identity_adapter(self):
        """Test the MockIdentityAdapter functionality"""
        from adapters.identity.mock_adapter import MockIdentityAdapter
        
        adapter = MockIdentityAdapter()
        token = "some-token"
        
        # Test validation
        is_valid = await adapter.validate_token(token)
        assert is_valid is True
        
        # Test user extraction
        user = await adapter.get_user_from_token(token)
        assert isinstance(user, AuthenticatedUser)
        assert user.email == "dev@bizoholic.net"
        assert "Admin" in user.roles

    @pytest.mark.asyncio
    async def test_clerk_adapter_mock(self):
        """Test ClerkAdapter with mocked clerk backend"""
        from adapters.identity.clerk_adapter import ClerkAdapter
        
        with patch('adapters.identity.clerk_adapter.Clerk') as mock_clerk:
            # Setup mock
            mock_instance = mock_clerk.return_value
            mock_instance.users.get.return_value = Mock(
                id="user_123",
                primary_email_address_id="email_123",
                email_addresses=[Mock(id="email_123", email_address="test@example.com")],
                first_name="Test",
                last_name="User",
                public_metadata={"roles": ["client"], "tenant_id": "tenant_123"}
            )
            
            adapter = ClerkAdapter(issuer="https://clerk.test")
            
            # Since we can't easily mock the JWT verification without a real key,
            # we focus on the mapping logic if it's accessible or the structure.
            assert adapter.issuer == "https://clerk.test"

class TestCampaignService:
    """UNIT-005: Campaign Service business logic"""
    
    def test_create_campaign(self):
        """Test campaign creation in service"""
        from app.services.campaign_service import CampaignService
        
        mock_db = Mock()
        service = CampaignService(mock_db)
        
        tenant_id = uuid4()
        user_id = uuid4()
        name = "Summer Sale"
        goal = "Increase conversions"
        
        campaign = service.create_campaign(tenant_id, name, goal, user_id)
        
        assert campaign.name == name
        assert campaign.tenant_id == tenant_id
        assert campaign.status == CampaignStatus.DRAFT
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_list_campaigns(self):
        """Test listing campaigns for a tenant"""
        from app.services.campaign_service import CampaignService
        
        mock_db = Mock()
        tenant_id = uuid4()
        
        # Mocking the query chain: db.query(Model).filter(...).order_by(...).all()
        mock_query = mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_order = mock_filter.order_by.return_value
        mock_order.all.return_value = [Campaign(name="C1"), Campaign(name="C2")]
        
        service = CampaignService(mock_db)
        results = service.list_campaigns(tenant_id)
        
        assert len(results) == 2
        mock_db.query.assert_called_with(Campaign)

class TestDependencies:
    """UNIT-003: Dependency injection and Auth logic"""
    
    @pytest.mark.asyncio
    async def test_get_current_user_disabled_auth(self):
        """Test get_current_user when auth is disabled"""
        from app.dependencies import get_current_user
        
        with patch.dict('os.environ', {'DISABLE_AUTH': 'true'}):
            user = await get_current_user(None)
            assert user.id == "00000000-0000-0000-0000-000000000001"
            assert "admin" in user.roles

    @pytest.mark.asyncio
    async def test_require_role_success(self):
        """Test role requirement decorator success"""
        from app.dependencies import require_role
        
        mock_user = AuthenticatedUser(
            id="u1", email="e1", name="n1", roles=["manager"]
        )
        
        # require_role returns a decorator
        role_checker = require_role(["manager", "editor"])
        
        # This should execute without raising
        result = await role_checker(mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_require_role_failure(self):
        """Test role requirement decorator failure"""
        from app.dependencies import require_role
        from fastapi import HTTPException
        
        mock_user = AuthenticatedUser(
            id="u1", email="e1", name="n1", roles=["viewer"]
        )
        
        role_checker = require_role(["admin", "manager"])
        
        with pytest.raises(HTTPException) as excinfo:
            await role_checker(mock_user)
        
        assert excinfo.value.status_code == 403

class TestBillingAPI:
    """UNIT-006: Billing API logic"""
    
    def test_billing_data_structure(self):
        """Verify the billing endpoint can be imported and has expected components"""
        # Primarily checking if the module exists and imports
        from app.api import billing
        assert hasattr(billing, 'router')

class TestAgentService:
    """UNIT-005: Agent Orchestration tests"""
    
    def test_agent_optimizations_query(self):
        """Test agent service static query method"""
        from app.services.agent_service import AgentService
        
        mock_db = Mock()
        AgentService.get_agent_optimizations(mock_db, "agent_123")
        
        mock_db.query.assert_called()

class TestConnectors:
    """UNIT-007: Connector logic and base classes"""
    
    def test_base_connector_structure(self):
        """Verify base connector exists"""
        from app.connectors.base import BaseConnector
        # Type check or structure check
        assert BaseConnector is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
