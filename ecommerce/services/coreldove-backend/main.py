from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

app = FastAPI(
    title="CorelDove E-commerce Brain API",
    description="Mock backend API for CorelDove e-commerce platform - Saleor compatible",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "https://coreldove.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class PriceInfo(BaseModel):
    amount: float
    currency: str

class PriceRange(BaseModel):
    start: Dict[str, PriceInfo]

class Pricing(BaseModel):
    priceRange: PriceRange

class Category(BaseModel):
    name: str
    slug: Optional[str] = None

class Thumbnail(BaseModel):
    url: str

class Product(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    pricing: Pricing
    thumbnail: Optional[Thumbnail] = None
    category: Optional[Category] = None
    rating: Optional[float] = 4.5
    reviews: Optional[int] = 100
    inStock: bool = True
    attributes: List[dict] = []

class CartLineItem(BaseModel):
    id: str
    productId: str
    quantity: int
    unitPrice: Dict[str, PriceInfo]
    totalPrice: Dict[str, PriceInfo]

class CartItem(BaseModel):
    productId: str
    quantity: int

class Address(BaseModel):
    firstName: str
    lastName: str
    streetAddress1: str
    city: str
    postalCode: str
    country: Dict[str, str]

class CheckoutData(BaseModel):
    email: str
    firstName: str
    lastName: str
    address: str
    city: str
    postalCode: str
    country: str
    items: List[CartItem]

class OrderLine(BaseModel):
    id: str
    productName: str
    quantity: int
    unitPrice: Dict[str, PriceInfo]
    totalPrice: Dict[str, PriceInfo]

class Order(BaseModel):
    id: str
    number: str
    token: str
    status: str
    paymentStatus: str
    created: str
    total: Dict[str, PriceInfo]
    lines: List[OrderLine]
    shippingAddress: Address
    billingAddress: Address

class OrderResponse(BaseModel):
    id: str
    status: str
    total: float
    currency: str
    created: datetime

# Mock data - Saleor compatible format
MOCK_PRODUCTS = [
    {
        "id": "fallback-1",
        "name": "Premium Wireless Headphones",
        "slug": "premium-wireless-headphones",
        "description": "High-quality wireless headphones with noise cancellation and premium sound quality.",
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 149.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "thumbnail": {
            "url": "/placeholder-product.jpg"
        },
        "category": {
            "name": "Electronics",
            "slug": "electronics"
        },
        "rating": 4.5,
        "reviews": 128,
        "inStock": True
    },
    {
        "id": "fallback-2",
        "name": "Organic Cotton T-Shirt",
        "slug": "organic-cotton-t-shirt",
        "description": "Comfortable and sustainable organic cotton t-shirt in various colors and sizes.",
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
            "url": "/placeholder-product.jpg"
        },
        "category": {
            "name": "Fashion",
            "slug": "fashion"
        },
        "rating": 4.2,
        "reviews": 64,
        "inStock": True
    },
    {
        "id": "fallback-3",
        "name": "Smart Plant Pot",
        "slug": "smart-plant-pot",
        "description": "Self-watering smart plant pot with built-in sensors and smartphone connectivity.",
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 79.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "thumbnail": {
            "url": "/placeholder-product.jpg"
        },
        "category": {
            "name": "Home & Garden",
            "slug": "home-garden"
        },
        "rating": 4.7,
        "reviews": 92,
        "inStock": True
    },
    {
        "id": "fallback-4",
        "name": "Bluetooth Speaker",
        "slug": "bluetooth-speaker",
        "description": "Portable wireless speaker with deep bass and 12-hour battery life.",
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 89.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "thumbnail": {
            "url": "/placeholder-product.jpg"
        },
        "category": {
            "name": "Electronics",
            "slug": "electronics"
        },
        "rating": 4.3,
        "reviews": 156,
        "inStock": True
    },
    {
        "id": "fallback-5",
        "name": "Designer Handbag",
        "slug": "designer-handbag",
        "description": "Elegant leather handbag with premium craftsmanship and timeless design.",
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 199.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "thumbnail": {
            "url": "/placeholder-product.jpg"
        },
        "category": {
            "name": "Fashion",
            "slug": "fashion"
        },
        "rating": 4.8,
        "reviews": 73,
        "inStock": True
    },
    {
        "id": "fallback-6",
        "name": "Garden Tool Set",
        "slug": "garden-tool-set",
        "description": "Complete set of premium gardening tools with ergonomic handles and storage case.",
        "pricing": {
            "priceRange": {
                "start": {
                    "gross": {
                        "amount": 124.99,
                        "currency": "USD"
                    }
                }
            }
        },
        "thumbnail": {
            "url": "/placeholder-product.jpg"
        },
        "category": {
            "name": "Home & Garden",
            "slug": "home-garden"
        },
        "rating": 4.6,
        "reviews": 89,
        "inStock": True
    }
]

# Mock categories
MOCK_CATEGORIES = [
    {"name": "Electronics", "slug": "electronics"},
    {"name": "Fashion", "slug": "fashion"},
    {"name": "Home & Garden", "slug": "home-garden"}
]

# Global cart storage (in production, this would be in database/redis)
MOCK_CARTS = {}

# API Endpoints
@app.get("/")
async def root():
    return {"message": "CorelDove E-commerce Brain API", "status": "running", "port": 8005}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "coreldove-backend", "port": 8005}

