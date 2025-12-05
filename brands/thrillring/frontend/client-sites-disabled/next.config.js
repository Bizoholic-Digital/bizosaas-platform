/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost', 'bizoholic.com', 'coreldove.com', 'thrillring.com'],
  },
  async rewrites() {
    return [
      // API proxy to backend services
      {
        source: '/api/ai-agents/:path*',
        destination: 'http://localhost:8000/:path*',
      },
      {
        source: '/api/crm/:path*',
        destination: 'http://localhost:8007/api/:path*',
      },
      {
        source: '/api/directory/:path*',
        destination: 'http://localhost:8003/api/:path*',
      },
      {
        source: '/api/temporal/:path*',
        destination: 'http://localhost:8202/:path*',
      },
    ];
  },
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'Content-Type,Authorization' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;