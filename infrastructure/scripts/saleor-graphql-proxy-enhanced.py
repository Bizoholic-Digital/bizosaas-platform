#!/usr/bin/env python3

"""
Enhanced Saleor GraphQL Proxy Server
Proxies requests to demo.saleor.io for proper GraphQL schema introspection
"""

import asyncio
import json
from aiohttp import web, ClientSession, ClientTimeout
import aiohttp_cors
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
PROXY_PORT = 8024
SALEOR_DEMO_API = "https://demo.saleor.io/graphql/"
TIMEOUT = ClientTimeout(total=30, connect=10)

# Health check response
HEALTH_RESPONSE = {
    "status": "healthy",
    "service": "saleor-graphql-proxy",
    "version": "2.0.0",
    "upstream": SALEOR_DEMO_API,
    "endpoints": {
        "graphql": "/graphql/",
        "health": "/health/"
    },
    "features": [
        "GraphQL Proxy",
        "Schema Introspection", 
        "CORS Support",
        "Request Caching"
    ]
}

# Simple cache for schema introspection
schema_cache = {"data": None, "timestamp": 0, "ttl": 300}  # 5 minute TTL

async def health_check(request):
    """Health check endpoint"""
    return web.json_response(HEALTH_RESPONSE)

async def graphql_playground(request):
    """GraphQL Playground HTML"""
    playground_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CoreLDove - Saleor GraphQL API</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
    </head>
    <body>
        <div id="root">
            <style>
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    height: 100vh;
                    margin: 0;
                    color: white;
                }
                .container {
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                    text-align: center;
                    padding: 40px;
                }
                .logo {
                    font-size: 3rem;
                    margin-bottom: 20px;
                }
                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                    font-weight: 300;
                }
                .subtitle {
                    font-size: 1.2rem;
                    opacity: 0.8;
                    margin-bottom: 40px;
                }
                .status {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 12px;
                    margin-bottom: 30px;
                    backdrop-filter: blur(10px);
                }
                .endpoint {
                    background: rgba(0, 0, 0, 0.2);
                    padding: 15px 25px;
                    border-radius: 8px;
                    margin: 10px 0;
                    font-family: 'Monaco', 'Consolas', monospace;
                }
                .sample-query {
                    background: rgba(0, 0, 0, 0.3);
                    padding: 25px;
                    border-radius: 12px;
                    text-align: left;
                    margin-top: 20px;
                }
                .sample-query pre {
                    margin: 0;
                    color: #61dafb;
                    font-size: 14px;
                    line-height: 1.5;
                }
            </style>
            <div class="container">
                <div class="logo">🚀</div>
                <h1>CoreLDove GraphQL API</h1>
                <div class="subtitle">Enhanced E-commerce Platform powered by Saleor</div>
                
                <div class="status">
                    <h3>🌐 API Status: <span style="color: #4CAF50;">Active</span></h3>
                    <div class="endpoint">POST /graphql/ - GraphQL API Endpoint</div>
                    <div class="endpoint">GET /health/ - Health Check</div>
                </div>
                
                <div class="sample-query">
                    <h3>📝 Sample Query:</h3>
                    <pre>{
  shop {
    name
    description
    defaultCountry {
      code
      country
    }
  }
  products(first: 3) {
    edges {
      node {
        name
        slug
      }
    }
  }
}</pre>
                </div>
                
                <div style="margin-top: 30px; opacity: 0.7;">
                    <p>💡 Use any GraphQL client or send POST requests to <code>/graphql/</code></p>
                    <p>🔗 Proxying requests to: demo.saleor.io</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=playground_html, content_type='text/html')

