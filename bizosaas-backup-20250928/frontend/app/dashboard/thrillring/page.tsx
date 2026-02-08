'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Heart, Users, MessageCircle, Calendar, TrendingUp, 
  ExternalLink, RefreshCw, AlertCircle, CheckCircle,
  Plus, Edit, Eye, Settings, Zap, Star, UserPlus
} from 'lucide-react'
import { FeatureGate } from '@/components/tenant/feature-gate'

interface Match {
  id: string
  name: string
  age: number
  compatibility: number
  status: 'matched' | 'liked' | 'passed'
  image?: string
  lastActive: string
}

interface Event {
  id: string
  title: string
  date: string
  attendees: number
  status: 'upcoming' | 'ongoing' | 'completed'
  category: string
}

export default function ThrillRingDashboard() {
  const [matches, setMatches] = useState<Match[]>([])
  const [events, setEvents] = useState<Event[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [aiStatus, setAiStatus] = useState<'connecting' | 'connected' | 'error'>('connecting')

  useEffect(() => {
    const loadData = async () => {
      try {
        // Simulate loading
        setTimeout(() => {
          setMatches([
            { id: '1', name: 'Sarah M.', age: 28, compatibility: 94, status: 'matched', lastActive: '2 hours ago' },
            { id: '2', name: 'Jessica L.', age: 25, compatibility: 87, status: 'liked', lastActive: '1 day ago' },
            { id: '3', name: 'Emma R.', age: 32, compatibility: 82, status: 'matched', lastActive: '3 hours ago' },
            { id: '4', name: 'Ashley K.', age: 29, compatibility: 78, status: 'liked', lastActive: '5 hours ago' },
          ])
          
          setEvents([
            { id: '1', title: 'Wine Tasting Social', date: '2025-09-15', attendees: 24, status: 'upcoming', category: 'Social' },
            { id: '2', title: 'Hiking Adventure Group', date: '2025-09-13', attendees: 18, status: 'upcoming', category: 'Outdoor' },
            { id: '3', title: 'Speed Dating Night', date: '2025-09-12', attendees: 32, status: 'completed', category: 'Dating' },
          ])
          
          setAiStatus('connected')
          setIsLoading(false)
        }, 1500)
      } catch (error) {
        console.error('Error loading ThrillRing data:', error)
        setAiStatus('error')
        setIsLoading(false)
      }
    }
    
    loadData()
  }, [])

  const stats = [
    { title: 'AI Matches Today', value: '12', change: '+8', icon: Heart, positive: true },
    { title: 'Profile Views', value: '247', change: '+23', icon: Users, positive: true },
    { title: 'Event RSVPs', value: '5', change: '+2', icon: Calendar, positive: true },
    { title: 'Compatibility Score', value: '94%', change: '+3%', icon: Zap, positive: true },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">ThrillRing Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            AI-powered dating and social networking platform
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            {aiStatus === 'connected' ? (
              <>
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm text-green-600">AI Matching Active</span>
              </>
            ) : aiStatus === 'connecting' ? (
              <>
                <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />
                <span className="text-sm text-blue-600">Connecting...</span>
              </>
            ) : (
              <>
                <AlertCircle className="h-4 w-4 text-red-500" />
                <span className="text-sm text-red-600">Connection Error</span>
              </>
            )}
          </div>
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => window.open('http://localhost:3004', '_blank')}
          >
            <ExternalLink className="h-4 w-4 mr-2" />
            View App
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className={`text-xs ${stat.positive ? 'text-green-600' : 'text-red-600'}`}>
                {stat.change} from yesterday
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="matches">AI Matches</TabsTrigger>
          <TabsTrigger value="events">Events</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Recent Matches */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Heart className="h-5 w-5 mr-2 text-red-500" />
                  Recent AI Matches
                </CardTitle>
                <CardDescription>Your latest AI-powered compatibility matches</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {matches.slice(0, 3).map((match) => (
                    <div key={match.id} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-r from-pink-400 to-red-400 rounded-full flex items-center justify-center">
                          <span className="text-white font-medium">{match.name.charAt(0)}</span>
                        </div>
                        <div>
                          <p className="font-medium">{match.name}</p>
                          <p className="text-sm text-muted-foreground">{match.age} years • {match.lastActive}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="flex items-center">
                          <Star className="h-4 w-4 text-yellow-400 mr-1" />
                          <span className="font-medium">{match.compatibility}%</span>
                        </div>
                        <Badge variant={match.status === 'matched' ? 'default' : 'secondary'}>
                          {match.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Upcoming Events */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="h-5 w-5 mr-2 text-blue-500" />
                  Upcoming Events
                </CardTitle>
                <CardDescription>Social events and activities near you</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {events.filter(e => e.status === 'upcoming').slice(0, 3).map((event) => (
                    <div key={event.id} className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{event.title}</p>
                        <p className="text-sm text-muted-foreground">
                          {event.date} • {event.attendees} attending
                        </p>
                      </div>
                      <div className="text-right">
                        <Badge variant="outline">{event.category}</Badge>
                        <Button size="sm" className="ml-2">RSVP</Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="matches">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>AI-Powered Matches</CardTitle>
                <CardDescription>Discover your perfect matches with advanced AI compatibility</CardDescription>
              </div>
              <FeatureGate 
                feature="ai-matching" 
                fallback={
                  <Button disabled>
                    <UserPlus className="h-4 w-4 mr-2" />
                    Find More Matches (Pro)
                  </Button>
                }
              >
                <Button>
                  <UserPlus className="h-4 w-4 mr-2" />
                  Find More Matches
                </Button>
              </FeatureGate>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {matches.map((match) => (
                  <div key={match.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-gradient-to-r from-pink-400 to-red-400 rounded-full flex items-center justify-center">
                        <span className="text-white font-medium">{match.name.charAt(0)}</span>
                      </div>
                      <div>
                        <h3 className="font-medium">{match.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {match.age} years • Last active {match.lastActive}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="text-right">
                        <div className="flex items-center">
                          <Star className="h-4 w-4 text-yellow-400 mr-1" />
                          <span className="font-bold text-lg">{match.compatibility}%</span>
                        </div>
                        <Badge variant={match.status === 'matched' ? 'default' : 'secondary'}>
                          {match.status}
                        </Badge>
                      </div>
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <MessageCircle className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Heart className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="events">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Social Events</CardTitle>
                <CardDescription>Join exciting events and meet new people</CardDescription>
              </div>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Create Event
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {events.map((event) => (
                  <div key={event.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-medium">{event.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {event.date} • {event.attendees} attendees
                      </p>
                    </div>
                    <div className="flex items-center gap-4">
                      <Badge variant={
                        event.status === 'completed' ? 'default' : 
                        event.status === 'ongoing' ? 'secondary' : 'outline'
                      }>
                        {event.status}
                      </Badge>
                      <Badge variant="outline">{event.category}</Badge>
                      <Button size="sm" disabled={event.status === 'completed'}>
                        {event.status === 'upcoming' ? 'RSVP' : 'View'}
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Matching Analytics</CardTitle>
                <CardDescription>Your dating and social activity insights</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Total Matches This Month</span>
                    <span className="font-semibold">47</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Average Compatibility</span>
                    <span className="font-semibold">82%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Events Attended</span>
                    <span className="font-semibold">8</span>
                  </div>
                  <div className="flex justify-between text-green-600">
                    <span>Success Rate</span>
                    <span className="font-semibold">34%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>AI Insights</CardTitle>
                <CardDescription>Personalized recommendations from our AI</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-pink-50 rounded-lg">
                    <p className="text-sm">💕 <strong>Match AI:</strong> Try events on weekends - 40% higher match success</p>
                  </div>
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm">🎯 <strong>Profile AI:</strong> Update your photos - recent ones get 60% more views</p>
                  </div>
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <p className="text-sm">🌟 <strong>Event AI:</strong> Wine tasting events match your interests perfectly</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>ThrillRing Settings</CardTitle>
              <CardDescription>Customize your dating and social experience</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-medium mb-3">AI Matching Preferences</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Age Range</span>
                      <Badge variant="outline">25-35 years</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Distance</span>
                      <Badge variant="outline">Within 25 miles</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Compatibility Threshold</span>
                      <Badge variant="outline">75%+</Badge>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-medium mb-3">Quick Actions</h3>
                  <div className="space-y-2">
                    <Button variant="outline" className="w-full justify-start">
                      <Settings className="h-4 w-4 mr-2" />
                      Profile Settings
                    </Button>
                    <Button variant="outline" className="w-full justify-start">
                      <Heart className="h-4 w-4 mr-2" />
                      Match Preferences
                    </Button>
                    <Button variant="outline" className="w-full justify-start">
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Open ThrillRing App
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}