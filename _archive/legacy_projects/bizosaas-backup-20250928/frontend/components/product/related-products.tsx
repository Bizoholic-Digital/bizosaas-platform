"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Star, ChevronLeft, ChevronRight } from "lucide-react"
import { cn } from "@/lib/utils"
import { saleorAPI, SaleorProduct } from "@/lib/saleor-api"

function ProductCard({ product }: { product: SaleorProduct }) {
  const rating = 4.2 // Mock rating since SaleorProduct doesn't have rating

  return (
    <Card className="group hover:shadow-lg transition-all duration-200 border border-gray-200 dark:border-gray-700">
      <div className="aspect-square bg-gray-50 dark:bg-gray-800 rounded-t-lg relative overflow-hidden">
        {product.thumbnail?.url ? (
          <Image
            src={product.thumbnail.url}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            No image
          </div>
        )}
        
        {/* Quick actions overlay */}
        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-200" />
      </div>
      
      <CardContent className="p-4 space-y-3">
        <div>
          <Link 
            href={`/products/${product.slug || product.id}`}
            className="font-medium text-gray-900 dark:text-white hover:text-red-600 transition-colors line-clamp-2"
          >
            {product.name}
          </Link>
          
        </div>
        
        {/* Rating */}
        {rating > 0 && (
          <div className="flex items-center gap-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={cn(
                    "h-3 w-3",
                    i < Math.floor(rating)
                      ? "fill-yellow-400 text-yellow-400"
                      : "text-gray-300 dark:text-gray-600"
                  )}
                />
              ))}
            </div>
            <span className="text-sm text-gray-500">{rating}</span>
          </div>
        )}
        
        {/* Pricing */}
        <div className="flex items-center justify-between">
          {product.defaultVariant?.pricing?.price ? (
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg text-red-600">
                ${product.defaultVariant.pricing.price.gross.amount}
              </span>
            </div>
          ) : (
            <span className="text-sm text-gray-500">Price not available</span>
          )}
          
          <Button size="sm" variant="outline">
            View
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

interface RelatedProductsProps {
  currentProduct: SaleorProduct
  categoryId?: string
  className?: string
  limit?: number
}

export function RelatedProducts({ 
  currentProduct, 
  categoryId, 
  className, 
  limit = 8 
}: RelatedProductsProps) {
  const [relatedProducts, setRelatedProducts] = useState<SaleorProduct[]>([])
  const [loading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(0)
  
  const productsPerPage = 4
  const totalPages = Math.ceil(relatedProducts.length / productsPerPage)
  
  useEffect(() => {
    const fetchRelatedProducts = async () => {
      try {
        setLoading(true)
        
        // Simplified - just get some products (in a real implementation this would be smarter)
        const response = await saleorAPI.getProducts({
          first: limit * 2
        })
        
        if (response.products?.edges) {
          // Filter out current product and limit results
          const filtered = response.products.edges
            .map(edge => edge.node)
            .filter(p => p.id !== currentProduct.id)
            .slice(0, limit)
          
          setRelatedProducts(filtered)
        }
      } catch (error) {
        console.error('Failed to fetch related products:', error)
        // Use mock data on error
        setRelatedProducts([])
      } finally {
        setLoading(false)
      }
    }
    
    fetchRelatedProducts()
  }, [currentProduct.id, limit])

  if (loading) {
    return (
      <div className={cn("space-y-6", className)}>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">You might also like</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="aspect-square bg-gray-200 dark:bg-gray-700 rounded-lg mb-4" />
              <div className="space-y-2">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded" />
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4" />
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (relatedProducts.length === 0) {
    return null
  }

  const visibleProducts = relatedProducts.slice(
    currentPage * productsPerPage,
    (currentPage + 1) * productsPerPage
  )

  return (
    <div className={cn("space-y-6", className)}>
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">You might also like</h2>
        
        {totalPages > 1 && (
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage(prev => Math.max(0, prev - 1))}
              disabled={currentPage === 0}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <span className="text-sm text-gray-500">
              {currentPage + 1} / {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setCurrentPage(prev => Math.min(totalPages - 1, prev + 1))}
              disabled={currentPage === totalPages - 1}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {visibleProducts.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  )
}