'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  ShoppingCart, Package, TrendingUp, Users, DollarSign, 
  ExternalLink, RefreshCw, AlertCircle, CheckCircle,
  Plus, Edit, Trash2, Eye, Settings, Brain, Zap, Shield
} from 'lucide-react'
import { FeatureGate } from '@/components/tenant/feature-gate'

interface Product {
  id: string
  name: string
  price: number
  stock: number
  status: 'active' | 'draft' | 'out_of_stock'
  image?: string
  category: string
  rating: number
  reviews: number
}

interface Supplier {
  id: string
  name: string
  location: string
  rating: number
  products: number
  verified: boolean
}

export default function CoreLDoveDashboard() {
  const [products, setProducts] = useState<Product[]>([])
  const [suppliers, setSuppliers] = useState<Supplier[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [saleorStatus, setSaleorStatus] = useState<'connecting' | 'connected' | 'error'>('connecting')
  const [aiInsights, setAiInsights] = useState({
    profitOpportunities: 0,
    trendingProducts: 0,
    supplierMatches: 0
  })

  // Load data with Saleor integration
  useEffect(() => {
    const loadData = async () => {
      try {
        // Test Saleor connection
        const healthResponse = await fetch('http://localhost:8020/health/', {
          method: 'GET',
          headers: { 'Accept': 'application/json' }
        })
        
        if (healthResponse.ok) {
          setSaleorStatus('connected')
        } else {
          setSaleorStatus('error')
        }
        
        // Load mock data for now
        setProducts([
          { id: '1', name: 'Wireless Bluetooth Earbuds Pro', price: 79.99, stock: 45, status: 'active', category: 'Electronics', rating: 4.8, reviews: 247 },
          { id: '2', name: 'Smart Phone Wireless Charger', price: 34.99, stock: 0, status: 'out_of_stock', category: 'Electronics', rating: 4.6, reviews: 183 },
          { id: '3', name: 'LED Strip Lights RGB Smart', price: 45.99, stock: 150, status: 'active', category: 'Home & Garden', rating: 4.7, reviews: 156 },
          { id: '4', name: 'Fitness Tracker Pro', price: 89.99, stock: 23, status: 'active', category: 'Health & Fitness', rating: 4.5, reviews: 92 },
        ])
        
        setSuppliers([
          { id: '1', name: 'TechSource Global', location: 'Shenzhen, China', rating: 4.8, products: 1247, verified: true },
          { id: '2', name: 'ElectroMax Ltd', location: 'Hong Kong', rating: 4.6, products: 892, verified: true },
          { id: '3', name: 'SmartTech Wholesale', location: 'Guangzhou, China', rating: 4.7, products: 2156, verified: false },
        ])
        
        setAiInsights({
          profitOpportunities: 247,
          trendingProducts: 89,
          supplierMatches: 156
        })
        
      } catch (error) {
        console.error('Error loading CoreLDove data:', error)
        setSaleorStatus('error')
      } finally {
        setIsLoading(false)
      }
    }
    
    loadData()
  }, [])

  const stats = [
    { title: 'AI Opportunities', value: aiInsights.profitOpportunities.toString(), change: '+23', icon: Brain, positive: true },
    { title: 'Active Products', value: products.filter(p => p.status === 'active').length.toString(), change: '+3', icon: Package, positive: true },
    { title: 'Verified Suppliers', value: suppliers.filter(s => s.verified).length.toString(), change: '+2', icon: Shield, positive: true },
    { title: 'Profit Margin', value: '247%', change: '+12%', icon: TrendingUp, positive: true },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">CoreLDove Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            AI-powered dropshipping and product sourcing platform
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            {saleorStatus === 'connected' ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm text-green-600">AI Engine Active</span>
              </>
            ) : saleorStatus === 'connecting' ? (
              <>
                <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />
                <span className="text-sm text-blue-600">Connecting...</span>
              </>
            ) : (
              <>
                <AlertCircle className="h-4 w-4 text-red-500" />
                <span className="text-sm text-red-600">Connection Error</span>
              </>
            )}
          </div>
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => window.open('http://localhost:3003', '_blank')}
          >
            <ExternalLink className="h-4 w-4 mr-2" />
            View Storefront
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className={`text-xs ${stat.positive ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change} from last month
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="products">AI Products</TabsTrigger>
          <TabsTrigger value="suppliers">Suppliers</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="ai-insights">AI Insights</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* AI Recommendations */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2 text-blue-600" />
                  AI Recommendations
                </CardTitle>
                <CardDescription>Latest AI-powered profit opportunities</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm font-medium text-blue-900">High-Profit Opportunity</p>
                    <p className="text-xs text-blue-700">Wireless earbuds trending +340% with 280% profit margin</p>
                    <Button size="sm" className="mt-2 bg-blue-600">Source Product</Button>
                  </div>
                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-sm font-medium text-green-900">Supplier Match</p>
                    <p className="text-xs text-green-700">New verified supplier in Shenzhen with 4.9★ rating</p>
                    <Button size="sm" variant="outline" className="mt-2">Connect</Button>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-sm font-medium text-purple-900">Market Trend</p>
                    <p className="text-xs text-purple-700">Smart home devices increasing 45% in demand</p>
                    <Button size="sm" variant="outline" className="mt-2">Explore</Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Top Products */}
            <Card>
              <CardHeader>
                <CardTitle>Top Performing Products</CardTitle>
                <CardDescription>Highest profit margin products this month</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {products.filter(p => p.status === 'active').slice(0, 3).map((product) => (
                    <div key={product.id} className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{product.name}</p>
                        <p className="text-sm text-muted-foreground">{product.category} • {product.stock} units</p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">${product.price}</p>
                        <div className="flex items-center">
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <div key={i} className={`h-2 w-2 ${i < Math.floor(product.rating) ? 'bg-yellow-400' : 'bg-gray-200'}`} />
                            ))}
                          </div>
                          <span className="text-xs text-muted-foreground ml-1">({product.reviews})</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="products">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>AI-Sourced Products</CardTitle>
                <CardDescription>Products identified and sourced by AI agents</CardDescription>
              </div>
              <FeatureGate 
                feature="ai-sourcing" 
                fallback={
                  <Button disabled>
                    <Plus className="h-4 w-4 mr-2" />
                    Source New Product (Pro)
                  </Button>
                }
              >
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  Source New Product
                </Button>
              </FeatureGate>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {products.map((product) => (
                  <div key={product.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                        <Package className="h-6 w-6 text-gray-500" />
                      </div>
                      <div>
                        <h3 className="font-medium">{product.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          ${product.price} • {product.stock} in stock • {product.category}
                        </p>
                        <div className="flex items-center mt-1">
                          <div className="flex">
                            {[...Array(5)].map((_, i) => (
                              <div key={i} className={`h-2 w-2 mr-0.5 ${i < Math.floor(product.rating) ? 'bg-yellow-400' : 'bg-gray-200'}`} />
                            ))}
                          </div>
                          <span className="text-xs text-muted-foreground ml-2">({product.reviews} reviews)</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant={
                        product.status === 'active' ? 'default' : 
                        product.status === 'out_of_stock' ? 'destructive' : 'secondary'
                      }>
                        {product.status.replace('_', ' ')}
                      </Badge>
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Edit className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="suppliers">
          <Card>
            <CardHeader>
              <CardTitle>Supplier Network</CardTitle>
              <CardDescription>AI-verified suppliers and partners</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {suppliers.map((supplier) => (
                  <div key={supplier.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-medium">{supplier.name}</h3>
                        {supplier.verified && (
                          <Badge className="bg-green-50 text-green-700">
                            <Shield className="h-3 w-3 mr-1" />
                            Verified
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {supplier.location} • {supplier.products} products • ⭐ {supplier.rating}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm">
                        View Catalog
                      </Button>
                      <Button size="sm">
                        Connect
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai-insights">
          <FeatureGate 
            feature="ai-sourcing" 
            subscriptionTier="professional"
            showUpgrade={true}
            fallback={
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="bg-gray-50">
                  <CardHeader>
                    <CardTitle className="flex items-center text-gray-500">
                      <Zap className="h-5 w-5 mr-2" />
                      AI Market Intelligence (Pro Feature)
                    </CardTitle>
                    <CardDescription>Upgrade to access advanced AI insights</CardDescription>
                  </CardHeader>
                </Card>
              </div>
            }
          >
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Zap className="h-5 w-5 mr-2 text-yellow-600" />
                    AI Market Intelligence
                  </CardTitle>
                  <CardDescription>Real-time market analysis and trends</CardDescription>
                </CardHeader>
                <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Market Growth Rate</span>
                    <span className="font-semibold text-green-600">+247%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Profit Opportunities</span>
                    <span className="font-semibold">{aiInsights.profitOpportunities}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Trending Categories</span>
                    <span className="font-semibold">Electronics, Home</span>
                  </div>
                  <div className="flex justify-between">
                    <span>AI Confidence</span>
                    <span className="font-semibold text-blue-600">94%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Automated Actions</CardTitle>
                <CardDescription>AI agent activity and automation</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm">🤖 <strong>Sourcing Agent:</strong> Found 23 new products with 200%+ margins</p>
                    <p className="text-xs text-muted-foreground">2 minutes ago</p>
                  </div>
                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-sm">📊 <strong>Analytics Agent:</strong> Market trend shift detected in fitness category</p>
                    <p className="text-xs text-muted-foreground">5 minutes ago</p>
                  </div>
                  <div className="p-3 bg-orange-50 rounded-lg">
                    <p className="text-sm">🔍 <strong>Research Agent:</strong> 3 new verified suppliers added to network</p>
                    <p className="text-xs text-muted-foreground">12 minutes ago</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
          </FeatureGate>
        </TabsContent>

        <TabsContent value="analytics">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Revenue Analytics</CardTitle>
                <CardDescription>Profit and revenue performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>This Month</span>
                    <span className="font-semibold">$24,847</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Last Month</span>
                    <span className="font-semibold">$18,432</span>
                  </div>
                  <div className="flex justify-between text-green-600">
                    <span>Growth</span>
                    <span className="font-semibold">+34.8%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg Profit Margin</span>
                    <span className="font-semibold">247%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Performance Metrics</CardTitle>
                <CardDescription>Key performance indicators</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Products Sourced</span>
                    <span className="font-semibold">1,247</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Success Rate</span>
                    <span className="font-semibold text-green-600">94.2%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Avg. ROI</span>
                    <span className="font-semibold">347%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Time to Market</span>
                    <span className="font-semibold">2.3 days</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}