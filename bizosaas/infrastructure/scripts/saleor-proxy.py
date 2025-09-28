#!/usr/bin/env python3

"""
Saleor GraphQL Proxy Server
Serves as a temporary GraphQL endpoint at localhost:8024 while the main Saleor infrastructure is being set up.
"""

import asyncio
import json
from aiohttp import web, ClientSession
import aiohttp_cors
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
PROXY_PORT = 8024
SALEOR_DEMO_API = "https://demo.saleor.io/graphql/"
HEALTH_RESPONSE = {
    "status": "ok",
    "service": "saleor-proxy",
    "version": "1.0.0",
    "endpoints": {
        "graphql": "/graphql/",
        "health": "/health/"
    }
}

# GraphQL Introspection Schema for Saleor
INTROSPECTION_QUERY = "query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description locations args { ...InputValue } } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }"

# Simplified Saleor Schema for Introspection
SALEOR_SCHEMA_INTROSPECTION = {
    "data": {
        "__schema": {
            "queryType": {"name": "Query"},
            "mutationType": {"name": "Mutation"},
            "subscriptionType": None,
            "types": [
                {
                    "kind": "OBJECT",
                    "name": "Query",
                    "description": "The root query object",
                    "fields": [
                        {
                            "name": "shop",
                            "description": "Return information about the shop",
                            "args": [],
                            "type": {
                                "kind": "OBJECT",
                                "name": "Shop",
                                "ofType": None
                            },
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "products",
                            "description": "List of products", 
                            "args": [
                                {
                                    "name": "first",
                                    "description": "Return the first n elements",
                                    "type": {
                                        "kind": "SCALAR",
                                        "name": "Int",
                                        "ofType": None
                                    },
                                    "defaultValue": None
                                }
                            ],
                            "type": {
                                "kind": "OBJECT",
                                "name": "ProductCountableConnection",
                                "ofType": None
                            },
                            "isDeprecated": False,
                            "deprecationReason": None
                        }
                    ],
                    "inputFields": None,
                    "interfaces": [],
                    "enumValues": None,
                    "possibleTypes": None
                },
                {
                    "kind": "OBJECT",
                    "name": "Shop",
                    "description": "Represents a shop resource",
                    "fields": [
                        {
                            "name": "name",
                            "description": "Shop's name",
                            "args": [],
                            "type": {
                                "kind": "NON_NULL",
                                "name": None,
                                "ofType": {
                                    "kind": "SCALAR",
                                    "name": "String",
                                    "ofType": None
                                }
                            },
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "description",
                            "description": "Shop's description",
                            "args": [],
                            "type": {
                                "kind": "SCALAR",
                                "name": "String",
                                "ofType": None
                            },
                            "isDeprecated": False,
                            "deprecationReason": None
                        }
                    ],
                    "inputFields": None,
                    "interfaces": [],
                    "enumValues": None,
                    "possibleTypes": None
                },
                {
                    "kind": "SCALAR",
                    "name": "String",
                    "description": "The String scalar type represents textual data",
                    "fields": None,
                    "inputFields": None,
                    "interfaces": None,
                    "enumValues": None,
                    "possibleTypes": None
                },
                {
                    "kind": "SCALAR",
                    "name": "Int",
                    "description": "The Int scalar type represents non-fractional signed whole numeric values",
                    "fields": None,
                    "inputFields": None,
                    "interfaces": None,
                    "enumValues": None,
                    "possibleTypes": None
                }
            ],
            "directives": []
        }
    }
}

# Sample GraphQL responses for common queries
SAMPLE_SHOP_DATA = {
    "data": {
        "shop": {
            "name": "CoreLDove Demo Store",
            "description": "Enhanced e-commerce platform powered by Saleor",
            "defaultCountry": {
                "code": "US",
                "country": "United States"
            },
            "defaultCurrency": "USD",
            "domain": {
                "host": "localhost:8024"
            }
        }
    }
}

SAMPLE_PRODUCTS_DATA = {
    "data": {
        "products": {
            "edges": [
                {
                    "node": {
                        "id": "UHJvZHVjdDox",
                        "name": "Sample Product 1",
                        "slug": "sample-product-1",
                        "description": "This is a sample product for testing the storefront",
                        "pricing": {
                            "priceRange": {
                                "start": {
                                    "gross": {
                                        "amount": 29.99,
                                        "currency": "USD"
                                    }
                                }
                            }
                        },
                        "thumbnail": {
                            "url": "https://via.placeholder.com/300x300?text=Product+1",
                            "alt": "Sample Product 1"
                        }
                    }
                },
                {
                    "node": {
                        "id": "UHJvZHVjdDoy",
                        "name": "Sample Product 2", 
                        "slug": "sample-product-2",
                        "description": "Another sample product for testing",
                        "pricing": {
                            "priceRange": {
                                "start": {
                                    "gross": {
                                        "amount": 49.99,
                                        "currency": "USD"
                                    }
                                }
                            }
                        },
                        "thumbnail": {
                            "url": "https://via.placeholder.com/300x300?text=Product+2",
                            "alt": "Sample Product 2"
                        }
                    }
                }
            ]
        }
    }
}

