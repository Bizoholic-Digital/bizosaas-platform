'use client'

import { useState, useEffect } from 'react'
import { Search, Filter, Package, TrendingUp, Star, ShoppingCart, Download } from 'lucide-react'

interface ProductSourcingRequest {
  query: string
  category: string
  minPrice: number
  maxPrice: number
  minRating: number
  limit: number
}

interface SourcedProduct {
  asin: string
  title: string
  price: string
  currency: string
  image_url: string
  category: string
  rating: number
  review_count: number
  features: string[]
  availability: string
}

const CategorySourcingInterface = () => {
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['fitness'])
  const [sourcingRequest, setSourcingRequest] = useState<ProductSourcingRequest>({
    query: 'fitness equipment',
    category: 'fitness',
    minPrice: 500,
    maxPrice: 10000,
    minRating: 4.0,
    limit: 10
  })
  const [sourcedProducts, setSourcedProducts] = useState<SourcedProduct[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedForPublish, setSelectedForPublish] = useState<string[]>([])

  // Health, Fitness, Sports & Wellness Categories
  const categories = [
    { id: 'fitness', name: 'Fitness Equipment', icon: '🏋️', color: 'bg-red-100 text-red-800' },
    { id: 'yoga', name: 'Yoga & Meditation', icon: '🧘', color: 'bg-purple-100 text-purple-800' },
    { id: 'sports', name: 'Sports Equipment', icon: '⚽', color: 'bg-blue-100 text-blue-800' },
    { id: 'running', name: 'Running & Athletics', icon: '🏃', color: 'bg-green-100 text-green-800' },
    { id: 'cycling', name: 'Cycling & Bikes', icon: '🚴', color: 'bg-yellow-100 text-yellow-800' },
    { id: 'nutrition', name: 'Sports Nutrition', icon: '🥤', color: 'bg-orange-100 text-orange-800' },
    { id: 'health', name: 'Health Products', icon: '💊', color: 'bg-pink-100 text-pink-800' },
    { id: 'wellness', name: 'Wellness & Recovery', icon: '🌿', color: 'bg-teal-100 text-teal-800' },
    { id: 'outdoor', name: 'Outdoor Activities', icon: '🏔️', color: 'bg-indigo-100 text-indigo-800' },
    { id: 'gym_equipment', name: 'Gym Equipment', icon: '🏃‍♂️', color: 'bg-gray-100 text-gray-800' }
  ]

  // Source products from Amazon API
  const sourceProducts = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8082/sourcing/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sourcingRequest)
      })
      
      if (response.ok) {
        const products = await response.json()
        setSourcedProducts(products)
      } else {
        console.error('Failed to source products')
      }
    } catch (error) {
      console.error('Error sourcing products:', error)
    }
    setLoading(false)
  }

  // Handle category selection
  const toggleCategory = (categoryId: string) => {
    const updatedCategories = selectedCategories.includes(categoryId)
      ? selectedCategories.filter(id => id !== categoryId)
      : [...selectedCategories, categoryId]
    
    setSelectedCategories(updatedCategories)
    setSourcingRequest(prev => ({
      ...prev,
      category: updatedCategories[0] || 'fitness',
      query: `${updatedCategories.join(' ')} products`
    }))
  }

  // Handle product selection for publishing
  const toggleProductSelection = (asin: string) => {
    setSelectedForPublish(prev =>
      prev.includes(asin)
        ? prev.filter(id => id !== asin)
        : [...prev, asin]
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          AI Product Sourcing Dashboard
        </h1>
        <p className="text-gray-600">
          Source premium health, fitness, sports & wellness products from Amazon India marketplace
        </p>
      </div>

      {/* Category Selection */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <Filter className="mr-2 h-5 w-5" />
          Select Categories to Source
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => toggleCategory(category.id)}
              className={`p-3 rounded-lg border-2 transition-all ${
                selectedCategories.includes(category.id)
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="text-center">
                <span className="text-2xl mb-1 block">{category.icon}</span>
                <span className="text-sm font-medium">{category.name}</span>
                {selectedCategories.includes(category.id) && (
                  <div className="mt-2">
                    <span className={`inline-block px-2 py-1 rounded-full text-xs ${category.color}`}>
                      Selected
                    </span>
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Sourcing Parameters */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <Search className="mr-2 h-5 w-5" />
          Sourcing Parameters
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Search Query</label>
            <input
              type="text"
              value={sourcingRequest.query}
              onChange={(e) => setSourcingRequest(prev => ({ ...prev, query: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter product keywords..."
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Min Price (₹)</label>
            <input
              type="number"
              value={sourcingRequest.minPrice}
              onChange={(e) => setSourcingRequest(prev => ({ ...prev, minPrice: Number(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Max Price (₹)</label>
            <input
              type="number"
              value={sourcingRequest.maxPrice}
              onChange={(e) => setSourcingRequest(prev => ({ ...prev, maxPrice: Number(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Products Limit</label>
            <select
              value={sourcingRequest.limit}
              onChange={(e) => setSourcingRequest(prev => ({ ...prev, limit: Number(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value={5}>5 products</option>
              <option value={10}>10 products</option>
              <option value={15}>15 products</option>
              <option value={20}>20 products</option>
            </select>
          </div>
        </div>
        <div className="mt-6">
          <button
            onClick={sourceProducts}
            disabled={loading || selectedCategories.length === 0}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center font-semibold"
          >
            {loading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            ) : (
              <Search className="mr-2 h-4 w-4" />
            )}
            {loading ? 'Sourcing Products...' : 'Source Products from Amazon India'}
          </button>
        </div>
      </div>

      {/* Sourced Products Results */}
      {sourcedProducts.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold flex items-center">
              <Package className="mr-2 h-5 w-5" />
              Sourced Products ({sourcedProducts.length})
            </h2>
            <div className="flex space-x-3">
              <button
                onClick={() => setSelectedForPublish(sourcedProducts.map(p => p.asin))}
                className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 text-sm font-medium"
              >
                Select All
              </button>
              <button
                onClick={() => setSelectedForPublish([])}
                className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 text-sm font-medium"
              >
                Clear Selection
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sourcedProducts.map(product => (
              <div key={product.asin} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="relative">
                  <div className="aspect-square bg-gray-100 rounded-md mb-3 flex items-center justify-center">
                    <Package className="h-12 w-12 text-gray-400" />
                  </div>
                  <button
                    onClick={() => toggleProductSelection(product.asin)}
                    className={`absolute top-2 right-2 p-1 rounded-full ${
                      selectedForPublish.includes(product.asin)
                        ? 'bg-green-500 text-white'
                        : 'bg-white text-gray-600 border'
                    }`}
                  >
                    <ShoppingCart className="h-4 w-4" />
                  </button>
                </div>
                
                <h3 className="font-semibold text-sm mb-2 line-clamp-2">{product.title}</h3>
                
                <div className="flex items-center justify-between mb-2">
                  <span className="text-lg font-bold text-green-600">
                    ₹{product.price}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    categories.find(c => c.id === product.category)?.color || 'bg-gray-100 text-gray-800'
                  }`}>
                    {product.category}
                  </span>
                </div>
                
                <div className="flex items-center mb-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`h-3 w-3 ${
                          i < Math.floor(product.rating)
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <span className="text-xs text-gray-500 ml-2">
                    {product.rating} ({product.review_count})
                  </span>
                </div>
                
                <div className="space-y-1 mb-3">
                  {product.features.slice(0, 2).map((feature, index) => (
                    <div key={index} className="text-xs text-gray-600">
                      • {feature}
                    </div>
                  ))}
                </div>
                
                <div className="text-xs text-green-600 font-medium">
                  {product.availability}
                </div>
              </div>
            ))}
          </div>

          {/* Bulk Actions */}
          {selectedForPublish.length > 0 && (
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-blue-800">
                  {selectedForPublish.length} products selected for publishing
                </span>
                <div className="flex space-x-3">
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm font-medium flex items-center">
                    <Download className="mr-2 h-4 w-4" />
                    Export Selected
                  </button>
                  <button className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 text-sm font-medium flex items-center">
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Publish to Store
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CategorySourcingInterface