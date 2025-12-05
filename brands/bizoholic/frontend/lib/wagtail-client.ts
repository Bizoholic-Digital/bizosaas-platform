/**
 * Wagtail CMS Client for Bizoholic
 * Handles all content fetching from Wagtail API
 */

const WAGTAIL_API_URL = process.env.NEXT_PUBLIC_WAGTAIL_URL || 'http://localhost:8002'

export interface WagtailPage {
  id: number
  meta: {
    type: string
    detail_url: string
    html_url: string
    slug: string
    first_published_at: string
  }
  title: string
  [key: string]: any
}

export interface WagtailListResponse {
  meta: {
    total_count: number
  }
  items: WagtailPage[]
}

/**
 * Fetch homepage content from Wagtail
 */
export async function getHomePage(): Promise<WagtailPage | null> {
  try {
    const response = await fetch(
      `${WAGTAIL_API_URL}/api/v2/pages/?type=cms.BizoholicHomePage&fields=*`,
      { next: { revalidate: 60 } } // Cache for 60 seconds
    )
    
    if (!response.ok) {
      console.error('Wagtail API error:', response.status, response.statusText)
      return null
    }
    
    const data: WagtailListResponse = await response.json()
    return data.items[0] || null
  } catch (error) {
    console.error('Failed to fetch homepage from Wagtail:', error)
    return null
  }
}

/**
 * Fetch all service pages from Wagtail
 */
export async function getServices(): Promise<WagtailPage[]> {
  try {
    const response = await fetch(
      `${WAGTAIL_API_URL}/api/v2/pages/?type=cms.ServicePage&fields=*&order=-featured,order`,
      { next: { revalidate: 300 } } // Cache for 5 minutes
    )
    
    if (!response.ok) {
      console.error('Wagtail API error:', response.status, response.statusText)
      return []
    }
    
    const data: WagtailListResponse = await response.json()
    return data.items
  } catch (error) {
    console.error('Failed to fetch services from Wagtail:', error)
    return []
  }
}

/**
 * Wagtail Client - consolidated API
 */
export const wagtailClient = {
  getHomePage,
  getServices,
}
