# Saleor E-commerce - Backend Service (DDD)

## Service Identity
- **Name**: Saleor E-commerce Backend
- **Type**: Backend - E-commerce GraphQL API
- **Container**: `bizosaas-saleor-staging`
- **Port**: `8000:8000`
- **Status**: ⚠️ Unhealthy (GraphQL startup issues)

## Purpose
Headless e-commerce platform with GraphQL API for product catalog, cart, checkout, payments, and order management.

## Domain Model

### Aggregates
- **Product**: Product catalog with variants
- **Order**: Customer order lifecycle
- **Checkout**: Shopping cart and checkout process
- **Payment**: Multi-gateway payment processing
- **Fulfillment**: Shipping and delivery

### Multi-Tenant Architecture
- Tenant-specific product catalogs
- Isolated order management
- Shared payment gateway config

## GraphQL Schema
```graphql
type Product {
  id: ID!
  name: String!
  description: String
  pricing: ProductPricing!
  variants: [ProductVariant!]!
}

type Mutation {
  checkoutCreate(input: CheckoutCreateInput!): CheckoutCreate
  checkoutAddLine(checkoutId: ID!, lines: [CheckoutLineInput!]!): CheckoutAddLine
  checkoutComplete(checkoutId: ID!): CheckoutComplete
}
```

## Integration with CorelDove
- Product catalog → CorelDove frontend
- Cart operations → Real-time sync
- Checkout flow → Payment processing
- Order tracking → Customer portal

---
**Status**: ⚠️ Needs Health Check Fix
**Priority**: HIGH
**Last Updated**: October 15, 2025
