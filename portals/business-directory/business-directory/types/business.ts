export interface Business {
  id: string;
  name: string;
  slug: string;
  description: string;
  category: Category;
  subcategory?: string;
  contact: ContactInfo;
  location: Location;
  hours?: BusinessHours | null;
  rating: number;
  reviewCount: number;
  images: string[];
  featured: boolean;
  verified: boolean;
  verification_status?: 'verified' | 'unverified' | 'pending';
  status: 'open' | 'closed' | 'temporarily_closed';
  tags: string[];
  socialMedia: SocialMedia;
  pricing: PricingInfo;
  amenities: string[];
  events?: BusinessEvent[];
  products?: BusinessProduct[];
  coupons?: BusinessCoupon[];
  viewCount: number;
  analytics?: {
    views?: number;
    website_clicks?: number;
    phone_clicks?: number;
    direction_clicks?: number;
  };
  claimStatus: 'claimed' | 'unclaimed' | 'pending';
  lastUpdated: string;
  seoMetadata?: {
    metaTitle?: string;
    metaDescription?: string;
    keywords?: string[];
  };
  createdAt: string;
  updatedAt: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  icon: string;
  description: string;
  subcategories: Subcategory[];
  businessCount: number;
}

export interface Subcategory {
  id: string;
  name: string;
  slug: string;
  description: string;
  businessCount: number;
}

export interface ContactInfo {
  phone: string;
  email: string;
  website: string;
}

export interface Location {
  address: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  coordinates: {
    lat: number;
    lng: number;
  };
}

export interface BusinessHours {
  monday: DayHours;
  tuesday: DayHours;
  wednesday: DayHours;
  thursday: DayHours;
  friday: DayHours;
  saturday: DayHours;
  sunday: DayHours;
}

export interface DayHours {
  open: string;
  close: string;
  closed: boolean;
}

export interface SocialMedia {
  facebook?: string;
  twitter?: string;
  instagram?: string;
  linkedin?: string;
  youtube?: string;
}

export interface PricingInfo {
  range: '$' | '$$' | '$$$' | '$$$$';
  currency: string;
  description: string;
}

export interface Review {
  id: string;
  businessId: string;
  authorName: string;
  authorEmail?: string;
  rating: number;
  title: string;
  content: string;
  images: string[];
  helpful: number;
  verified: boolean;
  response?: BusinessResponse;
  createdAt: string;
  updatedAt: string;
}

export interface BusinessResponse {
  content: string;
  authorName: string;
  createdAt: string;
}

export interface SearchFilters {
  query: string;
  category?: string;
  subcategory?: string;
  location?: string;
  latitude?: number;
  longitude?: number;
  rating?: number;
  priceRange?: string[];
  distance?: number;
  openNow?: boolean;
  featured?: boolean;
  verified?: boolean;
  amenities?: string[];
  sortBy?: 'relevance' | 'rating' | 'distance' | 'name' | 'newest';
  sortOrder?: 'asc' | 'desc';
}

export interface SearchResult {
  businesses: Business[];
  total: number;
  page: number;
  limit: number;
  filters: SearchFilters;
  suggestions: string[];
  facets?: {
    categories: { name: string; count: number; slug: string }[];
    priceRanges: { range: string; count: number }[];
    ratings: { rating: number; count: number }[];
    amenities: { amenity: string; count: number }[];
  };
  searchTime?: number;
}

export interface SearchSuggestion {
  id: string;
  text: string;
  type: 'business' | 'category' | 'location' | 'query';
  metadata?: {
    businessId?: string;
    categorySlug?: string;
    coordinates?: { lat: number; lng: number };
  };
}

export interface MapBounds {
  north: number;
  south: number;
  east: number;
  west: number;
}

export interface BusinessEvent {
  id: string;
  businessId: string;
  title: string;
  description: string;
  startDate: string;
  endDate?: string;
  type: 'promotion' | 'event' | 'sale' | 'announcement';
  image?: string;
  url?: string;
}

export interface BusinessProduct {
  id: string;
  businessId: string;
  name: string;
  description: string;
  price?: number;
  currency: string;
  category: string;
  images: string[];
  availability: 'in_stock' | 'out_of_stock' | 'limited';
  features: string[];
}

export interface BusinessCoupon {
  id: string;
  businessId: string;
  title: string;
  description: string;
  discountType: 'percentage' | 'fixed' | 'buy_one_get_one';
  discountValue: number;
  validFrom: string;
  validUntil: string;
  code?: string;
  termsAndConditions: string[];
  usageLimit?: number;
  usedCount: number;
  active: boolean;
}