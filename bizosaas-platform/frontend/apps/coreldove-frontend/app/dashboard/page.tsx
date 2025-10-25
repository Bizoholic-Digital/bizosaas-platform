'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { formatTimeAgo, createTimestamp } from '../../lib/utils'
import { 
  BarChart3,
  Package,
  ShoppingCart,
  TrendingUp,
  Users,
  Eye,
  ExternalLink,
  Settings,
  Bell,
  Search,
  Filter,
  Plus,
  RefreshCw,
  Download,
  CheckCircle,
  Clock,
  AlertTriangle,
  ChevronDown,
  Database,
  LayoutDashboard,
  Megaphone,
  Building,
  MessageCircle
} from 'lucide-react'

interface DashboardStats {
  totalProducts: number
  pendingApproval: number
  monthlyRevenue: number
  totalOrders: number
  conversionRate: number
  avgOrderValue: number
}

interface ProductSuggestion {
  id: string
  name: string
  category: string
  profitMargin: number
  demandScore: number
  competitionLevel: 'Low' | 'Medium' | 'High'
  estimatedRevenue: number
  status: 'pending' | 'approved' | 'rejected'
  source: 'amazon' | 'ai-discovery'
  confidence: number
}

interface RecentActivity {
  id: string
  type: 'product_added' | 'order_received' | 'ai_suggestion' | 'approval_needed'
  title: string
  description: string
  timestamp: Date
  status?: 'success' | 'pending' | 'warning'
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    totalProducts: 0,
    pendingApproval: 0,
    monthlyRevenue: 0,
    totalOrders: 0,
    conversionRate: 0,
    avgOrderValue: 0
  })
  const [aiSuggestions, setAiSuggestions] = useState<ProductSuggestion[]>([])
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTimeRange, setSelectedTimeRange] = useState<'7d' | '30d' | '90d'>('30d')
  const [showAdminDropdown, setShowAdminDropdown] = useState(false)
  const [showPlatformsDropdown, setShowPlatformsDropdown] = useState(false)
  const [userRole, setUserRole] = useState('tenant_admin') // Will be fetched from auth

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement
      if (!target.closest('.relative')) {
        setShowAdminDropdown(false)
        setShowPlatformsDropdown(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    // Load user role from session
    const loadUserRole = async () => {
      try {
        const response = await fetch('/api/auth/session')
        if (response.ok) {
          const data = await response.json()
          if (data.authenticated) {
            setUserRole(data.role || 'tenant_admin')
          }
        }
      } catch (error) {
        console.error('Failed to load user role:', error)
      }
    }

    loadUserRole()
  }, [])

  useEffect(() => {
    // Simulate loading dashboard data
    const loadDashboardData = async () => {
      try {
        // In production, these would be actual API calls
        await new Promise(resolve => setTimeout(resolve, 1000))

        setStats({
          totalProducts: 247,
          pendingApproval: 12,
          monthlyRevenue: 15847.32,
          totalOrders: 168,
          conversionRate: 3.2,
          avgOrderValue: 94.33
        })

        setAiSuggestions([
          {
            id: 'ai-1',
            name: 'Smart Fitness Tracker Pro',
            category: 'Health & Fitness',
            profitMargin: 45.2,
            demandScore: 8.7,
            competitionLevel: 'Medium',
            estimatedRevenue: 2850,
            status: 'pending',
            source: 'ai-discovery',
            confidence: 0.89
          },
          {
            id: 'ai-2',
            name: 'Wireless Charging Stand',
            category: 'Tech Accessories',
            profitMargin: 38.5,
            demandScore: 7.9,
            competitionLevel: 'High',
            estimatedRevenue: 1920,
            status: 'pending',
            source: 'amazon',
            confidence: 0.76
          },
          {
            id: 'ai-3',
            name: 'Eco-Friendly Water Bottle',
            category: 'Lifestyle',
            profitMargin: 52.8,
            demandScore: 9.1,
            competitionLevel: 'Low',
            estimatedRevenue: 3240,
            status: 'approved',
            source: 'ai-discovery',
            confidence: 0.94
          }
        ])

        setRecentActivity([
          {
            id: 'act-1',
            type: 'ai_suggestion',
            title: 'New AI Product Suggestion',
            description: 'Smart Fitness Tracker Pro identified with 89% confidence',
            timestamp: createTimestamp(2),
            status: 'pending'
          },
          {
            id: 'act-2',
            type: 'order_received',
            title: 'New Order #1847',
            description: 'Premium Wireless Earbuds - $89.99',
            timestamp: createTimestamp(4),
            status: 'success'
          },
          {
            id: 'act-3',
            type: 'product_added',
            title: 'Product Published',
            description: 'Yoga Mat Pro added to catalog',
            timestamp: createTimestamp(6),
            status: 'success'
          },
          {
            id: 'act-4',
            type: 'approval_needed',
            title: 'Review Required',
            description: '3 products pending approval',
            timestamp: createTimestamp(8),
            status: 'warning'
          }
        ])

        setLoading(false)
      } catch (error) {
        console.error('Error loading dashboard:', error)
        setLoading(false)
      }
    }

    loadDashboardData()
  }, [selectedTimeRange])

  const handleApproveProduct = (productId: string) => {
    setAiSuggestions(prev => 
      prev.map(product => 
        product.id === productId 
          ? { ...product, status: 'approved' }
          : product
      )
    )
    console.log('Approved product:', productId)
  }

  const handleRejectProduct = (productId: string) => {
    setAiSuggestions(prev => 
      prev.map(product => 
        product.id === productId 
          ? { ...product, status: 'rejected' }
          : product
      )
    )
    console.log('Rejected product:', productId)
  }

  const getStatusIcon = (type: RecentActivity['type']) => {
    switch (type) {
      case 'ai_suggestion':
        return <TrendingUp className="w-4 h-4" />
      case 'order_received':
        return <ShoppingCart className="w-4 h-4" />
      case 'product_added':
        return <Package className="w-4 h-4" />
      case 'approval_needed':
        return <AlertTriangle className="w-4 h-4" />
    }
  }

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'success': return 'text-green-600'
      case 'pending': return 'text-blue-600'
      case 'warning': return 'text-yellow-600'
      default: return 'text-gray-600'
    }
  }

  // Platform navigation data based on user role
  const getPlatformTabs = () => {
    const adminPlatforms = []
    const businessPlatforms = []
    
    // Admin platforms (excluding current CoreLDove)
    if (userRole === 'super_admin' || userRole === 'tenant_admin') {
      adminPlatforms.push({
        id: 'tailadmin',
        name: 'BizOSaaS Admin',
        url: 'http://localhost:3001/',
        description: 'Business Operations Dashboard',
        icon: LayoutDashboard,
        status: 'active'
      })
    }

    if (userRole === 'super_admin') {
      adminPlatforms.push({
        id: 'sqladmin',
        name: 'SQL Admin',
        url: 'http://localhost:5000/',
        description: 'Infrastructure Management',
        icon: Database,
        status: 'active'
      })
    }

    // Business platforms
    if (userRole === 'super_admin' || userRole === 'tenant_admin' || userRole === 'manager') {
      businessPlatforms.push(
        {
          id: 'bizoholic',
          name: 'Bizoholic',
          url: 'http://localhost:3000',
          description: 'AI Marketing Agency Platform',
          icon: Megaphone,
          status: 'active',
          features: ['Marketing Campaigns', 'AI Agents', 'Analytics', 'CRM']
        },
        {
          id: 'directory',
          name: 'Directory',
          url: 'http://localhost:8003/directories',
          description: 'Business Directory Management',
          icon: Building,
          status: 'active',
          features: ['Business Listings', 'Directory Sync', 'Local SEO', 'Lead Gen']
        }
      )
    }

    return { adminPlatforms, businessPlatforms }
  }

  const handlePlatformNavigation = (url: string, isExternal: boolean = true) => {
    if (isExternal) {
      window.open(url, '_blank')
    } else {
      window.location.href = url
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-red-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <div className="flex items-center">
                <Image
                  src="/coreldove-simple-logo.png"
                  alt="CoreLDove"
                  width={120}
                  height={40}
                  className="h-8 w-auto mr-4"
                />
                <h1 className="text-xl font-bold text-gray-900">CoreLDove Dashboard</h1>
              </div>

              {/* Multi-Platform Navigation Tabs */}
              <div className="flex items-center space-x-2">
                {(() => {
                  const { adminPlatforms, businessPlatforms } = getPlatformTabs()
                  
                  return (
                    <>
                      {/* Admin Platforms Dropdown */}
                      {adminPlatforms.length > 0 && (
                        <div className="relative">
                          <button
                            onClick={() => {
                              setShowAdminDropdown(!showAdminDropdown)
                              setShowPlatformsDropdown(false)
                            }}
                            className="bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700 flex items-center space-x-1"
                          >
                            <span>Admin</span>
                            <ChevronDown className="w-4 h-4" />
                          </button>
                          
                          {showAdminDropdown && (
                            <div className="absolute right-0 mt-2 w-64 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
                              <div className="py-1">
                                <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200">
                                  Admin Dashboards
                                </div>
                                {adminPlatforms.map((platform) => {
                                  const IconComponent = platform.icon
                                  return (
                                    <button
                                      key={platform.id}
                                      onClick={() => handlePlatformNavigation(platform.url, false)}
                                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                                    >
                                      <div className="w-2 h-2 rounded-full bg-green-500"></div>
                                      <IconComponent className="w-4 h-4" />
                                      <div>
                                        <div className="font-medium">{platform.name}</div>
                                        <div className="text-xs text-gray-500">{platform.description}</div>
                                      </div>
                                    </button>
                                  )
                                })}
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Business Platforms Dropdown */}
                      {businessPlatforms.length > 0 && (
                        <div className="relative">
                          <button
                            onClick={() => {
                              setShowPlatformsDropdown(!showPlatformsDropdown)
                              setShowAdminDropdown(false)
                            }}
                            className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 flex items-center space-x-1"
                          >
                            <span>Platforms</span>
                            <ChevronDown className="w-4 h-4" />
                          </button>
                          
                          {showPlatformsDropdown && (
                            <div className="absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50">
                              <div className="py-1">
                                <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b border-gray-200">
                                  Business Platforms
                                </div>
                                {businessPlatforms.map((platform) => {
                                  const IconComponent = platform.icon
                                  return (
                                    <button
                                      key={platform.id}
                                      onClick={() => handlePlatformNavigation(platform.url, true)}
                                      className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                                    >
                                      <div className="w-2 h-2 rounded-full bg-green-500"></div>
                                      <IconComponent className="w-4 h-4" />
                                      <div className="flex-1">
                                        <div className="font-medium">{platform.name}</div>
                                        <div className="text-xs text-gray-500">{platform.description}</div>
                                        {platform.features && (
                                          <div className="text-xs text-blue-600 mt-1">
                                            {platform.features.slice(0, 2).join(', ')}
                                          </div>
                                        )}
                                      </div>
                                    </button>
                                  )
                                })}
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* AI Chat Service Direct Link */}
                      <button
                        onClick={() => handlePlatformNavigation('http://localhost:3003', true)}
                        className="bg-emerald-600 text-white px-3 py-1 rounded text-sm hover:bg-emerald-700 flex items-center space-x-1"
                      >
                        <MessageCircle className="w-4 h-4" />
                        <span>AI Assistant</span>
                      </button>
                    </>
                  )
                })()}
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Bell className="h-6 w-6" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <Settings className="h-6 w-6" />
              </button>
              <Link
                href="/"
                className="text-gray-600 hover:text-gray-900 font-medium"
              >
                View Store
              </Link>
              <button 
                onClick={() => window.location.href = '/auth/logout'}
                className="text-red-600 hover:text-red-800 font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome back! 👋</h2>
          <p className="text-gray-600">Your AI-powered e-commerce automation platform is working to find winning products.</p>
        </div>

        {/* Time Range Selector */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
            {(['7d', '30d', '90d'] as const).map((range) => (
              <button
                key={range}
                onClick={() => setSelectedTimeRange(range)}
                className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                  selectedTimeRange === range
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                {range === '7d' ? 'Last 7 days' : range === '30d' ? 'Last 30 days' : 'Last 3 months'}
              </button>
            ))}
          </div>
          
          <div className="flex items-center space-x-3">
            <button className="flex items-center gap-2 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button className="flex items-center gap-2 px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700">
              <RefreshCw className="w-4 h-4" />
              Sync Data
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <Package className="w-4 h-4 text-blue-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Total Products</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalProducts}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                <Clock className="w-4 h-4 text-yellow-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Pending Approval</p>
                <p className="text-2xl font-bold text-gray-900">{stats.pendingApproval}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <TrendingUp className="w-4 h-4 text-green-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
                <p className="text-2xl font-bold text-gray-900">${stats.monthlyRevenue.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <ShoppingCart className="w-4 h-4 text-purple-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Total Orders</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalOrders}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* AI Product Suggestions */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b border-gray-100">
                <div className="flex justify-between items-center">
                  <h3 className="text-lg font-semibold text-gray-900">AI Product Suggestions</h3>
                  <div className="flex items-center space-x-2">
                    <button className="p-2 text-gray-400 hover:text-gray-600">
                      <Filter className="w-4 h-4" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-600">
                      <Search className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="divide-y divide-gray-100">
                {aiSuggestions.map((suggestion) => (
                  <div key={suggestion.id} className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-1">{suggestion.name}</h4>
                        <p className="text-sm text-gray-600">{suggestion.category}</p>
                      </div>
                      <div className="flex items-center space-x-1">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          suggestion.status === 'approved' ? 'bg-green-100 text-green-800' :
                          suggestion.status === 'rejected' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {suggestion.status === 'approved' && <CheckCircle className="w-3 h-3 mr-1" />}
                          {suggestion.status === 'pending' && <Clock className="w-3 h-3 mr-1" />}
                          {suggestion.status.charAt(0).toUpperCase() + suggestion.status.slice(1)}
                        </span>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-4 gap-4 mb-4">
                      <div>
                        <p className="text-xs text-gray-500">Profit Margin</p>
                        <p className="font-semibold text-green-600">{suggestion.profitMargin}%</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Demand Score</p>
                        <p className="font-semibold text-blue-600">{suggestion.demandScore}/10</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Competition</p>
                        <p className={`font-semibold ${
                          suggestion.competitionLevel === 'Low' ? 'text-green-600' :
                          suggestion.competitionLevel === 'Medium' ? 'text-yellow-600' :
                          'text-red-600'
                        }`}>{suggestion.competitionLevel}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Est. Revenue</p>
                        <p className="font-semibold text-gray-900">${suggestion.estimatedRevenue}</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-sm text-gray-500">
                        <span className="mr-2">Confidence:</span>
                        <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${suggestion.confidence * 100}%` }}
                          ></div>
                        </div>
                        <span>{Math.round(suggestion.confidence * 100)}%</span>
                      </div>

                      {suggestion.status === 'pending' && (
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleRejectProduct(suggestion.id)}
                            className="px-3 py-1 text-xs border border-gray-300 rounded-md hover:bg-gray-50"
                          >
                            Reject
                          </button>
                          <button
                            onClick={() => handleApproveProduct(suggestion.id)}
                            className="px-3 py-1 text-xs bg-red-600 text-white rounded-md hover:bg-red-700"
                          >
                            Approve
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recent Activity & Quick Actions */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Link
                  href="http://localhost:9020"
                  target="_blank"
                  className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                    <ExternalLink className="w-4 h-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">Saleor Dashboard</p>
                    <p className="text-xs text-gray-500">Manage inventory & orders</p>
                  </div>
                </Link>

                <Link
                  href="/catalog"
                  className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <Eye className="w-4 h-4 text-green-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">View Storefront</p>
                    <p className="text-xs text-gray-500">See customer experience</p>
                  </div>
                </Link>

                <button className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors w-full">
                  <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Plus className="w-4 h-4 text-purple-600" />
                  </div>
                  <div className="text-left">
                    <p className="font-medium text-gray-900">Add Product</p>
                    <p className="text-xs text-gray-500">Manual product entry</p>
                  </div>
                </button>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start gap-3">
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center ${getStatusColor(activity.status)} bg-gray-50`}>
                      {getStatusIcon(activity.type)}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 text-sm">{activity.title}</p>
                      <p className="text-xs text-gray-500">{activity.description}</p>
                      <p className="text-xs text-gray-400 mt-1">{formatTimeAgo(activity.timestamp)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}