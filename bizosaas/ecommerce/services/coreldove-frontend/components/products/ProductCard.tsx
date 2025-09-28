'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { 
  Heart, 
  ShoppingCart, 
  Eye, 
  Star, 
  Truck,
  Zap,
  Badge as BadgeIcon
} from 'lucide-react'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'
import { Card, CardContent } from '../ui/card'

interface Product {
  id: string
  name: string
  slug?: string
  description: string
  price: number
  originalPrice?: number
  image: string
  images?: { url: string; alt: string }[]
  category: string
  rating: number
  reviews: number
  inStock: boolean
  totalStock?: number
  isNew?: boolean
  isSale?: boolean
  isFeatured?: boolean
  currency?: string
  variants?: Array<{
    id: string
    name: string
    sku: string
    price: number
    quantityAvailable: number
  }>
}

interface ProductCardProps {
  product: Product
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (productId: string) => void
  onQuickView?: (productId: string) => void
  viewMode?: 'grid' | 'list'
  showQuickActions?: boolean
}

export default function ProductCard({
  product,
  onAddToCart,
  onAddToWishlist,
  onQuickView,
  viewMode = 'grid',
  showQuickActions = true
}: ProductCardProps) {
  const [imageError, setImageError] = useState(false)
  const [isHovered, setIsHovered] = useState(false)

  const discountPercentage = product.originalPrice 
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    onAddToCart?.(product)
  }

  const handleAddToWishlist = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    onAddToWishlist?.(product.id)
  }

  const handleQuickView = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    onQuickView?.(product.id)
  }

  const productUrl = `/product/${product.slug || product.id}`

  const renderGridCard = () => (
    <Card 
      className="group hover:shadow-xl transition-all duration-300 border-0 shadow-md overflow-hidden"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Link href={productUrl}>
        <div className="relative overflow-hidden bg-gray-50">
          <div className="aspect-square relative">
            {!imageError && product.image ? (
              <Image
                src={product.image}
                alt={product.name}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
                onError={() => setImageError(true)}
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              />
            ) : (
              <div className="flex items-center justify-center h-full bg-gradient-to-br from-gray-100 to-gray-200">
                <div className="text-6xl">
                  {getProductEmoji(product.category)}
                </div>
              </div>
            )}
            
            {/* Overlay Badges */}
            <div className="absolute top-3 left-3 flex flex-col gap-1">
              {product.isNew && (
                <Badge className="bg-green-500 text-white border-0">
                  <Zap className="h-3 w-3 mr-1" />
                  New
                </Badge>
              )}
              {product.isSale && discountPercentage > 0 && (
                <Badge className="bg-red-500 text-white border-0">
                  -{discountPercentage}%
                </Badge>
              )}
              {product.isFeatured && (
                <Badge className="bg-purple-500 text-white border-0">
                  <BadgeIcon className="h-3 w-3 mr-1" />
                  Featured
                </Badge>
              )}
            </div>

            {/* Quick Actions */}
            {showQuickActions && (
              <div className={`absolute top-3 right-3 flex flex-col gap-2 transition-opacity duration-200 ${
                isHovered ? 'opacity-100' : 'opacity-0'
              }`}>
                <Button
                  size="sm"
                  variant="secondary"
                  className="h-8 w-8 p-0 bg-white/90 hover:bg-white"
                  onClick={handleAddToWishlist}
                >
                  <Heart className="h-4 w-4" />
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  className="h-8 w-8 p-0 bg-white/90 hover:bg-white"
                  onClick={handleQuickView}
                >
                  <Eye className="h-4 w-4" />
                </Button>
              </div>
            )}

            {/* Stock Status */}
            {!product.inStock && (
              <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                <Badge variant="secondary" className="bg-white text-gray-900">
                  Out of Stock
                </Badge>
              </div>
            )}
          </div>
        </div>
      </Link>

      <CardContent className="p-4">
        <Link href={productUrl} className="block">
          <div className="space-y-3">
            {/* Product Category */}
            <div className="flex items-center justify-between">
              <Badge variant="outline" className="text-xs capitalize">
                {product.category}
              </Badge>
              {product.totalStock && product.totalStock < 10 && (
                <Badge variant="destructive" className="text-xs">
                  Only {product.totalStock} left
                </Badge>
              )}
            </div>

            {/* Product Name */}
            <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 text-sm">
              {product.name}
            </h3>

            {/* Description - only show in grid mode */}
            <p className="text-sm text-gray-600 line-clamp-2">
              {product.description}
            </p>
            
            {/* Rating */}
            <div className="flex items-center gap-1">
              <div className="flex text-yellow-400">
                {[...Array(5)].map((_, i) => (
                  <Star 
                    key={i} 
                    className={`h-4 w-4 ${
                      i < Math.floor(product.rating) ? 'fill-current' : 'stroke-current fill-transparent'
                    }`} 
                  />
                ))}
              </div>
              <span className="text-sm text-gray-500 ml-1">
                {product.rating} ({product.reviews})
              </span>
            </div>

            {/* Price */}
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-gray-900">
                ${product.price}
              </span>
              {product.originalPrice && (
                <span className="text-sm text-gray-500 line-through">
                  ${product.originalPrice}
                </span>
              )}
              {discountPercentage > 0 && (
                <span className="text-sm text-green-600 font-medium">
                  Save ${(product.originalPrice! - product.price).toFixed(2)}
                </span>
              )}
            </div>

            {/* Features */}
            <div className="flex items-center gap-4 text-xs text-gray-600">
              <div className="flex items-center gap-1">
                <Truck className="h-3 w-3" />
                <span>Free Shipping</span>
              </div>
              {product.variants && product.variants.length > 1 && (
                <div className="flex items-center gap-1">
                  <BadgeIcon className="h-3 w-3" />
                  <span>{product.variants.length} variants</span>
                </div>
              )}
            </div>
          </div>
        </Link>

        {/* Add to Cart Button */}
        <Button
          onClick={handleAddToCart}
          className="w-full mt-4 bg-blue-600 hover:bg-blue-700"
          disabled={!product.inStock}
        >
          <ShoppingCart className="h-4 w-4 mr-2" />
          {product.inStock ? 'Add to Cart' : 'Out of Stock'}
        </Button>
      </CardContent>
    </Card>
  )

  const renderListCard = () => (
    <Card className="group hover:shadow-lg transition-all duration-300 border-0 shadow-md overflow-hidden">
      <Link href={productUrl}>
        <div className="flex">
          {/* Product Image */}
          <div className="w-48 h-48 relative overflow-hidden bg-gray-50 flex-shrink-0">
            {!imageError && product.image ? (
              <Image
                src={product.image}
                alt={product.name}
                fill
                className="object-cover group-hover:scale-105 transition-transform duration-300"
                onError={() => setImageError(true)}
                sizes="192px"
              />
            ) : (
              <div className="flex items-center justify-center h-full bg-gradient-to-br from-gray-100 to-gray-200">
                <div className="text-4xl">
                  {getProductEmoji(product.category)}
                </div>
              </div>
            )}
            
            {/* Badges */}
            <div className="absolute top-2 left-2 flex flex-col gap-1">
              {product.isNew && (
                <Badge className="bg-green-500 text-white border-0 text-xs">
                  New
                </Badge>
              )}
              {product.isSale && discountPercentage > 0 && (
                <Badge className="bg-red-500 text-white border-0 text-xs">
                  -{discountPercentage}%
                </Badge>
              )}
            </div>
          </div>

          {/* Product Info */}
          <div className="flex-1 p-6">
            <div className="h-full flex flex-col">
              <div className="flex-1">
                <div className="flex items-start justify-between mb-2">
                  <Badge variant="outline" className="text-xs capitalize mb-2">
                    {product.category}
                  </Badge>
                  {showQuickActions && (
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="ghost"
                        className="h-8 w-8 p-0"
                        onClick={handleAddToWishlist}
                      >
                        <Heart className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        className="h-8 w-8 p-0"
                        onClick={handleQuickView}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                    </div>
                  )}
                </div>

                <h3 className="font-semibold text-lg text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 mb-2">
                  {product.name}
                </h3>

                <p className="text-gray-600 line-clamp-3 mb-3">
                  {product.description}
                </p>
                
                {/* Rating */}
                <div className="flex items-center gap-2 mb-3">
                  <div className="flex text-yellow-400">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`h-4 w-4 ${
                          i < Math.floor(product.rating) ? 'fill-current' : 'stroke-current fill-transparent'
                        }`} 
                      />
                    ))}
                  </div>
                  <span className="text-sm text-gray-500">
                    {product.rating} ({product.reviews} reviews)
                  </span>
                </div>

                {/* Features */}
                <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                  <div className="flex items-center gap-1">
                    <Truck className="h-4 w-4" />
                    <span>Free Shipping</span>
                  </div>
                  {product.inStock ? (
                    <div className="flex items-center gap-1 text-green-600">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>In Stock</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-1 text-red-600">
                      <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                      <span>Out of Stock</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Price and Actions */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-xl font-bold text-gray-900">
                    ${product.price}
                  </span>
                  {product.originalPrice && (
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-500 line-through">
                        ${product.originalPrice}
                      </span>
                      <span className="text-sm text-green-600 font-medium">
                        Save ${(product.originalPrice - product.price).toFixed(2)}
                      </span>
                    </div>
                  )}
                </div>

                <Button
                  onClick={handleAddToCart}
                  className="bg-blue-600 hover:bg-blue-700"
                  disabled={!product.inStock}
                >
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  {product.inStock ? 'Add to Cart' : 'Out of Stock'}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Link>
    </Card>
  )

  return viewMode === 'grid' ? renderGridCard() : renderListCard()
}

function getProductEmoji(category: string): string {
  const categoryMap: Record<string, string> = {
    electronics: '🎧',
    furniture: '🪑',
    sports: '💪',
    health: '💧',
    home: '🏠',
    tech: '📱',
    outdoor: '🏕️',
    default: '📦'
  }
  
  return categoryMap[category.toLowerCase()] || categoryMap.default
}