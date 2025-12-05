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
import { ScrollArea } from "@/components/ui/scroll-area"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
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
  Upload,
  AlertCircle,
  PackageX,
  TrendingDown,
  Edit,
  Save,
  X,
  ChevronLeft,
  ChevronRight
} from "lucide-react"
import { useDebounce } from "@/hooks/use-debounce"
import { SellerInventoryItem, BulkInventoryUpdate } from "@/lib/amazon-sp-api"
import { SyncJob, InventoryAlert } from "@/lib/inventory-sync"

interface InventoryDashboardProps {
  className?: string
}

export function InventoryDashboard({ className }: InventoryDashboardProps) {
  // State management
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [selectedStatus, setSelectedStatus] = useState("all")
  const [isLoading, setIsLoading] = useState(false)
  const [inventory, setInventory] = useState<SellerInventoryItem[]>([])
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set())
  const [syncJobs, setSyncJobs] = useState<SyncJob[]>([])
  const [alerts, setAlerts] = useState<InventoryAlert[]>([])
  const [editingItems, setEditingItems] = useState<Map<string, Partial<SellerInventoryItem>>>(new Map())
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [summary, setSummary] = useState({
    totalProducts: 0,
    totalValue: 0,
    totalQuantity: 0,
    averagePrice: 0,
    byStatus: { active: 0, inactive: 0, incomplete: 0 },
    byFulfillment: { FBA: 0, FBM: 0 },
    lowStock: 0,
    outOfStock: 0
  })

  // Debounced search
  const debouncedSearchQuery = useDebounce(searchQuery, 500)

  // Load inventory data
  const loadInventory = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`/api/inventory/seller?${new URLSearchParams({
        page: currentPage.toString(),
        limit: '20',
        ...(selectedCategory !== 'all' && { category: selectedCategory }),
        ...(selectedStatus !== 'all' && { status: selectedStatus }),
        ...(debouncedSearchQuery && { search: debouncedSearchQuery })
      })}`)

      const data = await response.json()
      
      if (data.success) {
        setInventory(data.data.items)
        setSummary(data.data.summary)
        setTotalPages(data.data.pagination.pages)
      }
    } catch (error) {
      console.error('Failed to load inventory:', error)
    } finally {
      setIsLoading(false)
    }
  }, [currentPage, selectedCategory, selectedStatus, debouncedSearchQuery])

  // Load sync jobs
  const loadSyncJobs = useCallback(async () => {
    try {
      const response = await fetch('/api/inventory/sync')
      const data = await response.json()
      if (data.jobs) {
        setSyncJobs(data.jobs.slice(0, 5)) // Show last 5 jobs
      }
    } catch (error) {
      console.error('Failed to load sync jobs:', error)
    }
  }, [])

  // Load alerts
  const loadAlerts = useCallback(async () => {
    try {
      const response = await fetch('/api/inventory/alerts?resolved=false&limit=10')
      const data = await response.json()
      if (data.success) {
        setAlerts(data.data.alerts)
      }
    } catch (error) {
      console.error('Failed to load alerts:', error)
    }
  }, [])

  // Initialize data
  useEffect(() => {
    loadInventory()
    loadSyncJobs()
    loadAlerts()
  }, [loadInventory, loadSyncJobs, loadAlerts])

  // Handle item selection
  const toggleItemSelection = (asin: string) => {
    const newSelection = new Set(selectedItems)
    if (newSelection.has(asin)) {
      newSelection.delete(asin)
    } else {
      newSelection.add(asin)
    }
    setSelectedItems(newSelection)
  }

  // Start sync
  const startSync = async (type: 'full' | 'partial' = 'full', asins?: string[]) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/inventory/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type,
          ...(asins && { asins })
        })
      })

      const data = await response.json()
      if (data.success) {
        await loadSyncJobs()
      }
    } catch (error) {
      console.error('Failed to start sync:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Handle inline editing
  const startEdit = (asin: string, item: SellerInventoryItem) => {
    setEditingItems(prev => new Map(prev).set(asin, { ...item }))
  }

  const cancelEdit = (asin: string) => {
    setEditingItems(prev => {
      const newMap = new Map(prev)
      newMap.delete(asin)
      return newMap
    })
  }

  const saveEdit = async (asin: string) => {
    const editedItem = editingItems.get(asin)
    if (!editedItem) return

    try {
      const updates: BulkInventoryUpdate[] = [{
        asin,
        quantity: editedItem.quantity,
        price: editedItem.price
      }]

      const response = await fetch('/api/inventory/bulk-update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ updates })
      })

      if (response.ok) {
        await loadInventory()
        cancelEdit(asin)
      }
    } catch (error) {
      console.error('Failed to save changes:', error)
    }
  }

  const updateEditValue = (asin: string, field: string, value: any) => {
    setEditingItems(prev => {
      const newMap = new Map(prev)
      const item = newMap.get(asin) || {}
      newMap.set(asin, { ...item, [field]: value })
      return newMap
    })
  }

  // Bulk update selected items
  const bulkUpdateSelected = async (updates: Partial<BulkInventoryUpdate>) => {
    if (selectedItems.size === 0) return

    setIsLoading(true)
    try {
      const bulkUpdates: BulkInventoryUpdate[] = Array.from(selectedItems).map(asin => ({
        asin,
        ...updates
      }))

      const response = await fetch('/api/inventory/bulk-update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ updates: bulkUpdates })
      })

      if (response.ok) {
        await loadInventory()
        setSelectedItems(new Set())
      }
    } catch (error) {
      console.error('Failed to bulk update:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Export inventory
  const exportInventory = async (format: 'csv' | 'json') => {
    try {
      const response = await fetch(`/api/inventory/export?format=${format}`)
      const data = await response.blob()
      
      const url = window.URL.createObjectURL(data)
      const a = document.createElement('a')
      a.href = url
      a.download = `inventory_export_${new Date().toISOString().split('T')[0]}.${format}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to export inventory:', error)
    }
  }

  // Resolve alert
  const resolveAlert = async (alertId: string) => {
    try {
      const response = await fetch('/api/inventory/alerts', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alertId, action: 'resolve' })
      })

      if (response.ok) {
        await loadAlerts()
      }
    } catch (error) {
      console.error('Failed to resolve alert:', error)
    }
  }

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'active': return 'default'
      case 'inactive': return 'secondary'
      case 'incomplete': return 'destructive'
      default: return 'outline'
    }
  }

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'low_stock': return <TrendingDown className="h-4 w-4" />
      case 'out_of_stock': return <PackageX className="h-4 w-4" />
      case 'sync_conflict': return <AlertTriangle className="h-4 w-4" />
      case 'sync_error': return <XCircle className="h-4 w-4" />
      default: return <AlertCircle className="h-4 w-4" />
    }
  }

  return (
    <div className={className}>
      <div className="space-y-6">
        {/* Header Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Products</CardTitle>
              <Package className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{summary.totalProducts.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">
                Active: {summary.byStatus.active} | Inactive: {summary.byStatus.inactive}
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Value</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">${summary.totalValue.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">
                Avg: ${summary.averagePrice.toFixed(2)} per item
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Stock Alerts</CardTitle>
              <AlertTriangle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{summary.lowStock}</div>
              <p className="text-xs text-muted-foreground">
                Out of stock: {summary.outOfStock}
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Fulfillment</CardTitle>
              <Truck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{summary.byFulfillment.FBA + summary.byFulfillment.FBM}</div>
              <p className="text-xs text-muted-foreground">
                FBA: {summary.byFulfillment.FBA} | FBM: {summary.byFulfillment.FBM}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="inventory" className="space-y-4">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="inventory">Inventory Management</TabsTrigger>
            <TabsTrigger value="sync">Sync Jobs</TabsTrigger>
            <TabsTrigger value="alerts">Alerts</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          {/* Inventory Management Tab */}
          <TabsContent value="inventory" className="space-y-4">
            {/* Search and Controls */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Inventory Management</CardTitle>
                    <CardDescription>
                      Manage your Amazon seller inventory and sync across platforms
                    </CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button onClick={() => startSync('full')} disabled={isLoading}>
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Sync All
                    </Button>
                    <Button variant="outline" onClick={() => exportInventory('csv')}>
                      <Download className="h-4 w-4 mr-2" />
                      Export
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Search and Filters */}
                <div className="flex gap-4">
                  <div className="relative flex-1">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search by ASIN, title, or brand..."
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
                      <SelectItem value="all">All Categories</SelectItem>
                      <SelectItem value="electronics">Electronics</SelectItem>
                      <SelectItem value="home">Home & Kitchen</SelectItem>
                      <SelectItem value="books">Books</SelectItem>
                      <SelectItem value="clothing">Clothing</SelectItem>
                    </SelectContent>
                  </Select>
                  <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                    <SelectTrigger className="w-48">
                      <SelectValue placeholder="Status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Status</SelectItem>
                      <SelectItem value="active">Active</SelectItem>
                      <SelectItem value="inactive">Inactive</SelectItem>
                      <SelectItem value="incomplete">Incomplete</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Bulk Actions */}
                {selectedItems.size > 0 && (
                  <div className="flex items-center gap-4 p-3 bg-blue-50 dark:bg-blue-950 rounded-lg">
                    <span className="text-sm font-medium">
                      {selectedItems.size} items selected
                    </span>
                    <div className="flex gap-2">
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button size="sm" variant="outline">
                            <Edit className="h-4 w-4 mr-1" />
                            Bulk Edit
                          </Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Bulk Update {selectedItems.size} Items</DialogTitle>
                          </DialogHeader>
                          <div className="space-y-4">
                            <div>
                              <Label>Quantity</Label>
                              <Input placeholder="Leave empty to keep current" type="number" />
                            </div>
                            <div>
                              <Label>Price</Label>
                              <Input placeholder="Leave empty to keep current" type="number" step="0.01" />
                            </div>
                            <div>
                              <Label>Status</Label>
                              <Select>
                                <SelectTrigger>
                                  <SelectValue placeholder="Leave empty to keep current" />
                                </SelectTrigger>
                                <SelectContent>
                                  <SelectItem value="active">Active</SelectItem>
                                  <SelectItem value="inactive">Inactive</SelectItem>
                                </SelectContent>
                              </Select>
                            </div>
                            <Button className="w-full">
                              Update Selected Items
                            </Button>
                          </div>
                        </DialogContent>
                      </Dialog>
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => startSync('partial', Array.from(selectedItems))}
                        disabled={isLoading}
                      >
                        <RefreshCw className="h-4 w-4 mr-1" />
                        Sync Selected
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Inventory Table */}
            <Card>
              <CardContent className="p-0">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-12">
                        <Checkbox
                          checked={selectedItems.size === inventory.length && inventory.length > 0}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedItems(new Set(inventory.map(item => item.asin)))
                            } else {
                              setSelectedItems(new Set())
                            }
                          }}
                        />
                      </TableHead>
                      <TableHead>Product</TableHead>
                      <TableHead>ASIN/SKU</TableHead>
                      <TableHead>Price</TableHead>
                      <TableHead>Quantity</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Fulfillment</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {inventory.map((item) => {
                      const isEditing = editingItems.has(item.asin)
                      const editedItem = editingItems.get(item.asin) || item

                      return (
                        <TableRow key={item.asin}>
                          <TableCell>
                            <Checkbox
                              checked={selectedItems.has(item.asin)}
                              onCheckedChange={() => toggleItemSelection(item.asin)}
                            />
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-3">
                              {item.images[0] && (
                                <div className="w-12 h-12 bg-gray-100 rounded flex-shrink-0">
                                  <img
                                    src={item.images[0]}
                                    alt={item.title}
                                    className="w-full h-full object-cover rounded"
                                  />
                                </div>
                              )}
                              <div>
                                <div className="font-medium text-sm line-clamp-2">{item.title}</div>
                                {item.brand && (
                                  <div className="text-sm text-muted-foreground">{item.brand}</div>
                                )}
                              </div>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="text-sm">
                              <div className="font-mono">{item.asin}</div>
                              <div className="text-muted-foreground">{item.sellerSku}</div>
                            </div>
                          </TableCell>
                          <TableCell>
                            {isEditing ? (
                              <Input
                                type="number"
                                step="0.01"
                                value={editedItem.price}
                                onChange={(e) => updateEditValue(item.asin, 'price', parseFloat(e.target.value))}
                                className="w-20"
                              />
                            ) : (
                              <div className="font-medium">${item.price.toFixed(2)}</div>
                            )}
                          </TableCell>
                          <TableCell>
                            {isEditing ? (
                              <Input
                                type="number"
                                value={editedItem.quantity}
                                onChange={(e) => updateEditValue(item.asin, 'quantity', parseInt(e.target.value))}
                                className="w-20"
                              />
                            ) : (
                              <div className={`font-medium ${item.quantity === 0 ? 'text-red-600' : item.quantity <= 10 ? 'text-orange-600' : ''}`}>
                                {item.quantity}
                              </div>
                            )}
                          </TableCell>
                          <TableCell>
                            <Badge variant={getStatusBadgeVariant(item.status)}>
                              {item.status}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline">{item.fulfillmentChannel}</Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex gap-1">
                              {isEditing ? (
                                <>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => saveEdit(item.asin)}
                                  >
                                    <Save className="h-3 w-3" />
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => cancelEdit(item.asin)}
                                  >
                                    <X className="h-3 w-3" />
                                  </Button>
                                </>
                              ) : (
                                <>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => startEdit(item.asin, item)}
                                  >
                                    <Edit className="h-3 w-3" />
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => startSync('partial', [item.asin])}
                                  >
                                    <RefreshCw className="h-3 w-3" />
                                  </Button>
                                </>
                              )}
                            </div>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>

                {/* Pagination */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-between px-4 py-3 border-t">
                    <div className="text-sm text-muted-foreground">
                      Page {currentPage} of {totalPages}
                    </div>
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                        disabled={currentPage === 1}
                      >
                        <ChevronLeft className="h-4 w-4" />
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                        disabled={currentPage === totalPages}
                      >
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Sync Jobs Tab */}
          <TabsContent value="sync" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Sync Jobs</CardTitle>
                <CardDescription>
                  View recent inventory synchronization jobs and their status
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {syncJobs.map((job) => (
                    <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className={`w-2 h-2 rounded-full ${
                          job.status === 'completed' ? 'bg-green-500' :
                          job.status === 'running' ? 'bg-blue-500' :
                          job.status === 'failed' ? 'bg-red-500' :
                          'bg-yellow-500'
                        }`} />
                        <div>
                          <div className="font-medium">{job.type} sync</div>
                          <div className="text-sm text-muted-foreground">
                            {job.startedAt && new Date(job.startedAt).toLocaleString()}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        {job.status === 'running' && (
                          <Progress value={job.progress} className="w-24" />
                        )}
                        <Badge variant={
                          job.status === 'completed' ? 'default' :
                          job.status === 'running' ? 'secondary' :
                          job.status === 'failed' ? 'destructive' :
                          'outline'
                        }>
                          {job.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                  {syncJobs.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground">
                      No sync jobs yet
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Alerts Tab */}
          <TabsContent value="alerts" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Inventory Alerts</CardTitle>
                <CardDescription>
                  Monitor inventory issues and sync conflicts
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {alerts.map((alert) => (
                    <Alert key={alert.id} className={alert.priority === 'high' || alert.priority === 'critical' ? 'border-red-200 bg-red-50' : ''}>
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-2">
                          {getAlertIcon(alert.type)}
                          <div>
                            <div className="font-medium">{alert.title}</div>
                            <div className="text-sm text-muted-foreground">{alert.message}</div>
                            <div className="text-xs text-muted-foreground mt-1">
                              {new Date(alert.createdAt).toLocaleString()}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge variant={
                            alert.priority === 'critical' ? 'destructive' :
                            alert.priority === 'high' ? 'destructive' :
                            alert.priority === 'medium' ? 'secondary' :
                            'outline'
                          }>
                            {alert.priority}
                          </Badge>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => resolveAlert(alert.id)}
                          >
                            <CheckCircle className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    </Alert>
                  ))}
                  {alerts.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground">
                      No active alerts
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle>Inventory Distribution</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>Active Products</span>
                      <span className="font-medium">{summary.byStatus.active}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Inactive Products</span>
                      <span className="font-medium">{summary.byStatus.inactive}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Incomplete Products</span>
                      <span className="font-medium">{summary.byStatus.incomplete}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Fulfillment Methods</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span>FBA (Fulfilled by Amazon)</span>
                      <span className="font-medium">{summary.byFulfillment.FBA}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>FBM (Fulfilled by Merchant)</span>
                      <span className="font-medium">{summary.byFulfillment.FBM}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}