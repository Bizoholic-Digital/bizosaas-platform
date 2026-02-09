"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Textarea } from '@/components/ui/textarea';
import { 
  Search, Filter, Plus, TrendingUp, TrendingDown, AlertCircle, CheckCircle, 
  Star, Eye, ShoppingCart, Zap, Target, Package, Loader2, Brain, 
  ArrowRight, BarChart3, DollarSign, Users, Clock, Sparkles, Upload, Download,
  Bot, RefreshCw, Truck, Calculator
} from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import Link from 'next/link';

interface SearchCriteria {
  keywords: string[];
  category: string;
  minPrice: number;
  maxPrice: number;
  minRating: number;
  maxResults: number;
  excludeBrands: string[];
  profitMarginTarget: number;
}

interface ProductResult {
  asin: string;
  title: string;
  price: number;
  rating: number;
  reviewCount: number;
  imageUrl: string;
  category: string;
  brand: string;
  availability: string;
  primeEligible: boolean;
  profitPotential: string;
  status?: 'pending_approval' | 'approved' | 'rejected';
  aiAnalysis?: {
    demandScore: number;
    competitionScore: number;
    profitabilityScore: number;
  };
}

interface SearchTask {
  searchTaskId: string;
  status: string;
  estimatedCompletion: string;
  products?: ProductResult[];
  totalFound?: number;
  processingTime?: string;
  error?: string;
}

interface ApprovalWorkflow {
  id: string;
  productId: string;
  reviewerId: string;
  status: 'pending' | 'approved' | 'rejected' | 'needs_revision';
  notes?: string;
  feedback?: any;
  createdAt: string;
}

