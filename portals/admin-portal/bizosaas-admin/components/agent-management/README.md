# Agent Management UI System

A comprehensive React-based UI system for managing and monitoring the BizOSaaS AI agent ecosystem.

## Overview

The Agent Management UI provides administrators with complete visibility and control over the hierarchical AI agent system, including:

- **Master Orchestration Layer**: 1 Master Business Supervisor
- **Domain Supervisors**: 6 specialized domain supervisors (70% complete)
- **Specialist Agents**: 32 specialist agents across all domains

## Components

### 1. AgentDashboard (Main Component)
- **File**: `agent-dashboard.tsx`
- **Purpose**: Primary dashboard interface with tabbed views
- **Features**:
  - Real-time agent status overview
  - Search and filtering capabilities
  - Grid view of all agents with quick actions
  - Integrated tabs for hierarchy, metrics, and logs

### 2. AgentHierarchy
- **File**: `agent-hierarchy.tsx`
- **Purpose**: Tree-style hierarchical visualization
- **Features**:
  - Expandable/collapsible agent tree
  - Master → Supervisor → Specialist hierarchy display
  - Real-time status indicators
  - Individual agent controls within hierarchy

### 3. AgentMetrics
- **File**: `agent-metrics.tsx`
- **Purpose**: Performance analytics and monitoring
- **Features**:
  - System-wide performance overview
  - Domain-specific performance breakdown
  - Individual agent deep-dive metrics
  - Resource utilization monitoring
  - Historical performance trends

### 4. AgentLogs
- **File**: `agent-logs.tsx`
- **Purpose**: Real-time activity monitoring and debugging
- **Features**:
  - Live log streaming with auto-scroll
  - Log level filtering (error, warning, success, info, debug)
  - Search functionality across all logs
  - Time-based filtering
  - Detailed log expansion with metadata
  - Export capabilities

### 5. AgentControls
- **File**: `agent-controls.tsx`
- **Purpose**: Agent configuration and control panel
- **Features**:
  - Start/stop/restart agent operations
  - Configuration management
  - Environment variable editing
  - Resource limit adjustment
  - Performance monitoring
  - Real-time status updates

## State Management

### AgentStore (Zustand)
- **File**: `lib/stores/agent-store.ts`
- **Purpose**: Centralized state management for agent data
- **Features**:
  - Agent CRUD operations
  - Real-time status updates
  - Performance metrics tracking
  - Error handling and recovery
  - Optimistic updates

## Data Architecture

### Agent Hierarchy Structure
```
Master Business Supervisor (ACTIVE)
├── Strategic Decision Coordinator ✅
├── Resource Allocation Manager ✅
└── Cross-Platform Orchestrator ✅

Domain Supervisors (70% Complete)
├── CRM Domain Supervisor ✅
│   ├── Lead Scoring Agent ✅
│   ├── Lead Assignment Agent ✅
│   ├── Nurturing Campaign Agent ✅
│   ├── Sales Pipeline Agent ✅
│   ├── Customer Segmentation Agent ✅
│   └── Relationship Scoring Agent ✅
│
├── E-commerce Domain Supervisor ✅
│   ├── Product Recommendation Agent ✅
│   ├── Inventory Optimization Agent ⭐ (Starting)
│   ├── Price Optimization Agent ⭐ (Starting)
│   ├── Order Fulfillment Agent ⭐ (Starting)
│   ├── Customer Service Agent 📋 (Inactive)
│   └── Fraud Detection Agent 📋 (Inactive)
│
└── Analytics Domain Supervisor ✅
    ├── Data Collection Agent ✅
    ├── Report Generation Agent ✅
    ├── Insight Discovery Agent 📋 (Inactive)
    ├── Performance Monitoring Agent ✅
    ├── Predictive Analytics Agent 📋 (Inactive)
    └── Dashboard Creation Agent ✅
```

## API Integration

### Brain API Endpoints
- **Base URL**: `http://bizosaas-brain:8001/api/agents/`
- **Authentication**: Bearer token (JWT)

#### Endpoints:
```
GET    /api/agents/                 # List all agents
GET    /api/agents/{id}             # Get specific agent
POST   /api/agents/{id}/start       # Start agent
POST   /api/agents/{id}/stop        # Stop agent
POST   /api/agents/{id}/restart     # Restart agent
PATCH  /api/agents/{id}/config      # Update configuration
GET    /api/agents/{id}/logs        # Get agent logs
GET    /api/agents/{id}/metrics     # Get performance metrics
WebSocket /api/agents/events        # Real-time updates
```

