"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Search, Package, AlertTriangle, TrendingDown, TrendingUp, RefreshCw, 
  Download, BarChart3, Zap, Target, Clock, DollarSign, Brain,
  ShoppingCart, Truck, Eye, Settings, Calculator, ArrowUp, ArrowDown,
  CheckCircle, XCircle, Filter, Upload, Calendar
} from 'lucide-react';
import Link from 'next/link';

interface InventoryItem {
  id: string;
  product_id: string;
  tenant_id: number;
  sku: string;
  title: string;
  category: string;
  current_stock: number;
  reserved_stock: number;
  available_stock: number;
  reorder_level: number;
  max_stock_level: number;
  unit_cost: number;
  unit_price: number;
  total_value: number;
  supplier_info: {
    supplier_id: string;
    supplier_name: string;
    lead_time_days: number;
    minimum_order_qty: number;
  };
  sales_data: {
    daily_sales_velocity: number;
    weekly_sales: number;
    monthly_sales: number;
    days_of_stock_remaining: number;
  };
  ai_recommendations: {
    optimal_stock_level: number;
    reorder_quantity: number;
    reorder_urgency: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    estimated_stockout_date: string;
    recommendations: string[];
  };
  last_restock_date: string;
  last_updated: string;
  status: 'in_stock' | 'low_stock' | 'out_of_stock' | 'overstocked';
}

interface InventoryFilters {
  search: string;
  category: string;
  status: string;
  urgency: string;
  sortBy: string;
}

