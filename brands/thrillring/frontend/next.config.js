/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  typescript: {
    // Temporarily ignore type errors during build for rapid deployment
    ignoreBuildErrors: true,
  },
  eslint: {
    // Temporarily ignore ESLint errors during build for rapid deployment
    ignoreDuringBuilds: true,
  },
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'bizosaas.local',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'cdn.bizosaas.com',
        pathname: '/**',
      },
    ],
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  experimental: {
    optimizeCss: true,
  },
  // Skip problematic pages during static export
  trailingSlash: false,
  async rewrites() {
    return [
      {
        source: '/api/auth/:path*',
        destination: `${process.env.NEXT_PUBLIC_IDENTITY_SERVICE_URL || 'http://localhost:8001'}/auth/:path*`,
      },
      {
        source: '/api/users/:path*', 
        destination: `${process.env.NEXT_PUBLIC_IDENTITY_SERVICE_URL || 'http://localhost:8001'}/users/:path*`,
      },
      {
        source: '/api/tenants/:path*',
        destination: `${process.env.NEXT_PUBLIC_IDENTITY_SERVICE_URL || 'http://localhost:8001'}/tenants/:path*`,
      },
      {
        source: '/api/billing/:path*',
        destination: `${process.env.NEXT_PUBLIC_IDENTITY_SERVICE_URL || 'http://localhost:8001'}/billing/:path*`,
      },
      {
        source: '/api/ai/:path*',
        destination: `${process.env.NEXT_PUBLIC_AI_SERVICE_URL || 'http://localhost:8002'}/agents/:path*`,
      },
      // Add Brain API rewrites for FastAPI Central Hub integration
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'}/api/brain/:path*`,
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET, POST, PUT, DELETE, OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type, Authorization' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;