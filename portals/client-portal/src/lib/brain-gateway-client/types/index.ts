/**
 * Common TypeScript types for Brain Gateway API responses
 */

// Pagination
export interface PaginationParams {
  page?: number
  limit?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  total_pages: number
}

// Common response format
export interface ApiResponse<T> {
  data: T
  message?: string
  status: 'success' | 'error'
}

// Project types
export interface Project {
  id: string
  name: string
  description?: string
  status: 'active' | 'paused' | 'completed' | 'archived'
  tenant_id: string
  created_at: string
  updated_at: string
}

export interface CreateProjectData {
  name: string
  description?: string
  status?: 'active' | 'paused'
}

export interface UpdateProjectData {
  name?: string
  description?: string
  status?: 'active' | 'paused' | 'completed' | 'archived'
}

// Analytics types
export interface AnalyticsMetrics {
  views: number
  clicks: number
  conversions: number
  revenue: number
  period: string
}

export interface AnalyticsQuery {
  start_date: string
  end_date: string
  metric_type?: 'views' | 'clicks' | 'conversions' | 'revenue'
  group_by?: 'day' | 'week' | 'month'
}

// Content types
export interface Content {
  id: string
  title: string
  slug: string
  content_type: 'blog' | 'service' | 'case-study' | 'page'
  status: 'draft' | 'published' | 'archived'
  body?: string
  excerpt?: string
  author_id: string
  tenant_id: string
  created_at: string
  updated_at: string
  published_at?: string
}

export interface AutonomousContentRequest {
  topic: string
  persona_id?: string
  target_cms?: string
  require_approval?: boolean
}

export interface ContentWorkflowStatus {
  workflow_id: string
  phase: string
  status: string
}

export interface ApprovalActionRequest {
  workflow_id: string
  phase: string
  notes?: string
}

export interface CreateContentData {
  title: string
  slug: string
  content_type: 'blog' | 'service' | 'case-study' | 'page'
  status?: 'draft' | 'published'
  body?: string
  excerpt?: string
}

export interface UpdateContentData {
  title?: string
  slug?: string
  status?: 'draft' | 'published' | 'archived'
  body?: string
  excerpt?: string
}

// Campaign types
export interface Campaign {
  id: string
  name: string
  type: 'email' | 'social' | 'ads' | 'seo'
  status: 'draft' | 'active' | 'paused' | 'completed'
  budget?: number
  start_date?: string
  end_date?: string
  tenant_id: string
  created_at: string
  updated_at: string
}

export interface CreateCampaignData {
  name: string
  type: 'email' | 'social' | 'ads' | 'seo'
  status?: 'draft' | 'active'
  budget?: number
  start_date?: string
  end_date?: string
}

// Agent types
export interface Agent {
  id: string
  name: string
  description: string
  role: string
  category: string
  status: 'active' | 'paused' | 'archived'
  capabilities: string[]
  tools: string[]
  icon: string
  color: string
  cost_tier: 'standard' | 'premium' | 'enterprise'
  instructions?: string
  tenant_id: string
  is_system?: boolean
  created_at?: string
  updated_at?: string
}

export interface AgentCreate {
  name: string
  description: string
  role: string
  category?: string
  capabilities?: string[]
  tools?: string[]
  icon?: string
  color?: string
  cost_tier?: string
  instructions?: string
}

export interface AgentUpdate {
  name?: string
  description?: string
  role?: string
  category?: string
  capabilities?: string[]
  tools?: string[]
  icon?: string
  color?: string
  cost_tier?: string
  instructions?: string
  status?: 'active' | 'paused' | 'archived'
}

export interface AgentOptimization {
  id: string
  agent_id: string
  type: 'prompt' | 'performance' | 'cost' | 'latency'
  description: string
  improvement: string
  impact: 'High' | 'Medium' | 'Low'
  status: 'pending' | 'approved' | 'rejected' | 'executed'
  auto_execute: boolean
  potential_savings?: {
    amount: number
    currency: string
    period: string
  }
  suggested_at: string
  executed_at?: string
}

export interface AgentTask {
  id: string
  agent_id: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  result?: unknown
  error?: string
  created_at: string
  completed_at?: string
}

export interface CreateAgentTaskData {
  agent_id: string
  description: string
  context?: Record<string, unknown>
}

// Support ticket types
export interface SupportTicket {
  id: string
  subject: string
  description: string
  status: 'open' | 'in_progress' | 'resolved' | 'closed'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  tenant_id: string
  user_id: string
  assigned_to?: string
  created_at: string
  updated_at: string
}

export interface CreateTicketData {
  subject: string
  description: string
  priority?: 'low' | 'medium' | 'high' | 'urgent'
}
