// CoreLDove Brand Configuration
// Minimalistic, Elegant, Conversion-Optimized Brand System

export const brand = {
  name: 'CoreLDove',
  tagline: 'AI-Curated Premium Products',
  description: 'Discover the finest products through our AI-powered curation platform',
  
  // Brand Colors - CoreLDove Official Palette
  colors: {
    primary: {
      50: '#fff5f5',
      100: '#fed7d7', 
      200: '#feb2b2',
      300: '#fc8181',
      400: '#f56565',
      500: '#ff6b6b', // CoreLDove Coral Red
      600: '#e53e3e',
      700: '#c53030',
      800: '#9b2c2c',
      900: '#742a2a',
    },
    secondary: {
      50: '#e6f7ff',
      100: '#bae7ff',
      200: '#91d5ff',
      300: '#69c0ff', 
      400: '#40a9ff',
      500: '#4fc3f7', // CoreLDove Blue
      600: '#1890ff',
      700: '#096dd9',
      800: '#0050b3',
      900: '#003a8c',
    },
    neutral: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb', 
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827',
    },
    success: '#10b981',
    warning: '#f59e0b', 
    error: '#ef4444',
    info: '#3b82f6'
  },

  // Typography System
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace']
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem'
    }
  },

  // Logo Configuration - Using Actual CoreLDove Assets
  logo: {
    primary: '/images/Coreldove-Simple.png',
    monochrome: '/images/Coreldove-Simple-black-white.png',
    favicon: '/coreldove_favicon.png',
    svg: '/images/coreldove-logo.svg',
    svgWhite: '/images/coreldove-logo-white.svg'
  },

  // Conversion Optimization Settings
  conversion: {
    // Trust Indicators
    trustBadges: [
      { text: 'Free Shipping $50+', icon: 'truck' },
      { text: '30-Day Returns', icon: 'refresh' },
      { text: 'Secure Checkout', icon: 'shield' },
      { text: '5-Star Service', icon: 'award' }
    ],

    // Social Proof
    socialProof: {
      customerCount: '50,000+',
      reviewCount: '12,847',
      averageRating: 4.9,
      trustpilotScore: 4.8
    },

    // Urgency Indicators
    urgencyMessages: [
      'Only {count} left in stock',
      'Limited time offer',
      '{count} people viewing this',
      'Hot seller - order soon',
      'Back in stock - limited quantity'
    ],

    // Conversion Copy
    headlines: {
      primary: 'Discover Premium Products',
      secondary: 'AI-Curated Selection for Modern Living',
      value: 'Best Prices Guaranteed'
    }
  },

  // Animation Settings
  animations: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms'
    },
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      smooth: 'cubic-bezier(0.25, 0.1, 0.25, 1)'
    }
  },

  // Spacing System
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem', 
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem'
  },

  // Border Radius
  borderRadius: {
    sm: '0.375rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    full: '9999px'
  },

  // Shadows
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
  },

  // Component Defaults
  components: {
    button: {
      primary: {
        bg: 'bg-blue-600',
        text: 'text-white',
        hover: 'hover:bg-blue-700',
        focus: 'focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
      },
      secondary: {
        bg: 'bg-white',
        text: 'text-gray-700', 
        border: 'border border-gray-300',
        hover: 'hover:bg-gray-50'
      }
    },
    card: {
      bg: 'bg-white',
      border: 'border border-gray-200',
      shadow: 'shadow-sm',
      hover: 'hover:shadow-md'
    }
  }
}

// Conversion Rate Optimization Configuration
export const cro = {
  // A/B Testing Variants
  variants: {
    primaryCTA: ['Shop Now', 'Discover Products', 'Browse Collection'],
    headlines: [
      'Premium Products, AI-Curated',
      'Discover Your Perfect Product',
      'Quality Products, Unbeatable Prices'
    ],
    urgency: ['limited', 'popular', 'trending', 'bestseller']
  },

  // Conversion Tracking Events
  events: {
    pageView: 'page_view',
    productView: 'product_view',
    addToCart: 'add_to_cart',
    beginCheckout: 'begin_checkout',
    purchase: 'purchase',
    signUp: 'sign_up',
    search: 'search'
  },

  // Performance Thresholds
  performance: {
    pageLoadTime: 2000, // 2 seconds
    lcp: 2.5, // Largest Contentful Paint
    fid: 100, // First Input Delay (ms)
    cls: 0.1  // Cumulative Layout Shift
  }
}

export default brand