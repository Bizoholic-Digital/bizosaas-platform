# Client Portal AI Assistant

A comprehensive conversational AI interface that provides natural language support for Client Portal users in the BizOSaaS ecosystem.

## Features

### Core Capabilities
- **Account Management**: Check subscription status, billing history, usage statistics
- **Technical Support**: Troubleshoot integration issues, explain errors, escalate to human support
- **Business Intelligence**: Explain analytics data, provide insights, generate reports
- **Automation Management**: Create/modify workflows, schedule campaigns, monitor performance

### Natural Language Processing
- **Intent Recognition**: Account inquiries, technical support, performance analysis, feature requests
- **Entity Extraction**: Service names, dates, metrics, user names, campaign IDs
- **Context Awareness**: Remember conversation history, understand platform context

### Conversational Interface
- **Rich Chat UI**: Message bubbles, typing indicators, quick actions, voice input
- **Interaction Patterns**: Guided conversations, proactive assistance, multi-turn dialogs
- **File Support**: Screenshot sharing, document attachments

## Architecture

### Frontend Components
- **React 18** with TypeScript for type safety
- **ShadCN UI** components for consistent design
- **Zustand** for local state management
- **WebSocket** connections for real-time communication

### Backend Integration
- **BizOSaaS Brain API** (port 8001): Core business logic
- **Auth Service** (port 8007): User authentication
- **CRM API** (port 8008): Customer data
- **Analytics API**: Performance metrics
- **Billing API**: Subscription information

### AI Services
- **OpenAI GPT-4**: Natural language understanding and generation
- **Anthropic Claude**: Complex reasoning and analysis
- **Speech Recognition**: Browser Web Speech API
- **Knowledge Base**: Vector database for platform documentation

## Usage

### Basic Setup

```tsx
import { AIAssistantProvider } from '@/components/ai-assistant';

function App() {
  return (
    <AIAssistantProvider
      userContext={{
        userId: "user_123",
        tenantId: "tenant_456",
        userProfile: {
          name: "John Doe",
          email: "john@example.com",
          role: "admin",
          subscription: {
            plan: "pro",
            status: "active",
            features: ["advanced_analytics", "api_access"]
          }
        }
      }}
      config={{
        apiEndpoint: process.env.NEXT_PUBLIC_AI_API_ENDPOINT,
        websocketUrl: process.env.NEXT_PUBLIC_AI_WS_URL,
        enableVoiceInput: true,
        enableFileUpload: true
      }}
    >
      <YourAppContent />
    </AIAssistantProvider>
  );
}
```

### Standalone Component

```tsx
import { AIAssistant } from '@/components/ai-assistant';

function Dashboard() {
  return (
    <div>
      <YourDashboardContent />
      <AIAssistant
        initialContext={{
          userId: "user_123",
          tenantId: "tenant_456",
          currentPage: "/dashboard",
          userProfile: {
            // ... user profile data
          }
        }}
      />
    </div>
  );
}
```

### Using the Hook

```tsx
import { useAIAssistant } from '@/components/ai-assistant';

function CustomChatInterface() {
  const {
    conversation,
    isOpen,
    sendMessage,
    openAssistant,
    handleQuickAction,
    startVoiceInput
  } = useAIAssistant();

  return (
    <div>
      <button onClick={openAssistant}>
        Open AI Assistant
      </button>
      
      {conversation && (
        <div>
          {conversation.messages.map(message => (
            <div key={message.id}>
              {message.content}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Configuration

### Environment Variables

```env
NEXT_PUBLIC_AI_API_ENDPOINT=http://localhost:8001/ai
NEXT_PUBLIC_AI_WS_URL=ws://localhost:8001/ai/ws
```

### AI Assistant Config

```typescript
interface AIAssistantConfig {
  apiEndpoint: string;
  websocketUrl: string;
  maxMessageHistory: number;
  responseTimeout: number;
  enableVoiceInput: boolean;
  enableFileUpload: boolean;
  personality: {
    tone: 'professional' | 'friendly' | 'casual';
    verbosity: 'concise' | 'detailed' | 'comprehensive';
    proactivity: 'low' | 'medium' | 'high';
  };
}
```

## API Endpoints

### Chat API
```typescript
POST /ai/chat
{
  "message": "Check my account status",
  "context": {
    "userId": "user_123",
    "tenantId": "tenant_456",
    "currentPage": "/dashboard"
  },
  "conversationId": "conv_abc123"
}
```

### Intent Analysis
```typescript
POST /ai/analyze-intent
{
  "message": "I need help with billing",
  "context": { ... }
}
```

### Knowledge Base Search
```typescript
POST /ai/knowledge-base/search
{
  "query": "how to integrate API",
  "context": ["integration", "api"],
  "filters": {
    "category": "technical",
    "tags": ["api", "setup"]
  }
}
```

### Account Status
```typescript
POST /ai/account-status
{
  "userId": "user_123",
  "tenantId": "tenant_456"
}
```

### Analytics Overview
```typescript
POST /ai/analytics-overview
{
  "userId": "user_123",
  "tenantId": "tenant_456",
  "timeRange": "last_30_days"
}
```

### Escalation
```typescript
POST /ai/escalate
{
  "conversationId": "conv_abc123",
  "reason": "Complex technical issue",
  "context": { ... }
}
```

## Components

### AIAssistant
Main component that renders the complete AI assistant interface.

**Props:**
- `initialContext`: User and platform context
- `className`: CSS classes for styling

### MessageBubble
Individual message component with support for rich content and actions.

**Props:**
- `message`: Message object with content and metadata
- `onQuickAction`: Handler for quick action buttons
- `onFeedback`: Handler for user feedback

### ChatInput
Input component with support for text, voice, and file uploads.

**Props:**
- `onSendMessage`: Handler for sending messages
- `onStartVoiceInput`: Handler for voice input
- `onFileUpload`: Handler for file uploads
- `isLoading`: Loading state
- `isVoiceAvailable`: Voice input availability

### TypingIndicator
Visual indicator when AI is processing a response.

## State Management

### Zustand Store
The AI Assistant uses Zustand for state management with the following store structure:

```typescript
interface AIAssistantStore {
  conversation: ConversationState | null;
  isOpen: boolean;
  isMinimized: boolean;
  isTyping: boolean;
  isConnected: boolean;
  config: AIAssistantConfig;
  sessions: ConversationSession[];
  
