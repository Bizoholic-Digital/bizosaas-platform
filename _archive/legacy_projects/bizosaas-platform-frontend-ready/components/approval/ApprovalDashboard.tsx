'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Progress } from '@/components/ui/progress'
import { 
  CheckCircle, X, Clock, AlertTriangle, Settings, Eye, 
  TrendingUp, Shield, Zap, User
} from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'

interface ApprovalRequest {
  request_id: string
  decision_type: string
  impact_level: string
  confidence_score: number
  ai_reasoning: string
  urgency_level: string
  created_at: string
  expires_at?: string
}

interface ApprovalDashboard {
  current_mode: string
  pending_approvals: number
  approval_statistics: {
    pending: number
    approved: number
    rejected: number
    auto_approved: number
    average_approval_time_hours: number
  }
  recent_decisions: any[]
  mode_recommendations: any[]
}

const APPROVAL_MODES = {
  manual: {
    title: "Manual Mode",
    description: "100% human oversight - all decisions require manual approval",
    icon: User,
    color: "text-red-500",
    bgColor: "bg-red-50 border-red-200"
  },
  semi_auto: {
    title: "Semi-Auto Mode", 
    description: "Strategic decisions require approval - routine optimizations automated",
    icon: Shield,
    color: "text-yellow-500",
    bgColor: "bg-yellow-50 border-yellow-200"
  },
  fully_auto: {
    title: "Fully-Auto Mode",
    description: "Complete AI autonomy with full transparency and monitoring",
    icon: Zap,
    color: "text-green-500",
    bgColor: "bg-green-50 border-green-200"
  }
}

const IMPACT_LEVELS = {
  low: { label: "Low Impact", color: "text-green-600 bg-green-100" },
  medium: { label: "Medium Impact", color: "text-yellow-600 bg-yellow-100" },
  high: { label: "High Impact", color: "text-orange-600 bg-orange-100" },
  critical: { label: "Critical Impact", color: "text-red-600 bg-red-100" }
}

