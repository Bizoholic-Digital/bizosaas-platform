// Agent Management Types

export type AgentStatus = 'active' | 'inactive' | 'error' | 'starting' | 'stopping'
export type AgentType = 'master' | 'supervisor' | 'specialist'
export type LogLevel = 'debug' | 'info' | 'warning' | 'error' | 'success'

export interface AgentMetadata {
  version: string
  createdAt: string
  updatedAt: string
  tags: string[]
  category: string
}

export interface AgentConfiguration {
  name: string
  description: string
  enabled: boolean
  autoRestart: boolean
  maxRetries: number
  timeout: number
  memoryLimit: number
  cpuLimit: number
  logLevel: LogLevel
  priority: number
  environment: Record<string, string>
  schedule?: string
  healthCheck?: {
    enabled: boolean
    interval: number
    timeout: number
    retries: number
  }
}

export interface AgentPerformanceMetrics {
  performance: number
  tasksCompleted: number
  successRate: number
  avgResponseTime: number
  errorRate: number
  uptime: number
  throughput: number
  lastHeartbeat: string
  memoryUsage: number
  cpuUsage: number
  diskUsage?: number
  networkLatency?: number
}

export interface AgentTask {
  id: string
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  createdAt: string
  startedAt?: string
  completedAt?: string
  duration?: number
  input?: any
  output?: any
  error?: string
  priority: number
  retryCount: number
}

export interface AgentLog {
  id: string
  timestamp: string
  level: LogLevel
  agentId: string
  agentName: string
  message: string
  details?: any
  duration?: number
  userId?: string
  sessionId?: string
  traceId?: string
  tags?: string[]
}

export interface AgentAlert {
  id: string
  agentId: string
  type: 'performance' | 'error' | 'resource' | 'dependency' | 'security'
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  message: string
  timestamp: string
  acknowledged: boolean
  resolvedAt?: string
  metadata?: Record<string, any>
}

export interface AgentDependency {
  id: string
  name: string
  type: 'agent' | 'service' | 'api' | 'database'
  status: 'healthy' | 'degraded' | 'unhealthy'
  lastCheck: string
  responseTime?: number
  errorRate?: number
}

export interface AgentResource {
  cpu: {
    usage: number
    limit: number
    requests: number
  }
  memory: {
    usage: number
    limit: number
    requests: number
  }
  disk?: {
    usage: number
    limit: number
  }
  network?: {
    bytesIn: number
    bytesOut: number
    connectionsActive: number
  }
}

export interface AgentHierarchyNode {
  id: string
  name: string
  type: AgentType
  status: AgentStatus
  children: AgentHierarchyNode[]
  parent?: string
  level: number
  expanded?: boolean
}

export interface AgentCluster {
  id: string
  name: string
  description: string
  agents: string[]
  status: 'healthy' | 'degraded' | 'critical'
  loadBalancing: 'round-robin' | 'least-connections' | 'weighted'
  autoScaling: {
    enabled: boolean
    minReplicas: number
    maxReplicas: number
    targetCPU: number
    targetMemory: number
  }
}

export interface AgentWorkflow {
  id: string
  name: string
  description: string
  agents: string[]
  steps: {
    id: string
    agentId: string
    action: string
    input?: any
    condition?: string
    timeout?: number
    retries?: number
  }[]
  status: 'draft' | 'active' | 'paused' | 'completed' | 'failed'
  schedule?: string
  createdAt: string
  updatedAt: string
}

// Utility types for API responses
export interface AgentListResponse {
  agents: Agent[]
  total: number
  page: number
  pageSize: number
}

export interface AgentStatsResponse {
  total: number
  active: number
  inactive: number
  error: number
  performance: number
  domains: Record<string, {
    total: number
    active: number
    performance: number
  }>
}

export interface AgentLogsResponse {
  logs: AgentLog[]
  total: number
  page: number
  pageSize: number
  filters: {
    agentId?: string
    level?: LogLevel
    startDate?: string
    endDate?: string
  }
}

// Event types for real-time updates
export interface AgentStatusEvent {
  type: 'agent.status.changed'
  agentId: string
  oldStatus: AgentStatus
  newStatus: AgentStatus
  timestamp: string
}

export interface AgentPerformanceEvent {
  type: 'agent.performance.updated'
  agentId: string
  metrics: Partial<AgentPerformanceMetrics>
  timestamp: string
}

export interface AgentLogEvent {
  type: 'agent.log.created'
  log: AgentLog
}

export interface AgentAlertEvent {
  type: 'agent.alert.created' | 'agent.alert.acknowledged' | 'agent.alert.resolved'
  alert: AgentAlert
}

export type AgentEvent = 
  | AgentStatusEvent 
  | AgentPerformanceEvent 
  | AgentLogEvent 
  | AgentAlertEvent

// Filter and search types
export interface AgentFilter {
  status?: AgentStatus[]
  type?: AgentType[]
  domain?: string[]
  performance?: {
    min?: number
    max?: number
  }
  lastActive?: {
    hours?: number
    days?: number
  }
  tags?: string[]
}

export interface AgentSearchQuery {
  query: string
  filters: AgentFilter
  sortBy: 'name' | 'status' | 'performance' | 'lastActive' | 'tasksCompleted'
  sortOrder: 'asc' | 'desc'
  page: number
  pageSize: number
}

// Complete Agent interface combining all aspects
export interface Agent extends AgentConfiguration, AgentPerformanceMetrics, AgentMetadata {
  id: string
  type: AgentType
  domain: string
  status: AgentStatus
  parentId?: string
  children?: Agent[]
  tasks?: AgentTask[]
  alerts?: AgentAlert[]
  dependencies?: AgentDependency[]
  resources?: AgentResource
  clusterId?: string
}