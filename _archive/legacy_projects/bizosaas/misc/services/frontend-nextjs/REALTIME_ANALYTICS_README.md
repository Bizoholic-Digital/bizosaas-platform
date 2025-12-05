# Real-time Analytics Enhancement

This implementation provides comprehensive real-time analytics with WebSocket live data streaming for the BizOSaaS platform dashboard system.

## 🚀 Features

### Core Real-time Capabilities
- **WebSocket Infrastructure**: Advanced connection management with automatic reconnection
- **Live Dashboard Updates**: Real-time metrics with smooth animations
- **Real-time Charts**: Interactive charts with live data streaming
- **Live Notifications**: Toast messages and notification center
- **Connection Status**: Visual indicators for connection health
- **Performance Optimization**: High-frequency update handling

### Advanced Features
- **Adaptive Throttling**: Intelligent update frequency management
- **Batched Updates**: Efficient handling of high-volume data
- **Performance Monitoring**: Real-time performance metrics
- **Error Recovery**: Automatic reconnection with exponential backoff
- **State Management**: Optimized Zustand store for real-time data

## 📁 File Structure

```
lib/
├── websocket/
│   ├── types.ts              # WebSocket type definitions
│   └── client.ts             # Advanced WebSocket client
├── store/
│   └── realtime-store.ts     # Zustand store for real-time data
├── hooks/
│   ├── useRealtime.ts        # Real-time React hooks
│   └── usePerformanceOptimization.ts # Performance optimization hooks
└── utils.ts                  # Utility functions

components/
├── realtime/
│   ├── RealtimeMetricCard.tsx        # Animated metric cards
│   ├── RealtimeChart.tsx             # Live updating charts
│   ├── RealtimeNotifications.tsx     # Notification system
│   ├── RealtimeStatusIndicator.tsx   # Connection status
│   ├── RealtimeDashboard.tsx         # Enhanced dashboard
│   ├── RealtimeSocialMediaDashboard.tsx # Social media dashboard
│   └── RealtimeTestDashboard.tsx     # Testing dashboard
└── providers/
    └── RealtimeProvider.tsx   # WebSocket provider
```

## 🔧 Configuration

### Environment Variables

```bash
# WebSocket Connection
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8001/ws/realtime
NEXT_PUBLIC_WEBSOCKET_HEARTBEAT_INTERVAL=30000
NEXT_PUBLIC_WEBSOCKET_RECONNECT_ATTEMPTS=10

# Performance Tuning
NEXT_PUBLIC_MAX_UPDATE_FREQUENCY=30
NEXT_PUBLIC_ENABLE_PERFORMANCE_MONITORING=true
NEXT_PUBLIC_ENABLE_ADAPTIVE_THROTTLING=true

# Notifications
NEXT_PUBLIC_ENABLE_TOAST_NOTIFICATIONS=true
NEXT_PUBLIC_MAX_NOTIFICATIONS=100
NEXT_PUBLIC_NOTIFICATION_AUTO_DISMISS=true
```

### WebSocket Configuration

```typescript
const config: WebSocketConfig = {
  url: 'ws://localhost:8001/ws/realtime',
  heartbeatInterval: 30000,
  reconnectInterval: 1000,
  maxReconnectAttempts: 10,
  backoffMultiplier: 1.5,
  maxBackoffDelay: 30000
};
```

## 🎯 Usage

### Basic Setup

```typescript
import { RealtimeProvider } from '@/components/providers/RealtimeProvider';
import { RealtimeDashboard } from '@/components/realtime/RealtimeDashboard';

export default function DashboardPage() {
  return (
    <RealtimeProvider
      config={{
        url: process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8001/ws/realtime'
      }}
      subscription={{
        metrics: ['dashboard', 'social_media', 'campaigns', 'leads', 'system_health', 'ai_agents'],
        notifications: true,
        events: ['campaign', 'lead', 'payment', 'system', 'ai_agent'],
        real_time_updates: true
      }}
      enableToasts={true}
    >
      <RealtimeDashboard />
    </RealtimeProvider>
  );
}
```

### Using Real-time Hooks

