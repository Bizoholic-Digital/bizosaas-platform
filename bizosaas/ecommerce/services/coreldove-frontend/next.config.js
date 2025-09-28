/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker optimization
  output: 'standalone',
  
  // Optimize for production
  reactStrictMode: true,
  compress: true,
  poweredByHeader: false,
  
  // Move serverComponentsExternalPackages out of experimental
  serverExternalPackages: ['axios'],
  
  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons'],
  },
  
  // Set output file tracing root to silence lockfile warnings
  outputFileTracingRoot: '/home/alagiri/projects/bizoholic/bizosaas-platform/frontend/apps/coreldove-frontend',
  
  images: {
    domains: ['localhost', 'coreldove.com', 'www.coreldove.com', 'bizosaas-saleor-api', 'bizosaas-wagtail-cms'],
    unoptimized: process.env.NODE_ENV === 'development',
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
};

module.exports = nextConfig;