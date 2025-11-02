# AI Assistant Backend Service Specification

This document outlines the required backend service implementation for the Client Portal AI Assistant.

## Service Overview

**Service Name**: AI Assistant Service  
**Port**: 8001  
**Base Path**: `/ai`  
**Technology Stack**: FastAPI + LangChain + CrewAI  
**Database**: PostgreSQL with pgvector extension  

## API Endpoints

### 1. Chat Endpoint
Handle conversational interactions with context awareness.

```http
POST /ai/chat
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "Check my account status",
  "context": {
    "userId": "user_123",
    "tenantId": "tenant_456",
    "currentPage": "/dashboard",
    "userProfile": {
      "name": "John Doe",
      "role": "admin",
      "subscription": {
        "plan": "pro",
        "status": "active",
        "features": ["advanced_analytics"]
      }
    },
    "platformContext": {
      "activeFeatures": ["crm", "analytics"],
      "recentAlerts": [],
      "accountStatus": {
        "health": "good"
      }
    }
  },
  "conversationId": "conv_abc123",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response:**
```json
{
  "message": "Your account is in excellent health! Here's your current status:\n\n**Subscription:** Pro Plan (Active)\n**Usage This Month:**\n- API Calls: 2,450 / 10,000\n- Storage: 8.2GB / 100GB\n- Active Campaigns: 5\n\n✅ Everything looks great! Is there anything specific you'd like me to help you with?",
  "intent": "account_inquiry",
  "confidence": 0.95,
  "actions": [
    {
      "id": "view_billing",
      "label": "View Billing Details",
      "type": "link",
      "action": "/billing",
      "variant": "outline"
    },
    {
      "id": "upgrade_plan",
      "label": "Upgrade Plan",
      "type": "link",
      "action": "/billing/upgrade",
      "variant": "primary"
    }
  ],
  "data": {
    "accountStatus": {
      "subscription": {
        "plan": "pro",
        "status": "active",
        "nextBilling": "2024-02-15",
        "amount": "$99.00"
      },
      "usage": {
        "apiCalls": { "current": 2450, "limit": 10000 },
        "storage": { "current": 8.2, "limit": 100, "unit": "GB" },
        "activeCampaigns": 5
      },
      "health": "excellent"
    }
  },
  "followUpQuestions": [
    "How can I optimize my API usage?",
    "What new features are available in my plan?",
    "How do I set up billing alerts?"
  ]
}
```

### 2. Intent Analysis
Analyze user message intent and extract entities.

```http
POST /ai/analyze-intent
Content-Type: application/json
Authorization: Bearer <token>

{
  "message": "I'm having trouble with my Google Ads integration",
  "context": {
    "userId": "user_123",
    "tenantId": "tenant_456",
    "currentPage": "/integrations"
  }
}
```

**Response:**
```json
{
  "intent": "technical_support",
  "confidence": 0.88,
  "entities": {
    "integration_type": "google_ads",
    "issue_category": "connection_problem",
    "urgency": "medium"
  },
  "suggestedActions": [
    "check_integration_status",
    "review_api_credentials",
    "test_connection"
  ]
}
```

### 3. Knowledge Base Search
Search platform documentation and help articles.

```http
POST /ai/knowledge-base/search
Content-Type: application/json
Authorization: Bearer <token>

{
  "query": "How to set up Google Ads API integration",
  "context": ["integration", "google_ads", "api_setup"],
  "filters": {
    "category": "technical",
    "tags": ["google_ads", "api", "setup"],
    "dateRange": {
      "start": "2023-01-01T00:00:00Z",
      "end": "2024-01-15T23:59:59Z"
    }
  },
  "limit": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "kb_001",
      "title": "Google Ads API Integration Setup Guide",
      "content": "Step-by-step guide to connect your Google Ads account...",
      "relevanceScore": 0.95,
      "category": "integration_guides",
      "tags": ["google_ads", "api", "setup", "oauth"],
      "lastUpdated": "2024-01-10T12:00:00Z",
      "url": "/help/integrations/google-ads-setup"
    },
    {
      "id": "kb_002",
      "title": "Troubleshooting Google Ads Connection Issues",
      "content": "Common problems and solutions for Google Ads API...",
      "relevanceScore": 0.87,
      "category": "troubleshooting",
      "tags": ["google_ads", "troubleshooting", "api_errors"],
      "lastUpdated": "2024-01-08T09:30:00Z",
      "url": "/help/troubleshooting/google-ads"
    }
  ],
  "totalCount": 12,
  "searchTime": 0.045
}
```

### 4. Account Status
Retrieve comprehensive account information.

```http
POST /ai/account-status
Content-Type: application/json
Authorization: Bearer <token>

