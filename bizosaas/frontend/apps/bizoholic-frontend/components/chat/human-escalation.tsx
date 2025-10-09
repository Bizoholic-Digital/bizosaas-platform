"use client"

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import {
  UserPlus, MessageCircle, Clock, AlertTriangle, Check, X,
  Settings, Shield, User, Phone, Mail, Headphones
} from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'

interface HumanAgent {
  id: string
  name: string
  email: string
  role: 'support' | 'technical' | 'sales' | 'manager'
  status: 'online' | 'offline' | 'busy' | 'away'
  specialties: string[]
  languages: string[]
  averageResponseTime: number // minutes
  currentTickets: number
  maxTickets: number
  lastSeen?: string
}

interface EscalationRequest {
  id: string
  conversationId: string
  userId: string
  reason: 'complex_query' | 'technical_issue' | 'complaint' | 'sales_inquiry' | 'custom'
  priority: 'low' | 'medium' | 'high' | 'urgent'
  summary: string
  context: string
  status: 'pending' | 'assigned' | 'in_progress' | 'resolved' | 'cancelled'
  assignedAgent?: HumanAgent
  createdAt: string
  estimatedWaitTime?: number
}

interface EscalationSettings {
  enabled: boolean
  globalEnabled: boolean
  userEnabled: boolean
  autoEscalationRules: {
    failedAttemptsThreshold: number
    complexQueryKeywords: string[]
    sentimentThreshold: number
  }
  availableReasons: string[]
  workingHours: {
    start: string
    end: string
    timezone: string
    daysOfWeek: number[]
  }
}

interface HumanEscalationProps {
  conversationId: string
  conversationContext: string
  userSentiment?: {
    sentiment: string
    confidence: number
    frustrated: boolean
  }
  onEscalationRequested?: (request: EscalationRequest) => void
  className?: string
}

