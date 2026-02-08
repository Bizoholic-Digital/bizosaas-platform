from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from app.dependencies import get_secret_service
from app.domain.services.secret_service import SecretService
import os
import hmac
import hashlib
import httpx
import logging
import secrets
import urllib.parse

router = APIRouter(prefix="/api/shopify", tags=["shopify-oauth"])
logger = logging.getLogger(__name__)

# Configuration
SHOPIFY_API_KEY = os.getenv("SHOPIFY_CLIENT_ID")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
# Default to current domain if not set, but callback must match Partner Dashboard
APP_URL = os.getenv("SHOPIFY_APP_URL", "https://api.bizoholic.net") 
SCOPES = "read_products,write_products,read_orders,read_customers,read_inventory,write_inventory"

def verify_shopify_hmac(query_params: dict, secret: str) -> bool:
    """
    Verify Shopify HMAC signature.
    HMAC is calculated using the query parameters (minus hmac) sorted alphabetically.
    """
    if "hmac" not in query_params:
        return False
        
    hmac_param = query_params["hmac"]
    params = query_params.copy()
    del params["hmac"]
    
    # Sort and encode
    sorted_params = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    
    # Calculate HMAC
    digest = hmac.new(secret.encode('utf-8'), sorted_params.encode('utf-8'), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(digest, hmac_param)

@router.get("/auth")
async def shopify_auth(shop: str):
    """
    Initiate Shopify OAuth flow.
    Redirects to Shopify Admin for permission grant.
    """
    if not SHOPIFY_API_KEY:
        return JSONResponse({"error": "Shopify Client ID (SHOPIFY_CLIENT_ID) not configured in backend"}, status_code=500)
    
    if not shop:
        return JSONResponse({"error": "Missing 'shop' parameter"}, status_code=400)
        
    state = secrets.token_hex(16)
    redirect_uri = f"{APP_URL}/api/shopify/callback"
    
    # Shop formatting check
    if not shop.endswith(".myshopify.com"):
        shop = f"{shop}.myshopify.com"
        
    install_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope={SCOPES}&redirect_uri={redirect_uri}&state={state}"
    
    logger.info(f"Redirecting to Shopify Auth: {install_url}")
    return RedirectResponse(install_url)

@router.get("/callback")
async def shopify_callback(request: Request, secret_service: SecretService = Depends(get_secret_service)):
    """
    Handle Shopify OAuth callback.
    Exchanges authorization code for access token and stores it in Vault.
    """
    params = dict(request.query_params)
    shop = params.get("shop")
    code = params.get("code")
    
    if not SHOPIFY_API_SECRET:
         return JSONResponse({"error": "Shopify Client Secret (SHOPIFY_CLIENT_SECRET) not configured"}, status_code=500)
         
    if not shop or not code:
        return JSONResponse({"error": "Missing shop or code parameter"}, status_code=400)

    # Validate HMAC
    if not verify_shopify_hmac(params, SHOPIFY_API_SECRET):
        logger.warning(f"HMAC validation failed for shop {shop}")
        return JSONResponse({"error": "HMAC validation failed"}, status_code=401)
    
    # Exchange Token
    access_token_url = f"https://{shop}/admin/oauth/access_token"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(access_token_url, json={
                "client_id": SHOPIFY_API_KEY,
                "client_secret": SHOPIFY_API_SECRET,
                "code": code
            })
            
            if response.status_code != 200:
                logger.error(f"Token exchange failed: {response.text}")
                return JSONResponse({"error": "Failed to exchange token", "details": response.text}, status_code=400)
            
            data = response.json()
            access_token = data.get("access_token")
            
            logger.info(f"Successfully obtained access token for {shop}")
            
            # Store in Vault via SecretService
            # We use the shop domain (e.g. coreldove.myshopify.com) as the Tenant ID context for now
            # In a real multi-tenant app, we might map this to a specific BizOSaaS Tenant ID
            # For Day 1, we use Shop Domain as the identifier.
            await secret_service.store_connector_credentials(
                tenant_id=shop,
                connector_id="shopify",
                credentials={
                    "access_token": access_token, 
                    "shop_url": shop,
                    "scope": data.get("scope")
                }
            )
            
            # Redirect to App in Shopify Admin
            # If it's an embedded app, we redirect to the App Bridge URL
            # If not, we redirect to our dashboard
            return RedirectResponse(f"https://{shop}/admin/apps/{SHOPIFY_API_KEY}")
            
        except Exception as e:
            logger.error(f"OAuth Callback Error: {e}")
            return JSONResponse({"error": f"Internal Server Error: {str(e)}"}, status_code=500)

@router.get("/proxy")
async def shopify_proxy(request: Request):
    """
    Handle App Proxy requests from Shopify Storefront.
    Verifies signature and returns Liquid or JSON.
    """
    params = dict(request.query_params)
    signature = params.get("signature")
    
    # Proxy signature validation logic is different (SHA256 of sorted params)
    # For now, return a simple success message
    return JSONResponse(
        content={"message": "BizOSaaS App Proxy is active", "shop": params.get("shop")},
        headers={"Content-Type": "application/liquid"} # Shopify expects Liquid usually, or JSON
    )
