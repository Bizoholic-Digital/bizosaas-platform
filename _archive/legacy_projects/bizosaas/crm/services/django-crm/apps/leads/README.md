# Leads App

The Leads app provides comprehensive lead management functionality for the Django CRM system with AI-powered scoring, multi-tenant support, and advanced filtering capabilities.

## Features

### Core Functionality
- **Lead Management**: Complete CRUD operations for leads with detailed contact and company information
- **AI Scoring**: Automatic lead scoring based on multiple factors including company size, budget, decision maker status, and engagement level
- **Multi-tenant Support**: Full tenant isolation with row-level security
- **Source Tracking**: Track and analyze lead sources with conversion statistics
- **Tag System**: Flexible tagging system for lead categorization
- **Activity Tracking**: Complete activity log with scheduled activities and follow-ups
- **Note System**: Public and private notes with user access control

### Advanced Features
- **Smart Filtering**: Advanced filtering with 20+ filter options including date ranges, score ranges, and behavioral filters
- **Bulk Operations**: Bulk update capabilities for efficient lead management
- **Overdue Tracking**: Automatic tracking of overdue follow-ups and activities
- **Conversion Tracking**: Complete conversion funnel tracking with value attribution
- **Assignment Management**: Lead assignment with role-based access control
- **Custom Fields**: Extensible custom field system for additional lead data

## Models

### Lead
The main lead model with comprehensive contact and company information:
- Contact details (name, email, phone)
- Company information (company, job title, size, industry, revenue)
- Lead management (status, priority, assignment, source)
- AI scoring (score, factors, last scored)
- Marketing tracking (UTM parameters, referrer)
- Qualification data (budget, timeline, decision maker status)
- Conversion tracking (converted date, value, lost reason)

### LeadSource
Track lead origins and performance:
- Source name and description
- Conversion rate calculation
- Lead count statistics
- Active/inactive status

### LeadTag  
Flexible tagging system:
- Tag name and color coding
- Usage statistics
- Active/inactive management

### LeadActivity
Comprehensive activity tracking:
- Activity types (call, email, meeting, note, etc.)
- Scheduled vs completed activities
- User attribution
- Metadata storage

### LeadNote
Note system with privacy controls:
- Public and private notes
- User attribution
- Rich text content

### Custom Fields
Extensible field system:
- Multiple field types (text, number, date, select, etc.)
- Tenant-specific fields
- Validation and default values

## API Endpoints

### Lead Management
```
GET    /api/leads/api/v1/leads/                 # List leads with filtering
POST   /api/leads/api/v1/leads/                 # Create new lead
GET    /api/leads/api/v1/leads/{id}/            # Get lead details
PUT    /api/leads/api/v1/leads/{id}/            # Update lead
DELETE /api/leads/api/v1/leads/{id}/            # Delete lead
```

### Lead Actions
```
POST   /api/leads/api/v1/leads/{id}/update-score/      # Update AI score
POST   /api/leads/api/v1/leads/{id}/mark-contacted/    # Mark as contacted  
POST   /api/leads/api/v1/leads/{id}/convert/           # Convert to customer
POST   /api/leads/api/v1/leads/{id}/mark-lost/         # Mark as lost
GET    /api/leads/api/v1/leads/{id}/ai-insights/       # Get AI insights
```

### Bulk Operations
```
POST   /api/leads/api/v1/leads/bulk-update/            # Bulk update leads
POST   /api/leads/api/v1/leads/update-scores/          # Bulk score update
```

### Special Lists
```
GET    /api/leads/api/v1/leads/dashboard/              # Dashboard statistics
GET    /api/leads/api/v1/leads/overdue-followups/      # Overdue follow-ups
GET    /api/leads/api/v1/leads/high-priority/          # High priority leads
GET    /api/leads/api/v1/leads/unassigned/             # Unassigned leads
```

### Sources and Tags
```
GET    /api/leads/api/v1/sources/                      # List sources
POST   /api/leads/api/v1/sources/                      # Create source
GET    /api/leads/api/v1/tags/                         # List tags
POST   /api/leads/api/v1/tags/                         # Create tag
```

### Activities and Notes
```
GET    /api/leads/api/v1/activities/                   # List activities
POST   /api/leads/api/v1/activities/                   # Create activity
GET    /api/leads/api/v1/notes/                        # List notes
POST   /api/leads/api/v1/notes/                        # Create note
```

### Nested Resources
```
GET    /api/leads/api/v1/leads/{id}/activities/        # Lead activities
POST   /api/leads/api/v1/leads/{id}/activities/        # Create activity for lead
GET    /api/leads/api/v1/leads/{id}/notes/             # Lead notes
POST   /api/leads/api/v1/leads/{id}/notes/             # Create note for lead
```

## AI Scoring System

The AI scoring system automatically evaluates leads based on multiple factors:

