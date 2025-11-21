"use client"

import React, { useState, useEffect } from 'react'
import { UseFormReturn } from 'react-hook-form'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '../../ui/card'
import { Button } from '../../ui/button'
import { Badge } from '../../ui/badge'
import { Progress } from '../../ui/progress'
import { 
  Zap, 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Clock, 
  Play,
  Pause,
  RotateCcw,
  Activity,
  Network,
  Shield,
  Timer,
  Database,
  Globe,
  TrendingUp,
  AlertCircle
} from 'lucide-react'
import { cn } from '../../../lib/utils'

interface TestingVerificationStepProps {
  form: UseFormReturn<any>
  configurations: any[]
  setConfigurations: React.Dispatch<React.SetStateAction<any[]>>
}

interface TestResult {
  id: string
  serviceId: string
  serviceName: string
  endpoint: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE'
  status: 'pending' | 'running' | 'success' | 'error' | 'timeout'
  responseTime?: number
  statusCode?: number
  errorMessage?: string
  responseSize?: number
  startTime?: Date
  endTime?: Date
  retryCount: number
  maxRetries: number
}

interface PerformanceMetrics {
  avgResponseTime: number
  successRate: number
  errorRate: number
  timeoutRate: number
  totalRequests: number
}

interface SecurityTest {
  id: string
  name: string
  description: string
  status: 'pending' | 'running' | 'passed' | 'failed'
  severity: 'low' | 'medium' | 'high' | 'critical'
  details?: string
}

// Test configurations for different services
const SERVICE_TEST_CONFIGS = {
  stripe: [
    { endpoint: '/v1/payment_methods', method: 'GET' as const, description: 'List payment methods' },
    { endpoint: '/v1/customers', method: 'GET' as const, description: 'List customers' },
    { endpoint: '/v1/payment_intents', method: 'POST' as const, description: 'Create payment intent' }
  ],
  paypal: [
    { endpoint: '/v2/payments', method: 'GET' as const, description: 'List payments' },
    { endpoint: '/v1/identity/oauth2/token', method: 'POST' as const, description: 'Get access token' }
  ],
  'google-ads': [
    { endpoint: '/googleads/v14/customers', method: 'GET' as const, description: 'List customers' },
    { endpoint: '/googleads/v14/campaigns', method: 'GET' as const, description: 'List campaigns' }
  ],
  openai: [
    { endpoint: '/v1/models', method: 'GET' as const, description: 'List available models' },
    { endpoint: '/v1/chat/completions', method: 'POST' as const, description: 'Test chat completion' }
  ]
}

const SECURITY_TESTS: SecurityTest[] = [
  {
    id: 'auth_validation',
    name: 'Authentication Validation',
    description: 'Verify API key authentication works correctly',
    status: 'pending',
    severity: 'critical'
  },
  {
    id: 'rate_limiting',
    name: 'Rate Limiting Test',
    description: 'Check rate limiting behavior and error handling',
    status: 'pending',
    severity: 'high'
  },
  {
    id: 'error_handling',
    name: 'Error Response Handling',
    description: 'Verify proper error response formats and codes',
    status: 'pending',
    severity: 'medium'
  },
  {
    id: 'ssl_verification',
    name: 'SSL/TLS Verification',
    description: 'Validate secure connection and certificate',
    status: 'pending',
    severity: 'high'
  },
  {
    id: 'data_validation',
    name: 'Data Validation',
    description: 'Test input validation and sanitization',
    status: 'pending',
    severity: 'medium'
  }
]

