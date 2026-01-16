import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merges Tailwind CSS classes with clsx and tailwind-merge
 */
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

/**
 * Formats a numeric rating to 1 decimal place
 */
export function formatRating(rating: number): string {
    if (typeof rating !== 'number') return '0.0';
    return rating.toFixed(1)
}

/**
 * Formats a phone number string to (XXX) XXX-XXXX
 */
export function formatPhoneNumber(phone: string): string {
    if (!phone) return '';
    const cleaned = ('' + phone).replace(/\D/g, '')
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3]
    }
    return phone
}

/**
 * Checks if a business is currently open based on its hours object
 */
export function isBusinessOpen(hours: any): boolean {
    if (!hours) return false

    const now = new Date()
    // Adjust day to match the business hours object keys (lowercase)
    const day = now.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase()
    const currentHours = hours[day]

    if (!currentHours || currentHours.closed) return false

    try {
        const [nowH, nowM] = [now.getHours(), now.getMinutes()]
        const nowVal = nowH * 100 + nowM

        const [openH, openM] = currentHours.open.split(':').map(Number)
        const openVal = openH * 100 + openM

        const [closeH, closeM] = currentHours.close.split(':').map(Number)
        const closeVal = closeH * 100 + closeM

        // Handle cases where the business closes after midnight
        if (closeVal < openVal) {
            return nowVal >= openVal || nowVal <= closeVal
        }

        return nowVal >= openVal && nowVal <= closeVal
    } catch (e) {
        console.error('Error calculating business open status:', e)
        return false
    }
}

/**
 * Generates an array of star states for UI rendering
 */
export function generateStars(rating: number) {
    const stars = []
    const roundedRating = Math.round(rating)
    for (let i = 1; i <= 5; i++) {
        stars.push({
            filled: i <= roundedRating
        })
    }
    return stars
}
