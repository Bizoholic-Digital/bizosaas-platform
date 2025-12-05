'use client'

import React, { useState, useEffect } from 'react'
import Image from 'next/image'

interface ResistanceBandsProduct {
  id: string
  name: string
  description: string
  images: Array<{ url: string; alt: string }>
  price: { amount: number; currency: string }
  originalPrice: { amount: number; currency: string }
  discount: { percentage: number; amount: number }
  brand: string
  rating: number
  reviews: number
  specifications: any
  benefits: string[]
  workflowMetadata: any
}

export default function ResistanceBandsPage() {
  const [product, setProduct] = useState<ResistanceBandsProduct | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedImage, setSelectedImage] = useState(0)

  useEffect(() => {
    fetchProduct()
  }, [])

  const fetchProduct = async () => {
    try {
      const response = await fetch('/api/brain/saleor/resistance-bands')
      const data = await response.json()

      if (data.success) {
        setProduct(data.product)
      }
    } catch (error) {
      console.error('Error fetching resistance bands product:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Resistance Bands Product...</p>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800">Product Not Found</h2>
          <p className="text-gray-600">Unable to load the resistance bands product.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">CorelDove</h1>
              <p className="text-sm text-gray-600">Premium E-commerce Platform</p>
            </div>
            <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              ✅ Workflow Processed
            </div>
          </div>
        </div>
      </header>

      {/* Product Display */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Workflow Status Banner */}
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-5 h-5 bg-blue-400 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs">✓</span>
                </div>
              </div>
              <div className="ml-3">
                <p className="text-sm text-blue-700">
                  <strong>Amazon Workflow Status:</strong> Product successfully processed through
                  {product.workflowMetadata?.phases_completed?.length || 6}-phase automation pipeline
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-8">
            {/* Product Images */}
            <div className="space-y-4">
              <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                <Image
                  src={product.images[selectedImage]?.url || product.images[0]?.url}
                  alt={product.images[selectedImage]?.alt || product.name}
                  width={600}
                  height={600}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="flex space-x-2 overflow-x-auto">
                {product.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 ${
                      selectedImage === index ? 'border-blue-500' : 'border-gray-200'
                    }`}
                  >
                    <Image
                      src={image.url}
                      alt={image.alt}
                      width={64}
                      height={64}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            </div>

            {/* Product Details */}
            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                <p className="text-lg text-gray-600">by {product.brand}</p>
              </div>

              {/* Pricing */}
              <div className="flex items-center space-x-4">
                <span className="text-3xl font-bold text-green-600">
                  ₹{product.price.amount}
                </span>
                <span className="text-xl text-gray-500 line-through">
                  ₹{product.originalPrice.amount}
                </span>
                <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm font-medium">
                  {product.discount.percentage}% OFF
                </span>
              </div>

              {/* Rating */}
              <div className="flex items-center space-x-2">
                <div className="flex text-yellow-400">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className={i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'}>
                      ★
                    </span>
                  ))}
                </div>
                <span className="text-sm text-gray-600">
                  {product.rating} ({product.reviews.toLocaleString()} reviews)
                </span>
              </div>

              {/* Key Benefits */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Key Benefits</h3>
                <ul className="space-y-2">
                  {product.benefits.slice(0, 5).map((benefit, index) => (
                    <li key={index} className="flex items-center text-gray-700">
                      <span className="w-2 h-2 bg-green-500 rounded-full mr-3"></span>
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Specifications */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Specifications</h3>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div className="border rounded p-2">
                    <span className="font-medium">Material:</span>
                    <br />
                    {product.specifications.material}
                  </div>
                  <div className="border rounded p-2">
                    <span className="font-medium">Components:</span>
                    <br />
                    {product.specifications.components}
                  </div>
                  <div className="border rounded p-2">
                    <span className="font-medium">Weight:</span>
                    <br />
                    {product.specifications.weight}
                  </div>
                  <div className="border rounded p-2">
                    <span className="font-medium">Warranty:</span>
                    <br />
                    {product.specifications.warranty}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors">
                  Add to Cart
                </button>
                <button className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition-colors">
                  ✓ Ready for Amazon Listing
                </button>
              </div>
            </div>
          </div>

          {/* Product Description */}
          <div className="border-t p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Product Description</h2>
            <div className="prose max-w-none text-gray-700">
              {product.description.split('\n\n').map((paragraph, index) => (
                <p key={index} className="mb-4">{paragraph}</p>
              ))}
            </div>
          </div>

          {/* Workflow Metadata */}
          <div className="border-t bg-gray-50 p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Automation Workflow Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Processing Pipeline</h3>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li>✅ AI Content Generation (93+ Agents)</li>
                  <li>✅ SEO Optimization & Keyword Research</li>
                  <li>✅ Amazon Compliance Validation</li>
                  <li>✅ Image Processing & Optimization</li>
                  <li>✅ Pricing & Market Analysis</li>
                  <li>✅ Ready for Amazon API Submission</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Workflow Metadata</h3>
                <div className="text-sm text-gray-600 space-y-1">
                  <p><strong>Processed By:</strong> {product.workflowMetadata.processedBy}</p>
                  <p><strong>Version:</strong> {product.workflowMetadata.workflowVersion}</p>
                  <p><strong>Tenant:</strong> {product.workflowMetadata.tenantId}</p>
                  <p><strong>Timestamp:</strong> {new Date(product.workflowMetadata.timestamp).toLocaleDateString()}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}