'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'
import { Input } from '../../components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select'
import { 
  Search, 
  Star, 
  ExternalLink, 
  ShoppingCart, 
  Package,
  DollarSign,
  TrendingUp,
  Store,
  User
} from 'lucide-react'

interface AmazonProduct {
  id: string
  name: string
  description: string
  pricing: {
    priceRange: {
      start: {
        gross: {
          amount: number
          currency: string
        }
      }
    }
  }
  thumbnail: {
    url: string
  }
  category: {
    name: string
  }
  rating: number
  reviews: number
  brand: string
  brand_url?: string
  availability: string
  amazonUrl: string
  seller_name?: string
  seller_url?: string
  seller_rating?: number
  seller_review_count?: number
  source: string
}

interface SourcingFilters {
  query: string
  category: string
  priceRange: {
    min?: number
    max?: number
  }
}

export default function AmazonSourcingSection() {
  const [products, setProducts] = useState<AmazonProduct[]>([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState<SourcingFilters>({
    query: 'fitness equipment',
    category: 'fitness',
    priceRange: {}
  })

  const categories = [
    { value: 'fitness', label: 'Fitness & Sports' },
    { value: 'yoga', label: 'Yoga & Wellness' },
    { value: 'electronics', label: 'Electronics' },
    { value: 'home', label: 'Home & Garden' },
    { value: 'fashion', label: 'Fashion' },
    { value: 'books', label: 'Books' },
    { value: 'health', label: 'Health & Beauty' }
  ]

  const searchProducts = async () => {
    try {
      setLoading(true)
      console.log('🔍 Searching Amazon products with filters:', filters)
      
      const queryParams = new URLSearchParams({
        query: filters.query,
        ...(filters.category && { category: filters.category }),
        ...(filters.priceRange.min && { min_price: filters.priceRange.min.toString() }),
        ...(filters.priceRange.max && { max_price: filters.priceRange.max.toString() }),
        limit: '6'
      })

      const response = await fetch(`/api/sourcing?${queryParams}`)
      const data = await response.json()
      
      if (data.products && Array.isArray(data.products)) {
        console.log('✅ Found products:', data.products.length, 'items')
        setProducts(data.products)
      } else {
        console.warn('⚠️ No products found or API error:', data)
        setProducts([])
      }
    } catch (error) {
      console.error('❌ Error searching products:', error)
      setProducts([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    console.log('🚀 Component mounted, starting initial search...')
    searchProducts()
  }, [])

  const formatPrice = (amount: number, currency: string) => {
    if (currency === 'INR') {
      return `₹${amount.toLocaleString('en-IN')}`
    }
    return `${currency} ${amount}`
  }

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        size={14}
        className={i < Math.floor(rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}
      />
    ))
  }

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 rounded-lg p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 bg-blue-600 rounded-lg">
            <TrendingUp className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Amazon Product Sourcing
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Source products directly from Amazon India with live pricing, seller info, and reviews
            </p>
          </div>
        </div>
        
        {/* Search Filters */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="md:col-span-2">
            <Input
              placeholder="Search products (e.g., yoga mat, resistance bands)"
              value={filters.query}
              onChange={(e) => setFilters({ ...filters, query: e.target.value })}
              className="w-full"
            />
          </div>
          <Select
            value={filters.category}
            onValueChange={(value) => setFilters({ ...filters, category: value })}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select category" />
            </SelectTrigger>
            <SelectContent>
              {categories.map((cat) => (
                <SelectItem key={cat.value} value={cat.value}>
                  {cat.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button onClick={searchProducts} disabled={loading} className="w-full">
            <Search className="h-4 w-4 mr-2" />
            {loading ? 'Searching...' : 'Search Products'}
          </Button>
        </div>

        {/* Price Range Filters */}
        <div className="grid grid-cols-2 gap-4 mt-4">
          <Input
            type="number"
            placeholder="Min price (₹)"
            value={filters.priceRange.min || ''}
            onChange={(e) => setFilters({
              ...filters,
              priceRange: { ...filters.priceRange, min: e.target.value ? parseInt(e.target.value) : undefined }
            })}
          />
          <Input
            type="number"
            placeholder="Max price (₹)"
            value={filters.priceRange.max || ''}
            onChange={(e) => setFilters({
              ...filters,
              priceRange: { ...filters.priceRange, max: e.target.value ? parseInt(e.target.value) : undefined }
            })}
          />
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300">Sourcing products from Amazon India...</p>
        </div>
      )}

      {/* Products Grid */}
      {!loading && products.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <Card key={product.id} className="group hover:shadow-lg transition-shadow duration-300">
              <CardHeader className="p-0">
                <div className="relative overflow-hidden rounded-t-lg">
                  <Image
                    src={product.thumbnail.url || '/placeholder-product.jpg'}
                    alt={product.name}
                    width={400}
                    height={300}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement
                      target.src = '/placeholder-product.jpg'
                    }}
                  />
                  <div className="absolute top-2 right-2">
                    <Badge variant="secondary" className="bg-green-100 text-green-800">
                      {product.availability}
                    </Badge>
                  </div>
                  <div className="absolute top-2 left-2">
                    <Badge variant="outline" className="bg-white/90">
                      ASIN: {product.id}
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent className="p-4">
                <div className="space-y-3">
                  {/* Product Title */}
                  <h3 className="font-semibold text-lg leading-tight line-clamp-2 group-hover:text-blue-600 transition-colors">
                    {product.name}
                  </h3>
                  
                  {/* Brand */}
                  {product.brand && (
                    <div className="flex items-center gap-1">
                      <Store className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-600 dark:text-gray-300">
                        Brand: 
                        {product.brand_url ? (
                          <a 
                            href={product.brand_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="font-medium text-blue-600 hover:text-blue-800 ml-1"
                          >
                            {product.brand}
                          </a>
                        ) : (
                          <span className="font-medium ml-1">{product.brand}</span>
                        )}
                      </span>
                    </div>
                  )}
                  
                  {/* Product Rating & Reviews */}
                  <div className="flex items-center gap-2">
                    <div className="flex">{renderStars(product.rating)}</div>
                    <span className="text-sm text-gray-600 dark:text-gray-300">
                      {product.rating}/5 ({product.reviews.toLocaleString()} reviews)
                    </span>
                  </div>

                  {/* Seller Information */}
                  {product.seller_name && (
                    <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 border">
                      <div className="flex items-center gap-2 mb-2">
                        <User className="h-4 w-4 text-gray-500" />
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                          Sold by:
                          {product.seller_url ? (
                            <a 
                              href={product.seller_url} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:text-blue-800 ml-1"
                            >
                              {product.seller_name}
                            </a>
                          ) : (
                            <span className="ml-1">{product.seller_name}</span>
                          )}
                        </span>
                      </div>
                      {product.seller_rating && (
                        <div className="flex items-center gap-2">
                          <div className="flex">{renderStars(product.seller_rating)}</div>
                          <span className="text-xs text-gray-600 dark:text-gray-400">
                            {product.seller_rating}/5 ({product.seller_review_count?.toLocaleString()} seller reviews)
                          </span>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* Price */}
                  <div className="flex items-center justify-between">
                    <div className="text-2xl font-bold text-green-600">
                      {formatPrice(product.pricing.priceRange.start.gross.amount, product.pricing.priceRange.start.gross.currency)}
                    </div>
                    <Badge variant="outline" className="text-xs">
                      {product.category.name}
                    </Badge>
                  </div>
                  
                  {/* Description/Features */}
                  {product.description && (
                    <div className="text-sm text-gray-600 dark:text-gray-300">
                      <p className="line-clamp-2">{product.description}</p>
                    </div>
                  )}
                  
                  {/* Action Buttons */}
                  <div className="flex gap-2 pt-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex-1"
                      onClick={() => window.open(product.amazonUrl, '_blank')}
                    >
                      <ExternalLink className="h-4 w-4 mr-1" />
                      View on Amazon
                    </Button>
                    <Button
                      size="sm"
                      className="flex-1"
                      onClick={() => {
                        console.log('Adding to sourcing list:', product.id)
                        alert(`Product ${product.name} added to sourcing queue for import!`)
                      }}
                    >
                      <Package className="h-4 w-4 mr-1" />
                      Source Product
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* No Results */}
      {!loading && products.length === 0 && (
        <div className="text-center py-12">
          <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            No Products Found
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Try adjusting your search terms or category filter
          </p>
          <Button onClick={searchProducts} variant="outline">
            <Search className="h-4 w-4 mr-2" />
            Search Again
          </Button>
        </div>
      )}
    </div>
  )
}