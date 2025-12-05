/**
 * BizOSaaS Admin - Dropshipping Category Management
 * Allows administrators to select and manage categories for dropshipping product sourcing
 */

'use client'

import { useState, useEffect } from 'react'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Switch } from '../../components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs'
import { Alert, AlertDescription, AlertTitle } from '../../components/ui/alert'
import { 
  Package, 
  Settings, 
  Globe, 
  TrendingUp, 
  Search, 
  Filter,
  Save,
  RefreshCcw,
  CheckCircle,
  XCircle,
  AlertCircle,
  BarChart3,
  Users,
  ShoppingCart,
  Target
} from 'lucide-react'

interface DropshippingCategory {
  id: string
  name: string
  slug: string
  description: string
  marketplace: string
  products_count: number
  avg_price: number
  profit_margin_avg: number
  supplier_rating: number
  enabled: boolean
  priority: 'high' | 'medium' | 'low'
  updated_at: string
}

interface MarketplaceConfig {
  marketplace: string
  currency: string
  enabled: boolean
  min_order_value: number
  shipping_zones: string[]
  tax_rate: number
}

export default function DropshippingAdminPage() {
  const [categories, setCategories] = useState<DropshippingCategory[]>([])
  const [marketplaces, setMarketplaces] = useState<MarketplaceConfig[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMarketplace, setSelectedMarketplace] = useState('all')
  
  useEffect(() => {
    fetchDropshippingData()
  }, [])

  const fetchDropshippingData = async () => {
    try {
      setLoading(true)
      
      // Fetch categories and marketplace data
      const [categoriesRes, marketplacesRes] = await Promise.allSettled([
        fetch('/api/brain/admin/dropshipping/categories'),
        fetch('/api/brain/admin/dropshipping/marketplaces')
      ])
      
      // Process categories data
      if (categoriesRes.status === 'fulfilled' && categoriesRes.value.ok) {
        const data = await categoriesRes.value.json()
        setCategories(data.categories || [])
      } else {
        // Fallback data for development
        setCategories([
          {
            id: 'cat_mobile_accessories',
            name: 'Mobile Accessories',
            slug: 'mobile-accessories',
            description: 'Phone cases, chargers, and mobile accessories',
            marketplace: 'IN',
            products_count: 2547,
            avg_price: 299,
            profit_margin_avg: 45.2,
            supplier_rating: 4.5,
            enabled: true,
            priority: 'high',
            updated_at: '2025-01-15T10:30:00Z'
          },
          {
            id: 'cat_home_kitchen',
            name: 'Home & Kitchen',
            slug: 'home-kitchen',
            description: 'Kitchen gadgets and home essentials',
            marketplace: 'IN',
            products_count: 1854,
            avg_price: 899,
            profit_margin_avg: 38.7,
            supplier_rating: 4.3,
            enabled: true,
            priority: 'high',
            updated_at: '2025-01-15T09:45:00Z'
          },
          {
            id: 'cat_electronics',
            name: 'Electronics',
            slug: 'electronics',
            description: 'Consumer electronics and gadgets',
            marketplace: 'IN',
            products_count: 987,
            avg_price: 1299,
            profit_margin_avg: 42.1,
            supplier_rating: 4.2,
            enabled: true,
            priority: 'medium',
            updated_at: '2025-01-15T08:20:00Z'
          },
          {
            id: 'cat_fitness',
            name: 'Fitness Equipment',
            slug: 'fitness-equipment',
            description: 'Home workout equipment and accessories',
            marketplace: 'IN',
            products_count: 654,
            avg_price: 1599,
            profit_margin_avg: 35.5,
            supplier_rating: 4.1,
            enabled: false,
            priority: 'low',
            updated_at: '2025-01-14T16:10:00Z'
          },
          {
            id: 'cat_beauty',
            name: 'Beauty Products',
            slug: 'beauty-products',
            description: 'Skincare and cosmetics',
            marketplace: 'IN',
            products_count: 876,
            avg_price: 699,
            profit_margin_avg: 48.9,
            supplier_rating: 4.4,
            enabled: true,
            priority: 'medium',
            updated_at: '2025-01-15T07:30:00Z'
          }
        ])
      }
      
      // Process marketplaces data
      if (marketplacesRes.status === 'fulfilled' && marketplacesRes.value.ok) {
        const data = await marketplacesRes.value.json()
        setMarketplaces(data.marketplaces || [])
      } else {
        // Fallback marketplace data
        setMarketplaces([
          {
            marketplace: 'IN',
            currency: 'INR',
            enabled: true,
            min_order_value: 500,
            shipping_zones: ['North India', 'South India', 'West India', 'East India'],
            tax_rate: 18
          },
          {
            marketplace: 'US',
            currency: 'USD',
            enabled: false,
            min_order_value: 25,
            shipping_zones: ['Continental US', 'Alaska', 'Hawaii'],
            tax_rate: 8.5
          },
          {
            marketplace: 'UK',
            currency: 'GBP',
            enabled: false,
            min_order_value: 20,
            shipping_zones: ['England', 'Scotland', 'Wales', 'Northern Ireland'],
            tax_rate: 20
          }
        ])
      }
    } catch (error) {
      console.error('Error fetching dropshipping data:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleCategoryEnabled = (categoryId: string) => {
    setCategories(prev => prev.map(cat => 
      cat.id === categoryId ? { ...cat, enabled: !cat.enabled } : cat
    ))
  }

  const updateCategoryPriority = (categoryId: string, priority: 'high' | 'medium' | 'low') => {
    setCategories(prev => prev.map(cat => 
      cat.id === categoryId ? { ...cat, priority } : cat
    ))
  }

  const saveChanges = async () => {
    try {
      setSaving(true)
      
      // Save categories configuration
      const response = await fetch('/api/brain/admin/dropshipping/categories', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          categories: categories.map(cat => ({
            id: cat.id,
            enabled: cat.enabled,
            priority: cat.priority
          }))
        })
      })
      
      if (response.ok) {
        // Show success message
        alert('Category settings saved successfully!')
      } else {
        throw new Error('Failed to save settings')
      }
    } catch (error) {
      console.error('Error saving changes:', error)
      alert('Error saving settings. Please try again.')
    } finally {
      setSaving(false)
    }
  }

  const filteredCategories = categories.filter(cat => {
    const matchesSearch = cat.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         cat.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesMarketplace = selectedMarketplace === 'all' || cat.marketplace === selectedMarketplace
    return matchesSearch && matchesMarketplace
  })

  const enabledCategories = categories.filter(cat => cat.enabled)
  const totalProducts = categories.reduce((sum, cat) => sum + cat.products_count, 0)
  const averageMargin = categories.reduce((sum, cat) => sum + cat.profit_margin_avg, 0) / categories.length

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dropshipping Management</h1>
          <p className="text-muted-foreground">
            Configure product categories and marketplaces for dropshipping operations
          </p>
        </div>
        <Button onClick={saveChanges} disabled={saving} className="bg-green-600 hover:bg-green-700">
          {saving ? (
            <>
              <RefreshCcw className="w-4 h-4 mr-2 animate-spin" />
              Saving...
            </>
          ) : (
            <>
              <Save className="w-4 h-4 mr-2" />
              Save Changes
            </>
          )}
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Categories</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{enabledCategories.length}</div>
            <p className="text-xs text-muted-foreground">
              of {categories.length} total categories
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Products</CardTitle>
            <Package className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalProducts.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              across all categories
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Profit Margin</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{averageMargin.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              across enabled categories
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Markets</CardTitle>
            <Globe className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketplaces.filter(m => m.enabled).length}</div>
            <p className="text-xs text-muted-foreground">
              marketplaces enabled
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="categories" className="space-y-6">
        <TabsList>
          <TabsTrigger value="categories">Category Management</TabsTrigger>
          <TabsTrigger value="marketplaces">Marketplace Settings</TabsTrigger>
          <TabsTrigger value="analytics">Performance Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="categories" className="space-y-6">
          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle>Category Filters</CardTitle>
              <CardDescription>
                Filter and search through available dropshipping categories
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-4">
                <div className="flex-1">
                  <Label htmlFor="search">Search Categories</Label>
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="search"
                      placeholder="Search by name or description..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="marketplace">Marketplace</Label>
                  <select
                    id="marketplace"
                    value={selectedMarketplace}
                    onChange={(e) => setSelectedMarketplace(e.target.value)}
                    className="w-full p-2 border rounded-md"
                  >
                    <option value="all">All Marketplaces</option>
                    <option value="IN">India (IN)</option>
                    <option value="US">United States (US)</option>
                    <option value="UK">United Kingdom (UK)</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Categories List */}
          <div className="grid gap-4">
            {filteredCategories.map((category) => (
              <Card key={category.id} className={`transition-all ${category.enabled ? 'ring-2 ring-green-200' : 'opacity-75'}`}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <Switch
                        checked={category.enabled}
                        onCheckedChange={() => toggleCategoryEnabled(category.id)}
                      />
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          {category.name}
                          <Badge variant={category.enabled ? "default" : "secondary"}>
                            {category.enabled ? "Active" : "Disabled"}
                          </Badge>
                          <Badge variant="outline" className={`
                            ${category.priority === 'high' ? 'border-red-200 text-red-700' : ''}
                            ${category.priority === 'medium' ? 'border-yellow-200 text-yellow-700' : ''}
                            ${category.priority === 'low' ? 'border-gray-200 text-gray-700' : ''}
                          `}>
                            {category.priority} priority
                          </Badge>
                        </CardTitle>
                        <CardDescription>{category.description}</CardDescription>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant={category.priority === 'high' ? 'default' : 'outline'}
                        onClick={() => updateCategoryPriority(category.id, 'high')}
                      >
                        High
                      </Button>
                      <Button
                        size="sm"
                        variant={category.priority === 'medium' ? 'default' : 'outline'}
                        onClick={() => updateCategoryPriority(category.id, 'medium')}
                      >
                        Medium
                      </Button>
                      <Button
                        size="sm"
                        variant={category.priority === 'low' ? 'default' : 'outline'}
                        onClick={() => updateCategoryPriority(category.id, 'low')}
                      >
                        Low
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div className="flex items-center space-x-2">
                      <Package className="h-4 w-4 text-blue-500" />
                      <div>
                        <div className="font-semibold">{category.products_count}</div>
                        <div className="text-sm text-muted-foreground">Products</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <ShoppingCart className="h-4 w-4 text-green-500" />
                      <div>
                        <div className="font-semibold">₹{category.avg_price}</div>
                        <div className="text-sm text-muted-foreground">Avg. Price</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <TrendingUp className="h-4 w-4 text-purple-500" />
                      <div>
                        <div className="font-semibold">{category.profit_margin_avg}%</div>
                        <div className="text-sm text-muted-foreground">Profit Margin</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Users className="h-4 w-4 text-orange-500" />
                      <div>
                        <div className="font-semibold">{category.supplier_rating}/5</div>
                        <div className="text-sm text-muted-foreground">Supplier Rating</div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Globe className="h-4 w-4 text-cyan-500" />
                      <div>
                        <div className="font-semibold">{category.marketplace}</div>
                        <div className="text-sm text-muted-foreground">Marketplace</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="marketplaces" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Marketplace Configuration</CardTitle>
              <CardDescription>
                Configure supported marketplaces for dropshipping operations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {marketplaces.map((marketplace) => (
                  <div key={marketplace.marketplace} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-lg">{marketplace.marketplace} Market</h3>
                      <Switch checked={marketplace.enabled} />
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Currency:</span>
                        <div className="font-medium">{marketplace.currency}</div>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Min Order:</span>
                        <div className="font-medium">{marketplace.currency} {marketplace.min_order_value}</div>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Tax Rate:</span>
                        <div className="font-medium">{marketplace.tax_rate}%</div>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Shipping Zones:</span>
                        <div className="font-medium">{marketplace.shipping_zones.length} zones</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <Alert>
            <BarChart3 className="h-4 w-4" />
            <AlertTitle>Analytics Dashboard</AlertTitle>
            <AlertDescription>
              Detailed performance analytics and insights for dropshipping operations will be displayed here.
              This includes category performance, profit margins, supplier ratings, and market trends.
            </AlertDescription>
          </Alert>

          <Card>
            <CardHeader>
              <CardTitle>Coming Soon</CardTitle>
              <CardDescription>
                Advanced analytics and reporting features are being developed
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                This section will include:
              </p>
              <ul className="list-disc list-inside mt-2 space-y-1 text-muted-foreground">
                <li>Category performance metrics</li>
                <li>Profit margin analysis</li>
                <li>Supplier performance tracking</li>
                <li>Market trend analysis</li>
                <li>Inventory forecasting</li>
              </ul>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}