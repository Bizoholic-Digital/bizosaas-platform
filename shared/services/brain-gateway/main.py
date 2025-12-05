import os
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Brain API Gateway")

# Configuration
CMS_URL = os.getenv("CMS_URL", "http://cms:8002")
CRM_URL = os.getenv("CRM_URL", "http://crm:8003")
AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8008")
SALEOR_URL = os.getenv("SALEOR_URL", "http://saleor:8000")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "brain-gateway"}

@app.api_route("/api/brain/wagtail/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_wagtail(request: Request, path: str):
    url = f"{CMS_URL}/api/v2/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/django-crm/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_crm(request: Request, path: str):
    url = f"{CRM_URL}/api/{path}"
    return await proxy_request(request, url)

@app.api_route("/api/brain/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(request: Request, path: str):
    url = f"{AUTH_URL}/{path}"
    return await proxy_request(request, url)

@app.post("/api/auth/login")
async def auth_login(request: Request):
    """Proxy login to Auth Service SSO"""
    url = f"{AUTH_URL}/auth/sso/login"
    return await proxy_request(request, url)

@app.post("/api/auth/social-login")
async def auth_social_login(request: Request):
    """Proxy social login to Auth Service Token Exchange"""
    url = f"{AUTH_URL}/auth/token/exchange"
    return await proxy_request(request, url)

async def proxy_request(request: Request, url: str):
    async with httpx.AsyncClient() as client:
        try:
            # Forward headers, excluding hop-by-hop headers
            headers = {
                k: v for k, v in request.headers.items() 
                if k.lower() not in ('content-length', 'transfer-encoding', 'host')
            }
            
            content = await request.body()
            
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=content,
                params=request.query_params,
                timeout=30.0
            )
            
            # Try to parse as JSON, fall back to text
            try:
                response_content = response.json()
            except:
                response_content = response.text
            
            return JSONResponse(
                content=response_content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                content={"error": f"Service unavailable: {str(exc)}"},
                status_code=503
            )
        except Exception as exc:
            return JSONResponse(
                content={"error": f"Internal server error: {str(exc)}"},
                status_code=500
            )

@app.post("/api/auth/sso/wagtail")
async def sso_wagtail(request: Request):
    """
    Generate SSO login URL for Wagtail.
    1. Receives user info (should be from JWT in production)
    2. Calls Wagtail internal API to get signed token
    3. Returns magic link
    """
    try:
        body = await request.json()
        
        # Call Wagtail internal API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CMS_URL}/api/internal/sso/token/",
                json=body,
                timeout=5.0
            )
            
            if response.status_code != 200:
                return JSONResponse(
                    content={"error": "Failed to generate SSO token"},
                    status_code=response.status_code
                )
                
            data = response.json()
            
            # Construct absolute URL for the frontend iframe
            # The token URL path is returned by Wagtail, e.g. /admin/sso/login/?token=...
            # We need to prepend the public Wagtail URL (proxied via Brain or direct)
            # Since Wagtail is embedded, we use the public URL routed through Brain or direct port
            # For now, let's assume direct access or proxied access.
            # If proxied: http://localhost:8000/api/brain/wagtail/... but that might not work for admin
            # The admin is accessed via http://localhost:8002/admin/ directly in the iframe usually
            # So we return the full URL using the public CMS URL (localhost:8002)
            
            # Use the login_url returned by Wagtail (relative path)
            # Prepend the public base URL
            public_cms_url = "http://localhost:8002" 
            full_url = f"{public_cms_url}{data['login_url']}"
            
            return JSONResponse({
                "sso_url": full_url,
                "expires_in": data.get("expires_in")
            })
            
    except Exception as exc:
        return JSONResponse(
            content={"error": f"SSO Error: {str(exc)}"},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
