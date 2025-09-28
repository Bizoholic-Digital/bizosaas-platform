"use client"

import { DashboardLayout } from "@/components/dashboard-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import Link from "next/link"
import {
  Package,
  TrendingUp,
  DollarSign,
  ShoppingCart,
  Truck,
  BarChart3,
  Settings,
  Plus,
  Eye,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  Clock,
  Star,
  Globe
} from "lucide-react"

export default function SellerDashboard() {
  // Mock data for seller dashboard
  const stats = {
    totalProducts: 156,
    activeListings: 142,
    pendingApprovals: 8,
    totalSales: 28450,
    monthlyRevenue: 12800,
    profitMargin: 24.8,
    orders: {
      pending: 12,
      processing: 8,
      shipped: 45,
      delivered: 234
    }
  }

  const recentProducts = [
    {
      id: "1",
      name: "Echo Dot (4th Gen) Smart Speaker",
      asin: "B08N5WRWNW",
      price: 64.99,
      cost: 49.99,
      profit: 15.00,
      platforms: ["medusajs", "amazon"],
      status: "live",
      sales: 23
    },
    {
      id: "2", 
      name: "Fire TV Stick 4K Streaming Device",
      asin: "B07XJ8C8F5",
      price: 51.99,
      cost: 39.99,
      profit: 12.00,
      platforms: ["medusajs", "flipkart"],
      status: "pending",
      sales: 0
    },
    {
      id: "3",
      name: "Wireless Earbuds Bluetooth 5.0",
      asin: "B08C7KG5LP",
      price: 39.99,
      cost: 25.99,
      profit: 14.00,
      platforms: ["medusajs", "amazon", "flipkart"],
      status: "live", 
      sales: 45
    }
  ]

  const platforms = [
    { id: "medusajs", name: "CoreLDove Store", status: "connected", listings: 142, sales: 234 },
    { id: "amazon", name: "Amazon Marketplace", status: "connected", listings: 89, sales: 156 },
    { id: "flipkart", name: "Flipkart", status: "pending", listings: 45, sales: 23 }
  ]

  return (
    <DashboardLayout userRole="seller">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              Seller Dashboard
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              Welcome to your CoreLDove dropshipping command center
            </p>
          </div>
          <div className="flex gap-3">
            <Link href="/seller/dropshipping">
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Add Products
              </Button>
            </Link>
            <Button variant="outline">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Products</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalProducts}</div>
              <p className="text-xs text-muted-foreground">
                {stats.activeListings} active listings
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${stats.monthlyRevenue.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">
                +12.5% from last month
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Profit Margin</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.profitMargin}%</div>
              <p className="text-xs text-muted-foreground">
                Above industry average
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending Orders</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.orders.pending}</div>
              <p className="text-xs text-muted-foreground">
                {stats.orders.processing} processing
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Recent Products */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Recent Products</CardTitle>
                <Button variant="outline" size="sm">
                  <Eye className="h-4 w-4 mr-1" />
                  View All
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentProducts.map((product) => (
                  <div key={product.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex-1">
                      <h3 className="font-medium text-sm">{product.name}</h3>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                        <span>ASIN: {product.asin}</span>
                        <span>•</span>
                        <span>{product.sales} sales</span>
                      </div>
                      <div className="flex gap-1 mt-2">
                        {product.platforms.includes("medusajs") && (
                          <Badge variant="outline" className="text-xs">Store</Badge>
                        )}
                        {product.platforms.includes("amazon") && (
                          <Badge variant="outline" className="text-xs">Amazon</Badge>
                        )}
                        {product.platforms.includes("flipkart") && (
                          <Badge variant="outline" className="text-xs">Flipkart</Badge>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold">${product.price}</div>
                      <div className="text-xs text-green-600">+${product.profit}</div>
                      <Badge 
                        className={`mt-1 text-xs ${
                          product.status === 'live' ? 'bg-green-100 text-green-800' : 
                          'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {product.status}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Platform Status */}
          <Card>
            <CardHeader>
              <CardTitle>Platform Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {platforms.map((platform) => (
                  <div key={platform.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        platform.status === 'connected' ? 'bg-green-500' : 
                        platform.status === 'pending' ? 'bg-yellow-500' : 'bg-red-500'
                      }`} />
                      <div>
                        <h3 className="font-medium">{platform.name}</h3>
                        <p className="text-sm text-muted-foreground capitalize">
                          {platform.status}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold">{platform.listings} listings</div>
                      <div className="text-xs text-muted-foreground">{platform.sales} sales</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Order Pipeline */}
        <Card>
          <CardHeader>
            <CardTitle>Order Pipeline</CardTitle>
            <CardDescription>Track orders across all platforms</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">{stats.orders.pending}</div>
                <div className="text-sm text-muted-foreground">Pending</div>
                <Progress value={30} className="mt-2 h-2" />
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{stats.orders.processing}</div>
                <div className="text-sm text-muted-foreground">Processing</div>
                <Progress value={60} className="mt-2 h-2" />
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">{stats.orders.shipped}</div>
                <div className="text-sm text-muted-foreground">Shipped</div>
                <Progress value={80} className="mt-2 h-2" />
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{stats.orders.delivered}</div>
                <div className="text-sm text-muted-foreground">Delivered</div>
                <Progress value={100} className="mt-2 h-2" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Link href="/seller/dropshipping">
                <Button variant="outline" className="w-full h-20 flex flex-col">
                  <Plus className="h-6 w-6 mb-2" />
                  Add Products
                </Button>
              </Link>
              <Button variant="outline" className="w-full h-20 flex flex-col">
                <BarChart3 className="h-6 w-6 mb-2" />
                Analytics
              </Button>
              <Button variant="outline" className="w-full h-20 flex flex-col">
                <RefreshCw className="h-6 w-6 mb-2" />
                Sync Inventory
              </Button>
              <Button variant="outline" className="w-full h-20 flex flex-col">
                <Settings className="h-6 w-6 mb-2" />
                Platform Settings
              </Button>
            </div>
          </CardContent>
        </Card>
    </DashboardLayout>
  )
}