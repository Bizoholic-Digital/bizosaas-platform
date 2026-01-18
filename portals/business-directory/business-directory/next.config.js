/** @type {import('next').NextConfig} */
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development'
});

const nextConfig = {
  output: 'standalone',
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: true,
  },
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
  },
  serverExternalPackages: ['axios'],
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8080',
      },
    ],
  },
  async rewrites() {
    return [
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/brain/:path*`,
      },
    ]
  },
  async redirects() {
    return [
      {
        source: '/business/:slug',
        destination: '/biz/:slug',
        permanent: true,
      },
      {
        source: '/categories/:slug',
        destination: '/c/:slug',
        permanent: true,
      },
      {
        source: '/categories',
        destination: '/c',
        permanent: true,
      },
    ]
  },
}

module.exports = withPWA(nextConfig)