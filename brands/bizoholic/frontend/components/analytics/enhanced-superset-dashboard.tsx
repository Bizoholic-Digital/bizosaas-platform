'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Users, 
  DollarSign,
  Target,
  Globe,
  Database,
  RefreshCw,
  Download,
  Upload,
  Share,
  Settings,
  Eye,
  EyeOff,
  Plus,
  Trash2,
  Edit,
  Filter,
  Search,
  Calendar,
  Clock,
  AlertCircle,
  CheckCircle,
  Maximize,
  Minimize,
  Play,
  Pause,
  RotateCcw,
  ExternalLink,
  Layers,
  PieChart,
  LineChart,
  AreaChart,
  ScatterChart,
  Map,
  Table,
  Grid3X3,
  Layout,
  Code,
  Monitor,
  Smartphone,
  Tablet
} from 'lucide-react'

// Dashboard types
interface SupersetDashboard {
  id: string
  name: string
  description: string
  category: 'marketing' | 'sales' | 'operations' | 'financial' | 'custom'
  isPublic: boolean
  lastModified: Date
  owner: string
  charts: SupersetChart[]
  filters: DashboardFilter[]
  layout: DashboardLayout
  refreshInterval: number
  status: 'active' | 'draft' | 'archived'
}

interface SupersetChart {
  id: string
  name: string
  type: 'bar' | 'line' | 'pie' | 'area' | 'scatter' | 'table' | 'metric' | 'map'
  datasource: string
  query: string
  position: { x: number; y: number; w: number; h: number }
  config: Record<string, any>
  lastRefresh: Date
  status: 'loading' | 'success' | 'error'
}

interface DashboardFilter {
  id: string
  name: string
  type: 'date' | 'select' | 'multiselect' | 'range'
  column: string
  defaultValue: any
  options?: any[]
}

interface DashboardLayout {
  columns: number
  rows: number
  responsive: boolean
}

// Mock data
const MOCK_DASHBOARDS: SupersetDashboard[] = [
  {
    id: 'dash-1',
    name: 'Marketing Performance Overview',
    description: 'Comprehensive marketing metrics and campaign performance',
    category: 'marketing',
    isPublic: true,
    lastModified: new Date(),
    owner: 'Marketing Team',
    refreshInterval: 300, // 5 minutes
    status: 'active',
    layout: { columns: 12, rows: 8, responsive: true },
    filters: [
      { id: 'f1', name: 'Date Range', type: 'date', column: 'date', defaultValue: '30d' },
      { id: 'f2', name: 'Campaign', type: 'multiselect', column: 'campaign_id', defaultValue: [] }
    ],
    charts: [
      {
        id: 'c1',
        name: 'Total Impressions',
        type: 'metric',
        datasource: 'marketing_metrics',
        query: 'SELECT SUM(impressions) FROM campaigns WHERE date >= NOW() - INTERVAL 30 DAY',
        position: { x: 0, y: 0, w: 3, h: 2 },
        config: { format: 'number', suffix: 'M' },
        lastRefresh: new Date(),
        status: 'success'
      },
      {
        id: 'c2',
        name: 'Campaign Performance',
        type: 'bar',
        datasource: 'marketing_metrics',
        query: 'SELECT campaign_name, SUM(conversions) FROM campaigns GROUP BY campaign_name',
        position: { x: 3, y: 0, w: 6, h: 4 },
        config: { xAxis: 'campaign_name', yAxis: 'conversions' },
        lastRefresh: new Date(),
        status: 'success'
      },
      {
        id: 'c3',
        name: 'Conversion Trend',
        type: 'line',
        datasource: 'marketing_metrics',
        query: 'SELECT DATE(date), SUM(conversions) FROM campaigns GROUP BY DATE(date)',
        position: { x: 9, y: 0, w: 3, h: 4 },
        config: { xAxis: 'date', yAxis: 'conversions' },
        lastRefresh: new Date(),
        status: 'success'
      }
    ]
  },
  {
    id: 'dash-2',
    name: 'AI Agent Performance Analytics',
    description: 'Real-time monitoring of AI agent performance and task completion',
    category: 'operations',
    isPublic: false,
    lastModified: new Date(),
    owner: 'Operations Team',
    refreshInterval: 60, // 1 minute
    status: 'active',
    layout: { columns: 12, rows: 6, responsive: true },
    filters: [
      { id: 'f3', name: 'Agent Pattern', type: 'select', column: 'pattern', defaultValue: 'all' },
      { id: 'f4', name: 'Time Range', type: 'select', column: 'time_range', defaultValue: '1h' }
    ],
    charts: [
      {
        id: 'c4',
        name: 'Active Agents',
        type: 'metric',
        datasource: 'agent_metrics',
        query: 'SELECT COUNT(*) FROM agents WHERE status = "active"',
        position: { x: 0, y: 0, w: 2, h: 2 },
        config: { format: 'number' },
        lastRefresh: new Date(),
        status: 'success'
      },
      {
        id: 'c5',
        name: 'Agent Performance Distribution',
        type: 'pie',
        datasource: 'agent_metrics',
        query: 'SELECT status, COUNT(*) FROM agents GROUP BY status',
        position: { x: 2, y: 0, w: 4, h: 4 },
        config: {},
        lastRefresh: new Date(),
        status: 'success'
      }
    ]
  }
]

const CHART_TYPES = [
  { id: 'metric', name: 'Metric', icon: Target, description: 'Single value display' },
  { id: 'bar', name: 'Bar Chart', icon: BarChart3, description: 'Compare categories' },
  { id: 'line', name: 'Line Chart', icon: LineChart, description: 'Show trends over time' },
  { id: 'pie', name: 'Pie Chart', icon: PieChart, description: 'Show proportions' },
  { id: 'area', name: 'Area Chart', icon: AreaChart, description: 'Filled line chart' },
  { id: 'scatter', name: 'Scatter Plot', icon: ScatterChart, description: 'Show correlations' },
  { id: 'table', name: 'Table', icon: Table, description: 'Tabular data' },
  { id: 'map', name: 'Map', icon: Map, description: 'Geographic data' }
]

const DATASOURCES = [
  { id: 'marketing_metrics', name: 'Marketing Metrics', tables: 15 },
  { id: 'sales_data', name: 'Sales Data', tables: 12 },
  { id: 'agent_metrics', name: 'AI Agent Metrics', tables: 8 },
  { id: 'customer_data', name: 'Customer Data', tables: 20 },
  { id: 'financial_data', name: 'Financial Data', tables: 10 },
  { id: 'operational_metrics', name: 'Operational Metrics', tables: 18 }
]

