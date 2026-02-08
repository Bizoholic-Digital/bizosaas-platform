/**
 * Wagtail CMS Client for Bizoholic
 * Handles all content fetching from Wagtail API
 */

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'https://api.bizoholic.net'

export interface CMSPage {
  id: string
  title: string
  slug: string
  content: string
  status: string
  published_at?: string
}

/**
 * Fetch homepage content from WordPress via Brain Gateway
 */
export async function getHomePage(): Promise<CMSPage | null> {
  try {
    const response = await fetch(
      `${BRAIN_API_URL}/api/cms/pages?slug=home`,
      { next: { revalidate: 60 } }
    )

    if (!response.ok) {
      console.error('Brain CMS error:', response.status, response.statusText)
      return null
    }

    const data: CMSPage[] = await response.json()
    return data[0] || null
  } catch (error) {
    console.error('Failed to fetch homepage from Brain CMS:', error)
    return null
  }
}

/**
 * Fetch all service pages from WordPress via Brain Gateway
 */
export async function getServices(): Promise<CMSPage[]> {
  try {
    // We can use a category filter or just get all pages for now
    const response = await fetch(
      `${BRAIN_API_URL}/api/cms/pages?limit=100`,
      { next: { revalidate: 300 } }
    )

    if (!response.ok) {
      console.error('Brain CMS error:', response.status, response.statusText)
      return []
    }

    const data: CMSPage[] = await response.json()
    // In WordPress we might filter by category if mapped, 
    // for now return all and filter locally or as needed.
    return data
  } catch (error) {
    console.error('Failed to fetch services from Brain CMS:', error)
    return []
  }
}

/**
 * consolidated CMS Client
 */
export const cmsClient = {
  getHomePage,
  getServices,
}

// Keep legacy export
export const wagtailClient = cmsClient;
