"""
Models package for CRM Service v2
=================================

This package contains all Pydantic models for the CRM service including
lead management, customer data, and e-commerce functionality.
"""

from .ecommerce import (
    # Enums
    ProductCategory,
    ProductClassification,
    ProductStatus,
    OrderStatus,
    OrderFinancialStatus,
    FraudRiskLevel,
    MarketplaceType,
    
    # Product Models
    Product,
    ProductCreate,
    ProductUpdate,
    ProductDimensions,
    ProductImages,
    ProductPricing,
    ProductMarketData,
    ProductAIMetrics,
    
    # Order Models
    Order,
    OrderCreate,
    OrderUpdate,
    OrderItem,
    OrderAddress,
    FraudDetectionMetrics,
    
    # Inventory Models
    InventoryLevel,
    InventoryUpdate,
    InventoryAlert,
    
    # Supplier Models
    Supplier,
    
    # AI Workflow Models
    AIWorkflowExecution,
    
    # Response Models
    ProductListResponse,
    OrderListResponse,
    InventoryListResponse,
    AIWorkflowResponse,
    
    # Bulk Operation Models
    BulkProductUpdate,
    BulkInventoryUpdate,
    BulkOperationResult,
    
    # Base Models
    TimestampMixin,
    TenantMixin
)

__all__ = [
    # Enums
    "ProductCategory",
    "ProductClassification", 
    "ProductStatus",
    "OrderStatus",
    "OrderFinancialStatus",
    "FraudRiskLevel",
    "MarketplaceType",
    
    # Product Models
    "Product",
    "ProductCreate",
    "ProductUpdate",
    "ProductDimensions",
    "ProductImages", 
    "ProductPricing",
    "ProductMarketData",
    "ProductAIMetrics",
    
    # Order Models
    "Order",
    "OrderCreate",
    "OrderUpdate",
    "OrderItem",
    "OrderAddress",
    "FraudDetectionMetrics",
    
    # Inventory Models
    "InventoryLevel",
    "InventoryUpdate", 
    "InventoryAlert",
    
    # Supplier Models
    "Supplier",
    
    # AI Workflow Models
    "AIWorkflowExecution",
    
    # Response Models
    "ProductListResponse",
    "OrderListResponse",
    "InventoryListResponse",
    "AIWorkflowResponse",
    
    # Bulk Operation Models
    "BulkProductUpdate",
    "BulkInventoryUpdate",
    "BulkOperationResult",
    
    # Base Models
    "TimestampMixin",
    "TenantMixin"
]