```typescript
import { useRealtimeMetrics, useRealtimeNotifications, useConnectionStatus } from '@/lib/hooks/useRealtime';

function MyComponent() {
  const { dashboardMetrics, isConnected } = useRealtimeMetrics();
  const { notifications, unreadCount } = useRealtimeNotifications();
  const { connectionState, reconnect } = useConnectionStatus();

  return (
    <div>
      <h1>Revenue: {dashboardMetrics?.revenue_generated}</h1>
      <p>Notifications: {unreadCount}</p>
      <p>Status: {connectionState.status}</p>
      {!isConnected && <button onClick={reconnect}>Reconnect</button>}
    </div>
  );
}
```

### Real-time Charts

```typescript
import { RealtimeChart } from '@/components/realtime/RealtimeChart';

function ChartComponent() {
  const [data, setData] = useState([]);

  return (
    <RealtimeChart
      data={data}
      type="line"
      title="Revenue Over Time"
      color="#3B82F6"
      height={300}
      isRealtime={true}
      formatValue={(value) => `$${value.toFixed(0)}`}
    />
  );
}
```

### Performance Optimization

```typescript
import { useSmartUpdateScheduler, useBatchedUpdates } from '@/lib/hooks/usePerformanceOptimization';

function OptimizedComponent() {
  const updateData = useSmartUpdateScheduler(
    (newData) => setData(newData),
    {
      maxFrequency: 30,
      batchSize: 5,
      adaptiveThrottling: true
    }
  );

  const batchNotifications = useBatchedUpdates(
    (batch) => processBatch(batch),
    2000,
    10
  );

  return <div>Optimized Component</div>;
}
```

## 📊 WebSocket Message Types

### Metrics Update

```typescript
{
  type: 'metrics_update',
  data: {
    dashboard?: DashboardMetrics,
    social_media?: SocialMediaMetrics,
    campaigns?: CampaignMetrics,
    leads?: LeadMetrics,
    system_health?: SystemHealthMetrics,
    ai_agents?: AIAgentMetrics
  },
  timestamp: number
}
```

### Notification

```typescript
{
  type: 'notification',
  data: {
    id: string,
    title: string,
    message: string,
    severity: 'info' | 'warning' | 'error' | 'success',
    category: 'system' | 'campaign' | 'lead' | 'payment' | 'ai_agent',
    timestamp: number,
    action_url?: string,
    auto_dismiss?: boolean
  }
}
```

### Event

```typescript
{
  type: 'event',
  data: {
    event_type: string,
    entity_type: 'campaign' | 'lead' | 'payment' | 'system' | 'ai_agent',
    entity_id: string,
    details: any,
    timestamp: number
  }
}
```

## 🔍 Performance Monitoring

### Built-in Metrics

- **Connection State**: Real-time connection status
- **Update Frequency**: Updates per second tracking
- **Render Performance**: Frame rate and render time monitoring
- **Memory Usage**: JavaScript heap size tracking
- **Error Rates**: Connection and processing error tracking

### Performance Features

- **Adaptive Throttling**: Automatically adjusts update frequency based on load
- **Batched Updates**: Groups high-frequency updates for efficiency
- **Frame-rate Aware**: Respects browser refresh rate for smooth animations
- **Memory Management**: Automatic cleanup of old data and notifications
- **Queue Management**: Intelligent update scheduling with priority handling

## 🧪 Testing

### Test Dashboard

A comprehensive test dashboard is available at `/dashboard/test` with:

- **Test Scenarios**: Normal load, high frequency, and stress testing
- **Performance Metrics**: Real-time performance monitoring
- **Simulation Controls**: Start/stop/reset testing scenarios
- **Live Activity Feed**: Real-time event monitoring

### Performance Testing

```typescript
// Test different load scenarios
const scenarios = {
  normal: { updateInterval: 5000, errorRate: 0.01 },
  high_frequency: { updateInterval: 1000, errorRate: 0.02 },
  stress_test: { updateInterval: 100, errorRate: 0.05 }
};
```

## 🚨 Error Handling

### Connection Recovery

- **Automatic Reconnection**: Exponential backoff with configurable attempts
- **State Persistence**: Maintains data during temporary disconnections
- **Error Notifications**: User feedback for connection issues
- **Graceful Degradation**: Fallback to polling when WebSocket unavailable

### Performance Safeguards

- **Update Rate Limiting**: Prevents overwhelming the UI
- **Memory Leak Prevention**: Automatic cleanup of resources
- **Error Boundaries**: Component-level error isolation
- **Performance Monitoring**: Real-time performance alerts

## 🔧 Backend Integration

### WebSocket Server Requirements

The backend should implement these WebSocket endpoints:

```
ws://localhost:8001/ws/realtime
```

#### Required Message Handlers

1. **Connection**: Handle client connections and authentication
2. **Subscription**: Process subscription requests for metrics/events
3. **Heartbeat**: Respond to ping/pong messages
4. **Data Streaming**: Send real-time updates based on subscriptions

#### Example Backend Integration

```python
# FastAPI WebSocket endpoint
@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Send metrics update
            await websocket.send_json({
                "type": "metrics_update",
                "data": {
                    "dashboard": get_dashboard_metrics(),
                    "social_media": get_social_media_metrics()
                },
                "timestamp": time.time() * 1000
            })
            
            await asyncio.sleep(5)  # 5-second interval
            
    except WebSocketDisconnect:
        # Handle disconnection
        pass
```

## 📈 Scalability Considerations

### Frontend Optimization

- **Virtual Scrolling**: For large data sets
- **Lazy Loading**: Load components on demand
- **Memoization**: Prevent unnecessary re-renders
- **Code Splitting**: Load real-time features separately

### Performance Limits

- **Maximum Update Frequency**: 30 updates/second (configurable)
- **Maximum Batch Size**: 10 items per batch (configurable)
- **Maximum Notifications**: 100 active notifications
- **Maximum Chart Data Points**: 100 points per chart

## 🔐 Security

### WebSocket Security

- **Authentication**: JWT token validation on connection
- **Rate Limiting**: Prevent abuse of WebSocket connections
- **Input Validation**: Sanitize all incoming messages
- **CORS Configuration**: Proper origin validation

### Data Protection

- **Sensitive Data**: Avoid sending sensitive information via WebSocket
- **Encryption**: Use WSS (WebSocket Secure) in production
- **Access Control**: Implement proper authorization for data access

## 🚀 Deployment

### Production Configuration

```bash
# Production WebSocket URL
NEXT_PUBLIC_WEBSOCKET_URL=wss://api.bizosaas.com/ws/realtime

# Performance settings for production
NEXT_PUBLIC_MAX_UPDATE_FREQUENCY=20
NEXT_PUBLIC_ENABLE_PERFORMANCE_MONITORING=false
NEXT_PUBLIC_ENABLE_ADAPTIVE_THROTTLING=true
```

### Docker Configuration

```dockerfile
# Dockerfile for frontend
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3001
CMD ["npm", "start"]
```

## 🤝 Contributing

### Development Guidelines

1. **Type Safety**: All WebSocket messages must be typed
2. **Performance**: Consider performance impact of new features
3. **Testing**: Include performance tests for real-time features
4. **Documentation**: Update this README for new features

### Code Style

- Use TypeScript for all new code
- Follow React hooks patterns for state management
- Implement proper error boundaries
- Include comprehensive type definitions

## 📚 API Documentation

### Real-time Store Actions

```typescript
// Update metrics
updateDashboardMetrics(metrics: DashboardMetrics)
updateSocialMediaMetrics(metrics: SocialMediaMetrics)

// Manage notifications
addNotification(notification: NotificationMessage['data'])
dismissNotification(id: string)
dismissAllNotifications()

// Activity management
addActivityEvent(event: EventMessage['data'])
markEventAsRead(id: string)
clearOldEvents(olderThanMs?: number)
```

### Connection Management

```typescript
// Connection control
connect(subscription?: SubscriptionOptions): Promise<void>
disconnect(): void
reconnect(): Promise<void>

// Subscription management
subscribe(options: SubscriptionOptions): void
unsubscribe(): void

// Message handling
sendMessage(message: WebSocketMessage): boolean
on(messageType: string, handler: MessageHandler): void
off(messageType: string, handler: MessageHandler): void
```

This implementation provides a robust, scalable, and performant real-time analytics system that enhances the user experience across all BizOSaaS dashboard components.