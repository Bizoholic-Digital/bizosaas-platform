'use client'

import { useState, useEffect } from 'react'
import { DayPicker } from 'react-day-picker'
import { format, addHours, isWithinInterval, isPast, isFuture } from 'date-fns'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea'
import { Switch } from '@/components/ui/switch'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Settings, AlertTriangle, Clock, Server, Database, Wrench, Plus, Activity, Zap } from 'lucide-react'
import { useApiGatewayDashboard } from '@/hooks/use-api-gateway'
import { useAIAgentsData } from '@/hooks/use-ai-agents-live'

// Types for maintenance windows
interface MaintenanceWindow {
  id: string
  title: string
  description: string
  start_time: Date
  end_time: Date
  maintenance_type: 'scheduled' | 'emergency' | 'security' | 'upgrade' | 'optimization'
  affected_services: string[]
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'planned' | 'in_progress' | 'completed' | 'cancelled'
  impact_level: 'none' | 'minimal' | 'moderate' | 'high'
  requires_downtime: boolean
  estimated_downtime: number // in minutes
  notification_sent: boolean
  rollback_plan: string
  completion_notes?: string
  affected_tenants: string[]
  assigned_engineer: string
  approval_required: boolean
  approved_by?: string
  client_communication: boolean
}

interface MaintenanceWindowsProps {
  className?: string
  showOnlyUpcoming?: boolean
}

