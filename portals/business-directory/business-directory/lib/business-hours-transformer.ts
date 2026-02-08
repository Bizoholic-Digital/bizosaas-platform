// Business Hours Transformer
// Utilities for transforming and normalizing business hours data from various API sources

import { Business } from '@/types/business';

export interface RawBusinessHours {
  [key: string]: string | { open: string; close: string }[];
}

export function transformBusinessHours(rawHours: RawBusinessHours): Business['hours'] {
  if (!rawHours) return undefined;

  const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  const normalized: Business['hours'] = {};

  for (const day of daysOfWeek) {
    const dayData = rawHours[day];
    if (!dayData) continue;

    if (typeof dayData === 'string') {
      // Handle simple string format like "9:00 AM - 5:00 PM"
      const [open, close] = dayData.split('-').map(t => t.trim());
      if (open && close) {
        normalized[day] = { open, close, isClosed: false };
      }
    } else if (Array.isArray(dayData) && dayData.length > 0) {
      // Handle array format (multiple time slots)
      const firstSlot = dayData[0];
      normalized[day] = {
        open: firstSlot.open,
        close: firstSlot.close,
        isClosed: false,
      };
    }
  }

  return Object.keys(normalized).length > 0 ? normalized : undefined;
}

export function transformBusinessData(rawBusiness: any): Business {
  return {
    id: rawBusiness.id || rawBusiness._id || '',
    name: rawBusiness.name || '',
    description: rawBusiness.description || rawBusiness.about || '',
    category: rawBusiness.category || rawBusiness.categories?.[0] || '',
    tags: rawBusiness.tags || rawBusiness.categories || [],
    rating: rawBusiness.rating || 0,
    reviewCount: rawBusiness.reviewCount || rawBusiness.review_count || 0,
    verified: rawBusiness.verified || rawBusiness.is_verified || false,
    location: {
      address: rawBusiness.location?.address || rawBusiness.address || '',
      city: rawBusiness.location?.city || rawBusiness.city || '',
      state: rawBusiness.location?.state || rawBusiness.state || '',
      zip: rawBusiness.location?.zip || rawBusiness.zip_code || '',
      coordinates: rawBusiness.location?.coordinates || rawBusiness.coordinates || { lat: 0, lng: 0 },
    },
    contact: {
      phone: rawBusiness.contact?.phone || rawBusiness.phone || '',
      email: rawBusiness.contact?.email || rawBusiness.email || '',
      website: rawBusiness.contact?.website || rawBusiness.website || rawBusiness.url || '',
    },
    hours: transformBusinessHours(rawBusiness.hours || rawBusiness.business_hours || {}),
    pricing: {
      range: rawBusiness.pricing?.range || rawBusiness.price_range || '',
      currency: rawBusiness.pricing?.currency || 'USD',
    },
    images: rawBusiness.images || rawBusiness.photos || [],
    featured: rawBusiness.featured || false,
    amenities: rawBusiness.amenities || [],
    socialMedia: rawBusiness.socialMedia || rawBusiness.social_links || {},
  };
}

export function transformBusinessList(rawBusinesses: any[]): Business[] {
  if (!Array.isArray(rawBusinesses)) {
    return [];
  }

  return rawBusinesses.map(transformBusinessData);
}
