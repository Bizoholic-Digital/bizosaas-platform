/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker optimization
  output: 'standalone',

  // Set workspace root to silence warning about multiple lockfiles
  outputFileTracingRoot: require('path').join(__dirname, '../../..'),

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

  // External packages for server components (moved from experimental in Next.js 15)
  serverExternalPackages: ['axios'],

  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons'],
  },

  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
      },
      {
        protocol: 'https',
        hostname: 'bizoholic.com',
      },
      {
        protocol: 'https',
        hostname: 'www.bizoholic.com',
      },
      {
        protocol: 'http',
        hostname: 'bizosaas-wagtail-cms',
      },
      {
        protocol: 'http',
        hostname: 'bizosaas-brain',
      },
      {
        protocol: 'http',
        hostname: 'bizosaas-brain-staging',
      },
    ],
    unoptimized: process.env.NODE_ENV === 'development',
    qualities: [100],
  },

  async rewrites() {
    return [
      // Preserve Bizoholic-specific routing
      {
        source: '/services/:slug*',
        destination: '/services/:slug*',
      },
      {
        source: '/case-studies/:slug*',
        destination: '/case-studies/:slug*',
      },
      {
        source: '/blog/:slug*',
        destination: '/blog/:slug*',
      },
      // API routes to Brain API
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://bizosaas-brain-unified:8000'}/:path*`,
      },
      {
        source: '/api/wagtail/:path*',
        destination: `${process.env.NEXT_PUBLIC_WAGTAIL_URL || 'http://bizosaas-wagtail-unified:8002'}/:path*`,
      },
    ];
  },

  async redirects() {
    return [
      // Redirect all /portal/* routes to Client Portal (localhost:3003)
      {
        source: '/portal/:path*',
        destination: 'http://localhost:3003/:path*',
        permanent: false,
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
            value: 'bizoholic',
          },
          {
            key: 'X-Platform-Type',
            value: 'marketing-website',
          },
          // PWA Security Headers
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
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
      },
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
