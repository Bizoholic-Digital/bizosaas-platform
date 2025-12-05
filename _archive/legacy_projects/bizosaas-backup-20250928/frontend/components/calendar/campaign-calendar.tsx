'use client'

import { useState, useEffect } from 'react'
import { DayPicker } from 'react-day-picker'
import { format, addDays, isToday, isBefore, isAfter } from 'date-fns'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { CalendarDays, Plus, Clock, Users, Target, TrendingUp } from 'lucide-react'
import { useApiGatewayDashboard } from '@/hooks/use-api-gateway'

// Types for campaign scheduling
interface CampaignEvent {
  id: string
  title: string
  description?: string
  date: Date
  type: 'launch' | 'review' | 'optimization' | 'completion' | 'milestone'
  tier: 'tier_1' | 'tier_2' | 'tier_3'
  tenant_id: string
  assigned_agents: string[]
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled'
  estimated_duration: number // in hours
  priority: 'low' | 'medium' | 'high' | 'critical'
}

interface CampaignCalendarProps {
  tenantId?: string
  tier?: 'tier_1' | 'tier_2' | 'tier_3'
  className?: string
}

export function CampaignCalendar({ tenantId, tier, className }: CampaignCalendarProps) {
  const [selected, setSelected] = useState<Date | undefined>(new Date())
  const [events, setEvents] = useState<CampaignEvent[]>([])
  const [isAddingEvent, setIsAddingEvent] = useState(false)
  const [selectedEvent, setSelectedEvent] = useState<CampaignEvent | null>(null)
  const [newEvent, setNewEvent] = useState<Partial<CampaignEvent>>({
    title: '',
    description: '',
    type: 'launch',
    tier: tier || 'tier_1',
    priority: 'medium',
    estimated_duration: 2
  })

  const { data: gatewayData } = useApiGatewayDashboard()

  // Mock data - replace with real API call
  useEffect(() => {
    const mockEvents: CampaignEvent[] = [
      {
        id: '1',
        title: 'Product Launch Campaign',
        description: 'Launch new product line with full marketing automation',
        date: addDays(new Date(), 2),
        type: 'launch',
        tier: 'tier_3',
        tenant_id: 'tenant_1',
        assigned_agents: ['marketing-strategist', 'content-creator', 'seo-optimizer'],
        status: 'scheduled',
        estimated_duration: 8,
        priority: 'high'
      },
      {
        id: '2',
        title: 'Campaign Performance Review',
        description: 'Weekly review of ongoing campaigns',
        date: addDays(new Date(), 5),
        type: 'review',
        tier: 'tier_2',
        tenant_id: 'tenant_2',
        assigned_agents: ['analytics-expert', 'performance-optimizer'],
        status: 'scheduled',
        estimated_duration: 2,
        priority: 'medium'
      },
      {
        id: '3',
        title: 'SEO Optimization Sprint',
        description: 'Complete SEO audit and implementation',
        date: addDays(new Date(), 7),
        type: 'optimization',
        tier: 'tier_1',
        tenant_id: 'tenant_3',
        assigned_agents: ['seo-optimizer', 'technical-seo'],
        status: 'scheduled',
        estimated_duration: 6,
        priority: 'medium'
      }
    ]
    setEvents(mockEvents)
  }, [])

  // Filter events by tenant and tier if specified
  const filteredEvents = events.filter(event => {
    if (tenantId && event.tenant_id !== tenantId) return false
    if (tier && event.tier !== tier) return false
    return true
  })

  // Get events for selected date
  const selectedDateEvents = filteredEvents.filter(event => 
    selected && format(event.date, 'yyyy-MM-dd') === format(selected, 'yyyy-MM-dd')
  )

  // Get days with events for calendar highlighting
  const eventDays = filteredEvents.map(event => event.date)

  const handleAddEvent = () => {
    if (!newEvent.title || !selected) return

    const event: CampaignEvent = {
      id: Math.random().toString(36).substr(2, 9),
      title: newEvent.title,
      description: newEvent.description || '',
      date: selected,
      type: newEvent.type || 'launch',
      tier: newEvent.tier || 'tier_1',
      tenant_id: tenantId || 'default',
      assigned_agents: [],
      status: 'scheduled',
      estimated_duration: newEvent.estimated_duration || 2,
      priority: newEvent.priority || 'medium'
    }

    setEvents([...events, event])
    setNewEvent({
      title: '',
      description: '',
      type: 'launch',
      tier: tier || 'tier_1',
      priority: 'medium',
      estimated_duration: 2
    })
    setIsAddingEvent(false)
  }

  const getEventTypeColor = (type: string) => {
    const colors = {
      launch: 'bg-green-500',
      review: 'bg-blue-500',
      optimization: 'bg-yellow-500',
      completion: 'bg-purple-500',
      milestone: 'bg-orange-500'
    }
    return colors[type as keyof typeof colors] || 'bg-gray-500'
  }

  const getPriorityColor = (priority: string) => {
    const colors = {
      low: 'border-l-green-500',
      medium: 'border-l-yellow-500',
      high: 'border-l-orange-500',
      critical: 'border-l-red-500'
    }
    return colors[priority as keyof typeof colors] || 'border-l-gray-500'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CalendarDays className="h-5 w-5" />
            Campaign Calendar
          </CardTitle>
          <CardDescription>
            Schedule and manage marketing campaigns, AI agent tasks, and milestones
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Calendar */}
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold">
                  {format(selected || new Date(), 'MMMM yyyy')}
                </h3>
                <Dialog open={isAddingEvent} onOpenChange={setIsAddingEvent}>
                  <DialogTrigger asChild>
                    <Button size="sm" className="gap-2">
                      <Plus className="h-4 w-4" />
                      Add Event
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Schedule Campaign Event</DialogTitle>
                      <DialogDescription>
                        Create a new campaign milestone or task for {selected && format(selected, 'PPP')}
                      </DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid gap-2">
                        <Label htmlFor="title">Event Title</Label>
                        <Input
                          id="title"
                          value={newEvent.title}
                          onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                          placeholder="Enter event title..."
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="description">Description</Label>
                        <Input
                          id="description"
                          value={newEvent.description}
                          onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                          placeholder="Event description..."
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="grid gap-2">
                          <Label>Event Type</Label>
                          <Select
                            value={newEvent.type}
                            onValueChange={(value) => setNewEvent({ ...newEvent, type: value as any })}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="launch">Campaign Launch</SelectItem>
                              <SelectItem value="review">Performance Review</SelectItem>
                              <SelectItem value="optimization">Optimization</SelectItem>
                              <SelectItem value="completion">Completion</SelectItem>
                              <SelectItem value="milestone">Milestone</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="grid gap-2">
                          <Label>Priority</Label>
                          <Select
                            value={newEvent.priority}
                            onValueChange={(value) => setNewEvent({ ...newEvent, priority: value as any })}
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
                        <Label htmlFor="duration">Estimated Duration (hours)</Label>
                        <Input
                          id="duration"
                          type="number"
                          value={newEvent.estimated_duration}
                          onChange={(e) => setNewEvent({ ...newEvent, estimated_duration: parseInt(e.target.value) })}
                          min="1"
                          max="24"
                        />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button type="submit" onClick={handleAddEvent}>
                        Schedule Event
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
              
              <DayPicker
                mode="single"
                selected={selected}
                onSelect={setSelected}
                className="rounded-md border"
                modifiers={{
                  hasEvent: eventDays,
                  today: new Date()
                }}
                modifiersClassNames={{
                  hasEvent: 'bg-primary/20 font-bold',
                  today: 'bg-accent'
                }}
              />
            </div>

            {/* Events for Selected Date */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">
                {selected ? format(selected, 'PPP') : 'Select a date'}
              </h3>
              
              {selectedDateEvents.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <CalendarDays className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No events scheduled for this date</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {selectedDateEvents.map((event) => (
                    <Card
                      key={event.id}
                      className={`cursor-pointer hover:shadow-md transition-shadow border-l-4 ${getPriorityColor(event.priority)}`}
                      onClick={() => setSelectedEvent(event)}
                    >
                      <CardContent className="p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div className="flex items-center gap-2">
                            <Badge className={`${getEventTypeColor(event.type)} text-white`}>
                              {event.type}
                            </Badge>
                            <Badge variant="outline">
                              {event.tier.replace('_', ' ').toUpperCase()}
                            </Badge>
                          </div>
                          <Badge 
                            variant={event.status === 'completed' ? 'default' : 'secondary'}
                          >
                            {event.status}
                          </Badge>
                        </div>
                        <h4 className="font-semibold text-sm">{event.title}</h4>
                        {event.description && (
                          <p className="text-xs text-muted-foreground mt-1">
                            {event.description}
                          </p>
                        )}
                        <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {event.estimated_duration}h
                          </div>
                          <div className="flex items-center gap-1">
                            <Users className="h-3 w-3" />
                            {event.assigned_agents.length} agents
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
              <div className="text-2xl font-bold text-primary">{filteredEvents.length}</div>
              <div className="text-xs text-muted-foreground">Total Events</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {filteredEvents.filter(e => e.status === 'completed').length}
              </div>
              <div className="text-xs text-muted-foreground">Completed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {filteredEvents.filter(e => e.status === 'scheduled').length}
              </div>
              <div className="text-xs text-muted-foreground">Scheduled</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {filteredEvents.filter(e => e.status === 'in_progress').length}
              </div>
              <div className="text-xs text-muted-foreground">In Progress</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Event Details Dialog */}
      {selectedEvent && (
        <Dialog open={!!selectedEvent} onOpenChange={() => setSelectedEvent(null)}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                <Badge className={`${getEventTypeColor(selectedEvent.type)} text-white`}>
                  {selectedEvent.type}
                </Badge>
                {selectedEvent.title}
              </DialogTitle>
              <DialogDescription>
                {format(selectedEvent.date, 'PPP')} • {selectedEvent.estimated_duration} hours
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              {selectedEvent.description && (
                <div>
                  <h4 className="font-medium mb-1">Description</h4>
                  <p className="text-sm text-muted-foreground">{selectedEvent.description}</p>
                </div>
              )}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Tier</h4>
                  <Badge variant="outline">{selectedEvent.tier.replace('_', ' ').toUpperCase()}</Badge>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Priority</h4>
                  <Badge variant="outline">{selectedEvent.priority.toUpperCase()}</Badge>
                </div>
              </div>
              {selectedEvent.assigned_agents.length > 0 && (
                <div>
                  <h4 className="font-medium mb-1">Assigned AI Agents</h4>
                  <div className="flex flex-wrap gap-1">
                    {selectedEvent.assigned_agents.map((agent) => (
                      <Badge key={agent} variant="secondary" className="text-xs">
                        {agent}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setSelectedEvent(null)}>
                Close
              </Button>
              <Button>Edit Event</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}