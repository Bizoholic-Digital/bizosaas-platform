# BizOSaaS AI Chat Service

A comprehensive role-based conversational AI interface that integrates with admin dashboards and CrewAI agents.

## Features

### 🤖 Role-Based AI Assistants
- **InfraBot** (Super Admin): Infrastructure management and system monitoring
- **BizBot** (Tenant Admin): Business operations and analytics
- **MarketBot** (User): Marketing campaigns and lead management  
- **InfoBot** (Read-only): General support and information

### 🚀 Advanced Capabilities
- Real-time WebSocket communication
- LangChain integration for enhanced responses
- Conversation memory and context management
- CrewAI agent integration
- File upload and analysis support
- Multi-modal responses (text, charts, tables)
- Typing indicators and presence
- Cross-platform session management

### 🔐 Security & Authentication
- Unified authentication with auth-service-v2
- Role-based access control (RBAC)
- JWT token verification
- Rate limiting and usage tracking
- Secure session management

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your configuration
nano .env
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Service

```bash
# Development mode
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 3003 --reload
```

### 4. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t bizosaas-ai-chat .
docker run -p 3003:3003 bizosaas-ai-chat
```

## Integration Guide

### Dashboard Integration

#### TailAdmin Dashboard (localhost:3001)

Add to your React components:

```javascript
import { useEffect } from 'react';
import { useAuth } from './hooks/useAuth';

function ChatIntegration() {
    const { token } = useAuth();

    useEffect(() => {
        if (token) {
            // Load chat widget script
            const script = document.createElement('script');
            script.src = 'http://localhost:3003/chat/embed.js';
            script.onload = () => {
                // Initialize chat widget
                window.BizOSaaSChat = new BizOSaaSChat({
                    apiUrl: 'http://localhost:3003',
                    authToken: token,
                    position: 'bottom-right'
                });
            };
            document.head.appendChild(script);
        }
    }, [token]);

    return null; // Chat widget is rendered globally
}
```

#### SQLAdmin Dashboard (localhost:5000)

Add to your Flask/FastAPI templates:

```html
<!-- Load chat widget -->
<script src="http://localhost:3003/chat/embed.js"></script>

<script>
// Initialize after getting auth token
fetch('/api/auth/token')
    .then(response => response.json())
    .then(data => {
        const chat = new BizOSaaSChat({
            apiUrl: 'http://localhost:3003',
            authToken: data.token,
            position: 'bottom-left'
        });
    });
</script>
```

### API Integration

#### Send Message
```bash
POST /chat/message
Authorization: Bearer <jwt-token>
Content-Type: application/json

{
    "message": "How can I optimize my campaign performance?",
    "session_id": "optional-session-id",
    "context": {
        "current_page": "campaigns",
        "campaign_id": "123"
    }
}
```

#### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:3003/chat/ws/session-id?token=jwt-token');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('AI Response:', data.content);
};

ws.send(JSON.stringify({
    type: 'message',
    content: 'Hello, I need help with analytics'
}));
```

## Configuration

### Environment Variables

```bash
# Service Configuration
HOST=0.0.0.0
PORT=3003
LOG_LEVEL=info

# Authentication
AUTH_SERVICE_URL=http://localhost:3002
JWT_SECRET=your-secret-key

# CrewAI Integration
CREW_AI_SERVICE_URL=http://localhost:8000
CREW_AI_TIMEOUT=30

# AI/LLM Configuration
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=your-key

# Database (Optional)
DATABASE_URL=postgresql://user:pass@localhost/db
REDIS_URL=redis://localhost:6379/0
```

### Role Configuration

The service automatically provides different AI assistants based on user roles:

```python
# Available assistants by role
ROLE_ASSISTANTS = {
    UserRole.SUPER_ADMIN: "InfraBot",     # Infrastructure management
    UserRole.TENANT_ADMIN: "BizBot",      # Business operations  
    UserRole.USER: "MarketBot",           # Marketing & campaigns
    UserRole.READONLY: "InfoBot"          # General support
}
```

