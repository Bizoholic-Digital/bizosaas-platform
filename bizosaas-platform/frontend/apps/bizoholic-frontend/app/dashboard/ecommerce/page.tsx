'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  ShoppingCart, Package, TrendingUp, Users, DollarSign, 
  ExternalLink, RefreshCw, AlertCircle, CheckCircle,
  Plus, Edit, Trash2, Eye, Settings
} from 'lucide-react'

interface Product {
  id: string
  name: string
  price: number
  stock: number
  status: 'active' | 'draft' | 'out_of_stock'
  image?: string
}

interface Order {
  id: string
  customer: string
  total: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered'
  date: string
}

export default function EcommerceDashboard() {
  const [products, setProducts] = useState<Product[]>([])
  const [orders, setOrders] = useState<Order[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [saleorStatus, setSaleorStatus] = useState<'connecting' | 'connected' | 'error'>('connecting')

  // Test Saleor connection and load data
  useEffect(() => {
    const loadSaleorData = async () => {
      try {
        // Test Saleor connection first
        const healthResponse = await fetch('http://localhost:8020/health/', {
          method: 'GET',
          headers: { 'Accept': 'application/json' }
        })
        
        if (!healthResponse.ok) {
          throw new Error('Saleor health check failed')
        }
        
        // Try GraphQL query for shop info
        const graphqlResponse = await fetch('http://localhost:8020/graphql/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            query: `
              query {
                shop {
                  name
                  description
                }
                products(first: 10) {
                  edges {
                    node {
                      id
                      name
                      description
                      pricing {
                        priceRange {
                          start {
                            gross {
                              amount
                              currency
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            `
          })
        })
        
        if (graphqlResponse.ok) {
          const data = await graphqlResponse.json()
          if (data.data) {
            // Process real Saleor data if available
            const saleorProducts = data.data.products?.edges?.map((edge: any) => ({
              id: edge.node.id,
              name: edge.node.name,
              price: edge.node.pricing?.priceRange?.start?.gross?.amount || 0,
              stock: Math.floor(Math.random() * 100), // Mock stock data
              status: 'active' as const
            })) || []
            
            setProducts(saleorProducts.length > 0 ? saleorProducts : getMockProducts())
            setSaleorStatus('connected')
          } else {
            throw new Error('GraphQL query failed')
          }
        } else {
          throw new Error('GraphQL endpoint not responding')
        }
        
        // Load mock orders for now
        setOrders(getMockOrders())
        
      } catch (error) {
        console.error('Saleor connection error:', error)
        setSaleorStatus('error')
        // Use mock data as fallback
        setProducts(getMockProducts())
        setOrders(getMockOrders())
      } finally {
        setIsLoading(false)
      }
    }
    
    loadSaleorData()
  }, [])
  
  const getMockProducts = () => [
    { id: '1', name: 'Premium Wireless Headphones', price: 299.99, stock: 45, status: 'active' as const },
    { id: '2', name: 'Smart Fitness Tracker', price: 199.99, stock: 0, status: 'out_of_stock' as const },
    { id: '3', name: 'Eco-Friendly Water Bottle', price: 24.99, stock: 150, status: 'active' as const },
    { id: '4', name: 'Bluetooth Speaker Pro', price: 149.99, stock: 23, status: 'active' as const },
  ]
  
  const getMockOrders = () => [
    { id: '#ORD-001', customer: 'John Doe', total: 299.99, status: 'processing' as const, date: '2025-09-11' },
    { id: '#ORD-002', customer: 'Jane Smith', total: 174.98, status: 'shipped' as const, date: '2025-09-10' },
    { id: '#ORD-003', customer: 'Mike Johnson', total: 449.97, status: 'delivered' as const, date: '2025-09-09' },
  ]

  const stats = [
    { title: 'Total Revenue', value: '$12,847', change: '+12.5%', icon: DollarSign, positive: true },
    { title: 'Active Products', value: products.filter(p => p.status === 'active').length.toString(), change: '+3', icon: Package, positive: true },
    { title: 'Pending Orders', value: orders.filter(o => o.status === 'pending' || o.status === 'processing').length.toString(), change: '+2', icon: ShoppingCart, positive: true },
    { title: 'Conversion Rate', value: '3.2%', change: '+0.4%', icon: TrendingUp, positive: true },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">Ecommerce Management</h1>
          <p className="text-muted-foreground mt-2">
            Manage your CoreLDove store powered by Saleor
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            {saleorStatus === 'connected' ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm text-green-600">Saleor Connected</span>
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
          <TabsTrigger value="products">Products</TabsTrigger>
          <TabsTrigger value="orders">Orders</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Orders */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Orders</CardTitle>
                <CardDescription>Latest customer orders from your store</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {orders.slice(0, 3).map((order) => (
                    <div key={order.id} className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{order.id}</p>
                        <p className="text-sm text-muted-foreground">{order.customer}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">${order.total}</p>
                        <Badge variant={
                          order.status === 'delivered' ? 'default' : 
                          order.status === 'shipped' ? 'secondary' : 'outline'
                        }>
                          {order.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Product Performance */}
            <Card>
              <CardHeader>
                <CardTitle>Top Products</CardTitle>
                <CardDescription>Best selling products this month</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {products.filter(p => p.status === 'active').slice(0, 3).map((product) => (
                    <div key={product.id} className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{product.name}</p>
                        <p className="text-sm text-muted-foreground">{product.stock} in stock</p>
                      </div>
                      <div className="text-right">
                        <p className="font-medium">${product.price}</p>
                        <Badge variant="outline">Active</Badge>
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
                <CardTitle>Product Management</CardTitle>
                <CardDescription>Manage your store products and inventory</CardDescription>
              </div>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add Product
              </Button>
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
                          ${product.price} • {product.stock} in stock
                        </p>
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
                      <Button variant="ghost" size="sm">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="orders">
          <Card>
            <CardHeader>
              <CardTitle>Order Management</CardTitle>
              <CardDescription>Track and manage customer orders</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {orders.map((order) => (
                  <div key={order.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-medium">{order.id}</h3>
                      <p className="text-sm text-muted-foreground">
                        {order.customer} • {order.date}
                      </p>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <p className="font-medium">${order.total}</p>
                        <Badge variant={
                          order.status === 'delivered' ? 'default' : 
                          order.status === 'shipped' ? 'secondary' : 'outline'
                        }>
                          {order.status}
                        </Badge>
                      </div>
                      <Button variant="outline" size="sm">
                        View Details
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Sales Analytics</CardTitle>
                <CardDescription>Revenue and sales performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>This Month</span>
                    <span className="font-semibold">$12,847</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Last Month</span>
                    <span className="font-semibold">$11,432</span>
                  </div>
                  <div className="flex justify-between text-green-600">
                    <span>Growth</span>
                    <span className="font-semibold">+12.4%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>AI Insights</CardTitle>
                <CardDescription>Automated recommendations from your AI agents</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm">🤖 <strong>Marketing Agent:</strong> Consider promoting "Wireless Headphones" - 23% conversion rate</p>
                  </div>
                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-sm">📊 <strong>Analytics Agent:</strong> Restock "Fitness Tracker" - high demand detected</p>
                  </div>
                  <div className="p-3 bg-orange-50 rounded-lg">
                    <p className="text-sm">💡 <strong>Optimization Agent:</strong> Product descriptions need SEO updates</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>Store Settings</CardTitle>
              <CardDescription>Configure your CoreLDove store and Saleor integration</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium mb-3">Saleor Integration</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">GraphQL API</span>
                      <Badge variant="outline">http://localhost:8020/graphql/</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Storefront</span>
                      <Badge variant="outline">http://localhost:3003</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Status</span>
                      <Badge variant={saleorStatus === 'connected' ? 'default' : 'secondary'}>
                        {saleorStatus}
                      </Badge>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-medium mb-3">Quick Actions</h3>
                  <div className="space-y-2">
                    <Button variant="outline" className="w-full justify-start">
                      <Settings className="h-4 w-4 mr-2" />
                      Configure Payment Methods
                    </Button>
                    <Button variant="outline" className="w-full justify-start">
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Sync Products
                    </Button>
                    <Button variant="outline" className="w-full justify-start">
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Open Saleor Admin
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}