/**
 * CMS API Module
 *
 * Handles all CMS-related API calls to Wagtail CMS via brain-gateway
 */

import { apiClient } from './client'

export const cmsApi = {
  /**
   * Fetch a CMS page by slug
   */
  getPage: async (slug: string) => {
    return apiClient.get(`/api/cms/pages/${slug}`)
  },

  /**
   * Get homepage content
   */
  getHomepage: async () => {
    return apiClient.get('/api/cms/pages/home')
  },

  /**
   * Get blog posts
   */
  getBlogPosts: async (limit = 10, offset = 0) => {
    return apiClient.get('/api/cms/blog', {
      headers: {
        'X-Pagination-Limit': limit.toString(),
        'X-Pagination-Offset': offset.toString()
      }
    })
  },

  /**
   * Search CMS content
   */
  search: async (query: string) => {
    return apiClient.get('/api/cms/search', {
      headers: {
        'X-Search-Query': query
      }
    })
  },

  /**
   * Get menu items
   */
  getMenu: async (menuSlug: string) => {
    return apiClient.get(`/api/cms/menus/${menuSlug}`)
  }
}