export function MaintenanceWindows({ className, showOnlyUpcoming = false }: MaintenanceWindowsProps) {
  const [selected, setSelected] = useState<Date | undefined>(new Date())
  const [maintenanceWindows, setMaintenanceWindows] = useState<MaintenanceWindow[]>([])
  const [isScheduling, setIsScheduling] = useState(false)
  const [selectedWindow, setSelectedWindow] = useState<MaintenanceWindow | null>(null)
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [newWindow, setNewWindow] = useState<Partial<MaintenanceWindow>>({
    title: '',
    description: '',
    maintenance_type: 'scheduled',
    severity: 'medium',
    impact_level: 'minimal',
    requires_downtime: false,
    estimated_downtime: 0,
    approval_required: true,
    client_communication: true
  })

  const { data: gatewayData } = useApiGatewayDashboard()
  const { data: agentsData } = useAIAgentsData()

  // Available services for maintenance
  const availableServices = [
    'API Gateway',
    'AI Agents',
    'Authentication Service',
    'Database (PostgreSQL)',
    'Cache (Redis)',
    'Frontend Applications',
    'Payment Service',
    'Email Service',
    'File Storage',
    'Monitoring System',
    'Wagtail CMS',
    'Saleor E-commerce'
  ]

  // Mock data for maintenance windows
  useEffect(() => {
    const mockWindows: MaintenanceWindow[] = [
      {
        id: '1',
        title: 'Database Performance Optimization',
        description: 'Upgrade PostgreSQL version and optimize indexes for better performance',
        start_time: addHours(new Date(), 48),
        end_time: addHours(new Date(), 50),
        maintenance_type: 'optimization',
        affected_services: ['Database (PostgreSQL)', 'API Gateway', 'AI Agents'],
        severity: 'medium',
        status: 'planned',
        impact_level: 'moderate',
        requires_downtime: true,
        estimated_downtime: 30,
        notification_sent: false,
        rollback_plan: 'Restore from backup and switch to previous PostgreSQL version',
        affected_tenants: ['tenant_1', 'tenant_2', 'tenant_3'],
        assigned_engineer: 'John Smith',
        approval_required: true,
        client_communication: true
      },
      {
        id: '2',
        title: 'Security Patch Deployment',
        description: 'Deploy critical security patches for all services',
        start_time: addHours(new Date(), 72),
        end_time: addHours(new Date(), 73),
        maintenance_type: 'security',
        affected_services: ['API Gateway', 'Authentication Service', 'Frontend Applications'],
        severity: 'high',
        status: 'planned',
        impact_level: 'minimal',
        requires_downtime: false,
        estimated_downtime: 0,
        notification_sent: false,
        rollback_plan: 'Revert to previous container images',
        affected_tenants: ['tenant_1', 'tenant_2', 'tenant_3', 'tenant_4'],
        assigned_engineer: 'Sarah Wilson',
        approval_required: true,
        approved_by: 'Mike Johnson',
        client_communication: true
      },
      {
        id: '3',
        title: 'AI Agents Service Upgrade',
        description: 'Upgrade AI agents to latest version with new capabilities',
        start_time: addHours(new Date(), 120),
        end_time: addHours(new Date(), 124),
        maintenance_type: 'upgrade',
        affected_services: ['AI Agents', 'API Gateway'],
        severity: 'low',
        status: 'planned',
        impact_level: 'minimal',
        requires_downtime: false,
        estimated_downtime: 0,
        notification_sent: false,
        rollback_plan: 'Rollback to previous AI agents version',
        affected_tenants: [],
        assigned_engineer: 'Emily Davis',
        approval_required: false,
        client_communication: false
      }
    ]
    setMaintenanceWindows(mockWindows)
  }, [])

  // Filter windows based on status and upcoming flag
  const filteredWindows = maintenanceWindows.filter(window => {
    if (showOnlyUpcoming && isPast(window.start_time)) return false
    if (filterStatus !== 'all' && window.status !== filterStatus) return false
    return true
  })

  // Get windows for selected date
  const selectedDateWindows = filteredWindows.filter(window => 
    selected && (
      format(window.start_time, 'yyyy-MM-dd') === format(selected, 'yyyy-MM-dd') ||
      format(window.end_time, 'yyyy-MM-dd') === format(selected, 'yyyy-MM-dd') ||
      isWithinInterval(selected, { start: window.start_time, end: window.end_time })
    )
  )

  const handleScheduleWindow = () => {
    if (!newWindow.title || !newWindow.description || !selected) return

    // Calculate start and end times
    const startTime = new Date(selected)
    startTime.setHours(2, 0, 0, 0) // Default to 2 AM (low traffic time)
    
    const endTime = new Date(startTime)
    endTime.setHours(4, 0, 0, 0) // Default 2-hour window

    const window: MaintenanceWindow = {
      id: Math.random().toString(36).substr(2, 9),
      title: newWindow.title!,
      description: newWindow.description!,
      start_time: startTime,
      end_time: endTime,
      maintenance_type: newWindow.maintenance_type || 'scheduled',
      affected_services: newWindow.affected_services || [],
      severity: newWindow.severity || 'medium',
      status: 'planned',
      impact_level: newWindow.impact_level || 'minimal',
      requires_downtime: newWindow.requires_downtime || false,
      estimated_downtime: newWindow.estimated_downtime || 0,
      notification_sent: false,
      rollback_plan: newWindow.rollback_plan || 'TBD',
      affected_tenants: [],
      assigned_engineer: 'Unassigned',
      approval_required: newWindow.approval_required !== false,
      client_communication: newWindow.client_communication !== false
    }

    setMaintenanceWindows([...maintenanceWindows, window])
    setNewWindow({
      title: '',
      description: '',
      maintenance_type: 'scheduled',
      severity: 'medium',
      impact_level: 'minimal',
      requires_downtime: false,
      estimated_downtime: 0,
      approval_required: true,
      client_communication: true
    })
    setIsScheduling(false)
  }

  const getTypeColor = (type: string) => {
    const colors = {
      scheduled: 'bg-blue-500',
      emergency: 'bg-red-500',
      security: 'bg-orange-500',
      upgrade: 'bg-green-500',
      optimization: 'bg-purple-500'
    }
    return colors[type as keyof typeof colors] || 'bg-gray-500'
  }

  const getSeverityColor = (severity: string) => {
    const colors = {
      low: 'border-l-green-500',
      medium: 'border-l-yellow-500',
      high: 'border-l-orange-500',
      critical: 'border-l-red-500'
    }
    return colors[severity as keyof typeof colors] || 'border-l-gray-500'
  }

  const getImpactColor = (impact: string) => {
    const colors = {
      none: 'text-green-600',
      minimal: 'text-blue-600',
      moderate: 'text-yellow-600',
      high: 'text-red-600'
    }
    return colors[impact as keyof typeof colors] || 'text-gray-600'
  }

  const getStatusIcon = (status: string) => {
    const icons = {
      planned: <Clock className="h-4 w-4" />,
      in_progress: <Activity className="h-4 w-4" />,
      completed: <Wrench className="h-4 w-4" />,
      cancelled: <AlertTriangle className="h-4 w-4" />
    }
    return icons[status as keyof typeof icons] || <Clock className="h-4 w-4" />
  }

  // Get days with maintenance windows for calendar highlighting
  const maintenanceDays = filteredWindows.flatMap(window => [window.start_time, window.end_time])

  // Check for upcoming critical maintenance
  const upcomingCritical = maintenanceWindows.filter(window => 
    window.severity === 'critical' && 
    isFuture(window.start_time) &&
    window.status === 'planned'
  )

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Critical Maintenance Alert */}
      {upcomingCritical.length > 0 && (
        <Alert className="border-red-200">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>Critical Maintenance Scheduled:</strong> {upcomingCritical.length} critical maintenance window(s) scheduled. 
            Review and ensure proper communication to all affected clients.
          </AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Maintenance Windows
              </CardTitle>
              <CardDescription>
                Schedule and manage system maintenance, updates, and downtime windows
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-[120px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="planned">Planned</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                </SelectContent>
              </Select>
              <Dialog open={isScheduling} onOpenChange={setIsScheduling}>
                <DialogTrigger asChild>
                  <Button size="sm" className="gap-2">
                    <Plus className="h-4 w-4" />
                    Schedule Maintenance
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>Schedule Maintenance Window</DialogTitle>
                    <DialogDescription>
                      Plan system maintenance for {selected && format(selected, 'PPP')}
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4 max-h-[60vh] overflow-y-auto">
                    <div className="grid gap-2">
                      <Label htmlFor="title">Maintenance Title</Label>
                      <Input
                        id="title"
                        value={newWindow.title}
                        onChange={(e) => setNewWindow({ ...newWindow, title: e.target.value })}
                        placeholder="Enter maintenance title..."
                      />
                    </div>
                    
                    <div className="grid gap-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        value={newWindow.description}
                        onChange={(e) => setNewWindow({ ...newWindow, description: e.target.value })}
                        placeholder="Describe what maintenance will be performed..."
                        rows={3}
                      />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label>Maintenance Type</Label>
                        <Select
                          value={newWindow.maintenance_type}
                          onValueChange={(value) => setNewWindow({ ...newWindow, maintenance_type: value as any })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="scheduled">Scheduled</SelectItem>
                            <SelectItem value="emergency">Emergency</SelectItem>
                            <SelectItem value="security">Security</SelectItem>
                            <SelectItem value="upgrade">Upgrade</SelectItem>
                            <SelectItem value="optimization">Optimization</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid gap-2">
                        <Label>Severity</Label>
                        <Select
                          value={newWindow.severity}
                          onValueChange={(value) => setNewWindow({ ...newWindow, severity: value as any })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="low">Low</SelectItem>
                            <SelectItem value="medium">Medium</SelectItem>
                            <SelectItem value="high">High</SelectItem>
                            <SelectItem value="critical">Critical</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    
                    <div className="grid gap-2">
                      <Label>Affected Services</Label>
                      <div className="grid grid-cols-2 gap-2 max-h-32 overflow-y-auto">
                        {availableServices.map((service) => (
                          <label key={service} className="flex items-center space-x-2">
                            <input
                              type="checkbox"
                              checked={newWindow.affected_services?.includes(service)}
                              onChange={(e) => {
                                const services = newWindow.affected_services || []
                                if (e.target.checked) {
                                  setNewWindow({ ...newWindow, affected_services: [...services, service] })
                                } else {
                                  setNewWindow({ 
                                    ...newWindow, 
                                    affected_services: services.filter(s => s !== service) 
                                  })
                                }
                              }}
                              className="rounded"
                            />
                            <span className="text-sm">{service}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label>Impact Level</Label>
                        <Select
                          value={newWindow.impact_level}
                          onValueChange={(value) => setNewWindow({ ...newWindow, impact_level: value as any })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="none">None</SelectItem>
                            <SelectItem value="minimal">Minimal</SelectItem>
                            <SelectItem value="moderate">Moderate</SelectItem>
                            <SelectItem value="high">High</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="downtime">Est. Downtime (min)</Label>
                        <Input
                          id="downtime"
                          type="number"
                          value={newWindow.estimated_downtime}
                          onChange={(e) => setNewWindow({ ...newWindow, estimated_downtime: parseInt(e.target.value) })}
                          min="0"
                          max="480"
                        />
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="downtime_required"
                          checked={newWindow.requires_downtime}
                          onCheckedChange={(checked) => setNewWindow({ ...newWindow, requires_downtime: checked })}
                        />
                        <Label htmlFor="downtime_required">Requires System Downtime</Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="approval_required"
                          checked={newWindow.approval_required}
                          onCheckedChange={(checked) => setNewWindow({ ...newWindow, approval_required: checked })}
                        />
                        <Label htmlFor="approval_required">Requires Management Approval</Label>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Switch
                          id="client_communication"
                          checked={newWindow.client_communication}
                          onCheckedChange={(checked) => setNewWindow({ ...newWindow, client_communication: checked })}
                        />
                        <Label htmlFor="client_communication">Notify Clients</Label>
                      </div>
                    </div>
                    
                    <div className="grid gap-2">
                      <Label htmlFor="rollback">Rollback Plan</Label>
                      <Textarea
                        id="rollback"
                        value={newWindow.rollback_plan}
                        onChange={(e) => setNewWindow({ ...newWindow, rollback_plan: e.target.value })}
                        placeholder="Describe rollback procedure if maintenance fails..."
                        rows={2}
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button type="submit" onClick={handleScheduleWindow}>
                      Schedule Maintenance
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Calendar */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">
                {format(selected || new Date(), 'MMMM yyyy')}
              </h3>
              
              <DayPicker
                mode="single"
                selected={selected}
                onSelect={setSelected}
                className="rounded-md border"
                modifiers={{
                  hasMaintenance: maintenanceDays,
                  today: new Date()
                }}
                modifiersClassNames={{
                  hasMaintenance: 'bg-orange-100 font-bold',
                  today: 'bg-accent'
                }}
              />
            </div>

            {/* Maintenance Windows for Selected Date */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">
                Maintenance for {selected ? format(selected, 'PPP') : 'Select a date'}
              </h3>
              
              {selectedDateWindows.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <Settings className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No maintenance scheduled for this date</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {selectedDateWindows
                    .sort((a, b) => a.start_time.getTime() - b.start_time.getTime())
                    .map((window) => (
                      <Card
                        key={window.id}
                        className={`cursor-pointer hover:shadow-md transition-shadow border-l-4 ${getSeverityColor(window.severity)}`}
                        onClick={() => setSelectedWindow(window)}
                      >
                        <CardContent className="p-4">
                          <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-2">
                              <Badge className={`${getTypeColor(window.maintenance_type)} text-white`}>
                                {window.maintenance_type}
                              </Badge>
                              <Badge variant="outline">
                                {window.severity.toUpperCase()}
                              </Badge>
                              {window.requires_downtime && (
                                <Badge variant="destructive">
                                  <AlertTriangle className="h-3 w-3 mr-1" />
                                  Downtime
                                </Badge>
                              )}
                            </div>
                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                              {getStatusIcon(window.status)}
                              {window.status}
                            </div>
                          </div>
                          
                          <h4 className="font-semibold text-sm">{window.title}</h4>
                          <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                            {window.description}
                          </p>
                          
                          <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {format(window.start_time, 'HH:mm')} - {format(window.end_time, 'HH:mm')}
                            </div>
                            <div className="flex items-center gap-1">
                              <Server className="h-3 w-3" />
                              {window.affected_services.length} services
                            </div>
                            <div className={`flex items-center gap-1 ${getImpactColor(window.impact_level)}`}>
                              <Zap className="h-3 w-3" />
                              {window.impact_level} impact
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                </div>
              )}
            </div>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{filteredWindows.length}</div>
              <div className="text-xs text-muted-foreground">Total Windows</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {filteredWindows.filter(w => w.status === 'planned').length}
              </div>
              <div className="text-xs text-muted-foreground">Planned</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {filteredWindows.filter(w => w.requires_downtime).length}
              </div>
              <div className="text-xs text-muted-foreground">With Downtime</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {filteredWindows.filter(w => w.severity === 'critical').length}
              </div>
              <div className="text-xs text-muted-foreground">Critical</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Maintenance Window Details Dialog */}
      {selectedWindow && (
        <Dialog open={!!selectedWindow} onOpenChange={() => setSelectedWindow(null)}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                {getStatusIcon(selectedWindow.status)}
                {selectedWindow.title}
              </DialogTitle>
              <DialogDescription>
                {format(selectedWindow.start_time, 'PPP p')} - {format(selectedWindow.end_time, 'p')}
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Type</h4>
                  <Badge className={`${getTypeColor(selectedWindow.maintenance_type)} text-white`}>
                    {selectedWindow.maintenance_type}
                  </Badge>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Severity</h4>
                  <Badge variant="outline">{selectedWindow.severity.toUpperCase()}</Badge>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-1">Description</h4>
                <p className="text-sm text-muted-foreground">{selectedWindow.description}</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Impact Level</h4>
                  <p className={`text-sm ${getImpactColor(selectedWindow.impact_level)} capitalize`}>
                    {selectedWindow.impact_level}
                  </p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Estimated Downtime</h4>
                  <p className="text-sm">
                    {selectedWindow.estimated_downtime > 0 
                      ? `${selectedWindow.estimated_downtime} minutes`
                      : 'No downtime expected'
                    }
                  </p>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-1">Affected Services</h4>
                <div className="flex flex-wrap gap-1">
                  {selectedWindow.affected_services.map((service) => (
                    <Badge key={service} variant="secondary" className="text-xs">
                      {service}
                    </Badge>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-1">Rollback Plan</h4>
                <p className="text-sm text-muted-foreground">{selectedWindow.rollback_plan}</p>
              </div>
              
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <h4 className="font-medium mb-1">Approval Required</h4>
                  <p className={selectedWindow.approval_required ? 'text-yellow-600' : 'text-green-600'}>
                    {selectedWindow.approval_required ? 'Yes' : 'No'}
                  </p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Client Communication</h4>
                  <p className={selectedWindow.client_communication ? 'text-blue-600' : 'text-gray-600'}>
                    {selectedWindow.client_communication ? 'Required' : 'Not needed'}
                  </p>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Assigned Engineer</h4>
                  <p className="text-muted-foreground">{selectedWindow.assigned_engineer}</p>
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setSelectedWindow(null)}>
                Close
              </Button>
              <Button>Edit Maintenance</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}