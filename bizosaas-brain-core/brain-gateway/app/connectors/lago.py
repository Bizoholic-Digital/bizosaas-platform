import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..ports.billing_port import BillingPort, Customer, Subscription, SubscriptionPlan, Invoice, Wallet, WalletTransaction
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class LagoConnector(BaseConnector, BillingPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="lago",
            name="Lago Billing",
            type=ConnectorType.OTHER, # Maybe add BILLING type later
            description="Open Source Metering and Usage-Based Billing.",
            icon="lago",
            version="1.0.0",
            auth_schema={
                "api_url": {"type": "string", "label": "API URL", "default": "http://lago-api:3000"},
                "api_key": {"type": "string", "label": "API Key"}
            }
        )

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.credentials.get('api_key')}",
            "Content-Type": "application/json"
        }

    def _get_api_url(self, path: str) -> str:
        base_url = self.credentials.get("api_url", "http://lago-api:3000").rstrip("/")
        # Lago API usually starts with /api/v1
        return f"{base_url}/api/v1/{path.lstrip('/')}"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self._get_api_url("organizations"),
                    headers=self._get_headers(),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Lago validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    # --- BillingPort Implementation ---

    async def create_customer(self, customer: Customer) -> Customer:
        # Lago expects 'customer' object wrapping params
        payload = {
            "customer": {
                "external_id": customer.id, # Must provide external ID
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "currency": customer.currency,
                "metadata": [
                    {"key": k, "value": str(v)} 
                    for k, v in customer.metadata.items()
                ]
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("customers"),
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json().get("customer", {})
            return self._map_customer(data)

    async def get_customer(self, customer_id: str) -> Optional[Customer]:
        # customer_id here is the external_id passed to Lago
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url(f"customers/{customer_id}"),
                    headers=self._get_headers()
                )
                if response.status_code == 404: return None
                response.raise_for_status()
                data = response.json().get("customer", {})
                return self._map_customer(data)
            except Exception:
                return None

    async def create_customer(self, customer: Customer) -> Customer:
        """
        Register a new customer in Lago.
        """
        payload = {
            "customer": {
                "external_id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "currency": customer.currency or "USD",
                "phone": customer.phone,
                "address_line1": customer.metadata.get("address") if customer.metadata else None
            }
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url("customers"),
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                data = response.json().get("customer", {})
                return self._map_customer(data)
            except Exception as e:
                logger.error(f"Failed to create Lago customer: {e}")
                return None

    def _map_customer(self, data: Dict[str, Any]) -> Customer:
        # Lago returns metadata as list of objects
        meta = {}
        if "metadata" in data:
            for m in data["metadata"]:
                meta[m["key"]] = m["value"]
                
        return Customer(
            id=data.get("external_id"),
            email=data.get("email"),
            name=data.get("name"),
            phone=data.get("phone"),
            currency=data.get("currency"),
            metadata=meta
        )

    async def get_plans(self) -> List[SubscriptionPlan]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("plans"),
                headers=self._get_headers(),
                params={"per_page": 100}
            )
            response.raise_for_status()
            data = response.json().get("plans", [])
            return [
                SubscriptionPlan(
                    id=p["lago_id"], # Internal UUID
                    name=p["name"],
                    code=p["code"],
                    amount=float(p.get("amount_cents", 0) / 100),
                    currency=p.get("amount_currency"),
                    interval=p.get("interval"),
                    trial_period_days=p.get("trial_period")
                ) for p in data
            ]

    async def create_subscription(self, customer_id: str, plan_code: str) -> Subscription:
        payload = {
            "subscription": {
                "external_customer_id": customer_id,
                "plan_code": plan_code,
                "external_id": f"sub_{customer_id}_{int(datetime.now().timestamp())}" 
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("subscriptions"),
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json().get("subscription", {})
            return self._map_subscription(data)

    def _map_subscription(self, data: Dict[str, Any]) -> Subscription:
        return Subscription(
            id=data.get("external_id"),
            customer_id=data.get("external_customer_id"),
            plan_id=data.get("plan_code"),
            status=data.get("status"),
            current_period_start=datetime.fromisoformat(data.get("subscription_at").replace('Z', '+00:00')), # Approximate
            current_period_end=datetime.now() # Lago doesn't always send end date in simple object?
        )

    async def cancel_subscription(self, subscription_id: str) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self._get_api_url(f"subscriptions/{subscription_id}"),
                headers=self._get_headers()
            )
            return response.status_code == 200

    async def get_customer_subscriptions(self, customer_id: str) -> List[Subscription]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("subscriptions"),
                headers=self._get_headers(),
                params={"external_customer_id": customer_id}
            )
            data = response.json().get("subscriptions", [])
            return [self._map_subscription(s) for s in data]

    async def get_customer_invoices(self, customer_id: str) -> List[Invoice]:
         async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("invoices"),
                headers=self._get_headers(),
                params={"external_customer_id": customer_id}
            )
            data = response.json().get("invoices", [])
            return [
                Invoice(
                    id=i["lago_id"],
                    customer_id=customer_id,
                    amount_due=float(i.get("amount_cents", 0) / 100),
                    currency=i.get("amount_currency"),
                    status=i.get("status"),
                    created_at=datetime.fromisoformat(i.get("issuing_date") + "T00:00:00")
                ) for i in data
            ]

    # --- New Usage/Metering Methods ---

    async def track_event(self, customer_id: str, code: str, properties: Optional[Dict[str, Any]] = None) -> bool:
        """
        Record a metering event in Lago.
        """
        payload = {
            "event": {
                "transaction_id": f"event_{customer_id}_{int(datetime.now().timestamp())}",
                "external_customer_id": customer_id,
                "code": code,
                "properties": properties or {}
            }
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self._get_api_url("events"),
                    headers=self._get_headers(),
                    json=payload
                )
                return response.status_code == 200 or response.status_code == 202
            except Exception as e:
                logger.error(f"Failed to track Lago event: {e}")
                return False

    async def get_usage(self, customer_id: str, subscription_id: str) -> Dict[str, Any]:
        """
        Fetch current usage for a specific subscription.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url(f"subscriptions/{subscription_id}/usage"),
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json().get("customer_usage", {})
            except Exception as e:
                logger.error(f"Failed to fetch Lago usage: {e}")
                return {}

    # --- Wallet Management Implementation ---

    async def create_wallet(self, customer_id: str, name: str, currency: str, rate_amount: float = 1.0) -> Wallet:
        payload = {
            "wallet": {
                "external_customer_id": customer_id,
                "name": name,
                "currency": currency,
                "rate_amount": str(rate_amount) # Usually 1.0 for 1:1 currency match
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("wallets"),
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json().get("wallet", {})
            return self._map_wallet(data)

    async def get_wallet_balance(self, customer_id: str) -> Optional[Wallet]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url("wallets"),
                    headers=self._get_headers(),
                    params={"external_customer_id": customer_id}
                )
                response.raise_for_status()
                # Assuming first wallet found
                wallets = response.json().get("wallets", [])
                if not wallets: return None
                return self._map_wallet(wallets[0])
            except Exception:
                return None

    async def top_up_wallet(self, wallet_id: str, amount: float) -> WalletTransaction:
        payload = {
            "wallet_transaction": {
                "wallet_id": wallet_id,
                "paid_credits": str(amount),
                "granted_credits": "0.0" # Grant credits are bonus
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("wallet_transactions"),
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            # Lago returns a list of transactions sometimes or a single one depending on version
            data = response.json().get("wallet_transactions", [{}])[0]
            return WalletTransaction(
                id=data.get("lago_id"),
                wallet_id=wallet_id,
                amount=float(data.get("amount_cents", 0) / 100),
                type="inbound", # Top-up is inbound
                status=data.get("status"),
                created_at=datetime.now()
            )

    def _map_wallet(self, data: Dict[str, Any]) -> Wallet:
        return Wallet(
            id=data.get("lago_id"),
            customer_id=data.get("external_customer_id"),
            balance=float(data.get("credits_balance", 0)),
            consumed_credits=float(data.get("consumed_credits", 0)),
            currency=data.get("currency"),
            status=data.get("status"),
            expiration_at=datetime.fromisoformat(data["expiration_at"].replace('Z', '+00:00')) if data.get("expiration_at") else None
        )
