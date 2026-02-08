import asyncio
import os
import sys
import uuid
from sqlalchemy.orm import Session
from app.dependencies import SessionLocal
from app.services.billing_service import BillingService
from app.models.user import Tenant
from app.store import active_connectors
from app.ports.billing_port import Customer

async def initialize_tenants_and_wallets():
    print("🚀 Starting Comprehensive Tenant & Billing Onboarding...")
    
    db = SessionLocal()
    billing_service = BillingService(db)
    
    # 0. Inject Lago Credentials (bypassing registry for script context)
    # Using a common 'system' tenant ID or a placeholder for the connector config
    LAGO_CONFIG = {
        "connector_id": "lago",
        "credentials": {
            "api_url": "https://billing-api.bizoholic.net",
            "api_key": "d9ec66e8-f5e3-4314-8ed4-677f55da013a"
        }
    }
    
    # Primary tenants to onboard
    primary_tenants_data = [
        {"slug": "thrillring", "name": "Thrillring Gaming", "domain": "thrillring.com", "email": "billing@thrillring.com"},
        {"slug": "coreldove", "name": "Coreldove Wellness", "domain": "coreldove.com", "email": "billing@coreldove.com"},
        {"slug": "bizoholic", "name": "Bizoholic Agency (Internal)", "domain": "bizoholic.com", "email": "billing@bizoholic.com"}
    ]
    
    for data in primary_tenants_data:
        # 1. Check/Create Tenant in Database
        tenant = db.query(Tenant).filter(Tenant.slug == data["slug"]).first()
        if not tenant:
            print(f"➕ Creating Tenant in DB: {data['name']}...")
            tenant = Tenant(
                id=uuid.uuid4(),
                name=data["name"],
                slug=data["slug"],
                domain=data["domain"],
                status="active"
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            print(f"✅ Created Tenant in DB: {tenant.id}")
        else:
            print(f"📦 Tenant {data['name']} already exists in DB: {tenant.id}")

        # Inject config for THIS tenant so BillingService can find it
        active_connectors[f"{tenant.id}:lago"] = LAGO_CONFIG

        # 2. Check/Create Customer in Lago
        print(f"📦 Checking Lago Customer for {tenant.name}...")
        # We need a connector instance to check directly or use high-level service
        lago = billing_service._get_lago_connector(str(tenant.id))
        if not lago:
            print(f"❌ Failed to initialize Lago connector for {tenant.name}")
            continue
            
        lago_customer = await lago.get_customer(str(tenant.id))
        if not lago_customer:
            print(f"➕ Registering Customer in Lago...")
            lago_customer = await billing_service.create_customer(
                tenant_id=tenant.id,
                name=tenant.name,
                email=data["email"]
            )
            if lago_customer:
                print(f"✅ Registered in Lago: {lago_customer.id}")
            else:
                print(f"❌ Failed to register in Lago for {tenant.name}")
                continue
        else:
            print(f"✅ Customer already exists in Lago.")

        # 3. Check/Create Wallet in Lago
        wallet = await billing_service.get_wallet(str(tenant.id))
        if wallet:
            print(f"✅ Wallet already exists for {tenant.name}. Balance: {wallet.balance}")
        else:
            print(f"➕ Creating wallet for {tenant.name}...")
            new_wallet = await billing_service.create_wallet(
                tenant_id=str(tenant.id),
                name=f"{data['name']} Primary Wallet",
                currency="USD"
            )
            if new_wallet:
                print(f"🎉 Created wallet: {new_wallet.id}")
            else:
                print(f"❌ Failed to create wallet for {tenant.name}")

    db.close()
    print("🏁 Onboarding and Wallet initialization completed.")

if __name__ == "__main__":
    # Ensure we are in the right directory for imports
    sys.path.append(os.path.join(os.getcwd(), 'bizosaas-brain-core', 'brain-gateway'))
    asyncio.run(initialize_tenants_and_wallets())
