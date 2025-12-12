import { createRequire } from 'module';
const require = createRequire(import.meta.url);

/** @type {import('next').NextConfig} */
/* eslint-disable @typescript-eslint/no-var-requires */
const nextConfig = {
  transpilePackages: ['@bizosaas/shared-ui'],
  // Enable standalone output for Docker optimization
  output: 'standalone',

  // Skip type checking during build (for faster container builds)
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Optimize for production
  compress: true,
  poweredByHeader: false,

  // Environment variables
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001',
    PORT: process.env.PORT || '3000',
  },

  // API configuration - Central Hub Integration
  async rewrites() {
    return [
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'}/api/brain/:path*`,
      },
    ];
  },

  // CORS headers for API routes
  async headers() {
    return [
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

  // Image optimization
  images: {
    domains: [
      'localhost',
      'bizosaas-brain',
      'bizosaas-wagtail-cms',
      'bizosaas.local',
      'portal.bizosaas.local',
      'api.bizosaas.local',
    ],
    unoptimized: false,
  },

  // Move external packages out of experimental
  serverExternalPackages: ['axios'],

  // Experimental features
  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons'],
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    // Fix module resolution for shared packages
    config.resolve.alias = {
      ...config.resolve.alias,
      'lucide-react': require.resolve('lucide-react'),
      'next-auth': require.resolve('next-auth'),
      'react': require.resolve('react'),
      'react/jsx-runtime': require.resolve('react/jsx-runtime'),
      'react-dom': require.resolve('react-dom')
    };

    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
};

// PWA Configuration
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
});

export default withPWA(nextConfig);