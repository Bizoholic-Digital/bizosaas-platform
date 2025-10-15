# Wagtail CMS - Backend Service (DDD)

## Service Identity
- **Name**: Wagtail CMS
- **Type**: Backend - Content Management System
- **Container**: `bizosaas-wagtail-staging`
- **Port**: `8002:4000`
- **Status**: ✅ Running (13+ hours)

## Purpose
Django-based headless CMS for dynamic content management across Bizoholic marketing website and multi-tenant content delivery.

## Domain Model

### Aggregates
- **Page**: Content page with SEO metadata
- **ContentBlock**: Reusable content component
- **Form**: Contact/lead generation forms
- **Menu**: Site navigation structure

### Multi-Tenant Architecture
- Tenant-specific content trees
- Shared templates across tenants
- Row-level security on pages

## API Endpoints
- `GET /api/v2/pages/` - List pages
- `POST /api/v2/forms/submit/` - Submit form
- `GET /api/v2/pages/{id}/` - Get page content
- `GET /api/v2/menu/` - Get navigation menu

## Integration with Bizoholic
- Contact forms → Django CRM (dual submission)
- Blog content → Bizoholic frontend
- Landing pages → Dynamic rendering

---
**Status**: ✅ Production-Ready
**Last Updated**: October 15, 2025
