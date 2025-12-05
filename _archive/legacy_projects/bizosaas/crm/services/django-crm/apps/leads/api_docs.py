"""
API Documentation for Leads App
OpenAPI schema and endpoint documentation
"""
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# Lead ViewSet Documentation
LEAD_LIST_SCHEMA = extend_schema(
    summary="List leads",
    description="Get a paginated list of leads for the current tenant with filtering and search capabilities.",
    parameters=[
        OpenApiParameter(
            name='status',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter by lead status',
            enum=['new', 'contacted', 'qualified', 'proposal', 'negotiation', 'converted', 'lost', 'unresponsive']
        ),
        OpenApiParameter(
            name='priority',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter by priority level',
            enum=['low', 'medium', 'high', 'urgent']
        ),
        OpenApiParameter(
            name='score_min',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Minimum AI score (0-100)'
        ),
        OpenApiParameter(
            name='score_max',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Maximum AI score (0-100)'
        ),
        OpenApiParameter(
            name='assigned_to',
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description='Filter by assigned user ID'
        ),
        OpenApiParameter(
            name='source',
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description='Filter by lead source ID'
        ),
        OpenApiParameter(
            name='tags',
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description='Filter by tag IDs (comma-separated)'
        ),
        OpenApiParameter(
            name='search',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Search across name, email, company, and notes'
        ),
        OpenApiParameter(
            name='created_today',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter leads created today'
        ),
        OpenApiParameter(
            name='is_overdue',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter leads with overdue follow-ups'
        ),
    ],
    examples=[
        OpenApiExample(
            'High priority leads',
            value={'priority': 'high'},
            request_only=True,
        ),
        OpenApiExample(
            'New leads with high score',
            value={'status': 'new', 'score_min': 70},
            request_only=True,
        ),
    ]
)

LEAD_CREATE_SCHEMA = extend_schema(
    summary="Create a new lead",
    description="Create a new lead with AI scoring and automatic tenant assignment.",
    examples=[
        OpenApiExample(
            'Basic lead creation',
            value={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '+1-555-0123',
                'company': 'Acme Corp',
                'job_title': 'CTO',
                'status': 'new',
                'priority': 'medium',
                'source_id': 'uuid-of-source',
                'notes': 'Interested in our enterprise solution'
            },
            request_only=True,
        ),
    ]
)

LEAD_UPDATE_SCHEMA = extend_schema(
    summary="Update a lead",
    description="Update lead information. AI score will be recalculated if relevant fields change.",
)

LEAD_RETRIEVE_SCHEMA = extend_schema(
    summary="Get lead details",
    description="Get detailed information about a specific lead including activities and notes.",
)

LEAD_DELETE_SCHEMA = extend_schema(
    summary="Delete a lead",
    description="Delete a lead and all associated activities and notes.",
)

# Lead Actions Documentation
LEAD_UPDATE_SCORE_SCHEMA = extend_schema(
    summary="Update AI score",
    description="Manually trigger AI score recalculation for a lead.",
    examples=[
        OpenApiExample(
            'Update score with custom factors',
            value={
                'score_factors': {
                    'custom_factor': 25,
                    'manual_adjustment': 10
                }
            },
            request_only=True,
        ),
    ]
)

LEAD_BULK_UPDATE_SCHEMA = extend_schema(
    summary="Bulk update leads",
    description="Update multiple leads at once with the same values.",
    examples=[
        OpenApiExample(
            'Assign multiple leads to user',
            value={
                'lead_ids': ['uuid1', 'uuid2', 'uuid3'],
                'assigned_to_id': 'user-uuid',
                'status': 'contacted'
            },
            request_only=True,
        ),
    ]
)

LEAD_CONVERT_SCHEMA = extend_schema(
    summary="Convert lead to customer",
    description="Mark a lead as converted and optionally set conversion value.",
    examples=[
        OpenApiExample(
            'Convert with value',
            value={'conversion_value': 50000},
            request_only=True,
        ),
    ]
)

