/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'standalone', // Required for Docker deployment
  experimental: {
    appDir: true,
  },
  env: {
    BRAIN_GATEWAY_URL: process.env.BRAIN_GATEWAY_URL || 'http://localhost:8002',
    AUTH_SERVICE_URL: process.env.AUTH_SERVICE_URL || 'http://localhost:8007',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8002/api/:path*', // Brain Gateway proxy
      },
    ];
  },
};

module.exports = nextConfig;