"use client"

import React, { useState } from 'react'
import { APIKeyManagementWizard, type APIKeyConfiguration } from './api-key-management-wizard'
import { Button } from '../ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { 
  Rocket, 
  Settings, 
  CheckCircle, 
  AlertTriangle,
  Key,
  Users,
  Monitor,
  FileText
} from 'lucide-react'

/**
 * Demo component showcasing the API Key Management Wizard
 * This demonstrates how to integrate the wizard into your application
 */
export function APIKeyWizardDemo() {
  const [showWizard, setShowWizard] = useState(false)
  const [completedConfigurations, setCompletedConfigurations] = useState<APIKeyConfiguration[]>([])
  const [isCompleted, setIsCompleted] = useState(false)

  const handleWizardComplete = (configurations: APIKeyConfiguration[]) => {
    setCompletedConfigurations(configurations)
    setIsCompleted(true)
    setShowWizard(false)
    
    // Here you would typically:
    // 1. Send configurations to your backend API
    // 2. Initialize vault storage
    // 3. Set up monitoring
    // 4. Send team invitations
    console.log('Wizard completed with configurations:', configurations)
  }

  const handleWizardCancel = () => {
    setShowWizard(false)
  }

  const resetDemo = () => {
    setShowWizard(false)
    setCompletedConfigurations([])
    setIsCompleted(false)
  }

  if (showWizard) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <APIKeyManagementWizard
          onComplete={handleWizardComplete}
          onCancel={handleWizardCancel}
          initialData={{
            selectedServices: [], // Can pre-populate if needed
            securityConfiguration: {
              environment: 'development',
              securityLevel: 'enhanced',
              keyRotationPolicy: '90-days',
              accessControl: {
                requireTwoFactor: false,
                ipWhitelist: [],
                geoRestrictions: [],
                permissionLevel: 'read-write'
              }
            }
          }}
        />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            API Key Management Wizard Demo
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Enterprise-grade security-focused configuration wizard for BizOSaaS platform
          </p>
        </div>

        {/* Demo Controls */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>Demo Controls</span>
            </CardTitle>
            <CardDescription>
              Launch the API Key Management Wizard or view completed configurations
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex space-x-2">
              <Button 
                onClick={() => setShowWizard(true)}
                className="flex items-center space-x-2"
                disabled={showWizard}
              >
                <Rocket className="h-4 w-4" />
                <span>Launch Wizard</span>
              </Button>
              
              {isCompleted && (
                <Button 
                  variant="outline"
                  onClick={resetDemo}
                >
                  Reset Demo
                </Button>
              )}
            </div>
            
            {isCompleted && (
              <div className="p-4 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <span className="font-medium text-green-800 dark:text-green-200">
                    Wizard completed successfully! {completedConfigurations.length} API key{completedConfigurations.length !== 1 ? 's' : ''} configured.
                  </span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Features Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-6 text-center">
              <Key className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <h3 className="font-semibold mb-1">40+ Services</h3>
              <p className="text-sm text-gray-600">
                Payment, Marketing, AI, Analytics & Infrastructure APIs
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6 text-center">
              <Users className="h-8 w-8 text-green-500 mx-auto mb-2" />
              <h3 className="font-semibold mb-1">Team Management</h3>
              <p className="text-sm text-gray-600">
                Role-based access control and permissions
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6 text-center">
              <Monitor className="h-8 w-8 text-purple-500 mx-auto mb-2" />
              <h3 className="font-semibold mb-1">24/7 Monitoring</h3>
              <p className="text-sm text-gray-600">
                Real-time alerts and performance tracking
              </p>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6 text-center">
              <FileText className="h-8 w-8 text-orange-500 mx-auto mb-2" />
              <h3 className="font-semibold mb-1">Auto Documentation</h3>
              <p className="text-sm text-gray-600">
                Generated guides, examples and references
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Wizard Steps Preview */}
        <Card>
          <CardHeader>
            <CardTitle>6-Step Security-Focused Process</CardTitle>
            <CardDescription>
              The wizard guides users through comprehensive API key management setup
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-semibold">
                    1
                  </div>
                  <h4 className="font-medium">Service Selection</h4>
                </div>
                <p className="text-sm text-gray-600">
                  Choose from 40+ integrated services with smart recommendations
                </p>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-semibold">
                    2
                  </div>
                  <h4 className="font-medium">Security Configuration</h4>
                </div>
                <p className="text-sm text-gray-600">
                  Environment setup, security levels, and access control policies
                </p>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-semibold">
                    3
                  </div>
                  <h4 className="font-medium">Key Generation</h4>
                </div>
                <p className="text-sm text-gray-600">
                  Secure key generation with entropy validation and Vault storage
                </p>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-semibold">
                    4
                  </div>
                  <h4 className="font-medium">Testing & Verification</h4>
                </div>
                <p className="text-sm text-gray-600">
                  Automated API testing and security validation
                </p>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-semibold">
                    5
                  </div>
                  <h4 className="font-medium">Monitoring Setup</h4>
                </div>
                <p className="text-sm text-gray-600">
                  Configure alerts, thresholds, and monitoring dashboards
                </p>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-semibold">
                    6
                  </div>
                  <h4 className="font-medium">Documentation & Deployment</h4>
                </div>
                <p className="text-sm text-gray-600">
                  Auto-generated docs, team setup, and production deployment
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Completed Configurations */}
        {isCompleted && completedConfigurations.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <CheckCircle className="h-5 w-5 text-green-500" />
                <span>Completed Configurations</span>
              </CardTitle>
              <CardDescription>
                API keys have been generated and configured
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {completedConfigurations.map(config => (
                  <div key={config.keyId} className="flex items-center justify-between p-3 border rounded-lg bg-green-50 dark:bg-green-950">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-green-100 text-green-600 rounded-lg">
                        <Key className="h-4 w-4" />
                      </div>
                      <div>
                        <h4 className="font-medium">{config.service.name}</h4>
                        <p className="text-sm text-gray-600">
                          Environment: {config.environment} | Security Score: {config.securityScore}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Badge 
                        variant="secondary"
                        className={
                          config.status === 'active' ? 'bg-green-100 text-green-800' : 
                          'bg-gray-100 text-gray-800'
                        }
                      >
                        {config.status}
                      </Badge>
                      
                      <Badge variant="outline">
                        Score: {config.securityScore}
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Integration Guide */}
        <Card>
          <CardHeader>
            <CardTitle>Integration Guide</CardTitle>
            <CardDescription>
              How to integrate this wizard into your application
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <h4 className="font-medium mb-2">Basic Usage</h4>
                <pre className="text-sm overflow-x-auto">
{`import { APIKeyManagementWizard } from './components/wizards'

function MyApp() {
  const handleComplete = (configurations) => {
    // Process completed configurations
    console.log('Configurations:', configurations)
  }

  return (
    <APIKeyManagementWizard
      onComplete={handleComplete}
      onCancel={() => console.log('Cancelled')}
    />
  )
}`}
                </pre>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-2">Key Features</h4>
                  <ul className="text-sm space-y-1 text-gray-600">
                    <li>• TypeScript support with full type definitions</li>
                    <li>• Built with Next.js 15 and React 19</li>
                    <li>• ShadCN UI components for consistency</li>
                    <li>• Zod validation for form handling</li>
                    <li>• Zustand for state management</li>
                    <li>• React Query for API integration</li>
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Security Features</h4>
                  <ul className="text-sm space-y-1 text-gray-600">
                    <li>• HashiCorp Vault integration</li>
                    <li>• AES-256 encryption</li>
                    <li>• Role-based access control</li>
                    <li>• Automated key rotation</li>
                    <li>• Compliance reporting (SOC2, GDPR)</li>
                    <li>• Audit logging</li>
                  </ul>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default APIKeyWizardDemo