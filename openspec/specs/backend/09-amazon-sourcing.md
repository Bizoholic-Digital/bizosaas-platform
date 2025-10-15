# Amazon Sourcing - Backend Service (DDD)

## Service Identity
- **Name**: Amazon Product Sourcing Service
- **Type**: Backend - Dropshipping Integration
- **Container**: `bizosaas-amazon-sourcing-staging`
- **Port**: `8009:8000`
- **Status**: ⚠️ Unhealthy (API connection errors)

## Purpose
Amazon SP-API integration for product sourcing, inventory synchronization, and dropshipping automation.

## Domain Model

### Aggregates
- **SourceProduct**: Amazon product data
- **InventorySync**: Stock level synchronization
- **DropshipOrder**: Automated order fulfillment

### AI-Powered Features
- Product validation with HITL workflows
- Profit margin calculation
- Competitor price analysis
- Demand forecasting

## API Endpoints
- `GET /api/v1/products/search` - Search Amazon products
- `POST /api/v1/products/validate` - Validate product (HITL)
- `POST /api/v1/inventory/sync` - Sync inventory
- `POST /api/v1/orders/dropship` - Place dropship order

---
**Status**: ⚠️ Needs API Fix
**Last Updated**: October 15, 2025
