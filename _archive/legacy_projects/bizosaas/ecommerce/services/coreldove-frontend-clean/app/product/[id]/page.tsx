'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { 
  ArrowLeft,
  Star,
  Heart,
  ShoppingCart,
  Truck,
  Shield,
  RefreshCw,
  Plus,
  Minus,
  ChevronRight,
  MessageCircle,
  ThumbsUp,
  Share2,
  Loader2
} from 'lucide-react'
import NavigationHeader from '../../../components/layout/NavigationHeader'
import { Button } from '../../../components/ui/button'
import { Badge } from '../../../components/ui/badge'
import useCartStore from '../../../lib/stores/cartStore'

interface Product {
  id: string
  name: string
  description: string
  price: number
  originalPrice?: number
  images: string[]
  category: string
  rating: number
  reviews: Review[]
  inStock: boolean
  stockQuantity: number
  specifications: Record<string, string>
  features: string[]
  isNew?: boolean
  isSale?: boolean
}

interface Review {
  id: string
  userName: string
  rating: number
  comment: string
  date: string
  verified: boolean
  helpful: number
}

export default function ProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState<Product | null>(null)
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)
  const [quantity, setQuantity] = useState(1)
  const [activeTab, setActiveTab] = useState<'description' | 'specifications' | 'reviews'>('description')
  const [loading, setLoading] = useState(true)
  const [isWishlisted, setIsWishlisted] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<any>(null)
  const { addItem, getTotalItems } = useCartStore()

  // Load product data from API
  useEffect(() => {
    const loadProduct = async () => {
      try {
        setLoading(true)
        const response = await fetch(`/api/products/${params.id}`)
        if (response.ok) {
          const productData = await response.json()
          
          // Transform API data to match our Product interface
          const transformedProduct: Product = {
            id: productData.id,
            name: productData.name,
            description: productData.description || `Premium ${productData.name} with exceptional quality and performance. This product combines cutting-edge technology with elegant design to deliver an outstanding user experience.\n\nPerfect for those who demand the best quality and reliability. Every detail has been carefully crafted to ensure maximum satisfaction and long-lasting performance.\n\nBacked by our quality guarantee and excellent customer service, this product represents exceptional value for money.`,
            price: productData.price,
            originalPrice: productData.originalPrice,
            images: productData.images?.map((img: any) => img.url) || [productData.image],
            category: productData.category,
            rating: productData.rating || 4.5,
            stockQuantity: productData.totalStock || 50,
            inStock: productData.inStock,
            isNew: productData.isNew,
            isSale: productData.isSale,
            specifications: {
              'Category': productData.category?.charAt(0).toUpperCase() + productData.category?.slice(1) || 'General',
              'Availability': productData.inStock ? 'In Stock' : 'Out of Stock',
              'Currency': productData.currency || 'USD',
              'SKU': productData.variants?.[0]?.sku || 'N/A',
              'Stock Quantity': String(productData.totalStock || 0),
              'Variants': String(productData.variants?.length || 1)
            },
            features: [
              'Premium Quality Materials',
              'Exceptional Performance',
              'Modern Design',
              'Easy to Use',
              'Durable Construction',
              'Money Back Guarantee',
              'Fast Shipping',
              'Customer Support'
            ],
            reviews: [
              {
                id: '1',
                userName: 'Sarah M.',
                rating: 5,
                comment: 'Excellent product! Exactly as described and arrived quickly. Very satisfied with my purchase.',
                date: '2025-01-05',
                verified: true,
                helpful: 12
              },
              {
                id: '2',
                userName: 'Mike R.',
                rating: 4,
                comment: 'Good quality and fair price. Would recommend to others.',
                date: '2025-01-03',
                verified: true,
                helpful: 8
              },
              {
                id: '3',
                userName: 'Emma L.',
                rating: 5,
                comment: 'Love it! Great value for money and fast delivery.',
                date: '2025-01-01',
                verified: true,
                helpful: 6
              }
            ]
          }
          
          setProduct(transformedProduct)
        } else {
          throw new Error('Product not found')
        }
      } catch (error) {
        console.error('Failed to load product:', error)
        setProduct(null)
      } finally {
        setLoading(false)
      }
    }

    loadProduct()
  }, [params.id])

  const addToCart = () => {
    if (product) {
      addItem({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.images?.[0] || '/placeholder-product.jpg',
        quantity: quantity,
        maxQuantity: product.stockQuantity
      })
      console.log(`Added ${quantity}x ${product.name} to cart`)
    }
  }

  const handleAuthAction = () => {
    if (isAuthenticated) {
      setIsAuthenticated(false)
      setUser(null)
    } else {
      window.location.href = '/auth/login'
    }
  }

  const toggleWishlist = () => {
    setIsWishlisted(!isWishlisted)
    console.log(`${isWishlisted ? 'Removed from' : 'Added to'} wishlist`)
  }

  const shareProduct = () => {
    if (navigator.share) {
      navigator.share({
        title: product?.name,
        text: product?.description,
        url: window.location.href,
      })
    } else {
      navigator.clipboard.writeText(window.location.href)
      console.log('Product URL copied to clipboard')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <NavigationHeader
          cartCount={getTotalItems()}
          isAuthenticated={isAuthenticated}
          user={user}
          onAuthAction={handleAuthAction}
        />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-blue-600" />
            <p className="text-gray-600">Loading product...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50">
        <NavigationHeader
          cartCount={getTotalItems()}
          isAuthenticated={isAuthenticated}
          user={user}
          onAuthAction={handleAuthAction}
        />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Product Not Found</h2>
            <p className="text-gray-600 mb-6">The product you're looking for doesn't exist.</p>
            <Button asChild>
              <Link href="/catalog">Browse Products</Link>
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <NavigationHeader
        cartCount={getTotalItems()}
        isAuthenticated={isAuthenticated}
        user={user}
        onAuthAction={handleAuthAction}
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm text-gray-600 mb-8">
          <Link href="/" className="hover:text-gray-900">Home</Link>
          <ChevronRight className="w-4 h-4" />
          <Link href="/catalog" className="hover:text-gray-900">Products</Link>
          <ChevronRight className="w-4 h-4" />
          <span className="text-gray-900 capitalize">{product.category}</span>
          <ChevronRight className="w-4 h-4" />
          <span className="text-gray-900 truncate">{product.name}</span>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Product Images */}
          <div>
            <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden mb-4">
              <div className="flex items-center justify-center h-full text-8xl bg-gradient-to-br from-gray-50 to-gray-100">
                🎧
              </div>
            </div>
            
            {/* Image Thumbnails */}
            <div className="grid grid-cols-4 gap-2">
              {[0, 1, 2, 3].map((index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImageIndex(index)}
                  className={`aspect-square bg-gray-100 rounded-lg overflow-hidden border-2 ${
                    selectedImageIndex === index ? 'border-red-600' : 'border-gray-200'
                  }`}
                >
                  <div className="flex items-center justify-center h-full text-2xl bg-gradient-to-br from-gray-50 to-gray-100">
                    🎧
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Product Info */}
          <div>
            {/* Badges */}
            <div className="flex gap-2 mb-4">
              {product.isNew && (
                <Badge className="bg-green-500 text-white border-0">
                  New Arrival
                </Badge>
              )}
              {product.isSale && (
                <Badge className="bg-red-500 text-white border-0">
                  Sale
                </Badge>
              )}
              {product.originalPrice && (
                <Badge className="bg-orange-500 text-white border-0">
                  {Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)}% OFF
                </Badge>
              )}
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-4">{product.name}</h1>

            {/* Rating */}
            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center gap-1">
                <div className="flex text-yellow-400">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className={`w-5 h-5 ${i < Math.floor(product.rating) ? 'fill-current' : ''}`} />
                  ))}
                </div>
                <span className="text-lg font-medium text-gray-900 ml-2">{product.rating}</span>
              </div>
              <span className="text-gray-600">({product.reviews.length} reviews)</span>
            </div>

            {/* Price */}
            <div className="flex items-center gap-4 mb-6">
              <span className="text-3xl font-bold text-gray-900">${product.price}</span>
              {product.originalPrice && (
                <>
                  <span className="text-xl text-gray-500 line-through">${product.originalPrice}</span>
                  <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm font-medium">
                    Save ${(product.originalPrice - product.price).toFixed(2)}
                  </span>
                </>
              )}
            </div>

            {/* Stock Status */}
            <div className="flex items-center gap-2 mb-6">
              <div className={`w-3 h-3 rounded-full ${product.inStock ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className={`font-medium ${product.inStock ? 'text-green-700' : 'text-red-700'}`}>
                {product.inStock 
                  ? `In Stock (${product.stockQuantity} available)` 
                  : 'Out of Stock'
                }
              </span>
            </div>

            {/* Quantity Selector */}
            <div className="flex items-center gap-4 mb-6">
              <span className="font-medium text-gray-900">Quantity:</span>
              <div className="flex items-center border border-gray-300 rounded-lg">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2 hover:bg-gray-100 transition-colors"
                  disabled={quantity <= 1}
                >
                  <Minus className="w-4 h-4" />
                </button>
                <span className="px-4 py-2 min-w-[3rem] text-center">{quantity}</span>
                <button
                  onClick={() => setQuantity(Math.min(product.stockQuantity, quantity + 1))}
                  className="p-2 hover:bg-gray-100 transition-colors"
                  disabled={quantity >= product.stockQuantity}
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Add to Cart & Wishlist */}
            <div className="flex gap-4 mb-8">
              <Button
                onClick={addToCart}
                disabled={!product.inStock}
                className="flex-1 bg-blue-600 hover:bg-blue-700 py-6 text-lg"
                size="lg"
              >
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart
              </Button>
              <Button
                onClick={toggleWishlist}
                variant={isWishlisted ? "default" : "outline"}
                className={`p-6 ${isWishlisted ? 'bg-red-500 hover:bg-red-600' : 'hover:bg-red-50 hover:text-red-600 hover:border-red-600'}`}
                size="lg"
              >
                <Heart className={`w-5 h-5 ${isWishlisted ? 'fill-current' : ''}`} />
              </Button>
              <Button
                onClick={shareProduct}
                variant="outline"
                className="p-6 hover:bg-gray-50"
                size="lg"
              >
                <Share2 className="w-5 h-5" />
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="grid grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="text-center">
                <Truck className="w-6 h-6 text-red-600 mx-auto mb-2" />
                <p className="text-xs font-medium text-gray-900">Free Shipping</p>
                <p className="text-xs text-gray-600">Orders over $50</p>
              </div>
              <div className="text-center">
                <RefreshCw className="w-6 h-6 text-red-600 mx-auto mb-2" />
                <p className="text-xs font-medium text-gray-900">30-Day Returns</p>
                <p className="text-xs text-gray-600">Money back guarantee</p>
              </div>
              <div className="text-center">
                <Shield className="w-6 h-6 text-red-600 mx-auto mb-2" />
                <p className="text-xs font-medium text-gray-900">Warranty</p>
                <p className="text-xs text-gray-600">1 year coverage</p>
              </div>
            </div>
          </div>
        </div>

        {/* Product Details Tabs */}
        <div className="bg-white rounded-lg shadow-sm border">
          {/* Tab Navigation */}
          <div className="border-b border-gray-200">
            <nav className="flex">
              <button
                onClick={() => setActiveTab('description')}
                className={`py-4 px-6 font-medium text-sm border-b-2 ${
                  activeTab === 'description'
                    ? 'border-red-600 text-red-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                Description
              </button>
              <button
                onClick={() => setActiveTab('specifications')}
                className={`py-4 px-6 font-medium text-sm border-b-2 ${
                  activeTab === 'specifications'
                    ? 'border-red-600 text-red-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                Specifications
              </button>
              <button
                onClick={() => setActiveTab('reviews')}
                className={`py-4 px-6 font-medium text-sm border-b-2 ${
                  activeTab === 'reviews'
                    ? 'border-red-600 text-red-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                Reviews ({product.reviews.length})
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'description' && (
              <div>
                <div className="prose prose-gray max-w-none mb-8">
                  {product.description.split('\n\n').map((paragraph, index) => (
                    <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                      {paragraph}
                    </p>
                  ))}
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Features</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {product.features.map((feature, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-red-600 rounded-full"></div>
                      <span className="text-gray-700">{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'specifications' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Technical Specifications</h3>
                <div className="grid grid-cols-1 gap-4">
                  {Object.entries(product.specifications).map(([key, value]) => (
                    <div key={key} className="flex flex-col sm:flex-row sm:justify-between py-3 border-b border-gray-100">
                      <span className="font-medium text-gray-900">{key}</span>
                      <span className="text-gray-700">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'reviews' && (
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">Customer Reviews</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex text-yellow-400">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={`w-4 h-4 ${i < Math.floor(product.rating) ? 'fill-current' : ''}`} />
                        ))}
                      </div>
                      <span className="text-sm text-gray-600">
                        {product.rating} out of 5 based on {product.reviews.length} reviews
                      </span>
                    </div>
                  </div>
                  <Button className="bg-blue-600 hover:bg-blue-700">
                    Write a Review
                  </Button>
                </div>

                <div className="space-y-6">
                  {product.reviews.map((review) => (
                    <div key={review.id} className="border-b border-gray-100 pb-6">
                      <div className="flex items-start gap-4">
                        <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                          <span className="font-medium text-gray-600">{review.userName[0]}</span>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="font-medium text-gray-900">{review.userName}</span>
                            {review.verified && (
                              <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
                                Verified Purchase
                              </span>
                            )}
                            <span className="text-sm text-gray-500">{review.date}</span>
                          </div>
                          <div className="flex text-yellow-400 mb-3">
                            {[...Array(5)].map((_, i) => (
                              <Star key={i} className={`w-4 h-4 ${i < review.rating ? 'fill-current' : ''}`} />
                            ))}
                          </div>
                          <p className="text-gray-700 mb-3">{review.comment}</p>
                          <div className="flex items-center gap-4 text-sm">
                            <button className="flex items-center gap-1 text-gray-600 hover:text-gray-900">
                              <ThumbsUp className="w-4 h-4" />
                              <span>Helpful ({review.helpful})</span>
                            </button>
                            <button className="flex items-center gap-1 text-gray-600 hover:text-gray-900">
                              <MessageCircle className="w-4 h-4" />
                              <span>Reply</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}