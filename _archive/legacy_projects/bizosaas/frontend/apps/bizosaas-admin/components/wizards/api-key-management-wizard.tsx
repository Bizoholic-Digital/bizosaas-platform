"use client"

import React, { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '../ui/card'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'
import { Progress } from '../ui/progress'
import { 
  ShieldCheck, 
  Key, 
  Monitor, 
  AlertTriangle, 
  CheckCircle, 
  XCircle,
  Lock,
  Zap,
  Globe,
  Database,
  Eye,
  EyeOff
} from 'lucide-react'
import { cn } from '../../lib/utils'

// Import step components
import { ServiceSelectionStep } from './steps/service-selection-step'
import { SecurityConfigurationStep } from './steps/security-configuration-step'
import { KeyGenerationStep } from './steps/key-generation-step'
import { TestingVerificationStep } from './steps/testing-verification-step'
import { MonitoringSetupStep } from './steps/monitoring-setup-step'
import { DocumentationDeploymentStep } from './steps/documentation-deployment-step'

// Types
export interface APIService {
  id: string
  name: string
  category: 'payment' | 'marketing' | 'ai' | 'analytics' | 'infrastructure'
  icon: React.ReactNode
  description: string
  requiredKeys: string[]
  testEndpoints: string[]
  documentation: string
  securityLevel: 'basic' | 'enhanced' | 'enterprise'
  compliance: string[]
}

export interface SecurityConfiguration {
  environment: 'development' | 'staging' | 'production'
  securityLevel: 'basic' | 'enhanced' | 'enterprise'
  keyRotationPolicy: 'never' | '30-days' | '60-days' | '90-days' | 'custom'
  customRotationDays?: number
  accessControl: {
    requireTwoFactor: boolean
    ipWhitelist: string[]
    geoRestrictions: string[]
    permissionLevel: 'read-only' | 'read-write' | 'admin'
  }
}

export interface APIKeyConfiguration {
  keyId: string
  service: APIService
  environment: string
  keys: Record<string, string>
  status: 'generating' | 'validating' | 'active' | 'error'
  securityScore: number
  testResults: TestResult[]
  monitoring: MonitoringConfig
}

interface TestResult {
  endpoint: string
  status: 'pending' | 'success' | 'error'
  responseTime?: number
  errorMessage?: string
}

interface MonitoringConfig {
  usageThresholds: {
    requests: number
    cost: number
  }
  alertChannels: {
    email: boolean
    slack: boolean
    webhook?: string
  }
  securityMonitoring: {
    enabled: boolean
    suspiciousActivityThreshold: number
  }
}

// Wizard schema
const wizardSchema = z.object({
  selectedServices: z.array(z.string()).min(1, 'Select at least one service'),
  securityConfiguration: z.object({
    environment: z.enum(['development', 'staging', 'production']),
    securityLevel: z.enum(['basic', 'enhanced', 'enterprise']),
    keyRotationPolicy: z.enum(['never', '30-days', '60-days', '90-days', 'custom']),
    customRotationDays: z.number().optional(),
    accessControl: z.object({
      requireTwoFactor: z.boolean(),
      ipWhitelist: z.array(z.string()),
      geoRestrictions: z.array(z.string()),
      permissionLevel: z.enum(['read-only', 'read-write', 'admin'])
    })
  }),
  generatedKeys: z.array(z.object({
    serviceId: z.string(),
    keys: z.record(z.string())
  })),
  testResults: z.array(z.object({
    serviceId: z.string(),
    passed: z.boolean(),
    issues: z.array(z.string())
  })),
  monitoringConfig: z.object({
    enabled: z.boolean(),
    alertChannels: z.array(z.string()),
    thresholds: z.record(z.number())
  }),
  deploymentConfig: z.object({
    autoGenerate: z.boolean(),
    teamAccess: z.array(z.string()),
    backupStrategy: z.string()
  })
})

type WizardFormData = z.infer<typeof wizardSchema>

// Step configuration
const WIZARD_STEPS = [
  {
    id: 'service-selection',
    title: 'Service Selection',
    description: 'Choose services and integration scope',
    icon: Globe,
    component: ServiceSelectionStep
  },
  {
    id: 'security-configuration',
    title: 'Security Setup',
    description: 'Configure security policies and access control',
    icon: ShieldCheck,
    component: SecurityConfigurationStep
  },
  {
    id: 'key-generation',
    title: 'Key Generation',
    description: 'Generate and validate API keys',
    icon: Key,
    component: KeyGenerationStep
  },
  {
    id: 'testing-verification',
    title: 'Testing & Verification',
    description: 'Test API connectivity and validation',
    icon: Zap,
    component: TestingVerificationStep
  },
  {
    id: 'monitoring-setup',
    title: 'Monitoring Setup',
    description: 'Configure alerting and monitoring',
    icon: Monitor,
    component: MonitoringSetupStep
  },
  {
    id: 'documentation-deployment',
    title: 'Documentation & Deployment',
    description: 'Generate docs and deploy configuration',
    icon: Database,
    component: DocumentationDeploymentStep
  }
]

interface APIKeyManagementWizardProps {
  onComplete?: (configuration: APIKeyConfiguration[]) => void
  onCancel?: () => void
  initialData?: Partial<WizardFormData>
}

export function APIKeyManagementWizard({ 
  onComplete, 
  onCancel,
  initialData 
}: APIKeyManagementWizardProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())
  const [configurations, setConfigurations] = useState<APIKeyConfiguration[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [availableServices, setAvailableServices] = useState<any[]>([])
  const [securityConfigurations, setSecurityConfigurations] = useState<any>(null)
  const [generatedKeys, setGeneratedKeys] = useState<any[]>([])
  const [wizardState, setWizardState] = useState<'configuring' | 'generating' | 'testing' | 'completed'>('configuring')
  const [error, setError] = useState<string | null>(null)

  const form = useForm<WizardFormData>({
    resolver: zodResolver(wizardSchema),
    defaultValues: {
      selectedServices: initialData?.selectedServices || [],
      securityConfiguration: {
        environment: 'development',
        securityLevel: 'enhanced',
        keyRotationPolicy: '90-days',
        accessControl: {
          requireTwoFactor: true,
          ipWhitelist: [],
          geoRestrictions: [],
          permissionLevel: 'read-write'
        }
      },
      generatedKeys: [],
      testResults: [],
      monitoringConfig: {
        enabled: true,
        alertChannels: ['email'],
        thresholds: {}
      },
      deploymentConfig: {
        autoGenerate: true,
        teamAccess: [],
        backupStrategy: 'vault'
      }
    }
  })

  const currentStepConfig = WIZARD_STEPS[currentStep]
  const StepComponent = currentStepConfig.component
  const progress = ((currentStep + 1) / WIZARD_STEPS.length) * 100

  const handleNext = async () => {
    const isValid = await form.trigger()
    if (isValid) {
      setCompletedSteps(prev => new Set(Array.from(prev).concat(currentStep)))
      if (currentStep < WIZARD_STEPS.length - 1) {
        setCurrentStep(currentStep + 1)
      } else {
        handleComplete()
      }
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleComplete = async () => {
    setIsProcessing(true)
    try {
      const formData = form.getValues()
      
      // Process final configuration
      const finalConfigurations = await processWizardConfiguration(formData)
      setConfigurations(finalConfigurations)
      
      onComplete?.(finalConfigurations)
    } catch (error) {
      console.error('Failed to complete wizard:', error)
    } finally {
      setIsProcessing(false)
    }
  }

  const processWizardConfiguration = async (data: WizardFormData): Promise<APIKeyConfiguration[]> => {
    // Simulate processing - replace with actual API calls
    return data.selectedServices.map(serviceId => ({
      keyId: `key_${serviceId}_${Date.now()}`,
      service: getServiceById(serviceId),
      environment: data.securityConfiguration.environment,
      keys: {},
      status: 'active' as const,
      securityScore: calculateSecurityScore(data.securityConfiguration as SecurityConfiguration),
      testResults: [],
      monitoring: {
        usageThresholds: {
          requests: data.monitoringConfig.thresholds.requests || 10000,
          cost: data.monitoringConfig.thresholds.cost || 1000
        },
        alertChannels: {
          email: data.monitoringConfig.alertChannels.includes('email'),
          slack: data.monitoringConfig.alertChannels.includes('slack')
        },
        securityMonitoring: {
          enabled: true,
          suspiciousActivityThreshold: 5
        }
      }
    }))
  }

  const getServiceById = (id: string): APIService => {
    // Placeholder - replace with actual service lookup
    return {
      id,
      name: id,
      category: 'payment',
      icon: <Key className="h-4 w-4" />,
      description: 'Service description',
      requiredKeys: [],
      testEndpoints: [],
      documentation: '',
      securityLevel: 'enhanced',
      compliance: []
    }
  }

  const calculateSecurityScore = (config: SecurityConfiguration): number => {
    let score = 50 // Base score
    
    if (config.securityLevel === 'enterprise') score += 30
    else if (config.securityLevel === 'enhanced') score += 20
    
    if (config.accessControl.requireTwoFactor) score += 15
    if (config.keyRotationPolicy !== 'never') score += 10
    if (config.accessControl.ipWhitelist.length > 0) score += 10
    if (config.environment === 'production') score += 5
    
    return Math.min(score, 100)
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          API Key Management Wizard
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Secure configuration wizard for enterprise-grade API key management
        </p>
      </div>

      {/* Progress */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">
                Step {currentStep + 1} of {WIZARD_STEPS.length}
              </span>
              <span className="text-sm text-gray-500">
                {Math.round(progress)}% Complete
              </span>
            </div>
            <Progress value={progress} className="h-2" />
            
            {/* Step indicators */}
            <div className="flex justify-between items-center">
              {WIZARD_STEPS.map((step, index) => {
                const Icon = step.icon
                const isCompleted = completedSteps.has(index)
                const isCurrent = index === currentStep
                
                return (
                  <div
                    key={step.id}
                    className={cn(
                      "flex flex-col items-center space-y-2 text-center",
                      "w-full max-w-[120px]"
                    )}
                  >
                    <div
                      className={cn(
                        "w-10 h-10 rounded-full flex items-center justify-center",
                        "transition-all duration-200",
                        isCompleted 
                          ? "bg-green-500 text-white" 
                          : isCurrent 
                          ? "bg-blue-500 text-white" 
                          : "bg-gray-200 text-gray-500"
                      )}
                    >
                      {isCompleted ? (
                        <CheckCircle className="h-5 w-5" />
                      ) : (
                        <Icon className="h-5 w-5" />
                      )}
                    </div>
                    <div className="space-y-1">
                      <p className={cn(
                        "text-xs font-medium",
                        isCurrent ? "text-blue-600" : "text-gray-600"
                      )}>
                        {step.title}
                      </p>
                      {isCompleted && (
                        <Badge variant="secondary" className="text-xs">
                          <CheckCircle className="h-3 w-3 mr-1" />
                          Complete
                        </Badge>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Current Step */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <currentStepConfig.icon className="h-5 w-5" />
            <span>{currentStepConfig.title}</span>
          </CardTitle>
          <CardDescription>
            {currentStepConfig.description}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <StepComponent
            form={form}
            configurations={configurations}
            setConfigurations={setConfigurations}
          />
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <div>
          {currentStep > 0 && (
            <Button 
              variant="outline" 
              onClick={handlePrevious}
              disabled={isProcessing}
            >
              Previous
            </Button>
          )}
        </div>
        
        <div className="flex space-x-2">
          <Button 
            variant="outline" 
            onClick={onCancel}
            disabled={isProcessing}
          >
            Cancel
          </Button>
          <Button 
            onClick={handleNext}
            disabled={isProcessing}
            className="min-w-[120px]"
          >
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Processing...
              </>
            ) : currentStep === WIZARD_STEPS.length - 1 ? (
              'Complete Setup'
            ) : (
              'Next'
            )}
          </Button>
        </div>
      </div>

      {/* Security Status */}
      <Card className="border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="h-5 w-5 text-blue-600" />
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              Enterprise Security Active
            </span>
            <Badge variant="secondary" className="bg-blue-100 text-blue-800">
              Vault Encrypted
            </Badge>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              SOC2 Compliant
            </Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default APIKeyManagementWizard