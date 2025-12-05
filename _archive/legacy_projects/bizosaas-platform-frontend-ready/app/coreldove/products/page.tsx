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
import { 
  Search, Filter, Grid3X3, List, Plus, TrendingUp, TrendingDown, 
  Star, Eye, ShoppingCart, Zap, Target, AlertTriangle, Sparkles,
  Package, Truck, DollarSign, Brain, Activity, Clock
} from 'lucide-react';
import Link from 'next/link';

interface Product {
  id: string;
  tenant_id: number;
  asin: string;
  sku: string;
  title: string;
  category: string;
  description?: string;
  image_url?: string;
  pricing: {
    source_price: number;
    recommended_price: number;
    current_selling_price: number;
    profit_margin: number;
  };
  ai_metrics: {
    dropship_score: number;
    classification: 'HERO' | 'GOOD' | 'MODERATE' | 'POOR';
    profit_margin_estimate: number;
    market_demand?: number;
    competition_level?: number;
  };
  status: 'active' | 'draft' | 'archived';
  created_at: string;
  updated_at: string;
  inventory?: {
    stock_level: number;
    reserved: number;
    available: number;
    reorder_level: number;
  };
  performance?: {
    views: number;
    orders: number;
    conversion_rate: number;
    total_revenue: number;
  };
}

