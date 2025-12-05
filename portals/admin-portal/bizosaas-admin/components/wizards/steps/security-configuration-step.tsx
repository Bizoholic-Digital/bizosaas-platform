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
import { Select } from '../../ui/select'
import { 
  Shield, 
  Lock, 
  Globe, 
  Clock, 
  UserCheck, 
  AlertTriangle,
  CheckCircle,
  Info,
  Settings,
  Key,
  Eye,
  EyeOff,
  MapPin,
  Network
} from 'lucide-react'
import { cn } from '../../../lib/utils'

interface SecurityConfigurationStepProps {
  form: UseFormReturn<any>
  configurations: any[]
  setConfigurations: React.Dispatch<React.SetStateAction<any[]>>
}

const ENVIRONMENT_OPTIONS = [
  {
    value: 'development',
    label: 'Development',
    description: 'Local development and testing environment',
    securityFeatures: ['Basic encryption', 'Local storage', 'Debug logging'],
    icon: <Settings className="h-4 w-4" />,
    color: 'bg-blue-100 text-blue-800 border-blue-200'
  },
  {
    value: 'staging',
    label: 'Staging',
    description: 'Pre-production testing and validation',
    securityFeatures: ['Enhanced encryption', 'Audit logging', 'IP restrictions'],
    icon: <Eye className="h-4 w-4" />,
    color: 'bg-yellow-100 text-yellow-800 border-yellow-200'
  },
  {
    value: 'production',
    label: 'Production',
    description: 'Live production environment with full security',
    securityFeatures: ['Enterprise encryption', 'Full audit trail', 'Multi-factor auth'],
    icon: <Shield className="h-4 w-4" />,
    color: 'bg-green-100 text-green-800 border-green-200'
  }
]

const SECURITY_LEVELS = [
  {
    value: 'basic',
    label: 'Basic Security',
    description: 'Standard security measures for low-risk applications',
    features: [
      'AES-256 encryption',
      'Basic access controls',
      'Standard key rotation',
      'Email notifications'
    ],
    score: 60,
    compliance: ['Basic SOC2'],
    icon: <Lock className="h-5 w-5" />,
    color: 'bg-gray-100 text-gray-800'
  },
  {
    value: 'enhanced',
    label: 'Enhanced Security',
    description: 'Advanced security for business-critical applications',
    features: [
      'AES-256 encryption with HSM',
      'Role-based access control',
      'Automated key rotation',
      'Multi-channel alerts',
      'IP whitelisting',
      'Anomaly detection'
    ],
    score: 80,
    compliance: ['SOC2 Type II', 'GDPR'],
    icon: <Shield className="h-5 w-5" />,
    color: 'bg-blue-100 text-blue-800'
  },
  {
    value: 'enterprise',
    label: 'Enterprise Security',
    description: 'Maximum security for enterprise and regulated environments',
    features: [
      'Hardware Security Module (HSM)',
      'Zero-trust architecture',
      'Continuous key rotation',
      'Real-time monitoring',
      'Geographic restrictions',
      'Behavioral analytics',
      'Compliance reporting',
      'Incident response'
    ],
    score: 95,
    compliance: ['SOC2 Type II', 'GDPR', 'HIPAA', 'PCI-DSS'],
    icon: <Shield className="h-5 w-5" />,
    color: 'bg-green-100 text-green-800'
  }
]

const ROTATION_POLICIES = [
  { value: 'never', label: 'Never', description: 'Keys never expire (not recommended)', risk: 'high' },
  { value: '30-days', label: '30 Days', description: 'Monthly key rotation for high-security', risk: 'low' },
  { value: '60-days', label: '60 Days', description: 'Bi-monthly rotation (recommended)', risk: 'medium' },
  { value: '90-days', label: '90 Days', description: 'Quarterly rotation for standard security', risk: 'medium' },
  { value: 'custom', label: 'Custom', description: 'Define your own rotation schedule', risk: 'variable' }
]

