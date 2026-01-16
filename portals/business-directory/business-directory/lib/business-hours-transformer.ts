/**
 * Transforms business data from backend format to frontend format.
 * Specifically handles the transformation of business hours.
 */

export function transformBusinessData(business: any) {
    if (!business) return null;

    // Ensure hours are in the correct format for the frontend
    if (business.hours) {
        if (typeof business.hours === 'object' && !business.hours.monday && !business.hours.tuesday) {
            // It might be in a different format or empty, let's normalize it if possible
            // This is a placeholder for more complex transformation logic if needed
        }
    }

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