async def graphql_proxy(request):
    """GraphQL proxy handler"""
    
    try:
        # Parse request data
        data = await request.json()
        query = data.get('query', '')
        variables = data.get('variables', {})
        operation_name = data.get('operationName')
        
        # Log request info
        if '__schema' in query or 'IntrospectionQuery' in query:
            logger.info("🔍 Handling GraphQL introspection query")
        else:
            logger.info(f"📊 GraphQL Query: {query[:50]}{'...' if len(query) > 50 else ''}")
        
        # Check cache for introspection queries
        current_time = time.time()
        if ('__schema' in query or 'IntrospectionQuery' in query) and schema_cache['data']:
            if current_time - schema_cache['timestamp'] < schema_cache['ttl']:
                logger.info("📦 Serving cached schema introspection")
                return web.json_response(schema_cache['data'])
        
        # Proxy request to Saleor demo API
        request_data = {
            'query': query,
            'variables': variables
        }
        
        if operation_name:
            request_data['operationName'] = operation_name
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CoreLDove-GraphQL-Proxy/2.0'
        }
        
        async with ClientSession(timeout=TIMEOUT) as session:
            async with session.post(SALEOR_DEMO_API, json=request_data, headers=headers) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    # Cache introspection results
                    if '__schema' in query or 'IntrospectionQuery' in query:
                        schema_cache['data'] = result
                        schema_cache['timestamp'] = current_time
                        logger.info("💾 Cached schema introspection result")
                    
                    # Log successful response
                    if result.get('errors'):
                        logger.warning(f"⚠️  GraphQL response contains errors: {len(result['errors'])} error(s)")
                    else:
                        logger.info("✅ GraphQL request successful")
                    
                    return web.json_response(result)
                    
                else:
                    logger.error(f"❌ Upstream API error: HTTP {response.status}")
                    error_text = await response.text()
                    
                    return web.json_response({
                        "errors": [{
                            "message": f"Upstream API error: HTTP {response.status}",
                            "extensions": {
                                "code": "UPSTREAM_ERROR",
                                "status": response.status,
                                "details": error_text[:200]
                            }
                        }]
                    }, status=502)
                    
    except asyncio.TimeoutError:
        logger.error("⏱️  Request timeout")
        return web.json_response({
            "errors": [{
                "message": "Request timeout - upstream API took too long to respond",
                "extensions": {"code": "TIMEOUT_ERROR"}
            }]
        }, status=504)
        
    except json.JSONDecodeError:
        logger.error("📄 Invalid JSON in request")
        return web.json_response({
            "errors": [{
                "message": "Invalid JSON in request body",
                "extensions": {"code": "INVALID_JSON"}
            }]
        }, status=400)
        
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        return web.json_response({
            "errors": [{
                "message": f"Internal proxy error: {str(e)}",
                "extensions": {"code": "INTERNAL_ERROR"}
            }]
        }, status=500)

async def create_app():
    """Create and configure the web application"""
    
    app = web.Application()
    
    # Configure CORS for storefront
    cors = aiohttp_cors.setup(app, defaults={
        "http://localhost:3001": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS"]
        ),
        "http://127.0.0.1:3001": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*", 
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS"]
        ),
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=False,
            expose_headers="*",
            allow_headers=["Content-Type", "Authorization"],
            allow_methods=["GET", "POST", "OPTIONS"]
        )
    })
    
    # Add routes
    app.router.add_get('/health/', health_check)
    app.router.add_get('/graphql/', graphql_playground)
    app.router.add_post('/graphql/', graphql_proxy)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def test_upstream_connection():
    """Test connection to upstream Saleor API"""
    
    print("🔍 Testing connection to upstream Saleor API...")
    
    try:
        test_query = {"query": "{ shop { name } }"}
        headers = {'Content-Type': 'application/json'}
        
        async with ClientSession(timeout=TIMEOUT) as session:
            async with session.post(SALEOR_DEMO_API, json=test_query, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    shop_name = result.get('data', {}).get('shop', {}).get('name', 'Unknown')
                    print(f"✅ Upstream API connection successful!")
                    print(f"🏪 Connected to shop: {shop_name}")
                    return True
                else:
                    print(f"❌ Upstream API returned HTTP {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Failed to connect to upstream API: {e}")
        return False

async def main():
    """Main application entry point"""
    
    print("🚀 Starting Enhanced Saleor GraphQL Proxy...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Test upstream connection
    upstream_ok = await test_upstream_connection()
    
    if not upstream_ok:
        print("⚠️  Warning: Upstream API connection failed, but starting proxy anyway...")
    
    print(f"🌐 Proxy Server: http://localhost:{PROXY_PORT}")
    print(f"🔗 GraphQL Endpoint: http://localhost:{PROXY_PORT}/graphql/")
    print(f"❤️  Health Check: http://localhost:{PROXY_PORT}/health/")
    print(f"🎯 Upstream API: {SALEOR_DEMO_API}")
    print("")
    print("✨ Features:")
    print("   • GraphQL Schema Introspection")
    print("   • Request Proxying to demo.saleor.io")
    print("   • CORS Support for localhost:3001")
    print("   • Request Caching")
    print("   • Error Handling")
    print("")
    
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, 'localhost', PROXY_PORT)
    await site.start()
    
    print("✅ Enhanced Saleor GraphQL Proxy is running!")
    print("")
    print("💡 Test Commands:")
    print(f"   curl http://localhost:{PROXY_PORT}/health/")
    print(f"   curl -X POST http://localhost:{PROXY_PORT}/graphql/ \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d '{{\"query\":\"{{ shop {{ name }} }}\"}}'")
    print("")
    print("🛑 Press Ctrl+C to stop the server")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Enhanced Saleor GraphQL Proxy...")
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProxy server stopped.")