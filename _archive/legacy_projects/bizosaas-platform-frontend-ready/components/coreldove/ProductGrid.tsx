"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Search, Grid3X3, List, Eye, Star, Package, TrendingUp, 
  Brain, DollarSign, AlertTriangle, Sparkles, Target, Activity
} from 'lucide-react';
import { coreLDoveAPI, Product } from '@/lib/coreldove-api';

interface ProductGridProps {
  viewMode?: 'grid' | 'list';
  onViewModeChange?: (mode: 'grid' | 'list') => void;
  onProductSelect?: (product: Product) => void;
  className?: string;
}

interface ProductFilters {
  search: string;
  category: string;
  classification: string;
  status: string;
  sortBy: string;
}

export function ProductGrid({ 
  viewMode = 'grid', 
  onViewModeChange,
  onProductSelect,
  className = ''
}: ProductGridProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<ProductFilters>({
    search: '',
    category: 'all',
    classification: 'all',
    status: 'all',
    sortBy: 'score_desc'
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Fetch products
  useEffect(() => {
    fetchProducts();
  }, [filters, currentPage]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await coreLDoveAPI.getProducts({
        search: filters.search || undefined,
        category: filters.category !== 'all' ? filters.category : undefined,
        classification: filters.classification !== 'all' ? filters.classification : undefined,
        status: filters.status !== 'all' ? filters.status : undefined,
        page: currentPage,
        per_page: 20
      });

      if (response.success && response.data) {
        setProducts(response.data.items);
        setTotalPages(response.data.pages);
      } else {
        console.error('Failed to fetch products:', response.error);
        // Fallback to mock data for demo
        setProducts([]);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
      // Fallback to mock data for demo
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

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
    <Card 
      className="hover:shadow-lg transition-all duration-300 cursor-pointer border-orange-200"
      onClick={() => onProductSelect?.(product)}
    >
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
                <Package className="w-3 h-3 text-gray-400" />
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
          {product.inventory && product.inventory.available <= (product.inventory.reorder_level || 0) && (
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

  const ProductListItem = ({ product }: { product: Product }) => (
    <Card 
      className="hover:shadow-md transition-all duration-200 cursor-pointer"
      onClick={() => onProductSelect?.(product)}
    >
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          {/* Product Image */}
          <div className="w-16 h-16 bg-gradient-to-br from-orange-100 to-red-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <Package className="w-8 h-8 text-orange-400" />
          </div>

          {/* Product Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0 mr-4">
                <h3 className="font-semibold truncate">{product.title}</h3>
                <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                  <span>SKU: {product.sku}</span>
                  <span>ASIN: {product.asin}</span>
                  <Badge className={getClassificationColor(product.ai_metrics.classification)} variant="outline">
                    {product.ai_metrics.classification}
                  </Badge>
                </div>
              </div>

              {/* Pricing */}
              <div className="text-right flex-shrink-0">
                <div className="font-bold text-lg text-orange-600">
                  ${product.pricing.current_selling_price.toFixed(2)}
                </div>
                <div className="text-sm text-gray-600">
                  Cost: ${product.pricing.source_price.toFixed(2)}
                </div>
                <Badge className="bg-gradient-to-r from-orange-500 to-red-500 text-white mt-1">
                  {product.pricing.profit_margin.toFixed(1)}% Profit
                </Badge>
              </div>
            </div>

            {/* Metrics */}
            <div className="flex items-center gap-6 mt-3 text-sm">
              <div className="flex items-center gap-1">
                <Brain className="w-4 h-4 text-purple-500" />
                <span>AI Score: {product.ai_metrics.dropship_score}</span>
              </div>
              {product.performance && (
                <>
                  <div className="flex items-center gap-1">
                    <Eye className="w-4 h-4 text-gray-400" />
                    <span>{product.performance.views.toLocaleString()} views</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Package className="w-4 h-4 text-gray-400" />
                    <span>{product.performance.orders} orders</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <TrendingUp className="w-4 h-4 text-gray-400" />
                    <span>{product.performance.conversion_rate}% CVR</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <div className={`space-y-6 ${className}`}>
        {/* Filter Skeleton */}
        <div className="flex gap-4">
          <Skeleton className="h-10 flex-1" />
          <Skeleton className="h-10 w-40" />
          <Skeleton className="h-10 w-40" />
        </div>
        
        {/* Grid Skeleton */}
        <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' : 'grid-cols-1'} gap-6`}>
          {[...Array(8)].map((_, i) => (
            <Skeleton key={i} className={viewMode === 'grid' ? 'h-96' : 'h-32'} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Filters */}
      <Card>
        <CardContent className="p-6">
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
          
          <div className="flex items-center justify-between pt-4 border-t">
            <span className="text-sm text-gray-600">
              {products.length} products found
            </span>
            
            <div className="flex items-center gap-2">
              {onViewModeChange && (
                <>
                  <Button
                    variant={viewMode === 'grid' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => onViewModeChange('grid')}
                  >
                    <Grid3X3 className="w-4 h-4" />
                  </Button>
                  <Button
                    variant={viewMode === 'list' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => onViewModeChange('list')}
                  >
                    <List className="w-4 h-4" />
                  </Button>
                </>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Products */}
      {products.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center">
            <Package className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No products found</h3>
            <p className="text-gray-600">
              Try adjusting your filters or search terms.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' : 'grid-cols-1'} gap-6`}>
          {products.map((product) => (
            viewMode === 'grid' ? (
              <ProductCard key={product.id} product={product} />
            ) : (
              <ProductListItem key={product.id} product={product} />
            )
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2">
          <Button
            variant="outline"
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
          >
            Previous
          </Button>
          <span className="text-sm text-gray-600">
            Page {currentPage} of {totalPages}
          </span>
          <Button
            variant="outline"
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
}