#!/usr/bin/env python3
"""
Saleor GraphQL Proxy for CoreLDove Frontend
Provides a GraphQL API that resolves RANK sorting issues and provides sample e-commerce data
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CoreLDove Saleor GraphQL Proxy",
    description="GraphQL API proxy for CoreLDove frontend with RANK sorting fixes",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample product data
SAMPLE_PRODUCTS = [
    {
        "id": "UHJvZHVjdDox",
        "name": "Premium Wireless Headphones",
        "slug": "premium-wireless-headphones",
        "description": "High-quality wireless headphones with noise cancellation",
        "seoTitle": "Premium Wireless Headphones | CoreLDove",
        "seoDescription": "Experience superior sound quality with our premium wireless headphones",
        "thumbnail": {
            "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
            "alt": "Premium Wireless Headphones"
        },
        "media": [
            {
                "url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e",
                "alt": "Premium Wireless Headphones"
            }
        ],
        "category": {
            "id": "Q2F0ZWdvcnk6MQ==",
            "name": "Electronics",
            "slug": "electronics"
        },
        "variants": [
            {
                "id": "UHJvZHVjdFZhcmlhbnQ6MQ==",
                "name": "Black",
                "sku": "WH-001-BLK",
                "pricing": {
                    "priceRange": {
                        "start": {
                            "gross": {
                                "amount": 299.99,
                                "currency": "USD"
                            }
                        }
                    }
                },
                "quantityAvailable": 50
            }
        ],
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 299.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "isAvailable": True,
        "availableForPurchase": datetime.now().isoformat()
    },
    {
        "id": "UHJvZHVjdDoy",
        "name": "Ergonomic Office Chair",
        "slug": "ergonomic-office-chair",
        "description": "Comfortable ergonomic office chair for long work sessions",
        "seoTitle": "Ergonomic Office Chair | CoreLDove",
        "seoDescription": "Improve your work comfort with our ergonomic office chair",
        "thumbnail": {
            "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
            "alt": "Ergonomic Office Chair"
        },
        "media": [
            {
                "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
                "alt": "Ergonomic Office Chair"
            }
        ],
        "category": {
            "id": "Q2F0ZWdvcnk6Mg==",
            "name": "Furniture",
            "slug": "furniture"
        },
        "variants": [
            {
                "id": "UHJvZHVjdFZhcmlhbnQ6Mg==",
                "name": "Gray",
                "sku": "OC-001-GRY",
                "pricing": {
                    "priceRange": {
                        "start": {
                            "gross": {
                                "amount": 459.99,
                                "currency": "USD"
                            }
                        }
                    }
                },
                "quantityAvailable": 25
            }
        ],
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 459.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "isAvailable": True,
        "availableForPurchase": datetime.now().isoformat()
    },
    {
        "id": "UHJvZHVjdDoz",
        "name": "Smart Watch Pro",
        "slug": "smart-watch-pro",
        "description": "Advanced smartwatch with health monitoring and GPS",
        "seoTitle": "Smart Watch Pro | CoreLDove",
        "seoDescription": "Stay connected and healthy with our Smart Watch Pro",
        "thumbnail": {
            "url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
            "alt": "Smart Watch Pro"
        },
        "media": [
            {
                "url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
                "alt": "Smart Watch Pro"
            }
        ],
        "category": {
            "id": "Q2F0ZWdvcnk6MQ==",
            "name": "Electronics",
            "slug": "electronics"
        },
        "variants": [
            {
                "id": "UHJvZHVjdFZhcmlhbnQ6Mw==",
                "name": "Space Gray",
                "sku": "SW-001-SG",
                "pricing": {
                    "priceRange": {
                        "start": {
                            "gross": {
                                "amount": 399.99,
                                "currency": "USD"
                            }
                        }
                    }
                },
                "quantityAvailable": 30
            }
        ],
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 399.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "isAvailable": True,
        "availableForPurchase": datetime.now().isoformat()
    }
]

SAMPLE_CATEGORIES = [
    {
        "id": "Q2F0ZWdvcnk6MQ==",
        "name": "Electronics",
        "slug": "electronics",
        "description": "Latest electronic devices and gadgets",
        "backgroundImage": {
            "url": "https://images.unsplash.com/photo-1498049794561-7780e7231661",
            "alt": "Electronics Category"
        }
    },
    {
        "id": "Q2F0ZWdvcnk6Mg==",
        "name": "Furniture",
        "slug": "furniture",
        "description": "Modern and comfortable furniture for your home and office",
        "backgroundImage": {
            "url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
            "alt": "Furniture Category"
        }
    }
]

class GraphQLRequest(BaseModel):
    query: str
    variables: Optional[Dict[str, Any]] = None
    operationName: Optional[str] = None

def parse_graphql_query(query: str) -> Dict[str, Any]:
    """Parse GraphQL query to understand what data is being requested"""
    query_lower = query.lower()
    
    result = {
        "is_products_query": "products" in query_lower,
        "is_categories_query": "categories" in query_lower,
        "is_product_query": "product(" in query_lower,
        "has_search": "search:" in query_lower,
        "has_filter": "filter:" in query_lower,
        "has_sort": "sortby" in query_lower or "sort_by" in query_lower,
        "fields": []
    }
    
    # Extract requested fields (simplified parsing)
    if "name" in query_lower:
        result["fields"].append("name")
    if "description" in query_lower:
        result["fields"].append("description")
    if "thumbnail" in query_lower:
        result["fields"].append("thumbnail")
    if "pricing" in query_lower:
        result["fields"].append("pricing")
    if "category" in query_lower:
        result["fields"].append("category")
    
    return result

def filter_products(products: List[Dict], variables: Dict[str, Any] = None) -> List[Dict]:
    """Filter products based on GraphQL variables"""
    if not variables:
        return products
    
    filtered = products.copy()
    
    # Handle search filter
    if variables.get("filter", {}).get("search"):
        search_term = variables["filter"]["search"].lower()
        filtered = [
            p for p in filtered
            if search_term in p["name"].lower() or search_term in p["description"].lower()
        ]
    
    # Handle category filter
    if variables.get("filter", {}).get("categories"):
        category_ids = variables["filter"]["categories"]
        filtered = [
            p for p in filtered
            if p["category"]["id"] in category_ids
        ]
    
    # Handle price range filter
    if variables.get("filter", {}).get("price"):
        price_filter = variables["filter"]["price"]
        if price_filter.get("gte") is not None:
            min_price = price_filter["gte"]
            filtered = [
                p for p in filtered
                if p["pricing"]["priceRange"]["start"]["gross"]["amount"] >= min_price
            ]
        if price_filter.get("lte") is not None:
            max_price = price_filter["lte"]
            filtered = [
                p for p in filtered
                if p["pricing"]["priceRange"]["start"]["gross"]["amount"] <= max_price
            ]
    
    # Handle sorting (without RANK to avoid the error)
    sort_by = variables.get("sortBy")
    if sort_by:
        if sort_by.get("field") == "NAME":
            reverse_order = sort_by.get("direction") == "DESC"
            filtered.sort(key=lambda x: x["name"], reverse=reverse_order)
        elif sort_by.get("field") == "PRICE":
            reverse_order = sort_by.get("direction") == "DESC"
            filtered.sort(
                key=lambda x: x["pricing"]["priceRange"]["start"]["gross"]["amount"],
                reverse=reverse_order
            )
    
    return filtered

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "saleor-graphql-proxy", "timestamp": datetime.now().isoformat()}

@app.post("/graphql/")
async def graphql_proxy(request: GraphQLRequest):
    """Main GraphQL endpoint that handles queries from CoreLDove frontend"""
    try:
        logger.info(f"GraphQL Query: {request.query[:200]}...")
        
        query_info = parse_graphql_query(request.query)
        variables = request.variables or {}
        
        # Handle products query
        if query_info["is_products_query"]:
            products = filter_products(SAMPLE_PRODUCTS, variables)
            
            return {
                "data": {
                    "products": {
                        "edges": [
                            {
                                "node": product,
                                "cursor": f"cursor_{i}"
                            }
                            for i, product in enumerate(products)
                        ],
                        "pageInfo": {
                            "hasNextPage": False,
                            "hasPreviousPage": False,
                            "startCursor": "cursor_0" if products else None,
                            "endCursor": f"cursor_{len(products)-1}" if products else None
                        },
                        "totalCount": len(products)
                    }
                }
            }
        
        # Handle single product query
        elif query_info["is_product_query"]:
            # Extract product ID or slug from variables
            product_id = variables.get("id")
            product_slug = variables.get("slug")
            
            product = None
            if product_id:
                product = next((p for p in SAMPLE_PRODUCTS if p["id"] == product_id), None)
            elif product_slug:
                product = next((p for p in SAMPLE_PRODUCTS if p["slug"] == product_slug), None)
            
            return {
                "data": {
                    "product": product
                }
            }
        
        # Handle categories query
        elif query_info["is_categories_query"]:
            return {
                "data": {
                    "categories": {
                        "edges": [
                            {
                                "node": category,
                                "cursor": f"cursor_{i}"
                            }
                            for i, category in enumerate(SAMPLE_CATEGORIES)
                        ],
                        "pageInfo": {
                            "hasNextPage": False,
                            "hasPreviousPage": False,
                            "startCursor": "cursor_0",
                            "endCursor": f"cursor_{len(SAMPLE_CATEGORIES)-1}"
                        }
                    }
                }
            }
        
        # Handle introspection queries
        elif "__schema" in request.query or "__type" in request.query:
            # Return minimal schema for introspection
            return {
                "data": {
                    "__schema": {
                        "types": [
                            {"name": "Product"},
                            {"name": "Category"},
                            {"name": "ProductVariant"}
                        ]
                    }
                }
            }
        
        # Default response for unknown queries
        else:
            logger.warning(f"Unknown query type: {request.query[:100]}...")
            return {
                "data": {},
                "errors": [
                    {
                        "message": "Query type not implemented in proxy",
                        "extensions": {
                            "code": "NOT_IMPLEMENTED"
                        }
                    }
                ]
            }
            
    except Exception as e:
        logger.error(f"GraphQL Error: {str(e)}")
        return {
            "data": None,
            "errors": [
                {
                    "message": str(e),
                    "extensions": {
                        "code": "INTERNAL_ERROR"
                    }
                }
            ]
        }

@app.get("/graphql/")
async def graphql_playground():
    """GraphQL Playground for testing"""
    return {
        "message": "CoreLDove Saleor GraphQL Proxy",
        "endpoints": {
            "graphql": "/graphql/",
            "health": "/health"
        },
        "sample_products": len(SAMPLE_PRODUCTS),
        "sample_categories": len(SAMPLE_CATEGORIES),
        "note": "POST GraphQL queries to /graphql/ endpoint"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "CoreLDove Saleor GraphQL Proxy",
        "version": "1.0.0",
        "status": "running",
        "graphql_endpoint": "/graphql/",
        "health_endpoint": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "saleor-graphql-proxy:app",
        host="0.0.0.0",
        port=8024,
        reload=True,
        log_level="info"
    )