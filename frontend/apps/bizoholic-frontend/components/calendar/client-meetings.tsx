'use client'

import { useState, useEffect } from 'react'
import { DayPicker } from 'react-day-picker'
import { format, addHours, startOfWeek, endOfWeek, eachDayOfInterval } from 'date-fns'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Users, Video, Phone, MapPin, Clock, Plus, Calendar as CalendarIcon, ExternalLink } from 'lucide-react'
import { useApiGatewayDashboard } from '@/hooks/use-api-gateway'

// Types for client meetings
interface ClientMeeting {
  id: string
  title: string
  description?: string
  client_name: string
  client_email: string
  client_company: string
  client_tier: 'tier_1' | 'tier_2' | 'tier_3'
  meeting_date: Date
  duration: number // in minutes
  meeting_type: 'onboarding' | 'review' | 'strategy' | 'support' | 'demo' | 'training'
  format: 'video' | 'phone' | 'in_person'
  location?: string // For in-person or video link
  status: 'scheduled' | 'confirmed' | 'completed' | 'cancelled' | 'rescheduled'
  attendees: string[]
  agenda?: string[]
  preparation_notes?: string
  followup_required: boolean
  meeting_outcome?: string
  next_steps?: string[]
  assigned_team_member: string
}

interface ClientMeetingsProps {
  tenantId?: string
  teamMember?: string
  className?: string
}

