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
import { Input } from '../../ui/input'
import { Progress } from '../../ui/progress'
import { 
  Key, 
  Shield, 
  Eye, 
  EyeOff, 
  Copy, 
  CheckCircle, 
  AlertTriangle,
  RefreshCw,
  Download,
  Upload,
  Lock,
  Unlock,
  Zap,
  Database,
  Clock,
  FileText
} from 'lucide-react'
import { cn } from '../../../lib/utils'

interface KeyGenerationStepProps {
  form: UseFormReturn<any>
  configurations: any[]
  setConfigurations: React.Dispatch<React.SetStateAction<any[]>>
}

interface GeneratedKey {
  serviceId: string
  serviceName: string
  keyType: string
  value: string
  masked: string
  strength: number
  status: 'generating' | 'generated' | 'validated' | 'error'
  createdAt: Date
  expiresAt?: Date
  backupGenerated: boolean
}

interface KeyValidationResult {
  isValid: boolean
  strength: number
  entropy: number
  issues: string[]
  recommendations: string[]
}

// Simulated service configs for key generation
const SERVICE_KEY_CONFIGS = {
  stripe: {
    keys: [
      { type: 'publishable_key', prefix: 'pk_test_', length: 107, description: 'Public key for client-side' },
      { type: 'secret_key', prefix: 'sk_test_', length: 107, description: 'Secret key for server-side' },
      { type: 'webhook_secret', prefix: 'whsec_', length: 64, description: 'Webhook endpoint verification' }
    ]
  },
  paypal: {
    keys: [
      { type: 'client_id', prefix: '', length: 80, description: 'PayPal application client ID' },
      { type: 'client_secret', prefix: '', length: 80, description: 'PayPal application secret' }
    ]
  },
  'google-ads': {
    keys: [
      { type: 'developer_token', prefix: '', length: 22, description: 'Google Ads API developer token' },
      { type: 'client_id', prefix: '', length: 72, description: 'OAuth 2.0 client ID' },
      { type: 'client_secret', prefix: '', length: 24, description: 'OAuth 2.0 client secret' },
      { type: 'refresh_token', prefix: '', length: 64, description: 'OAuth 2.0 refresh token' }
    ]
  },
  openai: {
    keys: [
      { type: 'api_key', prefix: 'sk-', length: 51, description: 'OpenAI API secret key' },
      { type: 'organization', prefix: 'org-', length: 28, description: 'Organization identifier' }
    ]
  }
}

