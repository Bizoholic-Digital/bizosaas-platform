'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { CheckCircle, Circle, Clock, AlertTriangle, ExternalLink, Shield } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'

interface OnboardingData {
  company_name: string
  contact_email: string
  website: string
  phone?: string
  industry?: string
  monthly_budget?: number
  primary_goals: string[]
}

interface OnboardingStatus {
  workflow_id: string
  current_stage: string
  completion_percentage: number
  human_review_required: boolean
  estimated_value?: number
  validations: Record<string, string>
  created_at: string
  updated_at: string
}

const ONBOARDING_STAGES = {
  initial_capture: {
    title: "Basic Information",
    description: "Collecting and validating company details",
    icon: Circle
  },
  basic_validation: {
    title: "Data Enrichment", 
    description: "AI analysis of your website and business",
    icon: Clock
  },
  company_verification: {
    title: "Business Verification",
    description: "Verifying business presence and legitimacy",
    icon: Shield
  },
  credential_linking: {
    title: "Platform Connections",
    description: "Connecting your marketing accounts",
    icon: ExternalLink
  },
  comprehensive_data: {
    title: "Historical Analysis",
    description: "Analyzing your marketing performance data",
    icon: Clock
  },
  human_validation: {
    title: "Expert Review",
    description: "High-value account expert validation",
    icon: AlertTriangle
  },
  setup_completion: {
    title: "Completion",
    description: "Finalizing setup and generating strategy",
    icon: CheckCircle
  }
}

