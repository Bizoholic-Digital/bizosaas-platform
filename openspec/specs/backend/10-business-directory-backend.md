# Business Directory Backend - Backend Service (DDD)

## Service Identity
- **Name**: Business Directory Backend
- **Type**: Backend - Business Listings & Directory
- **Container**: `bizosaas-business-directory-staging`
- **Port**: `8004:8000`
- **Status**: ⚠️ Unhealthy (Database connection issues)

## Purpose
Multi-tenant business directory service with listings, categories, reviews, and search functionality.

## Domain Model

### Aggregates
- **BusinessListing**: Company profile with details
- **Category**: Business categorization
- **Review**: Customer reviews and ratings
- **Location**: Geographic data with search

### Features
- Full-text search (PostgreSQL pg_trgm)
- Geographic proximity search
- Review management
- Category hierarchies
- Featured listings

## API Endpoints
- `POST /api/v1/businesses` - Create business listing
- `GET /api/v1/businesses/search` - Search businesses
- `POST /api/v1/reviews` - Submit review
- `GET /api/v1/categories` - List categories

## Multi-Tenancy
- Tenant-specific directories
- Shared category taxonomy
- Tenant-branded listings

---
**Status**: ⚠️ Needs Database Fix
**Last Updated**: October 15, 2025