{
  "userId": "user_123",
  "tenantId": "tenant_456",
  "includeUsage": true,
  "includeBilling": true,
  "includeIntegrations": true
}
```

**Response:**
```json
{
  "account": {
    "id": "user_123",
    "tenantId": "tenant_456",
    "status": "active",
    "createdAt": "2023-06-15T10:00:00Z",
    "lastLogin": "2024-01-15T08:30:00Z"
  },
  "subscription": {
    "plan": "pro",
    "status": "active",
    "features": ["advanced_analytics", "api_access", "priority_support"],
    "limits": {
      "apiCalls": 10000,
      "storage": 100,
      "campaigns": 50,
      "integrations": 25
    },
    "billing": {
      "nextBillingDate": "2024-02-15",
      "amount": 99.00,
      "currency": "USD",
      "paymentMethod": "card_ending_4242"
    }
  },
  "usage": {
    "currentPeriod": {
      "start": "2024-01-01T00:00:00Z",
      "end": "2024-01-31T23:59:59Z"
    },
    "metrics": {
      "apiCalls": { "used": 2450, "limit": 10000, "percentage": 24.5 },
      "storage": { "used": 8.2, "limit": 100, "unit": "GB", "percentage": 8.2 },
      "activeCampaigns": { "count": 5, "limit": 50 },
      "activeIntegrations": { "count": 8, "limit": 25 }
    }
  },
  "integrations": [
    {
      "id": "google_ads",
      "name": "Google Ads",
      "status": "connected",
      "lastSync": "2024-01-15T06:00:00Z",
      "health": "good"
    },
    {
      "id": "facebook_ads",
      "name": "Facebook Ads",
      "status": "error",
      "lastSync": "2024-01-14T18:30:00Z",
      "health": "poor",
      "error": "Invalid access token"
    }
  ],
  "alerts": [
    {
      "id": "alert_001",
      "type": "integration_error",
      "severity": "medium",
      "message": "Facebook Ads integration requires reauthentication",
      "createdAt": "2024-01-15T07:00:00Z"
    }
  ]
}
```

### 5. Analytics Overview
Provide analytics insights and performance data.

```http
POST /ai/analytics-overview
Content-Type: application/json
Authorization: Bearer <token>