  // Actions
  openAssistant: () => void;
  closeAssistant: () => void;
  startConversation: (context: ConversationContext) => void;
  sendMessage: (message: string) => void;
  // ... more actions
}
```

### Persistence
- Conversation history (last 5 sessions)
- User preferences and configuration
- Session metadata for analytics

## Styling

The AI Assistant uses the same design system as the Client Portal:

### CSS Variables
```css
:root {
  --ai-assistant-width: 24rem;
  --ai-assistant-height: 32rem;
  --ai-assistant-border-radius: 0.5rem;
  --ai-assistant-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

### Responsive Design
- Mobile: Full screen overlay
- Tablet: Adjusted width and positioning
- Desktop: Fixed positioning with shadow

## Performance

### Optimization Features
- **Lazy Loading**: Components load only when needed
- **Message Virtualization**: Efficient rendering of long conversations
- **Debounced Input**: Reduces API calls during typing
- **Connection Pooling**: Reuse WebSocket connections
- **Caching**: Store frequent responses locally

### Metrics
- Response Time: <2 seconds for simple queries
- Memory Usage: <50MB for 100+ message conversations
- Bundle Size: ~15KB gzipped (without dependencies)

## Security

### Data Protection
- **Encryption**: All conversations encrypted in transit and at rest
- **Access Control**: User permission validation for sensitive data
- **Audit Logging**: Complete conversation tracking
- **Content Filtering**: Inappropriate content detection
- **Rate Limiting**: Prevent abuse and ensure fair usage

### Privacy
- **Data Minimization**: Only collect necessary conversation data
- **Retention Policy**: Conversations auto-deleted after 30 days
- **User Control**: Users can clear history anytime
- **Compliance**: GDPR and CCPA compliant

## Troubleshooting

### Common Issues

#### WebSocket Connection Failed
```typescript
// Check WebSocket URL and network connectivity
console.error('WebSocket connection failed. Falling back to HTTP API.');
```

#### Voice Input Not Working
```typescript
// Ensure HTTPS and microphone permissions
if (!navigator.mediaDevices) {
  console.warn('Voice input requires HTTPS');
}
```

#### API Rate Limiting
```typescript
// Implement exponential backoff
const retryDelay = Math.pow(2, retryCount) * 1000;
setTimeout(retryRequest, retryDelay);
```

### Debug Mode
Enable debug logging:
```typescript
localStorage.setItem('ai-assistant-debug', 'true');
```

## Testing

### Unit Tests
```bash
npm test components/ai-assistant
```

### Integration Tests
```bash
npm run test:integration ai-assistant
```

### E2E Tests
```bash
npm run test:e2e ai-assistant-flow
```

## Deployment

### Production Checklist
- [ ] Configure production API endpoints
- [ ] Set up WebSocket proxy (if needed)
- [ ] Enable error reporting
- [ ] Configure rate limiting
- [ ] Set up monitoring and analytics
- [ ] Test voice input in production environment
- [ ] Verify file upload security

### Monitoring
- **Response Times**: Track API response times
- **Error Rates**: Monitor failed requests
- **User Engagement**: Conversation length and satisfaction
- **Escalation Rates**: Track human handoff frequency

## Contributing

### Development Setup
1. Install dependencies: `npm install`
2. Start development server: `npm run dev`
3. Open http://localhost:3006

### Code Style
- Use TypeScript for all new components
- Follow existing naming conventions
- Add JSDoc comments for public APIs
- Include unit tests for new features

### Pull Request Process
1. Create feature branch from `development`
2. Implement changes with tests
3. Update documentation
4. Create pull request with detailed description