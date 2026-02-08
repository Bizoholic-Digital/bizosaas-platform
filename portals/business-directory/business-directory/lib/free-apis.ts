// Free Business APIs Integration
// Utilities for fetching business data from free public APIs

export interface BusinessAPIResult {
  source: string;
  businesses: any[];
  error?: string;
}

// Google Places API (requires API key)
export async function fetchFromGooglePlaces(query: string, location?: string): Promise<BusinessAPIResult> {
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_PLACES_API_KEY;

  if (!apiKey) {
    return {
      source: 'Google Places',
      businesses: [],
      error: 'API key not configured',
    };
  }

  try {
    // Note: This is a simplified example. In production, you'd use the full Google Places API
    const searchQuery = location ? `${query} in ${location}` : query;
    const response = await fetch(
      `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${encodeURIComponent(searchQuery)}&key=${apiKey}`
    );

    const data = await response.json();

    return {
      source: 'Google Places',
      businesses: data.results || [],
    };
  } catch (error) {
    return {
      source: 'Google Places',
      businesses: [],
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

// Yelp Fusion API (requires API key)
export async function fetchFromYelp(query: string, location?: string): Promise<BusinessAPIResult> {
  const apiKey = process.env.YELP_API_KEY;

  if (!apiKey) {
    return {
      source: 'Yelp',
      businesses: [],
      error: 'API key not configured',
    };
  }

  try {
    const params = new URLSearchParams();
    params.append('term', query);
    if (location) params.append('location', location);
    params.append('limit', '20');

    const response = await fetch(
      `https://api.yelp.com/v3/businesses/search?${params.toString()}`,
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
        },
      }
    );

    const data = await response.json();

    return {
      source: 'Yelp',
      businesses: data.businesses || [],
    };
  } catch (error) {
    return {
      source: 'Yelp',
      businesses: [],
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

// Mock/Sample business data for development
export function getMockBusinesses(count: number = 10): BusinessAPIResult {
  const mockBusinesses = Array.from({ length: count }, (_, i) => ({
    id: `mock-${i + 1}`,
    name: `Sample Business ${i + 1}`,
    description: `This is a sample business description for business ${i + 1}`,
    category: ['Restaurant', 'Retail', 'Services', 'Healthcare'][i % 4],
    rating: 3 + Math.random() * 2,
    reviewCount: Math.floor(Math.random() * 500),
    location: {
      address: `${100 + i} Main Street`,
      city: 'Sample City',
      state: 'CA',
      zip: '90210',
      coordinates: { lat: 34.05 + Math.random() * 0.1, lng: -118.25 + Math.random() * 0.1 },
    },
    contact: {
      phone: `(555) ${String(i).padStart(3, '0')}-${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
      website: `https://example-${i + 1}.com`,
    },
    pricing: {
      range: ['$', '$$', '$$$', '$$$$'][i % 4],
      currency: 'USD',
    },
  }));

  return {
    source: 'Mock Data',
    businesses: mockBusinesses,
  };
}

// Aggregate results from multiple free APIs
export const freeBusinessAPIs = {
  searchAll: async (query: string, location?: string): Promise<BusinessAPIResult[]> => {
    const results = await Promise.allSettled([
      fetchFromGooglePlaces(query, location),
      fetchFromYelp(query, location),
    ]);

    const apiResults: BusinessAPIResult[] = results
      .filter((result) => result.status === 'fulfilled')
      .map((result) => (result as PromiseFulfilledResult<BusinessAPIResult>).value);

    // Add mock data in development
    if (process.env.NODE_ENV === 'development') {
      apiResults.push(getMockBusinesses(5));
    }

    return apiResults;
  },

  googlePlaces: fetchFromGooglePlaces,
  yelp: fetchFromYelp,
  mock: getMockBusinesses,
};
