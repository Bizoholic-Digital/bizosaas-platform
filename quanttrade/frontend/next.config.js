/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable output file tracing for Docker optimization
  output: 'standalone',

  reactStrictMode: true,
  experimental: {
    appDir: true,
    // Enable server actions for real-time updates
    serverActions: true,
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8012',
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8012',
    QUANTTRADE_API_URL: process.env.QUANTTRADE_API_URL || 'http://localhost:8012',
    TRADINGVIEW_WIDGET_ID: process.env.TRADINGVIEW_WIDGET_ID || 'quanttrade-charts',
  },

  // Image optimization for trading charts and logos
  images: {
    domains: [
      'localhost',
      's3.tradingview.com',
      'cdn.tradingview.com',
      'finance.yahoo.com',
      'logo.clearbit.com'
    ],
    dangerouslyAllowSVG: true,
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
  },

  // Headers for security and CORS
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline' https://s3.tradingview.com https://cdn.tradingview.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' ws: wss: https: http:;"
          }
        ]
      }
    ]
  },

  // Rewrites for API routing to backend services
  async rewrites() {
    return [
      {
        source: '/api/portfolio/:path*',
        destination: 'http://quanttrade-backend:8012/api/portfolio/:path*'
      },
      {
        source: '/api/positions/:path*',
        destination: 'http://quanttrade-backend:8012/api/positions/:path*'
      },
      {
        source: '/api/market/:path*',
        destination: 'http://quanttrade-backend:8012/api/market/:path*'
      },
      {
        source: '/api/strategies/:path*',
        destination: 'http://quanttrade-backend:8012/api/strategies/:path*'
      },
      {
        source: '/api/backtesting/:path*',
        destination: 'http://quanttrade-backend:8012/api/backtesting/:path*'
      },
      {
        source: '/api/ai-agents/:path*',
        destination: 'http://quanttrade-backend:8012/api/ai-agents/:path*'
      },
      // Fallback for any other API routes
      {
        source: '/api/:path*',
        destination: 'http://localhost:8012/api/:path*',
      },
    ]
  },

  // Webpack configuration for trading libraries
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        os: false,
      }
    }
    return config
  },

  // Transpile packages for trading libraries
  transpilePackages: [
    'recharts',
    'framer-motion'
  ],

  // Production optimizations
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Compression and performance
  compress: true,
  poweredByHeader: false,
}

module.exports = nextConfig