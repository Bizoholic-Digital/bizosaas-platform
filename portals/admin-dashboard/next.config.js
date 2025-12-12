const withPWA = require("@ducanh2912/next-pwa").default({
  dest: "public",
  disable: process.env.NODE_ENV === "development",
  register: true,
  scope: "/app",
  sw: "service-worker.js",
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@bizosaas/shared-ui'],
  typescript: {
    ignoreBuildErrors: true,  // Temporarily ignore TS errors for deployment
  },
  eslint: {
    ignoreDuringBuilds: true,  // Temporarily ignore ESLint errors
  },
  output: 'standalone', // For Docker production builds
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  env: {
    NEXT_PUBLIC_BRAIN_GATEWAY_URL: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000',
    NEXT_PUBLIC_AUTH_URL: process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8008',
    NEXT_PUBLIC_TEMPORAL_UI_URL: process.env.NEXT_PUBLIC_TEMPORAL_UI_URL || 'http://localhost:8233',
    NEXT_PUBLIC_VAULT_UI_URL: process.env.NEXT_PUBLIC_VAULT_UI_URL || 'http://localhost:8200',
  },
  async rewrites() {
    return [
      {
        source: '/api/brain/:path*',
        destination: 'http://localhost:8000/:path*',
      },
    ];
  },
  webpack: (config, { isServer }) => {
    const path = require('path');
    // Fix module resolution for shared packages
    config.resolve.alias = {
      ...config.resolve.alias,
      'lucide-react': path.resolve(__dirname, 'node_modules/lucide-react'),
      'next-auth': path.resolve(__dirname, 'node_modules/next-auth'),
      'react': path.resolve(__dirname, 'node_modules/react'),
      'react/jsx-runtime': path.resolve(__dirname, 'node_modules/react/jsx-runtime'),
      'react-dom': path.resolve(__dirname, 'node_modules/react-dom')
    };
    return config;
  },
}

module.exports = withPWA(nextConfig);
