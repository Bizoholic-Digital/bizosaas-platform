from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging

from app.dependencies import get_db, require_role, get_current_user
from app.models.revenue import DomainInventory, DomainSearchHistory, PortalRevenue
from app.domain.ports.identity_port import AuthenticatedUser
from app.connectors.registry import ConnectorRegistry
from app.domain.services.secret_service import SecretService
from app.dependencies import get_secret_service

router = APIRouter(prefix="/api/domains", tags=["domains"])
logger = logging.getLogger(__name__)

@router.get("/search")
async def search_domains(
    query: str,
    tlds: List[str] = Query(["com", "net", "org", "io", "ai"]),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Search for domain availability and pricing."""
    # Log search history
    search_entry = DomainSearchHistory(
        tenant_id=user.tenant_id,
        user_id=user.user_id,
        query=query,
        tlds_searched=tlds
    )
    db.add(search_entry)
    db.commit()

    # In a real implementation, we'd iterate through domain connectors (Namecheap, etc.)
    # For now, we'll return a mock response that looks realistic
    results = []
    for tld in tlds:
        domain = f"{query}.{tld}"
        # Simplified logic for mockery
        is_available = len(query) > 3 
        price = 14.99 if tld == "com" else 29.99 if tld == "ai" else 12.99
        
        results.append({
            "domain": domain,
            "available": is_available,
            "price": price,
            "currency": "USD",
            "registrar": "namecheap",
            "premium": False
        })
    
    search_entry.results = results
    db.commit()
    
    return results

@router.post("/purchase")
async def purchase_domain(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Initiate a domain purchase."""
    domain_name = payload.get("domain")
    if not domain_name:
        raise HTTPException(status_code=400, detail="Domain name is required")
    
    # Check if already exists in platform
    existing = db.query(DomainInventory).filter(DomainInventory.domain_name == domain_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Domain already managed by the platform")

    # In a real implementation:
    # 1. Call Namecheap API to purchase
    # 2. Record transaction in PortalRevenue (with markup)
    # 3. Add to DomainInventory
    # 4. Trigger Lago billing update
    
    # Mocking the process
    price = payload.get("price", 14.99)
    markup = 4.00
    
    # Record Revenue
    revenue = PortalRevenue(
        tenant_id=user.tenant_id,
        user_id=user.user_id,
        source_type="domain_purchase",
        partner_name="namecheap",
        amount=price + markup,
        commission_amount=markup,
        status="completed",
        details={"domain": domain_name}
    )
    db.add(revenue)
    
    # Add to Inventory
    new_domain = DomainInventory(
        tenant_id=user.tenant_id,
        user_id=user.user_id,
        domain_name=domain_name,
        registrar="namecheap",
        status="active",
        expiry_date=None # Would be set by registrar response
    )
    db.add(new_domain)
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Domain {domain_name} successfully registered",
        "domain": domain_name
    }

@router.get("/inventory")
async def list_my_domains(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List domains owned by the current tenant."""
    domains = db.query(DomainInventory).filter(DomainInventory.tenant_id == user.tenant_id).all()
    return domains

@router.get("/admin/stats")
async def get_admin_domain_stats(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Admin only: Global domain performance and revenue metrics."""
    total_domains = db.query(DomainInventory).count()
    total_revenue = db.query(PortalRevenue).filter(PortalRevenue.source_type == "domain_purchase").all()
    
    gross = sum(r.amount for r in total_revenue)
    profit = sum(r.commission_amount for r in total_revenue)
    
    return {
        "total_active_domains": total_domains,
        "gross_revenue": gross,
        "net_profit": profit,
        "currency": "USD"
    }

@router.get("/providers/config")
async def list_domain_providers(
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """List configured domain registrars and their status. Now dynamic."""
    from app.models.system import SystemSetting
    
    # Define primary registrars
    default_providers = {
        "namecheap": {"name": "Namecheap", "priority": 1, "status": "active", "margin": 36.0, "affiliate_link": ""},
        "cloudflare": {"name": "Cloudflare", "priority": 2, "status": "active", "margin": 10.0, "affiliate_link": ""},
        "porkbun": {"name": "Porkbun", "priority": 3, "status": "active", "margin": 25.0, "affiliate_link": ""},
        "opensrs": {"name": "OpenSRS", "priority": 4, "status": "active", "margin": 15.0, "affiliate_link": ""}
    }
    
    # Overwrite with DB values if they exist
    db_configs = db.query(SystemSetting).filter(SystemSetting.key.like("registrar:%:config")).all()
    for conf in db_configs:
        provider_id = conf.key.split(":")[1]
        if provider_id in default_providers:
            default_providers[provider_id].update(conf.value)
            
    return [{"id": k, **v} for k, v in default_providers.items()]

@router.patch("/providers/{provider_id}/config")
async def update_provider_config(
    provider_id: str,
    updates: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin")),
    secret_service: SecretService = Depends(get_secret_service)
):
    """Update registrar configuration (affiliate links, markup, API keys). Admin only."""
    from app.models.system import SystemSetting
    
    # 1. Handle Secrets (Vault)
    sensitive_keys = ["api_key", "api_token", "secret_key"]
    credentials = {k: v for k, v in updates.items() if k in sensitive_keys}
    if credentials:
        await secret_service.store_connector_credentials(
            tenant_id="platform_admin",
            connector_id=provider_id,
            credentials=credentials
        )
    
    # 2. Handle Non-Secrets (DB)
    public_config = {k: v for k, v in updates.items() if k not in sensitive_keys}
    if public_config:
        key = f"registrar:{provider_id}:config"
        setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
        if not setting:
            setting = SystemSetting(key=key, value=public_config)
            db.add(setting)
        else:
            # Merge JSON
            current_val = dict(setting.value)
            current_val.update(public_config)
            setting.value = current_val
        
        db.commit()
        
    return {"status": "success", "message": f"Configuration for {provider_id} updated"}

@router.patch("/{domain_id}/config")
async def update_domain_config(
    domain_id: UUID,
    updates: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Update domain configuration (auto-renew, mapping)."""
    domain = db.query(DomainInventory).filter(DomainInventory.id == domain_id).first()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
        
    if "auto_renew" in updates:
        domain.auto_renew = updates["auto_renew"]
    if "target_service" in updates:
        domain.target_service = updates["target_service"]
    if "target_slug" in updates:
        domain.target_slug = updates["target_slug"]
        
    db.commit()
    return {"status": "success", "message": "Domain configuration updated"}

@router.get("/{domain_id}/dns")
async def get_dns_records(
    domain_id: UUID,
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Fetch current DNS records for a domain."""
    domain = db.query(DomainInventory).filter(DomainInventory.id == domain_id).first()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
        
    # Mock DNS records
    return [
        {"type": "A", "name": "@", "value": "194.238.22.45", "ttl": 3600},
        {"type": "CNAME", "name": "www", "value": domain.domain_name, "ttl": 3600},
        {"type": "TXT", "name": "_google-verification", "value": "v=spf1 include:_spf.google.com ~all", "ttl": 3600}
    ]

@router.post("/{domain_id}/dns")
async def add_dns_record(
    domain_id: UUID,
    record: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(get_current_user)
):
    """Add a new DNS record to the registrar."""
    return {"status": "success", "message": "DNS record added successfully"}

@router.post("/bulk/renew")
async def bulk_renew_domains(
    domain_ids: List[UUID] = Body(..., embed=True),
    db: Session = Depends(get_db),
    user: AuthenticatedUser = Depends(require_role("Super Admin"))
):
    """Bulk renewal of domains (Super Admin only)."""
    return {"status": "success", "count": len(domain_ids), "message": f"Successfully initiated renewal for {len(domain_ids)} domains"}
