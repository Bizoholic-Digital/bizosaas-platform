'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { 
  Bot, 
  Building, 
  Target, 
  Users, 
  CreditCard, 
  CheckCircle,
  ArrowRight,
  ArrowLeft,
  Zap,
  Globe,
  BarChart3,
  Settings,
  Palette,
  Mail
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { useOnboardingWorkflow } from '@/hooks/use-temporal-workflow'
import { cn } from '@/lib/utils'

interface OnboardingStep {
  id: string
  title: string
  description: string
  icon: React.ElementType
}

const steps: OnboardingStep[] = [
  {
    id: 'welcome',
    title: 'Welcome',
    description: 'Get started with BizoSaaS',
    icon: Bot
  },
  {
    id: 'company',
    title: 'Company Info',
    description: 'Tell us about your business',
    icon: Building
  },
  {
    id: 'goals',
    title: 'Marketing Goals',
    description: 'Define your objectives',
    icon: Target
  },
  {
    id: 'integrations',
    title: 'Integrations',
    description: 'Connect your tools',
    icon: Zap
  },
  {
    id: 'team',
    title: 'Team Setup',
    description: 'Invite team members',
    icon: Users
  },
  {
    id: 'complete',
    title: 'Complete',
    description: 'Ready to launch!',
    icon: CheckCircle
  }
]

interface FormData {
  // Company Info
  companyName: string
  industry: string
  companySize: string
  website: string
  description: string
  
  // Marketing Goals
  primaryGoals: string[]
  monthlyBudget: string
  targetAudience: string
  currentChallenges: string[]
  
  // Integrations
  selectedIntegrations: string[]
  
  // Team
  teamMembers: Array<{
    email: string
    role: string
  }>
}

const industries = [
  'Technology', 'Healthcare', 'Finance', 'E-commerce', 'Education',
  'Manufacturing', 'Real Estate', 'Professional Services', 'Other'
]

const companySizes = [
  '1-10 employees', '11-50 employees', '51-200 employees', 
  '201-1000 employees', '1000+ employees'
]

const marketingGoals = [
  'Increase brand awareness',
  'Generate more leads', 
  'Improve conversion rates',
  'Reduce customer acquisition cost',
  'Enhance customer retention',
  'Expand market reach',
  'Automate marketing processes',
  'Improve ROI tracking'
]

const budgetRanges = [
  'Under $1,000', '$1,000 - $5,000', '$5,000 - $10,000',
  '$10,000 - $25,000', '$25,000 - $50,000', 'Over $50,000'
]

const challenges = [
  'Limited marketing budget',
  'Lack of marketing expertise',
  'Time constraints',
  'Difficulty measuring ROI',
  'Poor lead quality',
  'Inconsistent messaging',
  'Manual processes',
  'Data silos'
]

const integrations = [
  { id: 'google-ads', name: 'Google Ads', icon: '🎯' },
  { id: 'meta-ads', name: 'Meta Ads', icon: '📘' },
  { id: 'linkedin', name: 'LinkedIn Marketing', icon: '💼' },
  { id: 'hubspot', name: 'HubSpot CRM', icon: '🧡' },
  { id: 'salesforce', name: 'Salesforce', icon: '☁️' },
  { id: 'mailchimp', name: 'Mailchimp', icon: '📧' },
  { id: 'shopify', name: 'Shopify', icon: '🛒' },
  { id: 'stripe', name: 'Stripe', icon: '💳' }
]

