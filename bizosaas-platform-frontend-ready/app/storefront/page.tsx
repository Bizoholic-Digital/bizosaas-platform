'use client'

/**
 * CoreLDove E-commerce Storefront
 * Hero section + 3 categories + products from Saleor via FastAPI Brain
 */

import { useEffect, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  ShoppingBag, 
  Star, 
  Search, 
  Filter,
  ArrowRight,
  Truck,
  Shield,
  RefreshCw
} from 'lucide-react'

// Types for Saleor products
interface Product {
  id: string
  name: string
  description?: string
  pricing?: {
    priceRange?: {
      start?: {
        gross?: {
          amount: number
          currency: string
        }
      }
    }
  }
  thumbnail?: {
    url: string
  }
  category?: {
    name: string
  }
  rating?: number
  reviews?: number
}

interface Category {
  id: string
  name: string
  slug: string
  description?: string
  products?: {
    edges: Array<{
      node: Product
    }>
  }
}

export default function StorefrontPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  // Fetch products from Saleor via FastAPI Brain
  useEffect(() => {
    fetchStorefrontData()
  }, [])

  const fetchStorefrontData = async () => {
    try {
      setLoading(true)
      
      // Fetch categories and products from FastAPI Brain
      const [categoriesRes, productsRes] = await Promise.all([
        fetch('/api/brain/saleor/categories'),
        fetch('/api/brain/saleor/products?limit=12')
      ])
      
      if (categoriesRes.ok) {
        const categoriesData = await categoriesRes.json()
        setCategories(categoriesData.categories || [])
      }
      
      if (productsRes.ok) {
        const productsData = await productsRes.json()
        setProducts(productsData.products || [])
        
        // Set featured products (first 6 products)
        setFeaturedProducts((productsData.products || []).slice(0, 6))
      }
    } catch (error) {
      console.error('Error fetching storefront data:', error)
      // Set fallback data on error
      setCategories([
        {
          id: "fallback-1",
          name: "Electronics", 
          slug: "electronics",
          description: "Latest gadgets and tech accessories",
          products: { totalCount: 45 }
        },
        {
          id: "fallback-2", 
          name: "Fashion",
          slug: "fashion", 
          description: "Trendy clothing and accessories",
          products: { totalCount: 89 }
        },
        {
          id: "fallback-3",
          name: "Home & Garden",
          slug: "home-garden",
          description: "Everything for your home and garden", 
          products: { totalCount: 67 }
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center">
            <Image
              src="/coreldove-logo.png"
              alt="CoreLDove - Premium E-commerce Platform"
              width={140}
              height={35}
              className="h-9 w-auto"
              priority
            />
          </Link>
          
          <nav className="hidden md:flex items-center space-x-6 text-sm font-medium">
            <Link href="/storefront" className="text-foreground">Shop</Link>
            <Link href="/products" className="text-foreground/60 hover:text-foreground">Products</Link>
            <Link href="#categories" className="text-foreground/60 hover:text-foreground">Categories</Link>
            <Link href="#about" className="text-foreground/60 hover:text-foreground">About</Link>
          </nav>
          
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="sm">
              <ShoppingBag className="h-4 w-4" />
            </Button>
            <Link href="/auth/login">
              <Button size="sm">Sign In</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 lg:py-28 bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-blue-950/30 dark:to-indigo-950/30">
        <div className="container">
          <div className="mx-auto max-w-4xl text-center">
            <Badge variant="outline" className="mb-6">
              <ShoppingBag className="mr-2 h-3 w-3" />
              Premium E-commerce Platform
            </Badge>
            
            <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl">
              Discover Amazing{' '}
              <span className="text-primary">Products</span>
            </h1>
            
            <p className="mt-6 text-lg leading-8 text-muted-foreground max-w-2xl mx-auto">
              CoreLDove brings you the finest selection of products with seamless shopping experience, 
              fast delivery, and exceptional customer service.
            </p>
            
            <div className="mt-10 flex items-center justify-center gap-6">
              <Button size="lg" className="px-8">
                Shop Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button variant="outline" size="lg">
                Browse Categories
              </Button>
            </div>

            {/* Trust Indicators */}
            <div className="mt-12 flex items-center justify-center space-x-8 text-sm text-muted-foreground">
              <div className="flex items-center space-x-2">
                <Truck className="h-4 w-4 text-green-600" />
                <span>Free Shipping</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="h-4 w-4 text-green-600" />
                <span>Secure Payments</span>
              </div>
              <div className="flex items-center space-x-2">
                <RefreshCw className="h-4 w-4 text-green-600" />
                <span>Easy Returns</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Search Bar */}
      <section className="py-8 border-b">
        <div className="container">
          <div className="max-w-md mx-auto">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
        </div>
      </section>

      {/* 3 Categories Section */}
      <section id="categories" className="py-16 bg-muted/30">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Shop by Category
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Explore our carefully curated product categories
            </p>
          </div>
          
          <div className="grid gap-8 md:grid-cols-3">
            {loading ? (
              // Loading skeleton for categories
              Array.from({ length: 3 }).map((_, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow animate-pulse">
                  <CardHeader className="text-center">
                    <div className="w-16 h-16 bg-muted rounded-full mx-auto mb-4"></div>
                    <div className="h-6 bg-muted rounded mb-2"></div>
                  </CardHeader>
                  <CardContent>
                    <div className="h-4 bg-muted rounded mb-2"></div>
                    <div className="h-4 bg-muted rounded w-3/4 mx-auto"></div>
                  </CardContent>
                </Card>
              ))
            ) : categories.length > 0 ? (
              categories.slice(0, 3).map((category) => (
                <Card key={category.id} className="hover:shadow-lg transition-shadow cursor-pointer group">
                  <CardHeader className="text-center">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary/20 transition-colors">
                      <ShoppingBag className="h-8 w-8 text-primary" />
                    </div>
                    <CardTitle className="group-hover:text-primary transition-colors">
                      {category.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-center">
                    <p className="text-muted-foreground mb-4">
                      {category.description || `Discover amazing ${category.name.toLowerCase()}`}
                    </p>
                    <Button variant="outline" size="sm" className="group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                      Browse {category.name}
                    </Button>
                  </CardContent>
                </Card>
              ))
            ) : (
              // Fallback categories if Saleor data not available
              [
                { name: "Electronics", description: "Latest gadgets and tech accessories" },
                { name: "Fashion", description: "Trendy clothing and accessories" },
                { name: "Home & Garden", description: "Everything for your home and garden" }
              ].map((category, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow cursor-pointer group">
                  <CardHeader className="text-center">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary/20 transition-colors">
                      <ShoppingBag className="h-8 w-8 text-primary" />
                    </div>
                    <CardTitle className="group-hover:text-primary transition-colors">
                      {category.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-center">
                    <p className="text-muted-foreground mb-4">{category.description}</p>
                    <Button variant="outline" size="sm" className="group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                      Browse {category.name}
                    </Button>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Features Section - Products from Saleor */}
      <section className="py-16">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-12">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Featured Products
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              {searchQuery ? `Search results for "${searchQuery}"` : 'Hand-picked products just for you'}
            </p>
          </div>
          
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {loading ? (
              // Loading skeleton for products
              Array.from({ length: 6 }).map((_, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow animate-pulse">
                  <div className="aspect-square bg-muted"></div>
                  <CardHeader>
                    <div className="h-4 bg-muted rounded mb-2"></div>
                    <div className="h-4 bg-muted rounded w-3/4"></div>
                  </CardHeader>
                  <CardContent>
                    <div className="h-4 bg-muted rounded mb-2"></div>
                    <div className="h-8 bg-muted rounded"></div>
                  </CardContent>
                </Card>
              ))
            ) : (
              (searchQuery ? filteredProducts : featuredProducts).map((product) => (
                <Card key={product.id} className="hover:shadow-lg transition-shadow group cursor-pointer">
                  <div className="aspect-square overflow-hidden rounded-t-lg bg-gray-100">
                    {product.thumbnail?.url ? (
                      <Image
                        src={product.thumbnail.url}
                        alt={product.name}
                        width={400}
                        height={400}
                        className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                    ) : (
                      <div className="h-full w-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                        <ShoppingBag className="h-12 w-12 text-gray-400" />
                      </div>
                    )}
                  </div>
                  <CardHeader className="pb-2">
                    <CardTitle className="line-clamp-2 group-hover:text-primary transition-colors">
                      {product.name}
                    </CardTitle>
                    {product.category && (
                      <Badge variant="secondary" className="w-fit">
                        {product.category.name}
                      </Badge>
                    )}
                  </CardHeader>
                  <CardContent>
                    {product.description && (
                      <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                        {product.description}
                      </p>
                    )}
                    
                    <div className="flex items-center justify-between">
                      <div className="flex flex-col">
                        {product.pricing?.priceRange?.start?.gross && (
                          <span className="text-lg font-bold text-primary">
                            {product.pricing.priceRange.start.gross.currency} {product.pricing.priceRange.start.gross.amount}
                          </span>
                        )}
                        {product.rating && (
                          <div className="flex items-center space-x-1 mt-1">
                            <div className="flex">
                              {[...Array(5)].map((_, i) => (
                                <Star
                                  key={i}
                                  className={`h-3 w-3 ${
                                    i < product.rating! 
                                      ? 'fill-yellow-400 text-yellow-400' 
                                      : 'text-gray-300'
                                  }`}
                                />
                              ))}
                            </div>
                            {product.reviews && (
                              <span className="text-xs text-muted-foreground">
                                ({product.reviews})
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                      
                      <Button size="sm" className="group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                        Add to Cart
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
          
          {!loading && (searchQuery ? filteredProducts : featuredProducts).length === 0 && (
            <div className="text-center py-12">
              <ShoppingBag className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-foreground mb-2">
                {searchQuery ? 'No products found' : 'No products available'}
              </h3>
              <p className="text-muted-foreground">
                {searchQuery ? 'Try adjusting your search terms' : 'Check back soon for new products'}
              </p>
            </div>
          )}
          
          {!loading && (searchQuery ? filteredProducts : featuredProducts).length > 0 && (
            <div className="text-center mt-12">
              <Link href="/products">
                <Button size="lg" variant="outline">
                  View All Products
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/30">
        <div className="container py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Image
                src="/coreldove-logo.png"
                alt="CoreLDove - Premium E-commerce Platform"
                width={100}
                height={25}
                className="h-6 w-auto"
              />
            </div>
            
            <p className="text-sm text-muted-foreground">
              © 2024 CoreLDove. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}