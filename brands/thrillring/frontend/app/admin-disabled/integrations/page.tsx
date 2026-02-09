'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  Settings,
  Shield,
  Globe,
  Users,
  Activity,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Plus,
  Save,
  RefreshCw,
  Eye,
  EyeOff,
  Trash2,
  Edit,
  Search,
  Filter,
  BarChart3,
  Database,
  Mail,
  ShoppingCart,
  MessageSquare,
  PieChart,
  Zap,
  CreditCard,
  Building,
  Share2,
  Megaphone
} from 'lucide-react'

interface Integration {
  id: string
  name: string
  category: 'analytics' | 'advertising' | 'social' | 'email' | 'payment' | 'crm' | 'communication' | 'webmaster' | 'automation' | 'ecommerce'
  description: string
  status: 'enabled' | 'disabled' | 'maintenance'
  global_enabled: boolean
  tenant_count: number
  usage_stats: {
    active_tenants: number
    total_requests: number
    success_rate: number
    avg_response_time: number
  }
  permissions: {
    super_admin_only: boolean
    require_approval: boolean
    auto_provision: boolean
    rate_limit: number
  }
  health: {
    status: 'healthy' | 'warning' | 'error'
    last_check: string
    uptime: number
    error_count: number
  }
  features: string[]
  dependencies: string[]
  created_at: string
  updated_at: string
}

interface TenantIntegration {
  tenant_id: string
  tenant_name: string
  integration_id: string
  integration_name: string
  enabled: boolean
  configured: boolean
  last_used: string
  usage_count: number
  error_count: number
  status: 'active' | 'inactive' | 'error' | 'suspended'
}

const categoryIcons = {
  analytics: BarChart3,
  advertising: Megaphone,
  social: Share2,
  email: Mail,
  payment: CreditCard,
  crm: Building,
  communication: MessageSquare,
  webmaster: Globe,
  automation: Zap,
  ecommerce: ShoppingCart
}

const categoryColors = {
  analytics: 'bg-blue-100 text-blue-800',
  advertising: 'bg-green-100 text-green-800',
  social: 'bg-purple-100 text-purple-800',
  email: 'bg-orange-100 text-orange-800',
  payment: 'bg-red-100 text-red-800',
  crm: 'bg-indigo-100 text-indigo-800',
  communication: 'bg-yellow-100 text-yellow-800',
  webmaster: 'bg-teal-100 text-teal-800',
  automation: 'bg-pink-100 text-pink-800',
  ecommerce: 'bg-emerald-100 text-emerald-800'
}

