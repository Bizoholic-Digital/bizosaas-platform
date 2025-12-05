/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
    serverActions: true,
  },
  output: 'standalone', // Enable standalone mode for Docker
  poweredByHeader: false, // Remove X-Powered-By header for security
  env: {
    // BizOSaaS Service URLs
    NEXT_PUBLIC_API_GATEWAY_URL: process.env.NEXT_PUBLIC_API_GATEWAY_URL || 'http://localhost:8080',
    NEXT_PUBLIC_AI_AGENTS_URL: process.env.NEXT_PUBLIC_AI_AGENTS_URL || 'http://localhost:8001',
    NEXT_PUBLIC_CRM_URL: process.env.NEXT_PUBLIC_CRM_URL || 'http://localhost:8007',
    NEXT_PUBLIC_CMS_URL: process.env.NEXT_PUBLIC_CMS_URL || 'http://localhost:8006',
    NEXT_PUBLIC_EVENT_BUS_URL: process.env.NEXT_PUBLIC_EVENT_BUS_URL || 'http://localhost:8009',
    NEXT_PUBLIC_DOMAIN_REPO_URL: process.env.NEXT_PUBLIC_DOMAIN_REPO_URL || 'http://localhost:8011',
    NEXT_PUBLIC_VAULT_URL: process.env.NEXT_PUBLIC_VAULT_URL || 'http://localhost:8201',
    NEXT_PUBLIC_TEMPORAL_URL: process.env.NEXT_PUBLIC_TEMPORAL_URL || 'http://localhost:8202',
    
    // Dashboard Configuration
    NEXT_PUBLIC_DASHBOARD_TITLE: process.env.NEXT_PUBLIC_DASHBOARD_TITLE || 'BizOSaaS Control Center',
    NEXT_PUBLIC_COMPANY_NAME: process.env.NEXT_PUBLIC_COMPANY_NAME || 'BizOSaaS',
    NEXT_PUBLIC_ENABLE_REAL_TIME: process.env.NEXT_PUBLIC_ENABLE_REAL_TIME || 'true',
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  async headers() {
    return [
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET, POST, PUT, DELETE, OPTIONS',
          },
          {
            key: 'Access-Control-Allow-Headers',
            value: 'Content-Type, Authorization',
          },
        ],
      },
    ];
  },
}

module.exports = nextConfig