interface ProductFilters {
  search: string;
  category: string;
  classification: string;
  status: string;
  sortBy: string;
  priceRange: [number, number];
  scoreRange: [number, number];
}

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [filters, setFilters] = useState<ProductFilters>({
    search: '',
    category: 'all',
    classification: 'all',
    status: 'all',
    sortBy: 'score_desc',
    priceRange: [0, 500],
    scoreRange: [0, 100]
  });

  // Mock data - Replace with actual API call
  useEffect(() => {
    const mockProducts: Product[] = [
      {
        id: '1',
        tenant_id: 1,
        asin: 'B08N5WRWNW',
        sku: 'FIT-001',
        title: 'Smart Fitness Tracker with Heart Rate Monitor',
        category: 'fitness',
        description: 'Advanced health monitoring with sleep tracking and waterproof design',
        image_url: '/placeholder-product-1.jpg',
        pricing: {
          source_price: 49.99,
          recommended_price: 89.99,
          current_selling_price: 84.99,
          profit_margin: 70.0
        },
        ai_metrics: {
          dropship_score: 92,
          classification: 'HERO',
          profit_margin_estimate: 0.7,
          market_demand: 85,
          competition_level: 35
        },
        status: 'active',
        created_at: '2025-01-05T10:00:00Z',
        updated_at: '2025-01-05T15:30:00Z',
        inventory: {
          stock_level: 150,
          reserved: 25,
          available: 125,
          reorder_level: 50
        },
        performance: {
          views: 2847,
          orders: 89,
          conversion_rate: 3.1,
          total_revenue: 7563.11
        }
      },
      {
        id: '2',
        tenant_id: 1,
        asin: 'B09K8HJMT2',
        sku: 'HOME-002',
        title: 'LED Strip Lights Kit with Smart Control',
        category: 'home_decor',
        description: 'RGB LED strip lights with app control and music sync',
        image_url: '/placeholder-product-2.jpg',
        pricing: {
          source_price: 15.99,
          recommended_price: 49.99,
          current_selling_price: 44.99,
          profit_margin: 181.0
        },
        ai_metrics: {
          dropship_score: 78,
          classification: 'GOOD',
          profit_margin_estimate: 0.65,
          market_demand: 72,
          competition_level: 60
        },
        status: 'active',
        created_at: '2025-01-04T14:20:00Z',
        updated_at: '2025-01-05T09:15:00Z',
        inventory: {
          stock_level: 89,
          reserved: 12,
          available: 77,
          reorder_level: 30
        },
        performance: {
          views: 1543,
          orders: 34,
          conversion_rate: 2.2,
          total_revenue: 1529.66
        }
      }
    ];

    setTimeout(() => {
      setProducts(mockProducts);
      setFilteredProducts(mockProducts);
      setLoading(false);
    }, 1000);
  }, []);

  // Filter and sort products
  useEffect(() => {
    let filtered = products.filter(product => {
      const matchesSearch = product.title.toLowerCase().includes(filters.search.toLowerCase()) ||
                           product.sku.toLowerCase().includes(filters.search.toLowerCase()) ||
                           product.asin.toLowerCase().includes(filters.search.toLowerCase());
      
      const matchesCategory = filters.category === 'all' || product.category === filters.category;
      const matchesClassification = filters.classification === 'all' || product.ai_metrics.classification === filters.classification;
      const matchesStatus = filters.status === 'all' || product.status === filters.status;
      
      const matchesPrice = product.pricing.current_selling_price >= filters.priceRange[0] &&
                          product.pricing.current_selling_price <= filters.priceRange[1];
      
      const matchesScore = product.ai_metrics.dropship_score >= filters.scoreRange[0] &&
                          product.ai_metrics.dropship_score <= filters.scoreRange[1];

      return matchesSearch && matchesCategory && matchesClassification && matchesStatus && matchesPrice && matchesScore;
    });

    // Sort products
    switch (filters.sortBy) {
      case 'score_desc':
        filtered.sort((a, b) => b.ai_metrics.dropship_score - a.ai_metrics.dropship_score);
        break;
      case 'score_asc':
        filtered.sort((a, b) => a.ai_metrics.dropship_score - b.ai_metrics.dropship_score);
        break;
      case 'profit_desc':
        filtered.sort((a, b) => b.pricing.profit_margin - a.pricing.profit_margin);
        break;
      case 'profit_asc':
        filtered.sort((a, b) => a.pricing.profit_margin - b.pricing.profit_margin);
        break;
      case 'revenue_desc':
        filtered.sort((a, b) => (b.performance?.total_revenue || 0) - (a.performance?.total_revenue || 0));
        break;
      case 'name_asc':
        filtered.sort((a, b) => a.title.localeCompare(b.title));
        break;
      default:
        break;
    }

    setFilteredProducts(filtered);
  }, [products, filters]);

  const getClassificationColor = (classification: string) => {
    switch (classification) {
      case 'HERO': return 'bg-green-100 text-green-800 border-green-200';
      case 'GOOD': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'MODERATE': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'POOR': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getClassificationIcon = (classification: string) => {
    switch (classification) {
      case 'HERO': return <Sparkles className="w-3 h-3" />;
      case 'GOOD': return <Target className="w-3 h-3" />;
      case 'MODERATE': return <Activity className="w-3 h-3" />;
      case 'POOR': return <AlertTriangle className="w-3 h-3" />;
      default: return null;
    }
  };

  const ProductCard = ({ product }: { product: Product }) => (
    <Card className="hover:shadow-lg transition-all duration-300 border-orange-200">
      <CardHeader className="p-4">
        <div className="aspect-square bg-gradient-to-br from-orange-100 to-red-100 rounded-lg mb-3 relative overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center">
            <Package className="w-12 h-12 text-orange-400" />
          </div>
          <div className="absolute top-2 right-2 space-y-1">
            <Badge className={`${getClassificationColor(product.ai_metrics.classification)} flex items-center gap-1`}>
              {getClassificationIcon(product.ai_metrics.classification)}
              {product.ai_metrics.classification}
            </Badge>
          </div>
          <div className="absolute bottom-2 left-2">
            <Badge variant="secondary" className="text-xs">
              Score: {product.ai_metrics.dropship_score}
            </Badge>
          </div>
        </div>
        
        <div className="space-y-2">
          <h3 className="font-semibold text-sm line-clamp-2 min-h-[2.5rem]">
            {product.title}
          </h3>
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>SKU: {product.sku}</span>
            <span>ASIN: {product.asin}</span>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-4 pt-0">
        <div className="space-y-3">
          {/* Pricing */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-500">Source:</span>
              <span>${product.pricing.source_price.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-500">Selling:</span>
              <span className="font-bold text-orange-600">${product.pricing.current_selling_price.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center text-sm font-semibold border-t pt-2">
              <span>Profit:</span>
              <span className="text-green-600">
                ${(product.pricing.current_selling_price - product.pricing.source_price).toFixed(2)}
              </span>
            </div>
            <div className="text-center">
              <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white">
                {product.pricing.profit_margin.toFixed(1)}% Margin
              </Badge>
            </div>
          </div>

          {/* Performance Metrics */}
          {product.performance && (
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="flex items-center gap-1">
                <Eye className="w-3 h-3 text-gray-400" />
                <span>{product.performance.views.toLocaleString()} views</span>
              </div>
              <div className="flex items-center gap-1">
                <ShoppingCart className="w-3 h-3 text-gray-400" />
                <span>{product.performance.orders} orders</span>
              </div>
              <div className="flex items-center gap-1">
                <TrendingUp className="w-3 h-3 text-gray-400" />
                <span>{product.performance.conversion_rate}% CVR</span>
              </div>
              <div className="flex items-center gap-1">
                <DollarSign className="w-3 h-3 text-gray-400" />
                <span>${product.performance.total_revenue.toLocaleString()}</span>
              </div>
            </div>
          )}

          {/* AI Metrics */}
          <div className="space-y-2 pt-2 border-t">
            <div className="flex items-center gap-2">
              <Brain className="w-4 h-4 text-purple-500" />
              <span className="text-xs font-medium">AI Analysis</span>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span>Market Demand:</span>
                <span>{product.ai_metrics.market_demand || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span>Competition:</span>
                <span>{product.ai_metrics.competition_level || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Inventory Alert */}
          {product.inventory && product.inventory.available <= product.inventory.reorder_level && (
            <div className="bg-yellow-50 border border-yellow-200 rounded p-2">
              <div className="flex items-center gap-1 text-yellow-700 text-xs">
                <AlertTriangle className="w-3 h-3" />
                <span>Low Stock: {product.inventory.available} remaining</span>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );

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
                <Skeleton className="aspect-square w-full" />
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Product Catalog</h1>
              <p className="text-gray-600 mt-1">
                AI-powered product management and optimization
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button asChild className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                <Link href="/coreldove/sourcing">
                  <Plus className="w-4 h-4 mr-2" />
                  Source Products
                </Link>
              </Button>
              <Button variant="outline">
                <Truck className="w-4 h-4 mr-2" />
                Bulk Actions
              </Button>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-100 rounded-lg">
                    <Sparkles className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-green-600">
                      {products.filter(p => p.ai_metrics.classification === 'HERO').length}
                    </p>
                    <p className="text-sm text-gray-600">Hero Products</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Target className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-blue-600">
                      {products.filter(p => p.status === 'active').length}
                    </p>
                    <p className="text-sm text-gray-600">Active Products</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <DollarSign className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-orange-600">
                      {products.reduce((sum, p) => sum + (p.performance?.total_revenue || 0), 0).toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 })}
                    </p>
                    <p className="text-sm text-gray-600">Total Revenue</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Brain className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-purple-600">
                      {Math.round(products.reduce((sum, p) => sum + p.ai_metrics.dropship_score, 0) / products.length) || 0}
                    </p>
                    <p className="text-sm text-gray-600">Avg AI Score</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Filters and Search */}
        <Card>
          <CardContent className="p-6">
            <Tabs defaultValue="filters" className="space-y-4">
              <TabsList>
                <TabsTrigger value="filters">Filters & Search</TabsTrigger>
                <TabsTrigger value="advanced">Advanced Filters</TabsTrigger>
              </TabsList>
              
              <TabsContent value="filters" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                  <div className="md:col-span-2">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <Input 
                        placeholder="Search products..." 
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
                  
                  <Select value={filters.classification} onValueChange={(value) => setFilters(prev => ({ ...prev, classification: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="AI Classification" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Classifications</SelectItem>
                      <SelectItem value="HERO">Hero Products</SelectItem>
                      <SelectItem value="GOOD">Good Products</SelectItem>
                      <SelectItem value="MODERATE">Moderate Products</SelectItem>
                      <SelectItem value="POOR">Poor Products</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Select value={filters.status} onValueChange={(value) => setFilters(prev => ({ ...prev, status: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Status</SelectItem>
                      <SelectItem value="active">Active</SelectItem>
                      <SelectItem value="draft">Draft</SelectItem>
                      <SelectItem value="archived">Archived</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Select value={filters.sortBy} onValueChange={(value) => setFilters(prev => ({ ...prev, sortBy: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Sort by" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="score_desc">AI Score (High to Low)</SelectItem>
                      <SelectItem value="score_asc">AI Score (Low to High)</SelectItem>
                      <SelectItem value="profit_desc">Profit Margin (High to Low)</SelectItem>
                      <SelectItem value="profit_asc">Profit Margin (Low to High)</SelectItem>
                      <SelectItem value="revenue_desc">Revenue (High to Low)</SelectItem>
                      <SelectItem value="name_asc">Name (A to Z)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </TabsContent>
              
              <TabsContent value="advanced" className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Price Range: $${filters.priceRange[0]} - $${filters.priceRange[1]}</label>
                    <div className="px-3">
                      <input
                        type="range"
                        min={0}
                        max={500}
                        step={5}
                        value={filters.priceRange[1]}
                        onChange={(e) => setFilters(prev => ({ ...prev, priceRange: [prev.priceRange[0], parseInt(e.target.value)] }))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <label className="text-sm font-medium">AI Score Range: {filters.scoreRange[0]} - {filters.scoreRange[1]}</label>
                    <div className="px-3">
                      <input
                        type="range"
                        min={0}
                        max={100}
                        step={5}
                        value={filters.scoreRange[1]}
                        onChange={(e) => setFilters(prev => ({ ...prev, scoreRange: [prev.scoreRange[0], parseInt(e.target.value)] }))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                      />
                    </div>
                  </div>
                </div>
              </TabsContent>
            </Tabs>
            
            <div className="flex items-center justify-between pt-4 border-t">
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">
                  {filteredProducts.length} of {products.length} products
                </span>
                {filters.search && (
                  <Badge variant="secondary">
                    Search: "{filters.search}"
                  </Badge>
                )}
              </div>
              
              <div className="flex items-center gap-2">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                >
                  <Grid3X3 className="w-4 h-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                >
                  <List className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Products Grid */}
        {filteredProducts.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No products found</h3>
              <p className="text-gray-600 mb-6">
                Try adjusting your filters or search terms, or add new products from the sourcing dashboard.
              </p>
              <Button asChild className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                <Link href="/coreldove/sourcing">
                  <Plus className="w-4 h-4 mr-2" />
                  Source New Products
                </Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' : 'grid-cols-1'} gap-6`}>
            {filteredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

        {/* Load More */}
        {filteredProducts.length > 0 && (
          <div className="text-center">
            <Button variant="outline" size="lg">
              <Clock className="w-4 h-4 mr-2" />
              Load More Products
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}