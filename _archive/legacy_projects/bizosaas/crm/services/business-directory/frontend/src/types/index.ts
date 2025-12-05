// API Response Types
export interface APIResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

// Directory Platform
export interface DirectoryPlatform {
  name: string;
  category: string;
  priority: string;
  auto_submit?: boolean;
  industries?: string[];
  description?: string;
  website?: string;
}

// Business Category
export interface BusinessCategory {
  id: string;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  business_count?: number;
  subcategories?: BusinessCategory[];
}

// Business Listing
export interface BusinessListing {
  business_id: string;
  name: string;
  category: string;
  address: string;
  phone: string;
  email: string;
  website: string;
  description: string;
  features: string[];
  rating: number;
  review_count: number;
  verification_status: string;
  premium_status: string;
  ai_enhanced: boolean;
  location?: {
    city: string;
    state: string;
    country: string;
    coordinates?: {
      lat: number;
      lng: number;
    };
  };
  images?: string[];
  hours?: BusinessHours;
  social_links?: SocialLinks;
  tags?: string[];
}

// Business Hours
export interface BusinessHours {
  monday?: string;
  tuesday?: string;
  wednesday?: string;
  thursday?: string;
  friday?: string;
  saturday?: string;
  sunday?: string;
}

// Social Links
export interface SocialLinks {
  facebook?: string;
  twitter?: string;
  instagram?: string;
  linkedin?: string;
  youtube?: string;
}

// Event
export interface BusinessEvent {
  id: string;
  title: string;
  description: string;
  date: string;
  time: string;
  location: string;
  business_id?: string;
  business_name?: string;
  category: string;
  image?: string;
  price?: number;
  tickets_available?: number;
  registration_url?: string;
}

// Product
export interface FeaturedProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  business_id: string;
  business_name: string;
  category: string;
  image?: string;
  rating?: number;
  review_count?: number;
  availability: string;
  features?: string[];
  website_url?: string;
}

// Coupon
export interface Coupon {
  id: string;
  title: string;
  description: string;
  discount_type: 'percentage' | 'fixed' | 'bogo';
  discount_value: number;
  business_id: string;
  business_name: string;
  category: string;
  expiry_date: string;
  terms_conditions?: string;
  coupon_code?: string;
  image?: string;
  min_purchase?: number;
  max_discount?: number;
}

// Blog Post
export interface BlogPost {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  author: string;
  published_date: string;
  category: string;
  tags: string[];
  featured_image?: string;
  read_time?: number;
  views?: number;
}

// Community Activity
export interface CommunityActivity {
  id: string;
  type: 'review' | 'question' | 'recommendation' | 'photo';
  user_name: string;
  user_avatar?: string;
  content: string;
  timestamp: string;
  business_id?: string;
  business_name?: string;
  rating?: number;
  likes?: number;
  replies?: number;
  images?: string[];
}

// Search Filters
export interface SearchFilters {
  query?: string;
  category?: string;
  city?: string;
  rating_min?: number;
  price_range?: string;
  verification_status?: string;
  premium_only?: boolean;
  open_now?: boolean;
  features?: string[];
  sort_by?: 'relevance' | 'rating' | 'distance' | 'name';
  limit?: number;
  offset?: number;
}

// Search Results
export interface SearchResults {
  businesses: BusinessListing[];
  total_count: number;
  page: number;
  per_page: number;
  filters_applied: SearchFilters;
  suggested_categories?: string[];
  suggested_locations?: string[];
}

// API Status
export interface APIStatus {
  status: string;
  timestamp: string;
  version: string;
  services: {
    database: string;
    cache: string;
    search: string;
    ai_agents: string;
  };
  metrics: {
    total_businesses: number;
    total_categories: number;
    total_events: number;
    total_products: number;
    total_coupons: number;
  };
}

// Form Types
export interface ContactForm {
  name: string;
  email: string;
  phone?: string;
  message: string;
  business_id?: string;
}

export interface ReviewForm {
  business_id: string;
  rating: number;
  title: string;
  content: string;
  reviewer_name: string;
  reviewer_email: string;
}

export interface BusinessClaimForm {
  business_id: string;
  owner_name: string;
  owner_email: string;
  owner_phone: string;
  verification_documents?: File[];
  additional_info?: string;
}

// UI State Types
export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message: string;
  details?: string;
}

export interface PaginationState {
  current_page: number;
  total_pages: number;
  per_page: number;
  total_items: number;
}

// Component Props Types
export interface BusinessCardProps {
  business: BusinessListing;
  showFullDetails?: boolean;
  showActions?: boolean;
  className?: string;
}

export interface SearchBarProps {
  onSearch: (query: string, filters: SearchFilters) => void;
  initialQuery?: string;
  placeholder?: string;
  showFilters?: boolean;
}

export interface CategoryGridProps {
  categories: BusinessCategory[];
  onCategorySelect: (category: string) => void;
  showCount?: boolean;
  columns?: number;
}