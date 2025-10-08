/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable standalone output for Docker optimization
  output: 'standalone',

  // Skip type checking during build (for faster container builds)
  typescript: {
    ignoreBuildErrors: true,
  },

  // Optimize for production
  compress: true,
  poweredByHeader: false,

  // Environment variables
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001',
    NEXT_PUBLIC_SOCKET_URL: process.env.NEXT_PUBLIC_SOCKET_URL || 'http://localhost:8001',
    PORT: process.env.PORT || '3005',
  },

  // API configuration - Central Hub Integration
  async rewrites() {
    return [
      {
        source: '/api/brain/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'}/api/brain/:path*`,
      },
      {
        source: '/api/gaming/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'}/api/brain/gaming/:path*`,
      },
      {
        source: '/api/tournaments/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'}/api/brain/gaming/tournaments/:path*`,
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

  // Image optimization for gaming assets
  images: {
    domains: [
      'localhost',
      'bizosaas-brain',
      'bizosaas-wagtail-cms',
      'cdn.thrillring.com',
      'images.unsplash.com',
      'via.placeholder.com'
    ],
    unoptimized: false,
  },

  // Move external packages out of experimental
  serverExternalPackages: ['axios', 'socket.io-client'],

  // Experimental features for gaming portal
  experimental: {
    optimizePackageImports: ['@radix-ui/react-icons', 'lucide-react'],
  },

  // Webpack configuration for gaming assets
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }

    // Add support for video files
    config.module.rules.push({
      test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)$/,
      use: {
        loader: 'file-loader',
        options: {
          publicPath: '/_next/static/media/',
          outputPath: 'static/media/',
        },
      },
    });

    return config;
  },
};

export default nextConfig;