const PERMISSION_LEVELS = [
  {
    value: 'read-only',
    label: 'Read-Only',
    description: 'View and retrieve data only',
    permissions: ['GET requests', 'Data retrieval', 'Status checks'],
    icon: <Eye className="h-4 w-4" />
  },
  {
    value: 'read-write',
    label: 'Read-Write',
    description: 'Full operational access (recommended)',
    permissions: ['GET/POST/PUT requests', 'Data management', 'Configuration changes'],
    icon: <Settings className="h-4 w-4" />
  },
  {
    value: 'admin',
    label: 'Administrator',
    description: 'Full administrative access',
    permissions: ['All HTTP methods', 'User management', 'Security settings', 'Billing access'],
    icon: <UserCheck className="h-4 w-4" />
  }
]

const COMMON_IP_RANGES = [
  { label: 'Office Network', value: '192.168.1.0/24' },
  { label: 'AWS US-East', value: '3.208.0.0/12' },
  { label: 'AWS EU-West', value: '3.248.0.0/13' },
  { label: 'Google Cloud', value: '35.235.240.0/20' },
  { label: 'Cloudflare', value: '103.21.244.0/22' }
]

const SUPPORTED_COUNTRIES = [
  'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
  'Netherlands', 'Australia', 'Japan', 'Singapore', 'India'
]

