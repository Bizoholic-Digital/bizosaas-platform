/**
 * API Module Exports
 *
 * All frontend services access backend via brain-gateway through these modules
 */

export { ApiClient, apiClient } from './client'
export type { ApiClientConfig } from './client'

export { cmsApi } from './cms'
export { crmApi } from './crm'
