/**
 * Generate a URL-safe slug from business name and location
 * @param businessName - The name of the business
 * @param location - The location/address of the business
 * @returns A URL-safe slug
 */
export function generateBusinessSlug(businessName: string, location: string): string {
    // Normalize business name
    const normalizedName = businessName
        .toLowerCase()
        .replace(/[^\w\s-]/g, '') // Remove special characters
        .replace(/\s+/g, '-') // Replace spaces with hyphens
        .replace(/-+/g, '-') // Replace multiple hyphens with single
        .trim();

    // Extract city from location (simple heuristic)
    const locationParts = location.split(',').map(p => p.trim());
    const city = locationParts[locationParts.length - 2] || locationParts[0] || '';

    const normalizedCity = city
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim();

    // Combine name and city
    const baseSlug = normalizedCity
        ? `${normalizedName}-${normalizedCity}`
        : normalizedName;

    // Ensure it's not too long (max 100 chars)
    return baseSlug.substring(0, 100).replace(/-$/, '');
}

/**
 * Generate a directory website URL for a business
 * @param businessName - The name of the business
 * @param location - The location/address of the business
 * @param domain - The base domain (default: bizoholic.net)
 * @returns Full directory URL
 */
export function generateDirectoryUrl(
    businessName: string,
    location: string,
    domain: string = 'bizoholic.net'
): string {
    const slug = generateBusinessSlug(businessName, location);
    return `https://directory.${domain}/biz/${slug}`;
}