export default function EnhancedSupersetDashboard() {
  const [dashboards, setDashboards] = useState<SupersetDashboard[]>(MOCK_DASHBOARDS)
  const [selectedDashboard, setSelectedDashboard] = useState<SupersetDashboard | null>(null)
  const [isCreating, setIsCreating] = useState(false)
  const [editingChart, setEditingChart] = useState<SupersetChart | null>(null)
  const [viewMode, setViewMode] = useState<'desktop' | 'tablet' | 'mobile'>('desktop')
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  
  const iframeRef = useRef<HTMLIFrameElement>(null)

  // Filter dashboards
  const filteredDashboards = dashboards.filter(dashboard => {
    const matchesSearch = dashboard.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         dashboard.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || dashboard.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  // Auto refresh simulation
  useEffect(() => {
    if (!autoRefresh || !selectedDashboard) return

    const interval = setInterval(() => {
      // Simulate chart refresh
      setSelectedDashboard(prev => {
        if (!prev) return null
        return {
          ...prev,
          charts: prev.charts.map(chart => ({
            ...chart,
            lastRefresh: new Date(),
            status: Math.random() > 0.1 ? 'success' : 'error' as const
          }))
        }
      })
    }, selectedDashboard.refreshInterval * 1000)

    return () => clearInterval(interval)
  }, [autoRefresh, selectedDashboard])

  // Create new dashboard
  const handleCreateDashboard = () => {
    const newDashboard: SupersetDashboard = {
      id: `dash-${Date.now()}`,
      name: 'New Dashboard',
      description: 'Custom dashboard created with enhanced builder',
      category: 'custom',
      isPublic: false,
      lastModified: new Date(),
      owner: 'Current User',
      refreshInterval: 300,
      status: 'draft',
      layout: { columns: 12, rows: 8, responsive: true },
      filters: [],
      charts: []
    }
    
    setDashboards(prev => [...prev, newDashboard])
    setSelectedDashboard(newDashboard)
    setIsCreating(true)
  }

  // Add chart to dashboard
  const handleAddChart = (type: string) => {
    if (!selectedDashboard) return

    const newChart: SupersetChart = {
      id: `chart-${Date.now()}`,
      name: `New ${type} Chart`,
      type: type as any,
      datasource: 'marketing_metrics',
      query: 'SELECT * FROM example_table LIMIT 100',
      position: { x: 0, y: 0, w: 4, h: 4 },
      config: {},
      lastRefresh: new Date(),
      status: 'loading'
    }

    setSelectedDashboard(prev => prev ? {
      ...prev,
      charts: [...prev.charts, newChart]
    } : null)
    
    setEditingChart(newChart)
  }

  // Chart component for dashboard layout
  const ChartComponent = ({ chart }: { chart: SupersetChart }) => {
    const ChartIcon = CHART_TYPES.find(t => t.id === chart.type)?.icon || BarChart3
    
    return (
      <Card 
        className="h-full cursor-pointer hover:shadow-lg transition-shadow"
        onClick={() => setEditingChart(chart)}
      >
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <ChartIcon className="w-4 h-4" />
              <CardTitle className="text-sm">{chart.name}</CardTitle>
            </div>
            <div className="flex items-center space-x-1">
              <Badge variant={chart.status === 'success' ? 'default' : chart.status === 'error' ? 'destructive' : 'secondary'}>
                {chart.status}
              </Badge>
              <Button variant="ghost" size="sm" onClick={(e) => {
                e.stopPropagation()
                setEditingChart(chart)
              }}>
                <Edit className="w-3 h-3" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="h-32 bg-muted rounded flex items-center justify-center">
            {chart.status === 'loading' ? (
              <div className="animate-spin">
                <RefreshCw className="w-6 h-6" />
              </div>
            ) : chart.status === 'error' ? (
              <div className="text-red-500 text-center">
                <AlertCircle className="w-6 h-6 mx-auto mb-1" />
                <div className="text-xs">Chart Error</div>
              </div>
            ) : (
              <div className="text-center">
                <ChartIcon className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
                <div className="text-xs text-muted-foreground">
                  {chart.type} visualization
                </div>
              </div>
            )}
          </div>
          <div className="mt-2 text-xs text-muted-foreground">
            Last updated: {chart.lastRefresh.toLocaleTimeString()}
          </div>
        </CardContent>
      </Card>
    )
  }

  // Dashboard layout grid
  const DashboardGrid = ({ dashboard }: { dashboard: SupersetDashboard }) => {
    const gridCols = viewMode === 'mobile' ? 1 : viewMode === 'tablet' ? 2 : 3
    
    return (
      <div className={`grid gap-4 grid-cols-${gridCols}`}>
        {dashboard.charts.map(chart => (
          <div key={chart.id} className="min-h-48">
            <ChartComponent chart={chart} />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Enhanced Apache Superset Integration</h2>
          <p className="text-muted-foreground">
            Advanced analytics dashboard with embedded Superset charts and custom visualizations
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Switch checked={autoRefresh} onCheckedChange={setAutoRefresh} />
            <span className="text-sm">Auto Refresh</span>
          </div>
          <Button onClick={handleCreateDashboard}>
            <Plus className="w-4 h-4 mr-2" />
            New Dashboard
          </Button>
        </div>
      </div>

      <Tabs defaultValue="dashboards" className="space-y-6">
        <TabsList>
          <TabsTrigger value="dashboards">Dashboards</TabsTrigger>
          <TabsTrigger value="builder">Dashboard Builder</TabsTrigger>
          <TabsTrigger value="embedded">Embedded Superset</TabsTrigger>
          <TabsTrigger value="datasources">Data Sources</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        {/* Dashboards Tab */}
        <TabsContent value="dashboards" className="space-y-6">
          {/* Filters */}
          <div className="flex items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="flex items-center space-x-2">
              <Search className="w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search dashboards..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-64"
              />
            </div>
            
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="marketing">Marketing</SelectItem>
                <SelectItem value="sales">Sales</SelectItem>
                <SelectItem value="operations">Operations</SelectItem>
                <SelectItem value="financial">Financial</SelectItem>
                <SelectItem value="custom">Custom</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex items-center space-x-2 ml-auto">
              <span className="text-sm text-muted-foreground">
                {filteredDashboards.length} dashboards
              </span>
            </div>
          </div>

          {/* Dashboard List */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredDashboards.map(dashboard => (
              <Card key={dashboard.id} className="cursor-pointer hover:shadow-lg transition-shadow"
                    onClick={() => setSelectedDashboard(dashboard)}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{dashboard.name}</CardTitle>
                    <div className="flex space-x-1">
                      <Badge variant={dashboard.status === 'active' ? 'default' : dashboard.status === 'draft' ? 'secondary' : 'outline'}>
                        {dashboard.status}
                      </Badge>
                      {dashboard.isPublic && (
                        <Badge variant="outline">
                          <Globe className="w-3 h-3 mr-1" />
                          Public
                        </Badge>
                      )}
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {dashboard.description}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span>Charts: {dashboard.charts.length}</span>
                      <span>Category: {dashboard.category}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm text-muted-foreground">
                      <span>Owner: {dashboard.owner}</span>
                      <span>Modified: {dashboard.lastModified.toLocaleDateString()}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Refresh: {dashboard.refreshInterval}s</span>
                      <div className="flex space-x-1">
                        <Button size="sm" variant="outline">
                          <Eye className="w-3 h-3" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Edit className="w-3 h-3" />
                        </Button>
                        <Button size="sm" variant="outline">
                          <Share className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Dashboard Builder Tab */}
        <TabsContent value="builder" className="space-y-6">
          {selectedDashboard ? (
            <div className="space-y-6">
              {/* Dashboard Controls */}
              <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
                <div className="flex items-center space-x-4">
                  <div>
                    <h3 className="font-semibold">{selectedDashboard.name}</h3>
                    <p className="text-sm text-muted-foreground">{selectedDashboard.description}</p>
                  </div>
                  <Badge variant={selectedDashboard.status === 'active' ? 'default' : 'secondary'}>
                    {selectedDashboard.status}
                  </Badge>
                </div>
                
                <div className="flex items-center space-x-2">
                  {/* View Mode Toggle */}
                  <div className="flex items-center space-x-1 border rounded">
                    <Button
                      variant={viewMode === 'desktop' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setViewMode('desktop')}
                    >
                      <Monitor className="w-4 h-4" />
                    </Button>
                    <Button
                      variant={viewMode === 'tablet' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setViewMode('tablet')}
                    >
                      <Tablet className="w-4 h-4" />
                    </Button>
                    <Button
                      variant={viewMode === 'mobile' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setViewMode('mobile')}
                    >
                      <Smartphone className="w-4 h-4" />
                    </Button>
                  </div>

                  <Button variant="outline" size="sm" onClick={() => setIsFullscreen(!isFullscreen)}>
                    {isFullscreen ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
                  </Button>
                  
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-2" />
                    Export
                  </Button>
                  
                  <Button size="sm">
                    <Play className="w-4 h-4 mr-2" />
                    Publish
                  </Button>
                </div>
              </div>

              {/* Chart Type Palette */}
              <div className="flex items-center space-x-2 p-4 border rounded-lg overflow-x-auto">
                <span className="text-sm font-medium whitespace-nowrap">Add Chart:</span>
                {CHART_TYPES.map(chartType => {
                  const Icon = chartType.icon
                  return (
                    <Button
                      key={chartType.id}
                      variant="outline"
                      size="sm"
                      onClick={() => handleAddChart(chartType.id)}
                      className="flex items-center space-x-2 whitespace-nowrap"
                    >
                      <Icon className="w-4 h-4" />
                      <span>{chartType.name}</span>
                    </Button>
                  )
                })}
              </div>

              {/* Dashboard Grid */}
              <div className={`border rounded-lg p-4 ${isFullscreen ? 'fixed inset-4 z-50 bg-white' : ''}`}>
                <DashboardGrid dashboard={selectedDashboard} />
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <Layout className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No Dashboard Selected</h3>
              <p className="text-muted-foreground mb-4">
                Select a dashboard to edit or create a new one
              </p>
              <Button onClick={handleCreateDashboard}>
                <Plus className="w-4 h-4 mr-2" />
                Create New Dashboard
              </Button>
            </div>
          )}
        </TabsContent>

        {/* Embedded Superset Tab */}
        <TabsContent value="embedded" className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold">Apache Superset Integration</h3>
              <p className="text-sm text-muted-foreground">
                Direct access to Apache Superset dashboards and charts
              </p>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline" size="sm">
                <ExternalLink className="w-4 h-4 mr-2" />
                Open Superset
              </Button>
              <Button variant="outline" size="sm">
                <RefreshCw className="w-4 h-4 mr-2" />
                Refresh
              </Button>
            </div>
          </div>

          {/* Embedded Superset iframe */}
          <div className="border rounded-lg overflow-hidden">
            <iframe
              ref={iframeRef}
              src="http://localhost:8088/dashboard/embedded/1" // Replace with actual Superset URL
              className="w-full h-96"
              title="Apache Superset Dashboard"
              onError={() => {
                // Fallback if Superset is not available
              }}
            />
          </div>

          {/* Quick Access Cards */}
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Marketing Dashboard</CardTitle>
              </CardHeader>
              <CardContent>
                <Button size="sm" className="w-full">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Open in Superset
                </Button>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Sales Analytics</CardTitle>
              </CardHeader>
              <CardContent>
                <Button size="sm" className="w-full">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Open in Superset
                </Button>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Operations Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <Button size="sm" className="w-full">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Open in Superset
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Data Sources Tab */}
        <TabsContent value="datasources" className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Data Sources</h3>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Add Data Source
            </Button>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {DATASOURCES.map(source => (
              <Card key={source.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{source.name}</CardTitle>
                    <Badge variant="outline">{source.tables} tables</Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Database className="w-4 h-4 text-muted-foreground" />
                      <span className="text-sm">PostgreSQL</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-green-600">Connected</span>
                    </div>
                    <div className="flex space-x-1 mt-3">
                      <Button size="sm" variant="outline" className="flex-1">
                        <Eye className="w-3 h-3 mr-1" />
                        Explore
                      </Button>
                      <Button size="sm" variant="outline" className="flex-1">
                        <Settings className="w-3 h-3 mr-1" />
                        Configure
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Settings Tab */}
        <TabsContent value="settings" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Apache Superset Connection</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="superset-url">Superset URL</Label>
                  <Input id="superset-url" defaultValue="http://localhost:8088" />
                </div>
                <div>
                  <Label htmlFor="superset-token">API Token</Label>
                  <Input id="superset-token" type="password" placeholder="Enter API token" />
                </div>
                <div className="flex items-center space-x-2">
                  <Switch defaultChecked />
                  <Label>Enable embedding</Label>
                </div>
                <Button>Test Connection</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Dashboard Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="default-refresh">Default Refresh Interval (seconds)</Label>
                  <Select defaultValue="300">
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="60">1 minute</SelectItem>
                      <SelectItem value="300">5 minutes</SelectItem>
                      <SelectItem value="900">15 minutes</SelectItem>
                      <SelectItem value="3600">1 hour</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex items-center space-x-2">
                  <Switch defaultChecked />
                  <Label>Auto-refresh on dashboard load</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Switch />
                  <Label>Enable real-time updates</Label>
                </div>
                <Button>Save Settings</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Chart Editor Modal */}
      {editingChart && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
             onClick={() => setEditingChart(null)}>
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full m-4 max-h-[80vh] overflow-y-auto" 
               onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Edit Chart: {editingChart.name}</h3>
              <Button variant="ghost" size="sm" onClick={() => setEditingChart(null)}>×</Button>
            </div>
            
            <div className="space-y-4">
              <div>
                <Label htmlFor="chart-name">Chart Name</Label>
                <Input
                  id="chart-name"
                  value={editingChart.name}
                  onChange={(e) => setEditingChart(prev => prev ? { ...prev, name: e.target.value } : null)}
                />
              </div>
              
              <div>
                <Label htmlFor="chart-type">Chart Type</Label>
                <Select value={editingChart.type} onValueChange={(value) => 
                  setEditingChart(prev => prev ? { ...prev, type: value as any } : null)
                }>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CHART_TYPES.map(type => (
                      <SelectItem key={type.id} value={type.id}>{type.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="chart-datasource">Data Source</Label>
                <Select value={editingChart.datasource} onValueChange={(value) => 
                  setEditingChart(prev => prev ? { ...prev, datasource: value } : null)
                }>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {DATASOURCES.map(source => (
                      <SelectItem key={source.id} value={source.id}>{source.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="chart-query">SQL Query</Label>
                <Textarea
                  id="chart-query"
                  value={editingChart.query}
                  onChange={(e) => setEditingChart(prev => prev ? { ...prev, query: e.target.value } : null)}
                  rows={6}
                  className="font-mono"
                />
              </div>
            </div>
            
            <div className="flex justify-between mt-6">
              <Button variant="destructive" onClick={() => {
                if (selectedDashboard) {
                  setSelectedDashboard({
                    ...selectedDashboard,
                    charts: selectedDashboard.charts.filter(c => c.id !== editingChart.id)
                  })
                }
                setEditingChart(null)
              }}>
                <Trash2 className="w-4 h-4 mr-2" />
                Delete Chart
              </Button>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={() => setEditingChart(null)}>
                  Cancel
                </Button>
                <Button onClick={() => {
                  if (selectedDashboard) {
                    setSelectedDashboard({
                      ...selectedDashboard,
                      charts: selectedDashboard.charts.map(c => 
                        c.id === editingChart.id ? editingChart : c
                      )
                    })
                  }
                  setEditingChart(null)
                }}>
                  Save Changes
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}