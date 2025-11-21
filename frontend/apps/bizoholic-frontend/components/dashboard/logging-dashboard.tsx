'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ScrollArea } from "@/components/ui/scroll-area"
import { 
  Activity,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  Database,
  Server,
  Cpu,
  AlertCircle,
  RefreshCw,
  Search,
  Filter,
  Download,
  FileText,
  TrendingUp,
  TrendingDown,
  BarChart3,
  PieChart,
  Eye,
  Calendar,
  Users,
  Shield,
  Zap,
  Bug,
  Info
} from 'lucide-react'

interface LogEntry {
  timestamp: string
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL' | 'AUDIT'
  category: string
  service: string
  message: string
  details?: any
  user_id?: string
  tenant_id?: string
  session_id?: string
  trace_id?: string
  error_details?: any
  performance_metrics?: any
}

interface LogStats {
  total_logs_today: number
  error_count_today: number
  warning_count_today: number
  categories: Record<string, number>
  services: Record<string, number>
  top_errors: string[]
}

export function LoggingDashboard() {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [stats, setStats] = useState<LogStats>({
    total_logs_today: 0,
    error_count_today: 0,
    warning_count_today: 0,
    categories: {},
    services: {},
    top_errors: []
  })
  const [selectedLevel, setSelectedLevel] = useState('all')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedService, setSelectedService] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  // Mock data - in real implementation, this would come from the logging API
  useEffect(() => {
    const mockStats: LogStats = {
      total_logs_today: 12847,
      error_count_today: 23,
      warning_count_today: 156,
      categories: {
        'system': 4523,
        'agent': 3421,
        'api': 2856,
        'database': 987,
        'auth': 654,
        'payment': 234,
        'integration': 172
      },
      services: {
        'crewai-agents': 3421,
        'bizosaas-frontend': 2856,
        'agent-monitor': 2103,
        'coreldove-sourcing': 1876,
        'temporal-worker': 1542,
        'vault-service': 987
      },
      top_errors: [
        'Database connection timeout',
        'API rate limit exceeded',
        'Agent task timeout',
        'Authentication failure'
      ]
    }

    const mockLogs: LogEntry[] = [
      {
        timestamp: '2024-08-26T11:15:00Z',
        level: 'ERROR',
        category: 'agent',
        service: 'crewai-agents',
        message: 'Marketing campaign agent failed to complete optimization task',
        details: { campaign_id: 'camp_123', error_type: 'timeout' },
        tenant_id: 'tenant_001',
        error_details: { exception_type: 'TimeoutError', exception_message: 'Task timeout after 300s' }
      },
      {
        timestamp: '2024-08-26T11:14:45Z',
        level: 'INFO',
        category: 'api',
        service: 'bizosaas-frontend',
        message: 'User successfully logged in',
        details: { endpoint: '/api/auth/login', method: 'POST' },
        user_id: 'user_456',
        tenant_id: 'tenant_001',
        performance_metrics: { duration_seconds: 0.245 }
      },
      {
        timestamp: '2024-08-26T11:14:30Z',
        level: 'WARNING',
        category: 'database',
        service: 'agent-monitor',
        message: 'Database connection pool nearing capacity',
        details: { active_connections: 145, max_connections: 200 },
        performance_metrics: { connection_utilization: 72.5 }
      },
      {
        timestamp: '2024-08-26T11:14:15Z',
        level: 'INFO',
        category: 'workflow',
        service: 'temporal-worker',
        message: 'Workflow execution completed successfully',
        details: { workflow_id: 'product-research-001', workflow_type: 'ProductResearchWorkflow' },
        performance_metrics: { duration_seconds: 145.2, success: true }
      },
      {
        timestamp: '2024-08-26T11:14:00Z',
        level: 'CRITICAL',
        category: 'security',
        service: 'vault-service',
        message: 'Multiple failed authentication attempts detected',
        details: { ip_address: '192.168.1.100', attempts: 5, time_window: '5min' },
        user_id: 'unknown',
        error_details: { security_threat: 'brute_force_attempt' }
      },
      {
        timestamp: '2024-08-26T11:13:45Z',
        level: 'INFO',
        category: 'integration',
        service: 'coreldove-sourcing',
        message: 'Successfully retrieved products from Amazon PA API',
        details: { products_found: 45, search_terms: 'smartphone accessories' },
        performance_metrics: { api_response_time: 1.2, products_processed: 45 }
      }
    ]

    setStats(mockStats)
    setLogs(mockLogs)
    setIsLoading(false)
  }, [])

  const filteredLogs = logs.filter(log => {
    const matchesLevel = selectedLevel === 'all' || log.level === selectedLevel
    const matchesCategory = selectedCategory === 'all' || log.category === selectedCategory
    const matchesService = selectedService === 'all' || log.service === selectedService
    const matchesSearch = searchTerm === '' || 
      log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.service.toLowerCase().includes(searchTerm.toLowerCase())
    
    return matchesLevel && matchesCategory && matchesService && matchesSearch
  })

  const getLevelBadge = (level: string) => {
    const variants = {
      'DEBUG': 'secondary' as const,
      'INFO': 'default' as const,
      'WARNING': 'outline' as const,
      'ERROR': 'destructive' as const,
      'CRITICAL': 'destructive' as const,
      'AUDIT': 'secondary' as const
    }
    
    return (
      <Badge variant={variants[level as keyof typeof variants]} className="text-xs">
        {level}
      </Badge>
    )
  }

  const getLevelIcon = (level: string) => {
    switch (level) {
      case 'DEBUG': return <Bug className="h-3 w-3 text-gray-500" />
      case 'INFO': return <Info className="h-3 w-3 text-blue-500" />
      case 'WARNING': return <AlertTriangle className="h-3 w-3 text-yellow-500" />
      case 'ERROR': return <XCircle className="h-3 w-3 text-red-500" />
      case 'CRITICAL': return <AlertCircle className="h-3 w-3 text-red-700" />
      case 'AUDIT': return <Shield className="h-3 w-3 text-purple-500" />
      default: return <Clock className="h-3 w-3 text-gray-500" />
    }
  }

  const getCategoryIcon = (category: string) => {
    const icons = {
      'system': Server,
      'agent': Zap,
      'api': Activity,
      'database': Database,
      'auth': Shield,
      'payment': CheckCircle,
      'integration': PieChart,
      'workflow': BarChart3,
      'security': Shield,
      'performance': TrendingUp
    }
    const Icon = icons[category as keyof typeof icons] || FileText
    return <Icon className="h-4 w-4" />
  }

  const handleRefresh = () => {
    setIsLoading(true)
    // In real implementation, this would fetch fresh data
    setTimeout(() => setIsLoading(false), 1000)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <RefreshCw className="h-8 w-8 animate-spin" />
        <span className="ml-2">Loading logs...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">Centralized Logging Dashboard</h3>
          <p className="text-sm text-muted-foreground">
            Monitor system activity, errors, and performance across all services
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleRefresh}>
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Logs Today</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_logs_today.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="h-3 w-3 inline mr-1 text-green-600" />
              <span className="text-green-600">+12%</span> vs yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Errors Today</CardTitle>
            <XCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{stats.error_count_today}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingDown className="h-3 w-3 inline mr-1 text-green-600" />
              <span className="text-green-600">-8%</span> vs yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Warnings Today</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">{stats.warning_count_today}</div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="h-3 w-3 inline mr-1 text-yellow-600" />
              <span className="text-yellow-600">+3%</span> vs yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {((stats.total_logs_today - stats.error_count_today) / stats.total_logs_today * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="h-3 w-3 inline mr-1 text-green-600" />
              System reliability
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="logs" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="logs">Live Logs</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="errors">Error Analysis</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
        </TabsList>

        <TabsContent value="logs" className="space-y-4">
          {/* Filters */}
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center gap-2 flex-1">
              <Search className="h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search logs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="max-w-sm"
              />
            </div>
            
            <Select value={selectedLevel} onValueChange={setSelectedLevel}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Level" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Levels</SelectItem>
                <SelectItem value="DEBUG">Debug</SelectItem>
                <SelectItem value="INFO">Info</SelectItem>
                <SelectItem value="WARNING">Warning</SelectItem>
                <SelectItem value="ERROR">Error</SelectItem>
                <SelectItem value="CRITICAL">Critical</SelectItem>
                <SelectItem value="AUDIT">Audit</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-36">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="system">System</SelectItem>
                <SelectItem value="agent">Agent</SelectItem>
                <SelectItem value="api">API</SelectItem>
                <SelectItem value="database">Database</SelectItem>
                <SelectItem value="auth">Auth</SelectItem>
                <SelectItem value="workflow">Workflow</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedService} onValueChange={setSelectedService}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Service" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Services</SelectItem>
                <SelectItem value="crewai-agents">CrewAI Agents</SelectItem>
                <SelectItem value="bizosaas-frontend">Frontend</SelectItem>
                <SelectItem value="agent-monitor">Agent Monitor</SelectItem>
                <SelectItem value="temporal-worker">Temporal Worker</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Log Entries */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Live Log Stream</CardTitle>
              <CardDescription>
                Showing {filteredLogs.length} of {logs.length} log entries
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ScrollArea className="h-[600px]">
                <div className="space-y-2">
                  {filteredLogs.map((log, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 rounded-lg border bg-card/50 hover:bg-card">
                      <div className="flex-shrink-0 mt-1">
                        {getLevelIcon(log.level)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex items-center space-x-2">
                            {getLevelBadge(log.level)}
                            <Badge variant="outline" className="text-xs">
                              {getCategoryIcon(log.category)}
                              <span className="ml-1">{log.category}</span>
                            </Badge>
                            <span className="text-xs text-muted-foreground">{log.service}</span>
                          </div>
                          <span className="text-xs text-muted-foreground">
                            {new Date(log.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-sm font-medium mb-1">{log.message}</p>
                        {log.details && (
                          <div className="text-xs text-muted-foreground bg-muted/50 p-2 rounded">
                            <pre className="whitespace-pre-wrap font-mono">
                              {JSON.stringify(log.details, null, 2)}
                            </pre>
                          </div>
                        )}
                        {log.error_details && (
                          <Alert className="mt-2 border-red-200">
                            <AlertTriangle className="h-4 w-4" />
                            <AlertDescription className="text-sm">
                              <strong>{log.error_details.exception_type}:</strong> {log.error_details.exception_message}
                            </AlertDescription>
                          </Alert>
                        )}
                        {log.performance_metrics && (
                          <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                            {log.performance_metrics.duration_seconds && (
                              <span>⏱ {log.performance_metrics.duration_seconds}s</span>
                            )}
                            {log.performance_metrics.success !== undefined && (
                              <span className={log.performance_metrics.success ? 'text-green-600' : 'text-red-600'}>
                                {log.performance_metrics.success ? '✓' : '✗'} 
                                {log.performance_metrics.success ? 'Success' : 'Failed'}
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Log Distribution by Category</CardTitle>
                <CardDescription>Breakdown of logs by category over the last 24 hours</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(stats.categories).map(([category, count]) => (
                    <div key={category} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {getCategoryIcon(category)}
                        <span className="text-sm capitalize">{category}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-sm font-medium">{count.toLocaleString()}</span>
                        <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-600 rounded-full"
                            style={{ width: `${(count / stats.total_logs_today) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Active Services</CardTitle>
                <CardDescription>Log volume by service in the last 24 hours</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(stats.services).map(([service, count]) => (
                    <div key={service} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <Server className="h-4 w-4" />
                        <span className="text-sm">{service}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-sm font-medium">{count.toLocaleString()}</span>
                        <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-600 rounded-full"
                            style={{ width: `${(count / stats.total_logs_today) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="errors" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <XCircle className="h-5 w-5 text-red-500 mr-2" />
                Error Analysis
              </CardTitle>
              <CardDescription>Most common errors and their frequency</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {stats.top_errors.map((error, index) => (
                  <Alert key={index} className="border-red-200">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      <div className="flex items-center justify-between">
                        <span>{error}</span>
                        <Badge variant="destructive">#{index + 1}</Badge>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="performance" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Avg Response Time</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">145ms</div>
                <p className="text-xs text-muted-foreground">
                  <TrendingDown className="h-3 w-3 inline mr-1 text-green-600" />
                  <span className="text-green-600">-12ms</span> vs yesterday
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Throughput</CardTitle>
                <BarChart3 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">2.4k/min</div>
                <p className="text-xs text-muted-foreground">
                  <TrendingUp className="h-3 w-3 inline mr-1 text-green-600" />
                  <span className="text-green-600">+15%</span> vs yesterday
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">System Load</CardTitle>
                <Cpu className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">45%</div>
                <p className="text-xs text-muted-foreground">
                  <Activity className="h-3 w-3 inline mr-1" />
                  Normal range
                </p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}