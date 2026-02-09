import os
import razorpay
from typing import List, Optional, Union, Any
from sqlalchemy.orm import Session
from app.models.billing import SubscriptionPlan, Subscription, Invoice, UsageEvent
from app.models.user import Tenant
from app.store import active_connectors
from app.connectors.registry import ConnectorRegistry
from app.ports.billing_port import BillingPort, Customer, Subscription as PortSubscription, SubscriptionPlan as PortPlan
from datetime import datetime, timedelta
import uuid

class BillingService:
    def __init__(self, db: Session):
        self.db = db
        self.key_id = os.getenv("RAZORPAY_KEY_ID")
        self.key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        self.razorpay_client = None
        if self.key_id and self.key_secret:
            self.razorpay_client = razorpay.Client(auth=(self.key_id, self.key_secret))

    def _get_lago_connector(self, tenant_id: str) -> Optional[BillingPort]:
        # Check active connectors for Lago
        try:
            conn_path = f"{tenant_id}:lago"
            if conn_path in active_connectors:
                config = active_connectors[conn_path]
                return ConnectorRegistry.create_connector("lago", tenant_id, config["credentials"])
            
            # Fallback to default if available
            if "default_tenant:lago" in active_connectors:
                config = active_connectors["default_tenant:lago"]
                return ConnectorRegistry.create_connector("lago", "default_tenant", config["credentials"])
        except Exception as e:
            print(f"Error creating Lago connector: {e}")
        return None

    async def get_plans(self) -> Union[List[SubscriptionPlan], List[PortPlan]]:
        lago = self._get_lago_connector("default_tenant")
        if lago:
            try:
                return await lago.get_plans()
            except Exception as e:
                print(f"Lago error fetching plans: {e}")
        
        return self.db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()

    async def create_subscription(self, tenant_id: str, plan_slug: str, email: str = None, name: str = None) -> Union[Subscription, PortSubscription]:
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                # Ensure customer exists in Lago
                tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
                customer = await lago.get_customer(tenant_id)
                if not customer:
                    customer = await lago.create_customer(Customer(
                        id=tenant_id,
                        email=email or f"admin@{tenant.slug}.com",
                        name=name or tenant.name
                    ))
                
                return await lago.create_subscription(tenant_id, plan_slug)
            except Exception as e:
                print(f"Lago error creating subscription: {e}")
                # Fallback to internal

        plan = self.db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == plan_slug).first()
        if not plan:
            raise ValueError("Plan not found")

        existing = self.db.query(Subscription).filter(
            Subscription.tenant_id == tenant_id,
            Subscription.status == "active"
        ).first()
        
        if existing:
            return existing

        now = datetime.utcnow()
        end_date = now + timedelta(days=30)
        
        gateway_sub_id = None
        if self.razorpay_client:
            try:
                rz_plan_id = plan.features.get("rz_plan_id", "plan_placeholder")
                rz_sub = self.razorpay_client.subscription.create({
                    "plan_id": rz_plan_id,
                    "customer_notify": 1,
                    "total_count": 12,
                    "notes": {"tenant_id": tenant_id}
                })
                gateway_sub_id = rz_sub['id']
            except Exception as e:
                print(f"Razorpay Error: {e}")
        
        new_sub = Subscription(
            tenant_id=tenant_id,
            plan_id=plan.id,
            status="active" if not gateway_sub_id else "created",
            current_period_start=now,
            current_period_end=end_date,
            gateway="razorpay" if gateway_sub_id else "internal",
            gateway_subscription_id=gateway_sub_id
        )
        
        self.db.add(new_sub)
        self.db.commit()
        self.db.refresh(new_sub)
        
        tenant = self.db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant:
            tenant.subscription_plan = plan.slug
            tenant.subscription_status = new_sub.status
            self.db.commit()

        return new_sub

    async def get_tenant_subscription(self, tenant_id: str) -> Optional[Union[Subscription, PortSubscription]]:
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                subs = await lago.get_customer_subscriptions(tenant_id)
                if subs:
                    return subs[0]
            except Exception as e:
                print(f"Lago error getting subscription: {e}")

        return self.db.query(Subscription).filter(
            Subscription.tenant_id == tenant_id
        ).order_by(Subscription.created_at.desc()).first()

    async def list_invoices(self, tenant_id: str) -> Union[List[Invoice], List[Invoice]]:
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                return await lago.get_customer_invoices(tenant_id)
            except Exception as e:
                print(f"Lago error listing invoices: {e}")

        return self.db.query(Invoice).filter(Invoice.tenant_id == tenant_id).all()

    # --- Wallet Management ---

    async def get_wallet(self, tenant_id: str) -> Optional[Any]:
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                return await lago.get_wallet_balance(tenant_id)
            except Exception as e:
                print(f"Lago error getting wallet: {e}")
        return None

    async def create_wallet(self, tenant_id: str, name: str = "Primary Wallet", currency: str = "USD") -> Optional[Any]:
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                return await lago.create_wallet(tenant_id, name, currency)
            except Exception as e:
                print(f"Lago error creating wallet: {e}")
        return None

    async def create_customer(self, tenant_id: str, name: str, email: str, currency: str = "USD") -> Optional[Customer]:
        """
        Create a new customer in the billing system.
        """
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                customer = Customer(
                    id=str(tenant_id),
                    name=name,
                    email=email,
                    currency=currency
                )
                return await lago.create_customer(customer)
            except Exception as e:
                print(f"Lago error creating customer: {e}")
        return None

    async def top_up_wallet(self, tenant_id: str, wallet_id: str, amount: float) -> Optional[Any]:
        lago = self._get_lago_connector(tenant_id)
        if lago:
            try:
                # In a real scenario, we'd process payment via Stripe/Razorpay first
                return await lago.top_up_wallet(wallet_id, amount)
            except Exception as e:
                print(f"Lago error topping up wallet: {e}")
        return None

    def track_usage(self, tenant_id: str, event_type: str, quantity: int = 1, properties: dict = None):
        # In Lago, we'd send an event here
        lago = self._get_lago_connector(tenant_id)
        if lago:
            import asyncio
            # Using fire-and-forget for usage tracking to avoid blocking
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(lago.track_event(tenant_id, event_type, properties))
            except Exception as e:
                print(f"Failed to track Lago event via fire-and-forget: {e}")

        # For now, keep internal tracking too
        event = UsageEvent(
            tenant_id=tenant_id,
            event_type=event_type,
            quantity=quantity,
            properties=properties
        )
        self.db.add(event)
        self.db.commit()
