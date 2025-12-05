"""
Fulfillment Management Service
Handles order fulfillment, shipping, and tracking with multi-carrier support
"""

import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4

from ..models.order_models import FulfillmentStatus, ShippingMethod, FulfillmentItem, Fulfillment

logger = logging.getLogger(__name__)


class FulfillmentManager:
    """
    Comprehensive fulfillment management service
    Handles pick/pack optimization, shipping, tracking, and carrier integration
    """
    
    def __init__(self):
        self.config = {
            "auto_assign_warehouse": True,
            "enable_route_optimization": True,
            "enable_batch_processing": True,
            "max_batch_size": 50,
            "quality_control_enabled": True,
            "auto_print_labels": True,
            "tracking_update_interval": 3600  # 1 hour
        }
        
        # Shipping carriers configuration
        self.carriers = {
            "fedex": {
                "name": "FedEx",
                "api_url": "https://apis.fedex.com/track/v1",
                "services": {
                    ShippingMethod.STANDARD: {"name": "FedEx Ground", "days": "1-5", "cost_base": Decimal("9.99")},
                    ShippingMethod.EXPRESS: {"name": "FedEx Express", "days": "1-3", "cost_base": Decimal("19.99")},
                    ShippingMethod.OVERNIGHT: {"name": "FedEx Overnight", "days": "1", "cost_base": Decimal("39.99")}
                },
                "enabled": True
            },
            "ups": {
                "name": "UPS",
                "api_url": "https://onlinetools.ups.com/track/v1",
                "services": {
                    ShippingMethod.STANDARD: {"name": "UPS Ground", "days": "1-5", "cost_base": Decimal("8.99")},
                    ShippingMethod.EXPRESS: {"name": "UPS 2-Day Air", "days": "2", "cost_base": Decimal("18.99")},
                    ShippingMethod.OVERNIGHT: {"name": "UPS Next Day Air", "days": "1", "cost_base": Decimal("35.99")}
                },
                "enabled": True
            },
            "usps": {
                "name": "USPS",
                "api_url": "https://secure.shippingapis.com/ShippingAPI.dll",
                "services": {
                    ShippingMethod.STANDARD: {"name": "USPS Ground Advantage", "days": "2-5", "cost_base": Decimal("7.99")},
                    ShippingMethod.EXPRESS: {"name": "USPS Priority Mail", "days": "1-3", "cost_base": Decimal("14.99")}
                },
                "enabled": True
            },
            "dhl": {
                "name": "DHL",
                "api_url": "https://api-eu.dhl.com/track/shipments",
                "services": {
                    ShippingMethod.EXPRESS: {"name": "DHL Express", "days": "1-3", "cost_base": Decimal("22.99")},
                    ShippingMethod.OVERNIGHT: {"name": "DHL Express 9:00", "days": "1", "cost_base": Decimal("45.99")}
                },
                "enabled": True
            }
        }
        
        # Warehouse configuration
        self.warehouses = {
            "warehouse_001": {
                "id": "warehouse_001",
                "name": "Main Fulfillment Center",
                "location": "New York, NY",
                "coordinates": {"lat": 40.7128, "lng": -74.0060},
                "capacity": 10000,
                "operating_hours": {"start": 6, "end": 22},
                "zones": ["A", "B", "C", "D"],
                "capabilities": ["pick", "pack", "qc", "shipping"],
                "enabled": True
            },
            "warehouse_002": {
                "id": "warehouse_002",
                "name": "West Coast Distribution",
                "location": "Los Angeles, CA",
                "coordinates": {"lat": 34.0522, "lng": -118.2437},
                "capacity": 8000,
                "operating_hours": {"start": 7, "end": 23},
                "zones": ["A", "B", "C"],
                "capabilities": ["pick", "pack", "shipping"],
                "enabled": True
            }
        }
        
        # In-memory storage (replace with database in production)
        self.fulfillments = {}
        self.shipments = {}
        self.tracking_cache = {}
        self.pick_lists = {}
        self.batch_jobs = {}
        
    async def initialize(self):
        """Initialize fulfillment manager"""
        logger.info("Initializing Fulfillment Manager...")
        
        try:
            # Initialize carrier connections
            await self._initialize_carriers()
            
            # Initialize warehouse systems
            await self._initialize_warehouses()
            
            # Start background tasks
            asyncio.create_task(self._process_pick_lists())
            asyncio.create_task(self._update_tracking_info())
            asyncio.create_task(self._monitor_shipments())
            
            logger.info("Fulfillment Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Fulfillment Manager: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup fulfillment manager"""
        logger.info("Shutting down Fulfillment Manager...")
    
    async def schedule_fulfillment(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule order for fulfillment"""
        logger.info(f"Scheduling fulfillment for order {order['id']}")
        
        try:
            # Select optimal warehouse
            warehouse_id = await self._select_warehouse(order)
            
            # Create fulfillment record
            fulfillment_id = str(uuid4())
            
            fulfillment = {
                "id": fulfillment_id,
                "order_id": order["id"],
                "warehouse_id": warehouse_id,
                "status": FulfillmentStatus.PENDING,
                "items": [
                    {
                        "order_item_id": item["id"],
                        "product_id": item["product_id"],
                        "variant_id": item.get("variant_id"),
                        "sku": item["sku"],
                        "quantity": item["quantity"],
                        "location": await self._get_item_location(warehouse_id, item["sku"])
                    }
                    for item in order["items"]
                ],
                "priority": await self._calculate_priority(order),
                "estimated_ship_date": await self._calculate_ship_date(order, warehouse_id),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            self.fulfillments[fulfillment_id] = fulfillment
            
            # Add to pick list queue
            await self._add_to_pick_list(fulfillment)
            
            return {
                "success": True,
                "fulfillment_id": fulfillment_id,
                "warehouse_id": warehouse_id,
                "estimated_ship_date": fulfillment["estimated_ship_date"]
            }
            
        except Exception as e:
            logger.error(f"Fulfillment scheduling failed for order {order['id']}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_fulfillment(
        self, 
        order_id: str, 
        order_items: List[Dict[str, Any]], 
        fulfillment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process order fulfillment with shipping"""
        logger.info(f"Processing fulfillment for order {order_id}")
        
        try:
            # Find or create fulfillment
            fulfillment = await self._get_or_create_fulfillment(order_id, fulfillment_data)
            
            # Update fulfillment status
            fulfillment["status"] = FulfillmentStatus.PICKING
            fulfillment["updated_at"] = datetime.utcnow()
            
            # Process picking
            pick_result = await self._process_picking(fulfillment)
            if not pick_result["success"]:
                raise Exception(f"Picking failed: {pick_result['error']}")
            
            fulfillment["status"] = FulfillmentStatus.PACKED
            fulfillment["picked_at"] = datetime.utcnow()
            
            # Quality control check
            if self.config["quality_control_enabled"]:
                qc_result = await self._quality_control_check(fulfillment)
                if not qc_result["passed"]:
                    fulfillment["status"] = FulfillmentStatus.FAILED
                    fulfillment["qc_notes"] = qc_result["notes"]
                    raise Exception(f"Quality control failed: {qc_result['notes']}")
            
            # Generate shipping label
            shipping_result = await self._generate_shipping_label(fulfillment, fulfillment_data)
            if not shipping_result["success"]:
                raise Exception(f"Shipping label generation failed: {shipping_result['error']}")
            
            # Update fulfillment with shipping details
            fulfillment["shipping_details"] = shipping_result["shipping_details"]
            fulfillment["tracking_number"] = shipping_result["tracking_number"]
            fulfillment["status"] = FulfillmentStatus.SHIPPED
            fulfillment["shipped_at"] = datetime.utcnow()
            
            # Create shipment record
            shipment_id = str(uuid4())
            shipment = {
                "id": shipment_id,
                "fulfillment_id": fulfillment["id"],
                "order_id": order_id,
                "tracking_number": fulfillment["tracking_number"],
                "carrier": shipping_result["carrier"],
                "service": shipping_result["service"],
                "status": "in_transit",
                "shipped_at": datetime.utcnow(),
                "estimated_delivery": shipping_result.get("estimated_delivery"),
                "shipping_cost": shipping_result.get("cost", Decimal("0")),
                "dimensions": shipping_result.get("dimensions", {}),
                "weight": shipping_result.get("weight", Decimal("0"))
            }
            
            self.shipments[shipment_id] = shipment
            
            # Start tracking
            await self._start_tracking(shipment_id)
            
            return {
                "id": fulfillment["id"],
                "status": fulfillment["status"],
                "items": fulfillment["items"],
                "shipping_details": fulfillment["shipping_details"],
                "tracking_number": fulfillment["tracking_number"],
                "shipped_at": fulfillment["shipped_at"],
                "estimated_delivery": shipment["estimated_delivery"]
            }
            
        except Exception as e:
            logger.error(f"Fulfillment processing failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_tracking_info(self, order_id: str) -> Dict[str, Any]:
        """Get tracking information for order"""
        
        # Find shipment for order
        shipment = next(
            (s for s in self.shipments.values() if s["order_id"] == order_id),
            None
        )
        
        if not shipment:
            return {
                "status": "not_shipped",
                "message": "Order has not been shipped yet"
            }
        
        # Get cached tracking info
        tracking_number = shipment["tracking_number"]
        carrier = shipment["carrier"]
        
        if tracking_number in self.tracking_cache:
            tracking_data = self.tracking_cache[tracking_number]
        else:
            # Fetch from carrier
            tracking_data = await self._fetch_tracking_from_carrier(carrier, tracking_number)
            self.tracking_cache[tracking_number] = tracking_data
        
        return {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "status": tracking_data.get("status", "unknown"),
            "estimated_delivery": tracking_data.get("estimated_delivery"),
            "events": tracking_data.get("events", []),
            "last_updated": tracking_data.get("last_updated", datetime.utcnow())
        }
    
    async def update_fulfillment_status(
        self, 
        fulfillment_id: str, 
        new_status: FulfillmentStatus,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update fulfillment status"""
        
        if fulfillment_id not in self.fulfillments:
            raise Exception(f"Fulfillment {fulfillment_id} not found")
        
        fulfillment = self.fulfillments[fulfillment_id]
        old_status = fulfillment["status"]
        
        fulfillment["status"] = new_status
        fulfillment["updated_at"] = datetime.utcnow()
        
        if notes:
            if "notes" not in fulfillment:
                fulfillment["notes"] = []
            fulfillment["notes"].append({
                "timestamp": datetime.utcnow(),
                "status_change": f"{old_status} -> {new_status}",
                "notes": notes
            })
        
        logger.info(f"Updated fulfillment {fulfillment_id} status from {old_status} to {new_status}")
        
        return fulfillment
    
    async def get_fulfillment_analytics(self) -> Dict[str, Any]:
        """Get fulfillment analytics and metrics"""
        
        total_fulfillments = len(self.fulfillments)
        
        # Count by status
        status_counts = {}
        for status in FulfillmentStatus:
            status_counts[status.value] = len([
                f for f in self.fulfillments.values() if f["status"] == status
            ])
        
        # Calculate average fulfillment time
        completed_fulfillments = [
            f for f in self.fulfillments.values() 
            if f["status"] == FulfillmentStatus.SHIPPED and "shipped_at" in f
        ]
        
        avg_fulfillment_time = 0
        if completed_fulfillments:
            total_time = sum(
                (f["shipped_at"] - f["created_at"]).total_seconds()
                for f in completed_fulfillments
            )
            avg_fulfillment_time = total_time / len(completed_fulfillments) / 3600  # hours
        
        # Warehouse utilization
        warehouse_stats = {}
        for warehouse_id, warehouse in self.warehouses.items():
            warehouse_fulfillments = [
                f for f in self.fulfillments.values() 
                if f.get("warehouse_id") == warehouse_id
            ]
            
            warehouse_stats[warehouse_id] = {
                "name": warehouse["name"],
                "total_fulfillments": len(warehouse_fulfillments),
                "pending_fulfillments": len([
                    f for f in warehouse_fulfillments 
                    if f["status"] in [FulfillmentStatus.PENDING, FulfillmentStatus.PICKING]
                ])
            }
        
        return {
            "total_fulfillments": total_fulfillments,
            "status_breakdown": status_counts,
            "average_fulfillment_time_hours": round(avg_fulfillment_time, 2),
            "warehouse_stats": warehouse_stats,
            "active_shipments": len(self.shipments),
            "generated_at": datetime.utcnow()
        }
    
    async def get_health(self) -> Dict[str, Any]:
        """Get fulfillment manager health status"""
        
        carrier_health = {}
        for carrier_id, carrier_config in self.carriers.items():
            if carrier_config["enabled"]:
                # In production, this would ping carrier APIs
                carrier_health[carrier_id] = {
                    "status": "healthy",
                    "response_time_ms": 200,
                    "last_check": datetime.utcnow()
                }
        
        return {
            "status": "healthy",
            "pending_fulfillments": len([
                f for f in self.fulfillments.values() 
                if f["status"] in [FulfillmentStatus.PENDING, FulfillmentStatus.PICKING]
            ]),
            "active_shipments": len(self.shipments),
            "carriers": carrier_health,
            "warehouses_active": len([w for w in self.warehouses.values() if w["enabled"]])
        }
    
    # Private helper methods
    
    async def _initialize_carriers(self):
        """Initialize shipping carrier connections"""
        logger.info("Initializing shipping carriers...")
        
        for carrier_id, carrier_config in self.carriers.items():
            if carrier_config["enabled"]:
                logger.info(f"Initialized carrier: {carrier_config['name']}")
    
    async def _initialize_warehouses(self):
        """Initialize warehouse management systems"""
        logger.info("Initializing warehouse systems...")
        
        for warehouse_id, warehouse_config in self.warehouses.items():
            if warehouse_config["enabled"]:
                logger.info(f"Initialized warehouse: {warehouse_config['name']}")
    
    async def _select_warehouse(self, order: Dict[str, Any]) -> str:
        """Select optimal warehouse for order fulfillment"""
        
        if not self.config["auto_assign_warehouse"]:
            return "warehouse_001"  # Default warehouse
        
        shipping_address = order["shipping_address"]
        
        # Simple distance-based selection (in production, use actual distance calculation)
        if shipping_address["state"] in ["CA", "WA", "OR", "NV", "AZ"]:
            return "warehouse_002"  # West Coast
        else:
            return "warehouse_001"  # East Coast
    
    async def _get_item_location(self, warehouse_id: str, sku: str) -> str:
        """Get item location in warehouse"""
        
        # Simulate warehouse location lookup
        import random
        zones = self.warehouses[warehouse_id]["zones"]
        zone = random.choice(zones)
        aisle = random.randint(1, 20)
        shelf = random.randint(1, 10)
        
        return f"{zone}-{aisle:02d}-{shelf:02d}"
    
    async def _calculate_priority(self, order: Dict[str, Any]) -> int:
        """Calculate fulfillment priority"""
        
        priority = 5  # Normal priority
        
        # High value orders get higher priority
        if order["pricing"]["total"] > Decimal("500"):
            priority = 3
        
        # Express shipping gets highest priority
        if order.get("shipping_method") == ShippingMethod.EXPRESS:
            priority = 1
        elif order.get("shipping_method") == ShippingMethod.OVERNIGHT:
            priority = 0  # Highest priority
        
        return priority
    
    async def _calculate_ship_date(self, order: Dict[str, Any], warehouse_id: str) -> datetime:
        """Calculate estimated ship date"""
        
        warehouse = self.warehouses[warehouse_id]
        current_hour = datetime.utcnow().hour
        
        # If after warehouse hours, ship next day
        if current_hour >= warehouse["operating_hours"]["end"]:
            ship_date = datetime.utcnow().replace(hour=warehouse["operating_hours"]["start"], minute=0, second=0) + timedelta(days=1)
        else:
            # Ship today if enough time
            ship_date = datetime.utcnow() + timedelta(hours=2)  # 2 hour processing time
        
        return ship_date
    
    async def _add_to_pick_list(self, fulfillment: Dict[str, Any]):
        """Add fulfillment to pick list queue"""
        
        warehouse_id = fulfillment["warehouse_id"]
        
        if warehouse_id not in self.pick_lists:
            self.pick_lists[warehouse_id] = []
        
        self.pick_lists[warehouse_id].append(fulfillment["id"])
        
        # Sort by priority
        self.pick_lists[warehouse_id].sort(
            key=lambda fid: self.fulfillments[fid]["priority"]
        )
    
    async def _get_or_create_fulfillment(self, order_id: str, fulfillment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get existing fulfillment or create new one"""
        
        # Find existing fulfillment
        existing = next(
            (f for f in self.fulfillments.values() if f["order_id"] == order_id),
            None
        )
        
        if existing:
            return existing
        
        # Create new fulfillment
        fulfillment_id = str(uuid4())
        warehouse_id = fulfillment_data.get("warehouse_id", "warehouse_001")
        
        fulfillment = {
            "id": fulfillment_id,
            "order_id": order_id,
            "warehouse_id": warehouse_id,
            "status": FulfillmentStatus.PENDING,
            "items": [
                {
                    "order_item_id": item["order_item_id"],
                    "quantity": item["quantity"],
                    "warehouse_id": item.get("warehouse_id", warehouse_id)
                }
                for item in fulfillment_data.get("items", [])
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        self.fulfillments[fulfillment_id] = fulfillment
        return fulfillment
    
    async def _process_picking(self, fulfillment: Dict[str, Any]) -> Dict[str, Any]:
        """Process picking for fulfillment"""
        
        logger.info(f"Processing picking for fulfillment {fulfillment['id']}")
        
        # Simulate picking process
        await asyncio.sleep(1)  # Simulate picking time
        
        # In production, this would interface with warehouse management system
        
        return {
            "success": True,
            "picked_items": len(fulfillment["items"]),
            "picked_at": datetime.utcnow()
        }
    
    async def _quality_control_check(self, fulfillment: Dict[str, Any]) -> Dict[str, Any]:
        """Perform quality control check"""
        
        logger.info(f"Performing QC check for fulfillment {fulfillment['id']}")
        
        # Simulate QC process
        await asyncio.sleep(0.5)
        
        # Simulate 99% pass rate
        import random
        passed = random.random() < 0.99
        
        return {
            "passed": passed,
            "notes": "QC passed" if passed else "Items damaged during picking",
            "checked_at": datetime.utcnow()
        }
    
    async def _generate_shipping_label(self, fulfillment: Dict[str, Any], fulfillment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate shipping label"""
        
        logger.info(f"Generating shipping label for fulfillment {fulfillment['id']}")
        
        try:
            # Select carrier and service
            shipping_method = fulfillment_data.get("shipping_method", ShippingMethod.STANDARD)
            carrier_id = await self._select_carrier(shipping_method)
            
            carrier = self.carriers[carrier_id]
            service_info = carrier["services"][shipping_method]
            
            # Generate tracking number
            tracking_number = f"{carrier_id.upper()}{uuid4().hex[:12].upper()}"
            
            # Calculate shipping cost
            shipping_cost = await self._calculate_shipping_cost(carrier_id, shipping_method, fulfillment)
            
            # Calculate estimated delivery
            ship_date = datetime.utcnow()
            if shipping_method == ShippingMethod.OVERNIGHT:
                estimated_delivery = ship_date + timedelta(days=1)
            elif shipping_method == ShippingMethod.EXPRESS:
                estimated_delivery = ship_date + timedelta(days=2)
            else:
                estimated_delivery = ship_date + timedelta(days=5)
            
            shipping_details = {
                "id": str(uuid4()),
                "method": shipping_method,
                "carrier": carrier_id,
                "service_type": service_info["name"],
                "tracking_number": tracking_number,
                "tracking_url": f"https://track.{carrier_id}.com/{tracking_number}",
                "estimated_delivery": estimated_delivery,
                "cost": shipping_cost,
                "weight": await self._calculate_package_weight(fulfillment),
                "dimensions": await self._calculate_package_dimensions(fulfillment)
            }
            
            return {
                "success": True,
                "tracking_number": tracking_number,
                "carrier": carrier_id,
                "service": service_info["name"],
                "shipping_details": shipping_details,
                "cost": shipping_cost,
                "estimated_delivery": estimated_delivery
            }
            
        except Exception as e:
            logger.error(f"Shipping label generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _select_carrier(self, shipping_method: ShippingMethod) -> str:
        """Select optimal carrier for shipping method"""
        
        # Find carriers that support the shipping method
        suitable_carriers = []
        
        for carrier_id, carrier_config in self.carriers.items():
            if (carrier_config["enabled"] and 
                shipping_method in carrier_config["services"]):
                
                service_info = carrier_config["services"][shipping_method]
                cost = service_info["cost_base"]
                
                suitable_carriers.append({
                    "id": carrier_id,
                    "name": carrier_config["name"],
                    "cost": cost
                })
        
        if not suitable_carriers:
            raise Exception(f"No suitable carrier found for shipping method {shipping_method}")
        
        # Select carrier with lowest cost
        selected = min(suitable_carriers, key=lambda c: c["cost"])
        
        return selected["id"]
    
    async def _calculate_shipping_cost(self, carrier_id: str, shipping_method: ShippingMethod, fulfillment: Dict[str, Any]) -> Decimal:
        """Calculate shipping cost"""
        
        carrier = self.carriers[carrier_id]
        base_cost = carrier["services"][shipping_method]["cost_base"]
        
        # Add weight-based cost
        weight = await self._calculate_package_weight(fulfillment)
        weight_cost = weight * Decimal("0.50")  # $0.50 per kg
        
        return base_cost + weight_cost
    
    async def _calculate_package_weight(self, fulfillment: Dict[str, Any]) -> Decimal:
        """Calculate total package weight"""
        
        # Simulate weight calculation
        total_weight = Decimal("0")
        
        for item in fulfillment["items"]:
            # Simulate item weight lookup
            item_weight = Decimal("0.5")  # Default 0.5 kg per item
            total_weight += item_weight * item["quantity"]
        
        # Add packaging weight
        packaging_weight = Decimal("0.2")  # 200g packaging
        
        return total_weight + packaging_weight
    
    async def _calculate_package_dimensions(self, fulfillment: Dict[str, Any]) -> Dict[str, Decimal]:
        """Calculate package dimensions"""
        
        # Simulate package dimensions calculation
        return {
            "length": Decimal("30"),  # cm
            "width": Decimal("20"),   # cm
            "height": Decimal("15")   # cm
        }
    
    async def _start_tracking(self, shipment_id: str):
        """Start tracking for shipment"""
        
        shipment = self.shipments[shipment_id]
        tracking_number = shipment["tracking_number"]
        
        # Initialize tracking data
        self.tracking_cache[tracking_number] = {
            "status": "in_transit",
            "events": [
                {
                    "timestamp": datetime.utcnow(),
                    "status": "shipped",
                    "location": "Fulfillment Center",
                    "description": "Package shipped from fulfillment center"
                }
            ],
            "estimated_delivery": shipment["estimated_delivery"],
            "last_updated": datetime.utcnow()
        }
    
    async def _fetch_tracking_from_carrier(self, carrier: str, tracking_number: str) -> Dict[str, Any]:
        """Fetch tracking information from carrier"""
        
        # Simulate carrier API call
        logger.info(f"Fetching tracking from {carrier} for {tracking_number}")
        
        # Return simulated tracking data
        return {
            "status": "in_transit",
            "events": [
                {
                    "timestamp": datetime.utcnow() - timedelta(hours=2),
                    "status": "shipped",
                    "location": "New York, NY",
                    "description": "Package shipped from fulfillment center"
                },
                {
                    "timestamp": datetime.utcnow() - timedelta(hours=1),
                    "status": "in_transit",
                    "location": "Philadelphia, PA",
                    "description": "Package in transit"
                }
            ],
            "estimated_delivery": datetime.utcnow() + timedelta(days=2),
            "last_updated": datetime.utcnow()
        }
    
    async def _process_pick_lists(self):
        """Background task to process pick lists"""
        
        while True:
            try:
                for warehouse_id, pick_list in self.pick_lists.items():
                    if pick_list and self.config["enable_batch_processing"]:
                        # Process batch of fulfillments
                        batch_size = min(len(pick_list), self.config["max_batch_size"])
                        batch = pick_list[:batch_size]
                        
                        logger.info(f"Processing pick list batch of {batch_size} items for warehouse {warehouse_id}")
                        
                        # Remove processed items from pick list
                        self.pick_lists[warehouse_id] = pick_list[batch_size:]
                
                await asyncio.sleep(300)  # Process every 5 minutes
                
            except Exception as e:
                logger.error(f"Pick list processing failed: {e}")
                await asyncio.sleep(60)
    
    async def _update_tracking_info(self):
        """Background task to update tracking information"""
        
        while True:
            try:
                # Update tracking for active shipments
                active_shipments = [
                    s for s in self.shipments.values() 
                    if s["status"] in ["shipped", "in_transit"]
                ]
                
                for shipment in active_shipments:
                    tracking_number = shipment["tracking_number"]
                    carrier = shipment["carrier"]
                    
                    # Fetch updated tracking info
                    updated_tracking = await self._fetch_tracking_from_carrier(carrier, tracking_number)
                    self.tracking_cache[tracking_number] = updated_tracking
                    
                    # Update shipment status if delivered
                    if updated_tracking["status"] == "delivered":
                        shipment["status"] = "delivered"
                        shipment["delivered_at"] = datetime.utcnow()
                
                await asyncio.sleep(self.config["tracking_update_interval"])
                
            except Exception as e:
                logger.error(f"Tracking update failed: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry
    
    async def _monitor_shipments(self):
        """Background task to monitor shipment status"""
        
        while True:
            try:
                # Check for delayed shipments
                current_time = datetime.utcnow()
                
                for shipment in self.shipments.values():
                    if (shipment["status"] == "in_transit" and 
                        shipment.get("estimated_delivery") and
                        shipment["estimated_delivery"] < current_time):
                        
                        logger.warning(f"Shipment {shipment['id']} is delayed - tracking: {shipment['tracking_number']}")
                        
                        # In production, this would trigger alerts
                
                await asyncio.sleep(3600)  # Check every hour
                
            except Exception as e:
                logger.error(f"Shipment monitoring failed: {e}")
                await asyncio.sleep(300)