### Scoring Factors
- **Company Size**: Enterprise (80pts) > Large (60pts) > Medium (40pts) > Small (20pts) > Startup (10pts)
- **Budget**: $100k+ (30pts), $50k+ (20pts), $10k+ (10pts)
- **Decision Maker**: +15 points if contact is decision maker
- **Contact Completeness**: +5 points each for phone, company, job title
- **Status Progress**: New (5pts) > Contacted (10pts) > Qualified (25pts) > Proposal (40pts) > Negotiation (60pts)
- **Timeline Urgency**: Immediate (20pts), This month (15pts), This quarter (10pts)

### Score Updates
Scores are automatically updated when:
- Lead is created (initial scoring)
- Relevant fields are changed (company size, budget, status, etc.)
- Manual score update is triggered
- Lead is converted (score set to 100)

## Filtering and Search

### Available Filters
- **Status**: new, contacted, qualified, proposal, negotiation, converted, lost, unresponsive
- **Priority**: low, medium, high, urgent
- **Score Range**: min/max score filtering
- **Budget Range**: min/max budget filtering
- **Assignment**: assigned user, unassigned leads
- **Source**: specific lead source
- **Tags**: multiple tag filtering
- **Company Size**: startup, small, medium, large, enterprise
- **Dates**: created date ranges, contact date ranges
- **Behavior**: has budget, decision maker, overdue follow-up
- **Timeline**: urgent timeline keywords
- **UTM Parameters**: source, medium, campaign filtering

### Search Functionality
Full-text search across:
- Name (first_name + last_name)
- Email address
- Phone number
- Company name
- Job title
- Notes content
- Pain points
- Requirements

### Custom Manager Methods
```python
# Using custom managers
Lead.objects.new()                    # New leads
Lead.objects.high_priority()          # High priority leads
Lead.objects.high_score(threshold=70) # High scoring leads
Lead.objects.unassigned()             # Unassigned leads
Lead.objects.overdue_followup()       # Overdue follow-ups
Lead.objects.created_recently(days=7) # Recent leads
Lead.objects.requiring_attention()    # Leads needing attention
Lead.objects.search(query)            # Search leads
```

## Permissions and Security

### Tenant Isolation
- All models inherit from `BaseModel` with automatic tenant filtering
- Row-level security ensures data isolation between tenants
- API endpoints automatically filter by tenant context

### Role-Based Access
- **Owner/Admin**: Full access to all leads and settings
- **Manager**: Full access to leads, limited settings access
- **User**: Can view all leads, modify assigned/unassigned leads
- **Read-only**: View-only access to leads

### Object-Level Permissions
- Users can modify their own assigned leads
- Admins can modify any lead
- Private notes only visible to author and admins

## Usage Examples

### Creating a Lead
```python
from apps.leads.models import Lead, LeadSource

source = LeadSource.objects.get(name='Website')
lead = Lead.objects.create(
    tenant=tenant,
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    company='Acme Corp',
    source=source,
    budget=50000,
    decision_maker=True
)
# Score will be calculated automatically
```

### Updating Lead Score
```python
# Manual score update
lead.update_score()

# Score with custom factors
lead.update_score(factors={'custom_factor': 25})
```

### Bulk Operations
```python
# Assign multiple leads
leads = Lead.objects.filter(status='new', score__gte=70)
leads.update(assigned_to=user, status='contacted')

# Bulk tag assignment
hot_leads = Lead.objects.filter(score__gte=80)
hot_tag = LeadTag.objects.get(name='Hot Lead')
for lead in hot_leads:
    lead.tags.add(hot_tag)
```

### Activity Tracking
```python
from apps.leads.models import LeadActivity

# Log a call
LeadActivity.objects.create(
    tenant=tenant,
    lead=lead,
    user=user,
    activity_type='call',
    description='Initial qualification call',
    is_completed=True
)

# Schedule follow-up
future_date = timezone.now() + timedelta(days=3)
LeadActivity.objects.create(
    tenant=tenant,
    lead=lead,
    user=user,
    activity_type='follow_up',
    description='Follow up on proposal',
    scheduled_at=future_date,
    is_completed=False
)
```

## Management Commands

### Setup Initial Data
```bash
# Setup data for all tenants
python manage.py setup_leads_data

# Setup for specific tenant
python manage.py setup_leads_data --tenant-slug=company-abc

# Skip existing data
python manage.py setup_leads_data --skip-existing
```

This command creates:
- 10 default lead sources (Website, Social Media, Google Ads, etc.)
- 12 default lead tags with color coding
- All properly configured for each tenant

## Testing

The app includes comprehensive tests covering:
- Model functionality and methods
- AI scoring calculations  
- Manager query methods
- API endpoints and permissions
- Bulk operations
- Activity tracking
- Signal handlers

Run tests with:
```bash
python manage.py test apps.leads
```

## Integration Points

### AI Agents Integration
- Lead scoring can be enhanced with external AI services
- The `ai_insights` endpoint is designed for CrewAI integration
- Supports custom scoring factors from AI analysis

### Temporal Workflows
- Activity scheduling can trigger Temporal workflows
- Lead nurturing sequences can be automated
- Follow-up reminders and escalations

### Vault Integration
- API keys for external services stored securely
- Lead data encryption for sensitive information
- Audit logging for compliance

This leads app provides a solid foundation for lead management with room for customization and extension based on specific business needs.