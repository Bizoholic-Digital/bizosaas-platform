"use client"

import { useEffect, useState } from "react"
import { useParams, useRouter, notFound } from "next/navigation"
import Image from "next/image"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"

import { ProductImageGallery } from "@/components/product/product-image-gallery"
import { ProductVariantSelector } from "@/components/product/product-variant-selector"
import { ProductQuantityControl } from "@/components/product/product-quantity-control"
import { ProductReviews } from "@/components/product/product-reviews"
import { RelatedProducts } from "@/components/product/related-products"
import { ProductShareButtons } from "@/components/product/product-share-buttons"
import { AddToCartButton } from "@/components/product/add-to-cart-button"

import { saleorAPI, SaleorProduct, SaleorProductVariant } from "@/lib/saleor-api"
import { usePlatform } from "@/lib/platform-config"
import { cn } from "@/lib/utils"

import {
  Star,
  Heart,
  ShoppingCart,
  Truck,
  Shield,
  RotateCcw,
  CheckCircle,
  AlertCircle,
  Share2,
  ChevronLeft,
  ChevronRight
} from "lucide-react"

interface ProductDetailClientProps {
  initialProduct: SaleorProduct
  slug: string
}

export function ProductDetailClient({ initialProduct, slug }: ProductDetailClientProps) {
  const { config } = usePlatform()
  
  const [product, setProduct] = useState<SaleorProduct>(initialProduct)
  const [selectedVariant, setSelectedVariant] = useState<SaleorProductVariant | null>(
    initialProduct.variants && initialProduct.variants.length > 0 ? initialProduct.variants[0] : null
  )
  const [quantity, setQuantity] = useState(1)
  const [wishlist, setWishlist] = useState(false)

  // Get current price from selected variant
  const currentPrice = selectedVariant?.pricing?.price?.gross.amount || 0
  const currency = selectedVariant?.pricing?.price?.gross.currency || 'USD'
  
  // Calculate savings and profit info
  const originalPrice = product.metadata?.find(m => m.key === 'amazon_price')?.value ? Number(product.metadata.find(m => m.key === 'amazon_price')?.value) : null
  const savings = originalPrice && currentPrice ? originalPrice - currentPrice : 0
  const savingsPercentage = originalPrice && currentPrice ? Math.round((savings / originalPrice) * 100) : 0
  
  // Stock status
  const stockQuantity = selectedVariant?.quantityAvailable || 0
  const inStock = stockQuantity > 0
  const lowStock = stockQuantity > 0 && stockQuantity <= 10

  // Rating data
  const rating = product.metadata?.find(m => m.key === 'amazon_rating')?.value ? Number(product.metadata.find(m => m.key === 'amazon_rating')?.value) : 4.5
  const reviewCount = product.metadata?.find(m => m.key === 'amazon_reviews')?.value ? Number(product.metadata.find(m => m.key === 'amazon_reviews')?.value) : 0

  // Handle add to cart
  const handleAddToCart = async () => {
    if (!selectedVariant) return
    
    try {
      // This would integrate with your cart system
      console.log('Adding to cart:', {
        productId: product.id,
        variantId: selectedVariant.id,
        quantity
      })
      // Show success message or redirect to cart
    } catch (error) {
      console.error('Failed to add to cart:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950/20 dark:to-orange-950/20">
      <div className="container mx-auto px-4 py-8">
        {/* Breadcrumb Navigation */}
        <Breadcrumb className="mb-8">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink href="/" className="text-red-600 hover:text-red-700">Home</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbLink href="/products" className="text-red-600 hover:text-red-700">Products</BreadcrumbLink>
            </BreadcrumbItem>
            {product.category && (
              <>
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  <BreadcrumbLink href={`/categories/${product.category.slug}`} className="text-red-600 hover:text-red-700">
                    {product.category.name}
                  </BreadcrumbLink>
                </BreadcrumbItem>
              </>
            )}
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage className="text-gray-500">{product.name}</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Product Images */}
          <div className="space-y-4">
            <ProductImageGallery
              images={product.media || []}
              alt={product.name}
              className="aspect-square"
            />
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            {/* Title and Brand */}
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                {product.name}
              </h1>
            </div>

            {/* Rating and Reviews */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={cn(
                      "h-5 w-5",
                      i < Math.floor(rating) ? "text-yellow-400 fill-current" : "text-gray-300"
                    )}
                  />
                ))}
                <span className="text-sm font-medium ml-1">{rating}</span>
              </div>
              {reviewCount > 0 && (
                <span className="text-sm text-gray-500">({reviewCount.toLocaleString()} reviews)</span>
              )}
            </div>

            {/* Price */}
            <div className="space-y-2">
              <div className="flex items-center gap-4">
                <span className="text-3xl font-bold text-red-600">
                  ${currentPrice.toFixed(2)}
                </span>
                {originalPrice && savings > 0 && (
                  <>
                    <span className="text-lg text-gray-500 line-through">
                      ${originalPrice.toFixed(2)}
                    </span>
                    <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100">
                      Save {savingsPercentage}%
                    </Badge>
                  </>
                )}
              </div>
              {savings > 0 && (
                <p className="text-sm text-green-600">You save ${savings.toFixed(2)}</p>
              )}
            </div>

            {/* Stock Status */}
            <div className="flex items-center gap-2">
              {inStock ? (
                <>
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <span className="text-green-600 font-medium">
                    {lowStock ? `Only ${stockQuantity} left in stock` : 'In Stock'}
                  </span>
                </>
              ) : (
                <>
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <span className="text-red-600 font-medium">Out of Stock</span>
                </>
              )}
            </div>

            {/* Product Description */}
            {product.description && (
              <div>
                <h3 className="text-lg font-semibold mb-2">Description</h3>
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                  {product.description}
                </p>
              </div>
            )}

            {/* Variant Selection */}
            {product.variants && product.variants.length > 1 && (
              <ProductVariantSelector
                variants={product.variants}
                selectedVariant={selectedVariant}
                onVariantChange={setSelectedVariant}
                options={product.attributes || []}
              />
            )}

            {/* Quantity and Add to Cart */}
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <ProductQuantityControl
                  quantity={quantity}
                  onQuantityChange={setQuantity}
                  maxQuantity={stockQuantity}
                  disabled={!inStock}
                />
                <Button
                  onClick={() => setWishlist(!wishlist)}
                  variant="outline"
                  size="icon"
                  className="border-red-200 hover:border-red-300"
                >
                  <Heart className={cn("h-5 w-5", wishlist && "fill-red-500 text-red-500")} />
                </Button>
              </div>

              <div className="flex gap-3">
                <AddToCartButton
                  product={product}
                  variant={selectedVariant}
                  quantity={quantity}
                  disabled={!inStock}
                  className="flex-1"
                />
                <Button variant="outline" className="border-red-200 hover:border-red-300">
                  <ShoppingCart className="h-5 w-5 mr-2" />
                  Buy Now
                </Button>
              </div>
            </div>

            {/* Trust Badges */}
            <div className="grid grid-cols-3 gap-4 pt-6 border-t border-gray-200 dark:border-gray-700">
              <div className="text-center">
                <Truck className="h-6 w-6 text-red-600 mx-auto mb-2" />
                <p className="text-sm font-medium">Free Shipping</p>
                <p className="text-xs text-gray-500">On orders over $50</p>
              </div>
              <div className="text-center">
                <Shield className="h-6 w-6 text-red-600 mx-auto mb-2" />
                <p className="text-sm font-medium">Secure Payment</p>
                <p className="text-xs text-gray-500">SSL protected</p>
              </div>
              <div className="text-center">
                <RotateCcw className="h-6 w-6 text-red-600 mx-auto mb-2" />
                <p className="text-sm font-medium">Easy Returns</p>
                <p className="text-xs text-gray-500">30-day policy</p>
              </div>
            </div>

            {/* Share Buttons */}
            <ProductShareButtons
              product={product}
              currentUrl={`${process.env.NEXT_PUBLIC_BASE_URL}/products/${slug}`}
            />
          </div>
        </div>

        {/* Product Tabs/Additional Information */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle>Product Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {selectedVariant && (
                <div>
                  <h4 className="font-semibold mb-3">Specifications</h4>
                  <dl className="space-y-2 text-sm">
                    {selectedVariant.sku && (
                      <div className="flex justify-between">
                        <dt className="text-gray-500">SKU:</dt>
                        <dd className="font-medium">{selectedVariant.sku}</dd>
                      </div>
                    )}
                    {selectedVariant.weight && (
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Weight:</dt>
                        <dd className="font-medium">{selectedVariant.weight.value} {selectedVariant.weight.unit}</dd>
                      </div>
                    )}
                  </dl>
                </div>
              )}
              
            </div>
          </CardContent>
        </Card>

        {/* Reviews Section */}
        <ProductReviews
          productId={product.id!}
          rating={rating}
          reviewCount={reviewCount}
          className="mb-12"
        />

        {/* Related Products */}
        <RelatedProducts
          currentProduct={product}
          categoryId={product.category?.id}
          className="mb-8"
        />
      </div>
    </div>
  )
}