LEAD_MARK_CONTACTED_SCHEMA = extend_schema(
    summary="Mark lead as contacted",
    description="Update lead status to contacted and set contact timestamps.",
)

LEAD_MARK_LOST_SCHEMA = extend_schema(
    summary="Mark lead as lost",
    description="Mark lead as lost with optional reason.",
    examples=[
        OpenApiExample(
            'Mark lost with reason',
            value={'reason': 'Budget constraints'},
            request_only=True,
        ),
    ]
)

LEAD_AI_INSIGHTS_SCHEMA = extend_schema(
    summary="Get AI insights",
    description="Get AI-powered insights and recommendations for a lead.",
)

LEAD_DASHBOARD_STATS_SCHEMA = extend_schema(
    summary="Get dashboard statistics",
    description="Get aggregated statistics for leads dashboard.",
)

# Lead Source Documentation
LEAD_SOURCE_LIST_SCHEMA = extend_schema(
    summary="List lead sources",
    description="Get all lead sources for the current tenant with performance statistics.",
)

LEAD_SOURCE_CREATE_SCHEMA = extend_schema(
    summary="Create lead source",
    description="Create a new lead source for tracking lead origins.",
    examples=[
        OpenApiExample(
            'Create website source',
            value={
                'name': 'Website Contact Form',
                'description': 'Leads from main website contact form',
                'is_active': True
            },
            request_only=True,
        ),
    ]
)

# Lead Tag Documentation
LEAD_TAG_LIST_SCHEMA = extend_schema(
    summary="List lead tags",
    description="Get all lead tags for the current tenant.",
)

LEAD_TAG_CREATE_SCHEMA = extend_schema(
    summary="Create lead tag",
    description="Create a new lead tag for categorization.",
    examples=[
        OpenApiExample(
            'Create hot lead tag',
            value={
                'name': 'Hot Lead',
                'color': '#ff4444',
                'description': 'High-priority leads requiring immediate attention',
                'is_active': True
            },
            request_only=True,
        ),
    ]
)

# Lead Activity Documentation
LEAD_ACTIVITY_LIST_SCHEMA = extend_schema(
    summary="List lead activities",
    description="Get activities for leads with filtering by type and status.",
    parameters=[
        OpenApiParameter(
            name='activity_type',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Filter by activity type',
            enum=['note', 'email', 'call', 'meeting', 'contact', 'follow_up', 'proposal', 'convert', 'lost']
        ),
        OpenApiParameter(
            name='is_completed',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter by completion status'
        ),
        OpenApiParameter(
            name='lead',
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description='Filter by lead ID'
        ),
    ]
)

LEAD_ACTIVITY_CREATE_SCHEMA = extend_schema(
    summary="Create lead activity",
    description="Create a new activity record for a lead.",
    examples=[
        OpenApiExample(
            'Schedule follow-up call',
            value={
                'lead_id': 'lead-uuid',
                'activity_type': 'follow_up',
                'title': 'Follow-up call scheduled',
                'description': 'Call to discuss proposal feedback',
                'scheduled_at': '2024-01-15T10:00:00Z',
                'is_completed': False
            },
            request_only=True,
        ),
    ]
)

# Lead Note Documentation
LEAD_NOTE_LIST_SCHEMA = extend_schema(
    summary="List lead notes",
    description="Get notes for leads with privacy filtering.",
    parameters=[
        OpenApiParameter(
            name='is_private',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='Filter by privacy status'
        ),
        OpenApiParameter(
            name='lead',
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            description='Filter by lead ID'
        ),
    ]
)

LEAD_NOTE_CREATE_SCHEMA = extend_schema(
    summary="Create lead note",
    description="Create a new note for a lead.",
    examples=[
        OpenApiExample(
            'Create private note',
            value={
                'lead_id': 'lead-uuid',
                'content': 'Called and left voicemail. Will try again tomorrow.',
                'is_private': True
            },
            request_only=True,
        ),
    ]
)