## Features

### Real-time Monitoring
- Live status updates every 30 seconds
- WebSocket integration for instant notifications
- Performance metric streaming
- Log tail functionality

### Control Operations
- Start/stop/restart individual agents
- Bulk operations on multiple agents
- Configuration hot-reloading
- Emergency shutdown procedures

### Performance Analytics
- Success rate tracking
- Response time monitoring
- Resource utilization (CPU, Memory)
- Task completion statistics
- Error rate analysis

### Advanced Filtering
- Multi-criteria search
- Status-based filtering
- Domain grouping
- Time-range selection
- Performance threshold filtering

### User Experience
- Responsive design for all screen sizes
- Keyboard shortcuts for common actions
- Context-sensitive help tooltips
- Accessible design (WCAG 2.1 AA)
- Dark/light theme support

## Usage

### Basic Setup
```tsx
import { AgentDashboard } from '@/components/agent-management'

export default function AgentsPage() {
  return <AgentDashboard />
}
```

### Standalone Components
```tsx
import { 
  AgentHierarchy, 
  AgentMetrics, 
  AgentLogs,
  useAgentStore 
} from '@/components/agent-management'

function CustomAgentView() {
  const { agents, fetchAgents } = useAgentStore()
  
  return (
    <div>
      <AgentHierarchy agents={agents} />
      <AgentMetrics agents={agents} />
      <AgentLogs />
    </div>
  )
}
```

## Configuration

### Environment Variables
```env
NEXT_PUBLIC_BRAIN_API_URL=http://bizosaas-brain:8001
NEXT_PUBLIC_WS_URL=ws://bizosaas-brain:8001/ws
NEXT_PUBLIC_REFRESH_INTERVAL=30000
```

### Agent Status Colors
- **Active**: Green (`#10B981`)
- **Inactive**: Gray (`#6B7280`)
- **Error**: Red (`#EF4444`)
- **Starting**: Yellow (`#F59E0B`)
- **Stopping**: Orange (`#F97316`)

### Performance Thresholds
- **Excellent**: 95%+ success rate
- **Good**: 85-94% success rate
- **Warning**: 70-84% success rate
- **Critical**: <70% success rate

## Development

### Prerequisites
- Node.js 18+
- Next.js 14+
- TypeScript 5+
- Tailwind CSS 3+

### Installation
```bash
npm install @radix-ui/react-* lucide-react zustand axios
```

### Development Commands
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run type-check   # TypeScript validation
npm run lint         # ESLint validation
```

## Error Handling

### Agent Communication Errors
- Automatic retry logic with exponential backoff
- Fallback to cached data when API unavailable
- User-friendly error messages with recovery actions
- Detailed error logging for debugging

### Performance Optimization
- Virtual scrolling for large agent lists
- Debounced search and filter operations
- Lazy loading of agent details
- Efficient re-rendering with React.memo
- WebSocket connection pooling

## Security Considerations

### Authentication
- JWT token-based authentication
- Role-based access control (RBAC)
- Session timeout handling
- Secure token storage

### Data Protection
- Sensitive data masking in UI
- Encrypted communication with Brain API
- Audit logging for all agent operations
- Input validation and sanitization

## Testing

### Unit Tests
```bash
npm run test         # Run Jest unit tests
npm run test:watch   # Watch mode for development
```

### E2E Tests
```bash
npm run test:e2e     # Playwright end-to-end tests
```

### Test Coverage
- Component rendering tests
- User interaction tests
- API integration tests
- Error boundary tests
- Accessibility tests

## Deployment

### Production Build
```bash
npm run build
npm run start
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
COPY . /app
WORKDIR /app
RUN npm ci --only=production
RUN npm run build
CMD ["npm", "start"]
```

### Monitoring
- Application performance monitoring (APM)
- Error tracking with Sentry
- User analytics with PostHog
- Health check endpoints

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Accessibility

- WCAG 2.1 AA compliance
- Screen reader support
- Keyboard navigation
- High contrast mode
- Reduced motion support

## Contributing

1. Follow the component structure patterns
2. Use TypeScript for all new code
3. Implement comprehensive error handling
4. Add unit tests for new features
5. Update documentation for API changes
6. Follow the established design system

## License

This software is proprietary to BizOSaaS and not licensed for external use.