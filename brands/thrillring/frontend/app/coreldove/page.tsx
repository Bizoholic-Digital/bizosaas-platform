'use client'

/*
CoreLDove Main Dashboard
AI-powered dropshipping automation with human-in-the-loop approval workflow
*/

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { Progress } from '@/components/ui/progress'
import { 
  ShoppingCart, 
  Search, 
  Star, 
  TrendingUp, 
  DollarSign, 
  Package, 
  CheckCircle, 
  XCircle, 
  Clock, 
  BarChart3, 
  Zap,
  Globe,
  Eye,
  ThumbsUp,
  ThumbsDown,
  Filter,
  RefreshCw,
  Play,
  Pause
} from 'lucide-react'

interface ProductInsight {
  product_id: string
  amazon_rating: number
  review_count: number
  seller_rating: number
  price_usd: number
  estimated_margin: number
  demand_score: number
  trending_score: number
  competition_level: 'low' | 'medium' | 'high'
  seasonal_factor: number
  key_features: string[]
  pros: string[]
  cons: string[]
  target_audience: string
  market_potential: 'low' | 'moderate' | 'high' | 'very_high'
}

interface SourcedProduct {
  id: string
  amazon_asin: string
  title: string
  description: string
  category: string
  price_usd: number
  rating: number
  review_count: number
  images: string[]
  features: string[]
  seller_info: any
  dropship_eligible: boolean
  insights: ProductInsight
  status: string
  tenant_id: string
  sourced_at: string
}

const CATEGORIES = [
  { value: 'sports', label: 'Sports Equipment' },
  { value: 'fitness', label: 'Fitness & Exercise' },
  { value: 'health', label: 'Health Products' },
  { value: 'wellness', label: 'Wellness & Recovery' },
  { value: 'nutrition', label: 'Sports Nutrition' },
  { value: 'outdoor', label: 'Outdoor Activities' },
  { value: 'gym_equipment', label: 'Gym Equipment' },
  { value: 'yoga', label: 'Yoga & Meditation' },
  { value: 'running', label: 'Running & Athletics' },
  { value: 'cycling', label: 'Cycling & Bikes' }
]

const PUBLISHING_PLATFORMS = [
  { value: 'saleor', label: 'CoreLDove Store (Saleor)', enabled: true },
  { value: 'amazon', label: 'Amazon Marketplace', enabled: true },
  { value: 'flipkart', label: 'Flipkart', enabled: true },
  { value: 'shopsy', label: 'Shopsy', enabled: true },
  { value: 'facebook', label: 'Facebook Shop', enabled: true },
  { value: 'instagram', label: 'Instagram Shopping', enabled: true },
  { value: 'whatsapp', label: 'WhatsApp Business', enabled: true },
  { value: 'google', label: 'Google Shopping', enabled: true }
]