## API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service health check |
| `/health` | GET | Detailed health status |
| `/chat/assistants` | GET | Get available assistants for user role |
| `/chat/message` | POST | Send chat message and get AI response |
| `/chat/history/{session_id}` | GET | Get chat history for session |
| `/chat/session/{session_id}` | DELETE | Delete chat session |
| `/chat/ws/{session_id}` | WS | WebSocket connection for real-time chat |
| `/chat/widget` | GET | Embeddable chat widget demo |
| `/chat/embed.js` | GET | JavaScript for embedding chat widget |

### WebSocket Message Types

```javascript
// Send message
{
    "type": "message",
    "content": "Your question here"
}

// Typing indicator
{
    "type": "typing", 
    "is_typing": true
}

// Ping/pong for keepalive
{
    "type": "ping"
}
```

## Architecture

### Component Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Admin         │    │   AI Chat        │    │   CrewAI        │
│   Dashboards    │◄──►│   Service        │◄──►│   Agents        │
│                 │    │                  │    │                 │
│ • TailAdmin     │    │ • WebSocket      │    │ • System        │
│ • SQLAdmin      │    │ • REST API       │    │ • Analytics     │
│                 │    │ • LangChain      │    │ • Marketing     │
└─────────────────┘    │ • Memory Mgmt    │    │ • Security      │
                       └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │   Auth Service   │
                       │   (localhost:3002)│
                       └──────────────────┘
```

### Key Components

1. **WebSocket Manager**: Real-time communication
2. **Chat Processor**: Enhanced AI response generation
3. **Agent Selector**: Intelligent agent routing
4. **Memory Manager**: Conversation context and history
5. **CrewAI Integration**: Backend agent communication

## Development

### Adding New Agents

1. Define agent capabilities in `app/agents.py`:

```python
"new_agent": AgentCapability(
    name="New Agent",
    description="Agent description",
    keywords=["keyword1", "keyword2"],
    confidence_threshold=0.7
)
```

2. Add endpoint mapping in `CrewAIIntegration`:

```python
self.agent_endpoints = {
    "new_agent": "/agents/new-endpoint",
    # ... existing agents
}
```

3. Update role assistants configuration:

```python
UserRole.USER: AIAssistant(
    available_agents=["existing_agent", "new_agent"],
    # ... other config
)
```

### Testing

```bash
# Run tests
python -m pytest tests/

# Test specific component
python -m pytest tests/test_chat_processor.py

# Integration tests with live services
python -m pytest tests/integration/ --live-services
```

### Monitoring

The service provides comprehensive monitoring:

- Health checks at `/health`
- Prometheus metrics at `/metrics` (if enabled)
- WebSocket connection statistics
- Conversation analytics
- Agent performance metrics

## Production Deployment

### Docker Compose

```yaml
services:
  ai-chat-service:
    build: .
    ports:
      - "3003:3003"
    environment:
      - ENV=production
      - LOG_LEVEL=warning
      - WORKERS=4
    networks:
      - bizosaas-network
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-chat-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-chat-service
  template:
    spec:
      containers:
      - name: ai-chat-service
        image: bizosaas/ai-chat-service:latest
        ports:
        - containerPort: 3003
```

### Security Checklist

- [ ] Configure CORS origins for production domains
- [ ] Set secure JWT secrets
- [ ] Enable rate limiting
- [ ] Configure SSL/TLS certificates
- [ ] Set up monitoring and logging
- [ ] Implement backup strategies
- [ ] Configure firewall rules

## Support

- **Documentation**: Check `/chat/docs` for API documentation
- **Health Status**: Monitor `/health` endpoint
- **Logs**: Check service logs for troubleshooting
- **Widget Demo**: Visit `/chat/widget` for integration examples

## License

This service is part of the BizOSaaS platform and follows the same licensing terms.