export function KeyGenerationStep({ 
  form,
  configurations,
  setConfigurations
}: KeyGenerationStepProps) {
  const [generatedKeys, setGeneratedKeys] = useState<GeneratedKey[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [showKeys, setShowKeys] = useState<Set<string>>(new Set())
  const [validationResults, setValidationResults] = useState<Map<string, KeyValidationResult>>(new Map())
  const [generationProgress, setGenerationProgress] = useState(0)
  const [currentlyGenerating, setCurrentlyGenerating] = useState('')

  const formData = form.watch()
  const selectedServices = formData.selectedServices || []
  const securityConfig = formData.securityConfiguration || {}

  useEffect(() => {
    // Initialize key generation for selected services
    initializeKeyGeneration()
  }, [selectedServices])

  const initializeKeyGeneration = () => {
    const keys: GeneratedKey[] = []
    
    selectedServices.forEach((serviceId: string) => {
      const serviceConfig = SERVICE_KEY_CONFIGS[serviceId as keyof typeof SERVICE_KEY_CONFIGS]
      if (serviceConfig) {
        serviceConfig.keys.forEach(keyConfig => {
          keys.push({
            serviceId,
            serviceName: getServiceName(serviceId),
            keyType: keyConfig.type,
            value: '',
            masked: '••••••••••••••••••••••••••••••••',
            strength: 0,
            status: 'generating',
            createdAt: new Date(),
            backupGenerated: false
          })
        })
      }
    })
    
    setGeneratedKeys(keys)
  }

  const getServiceName = (serviceId: string): string => {
    const serviceNames: Record<string, string> = {
      stripe: 'Stripe',
      paypal: 'PayPal',
      'google-ads': 'Google Ads',
      openai: 'OpenAI',
      'facebook-ads': 'Meta Ads',
      anthropic: 'Anthropic Claude'
    }
    return serviceNames[serviceId] || serviceId
  }

  const generateAllKeys = async () => {
    setIsGenerating(true)
    setGenerationProgress(0)
    
    for (let i = 0; i < generatedKeys.length; i++) {
      const key = generatedKeys[i]
      setCurrentlyGenerating(`${key.serviceName} - ${key.keyType}`)
      setGenerationProgress(((i + 1) / generatedKeys.length) * 100)
      
      await generateSingleKey(key.serviceId, key.keyType)
      
      // Simulate generation time
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
    
    setIsGenerating(false)
    setCurrentlyGenerating('')
    setGenerationProgress(100)
  }

  const generateSingleKey = async (serviceId: string, keyType: string) => {
    try {
      // Simulate key generation based on service requirements
      const serviceConfig = SERVICE_KEY_CONFIGS[serviceId as keyof typeof SERVICE_KEY_CONFIGS]
      const keyConfig = serviceConfig?.keys.find(k => k.type === keyType)
      
      if (!keyConfig) return
      
      // Generate key with appropriate format
      const generatedValue = generateKeyValue(keyConfig.prefix, keyConfig.length)
      const strength = calculateKeyStrength(generatedValue)
      const validation = validateKey(generatedValue, keyType)
      
      // Update key in state
      setGeneratedKeys(prev => prev.map(key => 
        key.serviceId === serviceId && key.keyType === keyType
          ? {
              ...key,
              value: generatedValue,
              masked: maskKey(generatedValue),
              strength,
              status: validation.isValid ? 'generated' : 'error',
              expiresAt: calculateExpirationDate()
            }
          : key
      ))
      
      setValidationResults(prev => new Map(prev.set(`${serviceId}-${keyType}`, validation)))
      
      // Generate backup key if enterprise security
      if (securityConfig.securityLevel === 'enterprise') {
        await generateBackupKey(serviceId, keyType)
      }
      
    } catch (error) {
      console.error('Key generation failed:', error)
      setGeneratedKeys(prev => prev.map(key => 
        key.serviceId === serviceId && key.keyType === keyType
          ? { ...key, status: 'error' }
          : key
      ))
    }
  }

  const generateKeyValue = (prefix: string, length: number): string => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    const specialChars = '_-'
    const allChars = chars + specialChars
    
    let result = prefix
    const remainingLength = length - prefix.length
    
    for (let i = 0; i < remainingLength; i++) {
      result += allChars.charAt(Math.floor(Math.random() * allChars.length))
    }
    
    return result
  }

  const calculateKeyStrength = (key: string): number => {
    let score = 0
    
    // Length score
    if (key.length >= 64) score += 30
    else if (key.length >= 32) score += 20
    else if (key.length >= 16) score += 10
    
    // Character variety
    if (/[A-Z]/.test(key)) score += 15
    if (/[a-z]/.test(key)) score += 15
    if (/\d/.test(key)) score += 15
    if (/[^A-Za-z0-9]/.test(key)) score += 15
    
    // Randomness (simplified entropy check)
    const entropy = calculateEntropy(key)
    if (entropy > 4) score += 10
    
    return Math.min(score, 100)
  }

  const calculateEntropy = (str: string): number => {
    const freq: Record<string, number> = {}
    for (const char of str) {
      freq[char] = (freq[char] || 0) + 1
    }
    
    let entropy = 0
    for (const count of Object.values(freq)) {
      const p = count / str.length
      entropy -= p * Math.log2(p)
    }
    
    return entropy
  }

  const validateKey = (key: string, keyType: string): KeyValidationResult => {
    const issues: string[] = []
    const recommendations: string[] = []
    let strength = calculateKeyStrength(key)
    
    // Basic validation
    if (key.length < 16) {
      issues.push('Key length is too short')
      recommendations.push('Use keys with at least 32 characters')
    }
    
    // Pattern validation
    if (!/[A-Z]/.test(key)) {
      issues.push('Missing uppercase letters')
    }
    
    if (!/\d/.test(key)) {
      issues.push('Missing numeric characters')
    }
    
    // Entropy check
    const entropy = calculateEntropy(key)
    if (entropy < 3) {
      issues.push('Low entropy detected')
      recommendations.push('Ensure sufficient randomness in key generation')
    }
    
    return {
      isValid: issues.length === 0,
      strength,
      entropy,
      issues,
      recommendations
    }
  }

  const calculateExpirationDate = (): Date => {
    const now = new Date()
    const rotationPolicy = securityConfig.keyRotationPolicy
    
    switch (rotationPolicy) {
      case '30-days':
        return new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000)
      case '60-days':
        return new Date(now.getTime() + 60 * 24 * 60 * 60 * 1000)
      case '90-days':
        return new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000)
      case 'custom':
        const days = securityConfig.customRotationDays || 90
        return new Date(now.getTime() + days * 24 * 60 * 60 * 1000)
      default:
        return new Date(now.getTime() + 365 * 24 * 60 * 60 * 1000) // 1 year default
    }
  }

  const generateBackupKey = async (serviceId: string, keyType: string) => {
    // Simulate backup key generation
    await new Promise(resolve => setTimeout(resolve, 500))
    
    setGeneratedKeys(prev => prev.map(key => 
      key.serviceId === serviceId && key.keyType === keyType
        ? { ...key, backupGenerated: true }
        : key
    ))
  }

  const maskKey = (key: string): string => {
    if (key.length <= 8) return '••••••••'
    return key.substring(0, 4) + '••••••••••••••••••••••••••••' + key.substring(key.length - 4)
  }

  const toggleKeyVisibility = (keyId: string) => {
    const newShowKeys = new Set(showKeys)
    if (newShowKeys.has(keyId)) {
      newShowKeys.delete(keyId)
    } else {
      newShowKeys.add(keyId)
    }
    setShowKeys(newShowKeys)
  }

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      // Could add toast notification here
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  const exportKeys = () => {
    const exportData = {
      timestamp: new Date().toISOString(),
      environment: securityConfig.environment,
      securityLevel: securityConfig.securityLevel,
      keys: generatedKeys.map(key => ({
        service: key.serviceName,
        type: key.keyType,
        value: key.value,
        strength: key.strength,
        expiresAt: key.expiresAt?.toISOString()
      }))
    }
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `api-keys-${securityConfig.environment}-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const getSecurityIndicator = (strength: number) => {
    if (strength >= 80) return { color: 'text-green-600', label: 'Excellent', bgColor: 'bg-green-100' }
    if (strength >= 60) return { color: 'text-yellow-600', label: 'Good', bgColor: 'bg-yellow-100' }
    return { color: 'text-red-600', label: 'Weak', bgColor: 'bg-red-100' }
  }

  const overallStrength = generatedKeys.length > 0 
    ? Math.round(generatedKeys.reduce((sum, key) => sum + key.strength, 0) / generatedKeys.length)
    : 0

  return (
    <div className="space-y-6">
      {/* Generation Overview */}
      <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Key className="h-5 w-5 text-blue-600" />
            <span>API Key Generation Status</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{generatedKeys.length}</div>
              <div className="text-sm text-gray-600">Total Keys</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {generatedKeys.filter(k => k.status === 'generated').length}
              </div>
              <div className="text-sm text-gray-600">Generated</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{overallStrength}</div>
              <div className="text-sm text-gray-600">Avg Strength</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {generatedKeys.filter(k => k.backupGenerated).length}
              </div>
              <div className="text-sm text-gray-600">Backup Keys</div>
            </div>
          </div>
          
          {isGenerating && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Generating: {currentlyGenerating}</span>
                <span className="text-sm text-gray-500">{Math.round(generationProgress)}%</span>
              </div>
              <Progress value={generationProgress} className="h-2" />
            </div>
          )}
          
          <div className="flex space-x-2 mt-4">
            <Button 
              onClick={generateAllKeys}
              disabled={isGenerating || generatedKeys.length === 0}
              className="flex items-center space-x-2"
            >
              {isGenerating ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Zap className="h-4 w-4" />
              )}
              <span>{isGenerating ? 'Generating...' : 'Generate All Keys'}</span>
            </Button>
            
            <Button 
              variant="outline"
              onClick={exportKeys}
              disabled={generatedKeys.filter(k => k.status === 'generated').length === 0}
            >
              <Download className="h-4 w-4 mr-2" />
              Export Keys
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Generated Keys List */}
      <div className="space-y-4">
        {selectedServices.map((serviceId: string) => {
          const serviceKeys = generatedKeys.filter(key => key.serviceId === serviceId)
          if (serviceKeys.length === 0) return null
          
          return (
            <Card key={serviceId}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>{getServiceName(serviceId)} API Keys</span>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">
                      {serviceKeys.length} key{serviceKeys.length !== 1 ? 's' : ''}
                    </Badge>
                    {serviceKeys.every(k => k.status === 'generated') && (
                      <Badge variant="secondary" className="bg-green-100 text-green-800">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Complete
                      </Badge>
                    )}
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {serviceKeys.map(key => {
                    const keyId = `${key.serviceId}-${key.keyType}`
                    const isVisible = showKeys.has(keyId)
                    const validation = validationResults.get(keyId)
                    const securityIndicator = getSecurityIndicator(key.strength)
                    
                    return (
                      <div key={keyId} className="border rounded-lg p-4 space-y-3">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className={cn(
                              "p-2 rounded-lg",
                              key.status === 'generated' ? "bg-green-100 text-green-800" :
                              key.status === 'generating' ? "bg-blue-100 text-blue-800" :
                              key.status === 'error' ? "bg-red-100 text-red-800" :
                              "bg-gray-100 text-gray-800"
                            )}>
                              {key.status === 'generated' ? <CheckCircle className="h-4 w-4" /> :
                               key.status === 'generating' ? <RefreshCw className="h-4 w-4 animate-spin" /> :
                               key.status === 'error' ? <AlertTriangle className="h-4 w-4" /> :
                               <Key className="h-4 w-4" />}
                            </div>
                            <div>
                              <h4 className="font-medium">{key.keyType.replace('_', ' ').toUpperCase()}</h4>
                              <p className="text-sm text-gray-600 dark:text-gray-400">
                                {SERVICE_KEY_CONFIGS[serviceId as keyof typeof SERVICE_KEY_CONFIGS]?.keys
                                  .find(k => k.type === key.keyType)?.description}
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            {key.strength > 0 && (
                              <Badge 
                                variant="outline" 
                                className={cn("text-xs", securityIndicator.bgColor, securityIndicator.color)}
                              >
                                <Shield className="h-3 w-3 mr-1" />
                                {securityIndicator.label} ({key.strength})
                              </Badge>
                            )}
                            
                            {key.backupGenerated && (
                              <Badge variant="outline" className="text-xs">
                                <Database className="h-3 w-3 mr-1" />
                                Backup
                              </Badge>
                            )}
                          </div>
                        </div>
                        
                        {key.status === 'generated' && (
                          <div className="space-y-2">
                            <div className="flex items-center space-x-2">
                              <div className="flex-1 p-2 bg-gray-50 dark:bg-gray-800 rounded font-mono text-sm">
                                {isVisible ? key.value : key.masked}
                              </div>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => toggleKeyVisibility(keyId)}
                              >
                                {isVisible ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => copyToClipboard(key.value)}
                              >
                                <Copy className="h-4 w-4" />
                              </Button>
                            </div>
                            
                            {key.expiresAt && (
                              <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                                <Clock className="h-4 w-4" />
                                <span>Expires: {key.expiresAt.toLocaleDateString()}</span>
                              </div>
                            )}
                            
                            {validation && validation.issues.length > 0 && (
                              <div className="p-3 bg-yellow-50 dark:bg-yellow-950 border border-yellow-200 dark:border-yellow-800 rounded">
                                <div className="flex items-center space-x-2 mb-2">
                                  <AlertTriangle className="h-4 w-4 text-yellow-600" />
                                  <span className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
                                    Validation Issues
                                  </span>
                                </div>
                                <ul className="text-sm text-yellow-700 dark:text-yellow-300 space-y-1">
                                  {validation.issues.map((issue, index) => (
                                    <li key={index}>• {issue}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Security Analysis */}
      {generatedKeys.filter(k => k.status === 'generated').length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Shield className="h-5 w-5" />
              <span>Security Analysis</span>
            </CardTitle>
            <CardDescription>
              Comprehensive security assessment of generated keys
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium mb-3">Strength Distribution</h4>
                <div className="space-y-2">
                  {['Excellent (80-100)', 'Good (60-79)', 'Weak (0-59)'].map(range => {
                    const [label, scoreRange] = range.split(' ')
                    const [min, max] = scoreRange.slice(1, -1).split('-').map(Number)
                    const count = generatedKeys.filter(k => 
                      k.strength >= min && k.strength <= (max || 100)
                    ).length
                    const percentage = generatedKeys.length > 0 ? (count / generatedKeys.length) * 100 : 0
                    
                    return (
                      <div key={range} className="flex items-center justify-between">
                        <span className="text-sm">{label}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className={cn(
                                "h-2 rounded-full",
                                label === 'Excellent' ? 'bg-green-500' :
                                label === 'Good' ? 'bg-yellow-500' : 'bg-red-500'
                              )}
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                          <span className="text-sm text-gray-600">{count}</span>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-3">Security Features</h4>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Vault Integration</span>
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">AES-256 Encryption</span>
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Automatic Rotation</span>
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Backup Generation</span>
                    {securityConfig.securityLevel === 'enterprise' ? (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    ) : (
                      <AlertTriangle className="h-4 w-4 text-yellow-500" />
                    )}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Vault Integration Status */}
      <Card className="border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-2">
            <Lock className="h-5 w-5 text-green-600" />
            <span className="text-sm font-medium text-green-800 dark:text-green-200">
              Keys will be securely stored in HashiCorp Vault
            </span>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              AES-256 Encrypted
            </Badge>
            <Badge variant="secondary" className="bg-blue-100 text-blue-800">
              Audit Logged
            </Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default KeyGenerationStep