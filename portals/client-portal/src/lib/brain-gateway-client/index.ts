// Export base client and utilities
export { BaseApiClient, apiClient, type ApiError, type RequestOptions } from './utils/base-client'

// Import API clients
import { ProjectsClient, projectsClient } from './clients/projects'
import { ContentClient, contentClient, type ContentListParams } from './clients/content'
import { AnalyticsClient, analyticsClient } from './clients/analytics'

// Re-export API clients
export { ProjectsClient, projectsClient }
export { ContentClient, contentClient, type ContentListParams }
export { AnalyticsClient, analyticsClient }

import { BaseApiClient, apiClient } from './utils/base-client'
import { OnboardingClient, onboardingClient } from './clients/onboarding'
import { PersonaClient, personaClient } from './clients/persona'
import { SeoClient } from './clients/seo'
import { SocialClient } from './clients/social'

const seoClient = new SeoClient(apiClient)
const socialClient = new SocialClient(apiClient)

// Combined brain gateway client
export const brainGateway = {
  projects: projectsClient,
  content: contentClient,
  analytics: analyticsClient,
  onboarding: onboardingClient,
  persona: personaClient,
  seo: seoClient,
  social: socialClient,
}

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