{
  "userId": "user_123",
  "tenantId": "tenant_456",
  "timeRange": "last_30_days",
  "metrics": ["traffic", "conversions", "revenue", "campaigns"],
  "includeComparisons": true,
  "includeInsights": true
}
```

**Response:**
```json
{
  "timeRange": {
    "period": "last_30_days",
    "start": "2023-12-16T00:00:00Z",
    "end": "2024-01-15T23:59:59Z"
  },
  "metrics": {
    "traffic": {
      "visitors": 15420,
      "pageViews": 45680,
      "sessions": 12350,
      "bounceRate": 0.34,
      "avgSessionDuration": 245.5
    },
    "conversions": {
      "total": 487,
      "rate": 0.039,
      "value": 48750.00,
      "topSources": ["google_ads", "organic", "facebook_ads"]
    },
    "revenue": {
      "total": 48750.00,
      "currency": "USD",
      "breakdown": {
        "google_ads": 28500.00,
        "organic": 12800.00,
        "facebook_ads": 7450.00
      }
    },
    "campaigns": {
      "active": 5,
      "performance": [
        {
          "id": "camp_001",
          "name": "Q1 Product Launch",
          "status": "active",
          "impressions": 125000,
          "clicks": 3750,
          "ctr": 0.03,
          "conversions": 180,
          "cost": 8500.00,
          "roas": 3.35
        }
      ]
    }
  },
  "trends": {
    "visitors": 0.15,
    "conversions": -0.08,
    "revenue": 0.22,
    "campaignPerformance": 0.12
  },
  "insights": [
    {
      "type": "opportunity",
      "category": "campaign_optimization",
      "title": "Optimize Google Ads Campaign",
      "description": "Your Q1 Product Launch campaign is performing 35% above average. Consider increasing budget by 20% to maximize returns.",
      "impact": "high",
      "effort": "low",
      "estimatedLift": "15-25% revenue increase"
    },
    {
      "type": "alert",
      "category": "performance_decline",
      "title": "Facebook Ads Conversion Drop",
      "description": "Facebook Ads conversions are down 8% compared to last month. Review ad creative and audience targeting.",
      "impact": "medium",
      "effort": "medium",
      "recommendations": ["refresh_creative", "audit_targeting", "check_landing_pages"]
    }
  ]
}
```

### 6. Human Escalation
Escalate conversation to human support agent.

```http
POST /ai/escalate
Content-Type: application/json
Authorization: Bearer <token>

{
  "conversationId": "conv_abc123",
  "reason": "Complex billing inquiry requiring human review",
  "context": {
    "userId": "user_123",
    "tenantId": "tenant_456",
    "userProfile": { ... },
    "conversationHistory": [
      {
        "timestamp": "2024-01-15T10:25:00Z",
        "type": "user",
        "message": "I was charged twice this month"
      },
      {
        "timestamp": "2024-01-15T10:25:30Z",
        "type": "assistant",
        "message": "I understand your concern about the billing charge..."
      }
    ]
  },
  "priority": "normal",
  "category": "billing"
}
```

**Response:**
```json
{
  "ticketId": "TICKET-2024-001234",
  "estimatedWaitTime": 15,
  "queuePosition": 3,
  "agentAvailability": {
    "business": true,
    "priority": false
  },
  "escalationDetails": {
    "department": "billing_support",
    "skillsRequired": ["billing", "subscription_management"],
    "context": "Complex billing inquiry with duplicate charges"
  },
  "followUp": {
    "email": "support@bizosaas.com",
    "phone": "+1-800-555-0123",
    "expectedResponse": "within 30 minutes"
  }
}
```

### 7. Feedback Recording
Record user feedback for AI responses.

```http
POST /ai/feedback
Content-Type: application/json
Authorization: Bearer <token>

