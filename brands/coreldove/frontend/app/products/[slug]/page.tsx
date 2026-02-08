/**
 * CorelDove Product Detail Page - Individual Product View
 * Integrates with Saleor backend via Brain API for detailed product information
 */

'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../../components/ui/card'
import { Badge } from '../../../components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../../components/ui/tabs'
import { useTenantTheme } from '../../../hooks/useTenantTheme'
import { useCart } from '../../../lib/stores/cart-store'
import { 
  ArrowRight, 
  ShoppingCart, 
  Star, 
  Heart,
  Share2,
  Truck,
  Shield,
  RotateCcw,
  ArrowLeft,
  Plus,
  Minus,
  Check
} from 'lucide-react'

interface ProductVariant {
  id: string
  name: string
  sku: string
  pricing: {
    price: {
      gross: {
        amount: number
        currency: string
      }
    }
  }
  quantityAvailable: number
}

interface ProductImage {
  id: string
  url: string
  alt: string
}

interface Product {
  id: string
  name: string
  slug: string
  description: string
  descriptionJson?: any
  seoTitle?: string
  seoDescription?: string
  images: ProductImage[]
  variants: ProductVariant[]
  category: {
    id: string
    name: string
    slug: string
  }
  collections: Array<{
    id: string
    name: string
    slug: string
  }>
  attributes: Array<{
    attribute: {
      name: string
      slug: string
    }
    values: Array<{
      name: string
      slug: string
    }>
  }>
  rating: number
  reviews: number
  isAvailable: boolean
  isPublished: boolean
  availableForPurchase: boolean
}

interface RelatedProduct {
  id: string
  name: string
  slug: string
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
  inStock: boolean
}

export default function ProductDetailPage({ 
  params 
}: { 
  params: { slug: string } 
}) {
  const { config } = useTenantTheme()
  const { addItem } = useCart()
  
  const [product, setProduct] = useState<Product | null>(null)
  const [relatedProducts, setRelatedProducts] = useState<RelatedProduct[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedImageIndex, setSelectedImageIndex] = useState(0)
  const [selectedVariantId, setSelectedVariantId] = useState<string>('')
  const [quantity, setQuantity] = useState(1)
  const [isAddingToCart, setIsAddingToCart] = useState(false)
  const [activeTab, setActiveTab] = useState('description')

  useEffect(() => {
    fetchProductDetails()
  }, [params.slug])

  const fetchProductDetails = async () => {
    try {
      setLoading(true)
      
      // Fetch product details
      const productResponse = await fetch(`/api/brain/saleor/products/${params.slug}`)
      
      if (productResponse.ok) {
        const productData = await productResponse.json()
        setProduct(productData.product)
        
        // Set default variant
        if (productData.product?.variants?.length > 0) {
          setSelectedVariantId(productData.product.variants[0].id)
        }

        // Fetch related products
        const relatedResponse = await fetch(`/api/brain/saleor/products?category=${productData.product.category.slug}&limit=4&exclude=${productData.product.id}`)
        if (relatedResponse.ok) {
          const relatedData = await relatedResponse.json()
          setRelatedProducts(relatedData.products || [])
        }
      } else {
        console.error('Failed to fetch product details')
      }
    } catch (error) {
      console.error('Error fetching product details:', error)
    } finally {
      setLoading(false)
    }
  }

  const selectedVariant = product?.variants.find(v => v.id === selectedVariantId) || product?.variants[0]
  const currentPrice = selectedVariant?.pricing.price.gross.amount || 0
  const currency = selectedVariant?.pricing.price.gross.currency || 'USD'
  const maxQuantity = Math.min(selectedVariant?.quantityAvailable || 0, 10)

  const handleAddToCart = async () => {
    if (!product || !selectedVariant) return
    
    setIsAddingToCart(true)
    
    try {
      addItem({
        id: `cart-${product.id}-${selectedVariantId}`,
        productId: product.id,
        name: product.name,
        slug: product.slug,
        description: product.description,
        thumbnail: product.images[0] ? {
          url: product.images[0].url,
          alt: product.images[0].alt
        } : undefined,
        pricing: {
          priceRange: {
            start: {
              gross: {
                amount: currentPrice,
                currency: currency
              }
            }
          }
        },
        category: product.category,
        inStock: selectedVariant.quantityAvailable > 0,
        maxQuantity: maxQuantity,
      })
      
      // Optional: Show success message or animation
      setTimeout(() => {
        setIsAddingToCart(false)
      }, 1000)
      
    } catch (error) {
      console.error('Error adding to cart:', error)
      setIsAddingToCart(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-500"></div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <h1 className="text-2xl font-bold mb-4">Product Not Found</h1>
        <p className="text-muted-foreground mb-6">The product you're looking for doesn't exist.</p>
        <Button asChild>
          <Link href="/products">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Products
          </Link>
        </Button>
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center">
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src={config.branding.logo}
              alt={config.branding.companyName}
              width={120}
              height={40}
              className="h-8 w-auto"
              priority
            />
          </Link>
          
          <nav className="ml-auto flex items-center space-x-6">
            <Link href="/products" className="text-sm font-medium hover:text-primary">
              Products
            </Link>
            <Link href="/categories" className="text-sm font-medium hover:text-primary">
              Categories
            </Link>
            <Link href="/about" className="text-sm font-medium hover:text-primary">
              About
            </Link>
            <Link href="/contact" className="text-sm font-medium hover:text-primary">
              Contact
            </Link>
            <Link href="/cart" className="relative">
              <ShoppingCart className="h-5 w-5" />
            </Link>
            <Link href="/auth/login">
              <Button size="sm" className="bg-red-600 hover:bg-red-700 text-white">
                Sign In
              </Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <Link href="/products" className="hover:text-foreground">Products</Link>
            <ArrowRight className="h-4 w-4" />
            <Link href={`/categories/${product.category.slug}`} className="hover:text-foreground">
              {product.category.name}
            </Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground line-clamp-1">{product.name}</span>
          </div>
        </div>
      </div>

      <main className="flex-1 py-8">
        <div className="container">
          <div className="grid lg:grid-cols-2 gap-12">
            {/* Product Images */}
            <div className="space-y-4">
              {/* Main Image */}
              <div className="aspect-square relative overflow-hidden rounded-lg border">
                {product.images[selectedImageIndex] ? (
                  <Image
                    src={product.images[selectedImageIndex].url}
                    alt={product.images[selectedImageIndex].alt || product.name || 'Product image'}
                    fill
                    className="object-cover"
                    priority
                  />
                ) : (
                  <div className="w-full h-full bg-muted flex items-center justify-center">
                    <span className="text-muted-foreground">No image available</span>
                  </div>
                )}
              </div>
              
              {/* Thumbnail Images */}
              {product.images.length > 1 && (
                <div className="grid grid-cols-4 gap-2">
                  {product.images.map((image, index) => (
                    <button
                      key={image.id}
                      onClick={() => setSelectedImageIndex(index)}
                      className={`aspect-square relative overflow-hidden rounded-md border-2 ${
                        index === selectedImageIndex ? 'border-red-500' : 'border-transparent'
                      }`}
                    >
                      <Image
                        src={image.url}
                        alt={image.alt || product.name || 'Product image'}
                        fill
                        className="object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-6">
              {/* Title and Rating */}
              <div>
                <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex items-center gap-1">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <Star
                        key={i}
                        className={`h-4 w-4 ${
                          i < Math.floor(product.rating) 
                            ? 'fill-yellow-400 text-yellow-400' 
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                    <span className="text-sm text-muted-foreground ml-2">
                      ({product.reviews} reviews)
                    </span>
                  </div>
                  <Badge variant="outline">{product.category.name}</Badge>
                </div>
              </div>

              {/* Price */}
              <div className="text-3xl font-bold text-red-500">
                ${currentPrice} {currency}
              </div>

              {/* Variants */}
              {product.variants.length > 1 && (
                <div>
                  <h3 className="font-semibold mb-2">Options:</h3>
                  <div className="flex flex-wrap gap-2">
                    {product.variants.map((variant) => (
                      <Button
                        key={variant.id}
                        variant={selectedVariantId === variant.id ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setSelectedVariantId(variant.id)}
                        disabled={variant.quantityAvailable === 0}
                      >
                        {variant.name}
                        {variant.quantityAvailable === 0 && ' (Sold Out)'}
                      </Button>
                    ))}
                  </div>
                </div>
              )}

              {/* Quantity Selector */}
              <div>
                <h3 className="font-semibold mb-2">Quantity:</h3>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    disabled={quantity <= 1}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <span className="w-12 text-center font-medium">{quantity}</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(Math.min(maxQuantity, quantity + 1))}
                    disabled={quantity >= maxQuantity}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                  <span className="text-sm text-muted-foreground ml-2">
                    {selectedVariant?.quantityAvailable} available
                  </span>
                </div>
              </div>

              {/* Add to Cart */}
              <div className="flex gap-4">
                <Button
                  onClick={handleAddToCart}
                  disabled={!selectedVariant || selectedVariant.quantityAvailable === 0 || isAddingToCart}
                  className="flex-1 bg-red-500 hover:bg-red-600"
                  size="lg"
                >
                  {isAddingToCart ? (
                    <>
                      <Check className="mr-2 h-4 w-4" />
                      Added to Cart!
                    </>
                  ) : (
                    <>
                      <ShoppingCart className="mr-2 h-4 w-4" />
                      Add to Cart
                    </>
                  )}
                </Button>
                <Button variant="outline" size="lg">
                  <Heart className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="lg">
                  <Share2 className="h-4 w-4" />
                </Button>
              </div>

              {/* Product Features */}
              <div className="grid grid-cols-3 gap-4 py-6 border-t border-b">
                <div className="text-center">
                  <Truck className="h-6 w-6 text-red-500 mx-auto mb-2" />
                  <div className="text-sm font-medium">Free Shipping</div>
                  <div className="text-xs text-muted-foreground">Orders over $50</div>
                </div>
                <div className="text-center">
                  <RotateCcw className="h-6 w-6 text-red-500 mx-auto mb-2" />
                  <div className="text-sm font-medium">Easy Returns</div>
                  <div className="text-xs text-muted-foreground">30-day policy</div>
                </div>
                <div className="text-center">
                  <Shield className="h-6 w-6 text-red-500 mx-auto mb-2" />
                  <div className="text-sm font-medium">Quality Guarantee</div>
                  <div className="text-xs text-muted-foreground">AI-verified</div>
                </div>
              </div>
            </div>
          </div>

          {/* Product Details Tabs */}
          <div className="mt-16">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="description">Description</TabsTrigger>
                <TabsTrigger value="specifications">Specifications</TabsTrigger>
                <TabsTrigger value="reviews">Reviews ({product.reviews})</TabsTrigger>
              </TabsList>
              
              <TabsContent value="description" className="mt-6">
                <Card>
                  <CardContent className="pt-6">
                    <div className="prose max-w-none">
                      <p>{product.description}</p>
                      {/* Add more detailed description content here */}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="specifications" className="mt-6">
                <Card>
                  <CardContent className="pt-6">
                    <div className="grid grid-cols-2 gap-4">
                      {product.attributes.map((attr) => (
                        <div key={attr.attribute.slug} className="border-b pb-2">
                          <div className="font-medium">{attr.attribute.name}</div>
                          <div className="text-muted-foreground">
                            {attr.values.map(v => v.name).join(', ')}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="reviews" className="mt-6">
                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center py-8">
                      <p className="text-muted-foreground">Review functionality coming soon!</p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Related Products */}
          {relatedProducts.length > 0 && (
            <div className="mt-16">
              <h2 className="text-2xl font-bold mb-8">Related Products</h2>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {relatedProducts.map((relatedProduct) => (
                  <Card key={relatedProduct.id} className="group hover:shadow-lg transition-shadow">
                    <Link href={`/products/${relatedProduct.slug}`}>
                      {relatedProduct.thumbnail && (
                        <div className="aspect-square relative overflow-hidden rounded-t-lg">
                          <Image
                            src={relatedProduct.thumbnail.url}
                            alt={relatedProduct.thumbnail.alt || relatedProduct.name || 'Related product image'}
                            fill
                            className="object-cover group-hover:scale-105 transition-transform duration-300"
                          />
                        </div>
                      )}
                      <CardHeader>
                        <CardTitle className="text-lg line-clamp-2">{relatedProduct.name}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center justify-between">
                          <span className="text-xl font-bold text-red-500">
                            ${relatedProduct.pricing.priceRange.start.gross.amount}
                          </span>
                          <Badge variant="outline">{relatedProduct.category.name}</Badge>
                        </div>
                      </CardContent>
                    </Link>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}