'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  CreditCard, 
  Download, 
  Calendar, 
  TrendingUp, 
  TrendingDown,
  Crown,
  Zap,
  Star,
  CheckCircle,
  XCircle,
  AlertCircle,
  DollarSign,
  Users,
  Bot,
  BarChart3,
  Mail,
  Target,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
  ExternalLink,
  Clock,
  Gift
} from 'lucide-react'

interface PlanFeature {
  name: string
  included: boolean
  limit?: string
}

interface Plan {
  id: string
  name: string
  price: number
  billing: 'monthly' | 'yearly'
  popular?: boolean
  features: PlanFeature[]
}

interface UsageMetric {
  id: string
  name: string
  current: number
  limit: number
  unit: string
  icon: React.ComponentType<{ className?: string }>
  color: 'green' | 'yellow' | 'red'
}

interface Invoice {
  id: string
  number: string
  date: string
  amount: number
  status: 'paid' | 'pending' | 'failed' | 'draft'
  description: string
  downloadUrl: string
}

interface PaymentMethod {
  id: string
  type: 'card' | 'bank_account' | 'paypal'
  last4?: string
  brand?: string
  expiryMonth?: number
  expiryYear?: number
  isDefault: boolean
}

const plans: Plan[] = [
  {
    id: 'starter',
    name: 'Starter',
    price: 49,
    billing: 'monthly',
    features: [
      { name: 'AI Marketing Campaigns', included: true, limit: '5/month' },
      { name: 'Social Media Accounts', included: true, limit: '3 accounts' },
      { name: 'Lead Generation', included: true, limit: '500/month' },
      { name: 'Email Marketing', included: true, limit: '2,000/month' },
      { name: 'Analytics Dashboard', included: true },
      { name: 'Basic Support', included: true },
      { name: 'API Access', included: false },
      { name: 'Custom Integrations', included: false },
      { name: 'White Label', included: false }
    ]
  },
  {
    id: 'professional',
    name: 'Professional',
    price: 149,
    billing: 'monthly',
    popular: true,
    features: [
      { name: 'AI Marketing Campaigns', included: true, limit: '25/month' },
      { name: 'Social Media Accounts', included: true, limit: '10 accounts' },
      { name: 'Lead Generation', included: true, limit: '2,500/month' },
      { name: 'Email Marketing', included: true, limit: '10,000/month' },
      { name: 'Analytics Dashboard', included: true },
      { name: 'Priority Support', included: true },
      { name: 'API Access', included: true },
      { name: 'Custom Integrations', included: true, limit: '5 integrations' },
      { name: 'White Label', included: false }
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 449,
    billing: 'monthly',
    features: [
      { name: 'AI Marketing Campaigns', included: true, limit: 'Unlimited' },
      { name: 'Social Media Accounts', included: true, limit: 'Unlimited' },
      { name: 'Lead Generation', included: true, limit: 'Unlimited' },
      { name: 'Email Marketing', included: true, limit: 'Unlimited' },
      { name: 'Analytics Dashboard', included: true },
      { name: 'Dedicated Support', included: true },
      { name: 'API Access', included: true },
      { name: 'Custom Integrations', included: true, limit: 'Unlimited' },
      { name: 'White Label', included: true }
    ]
  }
]

const usageMetrics: UsageMetric[] = [
  {
    id: 'campaigns',
    name: 'AI Campaigns',
    current: 12,
    limit: 25,
    unit: 'campaigns',
    icon: Target,
    color: 'green'
  },
  {
    id: 'leads',
    name: 'Lead Generation',
    current: 2245,
    limit: 2500,
    unit: 'leads',
    icon: Users,
    color: 'yellow'
  },
  {
    id: 'emails',
    name: 'Email Sends',
    current: 8756,
    limit: 10000,
    unit: 'emails',
    icon: Mail,
    color: 'green'
  },
  {
    id: 'ai_requests',
    name: 'AI Requests',
    current: 3421,
    limit: 5000,
    unit: 'requests',
    icon: Bot,
    color: 'green'
  }
]

const invoices: Invoice[] = [
  {
    id: 'inv_001',
    number: 'INV-2024-001',
    date: '2024-08-01',
    amount: 149,
    status: 'paid',
    description: 'Professional Plan - August 2024',
    downloadUrl: '/api/invoices/inv_001/download'
  },
  {
    id: 'inv_002',
    number: 'INV-2024-002',
    date: '2024-07-01',
    amount: 149,
    status: 'paid',
    description: 'Professional Plan - July 2024',
    downloadUrl: '/api/invoices/inv_002/download'
  },
  {
    id: 'inv_003',
    number: 'INV-2024-003',
    date: '2024-06-01',
    amount: 149,
    status: 'paid',
    description: 'Professional Plan - June 2024',
    downloadUrl: '/api/invoices/inv_003/download'
  }
]

const paymentMethods: PaymentMethod[] = [
  {
    id: 'pm_001',
    type: 'card',
    brand: 'visa',
    last4: '4242',
    expiryMonth: 12,
    expiryYear: 2027,
    isDefault: true
  },
  {
    id: 'pm_002',
    type: 'card',
    brand: 'mastercard',
    last4: '5555',
    expiryMonth: 8,
    expiryYear: 2026,
    isDefault: false
  }
]

export default function BillingPage() {
  const [currentPlan, setCurrentPlan] = useState('professional')
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly')
  const [isUpgrading, setIsUpgrading] = useState(false)
  const [showAddPayment, setShowAddPayment] = useState(false)

  const getCurrentPlan = () => plans.find(p => p.id === currentPlan)
  const getUsagePercentage = (metric: UsageMetric) => (metric.current / metric.limit) * 100
  
  const getUsageColor = (percentage: number) => {
    if (percentage >= 90) return 'text-red-500'
    if (percentage >= 75) return 'text-yellow-500'
    return 'text-green-500'
  }

  const getStatusBadge = (status: string) => {
    const variants = {
      paid: 'default' as const,
      pending: 'outline' as const,
      failed: 'destructive' as const,
      draft: 'secondary' as const
    }
    
    return (
      <Badge variant={variants[status as keyof typeof variants]}>
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </Badge>
    )
  }

  const getPaymentMethodIcon = (method: PaymentMethod) => {
    if (method.type === 'card') {
      return <CreditCard className="h-4 w-4" />
    }
    return <CreditCard className="h-4 w-4" />
  }

  const handleUpgrade = async (planId: string) => {
    setIsUpgrading(true)
    try {
      // API call to upgrade subscription
      console.log('Upgrading to plan:', planId)
      await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate API call
      setCurrentPlan(planId)
    } catch (error) {
      console.error('Failed to upgrade plan:', error)
    } finally {
      setIsUpgrading(false)
    }
  }

  const handleCancelSubscription = async () => {
    try {
      // API call to cancel subscription
      console.log('Canceling subscription')
    } catch (error) {
      console.error('Failed to cancel subscription:', error)
    }
  }

  const handleDownloadInvoice = (invoice: Invoice) => {
    // API call to download invoice
    window.open(invoice.downloadUrl, '_blank')
  }

  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Billing & Subscription</h2>
          <p className="text-muted-foreground">
            Manage your subscription, usage, and billing information
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Download Receipt
          </Button>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Plan</CardTitle>
            <Crown className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{getCurrentPlan()?.name}</div>
            <p className="text-xs text-muted-foreground">
              ${getCurrentPlan()?.price}/{billingCycle === 'monthly' ? 'month' : 'year'}
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Next Billing</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Sep 1</div>
            <p className="text-xs text-muted-foreground">
              Auto-renewal enabled
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$1,194</div>
            <p className="text-xs text-muted-foreground">
              <ArrowUpRight className="h-3 w-3 inline mr-1" />
              8 months active
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Savings</CardTitle>
            <TrendingDown className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">$357</div>
            <p className="text-xs text-muted-foreground">
              vs hiring agencies
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="usage">Usage</TabsTrigger>
          <TabsTrigger value="plans">Plans</TabsTrigger>
          <TabsTrigger value="invoices">Invoices</TabsTrigger>
          <TabsTrigger value="payment-methods">Payment Methods</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Subscription Status</CardTitle>
                <CardDescription>Your current subscription details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">{getCurrentPlan()?.name} Plan</p>
                    <p className="text-sm text-muted-foreground">
                      ${getCurrentPlan()?.price}/{billingCycle === 'monthly' ? 'month' : 'year'}
                    </p>
                  </div>
                  <Badge variant="default" className="bg-green-100 text-green-800">
                    <CheckCircle className="h-3 w-3 mr-1" />
                    Active
                  </Badge>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Billing Cycle</span>
                    <span className="capitalize">{billingCycle}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Next Payment</span>
                    <span>September 1, 2024</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Auto Renewal</span>
                    <Switch checked={true} />
                  </div>
                </div>

                <div className="pt-4 space-y-2">
                  <Button variant="outline" className="w-full">
                    <Crown className="h-4 w-4 mr-2" />
                    Upgrade Plan
                  </Button>
                  <AlertDialog>
                    <AlertDialogTrigger asChild>
                      <Button variant="outline" className="w-full text-red-600">
                        Cancel Subscription
                      </Button>
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>Cancel Subscription?</AlertDialogTitle>
                        <AlertDialogDescription>
                          Your subscription will remain active until September 1, 2024. 
                          After that, you'll lose access to all premium features.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Keep Subscription</AlertDialogCancel>
                        <AlertDialogAction 
                          onClick={handleCancelSubscription}
                          className="bg-red-600 hover:bg-red-700"
                        >
                          Cancel Subscription
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Usage Summary</CardTitle>
                <CardDescription>Current month usage across all features</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {usageMetrics.map((metric) => {
                  const percentage = getUsagePercentage(metric)
                  const Icon = metric.icon
                  
                  return (
                    <div key={metric.id} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Icon className="h-4 w-4" />
                          <span className="text-sm font-medium">{metric.name}</span>
                        </div>
                        <span className={`text-sm font-medium ${getUsageColor(percentage)}`}>
                          {metric.current.toLocaleString()}/{metric.limit.toLocaleString()}
                        </span>
                      </div>
                      <Progress value={percentage} className="h-2" />
                    </div>
                  )
                })}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="usage" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {usageMetrics.map((metric) => {
              const percentage = getUsagePercentage(metric)
              const Icon = metric.icon
              
              return (
                <Card key={metric.id}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
                    <Icon className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {metric.current.toLocaleString()}
                    </div>
                    <Progress value={percentage} className="mt-2 h-2" />
                    <p className="text-xs text-muted-foreground mt-2">
                      {percentage.toFixed(1)}% of {metric.limit.toLocaleString()} {metric.unit}
                    </p>
                  </CardContent>
                </Card>
              )
            })}
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Usage Alerts</CardTitle>
              <CardDescription>Get notified when you're approaching your limits</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <p className="text-sm font-medium">75% Usage Warning</p>
                  <p className="text-xs text-muted-foreground">
                    Get email alerts when you reach 75% of any limit
                  </p>
                </div>
                <Switch checked={true} />
              </div>
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <p className="text-sm font-medium">90% Usage Warning</p>
                  <p className="text-xs text-muted-foreground">
                    Get urgent alerts when you reach 90% of any limit
                  </p>
                </div>
                <Switch checked={true} />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="plans" className="space-y-4">
          <div className="flex items-center space-x-4 mb-6">
            <div className="flex items-center space-x-2">
              <Switch 
                checked={billingCycle === 'yearly'} 
                onCheckedChange={(checked) => setBillingCycle(checked ? 'yearly' : 'monthly')}
              />
              <Label>Yearly (Save 20%)</Label>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {plans.map((plan) => {
              const price = billingCycle === 'yearly' ? plan.price * 10 : plan.price
              const isCurrent = plan.id === currentPlan
              
              return (
                <Card key={plan.id} className={`relative ${plan.popular ? 'border-primary' : ''}`}>
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                      <Badge className="bg-primary text-primary-foreground">
                        <Star className="h-3 w-3 mr-1" />
                        Most Popular
                      </Badge>
                    </div>
                  )}
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      {plan.name}
                      {isCurrent && <Badge variant="outline">Current</Badge>}
                    </CardTitle>
                    <CardDescription>
                      <span className="text-3xl font-bold">${price}</span>
                      <span className="text-muted-foreground">/{billingCycle === 'monthly' ? 'month' : 'year'}</span>
                      {billingCycle === 'yearly' && (
                        <div className="text-green-600 text-sm mt-1">
                          Save ${plan.price * 2.4}/year
                        </div>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      {plan.features.map((feature, index) => (
                        <div key={index} className="flex items-center space-x-2">
                          {feature.included ? (
                            <CheckCircle className="h-4 w-4 text-green-500" />
                          ) : (
                            <XCircle className="h-4 w-4 text-muted-foreground" />
                          )}
                          <span className={`text-sm ${feature.included ? '' : 'text-muted-foreground'}`}>
                            {feature.name}
                            {feature.limit && (
                              <span className="text-muted-foreground ml-1">({feature.limit})</span>
                            )}
                          </span>
                        </div>
                      ))}
                    </div>
                    
                    <Button 
                      className="w-full" 
                      variant={isCurrent ? "outline" : plan.popular ? "default" : "outline"}
                      onClick={() => !isCurrent && handleUpgrade(plan.id)}
                      disabled={isCurrent || isUpgrading}
                    >
                      {isUpgrading ? (
                        <>
                          <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                          Upgrading...
                        </>
                      ) : isCurrent ? (
                        'Current Plan'
                      ) : (
                        `Upgrade to ${plan.name}`
                      )}
                    </Button>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>

        <TabsContent value="invoices" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Invoice History</CardTitle>
              <CardDescription>Download and view your billing history</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {invoices.map((invoice) => (
                  <div key={invoice.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div>
                        <p className="font-medium">{invoice.number}</p>
                        <p className="text-sm text-muted-foreground">{invoice.description}</p>
                      </div>
                      <div>
                        <p className="text-sm">{new Date(invoice.date).toLocaleDateString()}</p>
                        <p className="text-sm font-medium">${invoice.amount}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(invoice.status)}
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleDownloadInvoice(invoice)}
                      >
                        <Download className="h-4 w-4 mr-1" />
                        Download
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="payment-methods" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>Payment Methods</CardTitle>
                <CardDescription>Manage your payment methods and billing preferences</CardDescription>
              </div>
              <Dialog open={showAddPayment} onOpenChange={setShowAddPayment}>
                <DialogTrigger asChild>
                  <Button>
                    <CreditCard className="h-4 w-4 mr-2" />
                    Add Payment Method
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Add Payment Method</DialogTitle>
                    <DialogDescription>
                      Add a new credit card or payment method to your account
                    </DialogDescription>
                  </DialogHeader>
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="card-number">Card Number</Label>
                      <Input id="card-number" placeholder="1234 5678 9012 3456" />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="expiry">Expiry Date</Label>
                        <Input id="expiry" placeholder="MM/YY" />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="cvc">CVC</Label>
                        <Input id="cvc" placeholder="123" />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="name">Cardholder Name</Label>
                      <Input id="name" placeholder="John Doe" />
                    </div>
                    <div className="flex items-center space-x-2">
                      <Switch />
                      <Label>Set as default payment method</Label>
                    </div>
                    <Button className="w-full">Add Payment Method</Button>
                  </div>
                </DialogContent>
              </Dialog>
            </CardHeader>
            <CardContent className="space-y-4">
              {paymentMethods.map((method) => (
                <div key={method.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    {getPaymentMethodIcon(method)}
                    <div>
                      <p className="font-medium">
                        {method.brand?.toUpperCase()} •••• {method.last4}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Expires {method.expiryMonth?.toString().padStart(2, '0')}/{method.expiryYear}
                      </p>
                    </div>
                    {method.isDefault && (
                      <Badge variant="outline">Default</Badge>
                    )}
                  </div>
                  <div className="flex items-center space-x-2">
                    {!method.isDefault && (
                      <Button variant="outline" size="sm">
                        Set Default
                      </Button>
                    )}
                    <Button variant="outline" size="sm" className="text-red-600">
                      Remove
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}