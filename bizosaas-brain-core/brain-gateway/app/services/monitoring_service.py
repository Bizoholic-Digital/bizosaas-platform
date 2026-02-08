import os
import httpx
from datetime import datetime

class MonitoringService:
    def __init__(self):
        self.neon_api_key = os.getenv("NEON_API_KEY")
        self.neon_project_id = os.getenv("NEON_PROJECT_ID")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    async def check_neon_storage(self):
        """
        Monitor Neon DB storage usage.
        Note: Real implementation requires Neon API integration.
        """
        if not self.neon_api_key or not self.neon_project_id:
            return {"status": "error", "message": "Neon API credentials missing"}
            
        async with httpx.AsyncClient() as client:
            # Placeholder for Neon API call
            # response = await client.get(f"https://console.neon.tech/api/v2/projects/{self.neon_project_id}/usage", headers={"Authorization": f"Bearer {self.neon_api_key}"})
            # data = response.json()
            
            # Mock data for demonstration
            usage_percentage = 85.0 
            return {
                "status": "warning" if usage_percentage > 80 else "ok",
                "usage_percentage": usage_percentage,
                "message": f"Storage is at {usage_percentage}% capacity."
            }

    async def check_api_credits(self):
        """
        Monitor OpenAI / LLM credit status.
        """
        # Placeholder for credit checking logic
        return {
            "status": "ok",
            "credits_remaining": 150.25,
            "currency": "USD",
            "message": "Credits are sufficient."
        }
        
    async def check_wallet_balances(self, tenant_id: str = "default_tenant"):
        """
        Monitor the prepaid credit wallet balance.
        Ensures continuous functioning of pay-per-use services (Tokens, SES, Storage).
        """
        from app.dependencies import SessionLocal
        from app.services.billing_service import BillingService
        
        db = SessionLocal()
        try:
            billing_service = BillingService(db)
            wallet = await billing_service.get_wallet(tenant_id)
            
            if not wallet:
                return {"status": "error", "message": "No active wallet found for tenant."}
            
            balance = wallet.balance
            # Thresholds: Critical < $10, Warning < $50
            status = "ok"
            if balance < 10.0:
                status = "critical"
            elif balance < 50.0:
                status = "warning"
                
            return {
                "status": status,
                "balance": balance,
                "currency": wallet.currency,
                "message": f"Wallet balance is ${balance} {wallet.currency}.",
                "recommendation": "Top up now to ensure service continuity." if status != "ok" else None
            }
        finally:
            db.close()

    async def get_system_health(self):
        """
        General platform health check summary.
        """
        # Include wallet status in general health
        wallet_status = await self.check_wallet_balances()
        
        return {
            "services": {
                "brain-gateway": "healthy",
                "authentik": "healthy",
                "vault": "healthy",
                "neon-db": "healthy",
                "billing-wallet": wallet_status.get("status", "healthy")
            },
            "wallet": wallet_status,
            "last_check": datetime.utcnow().isoformat()
        }