export default function CoreLDoveDashboard() {
  const [activeTab, setActiveTab] = useState('sourcing')
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['sports', 'fitness'])
  const [maxProducts, setMaxProducts] = useState(50)
  const [minRating, setMinRating] = useState(4.0)
  const [maxPrice, setMaxPrice] = useState(500)
  const [minReviews, setMinReviews] = useState(100)
  const [sourcingInProgress, setSourcingInProgress] = useState(false)
  const [sourcedProducts, setSourcedProducts] = useState<SourcedProduct[]>([])
  const [selectedProducts, setSelectedProducts] = useState<string[]>([])
  const [processedProducts, setProcessedProducts] = useState<any[]>([])
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['saleor', 'amazon', 'flipkart'])
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterCategory, setFilterCategory] = useState<string>('all')

  // Mock data for demonstration
  useEffect(() => {
    if (activeTab === 'products' && sourcedProducts.length === 0) {
      // Simulate sourced products
      const mockProducts: SourcedProduct[] = [
        {
          id: 'prod-1',
          amazon_asin: 'B08XYZ123',
          title: 'Professional Resistance Bands Set with Door Anchor',
          description: 'Complete resistance training system with 5 resistance levels',
          category: 'fitness',
          price_usd: 29.99,
          rating: 4.5,
          review_count: 2847,
          images: ['/api/placeholder/300/300'],
          features: ['5 resistance levels', 'Door anchor included', 'Exercise guide'],
          seller_info: { rating: 4.8, name: 'FitnessGear Pro' },
          dropship_eligible: true,
          insights: {
            product_id: 'prod-1',
            amazon_rating: 4.5,
            review_count: 2847,
            seller_rating: 4.8,
            price_usd: 29.99,
            estimated_margin: 35.5,
            demand_score: 87.5,
            trending_score: 92.3,
            competition_level: 'medium',
            seasonal_factor: 1.2,
            key_features: ['Versatile training', 'Compact storage', 'Professional grade'],
            pros: ['High quality materials', 'Great customer reviews', 'Fast shipping'],
            cons: ['Higher price point', 'Medium competition'],
            target_audience: 'Home fitness enthusiasts, gym beginners',
            market_potential: 'high'
          },
          status: 'sourced',
          tenant_id: 'tenant-1',
          sourced_at: new Date().toISOString()
        },
        {
          id: 'prod-2',
          amazon_asin: 'B09ABC456',
          title: 'Smart Fitness Tracker with Heart Rate Monitor',
          description: 'Advanced fitness tracking with 24/7 health monitoring',
          category: 'health',
          price_usd: 89.99,
          rating: 4.3,
          review_count: 1523,
          images: ['/api/placeholder/300/300'],
          features: ['Heart rate monitoring', 'Sleep tracking', 'Water resistant'],
          seller_info: { rating: 4.6, name: 'TechFit Solutions' },
          dropship_eligible: true,
          insights: {
            product_id: 'prod-2',
            amazon_rating: 4.3,
            review_count: 1523,
            seller_rating: 4.6,
            price_usd: 89.99,
            estimated_margin: 28.7,
            demand_score: 78.9,
            trending_score: 95.1,
            competition_level: 'high',
            seasonal_factor: 1.0,
            key_features: ['Smart technology', 'Health monitoring', 'Long battery life'],
            pros: ['Popular category', 'High demand', 'Good margins'],
            cons: ['High competition', 'Technology updates needed'],
            target_audience: 'Health-conscious individuals, fitness enthusiasts',
            market_potential: 'very_high'
          },
          status: 'sourced',
          tenant_id: 'tenant-1',
          sourced_at: new Date().toISOString()
        }
      ]
      setSourcedProducts(mockProducts)
    }
  }, [activeTab, sourcedProducts.length])

  const handleStartSourcing = async () => {
    setSourcingInProgress(true)
    
    try {
      // Simulate API call to start sourcing
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Switch to products tab to show results
      setActiveTab('products')
      setSourcingInProgress(false)
    } catch (error) {
      console.error('Sourcing failed:', error)
      setSourcingInProgress(false)
    }
  }

  const handleApproveProducts = async (action: 'approve' | 'reject') => {
    if (selectedProducts.length === 0) return

    try {
      // Simulate approval process
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      if (action === 'approve') {
        // Move to processed tab
        setActiveTab('processed')
      }
      
      // Clear selection
      setSelectedProducts([])
    } catch (error) {
      console.error('Approval failed:', error)
    }
  }

  const handlePublishProducts = async () => {
    if (processedProducts.length === 0) return

    try {
      // Simulate publishing process
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Move to published tab
      setActiveTab('published')
    } catch (error) {
      console.error('Publishing failed:', error)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getCompetitionColor = (level: string) => {
    switch (level) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredProducts = sourcedProducts.filter(product => {
    if (filterStatus !== 'all' && product.status !== filterStatus) return false
    if (filterCategory !== 'all' && product.category !== filterCategory) return false
    return true
  })

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">CoreLDove AI Sourcing</h1>
          <p className="text-gray-600 mt-1">AI-powered dropshipping automation platform</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="bg-blue-50">
            <Zap className="h-3 w-3 mr-1" />
            AI-Powered
          </Badge>
          <Badge variant="outline" className="bg-green-50">
            <Globe className="h-3 w-3 mr-1" />
            Multi-Platform
          </Badge>
        </div>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="sourcing" className="flex items-center">
            <Search className="h-4 w-4 mr-2" />
            Product Sourcing
          </TabsTrigger>
          <TabsTrigger value="products" className="flex items-center">
            <Package className="h-4 w-4 mr-2" />
            Sourced Products
          </TabsTrigger>
          <TabsTrigger value="processed" className="flex items-center">
            <Eye className="h-4 w-4 mr-2" />
            Content Preview
          </TabsTrigger>
          <TabsTrigger value="published" className="flex items-center">
            <Globe className="h-4 w-4 mr-2" />
            Published Products
          </TabsTrigger>
          <TabsTrigger value="analytics" className="flex items-center">
            <BarChart3 className="h-4 w-4 mr-2" />
            Analytics
          </TabsTrigger>
        </TabsList>

        {/* Product Sourcing Tab */}
        <TabsContent value="sourcing" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Search className="h-5 w-5 mr-2" />
                AI Product Sourcing Configuration
              </CardTitle>
              <CardDescription>
                Configure your automated product sourcing preferences for sports, fitness, health and wellness categories
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Category Selection */}
              <div className="space-y-3">
                <Label className="text-sm font-medium">Target Categories</Label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {CATEGORIES.map((category) => (
                    <div key={category.value} className="flex items-center space-x-2">
                      <Checkbox
                        id={category.value}
                        checked={selectedCategories.includes(category.value)}
                        onCheckedChange={(checked) => {
                          if (checked) {
                            setSelectedCategories([...selectedCategories, category.value])
                          } else {
                            setSelectedCategories(selectedCategories.filter(c => c !== category.value))
                          }
                        }}
                      />
                      <Label htmlFor={category.value} className="text-sm">
                        {category.label}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Sourcing Parameters */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="maxProducts">Max Products</Label>
                  <Input
                    id="maxProducts"
                    type="number"
                    value={maxProducts}
                    onChange={(e) => setMaxProducts(parseInt(e.target.value))}
                    min={1}
                    max={500}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="minRating">Min Rating</Label>
                  <Input
                    id="minRating"
                    type="number"
                    value={minRating}
                    onChange={(e) => setMinRating(parseFloat(e.target.value))}
                    min={1}
                    max={5}
                    step={0.1}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="maxPrice">Max Price ($)</Label>
                  <Input
                    id="maxPrice"
                    type="number"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(parseInt(e.target.value))}
                    min={1}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="minReviews">Min Reviews</Label>
                  <Input
                    id="minReviews"
                    type="number"
                    value={minReviews}
                    onChange={(e) => setMinReviews(parseInt(e.target.value))}
                    min={1}
                  />
                </div>
              </div>

              {/* Dropship Settings */}
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox id="dropshipOnly" checked={true} disabled />
                  <Label htmlFor="dropshipOnly" className="text-sm">
                    Only show dropship-eligible products
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="aiInsights" checked={true} disabled />
                  <Label htmlFor="aiInsights" className="text-sm">
                    Generate AI-powered market insights
                  </Label>
                </div>
              </div>

              {/* Start Sourcing */}
              <div className="flex items-center justify-between pt-4 border-t">
                <div className="text-sm text-gray-600">
                  Selected categories: {selectedCategories.length} | Est. time: 10-15 minutes
                </div>
                <Button
                  onClick={handleStartSourcing}
                  disabled={sourcingInProgress || selectedCategories.length === 0}
                  size="lg"
                  className="flex items-center"
                >
                  {sourcingInProgress ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Sourcing Products...
                    </>
                  ) : (
                    <>
                      <Play className="h-4 w-4 mr-2" />
                      Start AI Sourcing
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Sourced Products Tab */}
        <TabsContent value="products" className="space-y-6">
          {/* Filters and Actions */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Products</SelectItem>
                  <SelectItem value="sourced">Sourced</SelectItem>
                  <SelectItem value="pending_approval">Pending</SelectItem>
                  <SelectItem value="approved">Approved</SelectItem>
                  <SelectItem value="rejected">Rejected</SelectItem>
                </SelectContent>
              </Select>

              <Select value={filterCategory} onValueChange={setFilterCategory}>
                <SelectTrigger className="w-[150px]">
                  <SelectValue placeholder="Filter by category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {CATEGORIES.map(cat => (
                    <SelectItem key={cat.value} value={cat.value}>{cat.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                onClick={() => handleApproveProducts('reject')}
                disabled={selectedProducts.length === 0}
                className="text-red-600 hover:text-red-700"
              >
                <XCircle className="h-4 w-4 mr-2" />
                Reject Selected ({selectedProducts.length})
              </Button>
              <Button
                onClick={() => handleApproveProducts('approve')}
                disabled={selectedProducts.length === 0}
                className="bg-green-600 hover:bg-green-700"
              >
                <CheckCircle className="h-4 w-4 mr-2" />
                Approve Selected ({selectedProducts.length})
              </Button>
            </div>
          </div>

          {/* Products Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredProducts.map((product) => (
              <Card key={product.id} className="hover:shadow-lg transition-shadow">
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <Checkbox
                          checked={selectedProducts.includes(product.id)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedProducts([...selectedProducts, product.id])
                            } else {
                              setSelectedProducts(selectedProducts.filter(id => id !== product.id))
                            }
                          }}
                        />
                        <Badge variant="outline">
                          {CATEGORIES.find(c => c.value === product.category)?.label}
                        </Badge>
                        <Badge className={getCompetitionColor(product.insights.competition_level)}>
                          {product.insights.competition_level} competition
                        </Badge>
                      </div>
                      <h3 className="font-semibold text-lg leading-tight">{product.title}</h3>
                      <p className="text-gray-600 text-sm mt-1 line-clamp-2">{product.description}</p>
                    </div>
                    <div className="ml-4">
                      <img
                        src={product.images[0] || '/api/placeholder/80/80'}
                        alt={product.title}
                        className="w-20 h-20 object-cover rounded-lg"
                      />
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Key Metrics */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="flex items-center space-x-2">
                      <DollarSign className="h-4 w-4 text-green-600" />
                      <div>
                        <div className="font-semibold">${product.price_usd}</div>
                        <div className="text-xs text-gray-600">
                          {product.insights.estimated_margin.toFixed(1)}% margin
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Star className="h-4 w-4 text-yellow-500" />
                      <div>
                        <div className="font-semibold">{product.rating}</div>
                        <div className="text-xs text-gray-600">
                          {product.review_count.toLocaleString()} reviews
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* AI Insights */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span>Demand Score</span>
                      <span className={`font-semibold ${getScoreColor(product.insights.demand_score)}`}>
                        {product.insights.demand_score.toFixed(1)}/100
                      </span>
                    </div>
                    <Progress value={product.insights.demand_score} className="h-2" />
                    
                    <div className="flex items-center justify-between text-sm">
                      <span>Trending Score</span>
                      <span className={`font-semibold ${getScoreColor(product.insights.trending_score)}`}>
                        {product.insights.trending_score.toFixed(1)}/100
                      </span>
                    </div>
                    <Progress value={product.insights.trending_score} className="h-2" />
                  </div>

                  {/* Market Analysis */}
                  <div className="pt-2 border-t">
                    <div className="text-sm text-gray-700 mb-2">
                      <span className="font-medium">Target Audience:</span> {product.insights.target_audience}
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {product.insights.key_features.slice(0, 3).map((feature, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {feature}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Other tabs would be implemented similarly */}
        <TabsContent value="processed" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Content Generation & Preview</CardTitle>
              <CardDescription>
                Review AI-generated content, enhanced images, and SEO optimization before publishing
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <Clock className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Content Generation in Progress</h3>
                <p className="text-gray-600 mb-4">
                  AI agents are working on keyword research, content generation, and image enhancement
                </p>
                <div className="max-w-md mx-auto">
                  <Progress value={65} className="h-3" />
                  <p className="text-sm text-gray-500 mt-2">Estimated completion: 5 minutes</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="published" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Multi-Platform Publishing</CardTitle>
              <CardDescription>
                Publish approved products across all selected platforms
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Platform Selection */}
              <div>
                <Label className="text-sm font-medium mb-3 block">Publishing Platforms</Label>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {PUBLISHING_PLATFORMS.map((platform) => (
                    <div key={platform.value} className="flex items-center space-x-2">
                      <Checkbox
                        id={platform.value}
                        checked={selectedPlatforms.includes(platform.value)}
                        onCheckedChange={(checked) => {
                          if (checked) {
                            setSelectedPlatforms([...selectedPlatforms, platform.value])
                          } else {
                            setSelectedPlatforms(selectedPlatforms.filter(p => p !== platform.value))
                          }
                        }}
                        disabled={!platform.enabled}
                      />
                      <Label htmlFor={platform.value} className="text-sm">
                        {platform.label}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>

              <Button onClick={handlePublishProducts} size="lg" className="w-full">
                <Globe className="h-4 w-4 mr-2" />
                Publish to Selected Platforms ({selectedPlatforms.length})
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Products Sourced</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-blue-600">247</div>
                <p className="text-sm text-gray-600">+23% from last week</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Avg. Success Rate</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-600">78.5%</div>
                <p className="text-sm text-gray-600">Sourcing to approval</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Est. Revenue</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-purple-600">$12.4k</div>
                <p className="text-sm text-gray-600">From published products</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}