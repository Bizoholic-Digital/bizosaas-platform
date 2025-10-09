'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { 
  Database, 
  Users, 
  Settings, 
  Activity, 
  Clock, 
  BarChart3,
  TrendingUp,
  TrendingDown,
  Cpu,
  HardDrive,
  Network,
  Shield,
  Key,
  Globe,
  Building,
  Package,
  Layers,
  Workflow,
  Zap,
  AlertTriangle,
  CheckCircle,
  Info,
  Plus,
  Trash2,
  Edit,
  Eye,
  EyeOff,
  RefreshCw,
  Download,
  Upload,
  Search,
  Filter,
  Copy,
  ExternalLink,
  Play,
  Pause,
  Square,
  RotateCcw,
  Terminal,
  Code,
  GitBranch,
  Server,
  Cloud
} from 'lucide-react'

// Namespace types
interface Namespace {
  id: string
  name: string
  displayName: string
  description: string
  tenantId: string
  tenantName: string
  category: 'marketing' | 'sales' | 'support' | 'operations' | 'analytics' | 'custom'
  status: 'active' | 'inactive' | 'suspended' | 'maintenance'
  region: 'us-east-1' | 'us-west-2' | 'eu-west-1' | 'ap-southeast-1'
  environment: 'production' | 'staging' | 'development' | 'testing'
  workflowCount: number
  activeWorkflows: number
  totalExecutions: number
  executionsToday: number
  avgExecutionTime: number
  successRate: number
  errorCount: number
  resourceUsage: {
    cpu: number
    memory: number
    storage: number
    network: number
  }
  limits: {
    maxWorkflows: number
    maxExecutionsPerDay: number
    maxConcurrentExecutions: number
    storageLimit: number
  }
  metrics: {
    queueDepth: number
    tasksPerSecond: number
    latencyP99: number
    throughput: number
  }
  createdAt: Date
  lastActivity: Date
  owner: string
  tags: string[]
  isIsolated: boolean
  encryptionEnabled: boolean
}

interface TenantQuota {
  tenantId: string
  tenantName: string
  namespaces: number
  maxNamespaces: number
  totalWorkflows: number
  dailyExecutions: number
  storageUsed: number
  storageLimit: number
  isOverQuota: boolean
}

// Mock data generator
const generateMockNamespaces = (): Namespace[] => {
  const namespaces: Namespace[] = []
  const regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
  const environments = ['production', 'staging', 'development', 'testing']
  const categories = ['marketing', 'sales', 'support', 'operations', 'analytics', 'custom']
  const statuses = ['active', 'inactive', 'suspended', 'maintenance']
  
  // Generate tenant names
  const tenants = [
    'Acme Corp', 'TechStart Inc', 'Global Solutions', 'Innovation Labs',
    'Digital Dynamics', 'Future Systems', 'Smart Ventures', 'Cloud Connect',
    'Data Insights', 'AI Solutions', 'Business Pro', 'Enterprise Plus'
  ]

  for (let i = 1; i <= 1200; i++) {
    const tenantName = tenants[Math.floor(Math.random() * tenants.length)]
    const category = categories[Math.floor(Math.random() * categories.length)]
    const status = statuses[Math.floor(Math.random() * statuses.length)]
    const environment = environments[Math.floor(Math.random() * environments.length)]
    const region = regions[Math.floor(Math.random() * regions.length)]
    
    const workflowCount = Math.floor(Math.random() * 50) + 1
    const activeWorkflows = Math.floor(workflowCount * Math.random())
    const totalExecutions = Math.floor(Math.random() * 10000) + 100
    const executionsToday = Math.floor(Math.random() * 500) + 10
    
    namespaces.push({
      id: `ns-${i.toString().padStart(4, '0')}`,
      name: `${category}-${environment}-${i.toString().padStart(3, '0')}`,
      displayName: `${tenantName} - ${category.charAt(0).toUpperCase() + category.slice(1)} (${environment})`,
      description: `${category} workflows for ${tenantName} in ${environment} environment`,
      tenantId: `tenant-${Math.floor(i / 5) + 1}`,
      tenantName: tenantName,
      category: category as any,
      status: status as any,
      region: region as any,
      environment: environment as any,
      workflowCount,
      activeWorkflows,
      totalExecutions,
      executionsToday,
      avgExecutionTime: Math.floor(Math.random() * 5000) + 500,
      successRate: Math.floor(Math.random() * 20) + 80,
      errorCount: Math.floor(Math.random() * 20),
      resourceUsage: {
        cpu: Math.floor(Math.random() * 80) + 10,
        memory: Math.floor(Math.random() * 70) + 20,
        storage: Math.floor(Math.random() * 60) + 30,
        network: Math.floor(Math.random() * 40) + 10
      },
      limits: {
        maxWorkflows: 100,
        maxExecutionsPerDay: 1000,
        maxConcurrentExecutions: 50,
        storageLimit: 10240 // MB
      },
      metrics: {
        queueDepth: Math.floor(Math.random() * 100),
        tasksPerSecond: Math.floor(Math.random() * 50) + 5,
        latencyP99: Math.floor(Math.random() * 1000) + 100,
        throughput: Math.floor(Math.random() * 1000) + 100
      },
      createdAt: new Date(Date.now() - Math.random() * 365 * 24 * 3600000),
      lastActivity: new Date(Date.now() - Math.random() * 24 * 3600000),
      owner: `user-${Math.floor(Math.random() * 50) + 1}@company.com`,
      tags: ['temporal', category, environment, region].slice(0, Math.floor(Math.random() * 4) + 1),
      isIsolated: Math.random() > 0.7,
      encryptionEnabled: Math.random() > 0.3
    })
  }

  return namespaces
}

