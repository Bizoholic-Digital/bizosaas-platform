"use client"

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Separator } from '@/components/ui/separator'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Area,
  AreaChart
} from 'recharts'
import { 
  Plus, 
  Edit3, 
  Trash2, 
  Play, 
  Pause, 
  Eye,
  Download,
  Upload,
  Settings,
  Users,
  Mail,
  TrendingUp,
  Target,
  Zap,
  Clock,
  CheckCircle,
  AlertCircle,
  Info,
  Filter,
  Search,
  MoreHorizontal,
  ArrowRight,
  Send,
  UserCheck,
  DollarSign
} from 'lucide-react'

// Types
interface Funnel {
  id: string
  name: string
  description?: string
  funnel_type: string
  stages: FunnelStage[]
  automation_rules: any
  mautic_campaign_id?: string
  conversion_goals: any
  is_active: boolean
  created_at: string
  updated_at: string
  performance?: FunnelPerformance
}

interface FunnelStage {
  id: string
  name: string
  stage_type: string
  description?: string
  position: number
  is_active: boolean
  email_templates: EmailTemplate[]
  delay_before_action?: number
  entry_conditions: any[]
  exit_conditions: any[]
  actions: any[]
  conversion_goals: any
}

interface EmailTemplate {
  id: string
  name: string
  subject: string
  html_content: string
  text_content?: string
  delay_hours?: number
}

interface FunnelPerformance {
  total_entries: number
  total_completions: number
  completion_rate: number
  average_time_to_complete?: number
  stage_conversion_rates: { [key: string]: number }
  revenue_generated: number
}