export default function ProductSourcingPage() {
  const [searchCriteria, setSearchCriteria] = useState<SearchCriteria>({
    keywords: [],
    category: 'all',
    minPrice: 0,
    maxPrice: 1000,
    minRating: 3.0,
    maxResults: 50,
    excludeBrands: [],
    profitMarginTarget: 30
  });

  const [keywordInput, setKeywordInput] = useState('');
  const [excludeBrandInput, setExcludeBrandInput] = useState('');
  const [searchTasks, setSearchTasks] = useState<SearchTask[]>([]);
  const [activeSearch, setActiveSearch] = useState<SearchTask | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedProducts, setSelectedProducts] = useState<Set<string>>(new Set());
  const [approvalMode, setApprovalMode] = useState(false);
  const [pendingApprovals, setPendingApprovals] = useState<ProductResult[]>([]);

  // Mock data for demonstration
  const [featuredOpportunities] = useState([
    {
      category: "Electronics",
      avgProfitMargin: 65,
      demandScore: 89,
      competitionLevel: "Medium",
      trending: "up",
      productCount: 127
    },
    {
      category: "Home & Garden",
      avgProfitMargin: 45,
      demandScore: 76,
      competitionLevel: "Low",
      trending: "up",
      productCount: 89
    },
    {
      category: "Sports & Outdoors",
      avgProfitMargin: 38,
      demandScore: 82,
      competitionLevel: "High",
      trending: "stable",
      productCount: 156
    }
  ]);

  const [automationWorkflows] = useState([
    {
      id: '1',
      name: 'Amazon Product Scanner',
      description: 'Automated product discovery from Amazon with profitability analysis',
      status: 'idle',
      lastRun: '2 hours ago',
      successRate: '94%',
      productsFound: 1247
    },
    {
      id: '2',
      name: 'Market Trend Analyzer',
      description: 'AI-powered trend analysis for product demand prediction',
      status: 'running',
      lastRun: 'Running now',
      successRate: '88%',
      productsFound: 892
    },
    {
      id: '3',
      name: 'Competition Monitor',
      description: 'Track competitor pricing and market positioning',
      status: 'completed',
      lastRun: '30 minutes ago',
      successRate: '91%',
      productsFound: 523
    }
  ]);

  useEffect(() => {
    // Load any existing pending approvals
    const mockPendingApprovals: ProductResult[] = [
      {
        asin: 'B08N5WRWNW',
        title: 'Smart Fitness Tracker with Heart Rate Monitor',
        price: 49.99,
        rating: 4.8,
        reviewCount: 2847,
        imageUrl: 'https://via.placeholder.com/400x400?text=Fitness+Tracker',
        category: 'Electronics',
        brand: 'FitTech',
        availability: 'In Stock',
        primeEligible: true,
        profitPotential: 'high',
        status: 'pending_approval',
        aiAnalysis: {
          demandScore: 89,
          competitionScore: 65,
          profitabilityScore: 92
        }
      }
    ];
    setPendingApprovals(mockPendingApprovals);
  }, []);

  const addKeyword = () => {
    if (keywordInput.trim() && !searchCriteria.keywords.includes(keywordInput.trim())) {
      setSearchCriteria(prev => ({
        ...prev,
        keywords: [...prev.keywords, keywordInput.trim()]
      }));
      setKeywordInput('');
    }
  };

  const removeKeyword = (keyword: string) => {
    setSearchCriteria(prev => ({
      ...prev,
      keywords: prev.keywords.filter(k => k !== keyword)
    }));
  };

  const addExcludeBrand = () => {
    if (excludeBrandInput.trim() && !searchCriteria.excludeBrands.includes(excludeBrandInput.trim())) {
      setSearchCriteria(prev => ({
        ...prev,
        excludeBrands: [...prev.excludeBrands, excludeBrandInput.trim()]
      }));
      setExcludeBrandInput('');
    }
  };

  const removeExcludeBrand = (brand: string) => {
    setSearchCriteria(prev => ({
      ...prev,
      excludeBrands: prev.excludeBrands.filter(b => b !== brand)
    }));
  };

  const initiateSearch = async () => {
    if (searchCriteria.keywords.length === 0) {
      alert('Please add at least one keyword');
      return;
    }

    setIsSearching(true);
    
    try {
      // Mock API call - replace with actual CoreLDove sourcing API
      const newSearchTask: SearchTask = {
        searchTaskId: `search_${Date.now()}`,
        status: 'pending',
        estimatedCompletion: new Date(Date.now() + 5 * 60000).toISOString()
      };

      setSearchTasks(prev => [newSearchTask, ...prev]);
      setActiveSearch(newSearchTask);

      // Simulate search completion with AI analysis
      setTimeout(() => {
        const mockProducts: ProductResult[] = searchCriteria.keywords.map((keyword, index) => ({
          asin: `B${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
          title: `${keyword.charAt(0).toUpperCase() + keyword.slice(1)} - AI-Selected Premium Product ${index + 1}`,
          price: Math.round((20 + Math.random() * 100) * 100) / 100,
          rating: Math.round((3.5 + Math.random() * 1.5) * 10) / 10,
          reviewCount: Math.floor(100 + Math.random() * 2000),
          imageUrl: `https://via.placeholder.com/400x400?text=${encodeURIComponent(keyword)}`,
          category: searchCriteria.category === 'all' ? 'Electronics' : searchCriteria.category,
          brand: `Brand${index + 1}`,
          availability: 'In Stock',
          primeEligible: Math.random() > 0.3,
          profitPotential: ['high', 'medium', 'low'][Math.floor(Math.random() * 3)],
          aiAnalysis: {
            demandScore: Math.floor(60 + Math.random() * 40),
            competitionScore: Math.floor(30 + Math.random() * 70),
            profitabilityScore: Math.floor(50 + Math.random() * 50)
          }
        }));

        const completedTask: SearchTask = {
          ...newSearchTask,
          status: 'completed',
          products: mockProducts,
          totalFound: mockProducts.length,
          processingTime: '4.2 seconds'
        };

        setSearchTasks(prev => prev.map(task => 
          task.searchTaskId === newSearchTask.searchTaskId ? completedTask : task
        ));
        setActiveSearch(completedTask);
      }, 4000);

    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const toggleProductSelection = (asin: string) => {
    const newSelected = new Set(selectedProducts);
    if (newSelected.has(asin)) {
      newSelected.delete(asin);
    } else {
      newSelected.add(asin);
    }
    setSelectedProducts(newSelected);
  };

  const processSelectedProducts = async () => {
    if (selectedProducts.size === 0) {
      alert('Please select at least one product');
      return;
    }

    // Move selected products to approval workflow
    if (activeSearch?.products) {
      const selectedProductsData = activeSearch.products.filter(p => selectedProducts.has(p.asin));
      const updatedProducts = selectedProductsData.map(p => ({
        ...p,
        status: 'pending_approval' as const
      }));
      
      setPendingApprovals(prev => [...prev, ...updatedProducts]);
      setSelectedProducts(new Set());
      alert(`${selectedProducts.size} products sent for human approval`);
    }
  };

  const approveProduct = (asin: string, notes: string = '') => {
    setPendingApprovals(prev => prev.map(p => 
      p.asin === asin ? { ...p, status: 'approved' } : p
    ));
    // Here you would trigger the next stage: keyword research
    alert(`Product ${asin} approved! Initiating keyword research...`);
  };

  const rejectProduct = (asin: string, reason: string = '') => {
    setPendingApprovals(prev => prev.map(p => 
      p.asin === asin ? { ...p, status: 'rejected' } : p
    ));
    alert(`Product ${asin} rejected: ${reason}`);
  };

  const getProfitColor = (potential: string) => {
    switch (potential) {
      case 'high': return 'bg-green-100 text-green-800 border-green-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getCompetitionColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'high': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const renderApprovalInterface = () => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Users className="w-5 h-5" />
          Human Approval Workflow
          <Badge className="ml-2">{pendingApprovals.filter(p => p.status === 'pending_approval').length} pending</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {pendingApprovals.filter(p => p.status === 'pending_approval').length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <CheckCircle className="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p>No products pending approval</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {pendingApprovals.filter(p => p.status === 'pending_approval').map((product) => (
              <Card key={product.asin} className="border-orange-200">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold text-sm mb-2">{product.title}</h3>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>ASIN: {product.asin}</span>
                        <span>•</span>
                        <span>{product.brand}</span>
                      </div>
                    </div>
                    <Badge className={getProfitColor(product.profitPotential)}>
                      {product.profitPotential} profit
                    </Badge>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Price:</span>
                      <span className="ml-2 font-medium">${product.price}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Rating:</span>
                      <span className="ml-2 font-medium flex items-center gap-1">
                        <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                        {product.rating}
                      </span>
                    </div>
                  </div>

                  {product.aiAnalysis && (
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium flex items-center gap-1">
                        <Brain className="w-4 h-4 text-purple-500" />
                        AI Analysis
                      </h4>
                      <div className="grid grid-cols-3 gap-2 text-xs">
                        <div>
                          <div className="text-gray-500">Demand</div>
                          <div className="font-medium text-blue-600">{product.aiAnalysis.demandScore}%</div>
                        </div>
                        <div>
                          <div className="text-gray-500">Competition</div>
                          <div className="font-medium text-yellow-600">{product.aiAnalysis.competitionScore}%</div>
                        </div>
                        <div>
                          <div className="text-gray-500">Profit</div>
                          <div className="font-medium text-green-600">{product.aiAnalysis.profitabilityScore}%</div>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="space-y-2">
                    <label className="text-sm font-medium">Approval Notes:</label>
                    <Textarea 
                      placeholder="Add notes for this product..."
                      className="text-sm"
                      rows={2}
                    />
                  </div>

                  <div className="flex gap-2">
                    <Button 
                      size="sm" 
                      className="flex-1 bg-green-600 hover:bg-green-700"
                      onClick={() => approveProduct(product.asin)}
                    >
                      <CheckCircle className="w-3 h-3 mr-1" />
                      Approve
                    </Button>
                    <Button 
                      size="sm" 
                      variant="destructive" 
                      className="flex-1"
                      onClick={() => rejectProduct(product.asin, 'Manual review')}
                    >
                      <AlertCircle className="w-3 h-3 mr-1" />
                      Reject
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">CoreLDove Product Sourcing</h1>
              <p className="text-gray-600 mt-1">
                AI-powered Amazon product discovery with human-in-the-loop approval
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button 
                variant={approvalMode ? "default" : "outline"}
                onClick={() => setApprovalMode(!approvalMode)}
              >
                <Users className="w-4 h-4 mr-2" />
                Approval Mode
                {pendingApprovals.filter(p => p.status === 'pending_approval').length > 0 && (
                  <Badge className="ml-2 bg-red-100 text-red-800">
                    {pendingApprovals.filter(p => p.status === 'pending_approval').length}
                  </Badge>
                )}
              </Button>
              <Button asChild variant="outline">
                <Link href="/coreldove/products">
                  <Package className="w-4 h-4 mr-2" />
                  View Catalog
                </Link>
              </Button>
              <Button asChild className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                <Link href="/coreldove/analytics">
                  <BarChart3 className="w-4 h-4 mr-2" />
                  Analytics
                </Link>
              </Button>
            </div>
          </div>

          {/* Market Opportunities */}
          <div className="grid md:grid-cols-3 gap-4">
            {featuredOpportunities.map((opportunity, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow border-orange-200">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-gray-900">{opportunity.category}</h3>
                    <div className="flex items-center gap-1">
                      {opportunity.trending === 'up' ? (
                        <TrendingUp className="w-4 h-4 text-green-600" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-gray-400" />
                      )}
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Avg Profit:</span>
                      <span className="font-bold text-green-600">{opportunity.avgProfitMargin}%</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Demand Score:</span>
                      <span className="font-medium">{opportunity.demandScore}/100</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-500">Competition:</span>
                      <span className={`font-medium ${getCompetitionColor(opportunity.competitionLevel)}`}>
                        {opportunity.competitionLevel}
                      </span>
                    </div>
                    <div className="text-xs text-gray-500 mt-2">
                      {opportunity.productCount} opportunities found
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Approval Interface */}
        {approvalMode && renderApprovalInterface()}

        {/* Automation Workflows */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="w-5 h-5 text-purple-500" />
              Automation Workflows
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4 mb-6">
              {automationWorkflows.map((workflow) => (
                <div key={workflow.id} className="p-4 border rounded-lg hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      {workflow.status === 'running' ? (
                        <RefreshCw className="w-4 h-4 animate-spin text-blue-500" />
                      ) : workflow.status === 'completed' ? (
                        <CheckCircle className="w-4 h-4 text-green-500" />
                      ) : (
                        <Bot className="w-4 h-4 text-gray-500" />
                      )}
                      <span className="font-medium text-sm">{workflow.name}</span>
                    </div>
                    <Badge 
                      className={
                        workflow.status === 'running' ? 'bg-blue-100 text-blue-800' :
                        workflow.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }
                      variant="outline"
                    >
                      {workflow.status.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <p className="text-xs text-gray-600 mb-2">{workflow.description}</p>
                  
                  <div className="space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Last run:</span>
                      <span>{workflow.lastRun}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Success rate:</span>
                      <span className="text-green-600">{workflow.successRate}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Products found:</span>
                      <span className="font-medium">{workflow.productsFound.toLocaleString()}</span>
                    </div>
                  </div>

                  <Button 
                    size="sm" 
                    className="w-full mt-3" 
                    disabled={workflow.status === 'running'}
                  >
                    {workflow.status === 'running' ? (
                      <>
                        <Loader2 className="w-3 h-3 mr-1 animate-spin" />
                        Running...
                      </>
                    ) : (
                      <>
                        <Zap className="w-3 h-3 mr-1" />
                        Start Workflow
                      </>
                    )}
                  </Button>
                </div>
              ))}
            </div>

            <Alert>
              <Brain className="h-4 w-4" />
              <AlertTitle>AI-Powered Discovery</AlertTitle>
              <AlertDescription>
                Our AI continuously monitors Amazon for profitable products based on your criteria and market trends.
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>

        {!approvalMode && (
          <>
            {/* Search Configuration */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="w-5 h-5" />
                  Product Search Configuration
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="basic" className="space-y-6">
                  <TabsList>
                    <TabsTrigger value="basic">Basic Search</TabsTrigger>
                    <TabsTrigger value="advanced">Advanced Filters</TabsTrigger>
                    <TabsTrigger value="ai">AI Optimization</TabsTrigger>
                  </TabsList>

                  <TabsContent value="basic" className="space-y-6">
                    {/* Keywords */}
                    <div className="space-y-3">
                      <label className="text-sm font-medium">Search Keywords *</label>
                      <div className="flex gap-2">
                        <Input
                          placeholder="Enter product keywords..."
                          value={keywordInput}
                          onChange={(e) => setKeywordInput(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && addKeyword()}
                          className="flex-1"
                        />
                        <Button onClick={addKeyword} disabled={!keywordInput.trim()}>
                          <Plus className="w-4 h-4" />
                        </Button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {searchCriteria.keywords.map((keyword) => (
                          <Badge key={keyword} variant="secondary" className="cursor-pointer" onClick={() => removeKeyword(keyword)}>
                            {keyword} ×
                          </Badge>
                        ))}
                      </div>
                    </div>

                    {/* Basic Filters */}
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Category</label>
                        <Select value={searchCriteria.category} onValueChange={(value) => setSearchCriteria(prev => ({ ...prev, category: value }))}>
                          <SelectTrigger>
                            <SelectValue placeholder="Select category" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="all">All Categories</SelectItem>
                            <SelectItem value="electronics">Electronics</SelectItem>
                            <SelectItem value="home-garden">Home & Garden</SelectItem>
                            <SelectItem value="sports-outdoors">Sports & Outdoors</SelectItem>
                            <SelectItem value="health-beauty">Health & Beauty</SelectItem>
                            <SelectItem value="toys-games">Toys & Games</SelectItem>
                            <SelectItem value="fashion">Fashion</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Max Results</label>
                        <Select value={searchCriteria.maxResults.toString()} onValueChange={(value) => setSearchCriteria(prev => ({ ...prev, maxResults: parseInt(value) }))}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="25">25 products</SelectItem>
                            <SelectItem value="50">50 products</SelectItem>
                            <SelectItem value="100">100 products</SelectItem>
                            <SelectItem value="200">200 products</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="advanced" className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Min Price ($)</label>
                        <Input
                          type="number"
                          value={searchCriteria.minPrice}
                          onChange={(e) => setSearchCriteria(prev => ({ ...prev, minPrice: parseFloat(e.target.value) || 0 }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Max Price ($)</label>
                        <Input
                          type="number"
                          value={searchCriteria.maxPrice}
                          onChange={(e) => setSearchCriteria(prev => ({ ...prev, maxPrice: parseFloat(e.target.value) || 1000 }))}
                        />
                      </div>
                    </div>

                    <div className="space-y-3">
                      <label className="text-sm font-medium">Exclude Brands</label>
                      <div className="flex gap-2">
                        <Input
                          placeholder="Enter brand to exclude..."
                          value={excludeBrandInput}
                          onChange={(e) => setExcludeBrandInput(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && addExcludeBrand()}
                          className="flex-1"
                        />
                        <Button onClick={addExcludeBrand} disabled={!excludeBrandInput.trim()}>
                          <Plus className="w-4 h-4" />
                        </Button>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {searchCriteria.excludeBrands.map((brand) => (
                          <Badge key={brand} variant="outline" className="cursor-pointer" onClick={() => removeExcludeBrand(brand)}>
                            {brand} ×
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="ai" className="space-y-6">
                    <Alert>
                      <Brain className="h-4 w-4" />
                      <AlertTitle>AI-Powered Search Optimization</AlertTitle>
                      <AlertDescription>
                        Our AI will analyze market trends, competition, and profitability to optimize your search results automatically.
                      </AlertDescription>
                    </Alert>
                    
                    <div className="space-y-4">
                      <div className="flex items-center gap-3">
                        <input type="checkbox" id="trend-analysis" className="rounded" defaultChecked />
                        <label htmlFor="trend-analysis" className="text-sm">Enable trend analysis</label>
                      </div>
                      <div className="flex items-center gap-3">
                        <input type="checkbox" id="competition-scoring" className="rounded" defaultChecked />
                        <label htmlFor="competition-scoring" className="text-sm">Competition scoring</label>
                      </div>
                      <div className="flex items-center gap-3">
                        <input type="checkbox" id="demand-prediction" className="rounded" defaultChecked />
                        <label htmlFor="demand-prediction" className="text-sm">Demand prediction</label>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>

                <div className="flex justify-between items-center pt-6 border-t">
                  <div className="text-sm text-gray-500">
                    {searchCriteria.keywords.length} keywords configured
                  </div>
                  <Button 
                    onClick={initiateSearch} 
                    disabled={isSearching || searchCriteria.keywords.length === 0}
                    className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600"
                  >
                    {isSearching ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Searching...
                      </>
                    ) : (
                      <>
                        <Search className="w-4 h-4 mr-2" />
                        Start Search
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Search Results */}
            {activeSearch && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <Target className="w-5 h-5" />
                      Search Results
                    </CardTitle>
                    <div className="flex items-center gap-3">
                      {activeSearch.status === 'pending' && (
                        <Badge variant="secondary" className="flex items-center gap-1">
                          <Loader2 className="w-3 h-3 animate-spin" />
                          Processing
                        </Badge>
                      )}
                      {activeSearch.status === 'completed' && (
                        <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                          <CheckCircle className="w-3 h-3" />
                          Completed
                        </Badge>
                      )}
                      {selectedProducts.size > 0 && (
                        <Button onClick={processSelectedProducts} size="sm" className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600">
                          Send for Approval ({selectedProducts.size})
                        </Button>
                      )}
                    </div>
                  </div>
                  {activeSearch.status === 'completed' && (
                    <p className="text-sm text-gray-600">
                      Found {activeSearch.totalFound} products in {activeSearch.processingTime}
                    </p>
                  )}
                </CardHeader>

                <CardContent>
                  {activeSearch.status === 'pending' && (
                    <div className="space-y-4">
                      <div className="text-center py-8">
                        <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-orange-500" />
                        <p className="text-lg font-medium">Searching Amazon with AI analysis...</p>
                        <p className="text-sm text-gray-500">Analyzing profitability and market demand</p>
                      </div>
                      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {[...Array(6)].map((_, i) => (
                          <Card key={i} className="p-4 space-y-3">
                            <Skeleton className="aspect-square w-full" />
                            <Skeleton className="h-4 w-3/4" />
                            <Skeleton className="h-4 w-1/2" />
                            <Skeleton className="h-8 w-full" />
                          </Card>
                        ))}
                      </div>
                    </div>
                  )}

                  {activeSearch.status === 'completed' && activeSearch.products && (
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {activeSearch.products.map((product) => (
                        <Card 
                          key={product.asin} 
                          className={`hover:shadow-xl transition-all duration-300 cursor-pointer ${
                            selectedProducts.has(product.asin) ? 'ring-2 ring-orange-500 bg-orange-50' : 'border-orange-200'
                          }`}
                          onClick={() => toggleProductSelection(product.asin)}
                        >
                          <CardHeader className="p-4">
                            <div className="aspect-square bg-gray-100 rounded-lg mb-3 relative overflow-hidden">
                              <img 
                                src={product.imageUrl} 
                                alt={product.title}
                                className="w-full h-full object-cover"
                              />
                              <div className="absolute top-2 right-2">
                                <Badge className={getProfitColor(product.profitPotential)}>
                                  {product.profitPotential} profit
                                </Badge>
                              </div>
                              {product.primeEligible && (
                                <div className="absolute bottom-2 left-2">
                                  <Badge className="bg-blue-100 text-blue-800 text-xs">Prime</Badge>
                                </div>
                              )}
                            </div>
                            
                            <div className="space-y-2">
                              <h3 className="font-semibold text-sm line-clamp-2 min-h-[2.5rem]">
                                {product.title}
                              </h3>
                              <div className="flex items-center gap-2">
                                <div className="flex items-center gap-1">
                                  <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                                  <span className="text-xs font-medium">{product.rating}</span>
                                </div>
                                <span className="text-xs text-gray-500">({product.reviewCount.toLocaleString()})</span>
                                <Badge variant="outline" className="text-xs">{product.brand}</Badge>
                              </div>
                            </div>
                          </CardHeader>

                          <CardContent className="p-4 pt-0">
                            <div className="space-y-3">
                              <div className="flex justify-between items-center">
                                <span className="text-lg font-bold text-orange-600">${product.price}</span>
                                <span className="text-xs text-gray-500">ASIN: {product.asin}</span>
                              </div>
                              
                              {product.aiAnalysis && (
                                <div className="space-y-2">
                                  <h4 className="text-xs font-medium flex items-center gap-1">
                                    <Brain className="w-3 h-3 text-purple-500" />
                                    AI Analysis
                                  </h4>
                                  <div className="grid grid-cols-3 gap-2 text-xs">
                                    <div>
                                      <div className="text-gray-500">Demand</div>
                                      <div className="font-medium text-blue-600">{product.aiAnalysis.demandScore}%</div>
                                    </div>
                                    <div>
                                      <div className="text-gray-500">Competition</div>
                                      <div className="font-medium text-yellow-600">{product.aiAnalysis.competitionScore}%</div>
                                    </div>
                                    <div>
                                      <div className="text-gray-500">Profit</div>
                                      <div className="font-medium text-green-600">{product.aiAnalysis.profitabilityScore}%</div>
                                    </div>
                                  </div>
                                </div>
                              )}

                              <div className="flex items-center justify-between text-xs text-gray-500">
                                <span className="flex items-center gap-1">
                                  <Package className="w-3 h-3" />
                                  {product.availability}
                                </span>
                                <span>{product.category}</span>
                              </div>
                            </div>
                          </CardContent>

                          <CardFooter className="p-4 pt-0">
                            <Button 
                              className={`w-full ${
                                selectedProducts.has(product.asin)
                                  ? 'bg-orange-600 hover:bg-orange-700' 
                                  : 'bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600'
                              }`}
                              onClick={(e) => {
                                e.stopPropagation();
                                toggleProductSelection(product.asin);
                              }}
                            >
                              {selectedProducts.has(product.asin) ? (
                                <>
                                  <CheckCircle className="w-4 h-4 mr-2" />
                                  Selected
                                </>
                              ) : (
                                <>
                                  <Plus className="w-4 h-4 mr-2" />
                                  Select Product
                                </>
                              )}
                            </Button>
                          </CardFooter>
                        </Card>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
}