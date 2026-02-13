/**
 * Content API Client
 * Handles all content management operations (blog, services, case studies)
 */

import { apiClient } from '../utils/base-client'
import type {
  Content,
  CreateContentData,
  UpdateContentData,
  PaginatedResponse,
  PaginationParams,
  AutonomousContentRequest,
  ContentWorkflowStatus,
  ApprovalActionRequest,
} from '../types'

export interface ContentListParams extends PaginationParams {
  content_type?: 'blog' | 'service' | 'case-study' | 'page'
  status?: 'draft' | 'published' | 'archived'
  search?: string
}

export class ContentClient {
  private basePath = '/api/content'

  /**
   * Get all content items with filtering and pagination
   */
  async list(params?: ContentListParams): Promise<PaginatedResponse<Content>> {
    return apiClient.get<PaginatedResponse<Content>>(this.basePath, {
      params: params as unknown as Record<string, string | number | boolean>,
    })
  }

  /**
   * Get a single content item by ID
   */
  async get(contentId: string): Promise<Content> {
    return apiClient.get<Content>(`${this.basePath}/${contentId}`)
  }

  /**
   * Get a content item by slug
   */
  async getBySlug(slug: string): Promise<Content> {
    return apiClient.get<Content>(`${this.basePath}/slug/${slug}`)
  }

  /**
   * Create new content
   */
  async create(data: CreateContentData): Promise<Content> {
    return apiClient.post<Content>(this.basePath, data)
  }

  /**
   * Update existing content
   */
  async update(contentId: string, data: UpdateContentData): Promise<Content> {
    return apiClient.patch<Content>(`${this.basePath}/${contentId}`, data)
  }

  /**
   * Delete content
   */
  async delete(contentId: string): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${contentId}`)
  }

  /**
   * Publish a draft
   */
  async publish(contentId: string): Promise<Content> {
    return apiClient.post<Content>(`${this.basePath}/${contentId}/publish`)
  }

  /**
   * Archive content
   */
  async archive(contentId: string): Promise<Content> {
    return apiClient.patch<Content>(`${this.basePath}/${contentId}`, {
      status: 'archived',
    })
  }

  /**
   * Get content by type (blog, service, case study)
   */
  async getByType(
    contentType: 'blog' | 'service' | 'case-study' | 'page',
    params?: PaginationParams
  ): Promise<PaginatedResponse<Content>> {
    return this.list({ ...params, content_type: contentType })
  }

  /**
   * Start autonomous content creation pipeline
   */
  async createAutonomous(data: AutonomousContentRequest): Promise<{ status: string; workflow_id: string }> {
    return apiClient.post(`${this.basePath}/create`, data)
  }

  /**
   * Approve a content phase (HITL)
   */
  async approvePhase(data: ApprovalActionRequest): Promise<void> {
    return apiClient.post(`${this.basePath}/approve`, data)
  }

  /**
   * Request revision for a content phase (HITL)
   */
  async rejectPhase(data: ApprovalActionRequest): Promise<void> {
    return apiClient.post(`${this.basePath}/reject`, data)
  }

  /**
   * Get status of an autonomous content workflow
   */
  async getStatus(workflowId: string): Promise<ContentWorkflowStatus> {
    return apiClient.get(`${this.basePath}/status/${workflowId}`)
  }
}

export const contentClient = new ContentClient()