export default function InventoryPage() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [filteredInventory, setFilteredInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState<InventoryItem | null>(null);
  const [filters, setFilters] = useState<InventoryFilters>({
    search: '',
    category: 'all',
    status: 'all',
    urgency: 'all',
    sortBy: 'urgency_desc'
  });

  // Mock data - Replace with actual API call
  useEffect(() => {
    const mockInventory: InventoryItem[] = [
      {
        id: '1',
        product_id: '1',
        tenant_id: 1,
        sku: 'FIT-001',
        title: 'Smart Fitness Tracker with Heart Rate Monitor',
        category: 'fitness',
        current_stock: 125,
        reserved_stock: 25,
        available_stock: 100,
        reorder_level: 50,
        max_stock_level: 300,
        unit_cost: 49.99,
        unit_price: 84.99,
        total_value: 6248.75,
        supplier_info: {
          supplier_id: 'SUP-001',
          supplier_name: 'TechSource Manufacturing',
          lead_time_days: 14,
          minimum_order_qty: 50
        },
        sales_data: {
          daily_sales_velocity: 8.5,
          weekly_sales: 59,
          monthly_sales: 245,
          days_of_stock_remaining: 12
        },
        ai_recommendations: {
          optimal_stock_level: 180,
          reorder_quantity: 100,
          reorder_urgency: 'MEDIUM',
          estimated_stockout_date: '2025-01-17',
          recommendations: [
            'Reorder within 3 days to avoid stockout',
            'Consider increasing reorder level to 80 units',
            'Sales trending up 15% from last month'
          ]
        },
        last_restock_date: '2024-12-20',
        last_updated: '2025-01-05T15:30:00Z',
        status: 'low_stock'
      },
      {
        id: '2',
        product_id: '2',
        tenant_id: 1,
        sku: 'HOME-002',
        title: 'LED Strip Lights Kit with Smart Control',
        category: 'home_decor',
        current_stock: 15,
        reserved_stock: 12,
        available_stock: 3,
        reorder_level: 30,
        max_stock_level: 150,
        unit_cost: 15.99,
        unit_price: 44.99,
        total_value: 239.85,
        supplier_info: {
          supplier_id: 'SUP-002',
          supplier_name: 'LED Solutions Ltd',
          lead_time_days: 7,
          minimum_order_qty: 25
        },
        sales_data: {
          daily_sales_velocity: 4.2,
          weekly_sales: 29,
          monthly_sales: 124,
          days_of_stock_remaining: 4
        },
        ai_recommendations: {
          optimal_stock_level: 85,
          reorder_quantity: 75,
          reorder_urgency: 'CRITICAL',
          estimated_stockout_date: '2025-01-09',
          recommendations: [
            'URGENT: Place reorder immediately',
            'Consider expedited shipping',
            'High demand product - increase max stock level'
          ]
        },
        last_restock_date: '2024-12-15',
        last_updated: '2025-01-05T16:00:00Z',
        status: 'out_of_stock'
      },
      {
        id: '3',
        product_id: '3',
        tenant_id: 1,
        sku: 'TECH-003',
        title: 'Wireless Phone Charger Pad',
        category: 'electronics',
        current_stock: 250,
        reserved_stock: 15,
        available_stock: 235,
        reorder_level: 40,
        max_stock_level: 200,
        unit_cost: 12.99,
        unit_price: 39.99,
        total_value: 3247.50,
        supplier_info: {
          supplier_id: 'SUP-003',
          supplier_name: 'Wireless World Inc',
          lead_time_days: 10,
          minimum_order_qty: 30
        },
        sales_data: {
          daily_sales_velocity: 2.1,
          weekly_sales: 15,
          monthly_sales: 63,
          days_of_stock_remaining: 112
        },
        ai_recommendations: {
          optimal_stock_level: 120,
          reorder_quantity: 0,
          reorder_urgency: 'LOW',
          estimated_stockout_date: '2025-04-27',
          recommendations: [
            'Overstocked - reduce future orders',
            'Consider promotional campaigns',
            'Monitor for seasonal demand changes'
          ]
        },
        last_restock_date: '2024-12-28',
        last_updated: '2025-01-05T14:45:00Z',
        status: 'overstocked'
      }
    ];

    setTimeout(() => {
      setInventory(mockInventory);
      setFilteredInventory(mockInventory);
      setLoading(false);
    }, 1000);
  }, []);

  // Filter and sort inventory
  useEffect(() => {
    let filtered = inventory.filter(item => {
      const matchesSearch = item.title.toLowerCase().includes(filters.search.toLowerCase()) ||
                           item.sku.toLowerCase().includes(filters.search.toLowerCase());
      
      const matchesCategory = filters.category === 'all' || item.category === filters.category;
      const matchesStatus = filters.status === 'all' || item.status === filters.status;
      const matchesUrgency = filters.urgency === 'all' || item.ai_recommendations.reorder_urgency === filters.urgency;

      return matchesSearch && matchesCategory && matchesStatus && matchesUrgency;
    });

    // Sort inventory
    switch (filters.sortBy) {
      case 'urgency_desc':
        const urgencyOrder = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
        filtered.sort((a, b) => urgencyOrder[b.ai_recommendations.reorder_urgency] - urgencyOrder[a.ai_recommendations.reorder_urgency]);
        break;
      case 'stock_asc':
        filtered.sort((a, b) => a.available_stock - b.available_stock);
        break;
      case 'days_remaining_asc':
        filtered.sort((a, b) => a.sales_data.days_of_stock_remaining - b.sales_data.days_of_stock_remaining);
        break;
      case 'value_desc':
        filtered.sort((a, b) => b.total_value - a.total_value);
        break;
      case 'velocity_desc':
        filtered.sort((a, b) => b.sales_data.daily_sales_velocity - a.sales_data.daily_sales_velocity);
        break;
      default:
        break;
    }

    setFilteredInventory(filtered);
  }, [inventory, filters]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'in_stock': return 'bg-green-100 text-green-800 border-green-200';
      case 'low_stock': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'out_of_stock': return 'bg-red-100 text-red-800 border-red-200';
      case 'overstocked': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'CRITICAL': return 'bg-red-200 text-red-900 border-red-300';
      case 'HIGH': return 'bg-red-100 text-red-800 border-red-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStockHealthPercentage = (item: InventoryItem) => {
    if (item.status === 'out_of_stock') return 0;
    return Math.min(100, (item.available_stock / item.reorder_level) * 50);
  };

  const InventoryCard = ({ item }: { item: InventoryItem }) => {
    const stockHealthPercentage = getStockHealthPercentage(item);
    
    return (
      <Card className="hover:shadow-lg transition-all duration-300 cursor-pointer" onClick={() => setSelectedItem(item)}>
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="space-y-1 flex-1 mr-3">
              <h3 className="font-semibold text-sm line-clamp-2">{item.title}</h3>
              <p className="text-xs text-gray-500">SKU: {item.sku}</p>
            </div>
            <div className="flex flex-col items-end space-y-1">
              <Badge className={getStatusColor(item.status)} variant="outline">
                {item.status.replace('_', ' ').toUpperCase()}
              </Badge>
              <Badge className={getUrgencyColor(item.ai_recommendations.reorder_urgency)} variant="outline">
                {item.ai_recommendations.reorder_urgency}
              </Badge>
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* Stock Levels */}
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Available Stock</span>
              <span className="font-bold text-lg">{item.available_stock}</span>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span>Stock Health</span>
                <span>{stockHealthPercentage.toFixed(0)}%</span>
              </div>
              <Progress value={stockHealthPercentage} className="h-2" />
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-gray-500">Reserved:</span>
                <span className="ml-1 font-medium">{item.reserved_stock}</span>
              </div>
              <div>
                <span className="text-gray-500">Total:</span>
                <span className="ml-1 font-medium">{item.current_stock}</span>
              </div>
              <div>
                <span className="text-gray-500">Reorder at:</span>
                <span className="ml-1 font-medium">{item.reorder_level}</span>
              </div>
              <div>
                <span className="text-gray-500">Max level:</span>
                <span className="ml-1 font-medium">{item.max_stock_level}</span>
              </div>
            </div>
          </div>

          {/* Financial Info */}
          <div className="space-y-2 pt-2 border-t">
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-600">Unit Cost:</span>
              <span>${item.unit_cost.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-600">Unit Price:</span>
              <span className="font-medium text-orange-600">${item.unit_price.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center text-sm font-semibold border-t pt-2">
              <span>Total Value:</span>
              <span className="text-green-600">${item.total_value.toLocaleString()}</span>
            </div>
          </div>

          {/* Sales Velocity */}
          <div className="space-y-2 pt-2 border-t">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-purple-500" />
              <span className="text-sm font-medium">Sales Performance</span>
            </div>
            
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center gap-1">
                <TrendingUp className="w-3 h-3 text-gray-400" />
                <span>{item.sales_data.daily_sales_velocity.toFixed(1)}/day</span>
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="w-3 h-3 text-gray-400" />
                <span>{item.sales_data.monthly_sales}/month</span>
              </div>
            </div>

            <div className="text-center">
              <Badge className={
                item.sales_data.days_of_stock_remaining <= 7 ? 
                'bg-red-100 text-red-800' : 
                item.sales_data.days_of_stock_remaining <= 14 ? 
                'bg-yellow-100 text-yellow-800' : 
                'bg-green-100 text-green-800'
              }>
                {item.sales_data.days_of_stock_remaining} days remaining
              </Badge>
            </div>
          </div>

          {/* AI Recommendations */}
          <div className="space-y-2 pt-2 border-t">
            <div className="flex items-center gap-2">
              <Brain className="w-4 h-4 text-purple-500" />
              <span className="text-sm font-medium">AI Recommendations</span>
            </div>
            
            {item.ai_recommendations.recommendations.slice(0, 2).map((rec, index) => (
              <div key={index} className="text-xs text-gray-600 bg-purple-50 p-2 rounded">
                {rec}
              </div>
            ))}

            {item.ai_recommendations.reorder_quantity > 0 && (
              <div className="bg-blue-50 p-2 rounded">
                <div className="text-xs text-blue-700">
                  <strong>Recommended Reorder:</strong> {item.ai_recommendations.reorder_quantity} units
                </div>
                <div className="text-xs text-blue-600">
                  Optimal level: {item.ai_recommendations.optimal_stock_level} units
                </div>
              </div>
            )}
          </div>

          {/* Supplier Info */}
          <div className="flex justify-between items-center text-xs text-gray-500 pt-2 border-t">
            <div className="flex items-center gap-1">
              <Truck className="w-3 h-3" />
              <span>{item.supplier_info.supplier_name}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>{item.supplier_info.lead_time_days}d lead</span>
            </div>
          </div>

          {/* Action Button */}
          <div className="pt-2">
            {item.ai_recommendations.reorder_urgency === 'CRITICAL' || item.ai_recommendations.reorder_urgency === 'HIGH' ? (
              <Button size="sm" className="w-full bg-red-500 hover:bg-red-600 text-white">
                <AlertTriangle className="w-3 h-3 mr-1" />
                Urgent Reorder
              </Button>
            ) : item.ai_recommendations.reorder_quantity > 0 ? (
              <Button size="sm" variant="outline" className="w-full">
                <Package className="w-3 h-3 mr-1" />
                Reorder {item.ai_recommendations.reorder_quantity} units
              </Button>
            ) : (
              <Button size="sm" variant="ghost" className="w-full">
                <Eye className="w-3 h-3 mr-1" />
                View Details
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100 p-6">
        <div className="container mx-auto space-y-6">
          <div className="space-y-4">
            <Skeleton className="h-8 w-64" />
            <Skeleton className="h-4 w-96" />
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="space-y-4">
                <Skeleton className="h-80 w-full" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const totalValue = inventory.reduce((sum, item) => sum + item.total_value, 0);
  const criticalItems = inventory.filter(item => item.ai_recommendations.reorder_urgency === 'CRITICAL').length;
  const outOfStockItems = inventory.filter(item => item.status === 'out_of_stock').length;
  const averageVelocity = inventory.reduce((sum, item) => sum + item.sales_data.daily_sales_velocity, 0) / inventory.length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Inventory Management</h1>
              <p className="text-gray-600 mt-1">
                AI-powered inventory optimization and stock level monitoring
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="outline">
                <Upload className="w-4 h-4 mr-2" />
                Bulk Update
              </Button>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Export Report
              </Button>
              <Button variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Sync Inventory
              </Button>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <DollarSign className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-green-600">
                      {totalValue.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })}
                    </p>
                    <p className="text-sm text-gray-600">Total Value</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-red-100 rounded-lg">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-red-600">{criticalItems}</p>
                    <p className="text-sm text-gray-600">Critical Alerts</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <XCircle className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-orange-600">{outOfStockItems}</p>
                    <p className="text-sm text-gray-600">Out of Stock</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-purple-600">
                      {averageVelocity.toFixed(1)}
                    </p>
                    <p className="text-sm text-gray-600">Avg Daily Sales</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Package className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">{inventory.length}</p>
                    <p className="text-sm text-gray-600">Total SKUs</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Critical Alerts */}
        {criticalItems > 0 && (
          <Alert className="border-red-200 bg-red-50">
            <AlertTriangle className="w-4 h-4 text-red-600" />
            <AlertDescription className="text-red-700">
              <strong>{criticalItems} items require immediate attention</strong> - Critical stock levels detected. 
              Review AI recommendations and place reorders to avoid stockouts.
            </AlertDescription>
          </Alert>
        )}

        {/* Filters */}
        <Card>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
              <div className="md:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input 
                    placeholder="Search inventory..." 
                    className="pl-10"
                    value={filters.search}
                    onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
                  />
                </div>
              </div>
              
              <Select value={filters.category} onValueChange={(value) => setFilters(prev => ({ ...prev, category: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="fitness">Fitness</SelectItem>
                  <SelectItem value="home_decor">Home Decor</SelectItem>
                  <SelectItem value="electronics">Electronics</SelectItem>
                  <SelectItem value="fashion">Fashion</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filters.status} onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Stock Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="in_stock">In Stock</SelectItem>
                  <SelectItem value="low_stock">Low Stock</SelectItem>
                  <SelectItem value="out_of_stock">Out of Stock</SelectItem>
                  <SelectItem value="overstocked">Overstocked</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filters.urgency} onValueChange={(value) => setFilters(prev => ({ ...prev, urgency: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Reorder Urgency" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Urgency</SelectItem>
                  <SelectItem value="CRITICAL">Critical</SelectItem>
                  <SelectItem value="HIGH">High</SelectItem>
                  <SelectItem value="MEDIUM">Medium</SelectItem>
                  <SelectItem value="LOW">Low</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={filters.sortBy} onValueChange={(value) => setFilters(prev => ({ ...prev, sortBy: value }))}>
                <SelectTrigger>
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="urgency_desc">Urgency (High to Low)</SelectItem>
                  <SelectItem value="stock_asc">Stock Level (Low to High)</SelectItem>
                  <SelectItem value="days_remaining_asc">Days Remaining (Low to High)</SelectItem>
                  <SelectItem value="value_desc">Total Value (High to Low)</SelectItem>
                  <SelectItem value="velocity_desc">Sales Velocity (High to Low)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div className="flex items-center justify-between pt-4 border-t">
              <span className="text-sm text-gray-600">
                {filteredInventory.length} of {inventory.length} items
              </span>
              <div className="flex items-center gap-2">
                {filteredInventory.filter(item => item.ai_recommendations.reorder_urgency === 'CRITICAL').length > 0 && (
                  <Badge variant="destructive">
                    {filteredInventory.filter(item => item.ai_recommendations.reorder_urgency === 'CRITICAL').length} critical
                  </Badge>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Inventory Grid */}
        {filteredInventory.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No inventory found</h3>
              <p className="text-gray-600 mb-6">
                No items match your current filters. Try adjusting your search criteria.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredInventory.map((item) => (
              <InventoryCard key={item.id} item={item} />
            ))}
          </div>
        )}

        {/* Load More */}
        {filteredInventory.length > 0 && (
          <div className="text-center">
            <Button variant="outline" size="lg">
              <Clock className="w-4 h-4 mr-2" />
              Load More Items
            </Button>
          </div>
        )}
      </div>

      {/* Detailed Item Modal */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <div>
                <CardTitle className="text-xl">{selectedItem.title}</CardTitle>
                <p className="text-gray-600">SKU: {selectedItem.sku}</p>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setSelectedItem(null)}>
                ×
              </Button>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Stock Overview */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Stock Levels</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <span>Current Stock:</span>
                      <span className="font-bold text-xl">{selectedItem.current_stock}</span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <span>Available:</span>
                      <span className="font-bold text-lg text-green-600">{selectedItem.available_stock}</span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <span>Reserved:</span>
                      <span className="font-medium text-yellow-600">{selectedItem.reserved_stock}</span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-yellow-50 border border-yellow-200 rounded">
                      <span>Reorder Level:</span>
                      <span className="font-medium text-yellow-700">{selectedItem.reorder_level}</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Financial Overview</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <span>Unit Cost:</span>
                      <span>${selectedItem.unit_cost.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <span>Unit Price:</span>
                      <span className="font-bold text-orange-600">${selectedItem.unit_price.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-green-50 border border-green-200 rounded">
                      <span>Total Value:</span>
                      <span className="font-bold text-green-700">${selectedItem.total_value.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-purple-50 border border-purple-200 rounded">
                      <span>Profit Margin:</span>
                      <span className="font-bold text-purple-700">
                        {((selectedItem.unit_price - selectedItem.unit_cost) / selectedItem.unit_price * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Sales Performance */}
              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Sales Performance</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-3 bg-blue-50 rounded">
                    <div className="text-2xl font-bold text-blue-600">
                      {selectedItem.sales_data.daily_sales_velocity.toFixed(1)}
                    </div>
                    <div className="text-sm text-blue-700">Daily Velocity</div>
                  </div>
                  <div className="text-center p-3 bg-green-50 rounded">
                    <div className="text-2xl font-bold text-green-600">
                      {selectedItem.sales_data.weekly_sales}
                    </div>
                    <div className="text-sm text-green-700">Weekly Sales</div>
                  </div>
                  <div className="text-center p-3 bg-purple-50 rounded">
                    <div className="text-2xl font-bold text-purple-600">
                      {selectedItem.sales_data.monthly_sales}
                    </div>
                    <div className="text-sm text-purple-700">Monthly Sales</div>
                  </div>
                  <div className="text-center p-3 bg-orange-50 rounded">
                    <div className="text-2xl font-bold text-orange-600">
                      {selectedItem.sales_data.days_of_stock_remaining}
                    </div>
                    <div className="text-sm text-orange-700">Days Remaining</div>
                  </div>
                </div>
              </div>

              {/* AI Recommendations */}
              <div className="space-y-4">
                <h3 className="font-semibold text-lg flex items-center gap-2">
                  <Brain className="w-5 h-5 text-purple-500" />
                  AI Recommendations
                </h3>
                <div className="space-y-3">
                  <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge className={getUrgencyColor(selectedItem.ai_recommendations.reorder_urgency)} variant="outline">
                        {selectedItem.ai_recommendations.reorder_urgency} PRIORITY
                      </Badge>
                      <span className="text-sm text-gray-600">
                        Estimated stockout: {new Date(selectedItem.ai_recommendations.estimated_stockout_date).toLocaleDateString()}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                      <div>
                        <span className="text-sm text-gray-600">Optimal Stock Level:</span>
                        <div className="text-lg font-bold text-purple-600">
                          {selectedItem.ai_recommendations.optimal_stock_level} units
                        </div>
                      </div>
                      <div>
                        <span className="text-sm text-gray-600">Recommended Reorder:</span>
                        <div className="text-lg font-bold text-blue-600">
                          {selectedItem.ai_recommendations.reorder_quantity} units
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      {selectedItem.ai_recommendations.recommendations.map((rec, index) => (
                        <div key={index} className="flex items-start gap-2 text-sm">
                          <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span>{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Supplier Information */}
              <div className="space-y-4">
                <h3 className="font-semibold text-lg">Supplier Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="text-sm text-gray-600">Supplier</div>
                    <div className="font-medium">{selectedItem.supplier_info.supplier_name}</div>
                  </div>
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="text-sm text-gray-600">Lead Time</div>
                    <div className="font-medium">{selectedItem.supplier_info.lead_time_days} days</div>
                  </div>
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="text-sm text-gray-600">Minimum Order</div>
                    <div className="font-medium">{selectedItem.supplier_info.minimum_order_qty} units</div>
                  </div>
                  <div className="p-3 bg-gray-50 rounded">
                    <div className="text-sm text-gray-600">Last Restock</div>
                    <div className="font-medium">{new Date(selectedItem.last_restock_date).toLocaleDateString()}</div>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4 border-t">
                <Button className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                  <Package className="w-4 h-4 mr-2" />
                  Place Reorder
                </Button>
                <Button variant="outline" className="flex-1">
                  <Settings className="w-4 h-4 mr-2" />
                  Update Levels
                </Button>
                <Button variant="outline" className="flex-1">
                  <Calculator className="w-4 h-4 mr-2" />
                  Optimize
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}