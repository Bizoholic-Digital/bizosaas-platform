'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { 
  ArrowRight,
  Check,
  Star,
  TrendingUp,
  Brain,
  Zap,
  Shield,
  Play,
  DollarSign,
  Package,
  Search,
  ShoppingCart,
  Heart,
  User,
  Menu,
  ChevronRight,
  Award,
  Truck,
  RefreshCw
} from 'lucide-react'

// Conversion-Optimized CoreLDove E-commerce Homepage
// Minimalistic, Elegant, High-Converting Design
// Based on 2025 e-commerce best practices

const CoreLDovePage = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentHero, setCurrentHero] = useState(0)

  // Hero carousel data - Health, Fitness, Sports & Wellness Focus
  const heroSlides = [
    {
      title: "Elevate Your Fitness Journey",
      subtitle: "AI-Curated Premium Health & Fitness Products",
      cta: "Shop Fitness",
      image: "/hero/fitness-hero.jpg",
      badge: "New Arrivals"
    },
    {
      title: "Peak Performance Gear",
      subtitle: "Sports Equipment & Wellness Products",
      cta: "Explore Sports",
      image: "/hero/sports-hero.jpg", 
      badge: "Best Sellers"
    },
    {
      title: "Wellness Revolution",
      subtitle: "Transform Your Health with Premium Products",
      cta: "Shop Wellness",
      image: "/hero/wellness-hero.jpg", 
      badge: "Trending"
    }
  ]

  // Featured products - Health, Fitness, Sports & Wellness Focus
  const featuredProducts = [
    {
      id: "1",
      name: "Premium Yoga Mat Anti-Slip 6mm",
      price: 45,
      originalPrice: 65,
      image: "/products/yoga-mat.jpg",
      rating: 4.9,
      reviews: 2847,
      badge: "Bestseller",
      urgency: "Only 5 left",
      category: "fitness"
    },
    {
      id: "2", 
      name: "Adjustable Dumbbells Set 5-25kg",
      price: 189,
      originalPrice: 249,
      image: "/products/dumbbells.jpg",
      rating: 4.8,
      reviews: 1892,
      badge: "Featured",
      urgency: "Hot seller",
      category: "fitness"
    },
    {
      id: "3",
      name: "Smart Fitness Tracker & Heart Monitor",
      price: 99,
      originalPrice: 129,
      image: "/products/fitness-tracker.jpg",
      rating: 4.7,
      reviews: 3156,
      badge: "Tech Pick",
      urgency: "Trending",
      category: "health"
    },
    {
      id: "4",
      name: "Whey Protein Powder 2kg", 
      price: 67,
      originalPrice: 89,
      image: "/products/protein-powder.jpg",
      rating: 4.9,
      reviews: 2543,
      badge: "New",
      urgency: "Limited batch",
      category: "nutrition"
    },
    {
      id: "5",
      name: "Resistance Bands Set Pro", 
      price: 29,
      originalPrice: 45,
      image: "/products/resistance-bands.jpg",
      rating: 4.6,
      reviews: 1876,
      badge: "Value Pick",
      urgency: "Popular choice",
      category: "fitness"
    },
    {
      id: "6",
      name: "Foam Roller for Recovery", 
      price: 35,
      image: "/products/foam-roller.jpg",
      rating: 4.8,
      reviews: 967,
      badge: "Recovery",
      urgency: "Wellness essential",
      category: "wellness"
    }
  ]

  // Trust badges and social proof
  const trustIndicators = [
    { icon: Truck, text: "Free shipping on orders $50+" },
    { icon: RefreshCw, text: "30-day easy returns" },
    { icon: Shield, text: "Secure checkout" },
    { icon: Award, text: "5-star customer service" }
  ]

  // Auto-rotate hero carousel
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentHero((prev) => (prev + 1) % heroSlides.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [])

  return (
    <div className="min-h-screen bg-white">
      {/* Header - Minimalist Navigation */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-gray-100">
        <div className="container mx-auto px-4">
          {/* Top announcement bar */}
          <div className="py-2 text-center bg-gray-900 text-white text-sm">
            <span>Free shipping on orders over $50 • Limited time offer</span>
          </div>
          
          <div className="flex items-center justify-between py-4">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2">
              <Image 
                src="/images/Coreldove-Simple.png" 
                alt="CoreLDove - AI-Curated Premium Products" 
                width={160} 
                height={48}
                className="h-10 w-auto"
                priority
              />
            </Link>

            {/* Search Bar - Prominent placement */}
            <div className="hidden md:flex flex-1 max-w-lg mx-8">
              <div className="relative w-full">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 rounded-full border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Action buttons */}
            <div className="flex items-center space-x-4">
              <button className="p-2 hover:bg-gray-100 rounded-full">
                <Heart className="h-5 w-5" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-full">
                <User className="h-5 w-5" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded-full relative">
                <ShoppingCart className="h-5 w-5" />
                <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">0</span>
              </button>
              <button 
                className="md:hidden p-2"
                onClick={() => setIsMenuOpen(!isMenuOpen)}
              >
                <Menu className="h-5 w-5" />
              </button>
            </div>
          </div>

          {/* Navigation Menu - Health, Fitness, Sports & Wellness Focus */}
          <nav className="hidden md:flex items-center justify-center space-x-8 pb-4">
            <Link href="/collections/all" className="text-gray-700 hover:text-orange-600 font-medium">All Products</Link>
            <Link href="/collections/fitness" className="text-gray-700 hover:text-orange-600 font-medium">Fitness Equipment</Link>
            <Link href="/collections/sports" className="text-gray-700 hover:text-orange-600 font-medium">Sports & Athletics</Link>
            <Link href="/collections/health" className="text-gray-700 hover:text-orange-600 font-medium">Health Products</Link>
            <Link href="/collections/wellness" className="text-gray-700 hover:text-orange-600 font-medium">Wellness & Recovery</Link>
            <Link href="/collections/nutrition" className="text-gray-700 hover:text-orange-600 font-medium">Sports Nutrition</Link>
            <Link href="/deals" className="text-red-600 hover:text-red-700 font-semibold">Hot Deals</Link>
          </nav>
        </div>
      </header>

      {/* Hero Section - Conversion-Focused */}
      <section className="relative h-[80vh] bg-gray-50 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-black/20 to-transparent z-10" />
        <div className="container mx-auto px-4 relative z-20 h-full flex items-center">
          <div className="max-w-xl">
            {heroSlides[currentHero].badge && (
              <div className="inline-block mb-4">
                <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  {heroSlides[currentHero].badge}
                </span>
              </div>
            )}
            <h1 className="text-5xl font-bold text-gray-900 mb-4 leading-tight">
              {heroSlides[currentHero].title}
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              {heroSlides[currentHero].subtitle}
            </p>
            <div className="flex space-x-4">
              <button className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold flex items-center">
                {heroSlides[currentHero].cta}
                <ArrowRight className="ml-2 h-4 w-4" />
              </button>
              <button className="border border-gray-300 text-gray-700 px-8 py-4 rounded-lg hover:bg-gray-50 transition-colors font-semibold flex items-center">
                <Play className="mr-2 h-4 w-4" />
                Watch Demo
              </button>
            </div>
          </div>
        </div>
        
        {/* Hero carousel indicators */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2 z-20">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentHero(index)}
              className={`w-2 h-2 rounded-full transition-colors ${
                index === currentHero ? 'bg-blue-600' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </section>

      {/* Trust Indicators Bar */}
      <section className="bg-gray-50 py-4">
        <div className="container mx-auto px-4">
          <div className="flex justify-center items-center space-x-8 overflow-x-auto">
            {trustIndicators.map((indicator, index) => (
              <div key={index} className="flex items-center space-x-2 text-gray-600 whitespace-nowrap">
                <indicator.icon className="h-4 w-4" />
                <span className="text-sm font-medium">{indicator.text}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Featured Products</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Discover our hand-picked selection of premium products, curated by AI for quality and value.
            </p>
          </div>

          {/* Product Grid - Optimized for Conversion */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product) => (
              <div key={product.id} className="group bg-white rounded-lg shadow-sm hover:shadow-lg transition-shadow border border-gray-100 overflow-hidden">
                {/* Product Image */}
                <div className="relative aspect-square overflow-hidden bg-gray-100">
                  {product.badge && (
                    <div className="absolute top-3 left-3 z-10">
                      <span className="bg-blue-600 text-white px-2 py-1 rounded text-xs font-medium">
                        {product.badge}
                      </span>
                    </div>
                  )}
                  {product.urgency && (
                    <div className="absolute top-3 right-3 z-10">
                      <span className="bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
                        {product.urgency}
                      </span>
                    </div>
                  )}
                  <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
                    <Package className="h-12 w-12 text-gray-400" />
                  </div>
                  <button className="absolute top-3 right-3 p-2 bg-white/80 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                    <Heart className="h-4 w-4" />
                  </button>
                </div>

                {/* Product Details */}
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                    {product.name}
                  </h3>
                  
                  {/* Rating and Reviews */}
                  <div className="flex items-center mb-2">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`h-3 w-3 ${
                            i < Math.floor(product.rating)
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-xs text-gray-500 ml-1">
                      {product.rating} ({product.reviews})
                    </span>
                  </div>

                  {/* Price */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-xl font-bold text-gray-900">
                        ${product.price}
                      </span>
                      {product.originalPrice && (
                        <span className="text-sm text-gray-500 line-through">
                          ${product.originalPrice}
                        </span>
                      )}
                    </div>
                    {product.originalPrice && (
                      <span className="bg-red-100 text-red-600 px-2 py-1 rounded text-xs font-medium">
                        Save ${product.originalPrice - product.price}
                      </span>
                    )}
                  </div>

                  {/* Add to Cart Button */}
                  <button className="w-full bg-gray-900 text-white py-2 rounded-lg hover:bg-gray-800 transition-colors font-medium">
                    Add to Cart
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* View All Products CTA */}
          <div className="text-center mt-12">
            <Link href="/collections/all" className="inline-flex items-center bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold">
              View All Products
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose CoreLDove</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              We combine AI-powered curation with human expertise to bring you the best products at the best prices.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI-Curated Selection</h3>
              <p className="text-gray-600">
                Our AI algorithms analyze thousands of products to bring you only the highest quality items.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <DollarSign className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Best Prices Guaranteed</h3>
              <p className="text-gray-600">
                We continuously monitor prices to ensure you always get the best deals available.
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Lightning Fast Delivery</h3>
              <p className="text-gray-600">
                Free shipping on orders over $50 with express delivery options available.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Join 50,000+ Happy Customers</h2>
            <div className="flex justify-center items-center space-x-4 mb-8">
              <div className="flex">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                ))}
              </div>
              <span className="text-gray-600">4.9/5 based on 12,847 reviews</span>
            </div>
          </div>

          {/* Customer reviews would go here */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map((review) => (
              <div key={review} className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                <div className="flex mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-4">
                  "Amazing quality and fast shipping. CoreLDove has become my go-to for online shopping!"
                </p>
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-gray-300 rounded-full mr-3"></div>
                  <div>
                    <div className="font-semibold">Sarah M.</div>
                    <div className="text-sm text-gray-500">Verified Customer</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter Signup - Conversion Optimized */}
      <section className="bg-blue-600 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Get Exclusive Deals & New Arrivals
          </h2>
          <p className="text-blue-100 mb-8 max-w-2xl mx-auto">
            Join our newsletter and be the first to know about new products, exclusive discounts, and special offers.
          </p>
          <div className="max-w-md mx-auto flex">
            <input
              type="email"
              placeholder="Enter your email address"
              className="flex-1 px-4 py-3 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
            <button className="bg-gray-900 text-white px-6 py-3 rounded-r-lg hover:bg-gray-800 transition-colors font-semibold">
              Subscribe
            </button>
          </div>
          <p className="text-blue-100 text-sm mt-4">
            *Get 10% off your first order when you subscribe
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Company Info */}
            <div>
              <Image 
                src="/coreldove-logo-white.svg" 
                alt="CoreLDove" 
                width={140} 
                height={40}
                className="h-8 w-auto mb-4"
              />
              <p className="text-gray-400 mb-4">
                AI-powered e-commerce platform bringing you the best products at the best prices.
              </p>
              <div className="flex space-x-4">
                {/* Social media icons would go here */}
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="font-semibold mb-4">Shop</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/collections/all" className="hover:text-white">All Products</Link></li>
                <li><Link href="/collections/electronics" className="hover:text-white">Electronics</Link></li>
                <li><Link href="/collections/fitness" className="hover:text-white">Fitness</Link></li>
                <li><Link href="/deals" className="hover:text-white">Deals</Link></li>
              </ul>
            </div>

            {/* Customer Service */}
            <div>
              <h3 className="font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/help" className="hover:text-white">Help Center</Link></li>
                <li><Link href="/contact" className="hover:text-white">Contact Us</Link></li>
                <li><Link href="/returns" className="hover:text-white">Returns</Link></li>
                <li><Link href="/shipping" className="hover:text-white">Shipping Info</Link></li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white">About Us</Link></li>
                <li><Link href="/careers" className="hover:text-white">Careers</Link></li>
                <li><Link href="/privacy" className="hover:text-white">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white">Terms of Service</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 CoreLDove. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default CoreLDovePage