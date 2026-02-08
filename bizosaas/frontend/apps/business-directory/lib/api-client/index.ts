// Export base client and utilities
export { BaseApiClient, apiClient, type ApiError, type RequestOptions } from './utils/base-client'

// Export all API clients
export { ProjectsClient, projectsClient } from './clients/projects'
export { ContentClient, contentClient, type ContentListParams } from './clients/content'
export { AnalyticsClient, analyticsClient } from './clients/analytics'

// Export all types
export type {
  PaginationParams,
  PaginatedResponse,
  ApiResponse,
  Project,
  CreateProjectData,
  UpdateProjectData,
  AnalyticsMetrics,
  AnalyticsQuery,
  Content,
  CreateContentData,
  UpdateContentData,
  Campaign,
  CreateCampaignData,
  Agent,
  AgentTask,
  CreateAgentTaskData,
  SupportTicket,
  CreateTicketData,
} from './types'
