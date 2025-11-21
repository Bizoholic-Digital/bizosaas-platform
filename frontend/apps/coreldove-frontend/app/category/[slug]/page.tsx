/**
 * CorelDove Dynamic Category Page
 * Shows products for a specific category with filters and sorting
 */

'use client'

import { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../../components/ui/button'
import { Card, CardContent, CardFooter } from '../../../components/ui/card'
import { Badge } from '../../../components/ui/badge'
import { Input } from '../../../components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../../components/ui/select'
import { useTenantTheme } from '../../../hooks/useTenantTheme'
import Header from '../../../components/navigation/header'
import Footer from '../../../components/navigation/footer'
import { 
  ArrowRight, 
  ShoppingCart, 
  Heart,
  Search,
  Filter,
  Grid3X3,
  List,
  Star,
  ChevronDown
} from 'lucide-react'

interface Product {
  id: string
  name: string
  slug: string
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
  thumbnail?: {
    url: string
    alt?: string
  }
  category: {
    name: string
    slug: string
  }
  rating?: number
  reviews?: number
}

interface Category {
  id: string
  name: string
  slug: string
  description: string
  productCount: number
}

export default function CategoryPage() {
  const params = useParams()
  const searchParams = useSearchParams()
  const { config } = useTenantTheme()
  
  const [category, setCategory] = useState<Category | null>(null)
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('name')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  
  const categorySlug = params.slug as string

  useEffect(() => {
    const fetchCategoryData = async () => {
      try {
        setLoading(true)
        
        // Fetch category info and products in parallel
        const [categoryResponse, productsResponse] = await Promise.all([
          fetch(`/api/brain/saleor/categories?slug=${categorySlug}`),
          fetch(`/api/brain/saleor/products?category=${categorySlug}&limit=20&marketplace=IN&currency=INR`)
        ])
        
        const categoryData = await categoryResponse.json()
        const productsData = await productsResponse.json()
        
        // Set category info
        if (categoryData.categories && categoryData.categories.length > 0) {
          setCategory(categoryData.categories[0])
        } else {
          // Fallback category based on slug
          setCategory({
            id: categorySlug,
            name: categorySlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            slug: categorySlug,
            description: `Discover our collection of ${categorySlug.replace(/-/g, ' ')} products`,
            productCount: 0
          })
        }
        
        // Set products
        setProducts(productsData.products || [])
        
      } catch (error) {
        console.error('Error fetching category data:', error)
        
        // Fallback data
        setCategory({
          id: categorySlug,
          name: categorySlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          slug: categorySlug,
          description: `Discover our collection of ${categorySlug.replace(/-/g, ' ')} products`,
          productCount: 0
        })
        
        // Fallback products based on category
        const fallbackProducts = [
          {
            id: `fallback-${categorySlug}-1`,
            name: `Premium ${categorySlug.replace(/-/g, ' ')} Product`,
            slug: `premium-${categorySlug}-product`,
            description: `High-quality ${categorySlug.replace(/-/g, ' ')} product with excellent features.`,
            pricing: {
              priceRange: {
                start: {
                  gross: {
                    amount: 1999,
                    currency: 'INR'
                  }
                }
              }
            },
            thumbnail: {
              url: '/placeholder-product.jpg',
              alt: `Premium ${categorySlug} Product`
            },
            category: {
              name: categorySlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
              slug: categorySlug
            },
            rating: 4.5,
            reviews: 128
          },
          {
            id: `fallback-${categorySlug}-2`,
            name: `Best Selling ${categorySlug.replace(/-/g, ' ')} Item`,
            slug: `best-selling-${categorySlug}-item`,
            description: `Popular ${categorySlug.replace(/-/g, ' ')} item loved by customers.`,
            pricing: {
              priceRange: {
                start: {
                  gross: {
                    amount: 2499,
                    currency: 'INR'
                  }
                }
              }
            },
            thumbnail: {
              url: '/placeholder-product.jpg',
              alt: `Best Selling ${categorySlug} Item`
            },
            category: {
              name: categorySlug.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
              slug: categorySlug
            },
            rating: 4.7,
            reviews: 89
          }
        ]
        
        setProducts(fallbackProducts)
        
      } finally {
        setLoading(false)
      }
    }

    if (categorySlug) {
      fetchCategoryData()
    }
  }, [categorySlug])

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const sortedProducts = [...filteredProducts].sort((a, b) => {
    switch (sortBy) {
      case 'price-low':
        return a.pricing.priceRange.start.gross.amount - b.pricing.priceRange.start.gross.amount
      case 'price-high':
        return b.pricing.priceRange.start.gross.amount - a.pricing.priceRange.start.gross.amount
      case 'rating':
        return (b.rating || 0) - (a.rating || 0)
      case 'name':
      default:
        return a.name.localeCompare(b.name)
    }
  })

  const formatPrice = (amount: number, currency: string) => {
    const formatter = new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: currency,
    })
    return formatter.format(amount)
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header currentPath={`/category/${categorySlug}`} />
      
      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <Link href="/categories" className="hover:text-foreground">Categories</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground">{category?.name}</span>
          </div>
        </div>
      </div>

      <main className="flex-1 py-8">
        <div className="container">
          {/* Category Header */}
          {category && (
            <div className="mb-8">
              <h1 className="text-3xl font-bold mb-2">{category.name}</h1>
              <p className="text-muted-foreground mb-4">{category.description}</p>
              <Badge variant="secondary">
                {filteredProducts.length} product{filteredProducts.length !== 1 ? 's' : ''}
              </Badge>
            </div>
          )}
          
          {/* Filters and Controls */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  type="text"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-9 w-64"
                />
              </div>
              
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="name">Name (A-Z)</SelectItem>
                  <SelectItem value="price-low">Price (Low to High)</SelectItem>
                  <SelectItem value="price-high">Price (High to Low)</SelectItem>
                  <SelectItem value="rating">Rating</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex border rounded-md">
              <Button
                variant={viewMode === 'grid' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('grid')}
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'default' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('list')}
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Products Grid */}
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-500 mx-auto"></div>
              <p className="mt-4 text-muted-foreground">Loading products...</p>
            </div>
          ) : (
            <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6' : 'space-y-6'}>
              {sortedProducts.map((product) => (
                <Card key={product.id} className="group hover:shadow-lg transition-all duration-300">
                  <CardContent className="p-4">
                    {/* Product Image */}
                    <div className="relative aspect-square mb-4 rounded-lg overflow-hidden bg-gray-100">
                      <Image
                        src={product.thumbnail?.url || '/placeholder-product.jpg'}
                        alt={product.thumbnail?.alt || product.name}
                        fill
                        className="object-cover transition-transform duration-300 group-hover:scale-105"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                      />
                      <div className="absolute top-2 right-2">
                        <Button size="sm" variant="secondary" className="rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                          <Heart className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>

                    {/* Product Info */}
                    <div className="space-y-2">
                      <Badge variant="outline" className="text-xs">
                        {product.category.name}
                      </Badge>
                      
                      <Link href={`/products/${product.slug}`}>
                        <h3 className="font-semibold text-sm hover:text-primary transition-colors line-clamp-2">
                          {product.name}
                        </h3>
                      </Link>
                      
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {product.description}
                      </p>
                      
                      {/* Rating */}
                      {product.rating && (
                        <div className="flex items-center space-x-1">
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                className={`h-3 w-3 ${
                                  i < Math.floor(product.rating || 0)
                                    ? 'text-yellow-400 fill-current'
                                    : 'text-gray-300'
                                }`}
                              />
                            ))}
                          </div>
                          <span className="text-xs text-muted-foreground">
                            ({product.reviews || 0})
                          </span>
                        </div>
                      )}
                      
                      {/* Price */}
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-primary">
                          {formatPrice(
                            product.pricing?.priceRange?.start?.gross?.amount || product.price?.amount || 0,
                            product.pricing?.priceRange?.start?.gross?.currency || product.price?.currency || 'INR'
                          )}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                  
                  <CardFooter className="p-4 pt-0">
                    <Link href={`/products/${product.slug}`} className="w-full">
                      <Button className="w-full" size="sm">
                        <ShoppingCart className="w-4 h-4 mr-2" />
                        View Details
                      </Button>
                    </Link>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}

          {sortedProducts.length === 0 && !loading && (
            <div className="text-center py-12">
              <p className="text-muted-foreground">No products found in this category.</p>
              <Link href="/categories">
                <Button variant="outline" className="mt-4">
                  Browse All Categories
                </Button>
              </Link>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}