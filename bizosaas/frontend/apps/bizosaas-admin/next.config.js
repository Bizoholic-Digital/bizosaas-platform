/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker optimization
  output: 'standalone',
  
  // Skip type checking during build for container optimization
  typescript: {
    ignoreBuildErrors: process.env.SKIP_TYPE_CHECK === 'true',
  },
  
  // Optimize for production
  compress: true,
  poweredByHeader: false,
  
  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons'],
  },
  
  serverExternalPackages: ['axios'],
  
  transpilePackages: ['@bizosaas/shared-ui'],
  
  images: {
    domains: ['localhost', 'cdn.bizosaas.com', 'bizosaas-brain', 'bizosaas-wagtail-cms', 'bizosaas-superset'],
    unoptimized: process.env.NODE_ENV === 'development',
  },
  
  env: {
    NEXT_PUBLIC_APP_NAME: 'BizOSaaS Admin',
    NEXT_PUBLIC_APP_VERSION: '1.0.0',
    NEXT_PUBLIC_PLATFORM: 'BIZOSAAS',
  },

  // API configuration
  async rewrites() {
    return [
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://bizosaas-brain:8001'}/:path*`,
      },
      {
        source: '/api/auth/:path*',
        destination: `${process.env.NEXT_PUBLIC_AUTH_API_URL || 'http://bizosaas-auth-v2:8007'}/:path*`,
      },
      {
        source: '/api/analytics/:path*',
        destination: `${process.env.NEXT_PUBLIC_SUPERSET_URL || 'http://bizosaas-superset:8088'}/:path*`,
      },
      {
        source: '/api/crm/:path*',
        destination: `${process.env.NEXT_PUBLIC_CRM_API_URL || 'http://bizosaas-django-crm:8008'}/:path*`,
      },
    ];
  },

  // CORS headers for API routes
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Tenant',
            value: 'bizosaas',
          },
          {
            key: 'X-Platform-Type',
            value: 'admin-dashboard',
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
}

module.exports = nextConfig