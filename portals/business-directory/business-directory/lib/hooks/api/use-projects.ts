/**
 * useProjects hook
 * Manages projects data fetching and state
 */

import { useState, useEffect, useCallback } from 'react'

export interface Project {
  id: string
  name: string
  description?: string
  status: 'active' | 'paused' | 'completed' | 'archived'
  tenant_id: string
  created_at: string
  updated_at: string
}

export interface UseProjectsOptions {
  page?: number
  limit?: number
  autoFetch?: boolean
}

export interface UseProjectsResult {
  projects: Project[]
  loading: boolean
  error: Error | null
  total: number
  page: number
  totalPages: number
  refetch: () => Promise<void>
  createProject: (data: { name: string; description?: string }) => Promise<Project>
  updateProject: (id: string, data: Partial<Project>) => Promise<Project>
  deleteProject: (id: string) => Promise<void>
}

export function useProjects(options: UseProjectsOptions = {}): UseProjectsResult {
  const { page = 1, limit = 10, autoFetch = true } = options

  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  const [total, setTotal] = useState(0)
  const [totalPages, setTotalPages] = useState(0)

  const fetchProjects = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL}/api/projects?page=${page}&limit=${limit}`,
        { credentials: 'include' }
      )

      if (!response.ok) {
        throw new Error('Failed to fetch projects')
      }

      const data = await response.json()
      setProjects(data.items)
      setTotal(data.total)
      setTotalPages(data.total_pages)
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'))
    } finally {
      setLoading(false)
    }
  }, [page, limit])

  useEffect(() => {
    if (autoFetch) {
      fetchProjects()
    }
  }, [autoFetch, fetchProjects])

  const createProject = useCallback(async (data: { name: string; description?: string }) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL}/api/projects`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data),
      }
    )

    if (!response.ok) {
      throw new Error('Failed to create project')
    }

    const newProject = await response.json()
    setProjects(prev => [newProject, ...prev])
    return newProject
  }, [])

  const updateProject = useCallback(async (id: string, data: Partial<Project>) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL}/api/projects/${id}`,
      {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data),
      }
    )

    if (!response.ok) {
      throw new Error('Failed to update project')
    }

    const updatedProject = await response.json()
    setProjects(prev => prev.map(p => p.id === id ? updatedProject : p))
    return updatedProject
  }, [])

  const deleteProject = useCallback(async (id: string) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL}/api/projects/${id}`,
      {
        method: 'DELETE',
        credentials: 'include',
      }
    )

    if (!response.ok) {
      throw new Error('Failed to delete project')
    }

    setProjects(prev => prev.filter(p => p.id !== id))
  }, [])

  return {
    projects,
    loading,
    error,
    total,
    page,
    totalPages,
    refetch: fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  }
}