async def health_check(request):
    """Health check endpoint"""
    return web.json_response(HEALTH_RESPONSE)

async def graphql_handler(request):
    """GraphQL endpoint handler"""
    
    if request.method == 'GET':
        # GraphQL Playground
        playground_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Saleor GraphQL Playground</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
        </head>
        <body>
            <div id="root">
                <style>
                    body {
                        background-color: #1a1a1a;
                        font-family: Open Sans, sans-serif;
                        height: 90vh;
                    }
                    #root {
                        height: 100%;
                        width: 100%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                </style>
                <div style="color: white; text-align: center;">
                    <h1>🚀 Saleor GraphQL Proxy</h1>
                    <p>GraphQL endpoint is running at <code>/graphql/</code></p>
                    <p>Send POST requests with GraphQL queries to test the API</p>
                    <p>Status: <span style="color: #4CAF50;">Active</span></p>
                    
                    <h3>Sample Query:</h3>
                    <pre style="background: #2a2a2a; padding: 20px; border-radius: 8px; text-align: left;">
{
  shop {
    name
    description
    defaultCountry {
      code
      country
    }
  }
}</pre>
                </div>
            </div>
        </body>
        </html>
        """
        return web.Response(text=playground_html, content_type='text/html')
    
    try:
        # Handle POST requests (GraphQL queries)
        data = await request.json()
        query = data.get('query', '')
        variables = data.get('variables', {})
        
        logger.info(f"GraphQL Query: {query[:100]}...")
        
        # Handle introspection queries
        if '__schema' in query or 'IntrospectionQuery' in query:
            logger.info("Handling introspection query")
            return web.json_response(SALEOR_SCHEMA_INTROSPECTION)
        
        # Simple query routing based on content
        if 'shop' in query and 'products' not in query:
            return web.json_response(SAMPLE_SHOP_DATA)
        elif 'products' in query:
            return web.json_response(SAMPLE_PRODUCTS_DATA)
        else:
            # Try to proxy to demo API for complex queries
            try:
                async with ClientSession() as session:
                    async with session.post(SALEOR_DEMO_API, json=data) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            return web.json_response(result)
            except Exception as e:
                logger.warning(f"Demo API proxy failed: {e}")
            
            # Fallback response
            return web.json_response({
                "data": None,
                "errors": [
                    {
                        "message": "This is a development proxy. Full Saleor infrastructure is being set up.",
                        "extensions": {
                            "code": "PROXY_FALLBACK"
                        }
                    }
                ]
            })
            
    except Exception as e:
        logger.error(f"GraphQL handler error: {e}")
        return web.json_response({
            "errors": [
                {
                    "message": f"Internal server error: {str(e)}",
                    "extensions": {
                        "code": "INTERNAL_ERROR"
                    }
                }
            ]
        }, status=500)

async def create_app():
    """Create and configure the web application"""
    
    app = web.Application()
    
    # Configure CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add routes
    app.router.add_get('/health/', health_check)
    app.router.add_get('/graphql/', graphql_handler)
    app.router.add_post('/graphql/', graphql_handler)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def main():
    """Main application entry point"""
    
    print("🚀 Starting Saleor GraphQL Proxy Server...")
    print(f"🌐 Server will be available at: http://localhost:{PROXY_PORT}")
    print(f"🔗 GraphQL endpoint: http://localhost:{PROXY_PORT}/graphql/")
    print(f"❤️  Health check: http://localhost:{PROXY_PORT}/health/")
    print("📊 This is a development proxy while the full Saleor infrastructure is being set up.")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, 'localhost', PROXY_PORT)
    await site.start()
    
    print(f"✅ Saleor GraphQL Proxy Server started on port {PROXY_PORT}")
    print("💡 Test the endpoint:")
    print(f"   curl -X POST http://localhost:{PROXY_PORT}/graphql/ \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d '{{\"query\":\"{{ shop {{ name }} }}\"}}'")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Saleor GraphQL Proxy Server...")
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")