"use client"

import React, { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Switch } from "@/components/ui/switch"
import { 
  Package, 
  DollarSign, 
  TrendingUp, 
  ShoppingCart, 
  Bot, 
  Globe, 
  CheckCircle, 
  AlertTriangle, 
  ExternalLink,
  RefreshCw,
  Settings,
  BarChart3,
  Target,
  Zap,
  Brain,
  Activity,
  Users
} from 'lucide-react'

interface AmazonSPAPIIntegrationProps {
  tenantId: string
}

interface AIAgentStatus {
  agent_id: string
  performance_score: number
  decisions_made_today: number
  success_rate: number
  status: 'active' | 'idle' | 'error'
}

interface ProductSourcingResult {
  sourcing_recommendations: Array<{
    asin: string
    title: string
    price: number
    estimated_profit_margin: number
    competition_level: 'low' | 'medium' | 'high'
    ai_confidence_score: number
  }>
  market_analysis: {
    total_opportunities: number
    average_margin: number
    risk_level: string
  }
}

interface PricingOptimizationResult {
  pricing_recommendations: Array<{
    asin: string
    current_price: number
    recommended_price: number
    expected_impact: string
    confidence_score: number
  }>
  strategy: string
}

interface InventoryResult {
  inventory_status: Array<{
    sku: string
    current_quantity: number
    recommended_quantity: number
    reorder_point: number
    status: 'in_stock' | 'low_stock' | 'out_of_stock'
  }>
  reorder_recommendations: Array<{
    sku: string
    quantity: number
    urgency: 'low' | 'medium' | 'high'
    estimated_cost: number
  }>
}

interface OrderAutomationResult {
  order_processing_summary: {
    total_orders_processed: number
    automated_orders: number
    manual_review_required: number
    success_rate: number
  }
  automation_level: string
}