export function HumanEscalation({
  conversationId,
  conversationContext,
  userSentiment,
  onEscalationRequested,
  className = ""
}: HumanEscalationProps) {
  const { user } = useAuth()
  const [settings, setSettings] = useState<EscalationSettings | null>(null)
  const [availableAgents, setAvailableAgents] = useState<HumanAgent[]>([])
  const [activeRequest, setActiveRequest] = useState<EscalationRequest | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showEscalationForm, setShowEscalationForm] = useState(false)
  
  // Form state
  const [escalationReason, setEscalationReason] = useState<EscalationRequest['reason']>('complex_query')
  const [priority, setPriority] = useState<EscalationRequest['priority']>('medium')
  const [summary, setSummary] = useState('')
  const [customReason, setCustomReason] = useState('')

  const tenantId = user?.user.tenant_id || 'demo'
  const userId = user?.user.id || 'demo-user'
  const isAdmin = user?.user.role === 'super_admin' || user?.user.role === 'tenant_admin'
  const API_BASE_URL = 'http://localhost:8001'

  // Load escalation settings and check permissions
  useEffect(() => {
    loadEscalationSettings()
    loadAvailableAgents()
    checkActiveRequest()
  }, [tenantId, userId])

  const loadEscalationSettings = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/escalation/settings`, {
        headers: {
          'x-tenant-id': tenantId,
          'x-user-id': userId
        }
      })

      if (response.ok) {
        const data = await response.json()
        setSettings(data.settings)
      } else {
        // Default settings if API fails
        setSettings({
          enabled: false,
          globalEnabled: false,
          userEnabled: false,
          autoEscalationRules: {
            failedAttemptsThreshold: 3,
            complexQueryKeywords: ['technical', 'billing', 'refund', 'cancel'],
            sentimentThreshold: 0.3
          },
          availableReasons: ['complex_query', 'technical_issue', 'complaint', 'sales_inquiry'],
          workingHours: {
            start: '09:00',
            end: '17:00',
            timezone: 'UTC',
            daysOfWeek: [1, 2, 3, 4, 5]
          }
        })
      }
    } catch (error) {
      console.error('Failed to load escalation settings:', error)
    }
  }

  const loadAvailableAgents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/escalation/agents`, {
        headers: {
          'x-tenant-id': tenantId
        }
      })

      if (response.ok) {
        const data = await response.json()
        setAvailableAgents(data.agents || [])
      }
    } catch (error) {
      console.error('Failed to load available agents:', error)
      // Mock data for demo
      setAvailableAgents([
        {
          id: 'agent-1',
          name: 'Sarah Chen',
          email: 'sarah@bizosaas.com',
          role: 'support',
          status: 'online',
          specialties: ['general', 'technical'],
          languages: ['en'],
          averageResponseTime: 5,
          currentTickets: 3,
          maxTickets: 8,
          lastSeen: new Date().toISOString()
        }
      ])
    }
  }

  const checkActiveRequest = async () => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/escalation/requests/${conversationId}`,
        {
          headers: {
            'x-tenant-id': tenantId,
            'x-user-id': userId
          }
        }
      )

      if (response.ok) {
        const data = await response.json()
        if (data.request) {
          setActiveRequest(data.request)
        }
      }
    } catch (error) {
      console.error('Failed to check active request:', error)
    }
  }

  const requestEscalation = async () => {
    if (!settings?.enabled) return

    setIsLoading(true)
    try {
      const request: Partial<EscalationRequest> = {
        conversationId,
        userId,
        reason: escalationReason === 'custom' ? 'custom' : escalationReason,
        priority,
        summary: escalationReason === 'custom' ? customReason : summary || getDefaultSummary(),
        context: conversationContext
      }

      const response = await fetch(`${API_BASE_URL}/api/escalation/request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-tenant-id': tenantId,
          'x-user-id': userId
        },
        body: JSON.stringify(request)
      })

      if (response.ok) {
        const data = await response.json()
        setActiveRequest(data.request)
        setShowEscalationForm(false)
        
        if (onEscalationRequested) {
          onEscalationRequested(data.request)
        }

        // Reset form
        setSummary('')
        setCustomReason('')
        setEscalationReason('complex_query')
        setPriority('medium')
      } else {
        throw new Error('Failed to create escalation request')
      }
    } catch (error) {
      console.error('Escalation request failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const cancelEscalation = async () => {
    if (!activeRequest) return

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/escalation/requests/${activeRequest.id}/cancel`,
        {
          method: 'POST',
          headers: {
            'x-tenant-id': tenantId,
            'x-user-id': userId
          }
        }
      )

      if (response.ok) {
        setActiveRequest(null)
      }
    } catch (error) {
      console.error('Failed to cancel escalation:', error)
    }
  }

  const getDefaultSummary = () => {
    switch (escalationReason) {
      case 'complex_query':
        return 'User needs assistance with a complex query that requires human expertise'
      case 'technical_issue':
        return 'Technical issue that cannot be resolved through automated support'
      case 'complaint':
        return 'User complaint requiring human attention and resolution'
      case 'sales_inquiry':
        return 'Sales-related inquiry requiring specialist assistance'
      default:
        return 'User requests human assistance'
    }
  }

  const getReasonLabel = (reason: string) => {
    const labels: Record<string, string> = {
      complex_query: 'Complex Query',
      technical_issue: 'Technical Issue', 
      complaint: 'Complaint',
      sales_inquiry: 'Sales Inquiry',
      custom: 'Custom'
    }
    return labels[reason] || reason
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'text-red-600 bg-red-50 border-red-200'
      case 'high': return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'medium': return 'text-blue-600 bg-blue-50 border-blue-200'
      case 'low': return 'text-gray-600 bg-gray-50 border-gray-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online': return <div className="w-2 h-2 bg-green-500 rounded-full" />
      case 'busy': return <div className="w-2 h-2 bg-yellow-500 rounded-full" />
      case 'away': return <div className="w-2 h-2 bg-orange-500 rounded-full" />
      case 'offline': return <div className="w-2 h-2 bg-gray-500 rounded-full" />
      default: return <div className="w-2 h-2 bg-gray-500 rounded-full" />
    }
  }

  // Don't render if escalation is disabled
  if (!settings?.enabled || !settings?.globalEnabled || !settings?.userEnabled) {
    return null
  }

  // Show active escalation request status
  if (activeRequest) {
    return (
      <Card className={`${className}`}>
        <CardContent className="pt-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <Headphones className="w-5 h-5 text-blue-500" />
              <span className="font-medium">Human Support Requested</span>
            </div>
            <Badge className={getPriorityColor(activeRequest.priority)}>
              {activeRequest.priority} priority
            </Badge>
          </div>
          
          {activeRequest.assignedAgent ? (
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
                <div>
                  <p className="font-medium">{activeRequest.assignedAgent.name}</p>
                  <p className="text-sm text-muted-foreground">{activeRequest.assignedAgent.role}</p>
                </div>
                <div className="flex items-center space-x-1">
                  {getStatusIcon(activeRequest.assignedAgent.status)}
                  <span className="text-xs text-muted-foreground">
                    {activeRequest.assignedAgent.status}
                  </span>
                </div>
              </div>
              
              <div className="text-sm text-muted-foreground">
                Average response time: {activeRequest.assignedAgent.averageResponseTime} minutes
              </div>
            </div>
          ) : (
            <div className="flex items-center space-x-2 text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span className="text-sm">
                Waiting for agent assignment...
                {activeRequest.estimatedWaitTime && (
                  <span className="ml-1">
                    (Est. {activeRequest.estimatedWaitTime} min wait)
                  </span>
                )}
              </span>
            </div>
          )}
          
          <div className="flex space-x-2 mt-3">
            <Button 
              variant="outline" 
              size="sm"
              onClick={cancelEscalation}
              className="flex-1"
            >
              <X className="w-4 h-4 mr-1" />
              Cancel Request
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Show escalation request button
  return (
    <div className={`${className}`}>
      <Dialog open={showEscalationForm} onOpenChange={setShowEscalationForm}>
        <DialogTrigger asChild>
          <Button variant="outline" size="sm" className="w-full">
            <UserPlus className="w-4 h-4 mr-2" />
            Talk to Human Agent
          </Button>
        </DialogTrigger>
        
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2">
              <Headphones className="w-5 h-5" />
              <span>Request Human Support</span>
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Working Hours Notice */}
            <Alert>
              <Clock className="h-4 w-4" />
              <AlertDescription>
                Support agents are available {settings?.workingHours.start} - {settings?.workingHours.end} {settings?.workingHours.timezone}
              </AlertDescription>
            </Alert>

            {/* Available Agents */}
            {availableAgents.length > 0 && (
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm">Available Agents</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {availableAgents.slice(0, 2).map((agent) => (
                    <div key={agent.id} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(agent.status)}
                        <span className="text-sm font-medium">{agent.name}</span>
                        <Badge variant="secondary" className="text-xs">
                          {agent.role}
                        </Badge>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {agent.averageResponseTime}min
                      </span>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Reason Selection */}
            <div>
              <Label>Reason for Support</Label>
              <select
                value={escalationReason}
                onChange={(e) => setEscalationReason(e.target.value as EscalationRequest['reason'])}
                className="w-full mt-1 p-2 border rounded-md"
              >
                {settings?.availableReasons.map((reason) => (
                  <option key={reason} value={reason}>
                    {getReasonLabel(reason)}
                  </option>
                ))}
                <option value="custom">Custom</option>
              </select>
            </div>

            {/* Custom Reason */}
            {escalationReason === 'custom' && (
              <div>
                <Label>Describe Your Issue</Label>
                <Textarea
                  value={customReason}
                  onChange={(e) => setCustomReason(e.target.value)}
                  placeholder="Please describe what you need help with..."
                  className="mt-1"
                />
              </div>
            )}

            {/* Priority Selection */}
            <div>
              <Label>Priority</Label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as EscalationRequest['priority'])}
                className="w-full mt-1 p-2 border rounded-md"
              >
                <option value="low">Low - General question</option>
                <option value="medium">Medium - Need assistance</option>
                <option value="high">High - Important issue</option>
                <option value="urgent">Urgent - Critical problem</option>
              </select>
            </div>

            {/* Additional Context */}
            <div>
              <Label>Additional Details (Optional)</Label>
              <Textarea
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                placeholder="Any additional context that might help the agent..."
                className="mt-1"
              />
            </div>

            <div className="flex space-x-2">
              <Button
                onClick={requestEscalation}
                disabled={isLoading || (escalationReason === 'custom' && !customReason.trim())}
                className="flex-1"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                    Requesting...
                  </>
                ) : (
                  <>
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Request Support
                  </>
                )}
              </Button>
              <Button
                variant="outline"
                onClick={() => setShowEscalationForm(false)}
                disabled={isLoading}
              >
                Cancel
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}