export function ApprovalDashboard() {
  const [currentMode, setCurrentMode] = useState<string>('manual')
  const [dashboardData, setDashboardData] = useState<ApprovalDashboard | null>(null)
  const [pendingRequests, setPendingRequests] = useState<ApprovalRequest[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedRequest, setSelectedRequest] = useState<ApprovalRequest | null>(null)
  const { toast } = useToast()

  useEffect(() => {
    fetchDashboardData()
    fetchPendingApprovals()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('/api/business-logic/approval/dashboard')
      const result = await response.json()
      
      if (result.success) {
        setDashboardData(result.dashboard)
        setCurrentMode(result.dashboard.current_mode)
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    }
  }

  const fetchPendingApprovals = async () => {
    try {
      const response = await fetch('/api/business-logic/approval/pending')
      const result = await response.json()
      
      if (result.success) {
        setPendingRequests(result.pending_approvals)
      }
    } catch (error) {
      console.error('Failed to fetch pending approvals:', error)
    }
  }

  const switchApprovalMode = async (newMode: string, reason?: string) => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/business-logic/approval/mode/switch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_mode: newMode, reason })
      })

      const result = await response.json()
      if (result.success) {
        setCurrentMode(newMode)
        toast({
          title: "Mode Switched",
          description: `Approval mode changed to ${APPROVAL_MODES[newMode as keyof typeof APPROVAL_MODES].title}`,
        })
        await fetchDashboardData()
      } else {
        throw new Error(result.message || 'Failed to switch mode')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to switch approval mode",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const approveRequest = async (requestId: string) => {
    try {
      const response = await fetch(`/api/business-logic/approval/${requestId}/approve`, {
        method: 'POST'
      })

      const result = await response.json()
      if (result.success) {
        toast({
          title: "Request Approved",
          description: "The decision has been approved and will be executed",
        })
        await fetchPendingApprovals()
        await fetchDashboardData()
        setSelectedRequest(null)
      } else {
        throw new Error(result.message || 'Failed to approve request')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to approve request",
        variant: "destructive"
      })
    }
  }

  const rejectRequest = async (requestId: string, reason: string) => {
    try {
      const response = await fetch(`/api/business-logic/approval/${requestId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rejection_reason: reason })
      })

      const result = await response.json()
      if (result.success) {
        toast({
          title: "Request Rejected",
          description: "The decision has been rejected",
        })
        await fetchPendingApprovals()
        await fetchDashboardData()
        setSelectedRequest(null)
      } else {
        throw new Error(result.message || 'Failed to reject request')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to reject request",
        variant: "destructive"
      })
    }
  }

  const formatDecisionType = (type: string) => {
    return type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
  }

  const getTimeRemaining = (expiresAt: string) => {
    const expiry = new Date(expiresAt)
    const now = new Date()
    const hoursRemaining = Math.max(0, (expiry.getTime() - now.getTime()) / (1000 * 60 * 60))
    return Math.round(hoursRemaining)
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">Approval System Dashboard</CardTitle>
              <CardDescription>
                Three-tier approval system with dynamic mode switching
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Settings className="w-5 h-5 text-muted-foreground" />
              <Badge variant="outline">
                {APPROVAL_MODES[currentMode as keyof typeof APPROVAL_MODES]?.title || currentMode}
              </Badge>
            </div>
          </div>
        </CardHeader>
      </Card>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="pending" className="relative">
            Pending Approvals
            {pendingRequests.length > 0 && (
              <Badge className="ml-2 h-5 w-5 rounded-full p-0 text-xs">
                {pendingRequests.length}
              </Badge>
            )}
          </TabsTrigger>
          <TabsTrigger value="settings">Mode Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* Statistics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Pending</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-600">
                  {dashboardData?.approval_statistics.pending || 0}
                </div>
                <p className="text-xs text-muted-foreground">Awaiting decision</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Approved</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  {dashboardData?.approval_statistics.approved || 0}
                </div>
                <p className="text-xs text-muted-foreground">Last 30 days</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Auto-Approved</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">
                  {dashboardData?.approval_statistics.auto_approved || 0}
                </div>
                <p className="text-xs text-muted-foreground">AI decisions</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Avg. Time</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {Math.round(dashboardData?.approval_statistics.average_approval_time_hours || 0)}h
                </div>
                <p className="text-xs text-muted-foreground">To approval</p>
              </CardContent>
            </Card>
          </div>

          {/* Current Mode Status */}
          <Card>
            <CardHeader>
              <CardTitle>Current Approval Mode</CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`p-4 rounded-lg border-2 ${APPROVAL_MODES[currentMode as keyof typeof APPROVAL_MODES]?.bgColor}`}>
                <div className="flex items-center space-x-3">
                  {(() => {
                    const ModeIcon = APPROVAL_MODES[currentMode as keyof typeof APPROVAL_MODES]?.icon
                    return ModeIcon ? <ModeIcon className={`w-6 h-6 ${APPROVAL_MODES[currentMode as keyof typeof APPROVAL_MODES]?.color}`} /> : null
                  })()}
                  <div>
                    <h3 className="font-semibold">
                      {APPROVAL_MODES[currentMode as keyof typeof APPROVAL_MODES]?.title}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {APPROVAL_MODES[currentMode as keyof typeof APPROVAL_MODES]?.description}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pending" className="space-y-6">
          {pendingRequests.length === 0 ? (
            <Card>
              <CardContent className="py-8 text-center">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                <h3 className="text-lg font-semibold mb-2">No Pending Approvals</h3>
                <p className="text-muted-foreground">All decisions are up to date!</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {pendingRequests.map((request) => (
                <Card key={request.request_id} className="border-l-4 border-l-orange-500">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <CardTitle className="text-lg">
                          {formatDecisionType(request.decision_type)}
                        </CardTitle>
                        <Badge className={IMPACT_LEVELS[request.impact_level as keyof typeof IMPACT_LEVELS]?.color}>
                          {IMPACT_LEVELS[request.impact_level as keyof typeof IMPACT_LEVELS]?.label}
                        </Badge>
                        <Badge variant={request.urgency_level === 'high' ? 'destructive' : 'secondary'}>
                          {request.urgency_level.charAt(0).toUpperCase() + request.urgency_level.slice(1)} Priority
                        </Badge>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {request.expires_at && (
                          <span>Expires in {getTimeRemaining(request.expires_at)}h</span>
                        )}
                      </div>
                    </div>
                    <CardDescription>
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <span className="font-medium">AI Confidence:</span>
                          <Progress value={request.confidence_score * 100} className="w-24" />
                          <span className="text-sm">{Math.round(request.confidence_score * 100)}%</span>
                        </div>
                        <div>
                          <span className="font-medium">Reasoning:</span> {request.ai_reasoning}
                        </div>
                      </div>
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex space-x-2">
                      <Button 
                        size="sm" 
                        onClick={() => approveRequest(request.request_id)}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Approve
                      </Button>
                      <Button 
                        size="sm" 
                        variant="destructive"
                        onClick={() => rejectRequest(request.request_id, "Manual rejection")}
                      >
                        <X className="w-4 h-4 mr-2" />
                        Reject
                      </Button>
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => setSelectedRequest(request)}
                      >
                        <Eye className="w-4 h-4 mr-2" />
                        View Details
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="settings" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Approval Mode Settings</CardTitle>
              <CardDescription>
                Switch between different approval modes based on your comfort level with AI automation
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {Object.entries(APPROVAL_MODES).map(([mode, config]) => {
                const Icon = config.icon
                const isCurrentMode = mode === currentMode
                
                return (
                  <div 
                    key={mode}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      isCurrentMode ? config.bgColor : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <Icon className={`w-6 h-6 ${isCurrentMode ? config.color : 'text-gray-400'}`} />
                        <div>
                          <h3 className="font-semibold">{config.title}</h3>
                          <p className="text-sm text-muted-foreground">{config.description}</p>
                        </div>
                      </div>
                      {!isCurrentMode && (
                        <Button 
                          onClick={() => switchApprovalMode(mode)}
                          disabled={isLoading}
                        >
                          Switch to {config.title}
                        </Button>
                      )}
                      {isCurrentMode && (
                        <Badge>Current Mode</Badge>
                      )}
                    </div>
                  </div>
                )
              })}
            </CardContent>
          </Card>

          {/* Mode Benefits */}
          <Card>
            <CardHeader>
              <CardTitle>Mode Benefits & Recommendations</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Alert>
                <TrendingUp className="h-4 w-4" />
                <AlertDescription>
                  <strong>Recommendation:</strong> Start with Manual Mode for the first month to build trust, 
                  then gradually move to Semi-Auto Mode as you become comfortable with AI recommendations. 
                  Fully-Auto Mode is ideal for established accounts with consistent performance.
                </AlertDescription>
              </Alert>

              <div className="grid md:grid-cols-3 gap-4">
                <div className="p-3 border rounded-lg">
                  <h4 className="font-semibold text-red-600 mb-2">Manual Mode</h4>
                  <ul className="text-sm space-y-1 text-muted-foreground">
                    <li>• Complete control over all decisions</li>
                    <li>• Perfect for new accounts</li>
                    <li>• Learn AI reasoning patterns</li>
                    <li>• Build confidence gradually</li>
                  </ul>
                </div>

                <div className="p-3 border rounded-lg">
                  <h4 className="font-semibold text-yellow-600 mb-2">Semi-Auto Mode</h4>
                  <ul className="text-sm space-y-1 text-muted-foreground">
                    <li>• Balance of control and efficiency</li>
                    <li>• Strategic decisions need approval</li>
                    <li>• Routine optimizations automated</li>
                    <li>• Ideal for most businesses</li>
                  </ul>
                </div>

                <div className="p-3 border rounded-lg">
                  <h4 className="font-semibold text-green-600 mb-2">Fully-Auto Mode</h4>
                  <ul className="text-sm space-y-1 text-muted-foreground">
                    <li>• Maximum efficiency and speed</li>
                    <li>• Complete transparency logging</li>
                    <li>• Best for established accounts</li>
                    <li>• 24/7 optimization capability</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}