/**
 * Transforms business data from backend format to frontend format.
 * Specifically handles the transformation of business hours.
 */

export function transformBusinessData(b: any) {
    if (!b) return null;

    // Map backend snake_case fields to frontend camelCase fields
    const business = {
        id: b.id,
        name: b.business_name || b.name, // Handle both backend and potential Google data
        slug: b.business_slug || b.slug,
        description: b.description || "",
        category: typeof b.category === 'string'
            ? { id: b.category, name: b.category, slug: b.category.toLowerCase().replace(/ /g, '-') }
            : b.category || { id: 'unknown', name: 'General', slug: 'general' },
        rating: b.google_rating || b.rating || 0,
        reviewCount: b.google_reviews_count || b.reviewCount || 0,
        contact: {
            phone: b.phone || (b.contact?.phone) || "",
            email: b.email || (b.contact?.email) || "",
            website: b.website || (b.contact?.website) || "",
        },
        location: {
            address: b.address || (b.location?.address) || "",
            city: b.city || (b.location?.city) || "",
            state: b.state || (b.location?.state) || "",
            zipCode: b.postal_code || (b.location?.zipCode) || "",
            country: b.country || (b.location?.country) || "",
            coordinates: b.coordinates || { lat: 0, lng: 0 }
        },
        hours: b.hours_of_operation || b.hours || null,
        featured: !!b.featured,
        verified: b.verification_status === 'verified' || !!b.verified,
        claimStatus: b.claimed ? 'claimed' : 'unclaimed',
        tags: b.tags || [],
        images: (b.google_photos && Array.isArray(b.google_photos)) ? b.google_photos : (b.images || []),
        pricing: b.pricing_info || b.pricing || { range: '$$', currency: 'USD', description: '' },
    };

    return business;
}

export function transformBusinessList(businesses: any[]) {
    if (!Array.isArray(businesses)) return [];
    return businesses.map(transformBusinessData);
}

/**
 * Helper function to convert 12-hour time (e.g., "9:00 AM") to 24-hour time (e.g., "09:00")
 */
export function convertTo24Hour(timeStr: string): string {
    if (!timeStr) return '';

    const [time, period] = timeStr.trim().split(' ');
    let [hours, minutes] = time.split(':').map(Number);

    if (period === 'PM' && hours !== 12) hours += 12;
    if (period === 'AM' && hours === 12) hours = 0;

    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

/**
 * Normalizes business hours from various possible backend formats
 */
export function normalizeHours(hours: any) {
    if (!hours) return null;

    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    const result: any = {};

    days.forEach(day => {
        const dayData = hours[day];
        if (!dayData) {
            result[day] = { open: '', close: '', closed: true };
        } else if (typeof dayData === 'string') {
            if (dayData.toLowerCase() === 'closed') {
                result[day] = { open: '', close: '', closed: true };
            } else {
                const parts = dayData.split(' - ');
                if (parts.length === 2) {
                    result[day] = {
                        open: convertTo24Hour(parts[0]),
                        close: convertTo24Hour(parts[1]),
                        closed: false
                    };
                } else {
                    result[day] = { open: '', close: '', closed: true };
                }
            }
        } else {
            result[day] = {
                open: dayData.open || '',
                close: dayData.close || '',
                closed: !!dayData.closed
            };
        }
    });

    return result;
}
