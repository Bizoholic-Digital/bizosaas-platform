'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Checkbox } from '@/components/ui/checkbox'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Building2, Users, Target, DollarSign, Calendar, Globe, Key, Shield, Zap, Bot } from 'lucide-react'

const businessProfileSchema = z.object({
  // Basic Information
  companyName: z.string().min(2, 'Company name must be at least 2 characters'),
  industry: z.string().min(1, 'Please select an industry'),
  companySize: z.string().min(1, 'Please select company size'),
  website: z.string().url('Please enter a valid website URL').optional().or(z.literal('')),
  
  // Business Details
  businessType: z.string().min(1, 'Please select business type'),
  primaryProducts: z.string().min(10, 'Please describe your primary products/services (min 10 characters)'),
  targetAudience: z.string().min(10, 'Please describe your target audience (min 10 characters)'),
  
  // Goals & Budget
  primaryGoals: z.array(z.string()).min(1, 'Select at least one primary goal'),
  monthlyMarketingBudget: z.string().min(1, 'Please select your marketing budget range'),
  timeframe: z.string().min(1, 'Please select your expected timeframe'),
  
  // Current Marketing
  currentChannels: z.array(z.string()),
  currentChallenges: z.string().optional(),
  
  // BYOK Strategy
  credentialStrategy: z.string().min(1, 'Please select a credential strategy'),
})

type BusinessProfileData = z.infer<typeof businessProfileSchema>

interface BusinessProfileStepProps {
  onComplete: (data: BusinessProfileData) => void
  initialData?: Partial<BusinessProfileData>
}

const INDUSTRIES = [
  'Technology', 'E-commerce', 'Healthcare', 'Finance', 'Real Estate', 
  'Education', 'Manufacturing', 'Retail', 'Professional Services', 
  'Food & Beverage', 'Travel & Tourism', 'Fitness & Wellness', 'Other'
]

const COMPANY_SIZES = [
  '1-10 employees', '11-50 employees', '51-200 employees', 
  '201-1000 employees', '1000+ employees'
]

const BUSINESS_TYPES = [
  'B2B (Business to Business)', 'B2C (Business to Consumer)', 
  'B2B2C (Business to Business to Consumer)', 'Marketplace/Platform'
]

const MARKETING_GOALS = [
  'Increase brand awareness', 'Generate more leads', 'Drive online sales',
  'Improve customer retention', 'Launch new products', 'Expand to new markets',
  'Reduce customer acquisition cost', 'Improve ROI'
]

const BUDGET_RANGES = [
  '$500 - $2,000/month', '$2,000 - $5,000/month', '$5,000 - $10,000/month',
  '$10,000 - $25,000/month', '$25,000 - $50,000/month', '$50,000+/month'
]

const TIMEFRAMES = [
  'Quick wins (1-3 months)', 'Medium term (3-6 months)', 
  'Long term (6-12 months)', 'Ongoing optimization'
]

const CURRENT_CHANNELS = [
  'Google Ads', 'Facebook/Meta Ads', 'LinkedIn Ads', 'TikTok Ads',
  'Email Marketing', 'Content Marketing', 'SEO', 'Social Media',
  'Influencer Marketing', 'Traditional Advertising', 'None currently'
]

const CREDENTIAL_STRATEGIES = {
  bring_your_own_key: {
    name: 'Bring Your Own Keys (BYOK)',
    icon: Key,
    description: 'Use your own API keys for maximum control and cost savings',
    benefits: [
      'Direct billing from platforms',
      'Complete data ownership',
      'Maximum cost savings',
      'Full control over spend'
    ],
    pricing: '$99/month + your platform costs',
    recommended: true
  },
  platform_managed: {
    name: 'Platform Managed',
    icon: Shield,
    description: 'We handle all API keys and platform management for you',
    benefits: [
      'Zero setup required',
      'Managed compliance',
      'Unified billing',
      'Expert optimization'
    ],
    pricing: '$299/month + platform costs',
    recommended: false
  },
  hybrid_mode: {
    name: 'Hybrid Mode',
    icon: Zap,
    description: 'Combine your keys with our managed services',
    benefits: [
      'Best of both worlds',
      'Flexible per platform',
      'Gradual migration',
      'Custom optimization'
    ],
    pricing: '$199/month + platform costs',
    recommended: false
  }
}