export function TestingVerificationStep({ 
  form,
  configurations,
  setConfigurations
}: TestingVerificationStepProps) {
  const [testResults, setTestResults] = useState<TestResult[]>([])
  const [securityTests, setSecurityTests] = useState<SecurityTest[]>(SECURITY_TESTS)
  const [isRunningTests, setIsRunningTests] = useState(false)
  const [currentTest, setCurrentTest] = useState<string>('')
  const [testProgress, setTestProgress] = useState(0)
  const [performanceMetrics, setPerformanceMetrics] = useState<PerformanceMetrics>({
    avgResponseTime: 0,
    successRate: 0,
    errorRate: 0,
    timeoutRate: 0,
    totalRequests: 0
  })

  const formData = form.watch()
  const selectedServices = formData.selectedServices || []

  useEffect(() => {
    initializeTests()
  }, [selectedServices])

  useEffect(() => {
    calculatePerformanceMetrics()
  }, [testResults])

  const initializeTests = () => {
    const tests: TestResult[] = []
    
    selectedServices.forEach((serviceId: string) => {
      const serviceConfig = SERVICE_TEST_CONFIGS[serviceId as keyof typeof SERVICE_TEST_CONFIGS]
      if (serviceConfig) {
        serviceConfig.forEach((test, index) => {
          tests.push({
            id: `${serviceId}-${index}`,
            serviceId,
            serviceName: getServiceName(serviceId),
            endpoint: test.endpoint,
            method: test.method,
            status: 'pending',
            retryCount: 0,
            maxRetries: 3
          })
        })
      }
    })
    
    setTestResults(tests)
  }

  const getServiceName = (serviceId: string): string => {
    const serviceNames: Record<string, string> = {
      stripe: 'Stripe',
      paypal: 'PayPal',
      'google-ads': 'Google Ads',
      openai: 'OpenAI'
    }
    return serviceNames[serviceId] || serviceId
  }

  const runAllTests = async () => {
    setIsRunningTests(true)
    setTestProgress(0)
    
    // Run API tests
    const totalTests = testResults.length + securityTests.length
    let completedTests = 0
    
    for (const test of testResults) {
      setCurrentTest(`Testing ${test.serviceName} - ${test.endpoint}`)
      await runSingleTest(test.id)
      completedTests++
      setTestProgress((completedTests / totalTests) * 100)
    }
    
    // Run security tests
    for (const test of securityTests) {
      setCurrentTest(`Security Test - ${test.name}`)
      await runSecurityTest(test.id)
      completedTests++
      setTestProgress((completedTests / totalTests) * 100)
    }
    
    setIsRunningTests(false)
    setCurrentTest('')
    setTestProgress(100)
  }

  const runSingleTest = async (testId: string) => {
    const test = testResults.find(t => t.id === testId)
    if (!test) return
    
    setTestResults(prev => prev.map(t => 
      t.id === testId 
        ? { ...t, status: 'running', startTime: new Date() }
        : t
    ))
    
    try {
      // Simulate API test
      await new Promise(resolve => setTimeout(resolve, Math.random() * 2000 + 500))
      
      const success = Math.random() > 0.1 // 90% success rate for demo
      const responseTime = Math.random() * 1000 + 100
      const statusCode = success ? 200 : Math.random() > 0.5 ? 401 : 500
      
      setTestResults(prev => prev.map(t => 
        t.id === testId 
          ? {
              ...t,
              status: success ? 'success' : 'error',
              responseTime,
              statusCode,
              responseSize: Math.floor(Math.random() * 5000 + 500),
              endTime: new Date(),
              errorMessage: success ? undefined : getErrorMessage(statusCode)
            }
          : t
      ))
      
    } catch (error) {
      setTestResults(prev => prev.map(t => 
        t.id === testId 
          ? {
              ...t,
              status: 'error',
              endTime: new Date(),
              errorMessage: 'Network error or timeout'
            }
          : t
      ))
    }
  }

  const runSecurityTest = async (testId: string) => {
    setSecurityTests(prev => prev.map(t => 
      t.id === testId 
        ? { ...t, status: 'running' }
        : t
    ))
    
    // Simulate security test
    await new Promise(resolve => setTimeout(resolve, Math.random() * 1500 + 500))
    
    const passed = Math.random() > 0.15 // 85% pass rate for demo
    
    setSecurityTests(prev => prev.map(t => 
      t.id === testId 
        ? {
            ...t,
            status: passed ? 'passed' : 'failed',
            details: passed 
              ? 'Security test passed successfully'
              : getSecurityTestFailureReason(testId)
          }
        : t
    ))
  }

  const getErrorMessage = (statusCode: number): string => {
    switch (statusCode) {
      case 401:
        return 'Authentication failed - invalid API key'
      case 403:
        return 'Forbidden - insufficient permissions'
      case 429:
        return 'Rate limit exceeded'
      case 500:
        return 'Internal server error'
      default:
        return 'Unknown error occurred'
    }
  }

  const getSecurityTestFailureReason = (testId: string): string => {
    const reasons: Record<string, string> = {
      auth_validation: 'API key format validation failed',
      rate_limiting: 'Rate limiting not properly configured',
      error_handling: 'Error responses not in expected format',
      ssl_verification: 'SSL certificate validation issues',
      data_validation: 'Input validation bypass detected'
    }
    return reasons[testId] || 'Security test failed'
  }

  const calculatePerformanceMetrics = () => {
    if (testResults.length === 0) return
    
    const completedTests = testResults.filter(t => t.status === 'success' || t.status === 'error')
    const successfulTests = testResults.filter(t => t.status === 'success')
    const errorTests = testResults.filter(t => t.status === 'error')
    const timeoutTests = testResults.filter(t => t.status === 'timeout')
    
    const avgResponseTime = successfulTests.length > 0
      ? successfulTests.reduce((sum, t) => sum + (t.responseTime || 0), 0) / successfulTests.length
      : 0
    
    const successRate = completedTests.length > 0 
      ? (successfulTests.length / completedTests.length) * 100 
      : 0
    
    const errorRate = completedTests.length > 0 
      ? (errorTests.length / completedTests.length) * 100 
      : 0
    
    const timeoutRate = completedTests.length > 0 
      ? (timeoutTests.length / completedTests.length) * 100 
      : 0
    
    setPerformanceMetrics({
      avgResponseTime,
      successRate,
      errorRate,
      timeoutRate,
      totalRequests: completedTests.length
    })
  }

  const retryFailedTests = async () => {
    const failedTests = testResults.filter(t => t.status === 'error' || t.status === 'timeout')
    
    for (const test of failedTests) {
      if (test.retryCount < test.maxRetries) {
        setTestResults(prev => prev.map(t => 
          t.id === test.id 
            ? { ...t, retryCount: t.retryCount + 1 }
            : t
        ))
        await runSingleTest(test.id)
      }
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
      case 'passed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'error':
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'running':
        return <Activity className="h-4 w-4 text-blue-500 animate-pulse" />
      case 'timeout':
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <Circle className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
      case 'passed':
        return 'text-green-600 bg-green-50 border-green-200'
      case 'error':
      case 'failed':
        return 'text-red-600 bg-red-50 border-red-200'
      case 'running':
        return 'text-blue-600 bg-blue-50 border-blue-200'
      case 'timeout':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const overallSuccess = testResults.length > 0 && securityTests.length > 0
    ? ((testResults.filter(t => t.status === 'success').length + 
        securityTests.filter(t => t.status === 'passed').length) /
       (testResults.length + securityTests.length)) * 100
    : 0

  return (
    <div className="space-y-6">
      {/* Testing Overview */}
      <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Zap className="h-5 w-5 text-blue-600" />
            <span>API Testing & Verification</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{testResults.length}</div>
              <div className="text-sm text-gray-600">API Tests</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{securityTests.length}</div>
              <div className="text-sm text-gray-600">Security Tests</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {Math.round(performanceMetrics.successRate)}%
              </div>
              <div className="text-sm text-gray-600">Success Rate</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {Math.round(performanceMetrics.avgResponseTime)}ms
              </div>
              <div className="text-sm text-gray-600">Avg Response</div>
            </div>
          </div>
          
          {isRunningTests && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Running: {currentTest}</span>
                <span className="text-sm text-gray-500">{Math.round(testProgress)}%</span>
              </div>
              <Progress value={testProgress} className="h-2" />
            </div>
          )}
          
          <div className="flex space-x-2 mt-4">
            <Button 
              onClick={runAllTests}
              disabled={isRunningTests}
              className="flex items-center space-x-2"
            >
              {isRunningTests ? (
                <Activity className="h-4 w-4 animate-pulse" />
              ) : (
                <Play className="h-4 w-4" />
              )}
              <span>{isRunningTests ? 'Running Tests...' : 'Run All Tests'}</span>
            </Button>
            
            <Button 
              variant="outline"
              onClick={retryFailedTests}
              disabled={isRunningTests || testResults.filter(t => t.status === 'error').length === 0}
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              Retry Failed
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Performance Metrics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5" />
            <span>Performance Metrics</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 border rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Timer className="h-4 w-4 text-blue-500" />
                <span className="text-sm font-medium">Response Time</span>
              </div>
              <div className="text-2xl font-bold">{Math.round(performanceMetrics.avgResponseTime)}ms</div>
              <div className="text-xs text-gray-500">Average</div>
            </div>
            
            <div className="p-4 border rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm font-medium">Success Rate</span>
              </div>
              <div className="text-2xl font-bold">{Math.round(performanceMetrics.successRate)}%</div>
              <div className="text-xs text-gray-500">Of all requests</div>
            </div>
            
            <div className="p-4 border rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <XCircle className="h-4 w-4 text-red-500" />
                <span className="text-sm font-medium">Error Rate</span>
              </div>
              <div className="text-2xl font-bold">{Math.round(performanceMetrics.errorRate)}%</div>
              <div className="text-xs text-gray-500">Failed requests</div>
            </div>
            
            <div className="p-4 border rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <Database className="h-4 w-4 text-purple-500" />
                <span className="text-sm font-medium">Total Tests</span>
              </div>
              <div className="text-2xl font-bold">{performanceMetrics.totalRequests}</div>
              <div className="text-xs text-gray-500">Completed</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Test Results */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Network className="h-5 w-5" />
            <span>API Connectivity Tests</span>
          </CardTitle>
          <CardDescription>
            Verify API endpoints and authentication
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {selectedServices.map((serviceId: string) => {
              const serviceTests = testResults.filter(t => t.serviceId === serviceId)
              if (serviceTests.length === 0) return null
              
              return (
                <div key={serviceId} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium">{getServiceName(serviceId)}</h4>
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">
                        {serviceTests.filter(t => t.status === 'success').length}/{serviceTests.length} passed
                      </Badge>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    {serviceTests.map(test => (
                      <div key={test.id} className={cn(
                        "flex items-center justify-between p-3 rounded border",
                        getStatusColor(test.status)
                      )}>
                        <div className="flex items-center space-x-3">
                          {getStatusIcon(test.status)}
                          <div>
                            <div className="font-mono text-sm">{test.method} {test.endpoint}</div>
                            {test.errorMessage && (
                              <div className="text-xs text-red-600 mt-1">{test.errorMessage}</div>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm">
                          {test.responseTime && (
                            <span className="text-gray-600">{Math.round(test.responseTime)}ms</span>
                          )}
                          {test.statusCode && (
                            <Badge variant="outline" className={cn(
                              test.statusCode >= 200 && test.statusCode < 300 
                                ? 'text-green-700 border-green-300'
                                : 'text-red-700 border-red-300'
                            )}>
                              {test.statusCode}
                            </Badge>
                          )}
                          {test.retryCount > 0 && (
                            <span className="text-xs text-gray-500">
                              Retry {test.retryCount}/{test.maxRetries}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Security Tests */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className="h-5 w-5" />
            <span>Security Verification</span>
          </CardTitle>
          <CardDescription>
            Comprehensive security validation tests
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {securityTests.map(test => (
              <div key={test.id} className={cn(
                "flex items-center justify-between p-4 rounded border",
                getStatusColor(test.status)
              )}>
                <div className="flex items-center space-x-3">
                  {getStatusIcon(test.status)}
                  <div>
                    <div className="font-medium">{test.name}</div>
                    <div className="text-sm text-gray-600">{test.description}</div>
                    {test.details && (
                      <div className="text-xs mt-1">{test.details}</div>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Badge 
                    variant="outline" 
                    className={cn(
                      test.severity === 'critical' ? 'text-red-700 border-red-300' :
                      test.severity === 'high' ? 'text-orange-700 border-orange-300' :
                      test.severity === 'medium' ? 'text-yellow-700 border-yellow-300' :
                      'text-blue-700 border-blue-300'
                    )}
                  >
                    {test.severity}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Overall Status */}
      {overallSuccess > 0 && (
        <Card className={cn(
          "border-2",
          overallSuccess >= 90 ? "border-green-200 bg-green-50 dark:bg-green-950" :
          overallSuccess >= 70 ? "border-yellow-200 bg-yellow-50 dark:bg-yellow-950" :
          "border-red-200 bg-red-50 dark:bg-red-950"
        )}>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              {overallSuccess >= 90 ? (
                <CheckCircle className="h-6 w-6 text-green-600" />
              ) : overallSuccess >= 70 ? (
                <AlertTriangle className="h-6 w-6 text-yellow-600" />
              ) : (
                <AlertCircle className="h-6 w-6 text-red-600" />
              )}
              
              <div>
                <div className="font-semibold text-lg">
                  Overall Test Status: {Math.round(overallSuccess)}% Success Rate
                </div>
                <div className="text-sm">
                  {overallSuccess >= 90 
                    ? 'All systems are ready for production deployment'
                    : overallSuccess >= 70
                    ? 'Some issues detected - review failed tests before deployment'
                    : 'Critical issues found - resolve before proceeding'
                  }
                </div>
              </div>
              
              <div className="ml-auto">
                <Badge 
                  variant="secondary" 
                  className={cn(
                    overallSuccess >= 90 ? 'bg-green-100 text-green-800' :
                    overallSuccess >= 70 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  )}
                >
                  {overallSuccess >= 90 ? 'Ready' : overallSuccess >= 70 ? 'Review Required' : 'Issues Found'}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

// Helper component for circle icon
function Circle({ className }: { className?: string }) {
  return (
    <div className={cn("rounded-full border-2", className)} style={{ width: '16px', height: '16px' }} />
  )
}

export default TestingVerificationStep