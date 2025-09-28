/**
 * CorelDove Homepage - Dynamic E-commerce Content from Saleor
 * Product data is managed through BizOSaaS dashboard and served via Brain API
 */

'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { useTenantTheme } from '../hooks/useTenantTheme'
import Header from '../components/navigation/header'
import { 
  ArrowRight, 
  ShoppingCart, 
  Star, 
  Package, 
  Truck, 
  Shield,
  Search,
  Filter,
  Heart,
  Eye
} from 'lucide-react'

// Types for Saleor e-commerce data
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
  description: string
  backgroundImage?: {
    url: string
    alt: string
  }
  productsCount: number
}

interface HomepageData {
  featuredProducts: Product[]
  categories: Category[]
  heroSection: {
    title: string
    subtitle: string
    ctaText: string
    ctaUrl: string
    backgroundImage?: string
  }
  stats: {
    totalProducts: number
    happyCustomers: number
    countriesServed: number
    yearsExperience: number
  }
}

export default function CorelDoveHomepage() {
  const { config } = useTenantTheme()
  const [homepageData, setHomepageData] = useState<HomepageData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHomepageData()
  }, [])

  const fetchHomepageData = async () => {
    try {
      setLoading(true)
      
      // Set basic page data immediately
      const basicData = {
        featuredProducts: [],
        categories: [],
        heroSection: {
          title: "Smart E-commerce Solutions",
          subtitle: "Discover quality products with AI-powered sourcing, intelligent inventory management, and seamless shopping experience.",
          ctaText: "Shop Now",
          ctaUrl: "/products"
        },
        stats: {
          totalProducts: 10000,
          happyCustomers: 5000,
          countriesServed: 25,
          yearsExperience: 5
        }
      }
      
      // Set initial data to remove loading screen faster
      setHomepageData(basicData)
      setLoading(false)
      
      // Fetch e-commerce data from Saleor via Brain API with timeout
      const fetchWithTimeout = (url: string, timeout = 3000) => {
        return Promise.race([
          fetch(url),
          new Promise<Response>((_, reject) => 
            setTimeout(() => reject(new Error('Timeout')), timeout)
          )
        ]);
      }
      
      const [productsRes, categoriesRes] = await Promise.allSettled([
        fetchWithTimeout('/api/brain/saleor/products?featured=true&first=8'),
        fetchWithTimeout('/api/brain/saleor/categories?first=6')
      ])
      
      let featuredProducts: Product[] = []
      let categories: Category[] = []
      
      if (productsRes.status === 'fulfilled' && productsRes.value.ok) {
        const productsData = await productsRes.value.json()
        // Transform backend data structure to match frontend expectations
        const backendProducts = productsData.products || []
        featuredProducts = backendProducts.map((product: any) => ({
          id: product.id,
          name: product.name,
          slug: product.slug,
          description: product.description,
          thumbnail: product.images?.[0] ? {
            url: product.images[0].url,
            alt: product.images[0].alt
          } : undefined,
          pricing: {
            priceRange: {
              start: {
                gross: {
                  amount: product.price?.amount || 0,
                  currency: product.price?.currency || 'USD'
                }
              }
            }
          },
          category: {
            name: product.category?.name || 'General',
            slug: product.category?.slug || 'general'
          },
          rating: 4.5, // Default rating since backend doesn't provide it
          reviews: 128, // Default reviews since backend doesn't provide it
          inStock: product.inventory?.available || true,
          featured: true
        }))
      }
      
      if (categoriesRes.status === 'fulfilled' && categoriesRes.value.ok) {
        const categoriesData = await categoriesRes.value.json()
        // Transform backend data structure to match frontend expectations
        const backendCategories = categoriesData.categories || []
        categories = backendCategories.map((category: any) => ({
          id: category.id,
          name: category.name,
          slug: category.slug,
          description: category.description,
          backgroundImage: category.image ? {
            url: category.image.url,
            alt: category.image.alt
          } : undefined,
          productsCount: category.products_count || 0
        }))
      }

      // Update with API data if available
      setHomepageData({
        ...basicData,
        featuredProducts,
        categories
      })
    } catch (error) {
      console.error('Error fetching homepage data:', error)
      // Set fallback data
      setHomepageData({
        featuredProducts: [],
        categories: [],
        heroSection: {
          title: "Smart E-commerce Solutions",
          subtitle: "Discover quality products with AI-powered sourcing and intelligent inventory management.",
          ctaText: "Shop Now",
          ctaUrl: "/products"
        },
        stats: {
          totalProducts: 10000,
          happyCustomers: 5000,
          countriesServed: 25,
          yearsExperience: 5
        }
      })
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-emerald-600"></div>
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header - CorelDove branded */}
      <Header currentPath="/" />

      {/* Hero Section */}
      <section className="py-20 lg:py-28 bg-red-50">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <Badge variant="outline" className="mb-6">
                <Package className="mr-2 h-3 w-3" />
                AI-Powered E-commerce
              </Badge>
              
              <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl mb-6">
                {homepageData?.heroSection.title.split(' ').slice(0, -1).join(' ')}{' '}
                <span className="text-red-500">{homepageData?.heroSection.title.split(' ').slice(-1)[0]}</span>
              </h1>
              
              <p className="text-lg leading-8 text-muted-foreground mb-8">
                {homepageData?.heroSection.subtitle}
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link href={homepageData?.heroSection.ctaUrl || '/products'}>
                  <Button size="lg" className="bg-red-500 hover:bg-red-600">
                    {homepageData?.heroSection.ctaText}
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Button variant="outline" size="lg">
                  <Search className="mr-2 h-4 w-4" />
                  Browse Categories
                </Button>
              </div>
            </div>
            
            <div className="relative">
              {/* Hero Images: 4 medium images in 2x2 grid */}
              <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
                <Card className="card-hover">
                  <div className="aspect-square relative overflow-hidden rounded-lg bg-muted">
                    <div className="w-full h-full image-placeholder-primary flex items-center justify-center">
                      <Package className="h-12 w-12 text-red-500" />
                    </div>
                    <Badge className="absolute top-2 right-2 bg-red-500">
                      Featured
                    </Badge>
                  </div>
                </Card>
                <Card className="card-hover">
                  <div className="aspect-square relative overflow-hidden rounded-lg bg-muted">
                    <div className="w-full h-full image-placeholder-primary flex items-center justify-center">
                      <Package className="h-12 w-12 text-red-500" />
                    </div>
                  </div>
                </Card>
                <Card className="card-hover">
                  <div className="aspect-square relative overflow-hidden rounded-lg bg-muted">
                    <div className="w-full h-full image-placeholder-primary flex items-center justify-center">
                      <Package className="h-12 w-12 text-red-500" />
                    </div>
                  </div>
                </Card>
                <Card className="card-hover">
                  <div className="aspect-square relative overflow-hidden rounded-lg bg-muted">
                    <div className="w-full h-full image-placeholder-primary flex items-center justify-center">
                      <Package className="h-12 w-12 text-red-500" />
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-red-500 text-white">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl md:text-4xl font-bold mb-2">
                {homepageData?.stats.totalProducts.toLocaleString()}+
              </div>
              <div className="text-red-100">Products</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold mb-2">
                {homepageData?.stats.happyCustomers.toLocaleString()}+
              </div>
              <div className="text-red-100">Happy Customers</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold mb-2">
                {homepageData?.stats.countriesServed}
              </div>
              <div className="text-red-100">Countries Served</div>
            </div>
            <div>
              <div className="text-3xl md:text-4xl font-bold mb-2">
                {homepageData?.stats.yearsExperience}+
              </div>
              <div className="text-red-100">Years Experience</div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section - Dynamic from Saleor */}
      {homepageData?.categories && homepageData.categories.length > 0 && (
        <section className="py-20">
          <div className="container">
            <div className="mx-auto max-w-2xl text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Shop by <span className="text-red-500">Category</span>
              </h2>
              <p className="text-lg text-muted-foreground">
                Discover our wide range of product categories
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {homepageData.categories.map((category) => (
                <Card key={category.id} className="group card-hover cursor-pointer">
                  <Link href={`/category/${category.slug}`}>
                    <div className="aspect-video relative overflow-hidden rounded-t-lg bg-muted">
                      {category.backgroundImage ? (
                        <Image
                          src={category.backgroundImage.url}
                          alt={category.backgroundImage.alt || category.name || 'Category image'}
                          fill
                          className="object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none'
                          }}
                        />
                      ) : (
                        <div className="w-full h-full image-placeholder-secondary flex items-center justify-center">
                          <div className="text-center">
                            <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mx-auto mb-2">
                              <Package className="h-8 w-8 text-blue-500" />
                            </div>
                            <span className="text-sm font-medium text-white">Category</span>
                          </div>
                        </div>
                      )}
                    </div>
                    <CardHeader>
                      <CardTitle className="text-xl">{category.name}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-muted-foreground mb-4">{category.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-red-500">
                          {category.productsCount} products
                        </span>
                        <ArrowRight className="h-4 w-4 text-red-500 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </CardContent>
                  </Link>
                </Card>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Featured Products Section - Dynamic from Saleor */}
      {homepageData?.featuredProducts && homepageData.featuredProducts.length > 0 && (
        <section className="py-20 bg-muted/30">
          <div className="container">
            <div className="mx-auto max-w-2xl text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Featured <span className="text-red-500">Products</span>
              </h2>
              <p className="text-lg text-muted-foreground">
                Handpicked products with AI-powered quality assurance
              </p>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {homepageData.featuredProducts.map((product) => (
                <Card key={product.id} className="group card-hover flex flex-col h-full">
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
                        <div className="w-full h-full image-placeholder-primary flex items-center justify-center">
                          <Package className="h-16 w-16 text-red-500" />
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
                      <div className="absolute top-2 right-2 flex flex-col gap-1">
                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 bg-white/80 hover:bg-white">
                          <Heart className="h-4 w-4" />
                        </Button>
                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0 bg-white/80 hover:bg-white">
                          <Eye className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    <CardHeader className="flex-1">
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                        <span>{product.category?.name || 'General'}</span>
                        <span>•</span>
                        <div className="flex items-center gap-1">
                          <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                          <span>{product.rating || 0}</span>
                          <span>({product.reviews || 0})</span>
                        </div>
                      </div>
                      <CardTitle className="text-lg line-clamp-2">{product.name}</CardTitle>
                    </CardHeader>
                    <CardContent className="mt-auto">
                      <p className="text-muted-foreground line-clamp-2 mb-4">{product.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-red-500">
                          {product.pricing?.priceRange?.start?.gross?.currency === 'INR' ? '₹' : '$'}
                          {product.pricing?.priceRange?.start?.gross?.amount || 'TBD'}
                        </span>
                        <Button size="sm" className="bg-red-500 hover:bg-red-600" disabled={!product.inStock}>
                          <ShoppingCart className="h-4 w-4 mr-2" />
                          {product.inStock ? 'Add to Cart' : 'Notify Me'}
                        </Button>
                      </div>
                    </CardContent>
                  </Link>
                </Card>
              ))}
            </div>
            
            <div className="text-center mt-12">
              <Link href="/products">
                <Button size="lg" variant="outline">
                  View All Products
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="py-20">
        <div className="container">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose <span className="text-red-500">CorelDove</span>
            </h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center card-hover">
              <CardHeader>
                <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
                  <Package className="h-8 w-8 text-red-500" />
                </div>
                <CardTitle className="text-xl">AI-Powered Sourcing</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Smart algorithms find and source the best products from trusted suppliers worldwide.
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center card-hover">
              <CardHeader>
                <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
                  <Truck className="h-8 w-8 text-red-500" />
                </div>
                <CardTitle className="text-xl">Fast Delivery</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Quick and reliable shipping with real-time tracking and delivery updates.
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center card-hover">
              <CardHeader>
                <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-8 w-8 text-red-500" />
                </div>
                <CardTitle className="text-xl">Quality Guarantee</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Every product undergoes AI quality checks and comes with our satisfaction guarantee.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer - CorelDove branded with improved spacing */}
      <footer className="border-t border-gray-800 bg-gray-900">
        <div className="container py-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 pt-8">
            <div>
              <h3 className="font-semibold mb-6 text-white">Shop</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/products" className="hover:text-white transition-colors">All Products</Link></li>
                <li><Link href="/categories" className="hover:text-white transition-colors">Categories</Link></li>
                <li><Link href="/deals" className="hover:text-white transition-colors">Special Deals</Link></li>
                <li><Link href="/new-arrivals" className="hover:text-white transition-colors">New Arrivals</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6 text-white">Company</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
                <li><Link href="/careers" className="hover:text-white transition-colors">Careers</Link></li>
                <li><Link href="/press" className="hover:text-white transition-colors">Press</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6 text-white">Support</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/help" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="/returns" className="hover:text-white transition-colors">Returns</Link></li>
                <li><Link href="/shipping" className="hover:text-white transition-colors">Shipping Info</Link></li>
                <li><Link href="/track" className="hover:text-white transition-colors">Track Order</Link></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6 text-white">Legal</h3>
              <ul className="space-y-3 text-sm text-gray-400">
                <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                <li><Link href="/refund" className="hover:text-white transition-colors">Refund Policy</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 pt-12 mt-12 pb-8 text-center text-sm text-gray-400">
            <p>&copy; 2024 {config.branding.companyName}. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}