export function BusinessProfileStep({ onComplete, initialData = {} }: BusinessProfileStepProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)

  const form = useForm<BusinessProfileData>({
    resolver: zodResolver(businessProfileSchema),
    defaultValues: {
      companyName: '',
      industry: '',
      companySize: '',
      website: '',
      businessType: '',
      primaryProducts: '',
      targetAudience: '',
      primaryGoals: [],
      monthlyMarketingBudget: '',
      timeframe: '',
      currentChannels: [],
      currentChallenges: '',
      credentialStrategy: '',
      ...initialData,
    },
  })

  const onSubmit = async (data: BusinessProfileData) => {
    setIsSubmitting(true)
    try {
      // Simulate API call to save business profile
      await new Promise(resolve => setTimeout(resolve, 1000))
      onComplete(data)
    } catch (error) {
      console.error('Error saving business profile:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        {/* Company Information */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="h-5 w-5 text-blue-600" />
              Company Information
            </CardTitle>
            <CardDescription>
              Basic information about your business
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="companyName"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Company Name *</FormLabel>
                    <FormControl>
                      <Input placeholder="Acme Corporation" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="website"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Website</FormLabel>
                    <FormControl>
                      <Input placeholder="https://acme.com" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <FormField
                control={form.control}
                name="industry"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Industry *</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select industry" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {INDUSTRIES.map((industry) => (
                          <SelectItem key={industry} value={industry}>
                            {industry}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="companySize"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Company Size *</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select size" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {COMPANY_SIZES.map((size) => (
                          <SelectItem key={size} value={size}>
                            {size}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="businessType"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Business Model *</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select type" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {BUSINESS_TYPES.map((type) => (
                          <SelectItem key={type} value={type}>
                            {type}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </CardContent>
        </Card>

        {/* Business Details */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5 text-green-600" />
              Business & Audience
            </CardTitle>
            <CardDescription>
              Tell us about your products and target customers
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField
              control={form.control}
              name="primaryProducts"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Primary Products/Services *</FormLabel>
                  <FormControl>
                    <Textarea 
                      placeholder="Describe your main products or services, what makes them unique, and key benefits..."
                      className="min-h-[100px]"
                      {...field} 
                    />
                  </FormControl>
                  <FormDescription>
                    This helps our AI understand your value proposition and create targeted campaigns
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="targetAudience"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Target Audience *</FormLabel>
                  <FormControl>
                    <Textarea 
                      placeholder="Describe your ideal customers: demographics, pain points, buying behavior, where they spend time online..."
                      className="min-h-[100px]"
                      {...field} 
                    />
                  </FormControl>
                  <FormDescription>
                    The more specific you are, the better we can target your campaigns
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
          </CardContent>
        </Card>

        {/* Goals & Budget */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="h-5 w-5 text-purple-600" />
              Goals & Investment
            </CardTitle>
            <CardDescription>
              What are you looking to achieve and what's your investment level?
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <FormField
              control={form.control}
              name="primaryGoals"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Primary Marketing Goals * (Select all that apply)</FormLabel>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                    {MARKETING_GOALS.map((goal) => (
                      <div key={goal} className="flex items-center space-x-2">
                        <Checkbox
                          id={goal}
                          checked={field.value?.includes(goal)}
                          onCheckedChange={(checked) => {
                            const updatedGoals = checked
                              ? [...(field.value || []), goal]
                              : field.value?.filter((g) => g !== goal) || []
                            field.onChange(updatedGoals)
                          }}
                        />
                        <Label htmlFor={goal} className="text-sm font-normal">
                          {goal}
                        </Label>
                      </div>
                    ))}
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="monthlyMarketingBudget"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Monthly Marketing Budget *</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select budget range" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {BUDGET_RANGES.map((range) => (
                          <SelectItem key={range} value={range}>
                            {range}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="timeframe"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Expected Timeframe *</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select timeframe" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {TIMEFRAMES.map((timeframe) => (
                          <SelectItem key={timeframe} value={timeframe}>
                            {timeframe}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
          </CardContent>
        </Card>

        {/* Current Marketing */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5 text-orange-600" />
              Current Marketing (Optional)
            </CardTitle>
            <CardDescription>
              Help us understand your current marketing efforts
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField
              control={form.control}
              name="currentChannels"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Current Marketing Channels (Select all that apply)</FormLabel>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    {CURRENT_CHANNELS.map((channel) => (
                      <div key={channel} className="flex items-center space-x-2">
                        <Checkbox
                          id={channel}
                          checked={field.value?.includes(channel)}
                          onCheckedChange={(checked) => {
                            const updatedChannels = checked
                              ? [...(field.value || []), channel]
                              : field.value?.filter((c) => c !== channel) || []
                            field.onChange(updatedChannels)
                          }}
                        />
                        <Label htmlFor={channel} className="text-sm font-normal">
                          {channel}
                        </Label>
                      </div>
                    ))}
                  </div>
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="currentChallenges"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Current Marketing Challenges</FormLabel>
                  <FormControl>
                    <Textarea 
                      placeholder="What marketing challenges are you facing? What's not working? What would you like to improve?"
                      className="min-h-[80px]"
                      {...field} 
                    />
                  </FormControl>
                  <FormDescription>
                    This helps us prioritize solutions that address your specific pain points
                  </FormDescription>
                </FormItem>
              )}
            />
          </CardContent>
        </Card>

        {/* BYOK Credential Strategy */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Key className="h-5 w-5 text-blue-600" />
              API Key Management Strategy
            </CardTitle>
            <CardDescription>
              Choose how you'd like to manage your advertising platform API keys
            </CardDescription>
          </CardHeader>
          <CardContent>
            <FormField
              control={form.control}
              name="credentialStrategy"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Select your preferred approach *</FormLabel>
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                    {Object.entries(CREDENTIAL_STRATEGIES).map(([strategyKey, strategy]) => {
                      const IconComponent = strategy.icon;
                      const isSelected = field.value === strategyKey;
                      
                      return (
                        <Card
                          key={strategyKey}
                          className={`cursor-pointer transition-all hover:shadow-lg ${
                            isSelected ? 'ring-2 ring-primary bg-primary/5' : ''
                          } ${strategy.recommended ? 'ring-1 ring-green-300 bg-green-50/50' : ''}`}
                          onClick={() => field.onChange(strategyKey)}
                        >
                          <CardContent className="p-4">
                            <div className="flex items-start justify-between mb-3">
                              <div className="flex items-center gap-2">
                                <IconComponent className="h-5 w-5 text-primary" />
                                <h4 className="font-semibold text-sm">{strategy.name}</h4>
                              </div>
                              {strategy.recommended && (
                                <Badge className="bg-green-500 text-white text-xs">
                                  Recommended
                                </Badge>
                              )}
                            </div>
                            
                            <p className="text-sm text-muted-foreground mb-4">
                              {strategy.description}
                            </p>
                            
                            <div className="space-y-2 mb-4">
                              {strategy.benefits.slice(0, 3).map((benefit, index) => (
                                <div key={index} className="flex items-center gap-2 text-xs">
                                  <div className="w-1 h-1 bg-green-500 rounded-full" />
                                  <span className="text-muted-foreground">{benefit}</span>
                                </div>
                              ))}
                            </div>
                            
                            <div className="text-sm font-medium text-primary">
                              {strategy.pricing}
                            </div>
                          </CardContent>
                        </Card>
                      );
                    })}
                  </div>
                  <FormDescription className="mt-4">
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <div className="flex items-start gap-3">
                        <div className="w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                          <span className="text-white text-xs font-bold">?</span>
                        </div>
                        <div className="text-sm">
                          <p className="font-medium text-blue-900 mb-1">Not sure which to choose?</p>
                          <p className="text-blue-700">
                            <strong>BYOK is recommended</strong> for most businesses as it provides maximum cost savings 
                            and control. You can always switch strategies later from your dashboard.
                          </p>
                        </div>
                      </div>
                    </div>
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />
          </CardContent>
        </Card>

        {/* Submit */}
        <div className="flex justify-end gap-4">
          <Button
            type="submit"
            size="lg"
            disabled={isSubmitting}
            className="min-w-[200px]"
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Saving Profile...
              </>
            ) : (
              'Continue to Integrations →'
            )}
          </Button>
        </div>
      </form>
    </Form>
  )
}