{
  "conversationId": "conv_abc123",
  "messageId": "msg_xyz789",
  "feedback": "positive",
  "comment": "Very helpful and accurate response",
  "rating": 5,
  "categories": ["accuracy", "helpfulness", "speed"],
  "timestamp": "2024-01-15T10:35:00Z"
}
```

**Response:**
```json
{
  "status": "recorded",
  "feedbackId": "feedback_456",
  "message": "Thank you for your feedback! It helps us improve our AI assistant."
}
```

## WebSocket Events

### Connection
```
ws://localhost:8001/ai/ws?token=<auth_token>&conversationId=<conv_id>
```

### Message Types

#### 1. Chat Message
```json
{
  "type": "chat_message",
  "messageId": "msg_123",
  "conversationId": "conv_abc",
  "message": "Hello, I need help",
  "context": { ... },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Typing Indicator
```json
{
  "type": "typing_indicator",
  "conversationId": "conv_abc",
  "isTyping": true,
  "estimatedResponseTime": 3000
}
```

#### 3. Connection Status
```json
{
  "type": "connection_status",
  "connected": true,
  "latency": 45,
  "serverTime": "2024-01-15T10:30:00Z"
}
```

#### 4. Assistant Response
```json
{
  "type": "assistant_response",
  "messageId": "msg_124",
  "conversationId": "conv_abc",
  "message": "I can help you with that...",
  "metadata": {
    "intent": "general_help",
    "confidence": 0.92,
    "actions": [...],
    "processingTime": 2.34
  },
  "timestamp": "2024-01-15T10:30:03Z"
}
```

## Database Schema

### Conversations Table
```sql
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    session_id UUID,
    status VARCHAR(20) DEFAULT 'active',
    context JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    escalated BOOLEAN DEFAULT FALSE,
    satisfaction_rating INTEGER,
    
    INDEX idx_conversations_user (user_id),
    INDEX idx_conversations_tenant (tenant_id),
    INDEX idx_conversations_session (session_id)
);
```

### Messages Table
```sql
CREATE TABLE ai_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES ai_conversations(id),
    type VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    metadata JSONB,
    intent VARCHAR(50),
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_messages_conversation (conversation_id),
    INDEX idx_messages_type (type),
    INDEX idx_messages_intent (intent)
);
```

### Knowledge Base Table
```sql
CREATE TABLE ai_knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    content_vector vector(1536), -- OpenAI embedding dimension
    category VARCHAR(100),
    tags TEXT[],
    url VARCHAR(500),
    relevance_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_kb_category (category),
    INDEX idx_kb_tags USING GIN (tags),
    INDEX idx_kb_vector USING ivfflat (content_vector vector_cosine_ops)
);
```

### Feedback Table
```sql
CREATE TABLE ai_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES ai_conversations(id),
    message_id UUID NOT NULL REFERENCES ai_messages(id),
    user_id UUID NOT NULL,
    feedback_type VARCHAR(20) NOT NULL, -- 'positive', 'negative'
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    categories TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_feedback_conversation (conversation_id),
    INDEX idx_feedback_message (message_id),
    INDEX idx_feedback_type (feedback_type)
);
```

## Environment Variables

```env
# AI Service Configuration
AI_SERVICE_PORT=8001
AI_SERVICE_HOST=0.0.0.0

# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/bizosaas
VECTOR_DB_URL=postgresql://user:password@localhost:5432/bizosaas

# Redis Configuration (for caching and session management)
REDIS_URL=redis://localhost:6379/1

# Security
JWT_SECRET=your-jwt-secret
API_RATE_LIMIT=100  # requests per minute per user

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
MAX_CONVERSATION_HISTORY=50
RESPONSE_TIMEOUT=30  # seconds
EMBEDDING_CACHE_TTL=86400  # 24 hours
```

## Implementation Guidelines

### 1. FastAPI Service Structure
```
ai-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app and routes
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   │   ├── ai_service.py    # Main AI service
│   │   ├── knowledge_service.py
│   │   ├── intent_service.py
│   │   └── escalation_service.py
│   ├── database/            # Database models and operations
│   ├── utils/               # Utility functions
│   └── config.py            # Configuration management
├── requirements.txt
└── Dockerfile
```

### 2. Key Dependencies
```txt
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.0.4
crewai>=0.24.0
psycopg2-binary>=2.9.9
pgvector>=0.2.4
redis>=5.0.1
pydantic>=2.5.0
sqlalchemy>=2.0.23
alembic>=1.13.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
websockets>=12.0
```

### 3. Performance Optimizations
- **Async Operations**: Use async/await for all I/O operations
- **Connection Pooling**: Configure database and Redis connection pools
- **Caching**: Cache frequent queries and AI responses
- **Rate Limiting**: Implement user-based rate limiting
- **Background Tasks**: Use FastAPI background tasks for non-blocking operations

### 4. Security Measures
- **Authentication**: JWT token validation for all endpoints
- **Authorization**: Tenant-based access control
- **Input Validation**: Strict input validation using Pydantic
- **SQL Injection Prevention**: Use parameterized queries
- **CORS Configuration**: Configure appropriate CORS settings
- **Rate Limiting**: Prevent abuse with rate limiting

### 5. Monitoring and Logging
- **Structured Logging**: Use JSON format for structured logs
- **Metrics Collection**: Track response times, error rates, user satisfaction
- **Health Checks**: Implement comprehensive health check endpoints
- **Distributed Tracing**: Add tracing for debugging complex flows