"use client"

import { useState, useEffect, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Search,
  Package,
  TrendingUp,
  DollarSign,
  Eye,
  Plus,
  Settings,
  RefreshCw,
  CheckCircle,
  XCircle,
  Clock,
  AlertTriangle,
  Star,
  ShoppingCart,
  Truck,
  BarChart3,
  Filter,
  ExternalLink,
  Download,
  Upload
} from "lucide-react"
import {
  AmazonProduct,
  ProductListing,
  ListingPlatform,
  amazonSPAPI,
  productListingService,
  mockDropshipProducts,
  SellerInventoryItem
} from "@/lib/amazon-sp-api"
import { inventorySync, SyncJob, InventoryAlert } from "@/lib/inventory-sync"
import { InventoryDashboard } from "./inventory-dashboard"
import { useDebounce } from "@/hooks/use-debounce"

export function DropshippingDashboard() {
  // State management
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [isLoading, setIsLoading] = useState(false)
  const [products, setProducts] = useState<AmazonProduct[]>([])
  const [listings, setListings] = useState<ProductListing[]>([])
  const [selectedProducts, setSelectedProducts] = useState<Set<string>>(new Set())
  const [selectedPlatforms, setSelectedPlatforms] = useState<Set<string>>(new Set(['medusajs']))
  const [markup, setMarkup] = useState(30) // 30% markup
  const [minRating, setMinRating] = useState(4.0)
  const [maxPrice, setMaxPrice] = useState(1000)
  const [showFilters, setShowFilters] = useState(false)
  const [availablePlatforms, setAvailablePlatforms] = useState<ListingPlatform[]>([])
  const [stats, setStats] = useState({
    totalProducts: 0,
    listedProducts: 0,
    pendingApprovals: 0,
    totalRevenue: 0
  })
  const [sellerInventory, setSellerInventory] = useState<SellerInventoryItem[]>([])
  const [syncJobs, setSyncJobs] = useState<SyncJob[]>([])
  const [inventoryAlerts, setInventoryAlerts] = useState<InventoryAlert[]>([])
  const [showInventoryDashboard, setShowInventoryDashboard] = useState(false)

  // Debounced search
  const debouncedSearchQuery = useDebounce(searchQuery, 500)

  // Categories for Amazon product search
  const categories = [
    { value: "all", label: "All Categories" },
    { value: "electronics", label: "Electronics" },
    { value: "home-kitchen", label: "Home & Kitchen" },
    { value: "sports-outdoors", label: "Sports & Outdoors" },
    { value: "toys-games", label: "Toys & Games" },
    { value: "clothing", label: "Clothing & Accessories" },
    { value: "books", label: "Books" },
    { value: "beauty", label: "Beauty & Personal Care" }
  ]

  // Initialize data
  useEffect(() => {
    const initializeDashboard = async () => {
      setIsLoading(true)
      try {
        // Load available platforms
        const platforms = productListingService.getAvailablePlatforms()
        setAvailablePlatforms(platforms)
        
        // Load mock data for development
        setProducts(mockDropshipProducts)
        
        // Initialize with default platform selection
        setSelectedPlatforms(new Set(['medusajs']))
        
        // Mock stats
        setStats({
          totalProducts: mockDropshipProducts.length,
          listedProducts: 0,
          pendingApprovals: 0,
          totalRevenue: 0
        })
      } catch (error) {
        console.error('Failed to initialize dashboard:', error)
      } finally {
        setIsLoading(false)
      }
    }
    
    initializeDashboard()
  }, [])

  // Search products
  const searchProducts = useCallback(async () => {
    if (!debouncedSearchQuery.trim()) {
      setProducts(mockDropshipProducts)
      return
    }

    setIsLoading(true)
    try {
      // In development, filter mock data
      const filtered = mockDropshipProducts.filter(product =>
        product.title.toLowerCase().includes(debouncedSearchQuery.toLowerCase()) ||
        product.brand?.toLowerCase().includes(debouncedSearchQuery.toLowerCase()) ||
        product.category.toLowerCase().includes(debouncedSearchQuery.toLowerCase())
      )
      
      setProducts(filtered)
      
      // In production, this would call Amazon SP-API
      // const results = await amazonSPAPI.searchDropshipProducts(debouncedSearchQuery, selectedCategory, minRating)
      // setProducts(results)
    } catch (error) {
      console.error('Product search failed:', error)
    } finally {
      setIsLoading(false)
    }
  }, [debouncedSearchQuery, selectedCategory, minRating])

  // Effect for search
  useEffect(() => {
    searchProducts()
  }, [searchProducts])

  // Handle product selection
  const toggleProductSelection = (asin: string) => {
    const newSelection = new Set(selectedProducts)
    if (newSelection.has(asin)) {
      newSelection.delete(asin)
    } else {
      newSelection.add(asin)
    }
    setSelectedProducts(newSelection)
  }

  // Handle platform selection
  const togglePlatformSelection = (platformId: string) => {
    const newSelection = new Set(selectedPlatforms)
    if (newSelection.has(platformId)) {
      newSelection.delete(platformId)
    } else {
      newSelection.add(platformId)
    }
    setSelectedPlatforms(newSelection)
  }

  // Bulk list products
  const listSelectedProducts = async () => {
    if (selectedProducts.size === 0 || selectedPlatforms.size === 0) return

    setIsLoading(true)
    try {
      const productsToList = products.filter(p => selectedProducts.has(p.asin))
      const newListings: ProductListing[] = []
      
      for (const product of productsToList) {
        const listing = await productListingService.createListing(
          product,
          Array.from(selectedPlatforms),
          markup / 100
        )
        newListings.push(listing)
      }
      
      setListings(prev => [...prev, ...newListings])
      setSelectedProducts(new Set())
      
      // Update stats
      setStats(prev => ({
        ...prev,
        listedProducts: prev.listedProducts + newListings.length,
        pendingApprovals: prev.pendingApprovals + newListings.length
      }))
      
    } catch (error) {
      console.error('Failed to list products:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Calculate profit margins
  const profitMargins = productListingService.calculateProfitMargins(50, markup / 100) // Example with $50 cost

  // Filter products by criteria
  const filteredProducts = products.filter(product => {
    if (selectedCategory && selectedCategory !== "all" && product.category.toLowerCase() !== selectedCategory) return false
    if (product.reviews.rating < minRating) return false
    if (product.price.amount > maxPrice) return false
    return true
  })

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Products</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalProducts}</div>
            <p className="text-xs text-muted-foreground">Available for dropshipping</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Listed Products</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.listedProducts}</div>
            <p className="text-xs text-muted-foreground">Across all platforms</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Approvals</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.pendingApprovals}</div>
            <p className="text-xs text-muted-foreground">Awaiting platform approval</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Projected Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${stats.totalRevenue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">Monthly projection</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="products" className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="products">Product Sourcing</TabsTrigger>
          <TabsTrigger value="inventory">Inventory Sync</TabsTrigger>
          <TabsTrigger value="listings">My Listings</TabsTrigger>
          <TabsTrigger value="platforms">Platform Settings</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        {/* Product Sourcing Tab */}
        <TabsContent value="products" className="space-y-4">
          {/* Quick Actions Bar */}
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <Button 
                    onClick={() => setShowInventoryDashboard(true)}
                    variant="outline"
                  >
                    <Package className="h-4 w-4 mr-2" />
                    View Full Inventory
                  </Button>
                  <Button 
                    onClick={async () => {
                      try {
                        await fetch('/api/inventory/sync', {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ type: 'full' })
                        })
                      } catch (error) {
                        console.error('Sync failed:', error)
                      }
                    }}
                    variant="outline"
                    disabled={isLoading}
                  >
                    <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                    Sync Inventory
                  </Button>
                </div>
                <div className="text-sm text-muted-foreground">
                  Last sync: Never | Next: Auto in 30min
                </div>
              </div>
            </CardContent>
          </Card>
          {/* Search and Filters */}
          <Card>
            <CardHeader>
              <CardTitle>Find Dropship Products</CardTitle>
              <CardDescription>
                Search Amazon's catalog for profitable dropshipping opportunities
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Search Bar */}
              <div className="flex gap-4">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search products, brands, keywords..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="w-48">
                    <SelectValue placeholder="Category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((cat) => (
                      <SelectItem key={cat.value} value={cat.value}>
                        {cat.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button onClick={() => setShowFilters(!showFilters)} variant="outline">
                  <Filter className="h-4 w-4 mr-2" />
                  Filters
                </Button>
              </div>

              {/* Advanced Filters */}
              {showFilters && (
                <Card>
                  <CardContent className="p-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="space-y-2">
                        <Label>Minimum Rating</Label>
                        <Select value={minRating.toString()} onValueChange={(v) => setMinRating(Number(v))}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="3">3+ Stars</SelectItem>
                            <SelectItem value="4">4+ Stars</SelectItem>
                            <SelectItem value="4.5">4.5+ Stars</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <Label>Max Price</Label>
                        <Input
                          type="number"
                          value={maxPrice}
                          onChange={(e) => setMaxPrice(Number(e.target.value))}
                          placeholder="Maximum price"
                        />
                      </div>
                      
                      <div className="space-y-2">
                        <Label>Markup %</Label>
                        <Input
                          type="number"
                          value={markup}
                          onChange={(e) => setMarkup(Number(e.target.value))}
                          placeholder="Markup percentage"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Platform Selection */}
              <div className="space-y-2">
                <Label>List on Platforms:</Label>
                <div className="flex flex-wrap gap-2">
                  {availablePlatforms.map((platform) => (
                    <div key={platform.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={platform.id}
                        checked={selectedPlatforms.has(platform.id)}
                        onCheckedChange={() => togglePlatformSelection(platform.id)}
                      />
                      <Label htmlFor={platform.id} className="text-sm">
                        {platform.name}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bulk Actions */}
              {selectedProducts.size > 0 && (
                <div className="flex items-center gap-4 p-3 bg-blue-50 dark:bg-blue-950 rounded-lg">
                  <span className="text-sm font-medium">
                    {selectedProducts.size} products selected
                  </span>
                  <Button 
                    onClick={listSelectedProducts} 
                    disabled={isLoading || selectedPlatforms.size === 0}
                  >
                    {isLoading ? (
                      <>
                        <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                        Listing Products...
                      </>
                    ) : (
                      <>
                        <Plus className="h-4 w-4 mr-2" />
                        List Selected Products
                      </>
                    )}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Product Results */}
          <Card>
            <CardHeader>
              <CardTitle>Search Results ({filteredProducts.length} products)</CardTitle>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-96">
                <div className="space-y-4">
                  {filteredProducts.map((product) => (
                    <Card key={product.asin} className="p-4">
                      <div className="flex items-start gap-4">
                        <Checkbox
                          checked={selectedProducts.has(product.asin)}
                          onCheckedChange={() => toggleProductSelection(product.asin)}
                        />
                        
                        <div className="w-20 h-20 bg-gray-100 rounded-lg flex-shrink-0">
                          {product.images[0] && (
                            <img
                              src={product.images[0]}
                              alt={product.title}
                              className="w-full h-full object-cover rounded-lg"
                            />
                          )}
                        </div>
                        
                        <div className="flex-1 space-y-2">
                          <div className="flex items-start justify-between">
                            <div>
                              <h3 className="font-semibold text-sm line-clamp-2">{product.title}</h3>
                              <p className="text-sm text-muted-foreground">{product.brand}</p>
                            </div>
                            <div className="text-right">
                              <div className="text-lg font-bold">${product.price.amount}</div>
                              <div className="text-sm text-green-600">
                                +{markup}% = ${(product.price.amount * (1 + markup / 100)).toFixed(2)}
                              </div>
                            </div>
                          </div>
                          
                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                              <span>{product.reviews.rating}</span>
                              <span>({product.reviews.count.toLocaleString()})</span>
                            </div>
                            <Badge variant="outline">{product.category}</Badge>
                            {product.dropshipEligible && (
                              <Badge className="bg-green-100 text-green-800">
                                <Truck className="h-3 w-3 mr-1" />
                                Dropship Ready
                              </Badge>
                            )}
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <div className="flex gap-2">
                              <Button size="sm" variant="outline">
                                <Eye className="h-4 w-4 mr-1" />
                                View Details
                              </Button>
                              <Button size="sm" variant="outline">
                                <ExternalLink className="h-4 w-4 mr-1" />
                                Amazon Page
                              </Button>
                            </div>
                            
                            <div className="text-xs text-muted-foreground">
                              Est. commission: ${product.commission?.amount.toFixed(2)}
                            </div>
                          </div>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Inventory Sync Tab */}
        <TabsContent value="inventory" className="space-y-4">
          <InventoryDashboard />
        </TabsContent>

        {/* My Listings Tab */}
        <TabsContent value="listings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>My Product Listings</CardTitle>
              <CardDescription>
                Manage your active and pending product listings across all platforms
              </CardDescription>
            </CardHeader>
            <CardContent>
              {listings.length === 0 ? (
                <div className="text-center py-8">
                  <Package className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <h3 className="text-lg font-medium">No listings yet</h3>
                  <p className="text-muted-foreground">Start by sourcing and listing products from the Product Sourcing tab</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {listings.map((listing) => (
                    <Card key={listing.id} className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-semibold">{listing.title}</h3>
                          <p className="text-sm text-muted-foreground">ASIN: {listing.sourceAsin}</p>
                        </div>
                        <div className="text-right">
                          <div className="text-lg font-bold">${listing.price.selling.toFixed(2)}</div>
                          <div className="text-sm text-green-600">
                            Margin: ${listing.price.margin.toFixed(2)}
                          </div>
                        </div>
                      </div>
                      
                      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-blue-500" />
                          <span className="text-sm">MedusaJS: {listing.platforms.medusajs.status}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-orange-500" />
                          <span className="text-sm">Amazon: {listing.platforms.amazon.status}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-purple-500" />
                          <span className="text-sm">Flipkart: {listing.platforms.flipkart.status}</span>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Platform Settings Tab */}
        <TabsContent value="platforms" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Platform Configuration</CardTitle>
              <CardDescription>
                Configure your marketplace integrations and credentials
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {availablePlatforms.map((platform) => (
                  <Card key={platform.id}>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-lg">{platform.name}</CardTitle>
                        <Badge variant={platform.enabled ? "default" : "secondary"}>
                          {platform.enabled ? "Connected" : "Disconnected"}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <Label>Listing Fee</Label>
                          <p className="font-medium">${platform.fees.listingFee}</p>
                        </div>
                        <div>
                          <Label>Commission Rate</Label>
                          <p className="font-medium">{(platform.fees.commissionRate * 100)}%</p>
                        </div>
                        <div>
                          <Label>Fulfillment Fee</Label>
                          <p className="font-medium">${platform.fees.fulfillmentFee}</p>
                        </div>
                      </div>
                      
                      <div className="mt-4 flex gap-2">
                        <Button size="sm" variant="outline">
                          <Settings className="h-4 w-4 mr-1" />
                          Configure
                        </Button>
                        {platform.enabled && (
                          <Button size="sm" variant="outline">
                            <RefreshCw className="h-4 w-4 mr-1" />
                            Sync
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Profit Analysis</CardTitle>
              <CardDescription>
                Compare profit margins across different platforms
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {profitMargins.map((margin) => (
                  <div key={margin.platform} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-medium">{margin.platform}</h3>
                      <p className="text-sm text-muted-foreground">
                        Selling Price: ${margin.sellingPrice.toFixed(2)}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-green-600">
                        ${margin.profit.toFixed(2)}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {margin.profitMargin}% margin
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}