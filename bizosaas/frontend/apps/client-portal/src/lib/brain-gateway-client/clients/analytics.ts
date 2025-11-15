/**
 * Analytics API Client
 * Handles all analytics and metrics operations
 */

import { apiClient } from '../utils/base-client'
import type { AnalyticsMetrics, AnalyticsQuery } from '../types'

export class AnalyticsClient {
  private basePath = '/api/analytics'

  /**
   * Get metrics for a specific time period
   */
  async getMetrics(query: AnalyticsQuery): Promise<AnalyticsMetrics[]> {
    return apiClient.get<AnalyticsMetrics[]>(`${this.basePath}/metrics`, {
      params: query as unknown as Record<string, string | number | boolean>,
    })
  }

  /**
   * Get dashboard overview metrics
   */
  async getDashboard(): Promise<{
    today: AnalyticsMetrics
    week: AnalyticsMetrics
    month: AnalyticsMetrics
    year: AnalyticsMetrics
  }> {
    return apiClient.get(`${this.basePath}/dashboard`)
  }

  /**
   * Get project-specific metrics
   */
  async getProjectMetrics(
    projectId: string,
    query?: AnalyticsQuery
  ): Promise<AnalyticsMetrics[]> {
    return apiClient.get<AnalyticsMetrics[]>(
      `${this.basePath}/projects/${projectId}`,
      { params: query as unknown as Record<string, string | number | boolean> }
    )
  }

  /**
   * Get campaign performance metrics
   */
  async getCampaignMetrics(
    campaignId: string
  ): Promise<AnalyticsMetrics> {
    return apiClient.get<AnalyticsMetrics>(
      `${this.basePath}/campaigns/${campaignId}`
    )
  }

  /**
   * Get real-time metrics
   */
  async getRealtime(): Promise<{
    active_users: number
    active_sessions: number
    page_views_per_minute: number
  }> {
    return apiClient.get(`${this.basePath}/realtime`)
  }

  /**
   * Export analytics data to CSV
   */
  async exportData(query: AnalyticsQuery): Promise<Blob> {
    const response = await fetch(
      `${apiClient['baseUrl']}${this.basePath}/export?${new URLSearchParams(query as unknown as Record<string, string>)}`,
      {
        credentials: 'include',
      }
    )

    if (!response.ok) {
      throw new Error('Export failed')
    }

    return response.blob()
  }
}

export const analyticsClient = new AnalyticsClient()
