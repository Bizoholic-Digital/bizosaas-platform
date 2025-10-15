# Django CRM - Backend Service (DDD)

## Service Identity
- **Name**: Django CRM Service
- **Type**: Backend - Customer Relationship Management
- **Container**: `bizosaas-django-crm-staging`
- **Port**: `8003:8000`
- **Status**: ⚠️ Unhealthy (Worker timeout)

## Purpose
CRM system for lead management, sales pipeline, customer tracking, and automated workflows.

## Domain Model

### Aggregates
- **Lead**: Potential customer with scoring
- **Contact**: Customer information
- **Deal**: Sales opportunity
- **Activity**: Customer interactions

### Lead Scoring Algorithm
```python
def calculate_lead_score(lead: Lead) -> int:
    score = 0
    
    # Company size (0-20 points)
    if lead.company_size:
        score += min(lead.company_size / 50, 20)
    
    # Budget (0-25 points)
    if lead.budget:
        if lead.budget >= 10000: score += 25
        elif lead.budget >= 5000: score += 20
        elif lead.budget >= 1000: score += 15
    
    # Service interest (0-20 points)
    if lead.services_interested:
        score += len(lead.services_interested) * 5
    
    # Contact completeness (0-20 points)
    if lead.phone: score += 10
    if lead.website: score += 10
    
    # Engagement (0-15 points)
    if lead.message and len(lead.message) > 100:
        score += 15
    
    return min(score, 100)
```

## API Endpoints
- `POST /api/v1/leads/` - Create lead
- `GET /api/v1/leads/{id}/` - Get lead details
- `PUT /api/v1/leads/{id}/score/` - Update lead score
- `GET /api/v1/pipeline/` - Get sales pipeline

## Integration
- Wagtail forms → Automatic lead creation
- Email automation → Follow-up sequences
- Analytics → Performance tracking

---
**Status**: ⚠️ Needs Worker Fix
**Priority**: HIGH
**Last Updated**: October 15, 2025