export function SecurityConfigurationStep({ 
  form,
  configurations,
  setConfigurations
}: SecurityConfigurationStepProps) {
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [securityScore, setSecurityScore] = useState(0)
  const [ipInput, setIpInput] = useState('')
  const [selectedCountries, setSelectedCountries] = useState<string[]>([])

  const formData = form.watch()
  const securityConfig = formData.securityConfiguration || {}

  useEffect(() => {
    calculateSecurityScore()
  }, [securityConfig])

  const calculateSecurityScore = () => {
    let score = 40 // Base score
    
    // Environment scoring
    if (securityConfig.environment === 'production') score += 15
    else if (securityConfig.environment === 'staging') score += 10
    else if (securityConfig.environment === 'development') score += 5
    
    // Security level scoring
    if (securityConfig.securityLevel === 'enterprise') score += 25
    else if (securityConfig.securityLevel === 'enhanced') score += 15
    else if (securityConfig.securityLevel === 'basic') score += 5
    
    // Two-factor authentication
    if (securityConfig.accessControl?.requireTwoFactor) score += 10
    
    // Key rotation
    if (securityConfig.keyRotationPolicy === '30-days') score += 8
    else if (securityConfig.keyRotationPolicy === '60-days') score += 6
    else if (securityConfig.keyRotationPolicy === '90-days') score += 4
    
    // IP restrictions
    if (securityConfig.accessControl?.ipWhitelist?.length > 0) score += 8
    
    // Geographic restrictions
    if (securityConfig.accessControl?.geoRestrictions?.length > 0) score += 7
    
    setSecurityScore(Math.min(score, 100))
  }

  const handleEnvironmentChange = (environment: string) => {
    form.setValue('securityConfiguration.environment', environment)
    
    // Auto-adjust security level based on environment
    if (environment === 'production' && securityConfig.securityLevel === 'basic') {
      form.setValue('securityConfiguration.securityLevel', 'enhanced')
    }
  }

  const handleSecurityLevelChange = (level: string) => {
    form.setValue('securityConfiguration.securityLevel', level)
    
    // Auto-enable features based on security level
    if (level === 'enterprise') {
      form.setValue('securityConfiguration.accessControl.requireTwoFactor', true)
      if (securityConfig.keyRotationPolicy === 'never') {
        form.setValue('securityConfiguration.keyRotationPolicy', '30-days')
      }
    }
  }

  const addIpRange = () => {
    if (!ipInput.trim()) return
    
    const currentList = securityConfig.accessControl?.ipWhitelist || []
    const newList = [...currentList, ipInput.trim()]
    form.setValue('securityConfiguration.accessControl.ipWhitelist', newList)
    setIpInput('')
  }

  const removeIpRange = (ip: string) => {
    const currentList = securityConfig.accessControl?.ipWhitelist || []
    const newList = currentList.filter((item: string) => item !== ip)
    form.setValue('securityConfiguration.accessControl.ipWhitelist', newList)
  }

  const toggleCountry = (country: string) => {
    const current = securityConfig.accessControl?.geoRestrictions || []
    const newList = current.includes(country)
      ? current.filter((c: string) => c !== country)
      : [...current, country]
    
    form.setValue('securityConfiguration.accessControl.geoRestrictions', newList)
    setSelectedCountries(newList)
  }

  const getSecurityLevelConfig = (level: string) => {
    return SECURITY_LEVELS.find(sl => sl.value === level) || SECURITY_LEVELS[0]
  }

  return (
    <div className="space-y-6">
      {/* Security Score Dashboard */}
      <Card className="border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className="h-5 w-5 text-blue-600" />
            <span>Security Configuration Score</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <div className="text-3xl font-bold text-blue-600">
                {securityScore}
              </div>
              <div className="text-lg text-gray-600 dark:text-gray-400">/ 100</div>
            </div>
            <Badge 
              variant="secondary" 
              className={cn(
                securityScore >= 80 ? 'bg-green-100 text-green-800' :
                securityScore >= 60 ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              )}
            >
              {securityScore >= 80 ? 'Excellent' : securityScore >= 60 ? 'Good' : 'Needs Improvement'}
            </Badge>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mb-4">
            <div 
              className={cn(
                "h-3 rounded-full transition-all duration-500",
                securityScore >= 80 ? 'bg-green-500' :
                securityScore >= 60 ? 'bg-yellow-500' :
                'bg-red-500'
              )}
              style={{ width: `${securityScore}%` }}
            />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <CheckCircle className={cn(
                "h-4 w-4",
                securityConfig.environment ? "text-green-500" : "text-gray-400"
              )} />
              <span>Environment</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className={cn(
                "h-4 w-4",
                securityConfig.securityLevel ? "text-green-500" : "text-gray-400"
              )} />
              <span>Security Level</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className={cn(
                "h-4 w-4",
                securityConfig.accessControl?.requireTwoFactor ? "text-green-500" : "text-gray-400"
              )} />
              <span>Two-Factor Auth</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className={cn(
                "h-4 w-4",
                securityConfig.keyRotationPolicy && securityConfig.keyRotationPolicy !== 'never' ? "text-green-500" : "text-gray-400"
              )} />
              <span>Key Rotation</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Environment Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Globe className="h-5 w-5" />
            <span>Environment Configuration</span>
          </CardTitle>
          <CardDescription>
            Select the target environment for your API key deployment
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {ENVIRONMENT_OPTIONS.map(env => {
              const isSelected = securityConfig.environment === env.value
              return (
                <Card
                  key={env.value}
                  className={cn(
                    "cursor-pointer transition-all duration-200 hover:shadow-md",
                    isSelected 
                      ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-950" 
                      : "hover:ring-1 hover:ring-gray-300"
                  )}
                  onClick={() => handleEnvironmentChange(env.value)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center space-x-3 mb-3">
                      <div className={cn("p-2 rounded-lg", env.color)}>
                        {env.icon}
                      </div>
                      <div>
                        <h3 className="font-medium">{env.label}</h3>
                        {isSelected && (
                          <CheckCircle className="h-4 w-4 text-blue-600 mt-1" />
                        )}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      {env.description}
                    </p>
                    <div className="space-y-1">
                      {env.securityFeatures.map(feature => (
                        <div key={feature} className="flex items-center space-x-2 text-xs">
                          <CheckCircle className="h-3 w-3 text-green-500" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Security Level Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className="h-5 w-5" />
            <span>Security Level Configuration</span>
          </CardTitle>
          <CardDescription>
            Choose the appropriate security level for your use case
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {SECURITY_LEVELS.map(level => {
              const isSelected = securityConfig.securityLevel === level.value
              return (
                <Card
                  key={level.value}
                  className={cn(
                    "cursor-pointer transition-all duration-200",
                    isSelected 
                      ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-950" 
                      : "hover:ring-1 hover:ring-gray-300"
                  )}
                  onClick={() => handleSecurityLevelChange(level.value)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        <div className={cn("p-2 rounded-lg", level.color)}>
                          {level.icon}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <h3 className="font-medium">{level.label}</h3>
                            <Badge variant="outline">Score: {level.score}</Badge>
                            {isSelected && (
                              <CheckCircle className="h-4 w-4 text-blue-600" />
                            )}
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                            {level.description}
                          </p>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <p className="text-xs font-medium text-gray-500 mb-2">Security Features:</p>
                              <div className="space-y-1">
                                {level.features.map(feature => (
                                  <div key={feature} className="flex items-center space-x-2 text-xs">
                                    <CheckCircle className="h-3 w-3 text-green-500" />
                                    <span>{feature}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                            <div>
                              <p className="text-xs font-medium text-gray-500 mb-2">Compliance:</p>
                              <div className="flex flex-wrap gap-1">
                                {level.compliance.map(comp => (
                                  <Badge key={comp} variant="outline" className="text-xs">
                                    {comp}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Key Rotation Policy */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Clock className="h-5 w-5" />
            <span>Key Rotation Policy</span>
          </CardTitle>
          <CardDescription>
            Configure automatic key rotation for enhanced security
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {ROTATION_POLICIES.map(policy => {
              const isSelected = securityConfig.keyRotationPolicy === policy.value
              return (
                <Card
                  key={policy.value}
                  className={cn(
                    "cursor-pointer transition-all duration-200",
                    isSelected 
                      ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-950" 
                      : "hover:ring-1 hover:ring-gray-300"
                  )}
                  onClick={() => form.setValue('securityConfiguration.keyRotationPolicy', policy.value)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium">{policy.label}</h3>
                      {isSelected && (
                        <CheckCircle className="h-4 w-4 text-blue-600" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {policy.description}
                    </p>
                    <Badge 
                      variant="outline" 
                      className={cn(
                        "text-xs",
                        policy.risk === 'low' ? 'border-green-300 text-green-700' :
                        policy.risk === 'medium' ? 'border-yellow-300 text-yellow-700' :
                        policy.risk === 'high' ? 'border-red-300 text-red-700' :
                        'border-gray-300 text-gray-700'
                      )}
                    >
                      {policy.risk} risk
                    </Badge>
                  </CardContent>
                </Card>
              )
            })}
          </div>
          
          {securityConfig.keyRotationPolicy === 'custom' && (
            <div className="mt-4 p-4 border rounded-lg bg-gray-50 dark:bg-gray-800">
              <label className="block text-sm font-medium mb-2">
                Custom Rotation Period (days)
              </label>
              <Input
                type="number"
                min="1"
                max="365"
                placeholder="Enter days (1-365)"
                value={securityConfig.customRotationDays || ''}
                onChange={(e) => form.setValue('securityConfiguration.customRotationDays', parseInt(e.target.value))}
                className="w-32"
              />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Access Control */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <UserCheck className="h-5 w-5" />
            <span>Access Control Configuration</span>
          </CardTitle>
          <CardDescription>
            Configure authentication and authorization settings
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Two-Factor Authentication */}
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center space-x-3">
              <Lock className="h-5 w-5 text-blue-600" />
              <div>
                <h4 className="font-medium">Two-Factor Authentication</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Require 2FA for all API key access
                </p>
              </div>
            </div>
            <Button
              variant={securityConfig.accessControl?.requireTwoFactor ? "default" : "outline"}
              onClick={() => form.setValue('securityConfiguration.accessControl.requireTwoFactor', 
                !securityConfig.accessControl?.requireTwoFactor)}
            >
              {securityConfig.accessControl?.requireTwoFactor ? 'Enabled' : 'Enable'}
            </Button>
          </div>

          {/* Permission Level */}
          <div>
            <h4 className="font-medium mb-3">Permission Level</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {PERMISSION_LEVELS.map(perm => {
                const isSelected = securityConfig.accessControl?.permissionLevel === perm.value
                return (
                  <Card
                    key={perm.value}
                    className={cn(
                      "cursor-pointer transition-all duration-200",
                      isSelected 
                        ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-950" 
                        : "hover:ring-1 hover:ring-gray-300"
                    )}
                    onClick={() => form.setValue('securityConfiguration.accessControl.permissionLevel', perm.value)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-2 mb-2">
                        {perm.icon}
                        <h3 className="font-medium">{perm.label}</h3>
                        {isSelected && (
                          <CheckCircle className="h-4 w-4 text-blue-600" />
                        )}
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        {perm.description}
                      </p>
                      <div className="space-y-1">
                        {perm.permissions.slice(0, 2).map(permission => (
                          <div key={permission} className="flex items-center space-x-2 text-xs">
                            <CheckCircle className="h-3 w-3 text-green-500" />
                            <span>{permission}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Security Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>Advanced Security Settings</span>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowAdvanced(!showAdvanced)}
            >
              {showAdvanced ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              {showAdvanced ? 'Hide' : 'Show'} Advanced
            </Button>
          </CardTitle>
        </CardHeader>
        {showAdvanced && (
          <CardContent className="space-y-6">
            {/* IP Whitelisting */}
            <div>
              <h4 className="font-medium mb-3 flex items-center space-x-2">
                <Network className="h-4 w-4" />
                <span>IP Address Whitelisting</span>
              </h4>
              <div className="space-y-3">
                <div className="flex space-x-2">
                  <Input
                    placeholder="Enter IP address or CIDR range (e.g., 192.168.1.0/24)"
                    value={ipInput}
                    onChange={(e) => setIpInput(e.target.value)}
                    className="flex-1"
                  />
                  <Button onClick={addIpRange} disabled={!ipInput.trim()}>
                    Add
                  </Button>
                </div>
                
                {/* Quick Add Common Ranges */}
                <div className="flex flex-wrap gap-2">
                  {COMMON_IP_RANGES.map(range => (
                    <Button
                      key={range.value}
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        const current = securityConfig.accessControl?.ipWhitelist || []
                        if (!current.includes(range.value)) {
                          form.setValue('securityConfiguration.accessControl.ipWhitelist', [...current, range.value])
                        }
                      }}
                    >
                      {range.label}
                    </Button>
                  ))}
                </div>

                {/* Current IP List */}
                {securityConfig.accessControl?.ipWhitelist?.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm font-medium">Whitelisted IP Ranges:</p>
                    <div className="space-y-1">
                      {securityConfig.accessControl.ipWhitelist.map((ip: string) => (
                        <div key={ip} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                          <span className="font-mono text-sm">{ip}</span>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => removeIpRange(ip)}
                          >
                            Remove
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Geographic Restrictions */}
            <div>
              <h4 className="font-medium mb-3 flex items-center space-x-2">
                <MapPin className="h-4 w-4" />
                <span>Geographic Restrictions</span>
              </h4>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                Restrict API access to specific countries/regions
              </p>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-2">
                {SUPPORTED_COUNTRIES.map(country => {
                  const isSelected = securityConfig.accessControl?.geoRestrictions?.includes(country)
                  return (
                    <Button
                      key={country}
                      variant={isSelected ? "default" : "outline"}
                      size="sm"
                      onClick={() => toggleCountry(country)}
                      className="justify-start"
                    >
                      {isSelected && <CheckCircle className="h-3 w-3 mr-1" />}
                      {country}
                    </Button>
                  )
                })}
              </div>
            </div>
          </CardContent>
        )}
      </Card>

      {/* Security Recommendations */}
      {securityScore < 80 && (
        <Card className="border-yellow-200 bg-yellow-50 dark:bg-yellow-950 dark:border-yellow-800">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2 text-yellow-800 dark:text-yellow-200">
              <AlertTriangle className="h-5 w-5" />
              <span>Security Recommendations</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {!securityConfig.accessControl?.requireTwoFactor && (
                <div className="flex items-center space-x-2 text-yellow-700 dark:text-yellow-300">
                  <Info className="h-4 w-4" />
                  <span className="text-sm">Enable two-factor authentication for enhanced security</span>
                </div>
              )}
              {securityConfig.keyRotationPolicy === 'never' && (
                <div className="flex items-center space-x-2 text-yellow-700 dark:text-yellow-300">
                  <Info className="h-4 w-4" />
                  <span className="text-sm">Configure automatic key rotation to reduce security risks</span>
                </div>
              )}
              {(!securityConfig.accessControl?.ipWhitelist || securityConfig.accessControl.ipWhitelist.length === 0) && (
                <div className="flex items-center space-x-2 text-yellow-700 dark:text-yellow-300">
                  <Info className="h-4 w-4" />
                  <span className="text-sm">Consider adding IP restrictions for production environments</span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default SecurityConfigurationStep