// Generate tenant quotas
const generateTenantQuotas = (namespaces: Namespace[]): TenantQuota[] => {
  const tenantMap = new Map<string, TenantQuota>()

  namespaces.forEach(ns => {
    if (!tenantMap.has(ns.tenantId)) {
      tenantMap.set(ns.tenantId, {
        tenantId: ns.tenantId,
        tenantName: ns.tenantName,
        namespaces: 0,
        maxNamespaces: 20,
        totalWorkflows: 0,
        dailyExecutions: 0,
        storageUsed: 0,
        storageLimit: 50000,
        isOverQuota: false
      })
    }

    const quota = tenantMap.get(ns.tenantId)!
    quota.namespaces++
    quota.totalWorkflows += ns.workflowCount
    quota.dailyExecutions += ns.executionsToday
    quota.storageUsed += ns.resourceUsage.storage * 100 // Convert to MB
    quota.isOverQuota = quota.namespaces > quota.maxNamespaces || 
                       quota.dailyExecutions > 5000 || 
                       quota.storageUsed > quota.storageLimit
  })

  return Array.from(tenantMap.values())
}

export default function MultiTenantNamespaceManager() {
  const [namespaces, setNamespaces] = useState<Namespace[]>([])
  const [tenantQuotas, setTenantQuotas] = useState<TenantQuota[]>([])
  const [filteredNamespaces, setFilteredNamespaces] = useState<Namespace[]>([])
  const [selectedNamespace, setSelectedNamespace] = useState<Namespace | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [selectedEnvironment, setSelectedEnvironment] = useState<string>('all')
  const [selectedRegion, setSelectedRegion] = useState<string>('all')
  const [selectedTenant, setSelectedTenant] = useState<string>('all')
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'tree'>('grid')

  // Initialize data
  useEffect(() => {
    const mockNamespaces = generateMockNamespaces()
    const mockQuotas = generateTenantQuotas(mockNamespaces)
    setNamespaces(mockNamespaces)
    setTenantQuotas(mockQuotas)
    setFilteredNamespaces(mockNamespaces)
  }, [])

  // Auto refresh simulation
  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      setNamespaces(prev => prev.map(ns => ({
        ...ns,
        activeWorkflows: Math.max(0, ns.activeWorkflows + (Math.random() - 0.5) * 2),
        executionsToday: ns.executionsToday + Math.floor(Math.random() * 5),
        resourceUsage: {
          ...ns.resourceUsage,
          cpu: Math.max(0, Math.min(100, ns.resourceUsage.cpu + (Math.random() - 0.5) * 10)),
          memory: Math.max(0, Math.min(100, ns.resourceUsage.memory + (Math.random() - 0.5) * 10))
        },
        metrics: {
          ...ns.metrics,
          queueDepth: Math.max(0, ns.metrics.queueDepth + (Math.random() - 0.5) * 10),
          tasksPerSecond: Math.max(0, ns.metrics.tasksPerSecond + (Math.random() - 0.5) * 5)
        }
      })))
    }, 5000)

    return () => clearInterval(interval)
  }, [autoRefresh])

  // Filter namespaces
  useEffect(() => {
    let filtered = namespaces

    if (searchQuery) {
      filtered = filtered.filter(ns => 
        ns.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ns.displayName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ns.tenantName.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(ns => ns.category === selectedCategory)
    }

    if (selectedStatus !== 'all') {
      filtered = filtered.filter(ns => ns.status === selectedStatus)
    }

    if (selectedEnvironment !== 'all') {
      filtered = filtered.filter(ns => ns.environment === selectedEnvironment)
    }

    if (selectedRegion !== 'all') {
      filtered = filtered.filter(ns => ns.region === selectedRegion)
    }

    if (selectedTenant !== 'all') {
      filtered = filtered.filter(ns => ns.tenantId === selectedTenant)
    }

    setFilteredNamespaces(filtered)
  }, [namespaces, searchQuery, selectedCategory, selectedStatus, selectedEnvironment, selectedRegion, selectedTenant])

  // Calculate summary stats
  const summaryStats = {
    total: namespaces.length,
    active: namespaces.filter(ns => ns.status === 'active').length,
    production: namespaces.filter(ns => ns.environment === 'production').length,
    totalWorkflows: namespaces.reduce((sum, ns) => sum + ns.workflowCount, 0),
    totalExecutions: namespaces.reduce((sum, ns) => sum + ns.executionsToday, 0),
    avgSuccessRate: Math.round(namespaces.reduce((sum, ns) => sum + ns.successRate, 0) / namespaces.length),
    avgCpuUsage: Math.round(namespaces.reduce((sum, ns) => sum + ns.resourceUsage.cpu, 0) / namespaces.length)
  }

  // Get unique values for filters
  const uniqueTenants = Array.from(new Set(namespaces.map(ns => ({ id: ns.tenantId, name: ns.tenantName }))))

  // Status badge component
  const StatusBadge = ({ status }: { status: string }) => {
    const colors = {
      active: 'bg-green-500',
      inactive: 'bg-gray-500',
      suspended: 'bg-red-500',
      maintenance: 'bg-yellow-500'
    }
    
    return (
      <Badge variant="outline" className={`${colors[status as keyof typeof colors]} text-white border-0`}>
        {status}
      </Badge>
    )
  }

  // Resource usage component
  const ResourceUsage = ({ usage, limit, label, icon: Icon }: { 
    usage: number; 
    limit?: number; 
    label: string; 
    icon: any 
  }) => (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center space-x-1">
          <Icon className="w-3 h-3" />
          <span>{label}</span>
        </div>
        <span>{usage}%{limit && ` / ${limit}`}</span>
      </div>
      <Progress value={usage} className="h-1" />
    </div>
  )

  // Namespace card component
  const NamespaceCard = ({ namespace }: { namespace: Namespace }) => (
    <Card className="hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => setSelectedNamespace(namespace)}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-sm">{namespace.displayName}</CardTitle>
            <div className="text-xs text-muted-foreground">{namespace.name}</div>
          </div>
          <StatusBadge status={namespace.status} />
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <Badge variant="outline">{namespace.category}</Badge>
          <Badge variant="outline">{namespace.environment}</Badge>
          <Badge variant="outline">{namespace.region}</Badge>
          {namespace.isIsolated && (
            <Badge variant="secondary">
              <Shield className="w-2 h-2 mr-1" />
              Isolated
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="text-center p-2 bg-muted rounded">
            <div className="font-medium">{namespace.workflowCount}</div>
            <div className="text-muted-foreground">Workflows</div>
          </div>
          <div className="text-center p-2 bg-muted rounded">
            <div className="font-medium">{namespace.activeWorkflows}</div>
            <div className="text-muted-foreground">Active</div>
          </div>
        </div>

        <div className="space-y-2">
          <ResourceUsage usage={namespace.resourceUsage.cpu} label="CPU" icon={Cpu} />
          <ResourceUsage usage={namespace.resourceUsage.memory} label="Memory" icon={HardDrive} />
          <ResourceUsage usage={namespace.resourceUsage.storage} label="Storage" icon={HardDrive} />
        </div>

        <div className="grid grid-cols-3 gap-1 text-xs text-center">
          <div>
            <div className="font-medium">{namespace.executionsToday}</div>
            <div className="text-muted-foreground">Today</div>
          </div>
          <div>
            <div className="font-medium">{namespace.successRate}%</div>
            <div className="text-muted-foreground">Success</div>
          </div>
          <div>
            <div className="font-medium">{namespace.metrics.tasksPerSecond}</div>
            <div className="text-muted-foreground">TPS</div>
          </div>
        </div>

        <div className="flex space-x-1 pt-2">
          <Button size="sm" variant="outline" className="flex-1 text-xs">
            <Play className="w-3 h-3" />
          </Button>
          <Button size="sm" variant="outline" className="flex-1 text-xs">
            <Settings className="w-3 h-3" />
          </Button>
          <Button size="sm" variant="outline" className="flex-1 text-xs">
            <Eye className="w-3 h-3" />
          </Button>
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Multi-Tenant Namespace Manager</h2>
          <p className="text-muted-foreground">
            Manage 1200+ Temporal namespaces across multiple tenants with real-time monitoring and isolation
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Switch checked={autoRefresh} onCheckedChange={setAutoRefresh} />
            <span className="text-sm">Auto Refresh</span>
          </div>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Create Namespace
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Database className="w-4 h-4 text-blue-600" />
              <div className="text-2xl font-bold">{summaryStats.total}</div>
            </div>
            <div className="text-xs text-muted-foreground">Total Namespaces</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.active}</div>
            </div>
            <div className="text-xs text-muted-foreground">Active</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Server className="w-4 h-4 text-purple-600" />
              <div className="text-2xl font-bold">{summaryStats.production}</div>
            </div>
            <div className="text-xs text-muted-foreground">Production</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Workflow className="w-4 h-4 text-orange-600" />
              <div className="text-2xl font-bold">{summaryStats.totalWorkflows}</div>
            </div>
            <div className="text-xs text-muted-foreground">Total Workflows</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.totalExecutions}</div>
            </div>
            <div className="text-xs text-muted-foreground">Executions Today</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <div className="text-2xl font-bold">{summaryStats.avgSuccessRate}%</div>
            </div>
            <div className="text-xs text-muted-foreground">Avg Success Rate</div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Cpu className="w-4 h-4 text-blue-600" />
              <div className="text-2xl font-bold">{summaryStats.avgCpuUsage}%</div>
            </div>
            <div className="text-xs text-muted-foreground">Avg CPU Usage</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="namespaces" className="space-y-6">
        <TabsList>
          <TabsTrigger value="namespaces">Namespaces</TabsTrigger>
          <TabsTrigger value="tenants">Tenant Quotas</TabsTrigger>
          <TabsTrigger value="regional">Regional Distribution</TabsTrigger>
          <TabsTrigger value="monitoring">Live Monitoring</TabsTrigger>
          <TabsTrigger value="isolation">Isolation & Security</TabsTrigger>
        </TabsList>

        {/* Namespaces Tab */}
        <TabsContent value="namespaces" className="space-y-6">
          {/* Filters */}
          <div className="flex flex-wrap items-center gap-4 p-4 bg-muted rounded-lg">
            <div className="flex items-center space-x-2">
              <Search className="w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search namespaces..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-64"
              />
            </div>
            
            <Select value={selectedTenant} onValueChange={setSelectedTenant}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Tenants" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Tenants</SelectItem>
                {uniqueTenants.map(tenant => (
                  <SelectItem key={tenant.id} value={tenant.id}>{tenant.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="marketing">Marketing</SelectItem>
                <SelectItem value="sales">Sales</SelectItem>
                <SelectItem value="support">Support</SelectItem>
                <SelectItem value="operations">Operations</SelectItem>
                <SelectItem value="analytics">Analytics</SelectItem>
                <SelectItem value="custom">Custom</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedEnvironment} onValueChange={setSelectedEnvironment}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Environments" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Environments</SelectItem>
                <SelectItem value="production">Production</SelectItem>
                <SelectItem value="staging">Staging</SelectItem>
                <SelectItem value="development">Development</SelectItem>
                <SelectItem value="testing">Testing</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedRegion} onValueChange={setSelectedRegion}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="All Regions" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Regions</SelectItem>
                <SelectItem value="us-east-1">US East 1</SelectItem>
                <SelectItem value="us-west-2">US West 2</SelectItem>
                <SelectItem value="eu-west-1">EU West 1</SelectItem>
                <SelectItem value="ap-southeast-1">AP Southeast 1</SelectItem>
              </SelectContent>
            </Select>

            <div className="flex items-center space-x-2 ml-auto">
              <span className="text-sm text-muted-foreground">
                {filteredNamespaces.length} of {namespaces.length} namespaces
              </span>
              <div className="flex items-center space-x-1 border rounded">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                >
                  <Package className="w-4 h-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                >
                  <Database className="w-4 h-4" />
                </Button>
                <Button
                  variant={viewMode === 'tree' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('tree')}
                >
                  <GitBranch className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Namespaces Display */}
          {viewMode === 'grid' && (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {filteredNamespaces.map(namespace => (
                <NamespaceCard key={namespace.id} namespace={namespace} />
              ))}
            </div>
          )}

          {viewMode === 'list' && (
            <div className="space-y-2">
              {filteredNamespaces.map(namespace => (
                <Card key={namespace.id} className="p-4 hover:shadow-md transition-shadow cursor-pointer"
                      onClick={() => setSelectedNamespace(namespace)}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div>
                        <div className="font-medium">{namespace.displayName}</div>
                        <div className="text-sm text-muted-foreground">{namespace.name}</div>
                      </div>
                      <div className="flex space-x-2">
                        <Badge variant="outline">{namespace.category}</Badge>
                        <Badge variant="outline">{namespace.environment}</Badge>
                      </div>
                    </div>
                    <div className="flex items-center space-x-6 text-sm">
                      <div className="text-center">
                        <div className="font-medium">{namespace.workflowCount}</div>
                        <div className="text-muted-foreground">Workflows</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium">{namespace.activeWorkflows}</div>
                        <div className="text-muted-foreground">Active</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium">{namespace.resourceUsage.cpu}%</div>
                        <div className="text-muted-foreground">CPU</div>
                      </div>
                      <StatusBadge status={namespace.status} />
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        {/* Tenant Quotas Tab */}
        <TabsContent value="tenants" className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tenantQuotas.map(quota => (
              <Card key={quota.tenantId} className={quota.isOverQuota ? 'border-red-500' : ''}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{quota.tenantName}</CardTitle>
                    {quota.isOverQuota && (
                      <Badge variant="destructive">
                        <AlertTriangle className="w-3 h-3 mr-1" />
                        Over Quota
                      </Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Namespaces</span>
                      <span>{quota.namespaces} / {quota.maxNamespaces}</span>
                    </div>
                    <Progress value={(quota.namespaces / quota.maxNamespaces) * 100} className="h-2" />
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Storage Used</span>
                      <span>{(quota.storageUsed / 1024).toFixed(1)}GB / {(quota.storageLimit / 1024).toFixed(1)}GB</span>
                    </div>
                    <Progress value={(quota.storageUsed / quota.storageLimit) * 100} className="h-2" />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-center text-sm">
                    <div className="p-2 bg-muted rounded">
                      <div className="font-medium">{quota.totalWorkflows}</div>
                      <div className="text-muted-foreground">Workflows</div>
                    </div>
                    <div className="p-2 bg-muted rounded">
                      <div className="font-medium">{quota.dailyExecutions}</div>
                      <div className="text-muted-foreground">Daily Execs</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Regional Distribution Tab */}
        <TabsContent value="regional" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1'].map(region => {
              const regionNamespaces = namespaces.filter(ns => ns.region === region)
              const activeCount = regionNamespaces.filter(ns => ns.status === 'active').length
              const totalWorkflows = regionNamespaces.reduce((sum, ns) => sum + ns.workflowCount, 0)
              const avgCpu = regionNamespaces.length > 0 
                ? Math.round(regionNamespaces.reduce((sum, ns) => sum + ns.resourceUsage.cpu, 0) / regionNamespaces.length)
                : 0

              return (
                <Card key={region}>
                  <CardHeader>
                    <div className="flex items-center space-x-2">
                      <Globe className="w-5 h-5" />
                      <CardTitle>{region}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-2 text-center">
                      <div className="p-3 bg-blue-50 rounded">
                        <div className="text-lg font-bold text-blue-600">{regionNamespaces.length}</div>
                        <div className="text-xs text-muted-foreground">Namespaces</div>
                      </div>
                      <div className="p-3 bg-green-50 rounded">
                        <div className="text-lg font-bold text-green-600">{activeCount}</div>
                        <div className="text-xs text-muted-foreground">Active</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Utilization</span>
                        <span>{((activeCount / regionNamespaces.length) * 100).toFixed(1)}%</span>
                      </div>
                      <Progress value={(activeCount / regionNamespaces.length) * 100} className="h-2" />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="text-center">
                        <div className="font-medium">{totalWorkflows}</div>
                        <div className="text-muted-foreground">Workflows</div>
                      </div>
                      <div className="text-center">
                        <div className="font-medium">{avgCpu}%</div>
                        <div className="text-muted-foreground">Avg CPU</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        {/* Live Monitoring Tab */}
        <TabsContent value="monitoring" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Real-Time Metrics</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-blue-50 rounded">
                      <div className="text-2xl font-bold text-blue-600">
                        {namespaces.reduce((sum, ns) => sum + ns.metrics.tasksPerSecond, 0)}
                      </div>
                      <div className="text-sm text-muted-foreground">Total TPS</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded">
                      <div className="text-2xl font-bold text-green-600">
                        {Math.round(namespaces.reduce((sum, ns) => sum + ns.metrics.latencyP99, 0) / namespaces.length)}ms
                      </div>
                      <div className="text-sm text-muted-foreground">Avg P99 Latency</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Queue Depth Distribution</div>
                    {['0-10', '11-50', '51-100', '100+'].map(range => {
                      const [min, max] = range === '100+' ? [100, Infinity] : range.split('-').map(Number)
                      const count = namespaces.filter(ns => {
                        if (range === '100+') return ns.metrics.queueDepth > 100
                        return ns.metrics.queueDepth >= min && ns.metrics.queueDepth <= max
                      }).length
                      const percentage = (count / namespaces.length) * 100
                      
                      return (
                        <div key={range} className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span>{range} items</span>
                            <span>{count} namespaces ({percentage.toFixed(1)}%)</span>
                          </div>
                          <Progress value={percentage} className="h-1" />
                        </div>
                      )
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Resource Utilization Heatmap</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-10 gap-1">
                  {filteredNamespaces.slice(0, 100).map(ns => (
                    <div
                      key={ns.id}
                      className={`w-4 h-4 rounded ${
                        ns.resourceUsage.cpu > 80 ? 'bg-red-500' :
                        ns.resourceUsage.cpu > 60 ? 'bg-yellow-500' :
                        ns.resourceUsage.cpu > 40 ? 'bg-blue-500' :
                        'bg-green-500'
                      }`}
                      title={`${ns.name}: ${ns.resourceUsage.cpu}% CPU`}
                    />
                  ))}
                </div>
                <div className="flex items-center justify-between mt-4 text-xs">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded"></div>
                    <span>Low (0-40%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-blue-500 rounded"></div>
                    <span>Medium (41-60%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-yellow-500 rounded"></div>
                    <span>High (61-80%)</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded"></div>
                    <span>Critical (80%+)</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Isolation & Security Tab */}
        <TabsContent value="isolation" className="space-y-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Shield className="w-5 h-5" />
                  <span>Security Status</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className="p-3 bg-blue-50 rounded">
                      <div className="text-lg font-bold text-blue-600">
                        {namespaces.filter(ns => ns.isIsolated).length}
                      </div>
                      <div className="text-sm text-muted-foreground">Isolated Namespaces</div>
                    </div>
                    <div className="p-3 bg-green-50 rounded">
                      <div className="text-lg font-bold text-green-600">
                        {namespaces.filter(ns => ns.encryptionEnabled).length}
                      </div>
                      <div className="text-sm text-muted-foreground">Encrypted</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="text-sm font-medium">Security Compliance</div>
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span>Isolation Enabled</span>
                        <span>{((namespaces.filter(ns => ns.isIsolated).length / namespaces.length) * 100).toFixed(1)}%</span>
                      </div>
                      <Progress value={(namespaces.filter(ns => ns.isIsolated).length / namespaces.length) * 100} className="h-1" />
                    </div>
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span>Encryption Enabled</span>
                        <span>{((namespaces.filter(ns => ns.encryptionEnabled).length / namespaces.length) * 100).toFixed(1)}%</span>
                      </div>
                      <Progress value={(namespaces.filter(ns => ns.encryptionEnabled).length / namespaces.length) * 100} className="h-1" />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tenant Isolation Matrix</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {tenantQuotas.slice(0, 10).map(tenant => {
                    const tenantNamespaces = namespaces.filter(ns => ns.tenantId === tenant.tenantId)
                    const isolatedCount = tenantNamespaces.filter(ns => ns.isIsolated).length
                    const isolationPercentage = (isolatedCount / tenantNamespaces.length) * 100
                    
                    return (
                      <div key={tenant.tenantId} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="truncate">{tenant.tenantName}</span>
                          <span>{isolatedCount}/{tenantNamespaces.length} isolated</span>
                        </div>
                        <Progress value={isolationPercentage} className="h-1" />
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Namespace Detail Modal */}
      {selectedNamespace && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
             onClick={() => setSelectedNamespace(null)}>
          <div className="bg-white rounded-lg p-6 max-w-6xl w-full m-4 max-h-[90vh] overflow-y-auto" 
               onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-xl font-semibold">{selectedNamespace.displayName}</h3>
                <p className="text-muted-foreground">{selectedNamespace.name}</p>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setSelectedNamespace(null)}>×</Button>
            </div>
            
            <Tabs defaultValue="overview" className="space-y-4">
              <TabsList>
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="workflows">Workflows</TabsTrigger>
                <TabsTrigger value="metrics">Metrics</TabsTrigger>
                <TabsTrigger value="security">Security</TabsTrigger>
                <TabsTrigger value="logs">Logs</TabsTrigger>
              </TabsList>
              
              <TabsContent value="overview" className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedNamespace.workflowCount}</div>
                    <div className="text-sm text-muted-foreground">Total Workflows</div>
                  </div>
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedNamespace.activeWorkflows}</div>
                    <div className="text-sm text-muted-foreground">Active Workflows</div>
                  </div>
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedNamespace.executionsToday}</div>
                    <div className="text-sm text-muted-foreground">Executions Today</div>
                  </div>
                  <div className="p-4 border rounded">
                    <div className="text-2xl font-bold">{selectedNamespace.successRate}%</div>
                    <div className="text-sm text-muted-foreground">Success Rate</div>
                  </div>
                </div>
                
                <div className="grid gap-4 lg:grid-cols-2">
                  <Card>
                    <CardHeader>
                      <CardTitle>Resource Usage</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <ResourceUsage 
                        usage={selectedNamespace.resourceUsage.cpu} 
                        label="CPU" 
                        icon={Cpu} 
                      />
                      <ResourceUsage 
                        usage={selectedNamespace.resourceUsage.memory} 
                        label="Memory" 
                        icon={HardDrive} 
                      />
                      <ResourceUsage 
                        usage={selectedNamespace.resourceUsage.storage} 
                        label="Storage" 
                        icon={HardDrive} 
                      />
                      <ResourceUsage 
                        usage={selectedNamespace.resourceUsage.network} 
                        label="Network" 
                        icon={Network} 
                      />
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardHeader>
                      <CardTitle>Configuration</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Tenant:</span>
                        <span>{selectedNamespace.tenantName}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Environment:</span>
                        <Badge>{selectedNamespace.environment}</Badge>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Region:</span>
                        <Badge>{selectedNamespace.region}</Badge>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Isolated:</span>
                        <Badge variant={selectedNamespace.isIsolated ? 'default' : 'secondary'}>
                          {selectedNamespace.isIsolated ? 'Yes' : 'No'}
                        </Badge>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Encrypted:</span>
                        <Badge variant={selectedNamespace.encryptionEnabled ? 'default' : 'secondary'}>
                          {selectedNamespace.encryptionEnabled ? 'Yes' : 'No'}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      )}
    </div>
  )
}