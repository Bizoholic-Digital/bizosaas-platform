from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import User, Tenant

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def promote_to_partner(self, user_id: UUID) -> User:
        """Promote a user to partner role."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        user.role = "partner"
        self.db.commit()
        self.db.refresh(user)
        return user

    def demote_to_client(self, user_id: UUID) -> User:
        """Demote a partner to client role and remove managed tenants."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        user.role = "client" 
        # Clear managed tenants as they are no longer a partner
        user.managed_tenants = []
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def assign_client_to_partner(self, partner_id: UUID, tenant_id: UUID) -> User:
        """Assign a client tenant to a partner."""
        partner = self.db.query(User).filter(User.id == partner_id).first()
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        
        if not partner:
            raise ValueError("Partner not found")
        if not tenant:
            raise ValueError("Tenant not found")
            
        if partner.role != "partner" and partner.role != "admin" and partner.role != "super_admin":
             raise ValueError("User is not a partner")

        if tenant not in partner.managed_tenants:
            partner.managed_tenants.append(tenant)
            self.db.commit()
            self.db.refresh(partner)
            
        return partner

    def remove_client_from_partner(self, partner_id: UUID, tenant_id: UUID) -> User:
        """Remove a client tenant from a partner's management."""
        partner = self.db.query(User).filter(User.id == partner_id).first()
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        
        if not partner:
            raise ValueError("Partner not found")
        if not tenant:
            raise ValueError("Tenant not found")

        if tenant in partner.managed_tenants:
            partner.managed_tenants.remove(tenant)
            self.db.commit()
            self.db.refresh(partner)
            
        return partner

    def get_managed_clients(self, partner_id: UUID):
        """Get all tenants managed by a partner."""
        partner = self.db.query(User).filter(User.id == partner_id).first()
        if not partner:
            raise ValueError("Partner not found")
            
        return partner.managed_tenants
