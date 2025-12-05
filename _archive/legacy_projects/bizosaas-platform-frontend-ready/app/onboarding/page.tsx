'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, Clock, AlertCircle, Zap, Target, Rocket } from 'lucide-react'
import { BusinessProfileStep } from '@/components/onboarding/business-profile-step'
import { IntegrationSetupStep } from '@/components/onboarding/integration-setup-step'
import { SuccessStep } from '@/components/onboarding/success-step'

const ONBOARDING_STEPS = [
  {
    id: 'business-profile',
    title: 'Business Profile',
    description: 'Tell us about your business goals and target audience',
    icon: Target
  },
  {
    id: 'integrations',
    title: 'Connect Platforms',
    description: 'Connect your marketing and payment platforms',
    icon: Zap
  },
  {
    id: 'success',
    title: 'Ready to Launch',
    description: 'Your AI marketing system is ready to go!',
    icon: Rocket
  }
]

const TIER_STATUS = {
  tier1: { label: 'Instant Access', color: 'bg-green-500', icon: CheckCircle },
  tier2: { label: 'Quick Setup (2-7 Days)', color: 'bg-yellow-500', icon: Clock },
  tier3: { label: 'Application Process (2-4 Weeks)', color: 'bg-orange-500', icon: AlertCircle }
}

export default function OnboardingPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState(new Set<number>())
  const [businessData, setBusinessData] = useState<any>({})
  const [integrationData, setIntegrationData] = useState<any>({})

  const currentStepData = ONBOARDING_STEPS[currentStep]
  const progress = ((completedSteps.size / ONBOARDING_STEPS.length) * 100)

  const handleStepComplete = (stepIndex: number, data: any) => {
    setCompletedSteps(new Set(Array.from(completedSteps).concat([stepIndex])))
    
    if (stepIndex === 0) {
      setBusinessData(data)
    } else if (stepIndex === 1) {
      setIntegrationData(data)
    }

    if (stepIndex < ONBOARDING_STEPS.length - 1) {
      setCurrentStep(stepIndex + 1)
    }
  }

  const renderCurrentStep = () => {
    switch (currentStepData.id) {
      case 'business-profile':
        return (
          <BusinessProfileStep
            onComplete={(data) => handleStepComplete(0, data)}
            initialData={businessData}
          />
        )
      case 'integrations':
        return (
          <IntegrationSetupStep
            businessData={businessData}
            onComplete={(data) => handleStepComplete(1, data)}
            initialData={integrationData}
          />
        )
      case 'success':
        return (
          <SuccessStep
            businessData={businessData}
            integrationData={integrationData}
            onComplete={() => {
              // Redirect based on credential strategy
              if (businessData.credentialStrategy === 'bring_your_own_key') {
                router.push('/dashboard/byok?onboarding=true');
              } else {
                router.push('/dashboard');
              }
            }}
          />
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <div className="border-b bg-white/80 backdrop-blur dark:bg-slate-900/80">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-sm">
                B
              </div>
              <div>
                <h1 className="text-xl font-bold">BizoSaaS Onboarding</h1>
                <p className="text-sm text-muted-foreground">Set up your AI marketing platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm font-medium">
                Step {currentStep + 1} of {ONBOARDING_STEPS.length}
              </div>
              <Progress value={progress} className="w-32" />
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="mx-auto max-w-4xl">
          {/* Step Navigation */}
          <div className="mb-8">
            <div className="flex items-center justify-between">
              {ONBOARDING_STEPS.map((step, index) => {
                const StepIcon = step.icon
                const isCompleted = completedSteps.has(index)
                const isCurrent = index === currentStep
                
                return (
                  <div key={step.id} className="flex flex-col items-center space-y-2">
                    <div className={`
                      flex h-12 w-12 items-center justify-center rounded-full border-2 transition-all
                      ${isCompleted 
                        ? 'border-green-500 bg-green-500 text-white' 
                        : isCurrent 
                          ? 'border-blue-500 bg-blue-500 text-white' 
                          : 'border-gray-300 bg-white text-gray-400 dark:border-gray-600 dark:bg-slate-800'
                      }
                    `}>
                      <StepIcon className="h-5 w-5" />
                    </div>
                    <div className="text-center">
                      <div className="text-sm font-medium">{step.title}</div>
                      <div className="text-xs text-muted-foreground max-w-24">{step.description}</div>
                    </div>
                    {index < ONBOARDING_STEPS.length - 1 && (
                      <div className={`
                        absolute h-px w-24 translate-x-16 translate-y-6
                        ${isCompleted ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'}
                      `} />
                    )}
                  </div>
                )
              })}
            </div>
          </div>

          {/* Integration Tier Overview */}
          {currentStep === 1 && (
            <Card className="mb-6 border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950/30">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-blue-900 dark:text-blue-100">
                  <Zap className="h-5 w-5" />
                  Integration Timeline
                </CardTitle>
                <CardDescription className="text-blue-700 dark:text-blue-300">
                  We've organized integrations by setup speed to get you value immediately
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.entries({
                    'Tier 1': {
                      platforms: ['Stripe', 'Basic Analytics', 'Email Marketing'],
                      ...TIER_STATUS.tier1
                    },
                    'Tier 2': {
                      platforms: ['Google Ads', 'Meta Ads', 'E-commerce'],
                      ...TIER_STATUS.tier2
                    },
                    'Tier 3': {
                      platforms: ['LinkedIn Ads', 'TikTok Ads', 'Advanced AI'],
                      ...TIER_STATUS.tier3
                    }
                  }).map(([tier, info]) => {
                    const StatusIcon = info.icon
                    return (
                      <div key={tier} className="flex items-start gap-3 p-3 rounded-lg bg-white/60 dark:bg-slate-800/60">
                        <div className={`flex h-8 w-8 items-center justify-center rounded-full ${info.color} text-white`}>
                          <StatusIcon className="h-4 w-4" />
                        </div>
                        <div className="flex-1">
                          <Badge variant="outline" className="mb-2">{info.label}</Badge>
                          <div className="space-y-1">
                            {info.platforms.map((platform) => (
                              <div key={platform} className="text-sm text-muted-foreground">
                                • {platform}
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Main Content */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-3">
                <currentStepData.icon className="h-6 w-6 text-blue-600" />
                {currentStepData.title}
              </CardTitle>
              <CardDescription>
                {currentStepData.description}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {renderCurrentStep()}
            </CardContent>
          </Card>

          {/* Support */}
          <div className="mt-8 text-center">
            <p className="text-sm text-muted-foreground">
              Need help? <Button variant="link" className="p-0 h-auto">Contact our onboarding specialists</Button>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}