# CorelDove Backend - Backend Service (DDD)

## Service Identity
- **Name**: CorelDove E-commerce Backend
- **Type**: Backend - E-commerce Bridge Service
- **Container**: `bizosaas-coreldove-backend-staging`
- **Port**: `8005:8000`
- **Status**: ⚠️ Unhealthy (FastAPI startup issues)

## Purpose
FastAPI bridge service connecting CorelDove frontend to Saleor GraphQL backend, providing REST API abstraction and business logic.

## Domain Model

### Value-Added Features
- REST API wrapping Saleor GraphQL
- Product search and filtering
- Inventory validation
- Order processing logic
- Customer management

## API Endpoints
- `GET /api/v1/products` - List products (REST)
- `POST /api/v1/cart/add` - Add to cart
- `POST /api/v1/checkout` - Initiate checkout
- `GET /api/v1/orders/{id}` - Get order status

## Integration Pattern
```
CorelDove Frontend → CorelDove Backend (REST) → Saleor (GraphQL)
```

---
**Status**: ⚠️ Needs Health Check Fix
**Last Updated**: October 15, 2025