# Saleor-compatible Brain API endpoints
@app.get("/api/brain/saleor/products")
async def get_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(12, ge=1, le=100)
):
    """Get products with filtering"""
    products = MOCK_PRODUCTS.copy()

    # Filter by category
    if category:
        products = [p for p in products if p.get("category", {}).get("slug") == category]

    # Filter by search
    if search:
        search_lower = search.lower()
        products = [
            p for p in products
            if search_lower in p["name"].lower() or search_lower in p["description"].lower()
        ]

    # Apply limit
    products = products[:limit]

    return {
        "products": products,
        "count": len(products),
        "totalCount": len(MOCK_PRODUCTS),
        "hasNextPage": len(products) == limit and limit < len(MOCK_PRODUCTS),
        "source": "mock_backend"
    }

@app.get("/api/brain/saleor/products/{product_id}")
async def get_product(product_id: str):
    """Get product by ID"""
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product, "source": "mock_backend"}

@app.get("/api/brain/saleor/categories")
async def get_categories():
    """Get all product categories"""
    return {"categories": MOCK_CATEGORIES, "source": "mock_backend"}

@app.get("/api/brain/saleor/cart")
async def get_cart(cart_id: str = Query(...)):
    """Get cart contents"""
    cart = MOCK_CARTS.get(cart_id, {"lines": [], "totalPrice": {"gross": {"amount": 0.0, "currency": "USD"}}})
    return {"cart": cart, "source": "mock_backend"}

@app.post("/api/brain/saleor/cart")
async def create_cart():
    """Create new cart"""
    cart_id = str(uuid.uuid4())
    cart = {
        "id": cart_id,
        "lines": [],
        "totalPrice": {
            "gross": {
                "amount": 0.0,
                "currency": "USD"
            }
        }
    }
    MOCK_CARTS[cart_id] = cart
    return {"cart": cart, "source": "mock_backend"}

@app.post("/api/brain/saleor/cart/lines")
async def add_to_cart(cart_data: dict):
    """Add item to cart"""
    cart_id = cart_data.get("cartId")
    product_id = cart_data.get("productId")
    quantity = cart_data.get("quantity", 1)

    if not cart_id or not product_id:
        raise HTTPException(status_code=400, detail="Cart ID and Product ID required")

    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get or create cart
    cart = MOCK_CARTS.get(cart_id, {
        "id": cart_id,
        "lines": [],
        "totalPrice": {"gross": {"amount": 0.0, "currency": "USD"}}
    })

    # Check if product already in cart
    existing_line = next((line for line in cart["lines"] if line["productId"] == product_id), None)

    if existing_line:
        existing_line["quantity"] += quantity
    else:
        line = {
            "id": str(uuid.uuid4()),
            "productId": product_id,
            "quantity": quantity,
            "unitPrice": product["pricing"]["priceRange"]["start"],
            "totalPrice": {
                "gross": {
                    "amount": product["pricing"]["priceRange"]["start"]["gross"]["amount"] * quantity,
                    "currency": "USD"
                }
            },
            "product": product
        }
        cart["lines"].append(line)

    # Recalculate total
    total = sum(line["totalPrice"]["gross"]["amount"] for line in cart["lines"])
    cart["totalPrice"]["gross"]["amount"] = total

    MOCK_CARTS[cart_id] = cart

    return {"cart": cart, "source": "mock_backend"}

