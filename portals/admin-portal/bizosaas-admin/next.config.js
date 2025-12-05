/** @type {import('next').NextConfig} */
const nextConfig = {
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
}

module.exports = nextConfig
