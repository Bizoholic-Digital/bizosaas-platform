/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',

  // Base path for reverse proxy routing (e.g., /portal/)
  basePath: process.env.BASE_PATH || '',

  // Transpile local packages from monorepo
  transpilePackages: [
    '@bizoholic-digital/ui-components',
    '@bizoholic-digital/auth',
    '@bizoholic-digital/api-client',
    '@bizoholic-digital/hooks',
    '@bizoholic-digital/utils',
    '@bizoholic-digital/animated-components',
  ],

<<<<<<< HEAD:bizosaas-brain-core/client-portal/next.config.js
  // Base path for portal access
  // basePath: '/portal', // Removed for subdomain architecture (client.bizoholic.com)

  // Environment variables
=======
  // Configure for FastAPI Brain integration (centralized business logic)
>>>>>>> 689624bdacbb85634f44c01400300bc3ce37e57e:bizosaas/frontend/apps/client-portal/next.config.js
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
<<<<<<< HEAD:bizosaas-brain-core/client-portal/next.config.js
    ];
=======
    ]
>>>>>>> 689624bdacbb85634f44c01400300bc3ce37e57e:bizosaas/frontend/apps/client-portal/next.config.js
  },

  // Comprehensive security headers (Gold Standard 2025)
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          // Content Security Policy (XSS Protection)
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-eval' 'unsafe-inline' https://static.cloudflareinsights.com", // TODO: Remove unsafe-inline in production
              "style-src 'self' 'unsafe-inline'", // Required for Tailwind
              "img-src 'self' data: https: blob:",
              "font-src 'self' data:",
              "connect-src 'self' https://api.bizoholic.com https://cloudflareinsights.com",
              "frame-ancestors 'none'",
              "base-uri 'self'",
              "form-action 'self' https://accounts.google.com https://login.microsoftonline.com https://github.com https://slack.com https://www.linkedin.com",
              "upgrade-insecure-requests",
            ].join('; ')
          },
          // Clickjacking Protection
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          // MIME Type Sniffing Protection
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          // Referrer Policy
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          // Permissions Policy (formerly Feature-Policy)
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), interest-cohort=()',
          },
          // Strict Transport Security (HTTPS only)
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains; preload',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig