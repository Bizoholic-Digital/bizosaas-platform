#!/usr/bin/env python3

"""
Standalone Saleor-Compatible GraphQL API Server
Provides a basic GraphQL API compatible with Saleor storefront for development
"""

import asyncio
import json
from aiohttp import web
import aiohttp_cors
import logging
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_PORT = 8024

# GraphQL Schema Definition
GRAPHQL_SCHEMA = {
    "data": {
        "__schema": {
            "queryType": {"name": "Query"},
            "mutationType": {"name": "Mutation"},
            "subscriptionType": None,
            "types": [
                {
                    "kind": "OBJECT",
                    "name": "Query",
                    "description": "Root Query",
                    "fields": [
                        {
                            "name": "shop",
                            "description": "Return information about the shop",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "OBJECT", "name": "Shop", "ofType": None}},
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
                                    "type": {"kind": "SCALAR", "name": "Int", "ofType": None},
                                    "defaultValue": None
                                }
                            ],
                            "type": {"kind": "OBJECT", "name": "ProductCountableConnection", "ofType": None},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "categories",
                            "description": "List of categories",
                            "args": [
                                {
                                    "name": "first",
                                    "description": "Return the first n elements",
                                    "type": {"kind": "SCALAR", "name": "Int", "ofType": None},
                                    "defaultValue": None
                                }
                            ],
                            "type": {"kind": "OBJECT", "name": "CategoryCountableConnection", "ofType": None},
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
                    "description": "Shop information",
                    "fields": [
                        {
                            "name": "name",
                            "description": "Shop name",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "SCALAR", "name": "String", "ofType": None}},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "description",
                            "description": "Shop description",
                            "args": [],
                            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "defaultCountry",
                            "description": "Default country",
                            "args": [],
                            "type": {"kind": "OBJECT", "name": "CountryDisplay", "ofType": None},
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
                    "name": "CountryDisplay",
                    "description": "Country information",
                    "fields": [
                        {
                            "name": "code",
                            "description": "Country code",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "SCALAR", "name": "String", "ofType": None}},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "country",
                            "description": "Country name",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "SCALAR", "name": "String", "ofType": None}},
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
                    "name": "ProductCountableConnection",
                    "description": "Connection for paginated products",
                    "fields": [
                        {
                            "name": "edges",
                            "description": "Product edges",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "LIST", "name": None, "ofType": {"kind": "OBJECT", "name": "ProductCountableEdge", "ofType": None}}},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "totalCount",
                            "description": "Total count of products",
                            "args": [],
                            "type": {"kind": "SCALAR", "name": "Int", "ofType": None},
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
                    "name": "ProductCountableEdge",
                    "description": "Product edge",
                    "fields": [
                        {
                            "name": "node",
                            "description": "Product node",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "OBJECT", "name": "Product", "ofType": None}},
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
                    "name": "Product",
                    "description": "Product information",
                    "fields": [
                        {
                            "name": "id",
                            "description": "Product ID",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "SCALAR", "name": "ID", "ofType": None}},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "name",
                            "description": "Product name",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "SCALAR", "name": "String", "ofType": None}},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "slug",
                            "description": "Product slug",
                            "args": [],
                            "type": {"kind": "NON_NULL", "name": None, "ofType": {"kind": "SCALAR", "name": "String", "ofType": None}},
                            "isDeprecated": False,
                            "deprecationReason": None
                        },
                        {
                            "name": "description",
                            "description": "Product description",
                            "args": [],
                            "type": {"kind": "SCALAR", "name": "String", "ofType": None},
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
                    "description": "String scalar type",
                    "fields": None,
                    "inputFields": None,
                    "interfaces": None,
                    "enumValues": None,
                    "possibleTypes": None
                },
                {
                    "kind": "SCALAR",
                    "name": "Int",
                    "description": "Integer scalar type",
                    "fields": None,
                    "inputFields": None,
                    "interfaces": None,
                    "enumValues": None,
                    "possibleTypes": None
                },
                {
                    "kind": "SCALAR",
                    "name": "ID",
                    "description": "ID scalar type",
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

# Sample data responses
SHOP_DATA = {
    "data": {
        "shop": {
            "name": "CoreLDove Store",
            "description": "Enhanced e-commerce platform powered by Saleor - Development Environment",
            "defaultCountry": {
                "code": "US",
                "country": "United States"
            }
        }
    }
}

PRODUCTS_DATA = {
    "data": {
        "products": {
            "edges": [
                {
                    "node": {
                        "id": "UHJvZHVjdDox",
                        "name": "Premium Headphones",
                        "slug": "premium-headphones",
                        "description": "High-quality wireless headphones with noise cancellation"
                    }
                },
                {
                    "node": {
                        "id": "UHJvZHVjdDoy", 
                        "name": "Smart Watch",
                        "slug": "smart-watch",
                        "description": "Advanced smartwatch with health monitoring features"
                    }
                },
                {
                    "node": {
                        "id": "UHJvZHVjdDoz",
                        "name": "Laptop Stand",
                        "slug": "laptop-stand",
                        "description": "Adjustable aluminum laptop stand for better ergonomics"
                    }
                },
                {
                    "node": {
                        "id": "UHJvZHVjdDo0",
                        "name": "Wireless Charger",
                        "slug": "wireless-charger",
                        "description": "Fast wireless charging pad compatible with all Qi devices"
                    }
                },
                {
                    "node": {
                        "id": "UHJvZHVjdDo1",
                        "name": "Bluetooth Speaker",
                        "slug": "bluetooth-speaker",
                        "description": "Portable waterproof Bluetooth speaker with excellent sound quality"
                    }
                }
            ],
            "totalCount": 5
        }
    }
}

CATEGORIES_DATA = {
    "data": {
        "categories": {
            "edges": [
                {
                    "node": {
                        "id": "Q2F0ZWdvcnk6MQ==",
                        "name": "Electronics",
                        "slug": "electronics"
                    }
                },
                {
                    "node": {
                        "id": "Q2F0ZWdvcnk6Mg==",
                        "name": "Accessories", 
                        "slug": "accessories"
                    }
                },
                {
                    "node": {
                        "id": "Q2F0ZWdvcnk6Mw==",
                        "name": "Audio",
                        "slug": "audio"
                    }
                }
            ],
            "totalCount": 3
        }
    }
}

async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "saleor-api-standalone", 
        "version": "1.0.0",
        "features": ["GraphQL API", "Schema Introspection", "CORS Support"],
        "endpoints": {
            "graphql": "/graphql/",
            "health": "/health/"
        }
    })

async def graphql_playground(request):
    """GraphQL Playground interface"""
    playground_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CoreLDove - Saleor API</title>
        <style>
            body {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 40px;
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
            }
            h1 { font-size: 3rem; margin-bottom: 10px; font-weight: 300; }
            .subtitle { font-size: 1.3rem; opacity: 0.8; margin-bottom: 40px; }
            .status-box {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 30px;
                margin: 30px 0;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .endpoint {
                background: rgba(0, 0, 0, 0.2);
                padding: 15px 20px;
                border-radius: 8px;
                margin: 10px 0;
                font-family: 'Monaco', 'Consolas', monospace;
                font-size: 14px;
            }
            .sample-queries {
                text-align: left;
                background: rgba(0, 0, 0, 0.3);
                padding: 25px;
                border-radius: 12px;
                margin: 20px 0;
            }
            .sample-queries pre {
                margin: 10px 0;
                color: #61dafb;
                font-size: 13px;
                line-height: 1.4;
            }
            .feature-list {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }
            .feature-item {
                background: rgba(255, 255, 255, 0.05);
                padding: 15px;
                border-radius: 8px;
                border-left: 3px solid #4CAF50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 CoreLDove API</h1>
            <div class="subtitle">Saleor-Compatible GraphQL API - Development Server</div>
            
            <div class="status-box">
                <h3>🌐 Service Status: <span style="color: #4CAF50;">Active</span></h3>
                <div class="endpoint">POST /graphql/ - GraphQL API Endpoint</div>
                <div class="endpoint">GET /health/ - Health Check Endpoint</div>
            </div>
            
            <div class="feature-list">
                <div class="feature-item">
                    <strong>✨ Schema Introspection</strong><br>
                    Full GraphQL schema support
                </div>
                <div class="feature-item">
                    <strong>🛍️ Product Catalog</strong><br>
                    Sample product data
                </div>
                <div class="feature-item">
                    <strong>🏪 Shop Information</strong><br>
                    Store configuration
                </div>
                <div class="feature-item">
                    <strong>🔗 CORS Enabled</strong><br>
                    Storefront integration ready
                </div>
            </div>
            
            <div class="sample-queries">
                <h3>📝 Sample GraphQL Queries:</h3>
                
                <h4>Shop Information:</h4>
                <pre>query {
  shop {
    name
    description
    defaultCountry {
      code
      country
    }
  }
}</pre>
                
                <h4>Product Catalog:</h4>
                <pre>query {
  products(first: 5) {
    edges {
      node {
        id
        name
        slug
        description
      }
    }
    totalCount
  }
}</pre>
                
                <h4>Schema Introspection:</h4>
                <pre>query {
  __schema {
    queryType {
      name
    }
    types {
      name
      kind
    }
  }
}</pre>
            </div>
            
            <div style="margin-top: 40px; opacity: 0.8;">
                <p>💡 Send POST requests to <code>/graphql/</code> with your GraphQL queries</p>
                <p>🔧 This is a development API server for CoreLDove storefront integration</p>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=playground_html, content_type='text/html')

async def graphql_handler(request):
    """GraphQL API handler"""
    
    try:
        data = await request.json()
        query = data.get('query', '').strip()
        variables = data.get('variables', {})
        
        # Log the query
        if '__schema' in query or 'IntrospectionQuery' in query:
            logger.info("🔍 Handling GraphQL schema introspection")
        else:
            logger.info(f"📊 GraphQL Query: {query[:60]}{'...' if len(query) > 60 else ''}")
        
        # Handle introspection queries
        if '__schema' in query or 'IntrospectionQuery' in query:
            return web.json_response(GRAPHQL_SCHEMA)
        
        # Handle specific queries
        if 'shop' in query and 'products' not in query and 'categories' not in query:
            logger.info("🏪 Returning shop information")
            return web.json_response(SHOP_DATA)
        elif 'products' in query:
            logger.info("🛍️ Returning product catalog")
            return web.json_response(PRODUCTS_DATA)
        elif 'categories' in query:
            logger.info("📂 Returning categories")
            return web.json_response(CATEGORIES_DATA)
        else:
            # Generic response for unsupported queries
            logger.info("❓ Unsupported query, returning empty data")
            return web.json_response({
                "data": None,
                "errors": [
                    {
                        "message": "This query is not yet implemented in the development API server.",
                        "extensions": {
                            "code": "NOT_IMPLEMENTED",
                            "hint": "Try shop, products, or categories queries"
                        }
                    }
                ]
            })
            
    except json.JSONDecodeError:
        logger.error("📄 Invalid JSON in request")
        return web.json_response({
            "errors": [
                {
                    "message": "Invalid JSON in request body",
                    "extensions": {"code": "INVALID_JSON"}
                }
            ]
        }, status=400)
        
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        return web.json_response({
            "errors": [
                {
                    "message": f"Internal server error: {str(e)}",
                    "extensions": {"code": "INTERNAL_ERROR"}
                }
            ]
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
    app.router.add_post('/graphql/', graphql_handler)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

async def main():
    """Main application entry point"""
    
    print("🚀 Starting Standalone Saleor-Compatible API Server...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🌐 API Server: http://localhost:{API_PORT}")
    print(f"🔗 GraphQL Endpoint: http://localhost:{API_PORT}/graphql/")
    print(f"❤️  Health Check: http://localhost:{API_PORT}/health/")
    print("")
    print("✨ Features:")
    print("   • Full GraphQL Schema Introspection Support")
    print("   • Compatible with Saleor Storefront")
    print("   • CORS Enabled for localhost:3001")
    print("   • Sample Product and Shop Data")
    print("")
    
    app = await create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, 'localhost', API_PORT)
    await site.start()
    
    print("✅ Standalone Saleor API Server is running!")
    print("")
    print("💡 Test Commands:")
    print(f"   curl http://localhost:{API_PORT}/health/")
    print(f"   curl -X POST http://localhost:{API_PORT}/graphql/ \\")
    print(f"        -H 'Content-Type: application/json' \\")
    print(f"        -d '{{\"query\":\"{{ shop {{ name }} }}\"}}'")
    print("")
    print("🔧 Ready for storefront GraphQL code generation!")
    print("🛑 Press Ctrl+C to stop the server")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Standalone Saleor API Server...")
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAPI server stopped.")