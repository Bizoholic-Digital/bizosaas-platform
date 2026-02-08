# BizBook Business Directory Frontend

A modern Next.js 14 frontend for the business directory service with Bizbook-inspired design.

## Features

- **Modern Stack**: Next.js 14 with App Router, TypeScript, Tailwind CSS
- **UI Components**: ShadCN UI components for consistent design
- **Responsive Design**: Mobile-first approach with responsive layouts
- **Search & Filters**: Advanced search with multiple filter options
- **Business Listings**: Comprehensive business cards with ratings, reviews, and details
- **Categories**: Business category browsing and filtering
- **Real-time Data**: Integration with FastAPI backend
- **SEO Optimized**: Built-in Next.js SEO features
- **Performance**: Optimized for Core Web Vitals

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: ShadCN UI (Radix UI primitives)
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Forms**: React Hook Form with Zod validation
- **State Management**: React Query for server state

## Getting Started

### Prerequisites

- Node.js 18+ and npm 8+
- FastAPI backend running on localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:3002](http://localhost:3002) in your browser

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx          # Homepage
│   └── search/           # Search results page
├── components/            # React components
│   ├── ui/               # ShadCN UI components
│   ├── layout/           # Header, footer, navigation
│   ├── hero/             # Hero section components
│   ├── business/         # Business-related components
│   └── search/           # Search and filter components
├── lib/                  # Utilities and API
│   ├── api.ts           # API client and endpoints
│   └── utils.ts         # Utility functions
├── types/               # TypeScript type definitions
└── hooks/               # Custom React hooks
```

## API Integration

The frontend integrates with the FastAPI backend running on localhost:8000:

### Available Endpoints

- `GET /directories` - Directory platforms list
- `GET /categories` - Business categories
- `GET /search` - Search businesses with filters
- `GET /events` - Business events
- `GET /products` - Featured products
- `GET /coupons` - Deals and coupons
- `GET /blog` - Blog posts
- `GET /community` - Community activity
- `GET /api/status` - API status

### API Client

The API client (`src/lib/api.ts`) provides TypeScript-safe functions for all endpoints with:
- Request/response interceptors
- Error handling
- Type safety with TypeScript interfaces
- Automatic retries and timeout handling

## Components

### Business Card
Displays business information with:
- Business name, category, and description
- Star ratings and review counts
- Verification and premium badges
- Contact information
- Opening hours status
- Action buttons (view details, website)

### Search Bar
Advanced search functionality with:
- Text search for business names/descriptions
- Location-based filtering
- Category selection
- Rating filters
- Price range options
- Open now filter
- Verification status filter

### Hero Section
Homepage hero with:
- Gradient background design
- Search form
- Platform statistics
- Popular search suggestions

## Styling

### Tailwind CSS
- Utility-first CSS framework
- Custom color scheme for Bizbook branding
- Responsive design utilities
- Animation and transition classes

### Design System
- Primary color: `#2563eb` (blue)
- Secondary color: `#f59e0b` (amber)
- Success: `#10b981` (green)
- Error: `#ef4444` (red)
- Consistent spacing and typography
- Shadow and border radius system

## Performance

### Core Web Vitals Optimization
- Image optimization with Next.js Image component
- Code splitting and lazy loading
- Efficient re-renders with React.memo
- Bundle size optimization

### SEO Features
- Meta tags and OpenGraph support
- Structured data for businesses
- Sitemap generation
- Clean URLs with Next.js routing

## Development

### Scripts
- `npm run dev` - Start development server on port 3002
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - TypeScript type checking

### Code Quality
- TypeScript for type safety
- ESLint for code linting
- Prettier for code formatting (optional)
- Consistent component patterns

## Deployment

### Environment Variables
Create a `.env.local` file for local development:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3002
```

### Production Deployment
The app can be deployed to:
- Vercel (recommended for Next.js)
- Netlify
- Docker containers
- Traditional hosting platforms

## Contributing

1. Follow the established component patterns
2. Use TypeScript for all new code
3. Follow the design system colors and spacing
4. Add proper error handling and loading states
5. Test responsive design on multiple devices
6. Optimize for performance and accessibility

## License

This project is part of the BizOSaaS platform.