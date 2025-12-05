# CoreLDove E-commerce Website

A complete, modern e-commerce platform built with Next.js 14, integrated with Saleor GraphQL API, Amazon product sourcing, and AI-powered product recommendations.

## 🚀 Features

### Modern E-commerce Experience
- **Complete Product Catalog**: Browse products with advanced filtering and search
- **Product Detail Pages**: Comprehensive product information with reviews and specifications
- **Shopping Cart**: Full cart management with Saleor GraphQL integration
- **AI Recommendations**: Personalized product suggestions powered by AI agents
- **Responsive Design**: Mobile-first design that works on all devices

### AI-Powered Product Sourcing
- **Amazon API Integration**: Live product data and inventory management
- **AI Product Discovery**: Automated product sourcing with quality verification
- **Intelligent Categorization**: AI-driven product classification and tagging
- **Demand Analysis**: Market trend analysis and profit margin calculations

### Business Intelligence Dashboard
- **Real-time Analytics**: Sales metrics, conversion rates, and performance tracking
- **AI Sourcing Dashboard**: Product approval workflow and market insights
- **Inventory Management**: Live stock levels and automated reordering
- **Revenue Tracking**: Comprehensive financial reporting and forecasting

### CoreLDove Branding
- **Brand Identity**: Complete CoreLDove blue/red color scheme implementation
- **Professional Design**: Clean, modern UI with consistent brand elements
- **Trust Indicators**: Security badges, guarantees, and customer testimonials
- **SEO Optimized**: Meta tags, structured data, and performance optimized

## 🛠️ Technology Stack

- **Frontend**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom CoreLDove theme
- **State Management**: React hooks and Zustand
- **API Integration**: GraphQL (Saleor), REST (Amazon, AI Agents)
- **Icons**: Lucide React for consistent iconography
- **Performance**: Image optimization, lazy loading, and caching

## 📁 Project Structure

```
coreldove-frontend/
├── app/                          # Next.js 13+ app directory
│   ├── about/                    # About page
│   ├── catalog/                  # Product catalog with filters
│   ├── contact/                  # Contact form and support
│   ├── dashboard/                # AI sourcing dashboard
│   ├── product/[id]/            # Dynamic product detail pages
│   ├── api/                     # API routes
│   │   ├── products/            # Saleor product integration
│   │   ├── cart/                # Shopping cart management
│   │   └── ai/recommendations/   # AI-powered recommendations
│   ├── globals.css              # Global styles with CoreLDove theme
│   ├── layout.tsx               # Root layout with branding
│   └── page.tsx                 # Homepage with complete e-commerce sections
├── public/                      # Static assets
│   ├── coreldove-simple-logo.png
│   └── favicon.ico
├── package.json                 # Dependencies and scripts
├── tailwind.config.js          # Tailwind with CoreLDove colors
└── README.md                   # This file
```

## 🔌 API Integrations

### Saleor GraphQL API
- **Products**: Fetch product catalog with variants and pricing
- **Cart Management**: Create and manage shopping carts/checkouts
- **Orders**: Process orders and track fulfillment
- **Inventory**: Real-time stock levels and availability

### Amazon Sourcing Service
- **Product Discovery**: Import products from Amazon catalog
- **Pricing Data**: Live pricing and competitor analysis
- **Market Research**: Demand analysis and trend identification
- **Quality Metrics**: Product ratings and review analysis

### AI Agent System
- **Product Recommendations**: Personalized suggestions based on user behavior
- **Market Intelligence**: AI-powered demand forecasting
- **Content Generation**: Automated product descriptions and SEO content
- **Performance Analytics**: Conversion optimization insights

## 🎨 CoreLDove Brand Elements

### Color Palette
```css
/* Primary Colors */
--color-coreldove-red: #dc2626;
--color-coreldove-blue: #2563eb;

/* Gradients */
.coreldove-gradient: linear-gradient(135deg, #dc2626 0%, #2563eb 100%);
```

### Typography
- **Primary Font**: Inter (Google Fonts)
- **Headings**: Bold, clean hierarchy
- **Body Text**: Readable, accessible contrast ratios

### Components
- **Buttons**: Gradient backgrounds with hover effects
- **Cards**: Subtle shadows with hover animations
- **Navigation**: Clean, intuitive layout
- **Forms**: Consistent styling with validation

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ installed
- Access to Saleor GraphQL API (localhost:8020)
- AI Agents service running (localhost:8000)
- Amazon sourcing service (localhost:8010)

### Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your API keys and URLs
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Access the Website**
   - Main website: http://localhost:3002
   - Saleor Dashboard: http://localhost:9020
   - AI Dashboard: http://localhost:3002/dashboard

### Environment Configuration

```env
# Required for basic functionality
NEXT_PUBLIC_SALEOR_API_URL=http://localhost:8020/graphql/
AI_AGENTS_URL=http://localhost:8000

# Required for full AI functionality
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Optional for enhanced features
AMAZON_SOURCING_URL=http://localhost:8010
NEXT_PUBLIC_ENABLE_AI_RECOMMENDATIONS=true
```

## 📱 Pages & Features