export function OnboardingWorkflow() {
  const [currentStep, setCurrentStep] = useState('initial_capture')
  const [onboardingData, setOnboardingData] = useState<OnboardingData>({
    company_name: '',
    contact_email: '',
    website: '',
    phone: '',
    industry: '',
    monthly_budget: undefined,
    primary_goals: []
  })
  const [status, setStatus] = useState<OnboardingStatus | null>(null)
  const [workflowId, setWorkflowId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const industries = [
    'Technology', 'E-commerce', 'Healthcare', 'Finance', 'Education',
    'Retail', 'Services', 'Manufacturing', 'Real Estate', 'Other'
  ]

  const goalOptions = [
    'Increase lead generation', 'Improve brand awareness', 'Boost sales',
    'Reduce customer acquisition cost', 'Expand market reach', 'Improve ROI'
  ]

  useEffect(() => {
    if (workflowId) {
      const interval = setInterval(async () => {
        await fetchWorkflowStatus()
      }, 10000) // Poll every 10 seconds

      return () => clearInterval(interval)
    }
  }, [workflowId])

  const startOnboarding = async () => {
    if (!onboardingData.company_name || !onboardingData.contact_email || !onboardingData.website) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields",
        variant: "destructive"
      })
      return
    }

    setIsLoading(true)
    try {
      const response = await fetch('/api/business-logic/onboarding/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(onboardingData)
      })

      const result = await response.json()
      if (result.success) {
        setWorkflowId(result.workflow_id)
        setCurrentStep('basic_validation')
        toast({
          title: "Onboarding Started",
          description: "Your onboarding workflow has begun!",
        })
        await fetchWorkflowStatus()
      } else {
        throw new Error(result.message || 'Failed to start onboarding')
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to start onboarding",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  const fetchWorkflowStatus = async () => {
    if (!workflowId) return

    try {
      const response = await fetch(`/api/business-logic/onboarding/${workflowId}/status`)
      const result = await response.json()
      
      if (result.success) {
        setStatus(result.workflow_status)
        setCurrentStep(result.workflow_status.current_stage)
      }
    } catch (error) {
      console.error('Failed to fetch workflow status:', error)
    }
  }

  const handleGoalToggle = (goal: string) => {
    const newGoals = onboardingData.primary_goals.includes(goal)
      ? onboardingData.primary_goals.filter(g => g !== goal)
      : [...onboardingData.primary_goals, goal]
    
    setOnboardingData(prev => ({ ...prev, primary_goals: newGoals }))
  }

  const getStageStatus = (stage: string) => {
    const stages = Object.keys(ONBOARDING_STAGES)
    const currentIndex = stages.indexOf(currentStep)
    const stageIndex = stages.indexOf(stage)
    
    if (stageIndex < currentIndex) return 'completed'
    if (stageIndex === currentIndex) return 'current'
    return 'pending'
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Progress Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">Client Onboarding</CardTitle>
              <CardDescription>
                Progressive data collection with validation and verification
              </CardDescription>
            </div>
            <Badge variant={status?.human_review_required ? "destructive" : "default"}>
              {status?.human_review_required ? "Expert Review Required" : "Automated Process"}
            </Badge>
          </div>
          {status && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>Progress: {Math.round(status.completion_percentage)}%</span>
                {status.estimated_value && (
                  <span>Estimated Value: ${status.estimated_value.toLocaleString()}/month</span>
                )}
              </div>
              <Progress value={status.completion_percentage} className="w-full" />
            </div>
          )}
        </CardHeader>
      </Card>

      {/* Onboarding Stages */}
      <Card>
        <CardHeader>
          <CardTitle>Onboarding Progress</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(ONBOARDING_STAGES).map(([stage, config]) => {
              const stageStatus = getStageStatus(stage)
              const Icon = config.icon
              
              return (
                <div key={stage} className={`flex items-center space-x-3 p-3 rounded-lg border ${
                  stageStatus === 'current' ? 'border-blue-200 bg-blue-50' :
                  stageStatus === 'completed' ? 'border-green-200 bg-green-50' :
                  'border-gray-200'
                }`}>
                  <div className={`p-2 rounded-full ${
                    stageStatus === 'completed' ? 'bg-green-100 text-green-600' :
                    stageStatus === 'current' ? 'bg-blue-100 text-blue-600' :
                    'bg-gray-100 text-gray-400'
                  }`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">{config.title}</h4>
                    <p className="text-sm text-muted-foreground">{config.description}</p>
                  </div>
                  <div>
                    {stageStatus === 'completed' && (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    )}
                    {stageStatus === 'current' && (
                      <Clock className="w-5 h-5 text-blue-500 animate-spin" />
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Initial Data Collection Form */}
      {!workflowId && (
        <Card>
          <CardHeader>
            <CardTitle>Company Information</CardTitle>
            <CardDescription>
              Tell us about your company to get started with our AI-powered marketing platform
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="company_name">Company Name *</Label>
                <Input
                  id="company_name"
                  value={onboardingData.company_name}
                  onChange={(e) => setOnboardingData(prev => ({ ...prev, company_name: e.target.value }))}
                  placeholder="Your company name"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="contact_email">Contact Email *</Label>
                <Input
                  id="contact_email"
                  type="email"
                  value={onboardingData.contact_email}
                  onChange={(e) => setOnboardingData(prev => ({ ...prev, contact_email: e.target.value }))}
                  placeholder="your@company.com"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="website">Website *</Label>
                <Input
                  id="website"
                  value={onboardingData.website}
                  onChange={(e) => setOnboardingData(prev => ({ ...prev, website: e.target.value }))}
                  placeholder="https://yourcompany.com"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  value={onboardingData.phone || ''}
                  onChange={(e) => setOnboardingData(prev => ({ ...prev, phone: e.target.value }))}
                  placeholder="+1 (555) 123-4567"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="industry">Industry</Label>
                <select
                  id="industry"
                  className="w-full p-2 border border-gray-300 rounded-md"
                  value={onboardingData.industry || ''}
                  onChange={(e) => setOnboardingData(prev => ({ ...prev, industry: e.target.value }))}
                >
                  <option value="">Select an industry</option>
                  {industries.map(industry => (
                    <option key={industry} value={industry}>{industry}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="monthly_budget">Monthly Marketing Budget</Label>
                <Input
                  id="monthly_budget"
                  type="number"
                  value={onboardingData.monthly_budget || ''}
                  onChange={(e) => setOnboardingData(prev => ({ 
                    ...prev, 
                    monthly_budget: e.target.value ? parseFloat(e.target.value) : undefined 
                  }))}
                  placeholder="5000"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label>Primary Marketing Goals</Label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {goalOptions.map(goal => (
                  <Button
                    key={goal}
                    type="button"
                    variant={onboardingData.primary_goals.includes(goal) ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleGoalToggle(goal)}
                    className="justify-start"
                  >
                    {goal}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button onClick={startOnboarding} disabled={isLoading} className="w-full">
              {isLoading ? "Starting Onboarding..." : "Start Onboarding Process"}
            </Button>
          </CardFooter>
        </Card>
      )}

      {/* Status and Next Steps */}
      {status && (
        <Card>
          <CardHeader>
            <CardTitle>Current Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {status.human_review_required && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Your account has been flagged for expert review due to its high value potential 
                  (${status.estimated_value?.toLocaleString()}/month). Our specialists will personally 
                  ensure optimal setup for maximum performance.
                </AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <h4 className="font-medium">Next Steps:</h4>
              <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
                {currentStep === 'basic_validation' && (
                  <li>Our AI is analyzing your website and business model</li>
                )}
                {currentStep === 'company_verification' && (
                  <li>Verifying your business presence across digital platforms</li>
                )}
                {currentStep === 'credential_linking' && (
                  <li>You'll be prompted to connect your marketing platform accounts</li>
                )}
                {currentStep === 'comprehensive_data' && (
                  <li>Collecting historical performance data from connected platforms</li>
                )}
                {currentStep === 'human_validation' && (
                  <li>Expert review in progress - you'll be contacted within 24 hours</li>
                )}
              </ul>
            </div>

            <div className="text-xs text-muted-foreground">
              Workflow ID: {status.workflow_id} | Started: {new Date(status.created_at).toLocaleString()}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}