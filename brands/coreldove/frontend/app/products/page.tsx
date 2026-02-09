/**
 * CorelDove Products Page - Browse All Products with Filtering
 * Integrates with Saleor backend via Brain API for dynamic product data
 */

'use client'

import { useEffect, useState, useCallback } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'
import { Input } from '../../components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select'
import { useTenantTheme } from '../../hooks/useTenantTheme'
import { useCart } from '../../lib/stores/cart-store'
import Header from '../../components/navigation/header'
import Footer from '../../components/navigation/footer'
import { 
  ArrowRight, 
  ShoppingCart, 
  Star, 
  Search,
  Filter,
  Heart,
  Eye,
  Grid3X3,
  List,
  SlidersHorizontal,
  ArrowLeft
} from 'lucide-react'

interface Product {
  id: string
  name: string
  slug: string
  description: string
  thumbnail?: {
    url: string
    alt: string
  }
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
  category: {
    name: string
    slug: string
  }
  rating: number
  reviews: number
  inStock: boolean
  featured: boolean
}

interface Category {
  id: string
  name: string
  slug: string
  productsCount: number
}

export default function ProductsPage() {
  const { config } = useTenantTheme()
  const { addItem } = useCart()
  
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [sortBy, setSortBy] = useState('name')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [currentPage, setCurrentPage] = useState(1)
  const [totalCount, setTotalCount] = useState(0)
  const [hasNextPage, setHasNextPage] = useState(false)
  const [filtersOpen, setFiltersOpen] = useState(false)

  const ITEMS_PER_PAGE = 12

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true)
      
      const params = new URLSearchParams({
        limit: ITEMS_PER_PAGE.toString(),
        offset: ((currentPage - 1) * ITEMS_PER_PAGE).toString(),
        sortBy,
      })
      
      if (searchQuery) params.set('search', searchQuery)
      if (selectedCategory && selectedCategory !== 'all') params.set('category', selectedCategory)
      
      const response = await fetch(`/api/brain/saleor/products?${params}`)
      
      if (response.ok) {
        const data = await response.json()
        setProducts(data.products || [])
        setTotalCount(data.totalCount || 0)
        setHasNextPage(data.hasNextPage || false)
      } else {
        console.error('Failed to fetch products')
        setProducts([])
      }
    } catch (error) {
      console.error('Error fetching products:', error)
      setProducts([])
    } finally {
      setLoading(false)
    }
  }, [currentPage, searchQuery, selectedCategory, sortBy])

  const fetchCategories = useCallback(async () => {
    try {
      const response = await fetch('/api/brain/saleor/categories?first=20')
      if (response.ok) {
        const data = await response.json()
        setCategories(data.categories || [])
      }
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }, [])

  useEffect(() => {
    fetchCategories()
  }, [fetchCategories])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setCurrentPage(1)
    fetchProducts()
  }

  const handleCategoryChange = (value: string) => {
    setSelectedCategory(value === 'all' ? '' : value)
    setCurrentPage(1)
  }

  const handleSortChange = (value: string) => {
    setSortBy(value)
    setCurrentPage(1)
  }

  const handleAddToCart = (product: Product) => {
    if (product.inStock) {
      addItem({
        id: `cart-${product.id}`,
        productId: product.id,
        name: product.name,
        slug: product.slug,
        description: product.description,
        thumbnail: product.thumbnail,
        pricing: product.pricing,
        category: product.category,
        inStock: product.inStock,
        maxQuantity: 10,
      })
    }
  }

  const totalPages = Math.ceil(totalCount / ITEMS_PER_PAGE)

  return (
    <div className="flex flex-col min-h-screen">
      <Header currentPath="/products" />

      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground">Products</span>
            {selectedCategory && selectedCategory !== 'all' && (
              <>
                <ArrowRight className="h-4 w-4" />
                <span className="text-foreground">
                  {categories.find(c => c.slug === selectedCategory)?.name}
                </span>
              </>
            )}
          </div>
        </div>
      </div>

      <main className="flex-1 py-8">
        <div className="container">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">
              All Products
              {selectedCategory && selectedCategory !== 'all' && (
                <span className="text-red-500 ml-2">
                  in {categories.find(c => c.slug === selectedCategory)?.name}
                </span>
              )}
            </h1>
            <p className="text-muted-foreground">
              Discover our complete range of quality products with AI-powered recommendations
            </p>
          </div>

          {/* Search and Filters Bar */}
          <div className="mb-8 space-y-4">
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search */}
              <form onSubmit={handleSearch} className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Search products..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </form>

              {/* Category Filter */}
              <Select value={selectedCategory || 'all'} onValueChange={handleCategoryChange}>
                <SelectTrigger className="w-full lg:w-[200px]">
                  <Filter className="mr-2 h-4 w-4" />
                  <SelectValue placeholder="All Categories" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {categories.map((category) => (
                    <SelectItem key={category.id} value={category.slug}>
                      {category.name} ({category.productsCount})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              {/* Sort */}
              <Select value={sortBy} onValueChange={handleSortChange}>
                <SelectTrigger className="w-full lg:w-[150px]">
                  <SlidersHorizontal className="mr-2 h-4 w-4" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="name">Name A-Z</SelectItem>
                  <SelectItem value="price-low">Price Low-High</SelectItem>
                  <SelectItem value="price-high">Price High-Low</SelectItem>
                  <SelectItem value="newest">Newest First</SelectItem>
                  <SelectItem value="rating">Highest Rated</SelectItem>
                </SelectContent>
              </Select>

              {/* View Mode Toggle */}
              <div className="flex items-center border rounded-md">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                  className="rounded-r-none"
                >
                  <Grid3X3 className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                  className="rounded-l-none"
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Results Info */}
          <div className="flex items-center justify-between mb-6">
            <p className="text-sm text-muted-foreground">
              Showing {((currentPage - 1) * ITEMS_PER_PAGE) + 1}-{Math.min(currentPage * ITEMS_PER_PAGE, totalCount)} of {totalCount} products
            </p>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {Array.from({ length: 8 }).map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 aspect-square rounded-lg mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          )}

          {/* Products Grid */}
          {!loading && products.length > 0 && (
            <div className={`grid gap-6 ${
              viewMode === 'grid' 
                ? 'md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' 
                : 'grid-cols-1 lg:grid-cols-2'
            }`}>
              {products.map((product) => (
                <Card key={product.id} className="group card-hover product-card">
                  <Link href={`/products/${product.slug}`}>
                    <div className="aspect-square relative overflow-hidden rounded-t-lg bg-muted">
                      {product.thumbnail ? (
                        <Image
                          src={product.thumbnail.url}
                          alt={product.thumbnail.alt || product.name || 'Product image'}
                          fill
                          className="object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none'
                          }}
                        />
                      ) : (
                        <div className="w-full h-full image-placeholder-primary">
                          <div className="h-16 w-16" />
                        </div>
                      )}
                      <div className="absolute top-2 left-2">
                        {!product.inStock && (
                          <Badge variant="destructive">Out of Stock</Badge>
                        )}
                        {product.featured && (
                          <Badge className="bg-red-500">Featured</Badge>
                        )}
                      </div>
                      <div className="absolute top-2 right-2 flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 bg-white/80 hover:bg-white">
                          <Heart className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 bg-white/80 hover:bg-white">
                          <Eye className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </Link>
                  
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                      <span>{product.category.name}</span>
                      <span>•</span>
                      <div className="flex items-center gap-1">
                        <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                        <span>{product.rating}</span>
                        <span>({product.reviews})</span>
                      </div>
                    </div>
                    <CardTitle className="text-lg line-clamp-2">
                      <Link href={`/products/${product.slug}`} className="hover:text-red-500">
                        {product.name}
                      </Link>
                    </CardTitle>
                  </CardHeader>
                  
                  <CardContent>
                    <p className="text-muted-foreground line-clamp-2 mb-4">{product.description}</p>
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-red-500 price-tag">
                        ${product.pricing.priceRange.start.gross.amount}
                      </span>
                      <Button 
                        size="sm" 
                        className="bg-red-500 hover:bg-red-600" 
                        disabled={!product.inStock}
                        onClick={(e) => {
                          e.preventDefault()
                          handleAddToCart(product)
                        }}
                      >
                        <ShoppingCart className="h-4 w-4 mr-2" />
                        {product.inStock ? 'Add to Cart' : 'Notify Me'}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* No Products Found */}
          {!loading && products.length === 0 && (
            <div className="text-center py-16">
              <div className="w-24 h-24 mx-auto bg-muted rounded-full flex items-center justify-center mb-4">
                <Search className="h-12 w-12 text-muted-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-2">No products found</h3>
              <p className="text-muted-foreground mb-6">
                Try adjusting your search criteria or browse our categories
              </p>
              <div className="flex gap-4 justify-center">
                <Button onClick={() => {
                  setSearchQuery('')
                  setSelectedCategory('')
                  setCurrentPage(1)
                }}>
                  Clear Filters
                </Button>
                <Button variant="outline" asChild>
                  <Link href="/categories">Browse Categories</Link>
                </Button>
              </div>
            </div>
          )}

          {/* Pagination */}
          {!loading && products.length > 0 && totalPages > 1 && (
            <div className="flex items-center justify-center mt-12 space-x-2">
              <Button
                variant="outline"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(currentPage - 1)}
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Previous
              </Button>
              
              {Array.from({ length: Math.min(5, totalPages) }).map((_, i) => {
                let pageNum
                if (totalPages <= 5) {
                  pageNum = i + 1
                } else if (currentPage <= 3) {
                  pageNum = i + 1
                } else if (currentPage >= totalPages - 2) {
                  pageNum = totalPages - 4 + i
                } else {
                  pageNum = currentPage - 2 + i
                }

                return (
                  <Button
                    key={pageNum}
                    variant={currentPage === pageNum ? 'default' : 'outline'}
                    onClick={() => setCurrentPage(pageNum)}
                  >
                    {pageNum}
                  </Button>
                )
              })}
              
              <Button
                variant="outline"
                disabled={!hasNextPage}
                onClick={() => setCurrentPage(currentPage + 1)}
              >
                Next
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}