@app.delete("/api/brain/saleor/cart/lines/{line_id}")
async def remove_from_cart(line_id: str, cart_id: str = Query(...)):
    """Remove item from cart"""
    cart = MOCK_CARTS.get(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart["lines"] = [line for line in cart["lines"] if line["id"] != line_id]

    # Recalculate total
    total = sum(line["totalPrice"]["gross"]["amount"] for line in cart["lines"])
    cart["totalPrice"]["gross"]["amount"] = total

    MOCK_CARTS[cart_id] = cart

    return {"cart": cart, "source": "mock_backend"}

@app.get("/api/brain/saleor/orders")
async def get_orders(user_id: Optional[str] = None, order_id: Optional[str] = None):
    """Get user orders"""
    # Mock order data
    orders = [{
        "id": "fallback-order-1",
        "number": "CD-001",
        "token": "fallback-order-token-1",
        "status": "FULFILLED",
        "paymentStatus": "FULLY_CHARGED",
        "created": datetime.now().isoformat(),
        "total": {
            "gross": {
                "amount": 199.99,
                "currency": "USD"
            }
        },
        "lines": [{
            "id": "line-1",
            "productName": "Premium Wireless Headphones",
            "quantity": 1,
            "unitPrice": {
                "gross": {
                    "amount": 199.99,
                    "currency": "USD"
                }
            },
            "totalPrice": {
                "gross": {
                    "amount": 199.99,
                    "currency": "USD"
                }
            }
        }],
        "shippingAddress": {
            "firstName": "John",
            "lastName": "Doe",
            "streetAddress1": "123 Main St",
            "city": "New York",
            "postalCode": "10001",
            "country": {
                "code": "US",
                "country": "United States"
            }
        },
        "billingAddress": {
            "firstName": "John",
            "lastName": "Doe",
            "streetAddress1": "123 Main St",
            "city": "New York",
            "postalCode": "10001",
            "country": {
                "code": "US",
                "country": "United States"
            }
        }
    }]

    if order_id:
        orders = [order for order in orders if order["id"] == order_id]

    return {
        "orders": orders,
        "totalCount": len(orders),
        "source": "mock_backend"
    }

@app.post("/api/brain/saleor/orders")
async def create_order(order_data: dict):
    """Create order from checkout"""
    cart_id = order_data.get("cartId")
    shipping_address = order_data.get("shippingAddress", {})
    billing_address = order_data.get("billingAddress", {})

    cart = MOCK_CARTS.get(cart_id, {"lines": [], "totalPrice": {"gross": {"amount": 0.0, "currency": "USD"}}})

    order = {
        "id": str(uuid.uuid4()),
        "number": f"CD-{len(MOCK_CARTS) + 1:03d}",
        "token": str(uuid.uuid4()),
        "status": "UNFULFILLED",
        "paymentStatus": "NOT_CHARGED",
        "created": datetime.now().isoformat(),
        "total": cart["totalPrice"],
        "lines": [
            {
                "id": line["id"],
                "productName": line["product"]["name"],
                "quantity": line["quantity"],
                "unitPrice": line["unitPrice"],
                "totalPrice": line["totalPrice"]
            }
            for line in cart["lines"]
        ],
        "shippingAddress": shipping_address,
        "billingAddress": billing_address or shipping_address
    }

    return {"order": order, "source": "mock_backend"}

@app.get("/api/brain/saleor/auth")
async def get_auth_status():
    """Get authentication status"""
    return {
        "user": None,
        "isAuthenticated": False,
        "source": "mock_backend"
    }

@app.post("/api/brain/saleor/auth")
async def authenticate(auth_data: dict):
    """Authenticate user"""
    return {
        "user": {
            "id": "mock-user-1",
            "email": auth_data.get("email", "user@example.com"),
            "firstName": "Mock",
            "lastName": "User"
        },
        "token": "mock-jwt-token",
        "isAuthenticated": True,
        "source": "mock_backend"
    }

@app.get("/api/brain/saleor/shipping")
async def get_shipping_methods():
    """Get available shipping methods"""
    return {
        "shippingMethods": [
            {
                "id": "standard",
                "name": "Standard Shipping",
                "description": "5-7 business days",
                "price": {
                    "amount": 9.99,
                    "currency": "USD"
                }
            },
            {
                "id": "express",
                "name": "Express Shipping",
                "description": "2-3 business days",
                "price": {
                    "amount": 19.99,
                    "currency": "USD"
                }
            }
        ],
        "source": "mock_backend"
    }

@app.get("/api/brain/saleor/wishlist")
async def get_wishlist(user_id: Optional[str] = None):
    """Get user wishlist"""
    return {
        "wishlist": {
            "id": "mock-wishlist-1",
            "items": [],
            "totalCount": 0
        },
        "source": "mock_backend"
    }

@app.get("/api/brain/saleor/discounts")
async def get_discounts():
    """Get available discounts"""
    return {
        "discounts": [
            {
                "id": "welcome10",
                "name": "Welcome Discount",
                "value": 10,
                "type": "PERCENTAGE"
            }
        ],
        "source": "mock_backend"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)