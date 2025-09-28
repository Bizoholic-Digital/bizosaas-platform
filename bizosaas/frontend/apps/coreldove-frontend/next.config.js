/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker optimization
  output: 'standalone',
  
  // Optimize for production
  reactStrictMode: true,
  compress: true,
  poweredByHeader: false,
  
  // PWA Configuration
  env: {
    NEXT_PUBLIC_PWA_ENABLED: 'true',
    NEXT_PUBLIC_SW_URL: '/sw.js',
    NEXT_PUBLIC_MANIFEST_URL: '/manifest.json',
  },
  
  // Move serverComponentsExternalPackages out of experimental
  serverExternalPackages: ['axios'],
  
  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons'],
  },
  
  // Set output file tracing root to silence lockfile warnings
  outputFileTracingRoot: '/home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/coreldove-frontend',
  
  images: {
    domains: [
      'localhost', 
      'coreldove.com', 
      'www.coreldove.com', 
      'bizosaas-saleor-api', 
      'bizosaas-wagtail-cms',
      'images.unsplash.com',
      'm.media-amazon.com',
      'images-na.ssl-images-amazon.com'
    ],
    unoptimized: process.env.NODE_ENV === 'development',
    // Add image optimization settings for SEO and performance
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 160, 256, 384, 500, 1000],
    formats: ['image/webp', 'image/avif'],
    // Enable optimization for external images
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.unsplash.com',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'm.media-amazon.com',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'images-na.ssl-images-amazon.com',
        port: '',
        pathname: '/**',
      }
    ]
  },
  
  async rewrites() {
    return [
      // Preserve Coreldove-specific routing
      {
        source: '/products/:slug*',
        destination: '/products/:slug*',
      },
      {
        source: '/category/:slug*',
        destination: '/category/:slug*',
      },
      {
        source: '/cart',
        destination: '/cart',
      },
      {
        source: '/checkout',
        destination: '/checkout',
      },
      // API routes to Brain API
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://bizosaas-brain:8001'}/:path*`,
      },
      {
        source: '/api/saleor/:path*',
        destination: `${process.env.NEXT_PUBLIC_SALEOR_API_URL || 'http://bizosaas-saleor-api:8000'}/graphql/:path*`,
      },
      {
        source: '/api/auth/:path*',
        destination: `${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://bizosaas-auth-v2:8007'}/:path*`,
      },
    ];
  },
  
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Tenant',
            value: 'coreldove',
          },
          {
            key: 'X-Platform-Type',
            value: 'ecommerce-website',
          },
          // Add SEO and performance headers
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          // PWA Security Headers
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          }
        ],
      },
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,DELETE,PATCH,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization' },
        ],
      },
      // Optimize image loading
      {
        source: '/_next/image',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable'
          }
        ]
      },
      // PWA Manifest and Service Worker Headers
      {
        source: '/manifest.json',
        headers: [
          { key: 'Content-Type', value: 'application/manifest+json' },
          { key: 'Cache-Control', value: 'public, max-age=86400' },
        ],
      },
      {
        source: '/sw.js',
        headers: [
          { key: 'Content-Type', value: 'application/javascript' },
          { key: 'Cache-Control', value: 'no-cache, no-store, must-revalidate' },
          { key: 'Service-Worker-Allowed', value: '/' },
        ],
      },
      // PWA Icon Headers
      {
        source: '/icons/(.*)',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      }
    ];
  },
  
  // Webpack configuration
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;