export function ClientMeetings({ tenantId, teamMember, className }: ClientMeetingsProps) {
  const [selected, setSelected] = useState<Date | undefined>(new Date())
  const [meetings, setMeetings] = useState<ClientMeeting[]>([])
  const [isScheduling, setIsScheduling] = useState(false)
  const [selectedMeeting, setSelectedMeeting] = useState<ClientMeeting | null>(null)
  const [viewMode, setViewMode] = useState<'calendar' | 'week' | 'list'>('calendar')
  const [newMeeting, setNewMeeting] = useState<Partial<ClientMeeting>>({
    title: '',
    client_name: '',
    client_email: '',
    client_company: '',
    client_tier: 'tier_1',
    duration: 60,
    meeting_type: 'onboarding',
    format: 'video',
    followup_required: true
  })

  const { data: gatewayData } = useApiGatewayDashboard()

  // Mock data for client meetings
  useEffect(() => {
    const mockMeetings: ClientMeeting[] = [
      {
        id: '1',
        title: 'Client Onboarding - TechCorp',
        description: 'Initial onboarding session for new Tier 3 client',
        client_name: 'Sarah Johnson',
        client_email: 'sarah@techcorp.com',
        client_company: 'TechCorp Solutions',
        client_tier: 'tier_3',
        meeting_date: addHours(new Date(), 24),
        duration: 90,
        meeting_type: 'onboarding',
        format: 'video',
        location: 'https://zoom.us/j/123456789',
        status: 'confirmed',
        attendees: ['sarah@techcorp.com', 'john@techcorp.com'],
        agenda: [
          'Platform walkthrough',
          'Campaign strategy discussion',
          'AI agents setup',
          'Next steps planning'
        ],
        preparation_notes: 'Client is particularly interested in e-commerce automation',
        followup_required: true,
        assigned_team_member: 'John Smith'
      },
      {
        id: '2',
        title: 'Monthly Review - GrowthCo',
        description: 'Monthly performance review and strategy adjustment',
        client_name: 'Mike Chen',
        client_email: 'mike@growthco.com',
        client_company: 'GrowthCo Marketing',
        client_tier: 'tier_2',
        meeting_date: addHours(new Date(), 48),
        duration: 60,
        meeting_type: 'review',
        format: 'video',
        location: 'https://meet.google.com/xyz-abc-def',
        status: 'scheduled',
        attendees: ['mike@growthco.com'],
        agenda: [
          'Campaign performance review',
          'ROI analysis',
          'Optimization recommendations',
          'Next month planning'
        ],
        followup_required: true,
        assigned_team_member: 'Emily Davis'
      },
      {
        id: '3',
        title: 'Strategy Session - StartupX',
        description: 'Quarterly strategy planning session',
        client_name: 'Alex Rodriguez',
        client_email: 'alex@startupx.io',
        client_company: 'StartupX',
        client_tier: 'tier_1',
        meeting_date: addHours(new Date(), 72),
        duration: 45,
        meeting_type: 'strategy',
        format: 'phone',
        status: 'scheduled',
        attendees: ['alex@startupx.io'],
        agenda: [
          'Current campaign analysis',
          'Market positioning',
          'Growth strategy',
          'Budget allocation'
        ],
        followup_required: false,
        assigned_team_member: 'Sarah Wilson'
      }
    ]
    setMeetings(mockMeetings)
  }, [])

  // Filter meetings by tenant and team member if specified
  const filteredMeetings = meetings.filter(meeting => {
    if (teamMember && meeting.assigned_team_member !== teamMember) return false
    return true
  })

  // Get meetings for selected date
  const selectedDateMeetings = filteredMeetings.filter(meeting => 
    selected && format(meeting.meeting_date, 'yyyy-MM-dd') === format(selected, 'yyyy-MM-dd')
  )

  // Get week meetings for week view
  const weekStart = selected ? startOfWeek(selected) : startOfWeek(new Date())
  const weekEnd = endOfWeek(weekStart)
  const weekDays = eachDayOfInterval({ start: weekStart, end: weekEnd })
  
  const weekMeetings = weekDays.map(day => ({
    date: day,
    meetings: filteredMeetings.filter(meeting => 
      format(meeting.meeting_date, 'yyyy-MM-dd') === format(day, 'yyyy-MM-dd')
    )
  }))

  const handleScheduleMeeting = () => {
    if (!newMeeting.title || !newMeeting.client_name || !selected) return

    // Calculate meeting time (using selected date + time input)
    const meetingDate = new Date(selected)
    meetingDate.setHours(10, 0, 0, 0) // Default to 10 AM

    const meeting: ClientMeeting = {
      id: Math.random().toString(36).substr(2, 9),
      title: newMeeting.title!,
      description: newMeeting.description,
      client_name: newMeeting.client_name!,
      client_email: newMeeting.client_email!,
      client_company: newMeeting.client_company!,
      client_tier: newMeeting.client_tier || 'tier_1',
      meeting_date: meetingDate,
      duration: newMeeting.duration || 60,
      meeting_type: newMeeting.meeting_type || 'onboarding',
      format: newMeeting.format || 'video',
      location: newMeeting.location,
      status: 'scheduled',
      attendees: [newMeeting.client_email!],
      followup_required: newMeeting.followup_required !== false,
      assigned_team_member: teamMember || 'Unassigned'
    }

    setMeetings([...meetings, meeting])
    setNewMeeting({
      title: '',
      client_name: '',
      client_email: '',
      client_company: '',
      client_tier: 'tier_1',
      duration: 60,
      meeting_type: 'onboarding',
      format: 'video',
      followup_required: true
    })
    setIsScheduling(false)
  }

  const getStatusColor = (status: string) => {
    const colors = {
      scheduled: 'bg-blue-500',
      confirmed: 'bg-green-500',
      completed: 'bg-gray-500',
      cancelled: 'bg-red-500',
      rescheduled: 'bg-yellow-500'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-500'
  }

  const getMeetingTypeColor = (type: string) => {
    const colors = {
      onboarding: 'bg-purple-500',
      review: 'bg-blue-500',
      strategy: 'bg-green-500',
      support: 'bg-orange-500',
      demo: 'bg-pink-500',
      training: 'bg-indigo-500'
    }
    return colors[type as keyof typeof colors] || 'bg-gray-500'
  }

  const getTierColor = (tier: string) => {
    const colors = {
      tier_1: 'border-l-green-500',
      tier_2: 'border-l-yellow-500', 
      tier_3: 'border-l-purple-500'
    }
    return colors[tier as keyof typeof colors] || 'border-l-gray-500'
  }

  const getFormatIcon = (format: string) => {
    const icons = {
      video: <Video className="h-4 w-4" />,
      phone: <Phone className="h-4 w-4" />,
      in_person: <MapPin className="h-4 w-4" />
    }
    return icons[format as keyof typeof icons] || <CalendarIcon className="h-4 w-4" />
  }

  // Get days with meetings for calendar highlighting
  const meetingDays = filteredMeetings.map(meeting => meeting.meeting_date)

  return (
    <div className={`space-y-6 ${className}`}>
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Client Meetings
              </CardTitle>
              <CardDescription>
                Schedule and manage client meetings, onboarding sessions, and reviews
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Select value={viewMode} onValueChange={setViewMode as any}>
                <SelectTrigger className="w-[120px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="calendar">Calendar</SelectItem>
                  <SelectItem value="week">Week</SelectItem>
                  <SelectItem value="list">List</SelectItem>
                </SelectContent>
              </Select>
              <Dialog open={isScheduling} onOpenChange={setIsScheduling}>
                <DialogTrigger asChild>
                  <Button size="sm" className="gap-2">
                    <Plus className="h-4 w-4" />
                    Schedule Meeting
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>Schedule Client Meeting</DialogTitle>
                    <DialogDescription>
                      Create a new meeting for {selected && format(selected, 'PPP')}
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-4 py-4 max-h-[60vh] overflow-y-auto">
                    <div className="grid gap-2">
                      <Label htmlFor="title">Meeting Title</Label>
                      <Input
                        id="title"
                        value={newMeeting.title}
                        onChange={(e) => setNewMeeting({ ...newMeeting, title: e.target.value })}
                        placeholder="Enter meeting title..."
                      />
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label htmlFor="client_name">Client Name</Label>
                        <Input
                          id="client_name"
                          value={newMeeting.client_name}
                          onChange={(e) => setNewMeeting({ ...newMeeting, client_name: e.target.value })}
                          placeholder="Client name..."
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="client_email">Client Email</Label>
                        <Input
                          id="client_email"
                          type="email"
                          value={newMeeting.client_email}
                          onChange={(e) => setNewMeeting({ ...newMeeting, client_email: e.target.value })}
                          placeholder="client@company.com"
                        />
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label htmlFor="client_company">Company</Label>
                        <Input
                          id="client_company"
                          value={newMeeting.client_company}
                          onChange={(e) => setNewMeeting({ ...newMeeting, client_company: e.target.value })}
                          placeholder="Company name..."
                        />
                      </div>
                      <div className="grid gap-2">
                        <Label>Client Tier</Label>
                        <Select
                          value={newMeeting.client_tier}
                          onValueChange={(value) => setNewMeeting({ ...newMeeting, client_tier: value as any })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="tier_1">Tier 1 ($97)</SelectItem>
                            <SelectItem value="tier_2">Tier 2 ($297)</SelectItem>
                            <SelectItem value="tier_3">Tier 3 ($997)</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                    
                    <div className="grid gap-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        value={newMeeting.description}
                        onChange={(e) => setNewMeeting({ ...newMeeting, description: e.target.value })}
                        placeholder="Meeting description..."
                        rows={3}
                      />
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4">
                      <div className="grid gap-2">
                        <Label>Meeting Type</Label>
                        <Select
                          value={newMeeting.meeting_type}
                          onValueChange={(value) => setNewMeeting({ ...newMeeting, meeting_type: value as any })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="onboarding">Onboarding</SelectItem>
                            <SelectItem value="review">Review</SelectItem>
                            <SelectItem value="strategy">Strategy</SelectItem>
                            <SelectItem value="support">Support</SelectItem>
                            <SelectItem value="demo">Demo</SelectItem>
                            <SelectItem value="training">Training</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid gap-2">
                        <Label>Format</Label>
                        <Select
                          value={newMeeting.format}
                          onValueChange={(value) => setNewMeeting({ ...newMeeting, format: value as any })}
                        >
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="video">Video Call</SelectItem>
                            <SelectItem value="phone">Phone Call</SelectItem>
                            <SelectItem value="in_person">In Person</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="duration">Duration (min)</Label>
                        <Input
                          id="duration"
                          type="number"
                          value={newMeeting.duration}
                          onChange={(e) => setNewMeeting({ ...newMeeting, duration: parseInt(e.target.value) })}
                          min="15"
                          max="240"
                        />
                      </div>
                    </div>
                    
                    {(newMeeting.format === 'video' || newMeeting.format === 'in_person') && (
                      <div className="grid gap-2">
                        <Label htmlFor="location">
                          {newMeeting.format === 'video' ? 'Meeting Link' : 'Location'}
                        </Label>
                        <Input
                          id="location"
                          value={newMeeting.location}
                          onChange={(e) => setNewMeeting({ ...newMeeting, location: e.target.value })}
                          placeholder={newMeeting.format === 'video' ? 'https://zoom.us/j/...' : 'Meeting location...'}
                        />
                      </div>
                    )}
                  </div>
                  <DialogFooter>
                    <Button type="submit" onClick={handleScheduleMeeting}>
                      Schedule Meeting
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {viewMode === 'calendar' && (
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
                    hasMeeting: meetingDays,
                    today: new Date()
                  }}
                  modifiersClassNames={{
                    hasMeeting: 'bg-primary/20 font-bold',
                    today: 'bg-accent'
                  }}
                />
              </div>

              {/* Meetings for Selected Date */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">
                  Meetings for {selected ? format(selected, 'PPP') : 'Select a date'}
                </h3>
                
                {selectedDateMeetings.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <Users className="h-8 w-8 mx-auto mb-2 opacity-50" />
                    <p>No meetings scheduled for this date</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {selectedDateMeetings
                      .sort((a, b) => a.meeting_date.getTime() - b.meeting_date.getTime())
                      .map((meeting) => (
                        <Card
                          key={meeting.id}
                          className={`cursor-pointer hover:shadow-md transition-shadow border-l-4 ${getTierColor(meeting.client_tier)}`}
                          onClick={() => setSelectedMeeting(meeting)}
                        >
                          <CardContent className="p-4">
                            <div className="flex justify-between items-start mb-2">
                              <div className="flex items-center gap-2">
                                <Badge className={`${getMeetingTypeColor(meeting.meeting_type)} text-white`}>
                                  {meeting.meeting_type}
                                </Badge>
                                <Badge className={`${getStatusColor(meeting.status)} text-white`}>
                                  {meeting.status}
                                </Badge>
                              </div>
                              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                {getFormatIcon(meeting.format)}
                                {format(meeting.meeting_date, 'HH:mm')}
                              </div>
                            </div>
                            
                            <h4 className="font-semibold text-sm">{meeting.title}</h4>
                            <div className="flex items-center gap-2 mt-1">
                              <Avatar className="h-6 w-6">
                                <AvatarImage src={`https://avatar.vercel.sh/${meeting.client_email}`} />
                                <AvatarFallback>{meeting.client_name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                              </Avatar>
                              <div>
                                <p className="text-xs font-medium">{meeting.client_name}</p>
                                <p className="text-xs text-muted-foreground">{meeting.client_company}</p>
                              </div>
                            </div>
                            
                            <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                              <div className="flex items-center gap-1">
                                <Clock className="h-3 w-3" />
                                {meeting.duration}min
                              </div>
                              <Badge variant="outline" className="text-xs">
                                {meeting.client_tier.replace('_', ' ').toUpperCase()}
                              </Badge>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">{filteredMeetings.length}</div>
              <div className="text-xs text-muted-foreground">Total Meetings</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {filteredMeetings.filter(m => m.status === 'confirmed').length}
              </div>
              <div className="text-xs text-muted-foreground">Confirmed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {filteredMeetings.filter(m => m.status === 'scheduled').length}
              </div>
              <div className="text-xs text-muted-foreground">Scheduled</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {filteredMeetings.filter(m => m.followup_required).length}
              </div>
              <div className="text-xs text-muted-foreground">Need Follow-up</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Meeting Details Dialog */}
      {selectedMeeting && (
        <Dialog open={!!selectedMeeting} onOpenChange={() => setSelectedMeeting(null)}>
          <DialogContent className="max-w-2xl">
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2">
                {getFormatIcon(selectedMeeting.format)}
                {selectedMeeting.title}
              </DialogTitle>
              <DialogDescription>
                {format(selectedMeeting.meeting_date, 'PPP p')} • {selectedMeeting.duration} minutes
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <Avatar>
                  <AvatarImage src={`https://avatar.vercel.sh/${selectedMeeting.client_email}`} />
                  <AvatarFallback>{selectedMeeting.client_name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">{selectedMeeting.client_name}</p>
                  <p className="text-sm text-muted-foreground">{selectedMeeting.client_company}</p>
                  <p className="text-sm text-muted-foreground">{selectedMeeting.client_email}</p>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-1">Status</h4>
                  <Badge className={`${getStatusColor(selectedMeeting.status)} text-white`}>
                    {selectedMeeting.status}
                  </Badge>
                </div>
                <div>
                  <h4 className="font-medium mb-1">Client Tier</h4>
                  <Badge variant="outline">
                    {selectedMeeting.client_tier.replace('_', ' ').toUpperCase()}
                  </Badge>
                </div>
              </div>
              
              {selectedMeeting.description && (
                <div>
                  <h4 className="font-medium mb-1">Description</h4>
                  <p className="text-sm text-muted-foreground">{selectedMeeting.description}</p>
                </div>
              )}
              
              {selectedMeeting.location && (
                <div>
                  <h4 className="font-medium mb-1">
                    {selectedMeeting.format === 'video' ? 'Meeting Link' : 'Location'}
                  </h4>
                  {selectedMeeting.format === 'video' ? (
                    <div className="flex items-center gap-2">
                      <code className="text-sm bg-muted p-1 rounded">{selectedMeeting.location}</code>
                      <Button size="sm" variant="outline" asChild>
                        <a href={selectedMeeting.location} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="h-3 w-3" />
                        </a>
                      </Button>
                    </div>
                  ) : (
                    <p className="text-sm">{selectedMeeting.location}</p>
                  )}
                </div>
              )}
              
              {selectedMeeting.agenda && selectedMeeting.agenda.length > 0 && (
                <div>
                  <h4 className="font-medium mb-1">Agenda</h4>
                  <ul className="text-sm text-muted-foreground list-disc list-inside space-y-1">
                    {selectedMeeting.agenda.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {selectedMeeting.preparation_notes && (
                <div>
                  <h4 className="font-medium mb-1">Preparation Notes</h4>
                  <p className="text-sm text-muted-foreground">{selectedMeeting.preparation_notes}</p>
                </div>
              )}
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setSelectedMeeting(null)}>
                Close
              </Button>
              <Button>Edit Meeting</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}