/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Configure for FastAPI Brain integration (centralized business logic)
  env: {
    BRAIN_API_BASE_URL: process.env.BRAIN_API_BASE_URL || 'http://localhost:8001/api',
    SITE_NAME: 'Bizoholic - AI Marketing Automation',
    SITE_URL: process.env.SITE_URL || 'http://localhost:3000',
  },

  // Image optimization for FastAPI Brain served media
  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8001',
        pathname: '/media/**',
      },
      {
        protocol: 'https',
        hostname: 'api.bizoholic.com',
        pathname: '/media/**',
      },
    ],
  },

  // Rewrites for API proxy - ALL requests go through FastAPI Brain
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BRAIN_API_BASE_URL || 'http://localhost:8001/api'}/:path*`,
      },
    ]
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig