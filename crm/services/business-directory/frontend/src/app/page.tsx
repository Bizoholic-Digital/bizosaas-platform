'use client'

import React, { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import HeroSection from '@/components/hero/hero-section'
import BusinessCard from '@/components/business/business-card'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import {
  TrendingUp,
  Star,
  Users,
  Calendar,
  ShoppingBag,
  Tag,
  MessageSquare,
  ArrowRight,
  MapPin,
  Clock,
  Zap,
  Shield,
  Award,
  Globe
} from 'lucide-react'
import {
  getAPIStatus,
  getCategories,
  searchBusinesses,
  getEvents,
  getFeaturedProducts,
  getCoupons,
  getCommunityActivity
} from '@/lib/api'
import type {
  APIStatus,
  BusinessCategory,
  BusinessListing,
  BusinessEvent,
  FeaturedProduct,
  Coupon,
  CommunityActivity,
  SearchFilters
} from '@/types'

const HomePage = () => {
  const router = useRouter()
  const [isLoading, setIsLoading] = useState(true)
  const [apiStatus, setApiStatus] = useState<APIStatus | null>(null)
  const [categories, setCategories] = useState<BusinessCategory[]>([])
  const [featuredBusinesses, setFeaturedBusinesses] = useState<BusinessListing[]>([])
  const [recentEvents, setRecentEvents] = useState<BusinessEvent[]>([])
  const [featuredProducts, setFeaturedProducts] = useState<FeaturedProduct[]>([])
  const [topCoupons, setTopCoupons] = useState<Coupon[]>([])
  const [communityActivity, setCommunityActivity] = useState<CommunityActivity[]>([])

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true)
        
        // Load API status and metrics
        const status = await getAPIStatus()
        setApiStatus(status)

        // Load categories
        const categoriesData = await getCategories()
        setCategories(categoriesData.slice(0, 8)) // Show top 8 categories

        // Load featured businesses
        const businessResults = await searchBusinesses({
          premium_only: true,
          limit: 6,
          sort_by: 'rating'
        })
        setFeaturedBusinesses(businessResults.businesses || [])

        // Load recent events
        const events = await getEvents({ limit: 4 })
        setRecentEvents(events.slice(0, 4))

        // Load featured products
        const products = await getFeaturedProducts({ limit: 4 })
        setFeaturedProducts(products.slice(0, 4))

        // Load top coupons
        const coupons = await getCoupons({ active_only: true, limit: 4 })
        setTopCoupons(coupons.slice(0, 4))

        // Load community activity
        const community = await getCommunityActivity({ limit: 6 })
        setCommunityActivity(community.slice(0, 6))

      } catch (error) {
        console.error('Error loading homepage data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadData()
  }, [])

  const handleSearch = (query: string, location: string) => {
    const params = new URLSearchParams()
    if (query) params.set('q', query)
    if (location) params.set('location', location)
    router.push(`/search?${params.toString()}`)
  }

  const categoryIcons: { [key: string]: React.ReactNode } = {
    'restaurants': '🍽️',
    'retail': '🛍️',
    'healthcare': '🏥',
    'automotive': '🚗',
    'home-services': '🏠',
    'beauty': '💄',
    'fitness': '💪',
    'education': '📚',
    'professional': '💼',
    'entertainment': '🎭'
  }

  if (isLoading) {
    return (
      <div className="min-h-screen">
        {/* Hero Section Skeleton */}
        <div className="hero-bg h-96 flex items-center">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center space-y-6">
              <Skeleton className="h-16 w-3/4 mx-auto bg-white/20" />
              <Skeleton className="h-6 w-2/3 mx-auto bg-white/20" />
              <Skeleton className="h-16 w-full mx-auto bg-white/90" />
            </div>
          </div>
        </div>
        
        {/* Content Skeletons */}
        <div className="container mx-auto px-4 py-12 space-y-12">
          {/* Categories Skeleton */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[...Array(8)].map((_, i) => (
              <Skeleton key={i} className="h-24" />
            ))}
          </div>
          
          {/* Featured Businesses Skeleton */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} className="h-80" />
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection
        onSearch={handleSearch}
        totalBusinesses={apiStatus?.metrics?.total_businesses || 0}
        totalCategories={apiStatus?.metrics?.total_categories || 0}
        totalReviews={10000} // Mock data
      />

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12 space-y-16">
        {/* Categories Section */}
        <section className="fade-in">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Explore Business Categories
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Find exactly what you&apos;re looking for in our comprehensive business directory
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {categories.map((category, index) => (
              <Card
                key={category.id}
                className="cursor-pointer card-hover text-center"
                onClick={() => router.push(`/search?category=${category.slug}`)}
              >
                <CardContent className="p-6">
                  <div className="text-4xl mb-3">
                    {categoryIcons[category.slug] || '📁'}
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {category.name}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {category.business_count || 0} businesses
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div className="text-center mt-8">
            <Button
              variant="outline"
              size="lg"
              onClick={() => router.push('/categories')}
              className="border-bizbook-primary text-bizbook-primary hover:bg-bizbook-primary hover:text-white"
            >
              View All Categories
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </section>

        {/* Featured Businesses */}
        <section className="fade-in">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Featured Premium Businesses
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Discover top-rated, verified businesses that our community loves
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredBusinesses.map((business) => (
              <BusinessCard
                key={business.business_id}
                business={business}
                variant="featured"
                showFullDetails={false}
              />
            ))}
          </div>
          
          <div className="text-center mt-8">
            <Button
              size="lg"
              onClick={() => router.push('/search?premium_only=true')}
              className="bg-bizbook-primary hover:bg-blue-700"
            >
              View All Featured Businesses
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </section>

        {/* Stats Section */}
        <section className="bg-gradient-to-r from-bizbook-primary to-purple-600 text-white rounded-2xl p-12 fade-in">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Why Choose BizBook?</h2>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              The most trusted business directory platform with comprehensive features
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <Shield className="w-12 h-12 text-bizbook-secondary mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">Verified Businesses</h3>
              <p className="text-blue-100">All businesses go through our verification process</p>
            </div>
            
            <div className="text-center">
              <Star className="w-12 h-12 text-bizbook-secondary mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">Authentic Reviews</h3>
              <p className="text-blue-100">Real reviews from verified customers</p>
            </div>
            
            <div className="text-center">
              <Globe className="w-12 h-12 text-bizbook-secondary mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">Local & Global</h3>
              <p className="text-blue-100">Find businesses anywhere, anytime</p>
            </div>
            
            <div className="text-center">
              <Zap className="w-12 h-12 text-bizbook-secondary mx-auto mb-4" />
              <h3 className="text-xl font-bold mb-2">AI-Powered</h3>
              <p className="text-blue-100">Smart recommendations and insights</p>
            </div>
          </div>
        </section>

        {/* Multi-Section Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Events */}
          <section className="fade-in">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Recent Events</h2>
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push('/events')}
              >
                View All
              </Button>
            </div>
            
            <div className="space-y-4">
              {recentEvents.map((event) => (
                <Card key={event.id} className="cursor-pointer card-hover">
                  <CardContent className="p-4">
                    <div className="flex space-x-4">
                      <div className="w-16 h-16 bg-bizbook-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Calendar className="w-8 h-8 text-bizbook-primary" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 mb-1 truncate">
                          {event.title}
                        </h3>
                        <p className="text-sm text-gray-600 mb-2 line-clamp-2">
                          {event.description}
                        </p>
                        <div className="flex items-center text-sm text-gray-500">
                          <Clock className="w-4 h-4 mr-1" />
                          {event.date} at {event.time}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* Featured Products */}
          <section className="fade-in">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Featured Products</h2>
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push('/products')}
              >
                View All
              </Button>
            </div>
            
            <div className="space-y-4">
              {featuredProducts.map((product) => (
                <Card key={product.id} className="cursor-pointer card-hover">
                  <CardContent className="p-4">
                    <div className="flex space-x-4">
                      <div className="w-16 h-16 bg-green-50 rounded-lg flex items-center justify-center flex-shrink-0">
                        <ShoppingBag className="w-8 h-8 text-green-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 mb-1 truncate">
                          {product.name}
                        </h3>
                        <p className="text-lg font-bold text-bizbook-primary mb-1">
                          ${product.price}
                        </p>
                        <p className="text-sm text-gray-500">
                          by {product.business_name}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        </div>

        {/* Coupons & Deals */}
        <section className="fade-in">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Latest Deals & Coupons
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Save money with exclusive deals from local businesses
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {topCoupons.map((coupon) => (
              <Card key={coupon.id} className="cursor-pointer card-hover overflow-hidden">
                <div className="bg-gradient-to-r from-red-500 to-pink-500 text-white p-4">
                  <div className="flex items-center justify-between">
                    <Tag className="w-6 h-6" />
                    <Badge variant="secondary" className="bg-white text-red-600">
                      {coupon.discount_type === 'percentage' ? `${coupon.discount_value}% OFF` : `$${coupon.discount_value} OFF`}
                    </Badge>
                  </div>
                </div>
                <CardContent className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-2 line-clamp-1">
                    {coupon.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {coupon.description}
                  </p>
                  <p className="text-sm font-medium text-bizbook-primary">
                    {coupon.business_name}
                  </p>
                  <p className="text-xs text-gray-500 mt-2">
                    Expires: {new Date(coupon.expiry_date).toLocaleDateString()}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div className="text-center mt-8">
            <Button
              variant="outline"
              size="lg"
              onClick={() => router.push('/coupons')}
              className="border-red-500 text-red-600 hover:bg-red-500 hover:text-white"
            >
              View All Deals
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </section>

        {/* Community Activity */}
        <section className="fade-in">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Community Activity
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              See what our community is saying about local businesses
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {communityActivity.map((activity) => (
              <Card key={activity.id} className="cursor-pointer card-hover">
                <CardContent className="p-4">
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-bizbook-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                      <MessageSquare className="w-5 h-5 text-bizbook-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-2">
                        <p className="font-medium text-gray-900">{activity.user_name}</p>
                        {activity.rating && (
                          <div className="flex items-center">
                            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                            <span className="text-sm text-gray-600">{activity.rating}</span>
                          </div>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 line-clamp-3 mb-2">
                        {activity.content}
                      </p>
                      {activity.business_name && (
                        <p className="text-xs text-bizbook-primary">
                          @ {activity.business_name}
                        </p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          
          <div className="text-center mt-8">
            <Button
              variant="outline"
              size="lg"
              onClick={() => router.push('/community')}
              className="border-purple-500 text-purple-600 hover:bg-purple-500 hover:text-white"
            >
              Join Community
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </section>
      </div>
    </div>
  )
}

export default HomePage