export default function SuperAdminIntegrationsPage() {
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [tenantIntegrations, setTenantIntegrations] = useState<TenantIntegration[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [showConfigModal, setShowConfigModal] = useState<string | null>(null)
  const [bulkAction, setBulkAction] = useState<string>('')
  const [selectedIntegrations, setSelectedIntegrations] = useState<string[]>([])
  const [alerts, setAlerts] = useState<{ type: 'success' | 'error' | 'warning', message: string }[]>([])

  useEffect(() => {
    fetchIntegrations()
    fetchTenantIntegrations()
  }, [])

  const fetchIntegrations = async () => {
    try {
      const response = await fetch('/api/brain/integrations/admin/list')
      if (response.ok) {
        const data = await response.json()
        setIntegrations(data.integrations || [])
      }
    } catch (error) {
      addAlert('error', 'Failed to fetch integrations')
    }
  }

  const fetchTenantIntegrations = async () => {
    try {
      const response = await fetch('/api/brain/integrations/admin/tenant-usage')
      if (response.ok) {
        const data = await response.json()
        setTenantIntegrations(data.tenant_integrations || [])
      }
    } catch (error) {
      addAlert('error', 'Failed to fetch tenant integrations')
    } finally {
      setIsLoading(false)
    }
  }

  const addAlert = (type: 'success' | 'error' | 'warning', message: string) => {
    const alert = { type, message }
    setAlerts(prev => [...prev, alert])
    setTimeout(() => {
      setAlerts(prev => prev.filter(a => a !== alert))
    }, 5000)
  }

  const toggleIntegrationGlobally = async (integrationId: string, enabled: boolean) => {
    try {
      const response = await fetch(`/api/brain/integrations/admin/${integrationId}/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ global_enabled: enabled })
      })

      if (response.ok) {
        setIntegrations(prev => prev.map(int =>
          int.id === integrationId ? { ...int, global_enabled: enabled } : int
        ))
        addAlert('success', `Integration ${enabled ? 'enabled' : 'disabled'} globally`)
      } else {
        addAlert('error', 'Failed to update integration status')
      }
    } catch (error) {
      addAlert('error', 'Network error occurred')
    }
  }

  const updateIntegrationPermissions = async (integrationId: string, permissions: Partial<Integration['permissions']>) => {
    try {
      const response = await fetch(`/api/brain/integrations/admin/${integrationId}/permissions`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ permissions })
      })

      if (response.ok) {
        setIntegrations(prev => prev.map(int =>
          int.id === integrationId ? { ...int, permissions: { ...int.permissions, ...permissions } } : int
        ))
        addAlert('success', 'Permissions updated successfully')
        setShowConfigModal(null)
      } else {
        addAlert('error', 'Failed to update permissions')
      }
    } catch (error) {
      addAlert('error', 'Network error occurred')
    }
  }

  const runHealthCheck = async (integrationId: string) => {
    try {
      const response = await fetch(`/api/brain/integrations/admin/${integrationId}/health-check`, {
        method: 'POST'
      })

      if (response.ok) {
        const healthData = await response.json()
        setIntegrations(prev => prev.map(int =>
          int.id === integrationId ? { ...int, health: healthData.health } : int
        ))
        addAlert('success', 'Health check completed')
      } else {
        addAlert('error', 'Health check failed')
      }
    } catch (error) {
      addAlert('error', 'Network error occurred')
    }
  }

  const executeBulkAction = async () => {
    if (!bulkAction || selectedIntegrations.length === 0) return

    try {
      const response = await fetch('/api/brain/integrations/admin/bulk-action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: bulkAction,
          integration_ids: selectedIntegrations
        })
      })

      if (response.ok) {
        addAlert('success', `Bulk action "${bulkAction}" executed successfully`)
        setSelectedIntegrations([])
        setBulkAction('')
        fetchIntegrations()
      } else {
        addAlert('error', 'Bulk action failed')
      }
    } catch (error) {
      addAlert('error', 'Network error occurred')
    }
  }

  const filteredIntegrations = integrations.filter(integration => {
    const matchesSearch = integration.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      integration.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || integration.category === selectedCategory
    const matchesStatus = selectedStatus === 'all' || integration.status === selectedStatus

    return matchesSearch && matchesCategory && matchesStatus
  })

  const getHealthIcon = (health: Integration['health']) => {
    switch (health.status) {
      case 'healthy': return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'warning': return <AlertTriangle className="w-4 h-4 text-yellow-500" />
      case 'error': return <XCircle className="w-4 h-4 text-red-500" />
    }
  }

  const IntegrationCard = ({ integration }: { integration: Integration }) => {
    const IconComponent = categoryIcons[integration.category]
    const categoryColorClass = categoryColors[integration.category]

    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className={`p-2 rounded-lg ${categoryColorClass}`}>
                <IconComponent className="w-5 h-5" />
              </div>
              <div>
                <CardTitle className="text-lg">{integration.name}</CardTitle>
                <CardDescription className="text-sm">{integration.description}</CardDescription>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              {getHealthIcon(integration.health)}
              <Switch
                checked={integration.global_enabled}
                onCheckedChange={(checked) => toggleIntegrationGlobally(integration.id, checked)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              <Badge variant="outline" className={categoryColorClass}>
                {integration.category}
              </Badge>
              <Badge variant={integration.status === 'enabled' ? 'default' : 'secondary'}>
                {integration.status}
              </Badge>
              <Badge variant="outline">
                {integration.tenant_count} tenants
              </Badge>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <Label className="text-xs text-muted-foreground">Active Tenants</Label>
                <div className="font-medium">{integration.usage_stats.active_tenants}</div>
              </div>
              <div>
                <Label className="text-xs text-muted-foreground">Success Rate</Label>
                <div className="font-medium">{integration.usage_stats.success_rate}%</div>
              </div>
              <div>
                <Label className="text-xs text-muted-foreground">Total Requests</Label>
                <div className="font-medium">{integration.usage_stats.total_requests.toLocaleString()}</div>
              </div>
              <div>
                <Label className="text-xs text-muted-foreground">Avg Response</Label>
                <div className="font-medium">{integration.usage_stats.avg_response_time}ms</div>
              </div>
            </div>

            <div className="flex space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowConfigModal(integration.id)}
              >
                <Settings className="w-4 h-4 mr-1" />
                Configure
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => runHealthCheck(integration.id)}
              >
                <Activity className="w-4 h-4 mr-1" />
                Health Check
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  const ConfigurationModal = ({ integrationId }: { integrationId: string }) => {
    const integration = integrations.find(int => int.id === integrationId)
    const [permissions, setPermissions] = useState(integration?.permissions || ({} as any))

    if (!integration) return null

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <Card className="w-full max-w-2xl max-h-[80vh] overflow-y-auto">
          <CardHeader>
            <CardTitle>Configure {integration.name}</CardTitle>
            <CardDescription>Manage permissions and settings for this integration</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label>Super Admin Only</Label>
                <Switch
                  checked={permissions.super_admin_only}
                  onCheckedChange={(checked) => setPermissions(prev => ({ ...prev, super_admin_only: checked }))}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label>Require Admin Approval</Label>
                <Switch
                  checked={permissions.require_approval}
                  onCheckedChange={(checked) => setPermissions(prev => ({ ...prev, require_approval: checked }))}
                />
              </div>

              <div className="flex items-center justify-between">
                <Label>Auto Provision for New Tenants</Label>
                <Switch
                  checked={permissions.auto_provision}
                  onCheckedChange={(checked) => setPermissions(prev => ({ ...prev, auto_provision: checked }))}
                />
              </div>

              <div className="space-y-2">
                <Label>Rate Limit (requests per hour)</Label>
                <Input
                  type="number"
                  value={permissions.rate_limit}
                  onChange={(e) => setPermissions(prev => ({ ...prev, rate_limit: parseInt(e.target.value) || 0 }))}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label>Features</Label>
              <div className="flex flex-wrap gap-1">
                {integration.features.map((feature, index) => (
                  <Badge key={index} variant="outline">{feature}</Badge>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <Label>Dependencies</Label>
              <div className="flex flex-wrap gap-1">
                {integration.dependencies.map((dep, index) => (
                  <Badge key={index} variant="secondary">{dep}</Badge>
                ))}
              </div>
            </div>

            <div className="flex justify-end space-x-2">
              <Button variant="outline" onClick={() => setShowConfigModal(null)}>
                Cancel
              </Button>
              <Button onClick={() => updateIntegrationPermissions(integrationId, permissions)}>
                <Save className="w-4 h-4 mr-1" />
                Save Changes
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Alerts */}
      {alerts.map((alert, index) => (
        <Alert key={index} className={alert.type === 'error' ? 'border-red-200 bg-red-50' :
          alert.type === 'warning' ? 'border-yellow-200 bg-yellow-50' :
            'border-green-200 bg-green-50'}>
          <AlertDescription>{alert.message}</AlertDescription>
        </Alert>
      ))}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Super Admin - Integration Management</h1>
          <p className="text-muted-foreground">Manage global integration settings and tenant access</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={fetchIntegrations}>
            <RefreshCw className="w-4 h-4 mr-1" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px]">
              <Label>Search Integrations</Label>
              <div className="relative">
                <Search className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Search by name or description..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-9"
                />
              </div>
            </div>

            <div className="w-48">
              <Label>Category</Label>
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="analytics">Analytics</SelectItem>
                  <SelectItem value="advertising">Advertising</SelectItem>
                  <SelectItem value="social">Social Media</SelectItem>
                  <SelectItem value="email">Email</SelectItem>
                  <SelectItem value="payment">Payment</SelectItem>
                  <SelectItem value="crm">CRM</SelectItem>
                  <SelectItem value="communication">Communication</SelectItem>
                  <SelectItem value="webmaster">Webmaster</SelectItem>
                  <SelectItem value="automation">Automation</SelectItem>
                  <SelectItem value="ecommerce">E-commerce</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="w-48">
              <Label>Status</Label>
              <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="enabled">Enabled</SelectItem>
                  <SelectItem value="disabled">Disabled</SelectItem>
                  <SelectItem value="maintenance">Maintenance</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Bulk Actions */}
          {selectedIntegrations.length > 0 && (
            <div className="mt-4 p-4 bg-muted rounded-lg">
              <div className="flex items-center space-x-4">
                <span className="text-sm font-medium">
                  {selectedIntegrations.length} integration(s) selected
                </span>
                <Select value={bulkAction} onValueChange={setBulkAction}>
                  <SelectTrigger className="w-48">
                    <SelectValue placeholder="Select bulk action" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="enable">Enable All</SelectItem>
                    <SelectItem value="disable">Disable All</SelectItem>
                    <SelectItem value="health-check">Run Health Check</SelectItem>
                    <SelectItem value="reset-stats">Reset Statistics</SelectItem>
                  </SelectContent>
                </Select>
                <Button onClick={executeBulkAction} disabled={!bulkAction}>
                  Execute
                </Button>
                <Button variant="outline" onClick={() => setSelectedIntegrations([])}>
                  Clear Selection
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="integrations" className="space-y-4">
        <TabsList>
          <TabsTrigger value="integrations">Integrations ({filteredIntegrations.length})</TabsTrigger>
          <TabsTrigger value="tenant-usage">Tenant Usage</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="integrations">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredIntegrations.map((integration) => (
              <IntegrationCard key={integration.id} integration={integration} />
            ))}
          </div>

          {filteredIntegrations.length === 0 && (
            <Card>
              <CardContent className="text-center py-12">
                <p className="text-muted-foreground">No integrations match your current filters.</p>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="tenant-usage">
          <Card>
            <CardHeader>
              <CardTitle>Tenant Integration Usage</CardTitle>
              <CardDescription>Overview of integration usage across all tenants</CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-96">
                <div className="space-y-4">
                  {tenantIntegrations.map((tenantInt, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex-1">
                        <div className="font-medium">{tenantInt.tenant_name}</div>
                        <div className="text-sm text-muted-foreground">{tenantInt.integration_name}</div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <Badge variant={tenantInt.status === 'active' ? 'default' : 'secondary'}>
                          {tenantInt.status}
                        </Badge>
                        <div className="text-sm text-muted-foreground">
                          {tenantInt.usage_count} uses
                        </div>
                        <Switch checked={tenantInt.enabled} disabled />
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Integrations</CardTitle>
                <Database className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{integrations.length}</div>
                <p className="text-xs text-muted-foreground">
                  {integrations.filter(i => i.global_enabled).length} enabled globally
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Active Tenants</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {integrations.reduce((sum, int) => sum + int.usage_stats.active_tenants, 0)}
                </div>
                <p className="text-xs text-muted-foreground">
                  Across all integrations
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Requests</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {integrations.reduce((sum, int) => sum + int.usage_stats.total_requests, 0).toLocaleString()}
                </div>
                <p className="text-xs text-muted-foreground">
                  Last 30 days
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Avg Success Rate</CardTitle>
                <CheckCircle className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {integrations.length > 0 ?
                    Math.round(integrations.reduce((sum, int) => sum + int.usage_stats.success_rate, 0) / integrations.length) : 0}%
                </div>
                <p className="text-xs text-muted-foreground">
                  Across all integrations
                </p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Configuration Modal */}
      {showConfigModal && <ConfigurationModal integrationId={showConfigModal} />}
    </div>
  )
}