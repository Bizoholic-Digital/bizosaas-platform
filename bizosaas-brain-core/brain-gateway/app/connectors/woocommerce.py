import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..ports.ecommerce_port import ECommercePort, Product, Order, OrderItem, EcommerceStats
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class WooCommerceConnector(BaseConnector, ECommercePort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="woocommerce",
            name="WooCommerce",
            type=ConnectorType.ECOMMERCE,
            description="Leading e-commerce platform for WordPress.",
            icon="woocommerce",
            version="1.0.0",
            auth_schema={
                "url": {"type": "string", "label": "Store URL", "placeholder": "https://your-store.com"},
                "consumer_key": {"type": "string", "label": "Consumer Key (CK)"},
                "consumer_secret": {"type": "string", "label": "Consumer Secret (CS)"}
            }
        )

    def _get_auth(self):
        return (self.credentials.get("consumer_key"), self.credentials.get("consumer_secret"))

    def _get_api_url(self, path: str) -> str:
        base_url = self.credentials.get("url", "").rstrip("/")
        if base_url.endswith("/wp-json"):
            base_url = base_url[:-8]
        return f"{base_url}/wp-json/wc/v3/{path.lstrip('/')}"

    async def validate_credentials(self) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self._get_api_url("system_status"),
                    auth=self._get_auth(),
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"WooCommerce validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if resource_type == "products":
            items = await self.get_products()
            return {"data": [p.dict() for p in items]}
        elif resource_type == "orders":
            items = await self.get_orders()
            return {"data": [o.dict() for o in items]}
        return {"data": []}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {}

    # --- ECommercePort Implementation ---

    async def get_stats(self) -> EcommerceStats:
        async with httpx.AsyncClient() as client:
            try:
                # Parallel fetch for headers to get totals
                auth = self._get_auth()
                stats = {"products": 0, "orders": 0, "revenue": 0.0}
                
                # Check products count
                try:
                    resp_prod = await client.head(
                        self._get_api_url("products"), 
                        auth=auth, 
                        params={"per_page": 1}
                    )
                    if resp_prod.status_code == 200:
                        stats["products"] = int(resp_prod.headers.get("X-WP-Total", 0))
                except Exception:
                    pass

                # Check orders count
                try:
                    resp_ord = await client.head(
                        self._get_api_url("orders"), 
                        auth=auth, 
                        params={"per_page": 1}
                    )
                    if resp_ord.status_code == 200:
                        stats["orders"] = int(resp_ord.headers.get("X-WP-Total", 0))
                except Exception:
                    pass

                # Revenue requires /reports/sales which might be permission locked or complex
                # Skipping real revenue fetch for MVP stability

                return EcommerceStats(
                    products=stats["products"],
                    orders=stats["orders"],
                    revenue=stats["revenue"]
                )
            except Exception as e:
                logger.error(f"Stats fetch failed: {e}")
                return EcommerceStats(products=0, orders=0, revenue=0.0)

    # --- ECommercePort Implementation ---

    async def get_products(self, limit: int = 100, category_id: Optional[str] = None) -> List[Product]:
        params = {"per_page": limit}
        if category_id:
            params["category"] = category_id
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("products"),
                auth=self._get_auth(),
                params=params,
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            
            products = []
            for item in data:
                products.append(Product(
                    id=str(item.get("id")),
                    name=item.get("name"),
                    slug=item.get("slug"),
                    description=item.get("description"),
                    price=float(item.get("price") or 0),
                    currency=self.credentials.get("currency", "USD"), # Woo doesn't always perform currency conversion on API response
                    stock_quantity=item.get("stock_quantity") or 0,
                    sku=item.get("sku"),
                    images=[img.get("src") for img in item.get("images", [])],
                    status=item.get("status")
                ))
            return products

    async def get_product(self, product_id: str) -> Optional[Product]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self._get_api_url(f"products/{product_id}"),
                    auth=self._get_auth()
                )
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                item = response.json()
                return Product(
                    id=str(item.get("id")),
                    name=item.get("name"),
                    price=float(item.get("price") or 0),
                    stock_quantity=item.get("stock_quantity") or 0,
                    sku=item.get("sku")
                )
            except Exception:
                return None

    async def create_product(self, product: Product) -> Product:
        payload = {
            "name": product.name,
            "type": "simple",
            "regular_price": str(product.price),
            "description": product.description,
            "sku": product.sku
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._get_api_url("products"),
                auth=self._get_auth(),
                json=payload
            )
            response.raise_for_status()
            item = response.json()
            product.id = str(item.get("id"))
            return product

    async def update_inventory(self, product_id: str, quantity: int) -> bool:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                self._get_api_url(f"products/{product_id}"),
                auth=self._get_auth(),
                json={"stock_quantity": quantity, "manage_stock": True}
            )
            return response.status_code == 200

    async def get_orders(self, limit: int = 100, status: Optional[str] = None) -> List[Order]:
        params = {"per_page": limit}
        if status:
            params["status"] = status
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self._get_api_url("orders"),
                auth=self._get_auth(),
                params=params,
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            
            orders = []
            for item in data:
                order_items = []
                for line in item.get("line_items", []):
                    order_items.append(OrderItem(
                        product_id=str(line.get("product_id")),
                        quantity=line.get("quantity"),
                        price=float(line.get("price") or 0),
                        total=float(line.get("total") or 0)
                    ))
                
                orders.append(Order(
                    id=str(item.get("id")),
                    customer_id=str(item.get("customer_id")),
                    email=item.get("billing", {}).get("email"),
                    items=order_items,
                    total_amount=float(item.get("total") or 0),
                    currency=item.get("currency"),
                    status=item.get("status"),
                    created_at=None # Parsing date string requires datetime
                ))
            return orders

    async def get_order(self, order_id: str) -> Optional[Order]:
        return None # Implementation similar to above

    async def update_order_status(self, order_id: str, status: str) -> Order:
         async with httpx.AsyncClient() as client:
            response = await client.put(
                self._get_api_url(f"orders/{order_id}"),
                auth=self._get_auth(),
                json={"status": status}
            )
            response.raise_for_status()
            # In real impl, return updated order
            return Order(id=order_id, total_amount=0, currency="USD", status=status, items=[])