### Homepage (`/`)
- Hero section with CoreLDove branding
- Featured product categories
- Trending products grid
- Customer testimonials
- Trust indicators and guarantees
- Newsletter signup
- Comprehensive footer

### Product Catalog (`/catalog`)
- Advanced search and filtering
- Category-based navigation
- Grid/list view toggle
- Sort by price, rating, popularity
- Pagination and infinite scroll
- Real-time inventory status

### Product Details (`/product/[id]`)
- High-quality product imagery
- Detailed specifications and features
- Customer reviews and ratings
- Add to cart functionality
- Related product suggestions
- Trust badges and guarantees

### About Page (`/about`)
- Company story and mission
- CoreLDove values and principles
- Technology stack showcase
- Team and commitment information
- Brand timeline and milestones

### Contact Page (`/contact`)
- Multi-channel contact information
- Contact form with category selection
- FAQ section with common questions
- Business hours and support info
- Response time expectations

### AI Dashboard (`/dashboard`)
- Product sourcing analytics
- AI recommendations approval workflow
- Performance metrics and KPIs
- Recent activity feed
- Quick action buttons
- Saleor dashboard integration

## 🔧 API Routes

### Products API (`/api/products`)
- **GET**: Fetch products with filtering and pagination
- Integrates with Saleor GraphQL
- Fallback to Amazon sourcing service
- Supports category, price, and rating filters

### Cart API (`/api/cart`)
- **GET**: Retrieve current cart contents
- **POST**: Add items to cart
- **PUT**: Update item quantities
- **DELETE**: Remove items from cart
- Full Saleor checkout integration

### AI Recommendations (`/api/ai/recommendations`)
- **GET/POST**: Get personalized product recommendations
- Integrates with CoreLDove AI agents
- Supports user preferences and history
- Fallback to rule-based recommendations

## 🎯 Key Features Implementation

### AI-Powered Product Discovery
```typescript
// Fetch AI recommendations
const recommendations = await fetch('/api/ai/recommendations', {
  method: 'POST',
  body: JSON.stringify({
    userId: 'user-id',
    category: 'sports',
    priceRange: { min: 20, max: 100 }
  })
})
```

### Saleor Integration
```typescript
// Add to cart with Saleor
const cartData = await fetch('/api/cart', {
  method: 'POST',
  body: JSON.stringify({
    action: 'add',
    variantId: 'product-variant-id',
    quantity: 1
  })
})
```

### Real-time Search
```typescript
// Product search with filtering
const products = await fetch('/api/products?' + new URLSearchParams({
  search: searchQuery,
  category: selectedCategory,
  minPrice: '20',
  maxPrice: '200',
  sortBy: 'price-low'
}))
```

## 📊 Analytics & Performance

### Core Web Vitals
- **LCP**: < 2.5s (optimized images and lazy loading)
- **FID**: < 100ms (minimal JavaScript blocking)
- **CLS**: < 0.1 (stable layout with placeholders)

### E-commerce Metrics
- **Conversion Rate**: Tracked via user actions
- **Cart Abandonment**: Monitored and optimized
- **Page Load Speed**: Optimized for mobile and desktop
- **SEO Performance**: Schema.org markup and meta tags

### AI Performance
- **Recommendation Accuracy**: Tracked via click-through rates
- **Product Discovery**: Success rate of AI-sourced products
- **User Engagement**: Time spent browsing AI recommendations

## 🔐 Security & Privacy

### Data Protection
- **User Privacy**: No personal data stored without consent
- **Secure API**: All API calls use HTTPS in production
- **Payment Security**: PCI-compliant payment processing
- **Content Security**: CSP headers and XSS protection

### Performance Monitoring
- **Error Tracking**: Comprehensive error logging
- **Performance Metrics**: Real-time performance monitoring
- **User Analytics**: Privacy-compliant user behavior tracking

## 🚀 Deployment

### Production Build
```bash
npm run build
npm run start
```

### Docker Deployment
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3002
CMD ["npm", "start"]
```

### Environment Variables for Production
```env
NODE_ENV=production
NEXT_PUBLIC_API_BASE_URL=https://your-domain.com
NEXT_PUBLIC_SALEOR_API_URL=https://your-saleor-instance.com/graphql/
```

## 📈 Future Enhancements

### Phase 2 Features
- **Multi-language Support**: i18n for global markets
- **Advanced Analytics**: Enhanced reporting dashboard
- **Mobile App**: React Native companion app
- **Subscription Products**: Recurring payment support

### AI Enhancements
- **Visual Search**: AI-powered image-based product search
- **Chatbot Integration**: AI customer service assistant
- **Predictive Analytics**: Advanced demand forecasting
- **Personalization**: Enhanced user experience customization

## 📞 Support

For technical support or questions about the CoreLDove e-commerce platform:

- **Email**: support@coreldove.com
- **Documentation**: Internal wiki and API docs
- **Issue Tracking**: GitHub issues for bug reports
- **Feature Requests**: Product roadmap discussions

---

Built with ❤️ by the CoreLDove Team using Next.js, Saleor, and AI technology.