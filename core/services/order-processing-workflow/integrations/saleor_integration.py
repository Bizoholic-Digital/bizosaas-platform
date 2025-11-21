"""
Saleor E-commerce Integration
Integrates with existing Saleor backend via /api/brain/saleor/
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
import json

logger = logging.getLogger(__name__)


class SaleorIntegration:
    """
    Saleor e-commerce platform integration
    Syncs orders, products, and inventory with existing Saleor installation
    """
    
    def __init__(self):
        self.config = {
            "saleor_api_url": "http://localhost:8000/api/brain/saleor",
            "graphql_endpoint": "/graphql/",
            "webhook_endpoint": "/webhooks/",
            "api_token": "",  # Configure in production
            "sync_enabled": True,
            "real_time_sync": True,
            "batch_sync_interval": 3600,  # 1 hour
            "webhook_secret": "your-webhook-secret",
            "timeout": 30
        }
        
        # GraphQL queries and mutations
        self.queries = {
            "get_orders": """
                query GetOrders($first: Int, $after: String) {
                    orders(first: $first, after: $after) {
                        edges {
                            node {
                                id
                                number
                                status
                                created
                                total {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                                user {
                                    email
                                    firstName
                                    lastName
                                }
                                shippingAddress {
                                    firstName
                                    lastName
                                    streetAddress1
                                    streetAddress2
                                    city
                                    postalCode
                                    country {
                                        code
                                    }
                                    phone
                                }
                                billingAddress {
                                    firstName
                                    lastName
                                    streetAddress1
                                    streetAddress2
                                    city
                                    postalCode
                                    country {
                                        code
                                    }
                                    phone
                                }
                                lines {
                                    id
                                    quantity
                                    productName
                                    variantName
                                    unitPrice {
                                        gross {
                                            amount
                                            currency
                                        }
                                    }
                                    totalPrice {
                                        gross {
                                            amount
                                            currency
                                        }
                                    }
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            """,
            
            "get_order": """
                query GetOrder($id: ID!) {
                    order(id: $id) {
                        id
                        number
                        status
                        created
                        total {
                            gross {
                                amount
                                currency
                            }
                        }
                        user {
                            email
                            firstName
                            lastName
                        }
                        shippingAddress {
                            firstName
                            lastName
                            streetAddress1
                            streetAddress2
                            city
                            postalCode
                            country {
                                code
                            }
                            phone
                        }
                        billingAddress {
                            firstName
                            lastName
                            streetAddress1
                            streetAddress2
                            city
                            postalCode
                            country {
                                code
                            }
                            phone
                        }
                        lines {
                            id
                            quantity
                            productName
                            variantName
                            variant {
                                id
                                sku
                                product {
                                    id
                                    name
                                }
                            }
                            unitPrice {
                                gross {
                                    amount
                                    currency
                                }
                            }
                            totalPrice {
                                gross {
                                    amount
                                    currency
                                }
                            }
                        }
                        fulfillments {
                            id
                            status
                            trackingNumber
                            lines {
                                quantity
                                orderLine {
                                    id
                                }
                            }
                        }
                    }
                }
            """,
            
            "get_products": """
                query GetProducts($first: Int, $after: String) {
                    products(first: $first, after: $after) {
                        edges {
                            node {
                                id
                                name
                                slug
                                description
                                variants {
                                    id
                                    sku
                                    name
                                    pricing {
                                        price {
                                            gross {
                                                amount
                                                currency
                                            }
                                        }
                                    }
                                    quantityAvailable
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
            """
        }
        
        self.mutations = {
            "update_order_status": """
                mutation UpdateOrder($id: ID!, $input: OrderUpdateInput!) {
                    orderUpdate(id: $id, input: $input) {
                        order {
                            id
                            status
                        }
                        errors {
                            field
                            message
                        }
                    }
                }
            """,
            
            "create_fulfillment": """
                mutation CreateFulfillment($order: ID!, $input: FulfillmentCreateInput!) {
                    orderFulfillmentCreate(order: $order, input: $input) {
                        fulfillment {
                            id
                            status
                            trackingNumber
                        }
                        errors {
                            field
                            message
                        }
                    }
                }
            """,
            
            "update_inventory": """
                mutation UpdateVariantStock($id: ID!, $input: ProductVariantStocksUpdateInput!) {
                    productVariantStocksUpdate(variantId: $id, stocks: $input) {
                        productVariant {
                            id
                            quantityAvailable
                        }
                        errors {
                            field
                            message
                        }
                    }
                }
            """
        }
        
        # Cache for reducing API calls
        self.cache = {
            "products": {},
            "orders": {},
            "last_sync": None
        }
        
    async def initialize(self):
        """Initialize Saleor integration"""
        logger.info("Initializing Saleor Integration...")
        
        try:
            # Test connection
            await self._test_connection()
            
            if self.config["sync_enabled"]:
                # Start background sync
                asyncio.create_task(self._background_sync())
            
            logger.info("Saleor Integration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Saleor Integration: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup Saleor integration"""
        logger.info("Shutting down Saleor Integration...")
    
    async def sync_order_to_saleor(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Sync order information to Saleor"""
        logger.info(f"Syncing order {order.get('id')} to Saleor")
        
        try:
            # Check if order exists in Saleor
            saleor_order = await self._get_saleor_order(order.get("saleor_id"))
            
            if saleor_order:
                # Update existing order
                result = await self._update_saleor_order_status(
                    saleor_order["id"],
                    order["status"]
                )
            else:
                # Create new order (if needed)
                # Note: Usually orders come FROM Saleor, but this handles edge cases
                result = await self._create_saleor_order(order)
            
            return {
                "success": True,
                "saleor_order_id": result.get("id"),
                "synced_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Saleor order sync failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sync_fulfillment_to_saleor(self, order_id: str, fulfillment: Dict[str, Any]) -> Dict[str, Any]:
        """Sync fulfillment information to Saleor"""
        logger.info(f"Syncing fulfillment to Saleor for order {order_id}")
        
        try:
            # Get Saleor order ID
            saleor_order_id = await self._get_saleor_order_id(order_id)
            
            if not saleor_order_id:
                raise Exception(f"Saleor order not found for order {order_id}")
            
            # Create fulfillment in Saleor
            fulfillment_input = {
                "lines": [
                    {
                        "orderLineId": item["order_item_id"],
                        "quantity": item["quantity"]
                    }
                    for item in fulfillment.get("items", [])
                ],
                "trackingNumber": fulfillment.get("tracking_number"),
                "notifyCustomer": True
            }
            
            result = await self._execute_mutation(
                "create_fulfillment",
                {"order": saleor_order_id, "input": fulfillment_input}
            )
            
            if result.get("errors"):
                raise Exception(f"Saleor fulfillment creation failed: {result['errors']}")
            
            return {
                "success": True,
                "saleor_fulfillment_id": result["fulfillment"]["id"],
                "synced_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Saleor fulfillment sync failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sync_inventory_to_saleor(self, inventory_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sync inventory updates to Saleor"""
        logger.info(f"Syncing {len(inventory_updates)} inventory updates to Saleor")
        
        try:
            synced_count = 0
            failed_updates = []
            
            for update in inventory_updates:
                try:
                    # Get Saleor variant ID
                    variant_id = await self._get_saleor_variant_id(
                        update["product_id"],
                        update.get("variant_id")
                    )
                    
                    if variant_id:
                        # Update stock in Saleor
                        stock_input = [{
                            "warehouse": update.get("warehouse_id", "default"),
                            "quantity": update["new_quantity"]
                        }]
                        
                        result = await self._execute_mutation(
                            "update_inventory",
                            {"id": variant_id, "input": stock_input}
                        )
                        
                        if not result.get("errors"):
                            synced_count += 1
                        else:
                            failed_updates.append({
                                "product_id": update["product_id"],
                                "error": result["errors"]
                            })
                    
                except Exception as e:
                    failed_updates.append({
                        "product_id": update["product_id"],
                        "error": str(e)
                    })
            
            return {
                "success": True,
                "synced_count": synced_count,
                "failed_count": len(failed_updates),
                "failed_updates": failed_updates
            }
            
        except Exception as e:
            logger.error(f"Saleor inventory sync failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_orders_from_saleor(self, limit: int = 50, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get orders from Saleor"""
        logger.info(f"Fetching orders from Saleor (limit: {limit})")
        
        try:
            result = await self._execute_query(
                "get_orders",
                {"first": limit}
            )
            
            orders = []
            
            for edge in result.get("orders", {}).get("edges", []):
                order_node = edge["node"]
                
                # Convert Saleor order to our format
                converted_order = await self._convert_saleor_order(order_node)
                
                # Apply status filter if provided
                if not status_filter or converted_order["status"] == status_filter:
                    orders.append(converted_order)
            
            return orders
            
        except Exception as e:
            logger.error(f"Failed to fetch orders from Saleor: {e}")
            return []
    
    async def get_products_from_saleor(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get products from Saleor"""
        logger.info(f"Fetching products from Saleor (limit: {limit})")
        
        try:
            result = await self._execute_query(
                "get_products",
                {"first": limit}
            )
            
            products = []
            
            for edge in result.get("products", {}).get("edges", []):
                product_node = edge["node"]
                
                # Convert Saleor product to our format
                converted_product = await self._convert_saleor_product(product_node)
                products.append(converted_product)
            
            return products
            
        except Exception as e:
            logger.error(f"Failed to fetch products from Saleor: {e}")
            return []
    
    async def handle_saleor_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming Saleor webhook"""
        logger.info(f"Handling Saleor webhook: {event_type}")
        
        try:
            if event_type == "order_created":
                # New order from Saleor
                await self._handle_order_created(payload)
            
            elif event_type == "order_updated":
                # Order status change from Saleor
                await self._handle_order_updated(payload)
            
            elif event_type == "order_cancelled":
                # Order cancellation from Saleor
                await self._handle_order_cancelled(payload)
            
            elif event_type == "product_created":
                # New product from Saleor
                await self._handle_product_created(payload)
            
            elif event_type == "product_updated":
                # Product update from Saleor
                await self._handle_product_updated(payload)
            
            return {
                "success": True,
                "event_type": event_type,
                "processed_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Webhook handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_health(self) -> Dict[str, Any]:
        """Get Saleor integration health status"""
        
        try:
            # Test connection
            connection_test = await self._test_connection()
            
            return {
                "status": "healthy" if connection_test else "unhealthy",
                "connection": connection_test,
                "sync_enabled": self.config["sync_enabled"],
                "last_sync": self.cache.get("last_sync"),
                "cached_orders": len(self.cache.get("orders", {})),
                "cached_products": len(self.cache.get("products", {}))
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    # Private helper methods
    
    async def _test_connection(self) -> bool:
        """Test connection to Saleor"""
        
        try:
            # Simple query to test connection
            result = await self._execute_query(
                "get_orders",
                {"first": 1}
            )
            
            return result is not None
            
        except Exception as e:
            logger.error(f"Saleor connection test failed: {e}")
            return False
    
    async def _execute_query(self, query_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GraphQL query"""
        
        if query_name not in self.queries:
            raise Exception(f"Query {query_name} not found")
        
        query = self.queries[query_name]
        
        return await self._make_graphql_request(query, variables)
    
    async def _execute_mutation(self, mutation_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GraphQL mutation"""
        
        if mutation_name not in self.mutations:
            raise Exception(f"Mutation {mutation_name} not found")
        
        mutation = self.mutations[mutation_name]
        
        return await self._make_graphql_request(mutation, variables)
    
    async def _make_graphql_request(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Make GraphQL request to Saleor"""
        
        url = f"{self.config['saleor_api_url']}{self.config['graphql_endpoint']}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_token']}"
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config["timeout"])) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        if "errors" in result:
                            raise Exception(f"GraphQL errors: {result['errors']}")
                        
                        return result.get("data", {})
                    else:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")
                        
        except Exception as e:
            logger.error(f"GraphQL request failed: {e}")
            raise
    
    async def _get_saleor_order(self, saleor_order_id: str) -> Optional[Dict[str, Any]]:
        """Get order from Saleor by ID"""
        
        if not saleor_order_id:
            return None
        
        try:
            result = await self._execute_query(
                "get_order",
                {"id": saleor_order_id}
            )
            
            return result.get("order")
            
        except Exception as e:
            logger.error(f"Failed to get Saleor order {saleor_order_id}: {e}")
            return None
    
    async def _get_saleor_order_id(self, order_id: str) -> Optional[str]:
        """Get Saleor order ID from our order ID"""
        
        # In production, this would look up the mapping in database
        # For demo, we'll simulate
        return f"saleor_order_{order_id}"
    
    async def _get_saleor_variant_id(self, product_id: str, variant_id: Optional[str] = None) -> Optional[str]:
        """Get Saleor variant ID from our product/variant ID"""
        
        # In production, this would look up the mapping in database
        # For demo, we'll simulate
        if variant_id:
            return f"saleor_variant_{variant_id}"
        else:
            return f"saleor_variant_{product_id}_default"
    
    async def _update_saleor_order_status(self, saleor_order_id: str, status: str) -> Dict[str, Any]:
        """Update order status in Saleor"""
        
        # Map our status to Saleor status
        saleor_status_map = {
            "pending": "UNFULFILLED",
            "processing": "UNFULFILLED",
            "shipped": "PARTIALLY_FULFILLED",
            "delivered": "FULFILLED",
            "cancelled": "CANCELED",
            "refunded": "RETURNED"
        }
        
        saleor_status = saleor_status_map.get(status, "UNFULFILLED")
        
        result = await self._execute_mutation(
            "update_order_status",
            {
                "id": saleor_order_id,
                "input": {"status": saleor_status}
            }
        )
        
        if result.get("errors"):
            raise Exception(f"Failed to update Saleor order status: {result['errors']}")
        
        return result["order"]
    
    async def _create_saleor_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Create order in Saleor (rarely needed)"""
        
        # This would be implemented if we need to create orders in Saleor
        # from our system (uncommon scenario)
        logger.info(f"Creating order in Saleor for order {order['id']}")
        
        # Placeholder implementation
        return {"id": f"saleor_order_{order['id']}"}
    
    async def _convert_saleor_order(self, saleor_order: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Saleor order format to our format"""
        
        # Convert Saleor order structure to our order structure
        converted_order = {
            "id": f"converted_{saleor_order['id']}",
            "saleor_id": saleor_order["id"],
            "order_number": saleor_order["number"],
            "status": self._map_saleor_status(saleor_order["status"]),
            "customer_id": saleor_order.get("user", {}).get("email", "unknown"),
            "items": [],
            "billing_address": self._convert_saleor_address(saleor_order.get("billingAddress")),
            "shipping_address": self._convert_saleor_address(saleor_order.get("shippingAddress")),
            "pricing": {
                "total": saleor_order["total"]["gross"]["amount"],
                "currency": saleor_order["total"]["gross"]["currency"],
                "subtotal": saleor_order["total"]["gross"]["amount"],  # Simplified
                "tax_total": 0,
                "shipping_total": 0
            },
            "created_at": saleor_order["created"],
            "updated_at": datetime.utcnow(),
            "source": "saleor"
        }
        
        # Convert order lines
        for line in saleor_order.get("lines", []):
            item = {
                "id": line["id"],
                "product_id": line.get("variant", {}).get("product", {}).get("id", "unknown"),
                "variant_id": line.get("variant", {}).get("id"),
                "sku": line.get("variant", {}).get("sku", "unknown"),
                "name": line["productName"],
                "quantity": line["quantity"],
                "unit_price": line["unitPrice"]["gross"]["amount"],
                "total_price": line["totalPrice"]["gross"]["amount"]
            }
            converted_order["items"].append(item)
        
        return converted_order
    
    async def _convert_saleor_product(self, saleor_product: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Saleor product format to our format"""
        
        converted_product = {
            "id": f"converted_{saleor_product['id']}",
            "saleor_id": saleor_product["id"],
            "name": saleor_product["name"],
            "slug": saleor_product["slug"],
            "description": saleor_product.get("description", ""),
            "variants": [],
            "source": "saleor"
        }
        
        # Convert variants
        for variant in saleor_product.get("variants", []):
            converted_variant = {
                "id": f"converted_{variant['id']}",
                "saleor_id": variant["id"],
                "sku": variant["sku"],
                "name": variant["name"],
                "price": variant["pricing"]["price"]["gross"]["amount"],
                "currency": variant["pricing"]["price"]["gross"]["currency"],
                "quantity_available": variant.get("quantityAvailable", 0)
            }
            converted_product["variants"].append(converted_variant)
        
        return converted_product
    
    def _convert_saleor_address(self, saleor_address: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert Saleor address format to our format"""
        
        if not saleor_address:
            return {}
        
        return {
            "first_name": saleor_address.get("firstName", ""),
            "last_name": saleor_address.get("lastName", ""),
            "address_line_1": saleor_address.get("streetAddress1", ""),
            "address_line_2": saleor_address.get("streetAddress2", ""),
            "city": saleor_address.get("city", ""),
            "postal_code": saleor_address.get("postalCode", ""),
            "country": saleor_address.get("country", {}).get("code", ""),
            "phone": saleor_address.get("phone", "")
        }
    
    def _map_saleor_status(self, saleor_status: str) -> str:
        """Map Saleor order status to our status"""
        
        status_map = {
            "DRAFT": "pending",
            "UNCONFIRMED": "pending",
            "UNFULFILLED": "processing",
            "PARTIALLY_FULFILLED": "shipped",
            "FULFILLED": "delivered",
            "CANCELED": "cancelled",
            "RETURNED": "refunded"
        }
        
        return status_map.get(saleor_status, "pending")
    
    # Webhook handlers
    
    async def _handle_order_created(self, payload: Dict[str, Any]):
        """Handle order created webhook"""
        logger.info(f"Handling order created webhook")
        
        # Convert Saleor order and add to our system
        # This would trigger our order processing workflow
        pass
    
    async def _handle_order_updated(self, payload: Dict[str, Any]):
        """Handle order updated webhook"""
        logger.info(f"Handling order updated webhook")
        
        # Update order in our system
        pass
    
    async def _handle_order_cancelled(self, payload: Dict[str, Any]):
        """Handle order cancelled webhook"""
        logger.info(f"Handling order cancelled webhook")
        
        # Cancel order in our system
        pass
    
    async def _handle_product_created(self, payload: Dict[str, Any]):
        """Handle product created webhook"""
        logger.info(f"Handling product created webhook")
        
        # Add product to our inventory system
        pass
    
    async def _handle_product_updated(self, payload: Dict[str, Any]):
        """Handle product updated webhook"""
        logger.info(f"Handling product updated webhook")
        
        # Update product in our inventory system
        pass
    
    async def _background_sync(self):
        """Background task for periodic sync"""
        
        while True:
            try:
                logger.info("Starting background sync with Saleor")
                
                # Sync orders
                orders = await self.get_orders_from_saleor(limit=100)
                logger.info(f"Synced {len(orders)} orders from Saleor")
                
                # Sync products
                products = await self.get_products_from_saleor(limit=100)
                logger.info(f"Synced {len(products)} products from Saleor")
                
                # Update cache
                self.cache["last_sync"] = datetime.utcnow()
                
                await asyncio.sleep(self.config["batch_sync_interval"])
                
            except Exception as e:
                logger.error(f"Background sync failed: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry