"use client"

import { useState, useEffect, Suspense } from "react"

// Disable static generation for this page as it uses search params and external API
export const dynamic = 'force-dynamic'
import Link from "next/link"
import Image from "next/image"
import { useSearchParams } from "next/navigation"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"

import { saleorAPI, SaleorProduct } from "@/lib/saleor-api"
import { usePlatform } from "@/lib/platform-config"
import { cn } from "@/lib/utils"

import {
  Search,
  SlidersHorizontal,
  Star,
  ShoppingCart,
  Grid3X3,
  List,
  ChevronDown,
  Filter,
  X
} from "lucide-react"

interface ProductFilters {
  search: string
  category: string
  priceRange: string
  rating: string
  sortBy: string
  layout: 'grid' | 'list'
}

function ProductCard({ product, layout = 'grid' }: { product: SaleorProduct; layout?: 'grid' | 'list' }) {
  const price = product.variants?.[0]?.pricing?.price?.gross.amount || 0
  const originalPrice = product.metadata?.find(m => m.key === 'amazon_price')?.value ? Number(product.metadata.find(m => m.key === 'amazon_price')?.value) : null
  const rating = product.metadata?.find(m => m.key === 'amazon_rating')?.value ? Number(product.metadata.find(m => m.key === 'amazon_rating')?.value) : 4.5
  const reviewCount = product.metadata?.find(m => m.key === 'amazon_reviews')?.value ? Number(product.metadata.find(m => m.key === 'amazon_reviews')?.value) : 0
  
  const savings = originalPrice && price ? originalPrice - price : 0
  const savingsPercentage = originalPrice && price ? Math.round((savings / originalPrice) * 100) : 0
  const inStock = product.variants?.[0]?.quantityAvailable ? product.variants[0].quantityAvailable > 0 : true
  
  if (layout === 'list') {
    return (
      <Card className="hover:shadow-md transition-shadow duration-200">
        <CardContent className="p-6">
          <div className="flex gap-6">
            <Link href={`/products/${product.slug || product.id}`} className="flex-shrink-0">
              <div className="relative w-32 h-32 bg-gray-100 rounded-lg overflow-hidden">
                <Image
                  src={product.thumbnail?.url || product.media?.[0]?.url || '/placeholder-product.jpg'}
                  alt={product.name}
                  fill
                  className="object-cover hover:scale-105 transition-transform duration-300"
                  sizes="128px"
                />
                {savingsPercentage > 0 && (
                  <Badge className="absolute top-2 left-2 bg-red-500 text-white text-xs">
                    -{savingsPercentage}%
                  </Badge>
                )}
              </div>
            </Link>
            
            <div className="flex-1 space-y-3">
              <div>
                <Link 
                  href={`/products/${product.slug || product.id}`}
                  className="text-lg font-semibold text-gray-900 dark:text-white hover:text-red-600 transition-colors"
                >
                  {product.name}
                </Link>
                {product.description && (
                  <p className="text-sm text-gray-500 mt-1">{product.description?.substring(0, 100)}...</p>
                )}
              </div>
              
              {rating > 0 && (
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-1">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={cn(
                          "h-4 w-4",
                          i < Math.floor(rating) ? "text-yellow-400 fill-current" : "text-gray-300"
                        )}
                      />
                    ))}
                  </div>
                  <span className="text-sm text-gray-500">({reviewCount})</span>
                </div>
              )}
              
              {product.description && (
                <p className="text-gray-600 dark:text-gray-300 line-clamp-2">{product.description}</p>
              )}
              
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl font-bold text-red-600">${price.toFixed(2)}</span>
                    {originalPrice && savings > 0 && (
                      <span className="text-sm text-gray-500 line-through">
                        ${originalPrice.toFixed(2)}
                      </span>
                    )}
                  </div>
                  {savings > 0 && (
                    <p className="text-xs text-green-600">Save ${savings.toFixed(2)}</p>
                  )}
                </div>
                
                <Button className="bg-red-600 hover:bg-red-700">
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  Add to Cart
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
  
  return (
    <Card className="group overflow-hidden border-gray-200 hover:border-red-300 transition-all duration-200 hover:shadow-lg">
      <div className="relative aspect-square overflow-hidden bg-gray-100">
        <Link href={`/products/${product.slug || product.id}`}>
          <Image
            src={product.thumbnail?.url || product.media?.[0]?.url || '/placeholder-product.jpg'}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
          />
        </Link>
        
        {savingsPercentage > 0 && (
          <Badge className="absolute top-2 left-2 bg-red-500 text-white">
            -{savingsPercentage}%
          </Badge>
        )}
        
        {!inStock && (
          <Badge className="absolute top-2 right-2 bg-gray-500 text-white">
            Out of Stock
          </Badge>
        )}
        
        {product.metadata?.find(m => m.key === 'dropship')?.value && (
          <Badge className="absolute bottom-2 right-2 bg-blue-100 text-blue-800 text-xs">
            Dropship
          </Badge>
        )}
      </div>
      
      <CardContent className="p-4 space-y-3">
        <div>
          <Link 
            href={`/products/${product.slug || product.id}`}
            className="font-medium text-gray-900 dark:text-white hover:text-red-600 transition-colors line-clamp-2"
          >
            {product.name}
          </Link>
          
          {product.description && (
            <p className="text-sm text-gray-500 mt-1">{product.description.substring(0, 100)}...</p>
          )}
        </div>
        
        {rating > 0 && (
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={cn(
                    "h-3 w-3",
                    i < Math.floor(rating) ? "text-yellow-400 fill-current" : "text-gray-300"
                  )}
                />
              ))}
            </div>
            <span className="text-xs text-gray-500">({reviewCount})</span>
          </div>
        )}
        
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold text-red-600">
              ${price.toFixed(2)}
            </span>
            {originalPrice && savings > 0 && (
              <span className="text-sm text-gray-500 line-through">
                ${originalPrice.toFixed(2)}
              </span>
            )}
          </div>
          {savings > 0 && (
            <p className="text-xs text-green-600">Save ${savings.toFixed(2)}</p>
          )}
        </div>
        
        <Button
          size="sm"
          className="w-full bg-red-600 hover:bg-red-700 text-white"
          disabled={!inStock}
        >
          <ShoppingCart className="h-4 w-4 mr-2" />
          {inStock ? 'Add to Cart' : 'Out of Stock'}
        </Button>
      </CardContent>
    </Card>
  )
}

