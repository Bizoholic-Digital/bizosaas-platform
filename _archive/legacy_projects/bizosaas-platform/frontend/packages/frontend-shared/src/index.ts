/**
 * @bizosaas/frontend-shared
 *
 * Shared components, utilities, and API client for BizOSaaS frontend microservices
 *
 * ALL frontends communicate with backend services via brain-gateway (API Gateway + CrewAI)
 * This package provides:
 * - Unified API client
 * - Domain-specific API modules (CMS, CRM, E-commerce, AI)
 * - Shared UI components
 * - Common utilities
 */

// ========== API Client ==========
export { ApiClient, apiClient } from './api/client'
export type { ApiClientConfig } from './api/client'

// Domain-specific API modules
export { cmsApi } from './api/cms'
export { crmApi } from './api/crm'

// ========== Components ==========
export { LoadingSkeleton } from './components/LoadingSkeleton'
export type { LoadingSkeletonProps } from './components/LoadingSkeleton'

// ========== Hooks, Utils, Types (to be added) ==========
// export * from './hooks'
// export * from './utils'
// export * from './types'
