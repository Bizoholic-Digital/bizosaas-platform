const withPWA = require("@ducanh2912/next-pwa").default({
  dest: "public",
  disable: false, // Enable PWA
  register: true,
  scope: "/",
  sw: "sw.js",
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
  output: 'standalone',
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  env: {
    NEXT_PUBLIC_BRAIN_API_URL: process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_AUTH_URL: process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:8008',
    NEXT_PUBLIC_TEMPORAL_UI_URL: process.env.NEXT_PUBLIC_TEMPORAL_UI_URL || 'http://localhost:8233',
    NEXT_PUBLIC_VAULT_UI_URL: process.env.NEXT_PUBLIC_VAULT_UI_URL || 'http://localhost:8200',
  },
  async rewrites() {
    return [
      {
        source: '/api/brain/health',
        destination: `${process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000'}/health`,
      },
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000'}/api/:path*`,
      },
    ];
  },


};
module.exports = withPWA(nextConfig);