export function AmazonSPAPIIntegration({ tenantId }: AmazonSPAPIIntegrationProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [aiAgentsStatus, setAiAgentsStatus] = useState<Record<string, AIAgentStatus>>({})
  const [productSourcingResult, setProductSourcingResult] = useState<ProductSourcingResult | null>(null)
  const [pricingOptimizationResult, setPricingOptimizationResult] = useState<PricingOptimizationResult | null>(null)
  const [inventoryResult, setInventoryResult] = useState<InventoryResult | null>(null)
  const [orderAutomationResult, setOrderAutomationResult] = useState<OrderAutomationResult | null>(null)
  const [selectedMarketplaces, setSelectedMarketplaces] = useState<string[]>(['ATVPDKIKX0DER'])
  const [budgetRange, setBudgetRange] = useState({ min: 100, max: 5000 })
  const [targetMargin, setTargetMargin] = useState(30)
  const [automationLevel, setAutomationLevel] = useState('standard')
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['Electronics'])

  const BRAIN_API_BASE = 'http://localhost:8001'

  const MARKETPLACES = {
    'ATVPDKIKX0DER': 'United States',
    'A2EUQ1WTGCTBG2': 'Canada',
    'A1AM78C64UM0Y8': 'Mexico',
    'A1F83G8C2ARO7P': 'United Kingdom',
    'A1PA6795UKMFR9': 'Germany',
    'A13V1IB3VIYZZH': 'France',
    'APJ6JRA9NG5V4': 'Italy',
    'A1RKKUPIHCS9HS': 'Spain',
    'A1VC38T7YXB528': 'Japan',
    'A39IBJ37TRP1C6': 'Australia'
  }

  const PRODUCT_CATEGORIES = [
    'Electronics', 'Smart Home', 'Fitness', 'Fashion', 'Beauty',
    'Home & Garden', 'Sports & Outdoors', 'Toys & Games', 'Books',
    'Health & Personal Care', 'Automotive', 'Tools & Hardware'
  ]

  useEffect(() => {
    checkConnectionStatus()
    if (isConnected) {
      fetchAIAgentsStatus()
    }
  }, [isConnected])

  const checkConnectionStatus = async () => {
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/integrations/amazon-sp-api/oauth/status?tenant_id=${tenantId}`)
      const data = await response.json()
      setIsConnected(data.success && data.connection_status?.is_connected)
    } catch (error) {
      console.error('Error checking connection status:', error)
      setIsConnected(false)
    }
  }

  const initiateOAuthConnection = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/integrations/amazon-sp-api/oauth/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          seller_central_url: 'https://sellercentral.amazon.com',
          redirect_uri: `${window.location.origin}/integrations/amazon-sp-api/callback`,
          state: `${tenantId}_${Date.now()}`,
          scopes: ['sellingpartner:orders', 'sellingpartner:inventory', 'sellingpartner:catalog']
        })
      })
      
      const data = await response.json()
      if (data.success) {
        window.open(data.authorization_url, '_blank', 'width=600,height=700')
      }
    } catch (error) {
      console.error('Error initiating OAuth:', error)
    }
    setLoading(false)
  }

  const fetchAIAgentsStatus = async () => {
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/brain/integrations/amazon-sp/ai-agents-status?tenant_id=${tenantId}`)
      const data = await response.json()
      if (data.success) {
        setAiAgentsStatus(data.agents)
      }
    } catch (error) {
      console.error('Error fetching AI agents status:', error)
    }
  }

  const runProductSourcingAI = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/brain/integrations/amazon-sp/ai-product-sourcing`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          marketplace_ids: selectedMarketplaces,
          budget_range: budgetRange,
          target_margin: targetMargin,
          categories: selectedCategories
        })
      })
      
      const data = await response.json()
      if (data.success) {
        setProductSourcingResult(data.agent_analysis)
      }
    } catch (error) {
      console.error('Error running product sourcing AI:', error)
    }
    setLoading(false)
  }

  const runPricingOptimizationAI = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/brain/integrations/amazon-sp/ai-pricing-optimization`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          asins: ['B08N5WRWNW', 'B07XJ8C8F5', 'B094DBJLDS'], // Sample ASINs
          strategy: 'balanced'
        })
      })
      
      const data = await response.json()
      if (data.success) {
        setPricingOptimizationResult(data.agent_analysis)
      }
    } catch (error) {
      console.error('Error running pricing optimization AI:', error)
    }
    setLoading(false)
  }

  const runInventoryManagementAI = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/brain/integrations/amazon-sp/ai-inventory-management`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          marketplace_ids: selectedMarketplaces,
          include_fba: true
        })
      })
      
      const data = await response.json()
      if (data.success) {
        setInventoryResult(data.agent_analysis)
      }
    } catch (error) {
      console.error('Error running inventory management AI:', error)
    }
    setLoading(false)
  }

  const runOrderAutomationAI = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BRAIN_API_BASE}/api/brain/integrations/amazon-sp/ai-order-automation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          filters: { status: 'Unshipped' },
          automation_level: automationLevel
        })
      })
      
      const data = await response.json()
      if (data.success) {
        setOrderAutomationResult(data.agent_analysis)
      }
    } catch (error) {
      console.error('Error running order automation AI:', error)
    }
    setLoading(false)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500'
      case 'idle': return 'bg-yellow-500'
      case 'error': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getPerformanceColor = (score: number) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getCompetitionColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'high': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getStockStatusColor = (status: string) => {
    switch (status) {
      case 'in_stock': return 'text-green-600'
      case 'low_stock': return 'text-yellow-600'
      case 'out_of_stock': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  if (!isConnected) {
    return (
      <Card className="w-full">
        <CardHeader className="text-center">
          <div className="mx-auto w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mb-4">
            <Package className="w-8 h-8 text-orange-600" />
          </div>
          <CardTitle className="text-2xl">Amazon SP-API Integration</CardTitle>
          <CardDescription>
            Connect your Amazon Seller Central account to enable AI-powered marketplace operations through the Brain API Gateway
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center space-y-4">
          <div className="bg-orange-50 p-4 rounded-lg">
            <h3 className="font-semibold text-orange-800 mb-2">🧠 AI Agent Coordination Features</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-orange-700">
              <div className="flex items-center space-x-2">
                <Bot className="w-4 h-4" />
                <span>AI Product Sourcing Agent</span>
              </div>
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4" />
                <span>AI Pricing Optimization Agent</span>
              </div>
              <div className="flex items-center space-x-2">
                <Package className="w-4 h-4" />
                <span>AI Inventory Management Agent</span>
              </div>
              <div className="flex items-center space-x-2">
                <ShoppingCart className="w-4 h-4" />
                <span>AI Order Automation Agent</span>
              </div>
            </div>
          </div>
          
          <Alert>
            <Brain className="h-4 w-4" />
            <AlertDescription>
              All Amazon operations are coordinated through our FastAPI Central Hub Brain AI Agentic API Gateway, 
              where 57+ AI agents make autonomous decisions for optimal business results.
            </AlertDescription>
          </Alert>

          <Button 
            onClick={initiateOAuthConnection} 
            disabled={loading}
            size="lg"
            className="w-full bg-orange-600 hover:bg-orange-700"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                Connecting to Amazon...
              </>
            ) : (
              <>
                <ExternalLink className="w-4 h-4 mr-2" />
                Connect Amazon Seller Central
              </>
            )}
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="w-full space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                <Package className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <CardTitle className="text-xl">Amazon SP-API Integration</CardTitle>
                <CardDescription>Brain AI Gateway Coordinated Amazon Operations</CardDescription>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                <CheckCircle className="w-3 h-3 mr-1" />
                Connected
              </Badge>
              <Button variant="outline" size="sm" onClick={fetchAIAgentsStatus}>
                <RefreshCw className="w-4 h-4 mr-1" />
                Refresh
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview" className="flex items-center space-x-1">
            <Activity className="w-4 h-4" />
            <span className="hidden sm:inline">Overview</span>
          </TabsTrigger>
          <TabsTrigger value="sourcing" className="flex items-center space-x-1">
            <Bot className="w-4 h-4" />
            <span className="hidden sm:inline">Sourcing AI</span>
          </TabsTrigger>
          <TabsTrigger value="pricing" className="flex items-center space-x-1">
            <DollarSign className="w-4 h-4" />
            <span className="hidden sm:inline">Pricing AI</span>
          </TabsTrigger>
          <TabsTrigger value="inventory" className="flex items-center space-x-1">
            <Package className="w-4 h-4" />
            <span className="hidden sm:inline">Inventory AI</span>
          </TabsTrigger>
          <TabsTrigger value="orders" className="flex items-center space-x-1">
            <ShoppingCart className="w-4 h-4" />
            <span className="hidden sm:inline">Orders AI</span>
          </TabsTrigger>
          <TabsTrigger value="settings" className="flex items-center space-x-1">
            <Settings className="w-4 h-4" />
            <span className="hidden sm:inline">Settings</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(aiAgentsStatus).map(([agentName, status]) => (
              <Card key={agentName}>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <div className={`w-2 h-2 rounded-full ${getStatusColor(status.status)}`} />
                      <span className="font-medium text-sm capitalize">
                        {agentName.replace('_', ' ')}
                      </span>
                    </div>
                    <Brain className="w-4 h-4 text-gray-400" />
                  </div>
                  <div className="space-y-1 text-xs text-gray-600">
                    <div className="flex justify-between">
                      <span>Performance:</span>
                      <span className={`font-medium ${getPerformanceColor(status.performance_score)}`}>
                        {status.performance_score}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Decisions Today:</span>
                      <span className="font-medium">{status.decisions_made_today}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Success Rate:</span>
                      <span className="font-medium text-green-600">{status.success_rate}%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="w-5 h-5" />
                <span>Active Marketplaces</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                {selectedMarketplaces.map(marketplaceId => (
                  <div key={marketplaceId} className="flex items-center space-x-2 p-2 bg-blue-50 rounded-lg">
                    <Globe className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-medium text-blue-800">
                      {MARKETPLACES[marketplaceId as keyof typeof MARKETPLACES]}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sourcing" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Bot className="w-5 h-5" />
                <span>AI Product Sourcing Agent</span>
              </CardTitle>
              <CardDescription>
                Autonomous product discovery and sourcing decisions powered by AI market analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label>Budget Range ($)</Label>
                  <div className="flex space-x-2">
                    <Input
                      type="number"
                      placeholder="Min"
                      value={budgetRange.min}
                      onChange={(e) => setBudgetRange({ ...budgetRange, min: parseInt(e.target.value) || 0 })}
                    />
                    <Input
                      type="number"
                      placeholder="Max"
                      value={budgetRange.max}
                      onChange={(e) => setBudgetRange({ ...budgetRange, max: parseInt(e.target.value) || 0 })}
                    />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label>Target Margin (%)</Label>
                  <Input
                    type="number"
                    value={targetMargin}
                    onChange={(e) => setTargetMargin(parseInt(e.target.value) || 0)}
                  />
                </div>

                <div className="space-y-2">
                  <Label>Categories</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select categories" />
                    </SelectTrigger>
                    <SelectContent>
                      {PRODUCT_CATEGORIES.map(category => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button onClick={runProductSourcingAI} disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    AI Analyzing Market Opportunities...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 mr-2" />
                    Run AI Product Sourcing Analysis
                  </>
                )}
              </Button>

              {productSourcingResult && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card className="bg-blue-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <Target className="w-4 h-4 text-blue-600" />
                          <span className="text-sm font-medium">Total Opportunities</span>
                        </div>
                        <p className="text-2xl font-bold text-blue-800">
                          {productSourcingResult.market_analysis.total_opportunities}
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-green-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <TrendingUp className="w-4 h-4 text-green-600" />
                          <span className="text-sm font-medium">Average Margin</span>
                        </div>
                        <p className="text-2xl font-bold text-green-800">
                          {productSourcingResult.market_analysis.average_margin}%
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-purple-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <BarChart3 className="w-4 h-4 text-purple-600" />
                          <span className="text-sm font-medium">Risk Level</span>
                        </div>
                        <p className="text-2xl font-bold text-purple-800 capitalize">
                          {productSourcingResult.market_analysis.risk_level}
                        </p>
                      </CardContent>
                    </Card>
                  </div>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">AI Sourcing Recommendations</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Product</TableHead>
                            <TableHead>Price</TableHead>
                            <TableHead>Est. Margin</TableHead>
                            <TableHead>Competition</TableHead>
                            <TableHead>AI Confidence</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {productSourcingResult.sourcing_recommendations.map((rec, idx) => (
                            <TableRow key={idx}>
                              <TableCell>
                                <div>
                                  <p className="font-medium">{rec.title}</p>
                                  <p className="text-xs text-gray-500">{rec.asin}</p>
                                </div>
                              </TableCell>
                              <TableCell className="font-medium">${rec.price}</TableCell>
                              <TableCell className="text-green-600 font-medium">
                                {rec.estimated_profit_margin}%
                              </TableCell>
                              <TableCell>
                                <span className={`capitalize ${getCompetitionColor(rec.competition_level)}`}>
                                  {rec.competition_level}
                                </span>
                              </TableCell>
                              <TableCell>
                                <div className="flex items-center space-x-2">
                                  <Progress value={rec.ai_confidence_score} className="w-16" />
                                  <span className="text-xs">{rec.ai_confidence_score}%</span>
                                </div>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </CardContent>
                  </Card>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pricing" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <DollarSign className="w-5 h-5" />
                <span>AI Pricing Optimization Agent</span>
              </CardTitle>
              <CardDescription>
                Dynamic pricing optimization through AI market intelligence and competitive analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button onClick={runPricingOptimizationAI} disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    AI Optimizing Pricing Strategy...
                  </>
                ) : (
                  <>
                    <TrendingUp className="w-4 h-4 mr-2" />
                    Run AI Pricing Optimization
                  </>
                )}
              </Button>

              {pricingOptimizationResult && (
                <div className="space-y-4">
                  <Alert>
                    <TrendingUp className="h-4 w-4" />
                    <AlertDescription>
                      AI Strategy: <strong className="capitalize">{pricingOptimizationResult.strategy}</strong> pricing approach recommended
                    </AlertDescription>
                  </Alert>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">Pricing Recommendations</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>ASIN</TableHead>
                            <TableHead>Current Price</TableHead>
                            <TableHead>Recommended Price</TableHead>
                            <TableHead>Expected Impact</TableHead>
                            <TableHead>Confidence</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {pricingOptimizationResult.pricing_recommendations.map((rec, idx) => (
                            <TableRow key={idx}>
                              <TableCell className="font-medium">{rec.asin}</TableCell>
                              <TableCell>${rec.current_price}</TableCell>
                              <TableCell className="text-green-600 font-medium">
                                ${rec.recommended_price}
                              </TableCell>
                              <TableCell>{rec.expected_impact}</TableCell>
                              <TableCell>
                                <div className="flex items-center space-x-2">
                                  <Progress value={rec.confidence_score} className="w-16" />
                                  <span className="text-xs">{rec.confidence_score}%</span>
                                </div>
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </CardContent>
                  </Card>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="inventory" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Package className="w-5 h-5" />
                <span>AI Inventory Management Agent</span>
              </CardTitle>
              <CardDescription>
                Predictive inventory optimization with automated reorder point management
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button onClick={runInventoryManagementAI} disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    AI Analyzing Inventory Patterns...
                  </>
                ) : (
                  <>
                    <Package className="w-4 h-4 mr-2" />
                    Run AI Inventory Analysis
                  </>
                )}
              </Button>

              {inventoryResult && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Inventory Status</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead>SKU</TableHead>
                              <TableHead>Current</TableHead>
                              <TableHead>Recommended</TableHead>
                              <TableHead>Status</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {inventoryResult.inventory_status.map((item, idx) => (
                              <TableRow key={idx}>
                                <TableCell className="font-medium">{item.sku}</TableCell>
                                <TableCell>{item.current_quantity}</TableCell>
                                <TableCell className="text-blue-600 font-medium">
                                  {item.recommended_quantity}
                                </TableCell>
                                <TableCell>
                                  <span className={`capitalize ${getStockStatusColor(item.status)}`}>
                                    {item.status.replace('_', ' ')}
                                  </span>
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader>
                        <CardTitle className="text-lg">Reorder Recommendations</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead>SKU</TableHead>
                              <TableHead>Quantity</TableHead>
                              <TableHead>Cost</TableHead>
                              <TableHead>Urgency</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {inventoryResult.reorder_recommendations.map((rec, idx) => (
                              <TableRow key={idx}>
                                <TableCell className="font-medium">{rec.sku}</TableCell>
                                <TableCell>{rec.quantity}</TableCell>
                                <TableCell>${rec.estimated_cost}</TableCell>
                                <TableCell>
                                  <Badge 
                                    variant="outline" 
                                    className={
                                      rec.urgency === 'high' ? 'text-red-600 border-red-200' :
                                      rec.urgency === 'medium' ? 'text-yellow-600 border-yellow-200' :
                                      'text-green-600 border-green-200'
                                    }
                                  >
                                    {rec.urgency}
                                  </Badge>
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="orders" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <ShoppingCart className="w-5 h-5" />
                <span>AI Order Automation Agent</span>
              </CardTitle>
              <CardDescription>
                Intelligent order processing and fulfillment workflow automation
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Automation Level</Label>
                  <Select value={automationLevel} onValueChange={setAutomationLevel}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="basic">Basic - Manual Review Required</SelectItem>
                      <SelectItem value="standard">Standard - Automated with Exceptions</SelectItem>
                      <SelectItem value="advanced">Advanced - Full Automation</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="space-y-2">
                  <Label>Order Status Filter</Label>
                  <Select defaultValue="Unshipped">
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Unshipped">Unshipped Orders</SelectItem>
                      <SelectItem value="PartiallyShipped">Partially Shipped</SelectItem>
                      <SelectItem value="Shipped">Shipped Orders</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button onClick={runOrderAutomationAI} disabled={loading} className="w-full">
                {loading ? (
                  <>
                    <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                    AI Processing Orders...
                  </>
                ) : (
                  <>
                    <ShoppingCart className="w-4 h-4 mr-2" />
                    Run AI Order Automation
                  </>
                )}
              </Button>

              {orderAutomationResult && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <Card className="bg-blue-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <ShoppingCart className="w-4 h-4 text-blue-600" />
                          <span className="text-sm font-medium">Total Processed</span>
                        </div>
                        <p className="text-2xl font-bold text-blue-800">
                          {orderAutomationResult.order_processing_summary.total_orders_processed}
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-green-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <CheckCircle className="w-4 h-4 text-green-600" />
                          <span className="text-sm font-medium">Automated</span>
                        </div>
                        <p className="text-2xl font-bold text-green-800">
                          {orderAutomationResult.order_processing_summary.automated_orders}
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-yellow-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <AlertTriangle className="w-4 h-4 text-yellow-600" />
                          <span className="text-sm font-medium">Manual Review</span>
                        </div>
                        <p className="text-2xl font-bold text-yellow-800">
                          {orderAutomationResult.order_processing_summary.manual_review_required}
                        </p>
                      </CardContent>
                    </Card>
                    
                    <Card className="bg-purple-50">
                      <CardContent className="p-4">
                        <div className="flex items-center space-x-2">
                          <BarChart3 className="w-4 h-4 text-purple-600" />
                          <span className="text-sm font-medium">Success Rate</span>
                        </div>
                        <p className="text-2xl font-bold text-purple-800">
                          {orderAutomationResult.order_processing_summary.success_rate}%
                        </p>
                      </CardContent>
                    </Card>
                  </div>

                  <Alert>
                    <Zap className="h-4 w-4" />
                    <AlertDescription>
                      Automation Level: <strong className="capitalize">{orderAutomationResult.automation_level}</strong> 
                      - AI processed {orderAutomationResult.order_processing_summary.automated_orders} orders automatically
                    </AlertDescription>
                  </Alert>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="w-5 h-5" />
                <span>Integration Settings</span>
              </CardTitle>
              <CardDescription>
                Configure Amazon SP-API integration parameters and AI agent behavior
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label>Active Marketplaces</Label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {Object.entries(MARKETPLACES).map(([id, name]) => (
                      <div key={id} className="flex items-center space-x-2">
                        <Switch
                          checked={selectedMarketplaces.includes(id)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedMarketplaces([...selectedMarketplaces, id])
                            } else {
                              setSelectedMarketplaces(selectedMarketplaces.filter(m => m !== id))
                            }
                          }}
                        />
                        <span className="text-sm">{name}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Default Product Categories</Label>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {PRODUCT_CATEGORIES.map(category => (
                      <div key={category} className="flex items-center space-x-2">
                        <Switch
                          checked={selectedCategories.includes(category)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedCategories([...selectedCategories, category])
                            } else {
                              setSelectedCategories(selectedCategories.filter(c => c !== category))
                            }
                          }}
                        />
                        <span className="text-sm">{category}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Default Automation Level</Label>
                    <Select value={automationLevel} onValueChange={setAutomationLevel}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="basic">Basic</SelectItem>
                        <SelectItem value="standard">Standard</SelectItem>
                        <SelectItem value="advanced">Advanced</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="space-y-2">
                    <Label>Default Target Margin (%)</Label>
                    <Input
                      type="number"
                      value={targetMargin}
                      onChange={(e) => setTargetMargin(parseInt(e.target.value) || 0)}
                    />
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Connection Status</h3>
                    <p className="text-sm text-gray-600">Amazon SP-API OAuth connection</p>
                  </div>
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                    <CheckCircle className="w-3 h-3 mr-1" />
                    Connected
                  </Badge>
                </div>
                
                <Button variant="outline" className="w-full mt-4">
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Refresh Connection
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}