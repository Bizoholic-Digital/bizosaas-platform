'use client'

import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { ScrollArea } from '@/components/ui/scroll-area'
import { 
  MessageCircle, 
  Send, 
  Paperclip, 
  Phone, 
  Video, 
  MoreVertical,
  Clock,
  CheckCircle,
  AlertCircle,
  User,
  Headphones,
  FileText,
  Search,
  Filter,
  Plus,
  Star,
  Settings
} from 'lucide-react'

interface ChatMessage {
  id: string
  sender: 'client' | 'agent' | 'system'
  message: string
  timestamp: string
  attachments?: string[]
  status?: 'sent' | 'delivered' | 'read'
}

interface SupportTicket {
  id: string
  title: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: 'open' | 'in_progress' | 'resolved' | 'closed'
  customer: {
    name: string
    email: string
    avatar?: string
  }
  description: string
  created: string
  updated: string
  agent?: string
}

export default function ClientSupportPage() {
  const [activeTab, setActiveTab] = useState('chat')
  const [chatMessage, setChatMessage] = useState('')
  const [selectedTicket, setSelectedTicket] = useState<string | null>(null)
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([])
  const [supportTickets, setSupportTickets] = useState<SupportTicket[]>([])
  const [onlineUsers, setOnlineUsers] = useState(12)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Mock chat messages
    const mockMessages: ChatMessage[] = [
      {
        id: '1',
        sender: 'client',
        message: 'Hi! I need help with setting up my Google Ads integration.',
        timestamp: '10:30 AM',
        status: 'read'
      },
      {
        id: '2',
        sender: 'agent',
        message: 'Hello! I\'d be happy to help you with that. Can you tell me what specific issue you\'re encountering?',
        timestamp: '10:32 AM',
        status: 'read'
      },
      {
        id: '3',
        sender: 'client',
        message: 'The connection keeps failing when I try to authenticate. I\'ve tried refreshing the token multiple times.',
        timestamp: '10:35 AM',
        status: 'read'
      },
      {
        id: '4',
        sender: 'agent',
        message: 'I see. Let me check your integration settings. This usually happens when there\'s a scope permission issue. Can you navigate to Dashboard > Integrations and click on Google Ads?',
        timestamp: '10:37 AM',
        status: 'delivered'
      },
      {
        id: '5',
        sender: 'system',
        message: 'Agent shared a screenshot: google-ads-setup.png',
        timestamp: '10:38 AM',
        status: 'sent'
      }
    ]

    // Mock support tickets
    const mockTickets: SupportTicket[] = [
      {
        id: 'T-001',
        title: 'Google Ads Integration Issue',
        priority: 'high',
        status: 'in_progress',
        customer: {
          name: 'John Smith',
          email: 'john.smith@example.com',
          avatar: '/avatar-1.png'
        },
        description: 'Unable to connect Google Ads account, authentication keeps failing.',
        created: '2 hours ago',
        updated: '5 minutes ago',
        agent: 'Sarah Wilson'
      },
      {
        id: 'T-002',
        title: 'Campaign Performance Question',
        priority: 'medium',
        status: 'open',
        customer: {
          name: 'Emily Chen',
          email: 'emily.chen@company.com'
        },
        description: 'Questions about campaign optimization and AI recommendations.',
        created: '4 hours ago',
        updated: '1 hour ago'
      },
      {
        id: 'T-003',
        title: 'Billing Inquiry',
        priority: 'low',
        status: 'resolved',
        customer: {
          name: 'Michael Johnson',
          email: 'mjohnson@business.com'
        },
        description: 'Request for invoice details and subscription changes.',
        created: '1 day ago',
        updated: '3 hours ago',
        agent: 'Alex Rodriguez'
      }
    ]

    setChatMessages(mockMessages)
    setSupportTickets(mockTickets)
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const sendMessage = () => {
    if (!chatMessage.trim()) return

    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'agent',
      message: chatMessage,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      status: 'sent'
    }

    setChatMessages(prev => [...prev, newMessage])
    setChatMessage('')

    // Simulate client response
    setTimeout(() => {
      const clientReply: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'client',
        message: 'Thanks for the help! That worked perfectly.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        status: 'sent'
      }
      setChatMessages(prev => [...prev, clientReply])
    }, 2000)
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-100 text-red-800 border-red-200'
      case 'high': return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'low': return 'bg-green-100 text-green-800 border-green-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-blue-100 text-blue-800'
      case 'in_progress': return 'bg-yellow-100 text-yellow-800'
      case 'resolved': return 'bg-green-100 text-green-800'
      case 'closed': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Client Support</h1>
          <p className="text-muted-foreground">
            Manage client communications, support tickets, and live chat
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-green-600 border-green-200">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse" />
            {onlineUsers} online
          </Badge>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            New Ticket
          </Button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Tickets</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24</div>
            <p className="text-xs text-muted-foreground">+2 from yesterday</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Response Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12m</div>
            <p className="text-xs text-muted-foreground">Average response</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Satisfaction</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4.8</div>
            <p className="text-xs text-muted-foreground">Out of 5.0</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Online Agents</CardTitle>
            <Headphones className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">Available now</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Support Interface */}
        <div className="lg:col-span-2">
          <Card className="h-[600px]">
            <CardHeader>
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="chat" className="flex items-center">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Live Chat
                  </TabsTrigger>
                  <TabsTrigger value="tickets" className="flex items-center">
                    <FileText className="w-4 h-4 mr-2" />
                    Tickets
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </CardHeader>
            
            <CardContent className="flex-1 p-0">
              <Tabs value={activeTab} className="h-full">
                {/* Live Chat Tab */}
                <TabsContent value="chat" className="h-full m-0">
                  <div className="flex flex-col h-full">
                    {/* Chat Header */}
                    <div className="border-b p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src="/avatar-1.png" alt="John Smith" />
                            <AvatarFallback>JS</AvatarFallback>
                          </Avatar>
                          <div>
                            <h3 className="font-medium">John Smith</h3>
                            <p className="text-sm text-muted-foreground">john.smith@example.com</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button variant="outline" size="icon">
                            <Phone className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="icon">
                            <Video className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="icon">
                            <MoreVertical className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>

                    {/* Messages */}
                    <ScrollArea className="flex-1 p-4">
                      <div className="space-y-4">
                        {chatMessages.map((message) => (
                          <div
                            key={message.id}
                            className={`flex ${
                              message.sender === 'agent' ? 'justify-end' : 'justify-start'
                            }`}
                          >
                            <div
                              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                                message.sender === 'agent'
                                  ? 'bg-primary text-primary-foreground'
                                  : message.sender === 'system'
                                  ? 'bg-muted text-muted-foreground text-center text-sm'
                                  : 'bg-muted'
                              }`}
                            >
                              <p>{message.message}</p>
                              <p className={`text-xs mt-1 ${
                                message.sender === 'agent' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                              }`}>
                                {message.timestamp}
                                {message.sender === 'agent' && message.status && (
                                  <span className="ml-2">
                                    {message.status === 'read' && <CheckCircle className="inline w-3 h-3" />}
                                    {message.status === 'delivered' && <CheckCircle className="inline w-3 h-3 opacity-50" />}
                                  </span>
                                )}
                              </p>
                            </div>
                          </div>
                        ))}
                        <div ref={messagesEndRef} />
                      </div>
                    </ScrollArea>

                    {/* Message Input */}
                    <div className="border-t p-4">
                      <div className="flex items-center space-x-2">
                        <Button variant="outline" size="icon">
                          <Paperclip className="h-4 w-4" />
                        </Button>
                        <Input
                          placeholder="Type your message..."
                          value={chatMessage}
                          onChange={(e) => setChatMessage(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                          className="flex-1"
                        />
                        <Button onClick={sendMessage} disabled={!chatMessage.trim()}>
                          <Send className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </TabsContent>

                {/* Support Tickets Tab */}
                <TabsContent value="tickets" className="h-full m-0">
                  <div className="p-4">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-2">
                        <Input placeholder="Search tickets..." className="w-64" />
                        <Button variant="outline" size="icon">
                          <Search className="h-4 w-4" />
                        </Button>
                        <Button variant="outline" size="icon">
                          <Filter className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                    
                    <ScrollArea className="h-[400px]">
                      <div className="space-y-4">
                        {supportTickets.map((ticket) => (
                          <div
                            key={ticket.id}
                            className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                              selectedTicket === ticket.id ? 'border-primary bg-primary/5' : 'hover:border-muted-foreground/50'
                            }`}
                            onClick={() => setSelectedTicket(ticket.id)}
                          >
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center space-x-2">
                                <Badge className={getPriorityColor(ticket.priority)}>
                                  {ticket.priority.toUpperCase()}
                                </Badge>
                                <Badge className={getStatusColor(ticket.status)}>
                                  {ticket.status.replace('_', ' ').toUpperCase()}
                                </Badge>
                              </div>
                              <span className="text-sm text-muted-foreground">{ticket.id}</span>
                            </div>
                            
                            <h3 className="font-medium mb-1">{ticket.title}</h3>
                            <p className="text-sm text-muted-foreground mb-2">{ticket.description}</p>
                            
                            <div className="flex items-center justify-between text-xs text-muted-foreground">
                              <div className="flex items-center space-x-2">
                                <User className="h-3 w-3" />
                                <span>{ticket.customer.name}</span>
                              </div>
                              <div className="flex items-center space-x-4">
                                {ticket.agent && (
                                  <span>Agent: {ticket.agent}</span>
                                )}
                                <span>Updated {ticket.updated}</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </div>

        {/* Activity Panel */}
        <div className="space-y-6">
          {/* Team Status */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Team Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span className="text-sm">Sarah Wilson</span>
                </div>
                <Badge variant="outline" className="text-xs">3 tickets</Badge>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span className="text-sm">Alex Rodriguez</span>
                </div>
                <Badge variant="outline" className="text-xs">2 tickets</Badge>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full" />
                  <span className="text-sm">Mike Johnson</span>
                </div>
                <Badge variant="outline" className="text-xs">Away</Badge>
              </div>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Recent Activity</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                  <div>
                    <p className="text-sm">New ticket created</p>
                    <p className="text-xs text-muted-foreground">Payment issue - Emily Chen</p>
                    <p className="text-xs text-muted-foreground">2 minutes ago</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-2" />
                  <div>
                    <p className="text-sm">Ticket resolved</p>
                    <p className="text-xs text-muted-foreground">Integration issue - John Smith</p>
                    <p className="text-xs text-muted-foreground">15 minutes ago</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2" />
                  <div>
                    <p className="text-sm">Escalation requested</p>
                    <p className="text-xs text-muted-foreground">Complex setup - TechCorp Ltd</p>
                    <p className="text-xs text-muted-foreground">1 hour ago</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full justify-start">
                <Plus className="w-4 h-4 mr-2" />
                Create Ticket
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <MessageCircle className="w-4 h-4 mr-2" />
                Start Chat
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Settings className="w-4 h-4 mr-2" />
                Chat Settings
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}