export function OnboardingWizard() {
  const [currentStep, setCurrentStep] = useState(0)
  const [formData, setFormData] = useState<FormData>({
    companyName: '',
    industry: '',
    companySize: '',
    website: '',
    description: '',
    primaryGoals: [],
    monthlyBudget: '',
    targetAudience: '',
    currentChallenges: [],
    selectedIntegrations: [],
    teamMembers: [{ email: '', role: 'Admin' }]
  })
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const { toast } = useToast()
  const { 
    startOnboarding, 
    status: workflowStatus, 
    loading: workflowLoading,
    error: workflowError,
    isCompleted,
    isRunning 
  } = useOnboardingWorkflow()

  const updateFormData = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const toggleArrayField = (field: string, value: string) => {
    const currentArray = formData[field as keyof FormData] as string[]
    if (currentArray.includes(value)) {
      updateFormData(field, currentArray.filter(item => item !== value))
    } else {
      updateFormData(field, [...currentArray, value])
    }
  }

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const previousStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const completeOnboarding = async () => {
    setLoading(true)
    
    try {
      // Start Temporal workflow for comprehensive onboarding automation
      const result = await startOnboarding(formData)
      
      toast({
        title: 'Welcome to BizoSaaS!',
        description: `Onboarding workflow started successfully. ${result.agent_workflows?.length || 0} AI automation workflows are being set up.`,
      })
      
      // Navigate to dashboard with workflow tracking
      const params = new URLSearchParams({
        workflow_id: result.workflow_id,
        onboarding: 'true'
      })
      router.push(`/dashboard?${params}`)
      
    } catch (error) {
      console.error('Onboarding error:', error)
      toast({
        title: 'Setup failed',
        description: workflowError || 'Please try again or contact support.',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const progress = ((currentStep + 1) / steps.length) * 100

  const renderStepContent = () => {
    switch (steps[currentStep].id) {
      case 'welcome':
        return (
          <div className="text-center space-y-6">
            <div className="mx-auto w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center">
              <Bot className="h-10 w-10 text-primary" />
            </div>
            <div>
              <h2 className="text-3xl font-bold mb-4">Welcome to BizoSaaS!</h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Let's get your AI-powered marketing platform set up. This wizard will guide you through 
                the essential steps to configure your account and start automating your marketing.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <div className="text-center p-4">
                <Target className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold">Define Goals</h3>
                <p className="text-sm text-muted-foreground">Set your marketing objectives</p>
              </div>
              <div className="text-center p-4">
                <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold">Connect Tools</h3>
                <p className="text-sm text-muted-foreground">Integrate your existing platforms</p>
              </div>
              <div className="text-center p-4">
                <Bot className="h-8 w-8 text-primary mx-auto mb-2" />
                <h3 className="font-semibold">AI Automation</h3>
                <p className="text-sm text-muted-foreground">Let AI handle your marketing</p>
              </div>
            </div>
          </div>
        )

      case 'company':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <Building className="h-12 w-12 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold mb-2">Tell us about your company</h2>
              <p className="text-muted-foreground">This helps us personalize your experience</p>
            </div>
            
            <div className="grid gap-4 max-w-2xl mx-auto">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="companyName">Company Name *</Label>
                  <Input
                    id="companyName"
                    value={formData.companyName}
                    onChange={(e) => updateFormData('companyName', e.target.value)}
                    placeholder="Your company name"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="website">Website URL</Label>
                  <Input
                    id="website"
                    value={formData.website}
                    onChange={(e) => updateFormData('website', e.target.value)}
                    placeholder="https://yourcompany.com"
                  />
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Industry *</Label>
                  <Select value={formData.industry} onValueChange={(value) => updateFormData('industry', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select industry" />
                    </SelectTrigger>
                    <SelectContent>
                      {industries.map((industry) => (
                        <SelectItem key={industry} value={industry}>
                          {industry}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Company Size *</Label>
                  <Select value={formData.companySize} onValueChange={(value) => updateFormData('companySize', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select company size" />
                    </SelectTrigger>
                    <SelectContent>
                      {companySizes.map((size) => (
                        <SelectItem key={size} value={size}>
                          {size}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="description">Company Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => updateFormData('description', e.target.value)}
                  placeholder="Brief description of your business and what you do..."
                  rows={3}
                />
              </div>
            </div>
          </div>
        )

      case 'goals':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <Target className="h-12 w-12 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold mb-2">What are your marketing goals?</h2>
              <p className="text-muted-foreground">Select all that apply to help us configure your AI agents</p>
            </div>
            
            <div className="max-w-3xl mx-auto space-y-6">
              <div>
                <Label className="text-base font-medium">Primary Goals *</Label>
                <div className="grid md:grid-cols-2 gap-3 mt-3">
                  {marketingGoals.map((goal) => (
                    <div key={goal} className="flex items-center space-x-2">
                      <Checkbox
                        id={goal}
                        checked={formData.primaryGoals.includes(goal)}
                        onCheckedChange={() => toggleArrayField('primaryGoals', goal)}
                      />
                      <Label htmlFor={goal} className="text-sm font-normal">
                        {goal}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Monthly Marketing Budget</Label>
                  <Select value={formData.monthlyBudget} onValueChange={(value) => updateFormData('monthlyBudget', value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select budget range" />
                    </SelectTrigger>
                    <SelectContent>
                      {budgetRanges.map((range) => (
                        <SelectItem key={range} value={range}>
                          {range}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="targetAudience">Target Audience</Label>
                  <Input
                    id="targetAudience"
                    value={formData.targetAudience}
                    onChange={(e) => updateFormData('targetAudience', e.target.value)}
                    placeholder="e.g., Small business owners, B2B professionals"
                  />
                </div>
              </div>
              
              <div>
                <Label className="text-base font-medium">Current Challenges</Label>
                <div className="grid md:grid-cols-2 gap-3 mt-3">
                  {challenges.map((challenge) => (
                    <div key={challenge} className="flex items-center space-x-2">
                      <Checkbox
                        id={challenge}
                        checked={formData.currentChallenges.includes(challenge)}
                        onCheckedChange={() => toggleArrayField('currentChallenges', challenge)}
                      />
                      <Label htmlFor={challenge} className="text-sm font-normal">
                        {challenge}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )

      case 'integrations':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <Zap className="h-12 w-12 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold mb-2">Connect your tools</h2>
              <p className="text-muted-foreground">Select the platforms you want to integrate with BizoSaaS</p>
            </div>
            
            <div className="max-w-4xl mx-auto">
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                {integrations.map((integration) => (
                  <Card 
                    key={integration.id}
                    className={cn(
                      "cursor-pointer transition-all hover:shadow-md",
                      formData.selectedIntegrations.includes(integration.id) 
                        ? "ring-2 ring-primary bg-primary/5" 
                        : "hover:bg-accent/50"
                    )}
                    onClick={() => toggleArrayField('selectedIntegrations', integration.id)}
                  >
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl mb-2">{integration.icon}</div>
                      <h3 className="font-medium text-sm">{integration.name}</h3>
                      {formData.selectedIntegrations.includes(integration.id) && (
                        <CheckCircle className="h-4 w-4 text-primary mx-auto mt-2" />
                      )}
                    </CardContent>
                  </Card>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-muted/50 rounded-lg">
                <p className="text-sm text-muted-foreground text-center">
                  Don't worry if your platform isn't listed. You can add more integrations later 
                  from your dashboard settings.
                </p>
              </div>
            </div>
          </div>
        )

      case 'team':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <Users className="h-12 w-12 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold mb-2">Invite your team</h2>
              <p className="text-muted-foreground">Add team members to collaborate on your marketing campaigns</p>
            </div>
            
            <div className="max-w-2xl mx-auto space-y-4">
              {formData.teamMembers.map((member, index) => (
                <div key={index} className="grid md:grid-cols-3 gap-4 p-4 border rounded-lg">
                  <div className="md:col-span-2">
                    <Input
                      placeholder="Email address"
                      value={member.email}
                      onChange={(e) => {
                        const newMembers = [...formData.teamMembers]
                        newMembers[index].email = e.target.value
                        updateFormData('teamMembers', newMembers)
                      }}
                    />
                  </div>
                  <Select 
                    value={member.role} 
                    onValueChange={(value) => {
                      const newMembers = [...formData.teamMembers]
                      newMembers[index].role = value
                      updateFormData('teamMembers', newMembers)
                    }}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Admin">Admin</SelectItem>
                      <SelectItem value="Manager">Manager</SelectItem>
                      <SelectItem value="Analyst">Analyst</SelectItem>
                      <SelectItem value="Viewer">Viewer</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              ))}
              
              <Button
                variant="outline"
                onClick={() => updateFormData('teamMembers', [...formData.teamMembers, { email: '', role: 'Viewer' }])}
                className="w-full"
              >
                + Add Another Team Member
              </Button>
              
              <div className="p-4 bg-muted/50 rounded-lg">
                <p className="text-sm text-muted-foreground">
                  Team members will receive an invitation email to join your BizoSaaS workspace.
                  You can always add more members later.
                </p>
              </div>
            </div>
          </div>
        )

      case 'complete':
        return (
          <div className="text-center space-y-6">
            <div className="mx-auto w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
              <CheckCircle className="h-10 w-10 text-green-600" />
            </div>
            <div>
              <h2 className="text-3xl font-bold mb-4">You're all set!</h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Your BizoSaaS account has been configured. Our AI agents are ready to start 
                optimizing your marketing campaigns.
              </p>
            </div>

            {/* Temporal Workflow Status */}
            {workflowStatus && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-blue-900">Automation Setup Progress</h4>
                  <Badge variant={isCompleted ? "default" : isRunning ? "secondary" : "destructive"}>
                    {workflowStatus.status}
                  </Badge>
                </div>
                <Progress value={workflowStatus.progress} className="mb-2" />
                <p className="text-sm text-blue-700">
                  Current: {workflowStatus.current_step} ({workflowStatus.progress}% complete)
                </p>
                {workflowStatus.completed_steps.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-blue-600 mb-1">Completed steps:</p>
                    <div className="flex flex-wrap gap-1">
                      {workflowStatus.completed_steps.map((step, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {step}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
            
            <div className="grid md:grid-cols-3 gap-4 max-w-3xl mx-auto">
              <Card>
                <CardContent className="p-4 text-center">
                  <Bot className="h-8 w-8 text-primary mx-auto mb-2" />
                  <h3 className="font-semibold mb-1">AI Agents Activated</h3>
                  <p className="text-sm text-muted-foreground">12 specialized agents ready</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
                  <h3 className="font-semibold mb-1">Integrations Connected</h3>
                  <p className="text-sm text-muted-foreground">{formData.selectedIntegrations.length} platforms linked</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <Users className="h-8 w-8 text-primary mx-auto mb-2" />
                  <h3 className="font-semibold mb-1">Team Invited</h3>
                  <p className="text-sm text-muted-foreground">{formData.teamMembers.filter(m => m.email).length} members added</p>
                </CardContent>
              </Card>
            </div>
            
            <div className="bg-gradient-to-r from-primary/10 to-accent/10 rounded-lg p-6">
              <h3 className="font-semibold mb-2">What's next?</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Explore your dashboard and AI agents</li>
                <li>• Create your first automated campaign</li>
                <li>• Review real-time analytics and insights</li>
              </ul>
            </div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Bot className="h-6 w-6 text-primary" />
            <span className="font-semibold">BizoSaaS Setup</span>
          </div>
          <Badge variant="outline">
            Step {currentStep + 1} of {steps.length}
          </Badge>
        </div>
        
        <Progress value={progress} className="h-2" />
        
        <div className="flex justify-between mt-4 text-sm text-muted-foreground">
          {steps.map((step, index) => (
            <div key={step.id} className="flex flex-col items-center space-y-2">
              <div 
                className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center",
                  index <= currentStep ? "bg-primary text-primary-foreground" : "bg-muted"
                )}
              >
                {index < currentStep ? (
                  <CheckCircle className="h-4 w-4" />
                ) : (
                  <step.icon className="h-4 w-4" />
                )}
              </div>
              <span className="hidden md:block text-xs">{step.title}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Step Content */}
      <Card className="mb-8">
        <CardContent className="p-8">
          {renderStepContent()}
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={previousStep}
          disabled={currentStep === 0}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Previous
        </Button>
        
        <div className="flex items-center space-x-2">
          {currentStep < steps.length - 1 ? (
            <Button onClick={nextStep}>
              Next
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button 
              onClick={completeOnboarding} 
              disabled={loading}
              className="bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90"
            >
              {loading ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent mr-2" />
                  Setting up...
                </>
              ) : (
                <>
                  Complete Setup
                  <CheckCircle className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}