'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Eye, EyeOff, Mail, Lock, User, Building, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { useToast } from '@/hooks/use-toast'

export function RegisterForm() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    companyName: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [agreements, setAgreements] = useState({
    terms: false,
    privacy: false,
    marketing: false,
  })
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleAgreementChange = (field: string, checked: boolean) => {
    setAgreements(prev => ({ ...prev, [field]: checked }))
  }

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      toast({
        title: 'Password mismatch',
        description: 'Please make sure your passwords match.',
        variant: 'destructive',
      })
      return false
    }

    if (!agreements.terms || !agreements.privacy) {
      toast({
        title: 'Agreement required',
        description: 'Please accept the terms of service and privacy policy.',
        variant: 'destructive',
      })
      return false
    }

    return true
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return
    
    setIsLoading(true)

    try {
      // TODO: Implement actual registration
      await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate API call
      
      toast({
        title: 'Account created successfully!',
        description: 'Welcome to BizoSaaS. Redirecting to onboarding...',
      })
      
      // Redirect to onboarding
      router.push('/onboarding')
    } catch (error) {
      toast({
        title: 'Registration failed',
        description: 'Please try again or contact support if the problem persists.',
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Name Fields */}
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="firstName">First name</Label>
          <div className="relative">
            <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              id="firstName"
              type="text"
              placeholder="John"
              value={formData.firstName}
              onChange={(e) => handleInputChange('firstName', e.target.value)}
              className="pl-10"
              required
              disabled={isLoading}
            />
          </div>
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="lastName">Last name</Label>
          <Input
            id="lastName"
            type="text"
            placeholder="Doe"
            value={formData.lastName}
            onChange={(e) => handleInputChange('lastName', e.target.value)}
            required
            disabled={isLoading}
          />
        </div>
      </div>
      
      {/* Company Name */}
      <div className="space-y-2">
        <Label htmlFor="companyName">Company name</Label>
        <div className="relative">
          <Building className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            id="companyName"
            type="text"
            placeholder="Your company name"
            value={formData.companyName}
            onChange={(e) => handleInputChange('companyName', e.target.value)}
            className="pl-10"
            required
            disabled={isLoading}
          />
        </div>
      </div>
      
      {/* Email */}
      <div className="space-y-2">
        <Label htmlFor="email">Email address</Label>
        <div className="relative">
          <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            id="email"
            type="email"
            placeholder="john@company.com"
            value={formData.email}
            onChange={(e) => handleInputChange('email', e.target.value)}
            className="pl-10"
            required
            disabled={isLoading}
          />
        </div>
      </div>
      
      {/* Password */}
      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <div className="relative">
          <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            placeholder="Create a strong password"
            value={formData.password}
            onChange={(e) => handleInputChange('password', e.target.value)}
            className="pl-10 pr-10"
            required
            disabled={isLoading}
          />
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
            onClick={() => setShowPassword(!showPassword)}
            disabled={isLoading}
          >
            {showPassword ? (
              <EyeOff className="h-4 w-4 text-muted-foreground" />
            ) : (
              <Eye className="h-4 w-4 text-muted-foreground" />
            )}
          </Button>
        </div>
      </div>
      
      {/* Confirm Password */}
      <div className="space-y-2">
        <Label htmlFor="confirmPassword">Confirm password</Label>
        <div className="relative">
          <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            id="confirmPassword"
            type={showConfirmPassword ? 'text' : 'password'}
            placeholder="Confirm your password"
            value={formData.confirmPassword}
            onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
            className="pl-10 pr-10"
            required
            disabled={isLoading}
          />
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            disabled={isLoading}
          >
            {showConfirmPassword ? (
              <EyeOff className="h-4 w-4 text-muted-foreground" />
            ) : (
              <Eye className="h-4 w-4 text-muted-foreground" />
            )}
          </Button>
        </div>
      </div>
      
      {/* Agreements */}
      <div className="space-y-4">
        <div className="flex items-start space-x-2">
          <Checkbox
            id="terms"
            checked={agreements.terms}
            onCheckedChange={(checked) => handleAgreementChange('terms', !!checked)}
            disabled={isLoading}
          />
          <Label htmlFor="terms" className="text-sm leading-relaxed">
            I agree to the{' '}
            <a href="/terms" className="text-primary hover:underline">
              Terms of Service
            </a>{' '}
            and{' '}
            <a href="/privacy" className="text-primary hover:underline">
              Privacy Policy
            </a>
          </Label>
        </div>
        
        <div className="flex items-start space-x-2">
          <Checkbox
            id="marketing"
            checked={agreements.marketing}
            onCheckedChange={(checked) => handleAgreementChange('marketing', !!checked)}
            disabled={isLoading}
          />
          <Label htmlFor="marketing" className="text-sm leading-relaxed text-muted-foreground">
            I would like to receive marketing emails about new features and updates
          </Label>
        </div>
      </div>
      
      <Button 
        type="submit" 
        className="w-full" 
        disabled={isLoading || !agreements.terms}
      >
        {isLoading ? (
          <>
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-background border-t-transparent" />
            Creating account...
          </>
        ) : (
          <>
            Create Account
            <ArrowRight className="ml-2 h-4 w-4" />
          </>
        )}
      </Button>
    </form>
  )
}