// Shared types for multi-tenant architecture
export interface TenantConfig {
  id: string;
  name: string;
  slug: string;
  domain: string;
  theme: TenantTheme;
  branding: TenantBranding;
  features: string[];
  apiEndpoints: TenantApiEndpoints;
}

export interface TenantTheme {
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  backgroundColor: string;
  textColor: string;
  brandGradient: string;
  darkMode: boolean;
  customCSS?: string;
}

export interface TenantBranding {
  logo: string;
  favicon: string;
  companyName: string;
  tagline: string;
  description: string;
  socialLinks: {
    website?: string;
    linkedin?: string;
    twitter?: string;
    facebook?: string;
    instagram?: string;
  };
}

export interface TenantApiEndpoints {
  brain: string;
  auth: string;
  cms: string;
  analytics: string;
  webhooks: string;
}

export type TenantType = 'bizoholic' | 'coreldove' | 'bizosaas' | 'thrillring' | 'quanttrade';

export interface DashboardConfig {
  tenant: TenantType;
  layout: 'sidebar' | 'topbar' | 'hybrid';
  navigation: NavigationItem[];
  widgets: WidgetConfig[];
  permissions: string[];
}

export interface NavigationItem {
  id: string;
  label: string;
  icon?: string;
  href?: string;
  children?: NavigationItem[];
  requiredPermission?: string;
  tenantSpecific?: boolean;
}

export interface WidgetConfig {
  id: string;
  component: string;
  title: string;
  size: 'sm' | 'md' | 'lg' | 'xl';
  position: { x: number; y: number };
  data?: any;
  tenantSpecific?: boolean;
}

// Platform-specific configurations
export const TENANT_CONFIGS: Record<TenantType, TenantConfig> = {
  bizoholic: {
    id: 'bizoholic',
    name: 'Bizoholic',
    slug: 'bizoholic',
    domain: 'bizoholic.com',
    theme: {
      primaryColor: '#2563EB', // Blue (from "Bizoholic")
      secondaryColor: '#10B981', // Teal/Green (from "Digital")
      accentColor: '#059669',
      backgroundColor: '#FFFFFF',
      textColor: '#1F2937',
      brandGradient: 'from-blue-600 to-emerald-500',
      darkMode: false
    },
    branding: {
      logo: '/logos/bizoholic-logo.png',
      favicon: '/favicons/bizoholic-favicon.ico',
      companyName: 'Bizoholic',
      tagline: 'AI-Powered Marketing Solutions',
      description: 'Transform your marketing with AI-driven campaigns and automation',
      socialLinks: {}
    },
    features: ['marketing', 'campaigns', 'analytics', 'crm', 'ai-agents'],
    apiEndpoints: {
      brain: 'http://localhost:8001',
      auth: 'http://localhost:8001/auth',
      cms: 'http://localhost:8006',
      analytics: 'http://localhost:8001/analytics',
      webhooks: 'http://localhost:8001/webhooks'
    }
  },
  coreldove: {
    id: 'coreldove',
    name: 'CoreLDove',
    slug: 'coreldove',
    domain: 'coreldove.com',
    theme: {
      primaryColor: '#EF4444', // Coral/Red (from "Corel")
      secondaryColor: '#3B82F6', // Blue (from "Dove")
      accentColor: '#DC2626',
      backgroundColor: '#FFFFFF',
      textColor: '#1F2937',
      brandGradient: 'from-red-500 to-blue-500',
      darkMode: false
    },
    branding: {
      logo: '/logos/coreldove-logo.png',
      favicon: '/favicons/coreldove-favicon.ico',
      companyName: 'CoreLDove',
      tagline: 'Smart E-commerce Solutions',
      description: 'AI-powered e-commerce platform with intelligent sourcing and inventory management',
      socialLinks: {}
    },
    features: ['ecommerce', 'inventory', 'sourcing', 'analytics', 'ai-agents', 'storefront'],
    apiEndpoints: {
      brain: 'http://localhost:8001',
      auth: 'http://localhost:8001/auth',
      cms: 'http://localhost:8006',
      analytics: 'http://localhost:8001/analytics',
      webhooks: 'http://localhost:8001/webhooks'
    }
  },
  bizosaas: {
    id: 'bizosaas',
    name: 'BizOSaaS',
    slug: 'bizosaas',
    domain: 'app.bizoholic.com',
    theme: {
      primaryColor: '#8B5CF6', // Violet
      secondaryColor: '#7C3AED',
      accentColor: '#F59E0B',
      backgroundColor: '#FFFFFF',
      textColor: '#1F2937',
      brandGradient: 'from-violet-600 to-purple-600',
      darkMode: false
    },
    branding: {
      logo: '/logos/bizosaas-logo.png',
      favicon: '/favicons/bizosaas-favicon.ico',
      companyName: 'BizOSaaS',
      tagline: 'Multi-Tenant Business Platform',
      description: 'Comprehensive SaaS platform for managing multiple business operations',
      socialLinks: {}
    },
    features: ['super-admin', 'multi-tenant', 'analytics', 'integrations', 'ai-agents', 'workflows'],
    apiEndpoints: {
      brain: 'http://localhost:8001',
      auth: 'http://localhost:8001/auth',
      cms: 'http://localhost:8006',
      analytics: 'http://localhost:8001/analytics',
      webhooks: 'http://localhost:8001/webhooks'
    }
  },
  thrillring: {
    id: 'thrillring',
    name: 'ThrillRing',
    slug: 'thrillring',
    domain: 'thrillring.com',
    theme: {
      primaryColor: '#EF4444', // Red
      secondaryColor: '#DC2626',
      accentColor: '#F59E0B',
      backgroundColor: '#FFFFFF',
      textColor: '#1F2937',
      brandGradient: 'from-red-500 to-pink-600',
      darkMode: false
    },
    branding: {
      logo: '/logos/thrillring-logo.png',
      favicon: '/favicons/thrillring-favicon.ico',
      companyName: 'ThrillRing',
      tagline: 'Entertainment & Events Platform',
      description: 'Exciting entertainment and event management solutions',
      socialLinks: {}
    },
    features: ['events', 'entertainment', 'booking', 'analytics'],
    apiEndpoints: {
      brain: 'http://localhost:8001',
      auth: 'http://localhost:8001/auth',
      cms: 'http://localhost:8006',
      analytics: 'http://localhost:8001/analytics',
      webhooks: 'http://localhost:8001/webhooks'
    }
  },
  quanttrade: {
    id: 'quanttrade',
    name: 'QuantTrade',
    slug: 'quanttrade',
    domain: 'quanttrade.com',
    theme: {
      primaryColor: '#F59E0B', // Amber
      secondaryColor: '#D97706',
      accentColor: '#3B82F6',
      backgroundColor: '#FFFFFF',
      textColor: '#1F2937',
      brandGradient: 'from-amber-500 to-orange-600',
      darkMode: false
    },
    branding: {
      logo: '/logos/quanttrade-logo.png',
      favicon: '/favicons/quanttrade-favicon.ico',
      companyName: 'QuantTrade',
      tagline: 'Quantitative Trading Platform',
      description: 'Advanced algorithmic trading and financial analytics',
      socialLinks: {}
    },
    features: ['trading', 'analytics', 'algorithms', 'portfolio'],
    apiEndpoints: {
      brain: 'http://localhost:8001',
      auth: 'http://localhost:8001/auth',
      cms: 'http://localhost:8006',
      analytics: 'http://localhost:8001/analytics',
      webhooks: 'http://localhost:8001/webhooks'
    }
  }
};