interface FunnelTemplate {
  id: string
  name: string
  description: string
  category: string
  stages: any[]
  estimated_setup_time: string
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D']

export default function FunnelsPage() {
  const [funnels, setFunnels] = useState<Funnel[]>([])
  const [templates, setTemplates] = useState<FunnelTemplate[]>([])
  const [selectedFunnel, setSelectedFunnel] = useState<Funnel | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isTemplateDialogOpen, setIsTemplateDialogOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  // Mock data for development
  useEffect(() => {
    const mockFunnels: Funnel[] = [
      {
        id: '1',
        name: 'SaaS Trial Conversion',
        description: 'Convert trial users to paid subscribers',
        funnel_type: 'saas_trial',
        stages: [
          {
            id: 'stage_1',
            name: 'Welcome Email',
            stage_type: 'welcome_sequence',
            position: 0,
            is_active: true,
            email_templates: [
              {
                id: 'email_1',
                name: 'Welcome & Getting Started',
                subject: 'Welcome to BizoholicSaaS! Your journey starts here',
                html_content: '<p>Welcome email content...</p>',
                delay_hours: 0
              }
            ],
            delay_before_action: 0,
            entry_conditions: [],
            exit_conditions: [],
            actions: [],
            conversion_goals: {}
          },
          {
            id: 'stage_2',
            name: 'Feature Education',
            stage_type: 'nurture_sequence',
            position: 1,
            is_active: true,
            email_templates: [
              {
                id: 'email_2',
                name: 'Key Features Tour',
                subject: '5 features that will transform your workflow',
                html_content: '<p>Features email content...</p>',
                delay_hours: 24
              }
            ],
            delay_before_action: 24 * 60,
            entry_conditions: [],
            exit_conditions: [],
            actions: [],
            conversion_goals: {}
          }
        ],
        automation_rules: {},
        mautic_campaign_id: 'mautic_123',
        conversion_goals: {},
        is_active: true,
        created_at: '2024-01-15T10:00:00Z',
        updated_at: '2024-01-15T10:00:00Z',
        performance: {
          total_entries: 1250,
          total_completions: 156,
          completion_rate: 12.48,
          average_time_to_complete: 8.5,
          stage_conversion_rates: {
            'stage_1': 100,
            'stage_2': 80,
            'stage_3': 60,
            'stage_4': 40
          },
          revenue_generated: 15600
        }
      },
      {
        id: '2',
        name: 'Lead Nurturing Campaign',
        description: 'Nurture leads with valuable content',
        funnel_type: 'lead_generation',
        stages: [
          {
            id: 'stage_1',
            name: 'Lead Magnet Delivery',
            stage_type: 'lead_magnet',
            position: 0,
            is_active: true,
            email_templates: [
              {
                id: 'email_1',
                name: 'Download Your Free Guide',
                subject: 'Your free marketing guide is ready!',
                html_content: '<p>Lead magnet email content...</p>',
                delay_hours: 0
              }
            ],
            delay_before_action: 0,
            entry_conditions: [],
            exit_conditions: [],
            actions: [],
            conversion_goals: {}
          }
        ],
        automation_rules: {},
        mautic_campaign_id: 'mautic_456',
        conversion_goals: {},
        is_active: true,
        created_at: '2024-01-10T14:30:00Z',
        updated_at: '2024-01-10T14:30:00Z',
        performance: {
          total_entries: 850,
          total_completions: 127,
          completion_rate: 14.94,
          average_time_to_complete: 12.3,
          stage_conversion_rates: {
            'stage_1': 100,
            'stage_2': 75,
            'stage_3': 55
          },
          revenue_generated: 8500
        }
      }
    ]

    const mockTemplates: FunnelTemplate[] = [
      {
        id: 'saas_trial',
        name: 'SaaS Free Trial Funnel',
        description: 'Convert trial users to paid subscribers with proven email sequences',
        category: 'SaaS',
        stages: [],
        estimated_setup_time: '15 minutes'
      },
      {
        id: 'lead_generation',
        name: 'Lead Generation Funnel',
        description: 'Capture and nurture leads with valuable content',
        category: 'Lead Generation',
        stages: [],
        estimated_setup_time: '20 minutes'
      },
      {
        id: 'e_commerce',
        name: 'E-commerce Sales Funnel',
        description: 'Convert browsers to buyers with abandoned cart recovery',
        category: 'E-commerce',
        stages: [],
        estimated_setup_time: '25 minutes'
      },
      {
        id: 'webinar',
        name: 'Webinar Registration Funnel',
        description: 'Drive webinar registrations and attendance',
        category: 'Webinar',
        stages: [],
        estimated_setup_time: '18 minutes'
      }
    ]

    setFunnels(mockFunnels)
    setTemplates(mockTemplates)
    setIsLoading(false)
  }, [])

  const filteredFunnels = funnels.filter(funnel => {
    const matchesSearch = funnel.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         funnel.description?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || 
                         (statusFilter === 'active' && funnel.is_active) ||
                         (statusFilter === 'inactive' && !funnel.is_active)
    return matchesSearch && matchesStatus
  })

  const handleCreateFunnel = async (templateId?: string) => {
    // Implementation for creating funnel
    console.log('Creating funnel', templateId)
    setIsCreateDialogOpen(false)
    setIsTemplateDialogOpen(false)
  }

  const handleDeleteFunnel = async (funnelId: string) => {
    setFunnels(funnels.filter(f => f.id !== funnelId))
  }

  const handleToggleFunnelStatus = async (funnelId: string) => {
    setFunnels(funnels.map(f => 
      f.id === funnelId ? { ...f, is_active: !f.is_active } : f
    ))
  }

  const FunnelCard = ({ funnel }: { funnel: Funnel }) => (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <CardTitle className="flex items-center gap-2">
              {funnel.name}
              <Badge variant={funnel.is_active ? "default" : "secondary"}>
                {funnel.is_active ? "Active" : "Inactive"}
              </Badge>
              {funnel.mautic_campaign_id && (
                <Badge variant="outline" className="text-xs">
                  <Mail className="w-3 h-3 mr-1" />
                  Synced
                </Badge>
              )}
            </CardTitle>
            <CardDescription>{funnel.description}</CardDescription>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSelectedFunnel(funnel)}
            >
              <Eye className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleToggleFunnelStatus(funnel.id)}
            >
              {funnel.is_active ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleDeleteFunnel(funnel.id)}
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {/* Performance Metrics */}
          {funnel.performance && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {funnel.performance.total_entries}
                </div>
                <div className="text-sm text-gray-500">Total Entries</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {funnel.performance.total_completions}
                </div>
                <div className="text-sm text-gray-500">Completions</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {funnel.performance.completion_rate.toFixed(1)}%
                </div>
                <div className="text-sm text-gray-500">Conversion</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  ${funnel.performance.revenue_generated.toLocaleString()}
                </div>
                <div className="text-sm text-gray-500">Revenue</div>
              </div>
            </div>
          )}

          {/* Stage Progress */}
          <div className="space-y-2">
            <div className="text-sm font-medium">Funnel Stages ({funnel.stages.length})</div>
            <div className="flex items-center space-x-1">
              {funnel.stages.map((stage, index) => (
                <React.Fragment key={stage.id}>
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-gray-600 truncate">{stage.name}</div>
                    <Progress 
                      value={funnel.performance?.stage_conversion_rates[stage.id] || 0} 
                      className="h-2"
                    />
                  </div>
                  {index < funnel.stages.length - 1 && (
                    <ArrowRight className="w-3 h-3 text-gray-400" />
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </CardContent>

      <CardFooter className="pt-4">
        <div className="flex items-center justify-between w-full text-sm text-gray-500">
          <span>Created {new Date(funnel.created_at).toLocaleDateString()}</span>
          <div className="flex items-center space-x-4">
            <span className="flex items-center">
              <Users className="w-4 h-4 mr-1" />
              {funnel.stages.length} stages
            </span>
            <span className="flex items-center">
              <Mail className="w-4 h-4 mr-1" />
              {funnel.stages.reduce((acc, stage) => acc + stage.email_templates.length, 0)} emails
            </span>
          </div>
        </div>
      </CardFooter>
    </Card>
  )

  const FunnelAnalytics = ({ funnel }: { funnel: Funnel }) => {
    if (!funnel.performance) return null

    const stageData = funnel.stages.map((stage, index) => ({
      name: stage.name.length > 15 ? stage.name.substring(0, 15) + '...' : stage.name,
      fullName: stage.name,
      conversion: funnel.performance?.stage_conversion_rates[stage.id] || 0,
      position: index
    }))

    const conversionData = stageData.map((stage, index) => {
      const entries = index === 0 ? funnel.performance!.total_entries : 
        Math.round(funnel.performance!.total_entries * (stageData[index - 1]?.conversion || 100) / 100)
      const completions = Math.round(entries * stage.conversion / 100)
      
      return {
        stage: stage.name,
        entries,
        completions,
        dropoff: entries - completions
      }
    })

    const pieData = [
      { name: 'Completed', value: funnel.performance.total_completions, color: '#00C49F' },
      { name: 'Dropped Off', value: funnel.performance.total_entries - funnel.performance.total_completions, color: '#FF8042' }
    ]

    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Conversion Funnel Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Stage Conversion Rates
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stageData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [`${value}%`, 'Conversion Rate']}
                  labelFormatter={(label) => stageData.find(s => s.name === label)?.fullName || label}
                />
                <Bar dataKey="conversion" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Completion Overview */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="w-5 h-5" />
              Completion Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Funnel Flow */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              Funnel Flow Analysis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={conversionData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="stage" />
                <YAxis />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey="entries" 
                  stackId="1" 
                  stroke="#3B82F6" 
                  fill="#3B82F6" 
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="dropoff" 
                  stackId="1" 
                  stroke="#EF4444" 
                  fill="#EF4444" 
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    )
  }

  const TemplateSelector = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {templates.map((template) => (
        <Card key={template.id} className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              {template.name}
              <Badge variant="outline">{template.category}</Badge>
            </CardTitle>
            <CardDescription>{template.description}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between text-sm text-gray-500">
              <span className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {template.estimated_setup_time}
              </span>
            </div>
          </CardContent>
          <CardFooter>
            <Button 
              onClick={() => handleCreateFunnel(template.id)}
              className="w-full"
            >
              Use This Template
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto p-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Sales Funnels</h1>
          <p className="text-gray-600 mt-2">Create and manage automated email marketing funnels</p>
        </div>
        
        <div className="flex items-center space-x-3">
          <Dialog open={isTemplateDialogOpen} onOpenChange={setIsTemplateDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Templates
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Choose a Funnel Template</DialogTitle>
                <DialogDescription>
                  Start with a proven template or create a custom funnel from scratch
                </DialogDescription>
              </DialogHeader>
              <TemplateSelector />
            </DialogContent>
          </Dialog>

          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Create Funnel
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>Create New Funnel</DialogTitle>
                <DialogDescription>
                  Build a custom sales funnel from scratch
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <div>
                  <Label htmlFor="funnel-name">Funnel Name</Label>
                  <Input id="funnel-name" placeholder="Enter funnel name" />
                </div>
                <div>
                  <Label htmlFor="funnel-description">Description</Label>
                  <Textarea 
                    id="funnel-description" 
                    placeholder="Describe your funnel's purpose and goals" 
                  />
                </div>
                <div>
                  <Label htmlFor="funnel-type">Funnel Type</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select funnel type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="lead_nurturing">Lead Nurturing</SelectItem>
                      <SelectItem value="saas_trial">SaaS Trial</SelectItem>
                      <SelectItem value="e_commerce">E-commerce</SelectItem>
                      <SelectItem value="webinar">Webinar</SelectItem>
                      <SelectItem value="custom">Custom</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="flex items-center space-x-2">
                  <Switch id="activate-immediately" />
                  <Label htmlFor="activate-immediately">Activate immediately</Label>
                </div>
              </div>
              <div className="flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={() => handleCreateFunnel()}>
                  Create Funnel
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="flex items-center space-x-4 mb-6">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <Input
            placeholder="Search funnels..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {selectedFunnel ? (
        // Detailed Funnel View
        <div className="space-y-6">
          <div className="flex items-center space-x-4">
            <Button variant="ghost" onClick={() => setSelectedFunnel(null)}>
              ← Back to Funnels
            </Button>
            <div>
              <h2 className="text-2xl font-bold">{selectedFunnel.name}</h2>
              <p className="text-gray-600">{selectedFunnel.description}</p>
            </div>
          </div>

          <Tabs defaultValue="overview" className="space-y-6">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="analytics">Analytics</TabsTrigger>
              <TabsTrigger value="stages">Stages</TabsTrigger>
              <TabsTrigger value="emails">Email Templates</TabsTrigger>
              <TabsTrigger value="automation">Automation</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>

            <TabsContent value="overview">
              <div className="space-y-6">
                {selectedFunnel.performance && (
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <Card>
                      <CardContent className="p-6">
                        <div className="flex items-center space-x-2">
                          <Users className="w-8 h-8 text-blue-600" />
                          <div>
                            <div className="text-2xl font-bold">{selectedFunnel.performance.total_entries}</div>
                            <div className="text-sm text-gray-500">Total Entries</div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardContent className="p-6">
                        <div className="flex items-center space-x-2">
                          <CheckCircle className="w-8 h-8 text-green-600" />
                          <div>
                            <div className="text-2xl font-bold">{selectedFunnel.performance.total_completions}</div>
                            <div className="text-sm text-gray-500">Completions</div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardContent className="p-6">
                        <div className="flex items-center space-x-2">
                          <Target className="w-8 h-8 text-purple-600" />
                          <div>
                            <div className="text-2xl font-bold">{selectedFunnel.performance.completion_rate.toFixed(1)}%</div>
                            <div className="text-sm text-gray-500">Conversion Rate</div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardContent className="p-6">
                        <div className="flex items-center space-x-2">
                          <DollarSign className="w-8 h-8 text-orange-600" />
                          <div>
                            <div className="text-2xl font-bold">${selectedFunnel.performance.revenue_generated.toLocaleString()}</div>
                            <div className="text-sm text-gray-500">Revenue</div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                )}

                <Alert>
                  <Info className="h-4 w-4" />
                  <AlertTitle>Funnel Status</AlertTitle>
                  <AlertDescription>
                    This funnel is currently {selectedFunnel.is_active ? 'active' : 'inactive'} and 
                    {selectedFunnel.mautic_campaign_id ? ' synced with Mautic' : ' not synced with Mautic'}.
                    {selectedFunnel.is_active && ' New leads will automatically enter this funnel.'}
                  </AlertDescription>
                </Alert>
              </div>
            </TabsContent>

            <TabsContent value="analytics">
              <FunnelAnalytics funnel={selectedFunnel} />
            </TabsContent>

            <TabsContent value="stages">
              <div className="space-y-4">
                {selectedFunnel.stages.map((stage, index) => (
                  <Card key={stage.id}>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2">
                          Stage {index + 1}: {stage.name}
                          <Badge variant={stage.is_active ? "default" : "secondary"}>
                            {stage.is_active ? "Active" : "Inactive"}
                          </Badge>
                        </CardTitle>
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm">
                            <Edit3 className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Settings className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                      <CardDescription>{stage.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div>
                            <Label className="text-sm font-medium">Stage Type</Label>
                            <p className="text-sm text-gray-600 capitalize">
                              {stage.stage_type.replace('_', ' ')}
                            </p>
                          </div>
                          <div>
                            <Label className="text-sm font-medium">Email Templates</Label>
                            <p className="text-sm text-gray-600">
                              {stage.email_templates.length} template(s)
                            </p>
                          </div>
                          <div>
                            <Label className="text-sm font-medium">Delay</Label>
                            <p className="text-sm text-gray-600">
                              {stage.delay_before_action ? `${stage.delay_before_action / 60} hours` : 'No delay'}
                            </p>
                          </div>
                        </div>
                        
                        {selectedFunnel.performance && (
                          <div>
                            <Label className="text-sm font-medium">Conversion Rate</Label>
                            <Progress 
                              value={selectedFunnel.performance.stage_conversion_rates[stage.id] || 0} 
                              className="h-3 mt-2"
                            />
                            <p className="text-sm text-gray-600 mt-1">
                              {selectedFunnel.performance.stage_conversion_rates[stage.id]?.toFixed(1) || 0}%
                            </p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="emails">
              <div className="space-y-4">
                {selectedFunnel.stages.map((stage) => 
                  stage.email_templates.map((template) => (
                    <Card key={template.id}>
                      <CardHeader>
                        <div className="flex items-center justify-between">
                          <CardTitle className="flex items-center gap-2">
                            <Mail className="w-5 h-5" />
                            {template.name}
                          </CardTitle>
                          <div className="flex items-center space-x-2">
                            <Button variant="ghost" size="sm">
                              <Edit3 className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Send className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                        <CardDescription>
                          Stage: {stage.name} • 
                          Delay: {template.delay_hours ? `${template.delay_hours} hours` : 'Immediate'}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div>
                            <Label className="text-sm font-medium">Subject Line</Label>
                            <p className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                              {template.subject}
                            </p>
                          </div>
                          
                          <div>
                            <Label className="text-sm font-medium">Preview</Label>
                            <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded max-h-32 overflow-y-auto">
                              <div dangerouslySetInnerHTML={{ 
                                __html: template.html_content.substring(0, 200) + '...' 
                              }} />
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </TabsContent>

            <TabsContent value="automation">
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Zap className="w-5 h-5" />
                      Automation Rules
                    </CardTitle>
                    <CardDescription>
                      Configure triggers and actions for this funnel
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <Alert>
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Mautic Integration</AlertTitle>
                        <AlertDescription>
                          This funnel is connected to Mautic campaign ID: {selectedFunnel.mautic_campaign_id}
                        </AlertDescription>
                      </Alert>
                      
                      <div className="text-center py-8">
                        <p className="text-gray-500">
                          Automation rules will be displayed here
                        </p>
                        <Button className="mt-4">
                          <Plus className="w-4 h-4 mr-2" />
                          Add Automation Rule
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="settings">
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Funnel Settings</CardTitle>
                    <CardDescription>
                      Configure funnel behavior and integration settings
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label>Funnel Status</Label>
                        <p className="text-sm text-gray-600">
                          Enable or disable this funnel
                        </p>
                      </div>
                      <Switch 
                        checked={selectedFunnel.is_active}
                        onCheckedChange={() => handleToggleFunnelStatus(selectedFunnel.id)}
                      />
                    </div>

                    <Separator />

                    <div className="space-y-4">
                      <Label>Mautic Integration</Label>
                      <div className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <p className="font-medium">Campaign ID</p>
                          <p className="text-sm text-gray-600">
                            {selectedFunnel.mautic_campaign_id || 'Not connected'}
                          </p>
                        </div>
                        <Button variant="outline" size="sm">
                          {selectedFunnel.mautic_campaign_id ? 'Update' : 'Connect'}
                        </Button>
                      </div>
                    </div>

                    <Separator />

                    <div className="flex items-center space-x-2">
                      <Button variant="destructive" size="sm">
                        <Trash2 className="w-4 h-4 mr-2" />
                        Delete Funnel
                      </Button>
                      <Button variant="outline" size="sm">
                        <Download className="w-4 h-4 mr-2" />
                        Export
                      </Button>
                      <Button variant="outline" size="sm">
                        <Upload className="w-4 h-4 mr-2" />
                        Import
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      ) : (
        // Funnel List View
        <div className="space-y-6">
          {filteredFunnels.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Mail className="w-12 h-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900">No funnels found</h3>
                <p className="text-gray-600 text-center mb-6">
                  {searchTerm || statusFilter !== 'all' 
                    ? 'No funnels match your current filters.' 
                    : 'Create your first sales funnel to get started with email automation.'
                  }
                </p>
                <div className="flex items-center space-x-3">
                  <Button onClick={() => setIsTemplateDialogOpen(true)} variant="outline">
                    Browse Templates
                  </Button>
                  <Button onClick={() => setIsCreateDialogOpen(true)}>
                    Create Funnel
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {filteredFunnels.map((funnel) => (
                <FunnelCard key={funnel.id} funnel={funnel} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}