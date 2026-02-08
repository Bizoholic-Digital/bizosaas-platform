/**
 * Projects API Client
 * Handles all project-related API operations
 */

import { apiClient } from '../utils/base-client'
import type {
  Project,
  CreateProjectData,
  UpdateProjectData,
  PaginatedResponse,
  PaginationParams,
} from '../types'

export class ProjectsClient {
  private basePath = '/api/projects'

  /**
   * Get all projects with pagination
   */
  async list(params?: PaginationParams): Promise<PaginatedResponse<Project>> {
    return apiClient.get<PaginatedResponse<Project>>(this.basePath, {
      params: params as unknown as Record<string, string | number | boolean>,
    })
  }

  /**
   * Get a single project by ID
   */
  async get(projectId: string): Promise<Project> {
    return apiClient.get<Project>(`${this.basePath}/${projectId}`)
  }

  /**
   * Create a new project
   */
  async create(data: CreateProjectData): Promise<Project> {
    return apiClient.post<Project>(this.basePath, data)
  }

  /**
   * Update an existing project
   */
  async update(projectId: string, data: UpdateProjectData): Promise<Project> {
    return apiClient.patch<Project>(`${this.basePath}/${projectId}`, data)
  }

  /**
   * Delete a project
   */
  async delete(projectId: string): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${projectId}`)
  }

  /**
   * Archive a project (soft delete)
   */
  async archive(projectId: string): Promise<Project> {
    return apiClient.patch<Project>(`${this.basePath}/${projectId}`, {
      status: 'archived',
    })
  }

  /**
   * Get project statistics
   */
  async getStats(projectId: string): Promise<Record<string, number>> {
    return apiClient.get<Record<string, number>>(
      `${this.basePath}/${projectId}/stats`
    )
  }
}

export const projectsClient = new ProjectsClient()
