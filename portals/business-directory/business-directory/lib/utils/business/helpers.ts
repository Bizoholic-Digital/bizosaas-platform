/**
 * Business-specific utility functions for the Business Directory
 */

/**
 * Check if a business is currently open based on hours
 * @param hours - Business hours object with day keys and time values
 * @returns Boolean indicating if business is open
 */
export function isBusinessOpen(hours: Record<string, string> | null | undefined): boolean {
  if (!hours) return false

  const now = new Date()
  const dayNames = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
  const currentDay = dayNames[now.getDay()]
  const currentTime = now.getHours() * 60 + now.getMinutes()

  const todayHours = hours[currentDay]
  if (!todayHours || todayHours.toLowerCase() === 'closed') return false

  // Parse hours like "9:00 AM - 5:00 PM"
  const match = todayHours.match(/(\d{1,2}):(\d{2})\s*(AM|PM)\s*-\s*(\d{1,2}):(\d{2})\s*(AM|PM)/)
  if (!match) return false

  const [, openHour, openMin, openPeriod, closeHour, closeMin, closePeriod] = match

  const openTime =
    (parseInt(openHour) % 12 + (openPeriod === 'PM' ? 12 : 0)) * 60 + parseInt(openMin)
  const closeTime =
    (parseInt(closeHour) % 12 + (closePeriod === 'PM' ? 12 : 0)) * 60 + parseInt(closeMin)

  return currentTime >= openTime && currentTime <= closeTime
}

/**
 * Generate star rating array for rendering
 * @param rating - Numeric rating (0-5)
 * @returns Array of 5 booleans indicating filled/empty stars
 */
export function generateStars(rating: number): boolean[] {
  const stars: boolean[] = []
  const fullStars = Math.floor(rating)
  const hasHalfStar = rating % 1 >= 0.5

  for (let i = 0; i < 5; i++) {
    if (i < fullStars) {
      stars.push(true)
    } else if (i === fullStars && hasHalfStar) {
      stars.push(true) // Half star represented as true
    } else {
      stars.push(false)
    }
  }

  return stars
}

/**
 * Format rating number for display
 * @param rating - Numeric rating
 * @param reviewCount - Optional number of reviews
 * @returns Formatted string like "4.5" or "4.5 (123)"
 */
export function formatRating(rating: number, reviewCount?: number): string {
  const formattedRating = rating.toFixed(1)
  if (reviewCount !== undefined) {
    return `${formattedRating} (${reviewCount.toLocaleString()})`
  }
  return formattedRating
}

/**
 * Format phone number to standard US format
 * @param phone - Phone number string (digits only or with formatting)
 * @returns Formatted phone like "(555) 123-4567"
 */
export function formatPhoneNumber(phone: string): string {
  // Remove all non-digit characters
  const digits = phone.replace(/\D/g, '')

  // Handle different length inputs
  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`
  } else if (digits.length === 11 && digits[0] === '1') {
    return `+1 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`
  }

  // Return original if format not recognized
  return phone
}

/**
 * Calculate distance between two coordinates (Haversine formula)
 * @param lat1 - Latitude of first point
 * @param lon1 - Longitude of first point
 * @param lat2 - Latitude of second point
 * @param lon2 - Longitude of second point
 * @returns Distance in miles
 */
export function calculateDistance(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number
): number {
  const R = 3959 // Earth's radius in miles
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

function toRad(degrees: number): number {
  return (degrees * Math.PI) / 180
}

/**
 * Format distance for display
 * @param miles - Distance in miles
 * @returns Formatted string like "1.5 mi" or "0.3 mi"
 */
export function formatDistance(miles: number): string {
  return `${miles.toFixed(1)} mi`
}