function ProductsLoading({ layout = 'grid' }: { layout?: 'grid' | 'list' }) {
  const skeletonCount = layout === 'grid' ? 12 : 8
  
  return (
    <div className={cn(
      layout === 'grid' 
        ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" 
        : "space-y-6"
    )}>
      {[...Array(skeletonCount)].map((_, i) => (
        <div key={i} className="animate-pulse">
          {layout === 'grid' ? (
            <Card>
              <div className="aspect-square bg-gray-300 rounded-t-lg"></div>
              <CardContent className="p-4 space-y-3">
                <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                <div className="h-3 bg-gray-300 rounded w-1/2"></div>
                <div className="h-6 bg-gray-300 rounded w-1/3"></div>
                <div className="h-8 bg-gray-300 rounded w-full"></div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-6">
                <div className="flex gap-6">
                  <div className="w-32 h-32 bg-gray-300 rounded-lg"></div>
                  <div className="flex-1 space-y-3">
                    <div className="h-5 bg-gray-300 rounded w-3/4"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/2"></div>
                    <div className="h-16 bg-gray-300 rounded"></div>
                    <div className="flex justify-between">
                      <div className="h-6 bg-gray-300 rounded w-24"></div>
                      <div className="h-9 bg-gray-300 rounded w-32"></div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      ))}
    </div>
  )
}

function ProductsPageContent() {
  const { config } = usePlatform()
  const searchParams = useSearchParams()
  
  const [products, setProducts] = useState<SaleorProduct[]>([])
  const [loading, setLoading] = useState(true)
  const [totalCount, setTotalCount] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [showFilters, setShowFilters] = useState(false)
  
  const [filters, setFilters] = useState<ProductFilters>({
    search: searchParams?.get('search') || '',
    category: searchParams?.get('category') || '',
    priceRange: searchParams?.get('price') || '',
    rating: searchParams?.get('rating') || '',
    sortBy: searchParams?.get('sort') || 'newest',
    layout: (searchParams?.get('layout') as 'grid' | 'list') || 'grid'
  })
  
  const itemsPerPage = 24
  
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true)
        
        const queryParams: any = {
          limit: itemsPerPage,
          offset: (currentPage - 1) * itemsPerPage,
          status: 'published'
        }
        
        // Apply filters
        if (filters.search) {
          queryParams.title = filters.search
        }
        
        if (filters.category) {
          queryParams.collection_id = filters.category
        }
        
        // Sort mapping
        const sortMapping: Record<string, string> = {
          'newest': '-created_at',
          'oldest': 'created_at', 
          'price-low': 'variants.prices.amount',
          'price-high': '-variants.prices.amount',
          'name-asc': 'title',
          'name-desc': '-title'
        }
        
        if (filters.sortBy && sortMapping[filters.sortBy]) {
          queryParams.order = sortMapping[filters.sortBy]
        }
        
        const result = await saleorAPI.getProducts(queryParams)
        
        let filteredProducts = result.products.edges.map(edge => edge.node)
        
        // Client-side filtering for price and rating (since Saleor might not support these directly)
        if (filters.priceRange) {
          const [min, max] = filters.priceRange.split('-').map(Number)
          filteredProducts = filteredProducts.filter(product => {
            const price = product.variants?.[0]?.pricing?.price?.gross.amount || 0
            return price >= min && (max === 0 || price <= max)
          })
        }
        
        if (filters.rating) {
          const minRating = Number(filters.rating)
          filteredProducts = filteredProducts.filter(product => {
            const rating = product.metadata?.find(m => m.key === 'amazon_rating')?.value ? Number(product.metadata.find(m => m.key === 'amazon_rating')?.value) : 0
            return rating >= minRating
          })
        }
        
        setProducts(filteredProducts)
        setTotalCount(filteredProducts.length)
        
      } catch (error) {
        console.error('Failed to fetch products:', error)
        setProducts([])
      } finally {
        setLoading(false)
      }
    }
    
    fetchProducts()
  }, [filters, currentPage])
  
  const updateFilter = (key: keyof ProductFilters, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setCurrentPage(1)
  }
  
  const clearFilters = () => {
    setFilters({
      search: '',
      category: '',
      priceRange: '',
      rating: '',
      sortBy: 'newest',
      layout: 'grid'
    })
    setCurrentPage(1)
  }
  
  const totalPages = Math.ceil(totalCount / itemsPerPage)
  const hasActiveFilters = filters.search || filters.category || filters.priceRange || filters.rating
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950/20 dark:to-orange-950/20">
      <div className="container mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <Breadcrumb className="mb-8">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink href="/" className="text-red-600 hover:text-red-700">Home</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage className="text-gray-500">Products</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
        
        {/* Header */}
        <div className="flex flex-col gap-6 mb-8">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                All Products
              </h1>
              <p className="text-gray-600 dark:text-gray-300 mt-1">
                Discover amazing products from {config.name}
              </p>
            </div>
            
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="border-red-200 hover:border-red-300"
              >
                <Filter className="h-4 w-4 mr-2" />
                Filters
                {hasActiveFilters && (
                  <Badge className="ml-2 bg-red-500 text-white text-xs px-1 py-0 h-4 w-4 rounded-full flex items-center justify-center">
                    !
                  </Badge>
                )}
              </Button>
              
              <div className="flex items-center border border-gray-200 rounded-lg overflow-hidden">
                <Button
                  variant={filters.layout === 'grid' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => updateFilter('layout', 'grid')}
                  className={cn(
                    "rounded-none",
                    filters.layout === 'grid' && "bg-red-600 hover:bg-red-700"
                  )}
                >
                  <Grid3X3 className="h-4 w-4" />
                </Button>
                <Button
                  variant={filters.layout === 'list' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => updateFilter('layout', 'list')}
                  className={cn(
                    "rounded-none",
                    filters.layout === 'list' && "bg-red-600 hover:bg-red-700"
                  )}
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
          
          {/* Search and Quick Filters */}
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search products..."
                value={filters.search}
                onChange={(e) => updateFilter('search', e.target.value)}
                className="pl-10"
              />
            </div>
            
            <div className="flex flex-wrap gap-2">
              <Select value={filters.sortBy} onValueChange={(value) => updateFilter('sortBy', value)}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="newest">Newest</SelectItem>
                  <SelectItem value="oldest">Oldest</SelectItem>
                  <SelectItem value="price-low">Price: Low to High</SelectItem>
                  <SelectItem value="price-high">Price: High to Low</SelectItem>
                  <SelectItem value="name-asc">Name: A to Z</SelectItem>
                  <SelectItem value="name-desc">Name: Z to A</SelectItem>
                </SelectContent>
              </Select>
              
              {hasActiveFilters && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearFilters}
                  className="border-red-200 hover:border-red-300 text-red-600"
                >
                  <X className="h-4 w-4 mr-1" />
                  Clear
                </Button>
              )}
            </div>
          </div>
          
          {/* Advanced Filters */}
          {showFilters && (
            <Card className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Price Range</label>
                  <Select value={filters.priceRange} onValueChange={(value) => updateFilter('priceRange', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Any Price" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Any Price</SelectItem>
                      <SelectItem value="0-25">Under $25</SelectItem>
                      <SelectItem value="25-50">$25 - $50</SelectItem>
                      <SelectItem value="50-100">$50 - $100</SelectItem>
                      <SelectItem value="100-0">Over $100</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Minimum Rating</label>
                  <Select value={filters.rating} onValueChange={(value) => updateFilter('rating', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Any Rating" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Any Rating</SelectItem>
                      <SelectItem value="4">4+ Stars</SelectItem>
                      <SelectItem value="3">3+ Stars</SelectItem>
                      <SelectItem value="2">2+ Stars</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div>
                  <label className="text-sm font-medium mb-2 block">Category</label>
                  <Select value={filters.category} onValueChange={(value) => updateFilter('category', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="All Categories" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">All Categories</SelectItem>
                      <SelectItem value="electronics">Electronics</SelectItem>
                      <SelectItem value="clothing">Clothing</SelectItem>
                      <SelectItem value="home">Home & Garden</SelectItem>
                      <SelectItem value="books">Books</SelectItem>
                      <SelectItem value="sports">Sports</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="flex items-end">
                  <Button
                    variant="outline"
                    onClick={() => setShowFilters(false)}
                    className="w-full"
                  >
                    Apply Filters
                  </Button>
                </div>
              </div>
            </Card>
          )}
        </div>
        
        {/* Results Count */}
        {!loading && (
          <div className="flex justify-between items-center mb-6">
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Showing {products.length} of {totalCount} products
              {filters.search && ` for "${filters.search}"`}
            </p>
            {totalPages > 1 && (
              <p className="text-sm text-gray-600 dark:text-gray-300">
                Page {currentPage} of {totalPages}
              </p>
            )}
          </div>
        )}
        
        {/* Products Grid */}
        {loading ? (
          <ProductsLoading layout={filters.layout} />
        ) : products.length > 0 ? (
          <div className={cn(
            filters.layout === 'grid' 
              ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" 
              : "space-y-6"
          )}>
            {products.map((product) => (
              <ProductCard key={product.id} product={product} layout={filters.layout} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-gray-400 mb-4">
              <Search className="h-16 w-16 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                No products found
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {hasActiveFilters 
                  ? "Try adjusting your filters or search terms" 
                  : "No products available at the moment"
                }
              </p>
            </div>
            {hasActiveFilters && (
              <Button 
                onClick={clearFilters}
                className="bg-red-600 hover:bg-red-700"
              >
                Clear All Filters
              </Button>
            )}
          </div>
        )}
        
        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-12">
            <Button
              variant="outline"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(prev => prev - 1)}
              className="border-red-200 hover:border-red-300"
            >
              Previous
            </Button>
            
            {[...Array(Math.min(totalPages, 5))].map((_, i) => {
              const pageNumber = Math.max(1, currentPage - 2) + i
              if (pageNumber > totalPages) return null
              
              return (
                <Button
                  key={pageNumber}
                  variant={currentPage === pageNumber ? "default" : "outline"}
                  onClick={() => setCurrentPage(pageNumber)}
                  className={cn(
                    currentPage === pageNumber 
                      ? "bg-red-600 hover:bg-red-700" 
                      : "border-red-200 hover:border-red-300"
                  )}
                >
                  {pageNumber}
                </Button>
              )
            })}
            
            <Button
              variant="outline"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(prev => prev + 1)}
              className="border-red-200 hover:border-red-300"
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

export default function ProductsPage() {
  return (
    <Suspense fallback={<ProductsLoading />}>
      <ProductsPageContent />
    </Suspense>
  )
}