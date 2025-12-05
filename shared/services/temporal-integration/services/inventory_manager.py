"""
Inventory Management Service
Handles real-time inventory tracking, reservation, and optimization
"""

import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any, Set
from uuid import uuid4

logger = logging.getLogger(__name__)


class InventoryManager:
    """
    Comprehensive inventory management service
    Handles stock tracking, reservations, multi-location inventory, and reorder automation
    """
    
    def __init__(self):
        self.config = {
            "reservation_timeout": 1800,  # 30 minutes
            "low_stock_threshold": 10,
            "reorder_threshold": 5,
            "enable_auto_reorder": True,
            "enable_backorder": True,
            "max_backorder_days": 30
        }
        
        # In-memory storage (replace with database in production)
        self.inventory = {}  # product_id -> inventory data
        self.reservations = {}  # reservation_id -> reservation data
        self.warehouses = {}  # warehouse_id -> warehouse data
        self.suppliers = {}  # supplier_id -> supplier data
        self.reorder_rules = {}  # product_id -> reorder rules
        
        # Initialize sample data
        self._initialize_sample_data()
    
    async def initialize(self):
        """Initialize inventory manager"""
        logger.info("Initializing Inventory Manager...")
        
        try:
            # Initialize warehouse connections
            await self._initialize_warehouses()
            
            # Start background tasks
            asyncio.create_task(self._cleanup_expired_reservations())
            asyncio.create_task(self._monitor_stock_levels())
            
            logger.info("Inventory Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Inventory Manager: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup inventory manager"""
        logger.info("Shutting down Inventory Manager...")
    
    async def reserve_inventory(self, order_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Reserve inventory for order items
        
        Args:
            order_id: Order identifier
            items: List of order items to reserve
            
        Returns:
            Dict with reservation result
        """
        logger.info(f"Reserving inventory for order {order_id}")
        
        try:
            reservation_id = str(uuid4())
            reserved_items = []
            backorder_items = []
            insufficient_items = []
            
            for item in items:
                product_id = item["product_id"]
                variant_id = item.get("variant_id")
                quantity_needed = item["quantity"]
                
                # Get inventory key
                inventory_key = f"{product_id}:{variant_id}" if variant_id else product_id
                
                if inventory_key not in self.inventory:
                    insufficient_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "requested": quantity_needed,
                        "available": 0,
                        "reason": "Product not found"
                    })
                    continue
                
                inventory_data = self.inventory[inventory_key]
                available_stock = await self._get_available_stock(inventory_key)
                
                if available_stock >= quantity_needed:
                    # Reserve from available stock
                    await self._create_reservation(
                        reservation_id, order_id, inventory_key, quantity_needed
                    )
                    
                    reserved_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "quantity": quantity_needed,
                        "warehouse_id": inventory_data["primary_warehouse"],
                        "reserved_at": datetime.utcnow()
                    })
                    
                elif self.config["enable_backorder"] and available_stock > 0:
                    # Partial reservation with backorder
                    await self._create_reservation(
                        reservation_id, order_id, inventory_key, available_stock
                    )
                    
                    reserved_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "quantity": available_stock,
                        "warehouse_id": inventory_data["primary_warehouse"],
                        "reserved_at": datetime.utcnow()
                    })
                    
                    backorder_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "quantity": quantity_needed - available_stock,
                        "estimated_date": await self._estimate_restock_date(inventory_key)
                    })
                    
                elif self.config["enable_backorder"]:
                    # Full backorder
                    backorder_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "quantity": quantity_needed,
                        "estimated_date": await self._estimate_restock_date(inventory_key)
                    })
                    
                else:
                    # Insufficient stock and backorder disabled
                    insufficient_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "requested": quantity_needed,
                        "available": available_stock,
                        "reason": "Insufficient stock"
                    })
            
            # Check if reservation is successful
            success = len(insufficient_items) == 0
            
            if success:
                # Store reservation
                self.reservations[reservation_id] = {
                    "id": reservation_id,
                    "order_id": order_id,
                    "items": reserved_items,
                    "backorder_items": backorder_items,
                    "created_at": datetime.utcnow(),
                    "expires_at": datetime.utcnow() + timedelta(seconds=self.config["reservation_timeout"]),
                    "status": "active"
                }
                
                # Trigger auto-reorder if needed
                if self.config["enable_auto_reorder"]:
                    await self._check_reorder_triggers(items)
            
            return {
                "success": success,
                "reservation_id": reservation_id if success else None,
                "reserved_items": reserved_items,
                "backorder_items": backorder_items,
                "insufficient_items": insufficient_items,
                "total_reserved": len(reserved_items),
                "total_backorder": len(backorder_items),
                "message": "Inventory reserved successfully" if success else "Partial or failed reservation"
            }
            
        except Exception as e:
            logger.error(f"Inventory reservation failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def release_reservation(self, order_id: str) -> Dict[str, Any]:
        """Release inventory reservation for an order"""
        logger.info(f"Releasing inventory reservation for order {order_id}")
        
        try:
            # Find reservations for this order
            reservations_to_release = [
                res for res in self.reservations.values() 
                if res["order_id"] == order_id and res["status"] == "active"
            ]
            
            released_count = 0
            for reservation in reservations_to_release:
                # Release each reserved item
                for item in reservation["items"]:
                    inventory_key = f"{item['product_id']}:{item['variant_id']}" if item.get('variant_id') else item['product_id']
                    
                    if inventory_key in self.inventory:
                        self.inventory[inventory_key]["reserved"] -= item["quantity"]
                        released_count += 1
                
                # Mark reservation as released
                reservation["status"] = "released"
                reservation["released_at"] = datetime.utcnow()
            
            return {
                "success": True,
                "released_reservations": len(reservations_to_release),
                "released_items": released_count
            }
            
        except Exception as e:
            logger.error(f"Failed to release reservation for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fulfill_reservation(self, order_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fulfill inventory reservation by reducing actual stock"""
        logger.info(f"Fulfilling inventory for order {order_id}")
        
        try:
            # Find reservation for this order
            reservation = next(
                (res for res in self.reservations.values() 
                 if res["order_id"] == order_id and res["status"] == "active"),
                None
            )
            
            if not reservation:
                raise Exception(f"No active reservation found for order {order_id}")
            
            fulfilled_items = []
            
            for item in items:
                product_id = item["product_id"]
                variant_id = item.get("variant_id")
                quantity_to_fulfill = item["quantity"]
                
                inventory_key = f"{product_id}:{variant_id}" if variant_id else product_id
                
                if inventory_key in self.inventory:
                    inventory_data = self.inventory[inventory_key]
                    
                    # Reduce available and reserved stock
                    inventory_data["available"] -= quantity_to_fulfill
                    inventory_data["reserved"] -= quantity_to_fulfill
                    inventory_data["last_movement"] = datetime.utcnow()
                    
                    # Record movement
                    if "movements" not in inventory_data:
                        inventory_data["movements"] = []
                    
                    inventory_data["movements"].append({
                        "type": "fulfillment",
                        "quantity": -quantity_to_fulfill,
                        "order_id": order_id,
                        "timestamp": datetime.utcnow(),
                        "notes": f"Order fulfillment for {order_id}"
                    })
                    
                    fulfilled_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "quantity": quantity_to_fulfill,
                        "warehouse_id": inventory_data["primary_warehouse"]
                    })
            
            # Mark reservation as fulfilled
            reservation["status"] = "fulfilled"
            reservation["fulfilled_at"] = datetime.utcnow()
            
            return {
                "success": True,
                "fulfilled_items": fulfilled_items,
                "reservation_id": reservation["id"]
            }
            
        except Exception as e:
            logger.error(f"Inventory fulfillment failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def restock_items(self, order_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Restock items (e.g., for returns)"""
        logger.info(f"Restocking items for order {order_id}")
        
        try:
            restocked_items = []
            
            for item in items:
                product_id = item["product_id"]
                variant_id = item.get("variant_id")
                quantity_to_restock = item["quantity"]
                
                inventory_key = f"{product_id}:{variant_id}" if variant_id else product_id
                
                if inventory_key in self.inventory:
                    inventory_data = self.inventory[inventory_key]
                    
                    # Add back to available stock
                    inventory_data["available"] += quantity_to_restock
                    inventory_data["last_movement"] = datetime.utcnow()
                    
                    # Record movement
                    if "movements" not in inventory_data:
                        inventory_data["movements"] = []
                    
                    inventory_data["movements"].append({
                        "type": "restock",
                        "quantity": quantity_to_restock,
                        "order_id": order_id,
                        "timestamp": datetime.utcnow(),
                        "notes": f"Return restock for order {order_id}"
                    })
                    
                    restocked_items.append({
                        "product_id": product_id,
                        "variant_id": variant_id,
                        "quantity": quantity_to_restock,
                        "new_available": inventory_data["available"]
                    })
            
            return {
                "success": True,
                "restocked_items": restocked_items
            }
            
        except Exception as e:
            logger.error(f"Restock failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_stock_levels(self, product_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get current stock levels for products"""
        
        stock_levels = {}
        
        for product_id in product_ids:
            if product_id in self.inventory:
                inventory_data = self.inventory[product_id]
                stock_levels[product_id] = {
                    "available": inventory_data["available"],
                    "reserved": inventory_data["reserved"],
                    "total": inventory_data["available"] + inventory_data["reserved"],
                    "warehouse_id": inventory_data["primary_warehouse"],
                    "last_updated": inventory_data.get("last_movement", datetime.utcnow())
                }
            else:
                stock_levels[product_id] = {
                    "available": 0,
                    "reserved": 0,
                    "total": 0,
                    "warehouse_id": None,
                    "last_updated": datetime.utcnow()
                }
        
        return stock_levels
    
    async def get_analytics(self) -> Dict[str, Any]:
        """Get inventory analytics and insights"""
        
        total_products = len(self.inventory)
        low_stock_products = []
        out_of_stock_products = []
        high_turnover_products = []
        
        for product_id, inventory_data in self.inventory.items():
            available = inventory_data["available"]
            
            if available == 0:
                out_of_stock_products.append(product_id)
            elif available <= self.config["low_stock_threshold"]:
                low_stock_products.append(product_id)
            
            # Calculate turnover (simplified)
            movements = inventory_data.get("movements", [])
            recent_movements = [
                m for m in movements 
                if m["timestamp"] > datetime.utcnow() - timedelta(days=30)
            ]
            
            if len(recent_movements) > 10:  # High activity
                high_turnover_products.append(product_id)
        
        return {
            "total_products": total_products,
            "low_stock_count": len(low_stock_products),
            "out_of_stock_count": len(out_of_stock_products),
            "high_turnover_count": len(high_turnover_products),
            "low_stock_products": low_stock_products[:10],  # Top 10
            "out_of_stock_products": out_of_stock_products[:10],
            "reorder_recommendations": await self._get_reorder_recommendations(),
            "warehouse_utilization": await self._get_warehouse_utilization(),
            "generated_at": datetime.utcnow()
        }
    
    async def get_health(self) -> Dict[str, Any]:
        """Get inventory manager health status"""
        
        return {
            "status": "healthy",
            "total_inventory_items": len(self.inventory),
            "active_reservations": len([r for r in self.reservations.values() if r["status"] == "active"]),
            "warehouses_connected": len(self.warehouses),
            "last_check": datetime.utcnow()
        }
    
    # Private helper methods
    
    def _initialize_sample_data(self):
        """Initialize sample inventory data for demonstration"""
        
        # Sample products
        sample_products = [
            {
                "product_id": "prod_001",
                "name": "Premium Widget",
                "sku": "WIDGET-001",
                "available": 100,
                "reserved": 0,
                "reorder_point": 10,
                "max_stock": 500,
                "primary_warehouse": "warehouse_001",
                "supplier_id": "supplier_001",
                "cost": Decimal("15.00"),
                "weight": Decimal("0.5")
            },
            {
                "product_id": "prod_002",
                "name": "Standard Widget",
                "sku": "WIDGET-002",
                "available": 50,
                "reserved": 5,
                "reorder_point": 15,
                "max_stock": 300,
                "primary_warehouse": "warehouse_001",
                "supplier_id": "supplier_001",
                "cost": Decimal("10.00"),
                "weight": Decimal("0.3")
            },
            {
                "product_id": "prod_003",
                "name": "Premium Gadget",
                "sku": "GADGET-001",
                "available": 25,
                "reserved": 0,
                "reorder_point": 5,
                "max_stock": 100,
                "primary_warehouse": "warehouse_002",
                "supplier_id": "supplier_002",
                "cost": Decimal("45.00"),
                "weight": Decimal("1.2")
            }
        ]
        
        for product in sample_products:
            product_id = product["product_id"]
            self.inventory[product_id] = {
                **product,
                "movements": [],
                "last_movement": datetime.utcnow(),
                "created_at": datetime.utcnow()
            }
        
        # Sample warehouses
        self.warehouses = {
            "warehouse_001": {
                "id": "warehouse_001",
                "name": "Main Warehouse",
                "location": "New York, NY",
                "capacity": 10000,
                "utilization": 65.0,
                "status": "active"
            },
            "warehouse_002": {
                "id": "warehouse_002",
                "name": "West Coast Warehouse",
                "location": "Los Angeles, CA",
                "capacity": 8000,
                "utilization": 45.0,
                "status": "active"
            }
        }
        
        # Sample suppliers
        self.suppliers = {
            "supplier_001": {
                "id": "supplier_001",
                "name": "Widget Supplier Inc.",
                "contact": "supplier@widgets.com",
                "lead_time_days": 7,
                "reliability_score": 95.0,
                "status": "active"
            },
            "supplier_002": {
                "id": "supplier_002",
                "name": "Gadget Manufacturing Co.",
                "contact": "orders@gadgets.com",
                "lead_time_days": 14,
                "reliability_score": 88.0,
                "status": "active"
            }
        }
    
    async def _initialize_warehouses(self):
        """Initialize warehouse connections"""
        logger.info("Initializing warehouse connections...")
        
        # In production, this would establish connections to warehouse management systems
        for warehouse_id, warehouse_data in self.warehouses.items():
            logger.info(f"Connected to warehouse: {warehouse_data['name']}")
    
    async def _get_available_stock(self, inventory_key: str) -> int:
        """Get available stock for inventory item"""
        
        if inventory_key in self.inventory:
            inventory_data = self.inventory[inventory_key]
            return max(0, inventory_data["available"] - inventory_data["reserved"])
        
        return 0
    
    async def _create_reservation(self, reservation_id: str, order_id: str, inventory_key: str, quantity: int):
        """Create inventory reservation"""
        
        if inventory_key in self.inventory:
            self.inventory[inventory_key]["reserved"] += quantity
            
            logger.info(f"Reserved {quantity} units of {inventory_key} for order {order_id}")
    
    async def _estimate_restock_date(self, inventory_key: str) -> Optional[datetime]:
        """Estimate restock date for product"""
        
        if inventory_key in self.inventory:
            inventory_data = self.inventory[inventory_key]
            supplier_id = inventory_data.get("supplier_id")
            
            if supplier_id in self.suppliers:
                supplier = self.suppliers[supplier_id]
                lead_time = supplier["lead_time_days"]
                
                return datetime.utcnow() + timedelta(days=lead_time)
        
        return None
    
    async def _check_reorder_triggers(self, items: List[Dict[str, Any]]):
        """Check if any items need reordering"""
        
        for item in items:
            product_id = item["product_id"]
            
            if product_id in self.inventory:
                inventory_data = self.inventory[product_id]
                available = inventory_data["available"]
                reorder_point = inventory_data.get("reorder_point", self.config["reorder_threshold"])
                
                if available <= reorder_point:
                    await self._trigger_auto_reorder(product_id, inventory_data)
    
    async def _trigger_auto_reorder(self, product_id: str, inventory_data: Dict[str, Any]):
        """Trigger automatic reorder for product"""
        
        logger.info(f"Triggering auto-reorder for product {product_id}")
        
        # Calculate reorder quantity
        max_stock = inventory_data.get("max_stock", 100)
        current_stock = inventory_data["available"] + inventory_data["reserved"]
        reorder_quantity = max_stock - current_stock
        
        # Create purchase order (simplified)
        purchase_order = {
            "id": str(uuid4()),
            "product_id": product_id,
            "supplier_id": inventory_data.get("supplier_id"),
            "quantity": reorder_quantity,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "estimated_delivery": await self._estimate_restock_date(product_id)
        }
        
        logger.info(f"Created purchase order {purchase_order['id']} for {reorder_quantity} units")
        
        # In production, this would integrate with supplier systems
    
    async def _cleanup_expired_reservations(self):
        """Background task to cleanup expired reservations"""
        
        while True:
            try:
                current_time = datetime.utcnow()
                expired_reservations = [
                    res for res in self.reservations.values()
                    if res["status"] == "active" and res["expires_at"] < current_time
                ]
                
                for reservation in expired_reservations:
                    # Release reserved inventory
                    for item in reservation["items"]:
                        inventory_key = f"{item['product_id']}:{item['variant_id']}" if item.get('variant_id') else item['product_id']
                        
                        if inventory_key in self.inventory:
                            self.inventory[inventory_key]["reserved"] -= item["quantity"]
                    
                    # Mark as expired
                    reservation["status"] = "expired"
                    reservation["expired_at"] = current_time
                    
                    logger.info(f"Expired reservation {reservation['id']} for order {reservation['order_id']}")
                
                # Wait before next cleanup
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Reservation cleanup failed: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def _monitor_stock_levels(self):
        """Background task to monitor stock levels"""
        
        while True:
            try:
                # Check stock levels and trigger alerts
                for product_id, inventory_data in self.inventory.items():
                    available = inventory_data["available"]
                    reorder_point = inventory_data.get("reorder_point", self.config["reorder_threshold"])
                    
                    if available == 0:
                        logger.warning(f"Product {product_id} is out of stock")
                    elif available <= self.config["low_stock_threshold"]:
                        logger.warning(f"Product {product_id} has low stock: {available} units")
                    
                    if available <= reorder_point and self.config["enable_auto_reorder"]:
                        await self._trigger_auto_reorder(product_id, inventory_data)
                
                # Wait before next check
                await asyncio.sleep(1800)  # 30 minutes
                
            except Exception as e:
                logger.error(f"Stock monitoring failed: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry
    
    async def _get_reorder_recommendations(self) -> List[Dict[str, Any]]:
        """Get reorder recommendations"""
        
        recommendations = []
        
        for product_id, inventory_data in self.inventory.items():
            available = inventory_data["available"]
            reorder_point = inventory_data.get("reorder_point", self.config["reorder_threshold"])
            
            if available <= reorder_point:
                max_stock = inventory_data.get("max_stock", 100)
                recommended_quantity = max_stock - (available + inventory_data["reserved"])
                
                recommendations.append({
                    "product_id": product_id,
                    "current_stock": available,
                    "reorder_point": reorder_point,
                    "recommended_quantity": recommended_quantity,
                    "supplier_id": inventory_data.get("supplier_id"),
                    "estimated_cost": recommended_quantity * inventory_data.get("cost", Decimal("0"))
                })
        
        return recommendations
    
    async def _get_warehouse_utilization(self) -> Dict[str, Any]:
        """Get warehouse utilization metrics"""
        
        utilization = {}
        
        for warehouse_id, warehouse_data in self.warehouses.items():
            # Calculate current utilization
            total_items = sum(
                inv["available"] + inv["reserved"]
                for inv in self.inventory.values()
                if inv.get("primary_warehouse") == warehouse_id
            )
            
            capacity = warehouse_data["capacity"]
            utilization_pct = (total_items / capacity * 100) if capacity > 0 else 0
            
            utilization[warehouse_id] = {
                "name": warehouse_data["name"],
                "current_items": total_items,
                "capacity": capacity,
                "utilization_percentage": round(utilization_pct, 2),
                "available_space": capacity - total_items
            }
        
        return utilization