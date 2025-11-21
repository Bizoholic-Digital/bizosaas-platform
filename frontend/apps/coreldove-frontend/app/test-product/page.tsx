/**
 * Test Product Page - Sports & Fitness Product from Amazon Workflow
 * This page showcases our processed product from the automated Amazon listing workflow
 */

'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'
import {
  ArrowLeft,
  Star,
  ShoppingCart,
  Heart,
  Share2,
  Package,
  Truck,
  Shield,
  CheckCircle,
  Clock,
  Award,
  Zap
} from 'lucide-react'

interface TestProduct {
  id: string
  name: string
  description: string
  images: Array<{url: string, alt: string}>
  price: {amount: number, currency: string}
  originalPrice: {amount: number, currency: string}
  discount: {percentage: number, amount: number}
  category: {name: string, slug: string}
  brand: string
  rating: number
  reviews: number
  bulletPoints: string[]
  specifications: any
  workflowData: any
  customerReviews: any[]
  shipping: any
}

export default function TestProductPage() {
  const [product, setProduct] = useState<TestProduct | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedImage, setSelectedImage] = useState(0)
  const [quantity, setQuantity] = useState(1)

  useEffect(() => {
    fetchTestProduct()
  }, [])

  const fetchTestProduct = async () => {
    try {
      const response = await fetch('/api/brain/saleor/test-product')
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.product) {
          setProduct(data.product)
        }
      }
    } catch (error) {
      console.error('Error fetching test product:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-red-600"></div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Product Not Found</h1>
          <Link href="/">
            <Button>Back to Home</Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link href="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Home
                </Button>
              </Link>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-red-500 to-red-600 rounded-lg flex items-center justify-center">
                  <Package className="h-5 w-5 text-white" />
                </div>
                <span className="text-xl font-bold text-gray-900">CoreLDove</span>
              </div>
            </div>
            <nav className="hidden md:flex items-center space-x-8">
              <Link href="/products" className="text-gray-700 hover:text-red-600">Products</Link>
              <Link href="/categories" className="text-gray-700 hover:text-red-600">Categories</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex items-center space-x-2 text-sm text-gray-500 mb-8">
          <Link href="/" className="hover:text-red-600">Home</Link>
          <span>/</span>
          <Link href="/category/sports-fitness" className="hover:text-red-600">{product.category.name}</Link>
          <span>/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        {/* Workflow Source Badge */}
        <div className="mb-6">
          <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
            <Zap className="h-3 w-3 mr-1" />
            Generated via Amazon Workflow Automation
          </Badge>
        </div>

        <div className="grid lg:grid-cols-2 gap-12">
          {/* Product Images */}
          <div className="space-y-4">
            <div className="aspect-square relative overflow-hidden rounded-lg bg-white border">
              <Image
                src={product.images[selectedImage]?.url || '/images/placeholder.jpg'}
                alt={product.images[selectedImage]?.alt || product.name}
                fill
                className="object-cover"
                priority
              />
              {product.discount.percentage > 0 && (
                <Badge className="absolute top-4 left-4 bg-red-500">
                  {product.discount.percentage}% OFF
                </Badge>
              )}
            </div>

            {/* Image Thumbnails */}
            <div className="grid grid-cols-4 gap-2">
              {product.images.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`aspect-square relative overflow-hidden rounded-lg border-2 ${
                    selectedImage === index ? 'border-red-500' : 'border-gray-200'
                  }`}
                >
                  <Image
                    src={image.url}
                    alt={image.alt}
                    fill
                    className="object-cover"
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            <div>
              <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
                <span>{product.brand}</span>
                <span>•</span>
                <span>{product.category.name}</span>
              </div>

              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                {product.name}
              </h1>

              <div className="flex items-center gap-4 mb-4">
                <div className="flex items-center gap-1">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-5 w-5 ${
                        i < Math.floor(product.rating)
                          ? 'fill-yellow-400 text-yellow-400'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                  <span className="text-lg font-semibold">{product.rating}</span>
                </div>
                <span className="text-gray-500">({product.reviews.toLocaleString()} reviews)</span>
              </div>

              <div className="flex items-center gap-4 mb-6">
                <span className="text-3xl font-bold text-red-600">
                  ₹{product.price.amount.toLocaleString()}
                </span>
                {product.originalPrice.amount > product.price.amount && (
                  <span className="text-xl text-gray-500 line-through">
                    ₹{product.originalPrice.amount.toLocaleString()}
                  </span>
                )}
                {product.discount.percentage > 0 && (
                  <Badge variant="destructive">
                    Save ₹{product.discount.amount}
                  </Badge>
                )}
              </div>
            </div>

            {/* Key Features */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Key Features</h3>
              <ul className="space-y-2">
                {product.bulletPoints.slice(0, 4).map((point, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{point}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Add to Cart Section */}
            <div className="border-t pt-6">
              <div className="flex items-center gap-4 mb-4">
                <label className="text-sm font-medium">Quantity:</label>
                <select
                  value={quantity}
                  onChange={(e) => setQuantity(Number(e.target.value))}
                  className="border border-gray-300 rounded-md px-3 py-1"
                >
                  {[...Array(10)].map((_, i) => (
                    <option key={i + 1} value={i + 1}>{i + 1}</option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3 mb-4">
                <Button size="lg" className="flex-1 bg-red-600 hover:bg-red-700">
                  <ShoppingCart className="h-5 w-5 mr-2" />
                  Add to Cart
                </Button>
                <Button size="lg" variant="outline">
                  <Heart className="h-5 w-5" />
                </Button>
                <Button size="lg" variant="outline">
                  <Share2 className="h-5 w-5" />
                </Button>
              </div>

              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Truck className="h-4 w-4" />
                  <span>{product.shipping.estimatedDelivery} delivery</span>
                </div>
                <div className="flex items-center gap-2">
                  <Shield className="h-4 w-4" />
                  <span>30-day return policy</span>
                </div>
                <div className="flex items-center gap-2">
                  <Award className="h-4 w-4" />
                  <span>Quality guaranteed</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Product Details Tabs */}
        <div className="mt-16">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button className="border-b-2 border-red-500 py-2 px-1 text-sm font-medium text-red-600">
                Description
              </button>
              <button className="border-transparent py-2 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Specifications
              </button>
              <button className="border-transparent py-2 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Reviews
              </button>
              <button className="border-transparent py-2 px-1 text-sm font-medium text-gray-500 hover:text-gray-700">
                Workflow Data
              </button>
            </nav>
          </div>

          <div className="py-8">
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed">
                {product.description}
              </p>
            </div>
          </div>
        </div>

        {/* Workflow Information Card */}
        <Card className="mt-8 bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-blue-600" />
              Amazon Workflow Automation Details
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <strong>Source ASIN:</strong> {product.workflowData.sourceASIN}
              </div>
              <div>
                <strong>Processing Time:</strong> {product.workflowData.processingTime}
              </div>
              <div>
                <strong>Source Price:</strong> ₹{product.workflowData.sourcePrice}
              </div>
              <div>
                <strong>Profit Margin:</strong> {product.workflowData.profitMargin}%
              </div>
              <div>
                <strong>Quality Score:</strong> {product.workflowData.qualityScore}/100
              </div>
              <div>
                <strong>Workflow ID:</strong> {product.workflowData.workflowId}
              </div>
            </div>
            <div className="mt-4 p-3 bg-green-100 rounded-lg">
              <p className="text-green-800 text-sm">
                <CheckCircle className="h-4 w-4 inline mr-2" />
                This product was automatically sourced from Amazon, enhanced with AI-generated content,
                optimized for pricing and SEO, and prepared for listing on CorelDove.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Call to Action */}
        <div className="mt-12 text-center bg-red-600 text-white rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-4">Ready to List on Amazon?</h2>
          <p className="text-red-100 mb-6">
            This product has been processed through our automated workflow and is ready for Amazon submission.
          </p>
          <div className="flex justify-center gap-4">
            <Button size="lg" variant="secondary">
              Submit to Amazon SP-API
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-red-600">
              Download CSV Export
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}