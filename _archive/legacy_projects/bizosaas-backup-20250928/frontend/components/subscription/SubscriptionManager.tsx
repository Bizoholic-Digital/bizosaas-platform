import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { AlertCircle, CheckCircle, CreditCard, DollarSign, Globe, TrendingUp, Users } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface Subscription {
  subscription_status: string;
  plan_id: string;
  limits: {
    operations: number;
    users: number;
    campaigns: number;
  };
  usage: {
    operations: number;
    users: number;
    campaigns: number;
  };
  usage_percentage: {
    operations: number;
    users: number;
    campaigns: number;
  };
  period: {
    start: string;
    end: string;
  };
}

interface Plan {
  plan_id: string;
  name: string;
  features: string[];
  limits: {
    operations: number;
    users: number;
    campaigns: number;
  };
  pricing: {
    currency: string;
    monthly: number;
    yearly: number;
    yearly_discount: number;
  };
}

interface TaxCalculation {
  subtotal: number;
  tax_rate: number;
  tax_amount: number;
  total_amount: number;
  currency: string;
  tax_country: string;
  tax_type: string;
}

const SubscriptionManager: React.FC = () => {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [availablePlans, setAvailablePlans] = useState<Plan[]>([]);
  const [selectedCurrency, setSelectedCurrency] = useState('USD');
  const [selectedBillingCycle, setSelectedBillingCycle] = useState('monthly');
  const [taxCalculation, setTaxCalculation] = useState<TaxCalculation | null>(null);
  const [customerCountry, setCustomerCountry] = useState('US');
  const [loading, setLoading] = useState(false);
  const [showPlanChange, setShowPlanChange] = useState(false);
  const [showCancelDialog, setShowCancelDialog] = useState(false);

  useEffect(() => {
    fetchSubscriptionData();
    fetchAvailablePlans();
  }, [selectedCurrency]);

  const fetchSubscriptionData = async () => {
    try {
      const response = await fetch('/api/subscriptions/current', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      if (data.success) {
        setSubscription(data.subscription);
      }
    } catch (error) {
      console.error('Failed to fetch subscription:', error);
    }
  };

  const fetchAvailablePlans = async () => {
    try {
      const response = await fetch(`/api/subscriptions/plans?currency=${selectedCurrency}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      if (data.success) {
        setAvailablePlans(data.plans);
      }
    } catch (error) {
      console.error('Failed to fetch plans:', error);
    }
  };

  const calculateTax = async (amount: number) => {
    try {
      const response = await fetch('/api/subscriptions/calculate-tax', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          amount,
          currency: selectedCurrency,
          customer_country: customerCountry,
          customer_type: 'b2c'
        })
      });
      const data = await response.json();
      if (data.success) {
        setTaxCalculation(data.tax_calculation);
      }
    } catch (error) {
      console.error('Failed to calculate tax:', error);
    }
  };

  const changePlan = async (newPlanId: string) => {
    setLoading(true);
    try {
      const response = await fetch('/api/subscriptions/change-plan', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          new_plan_id: newPlanId,
          currency: selectedCurrency,
          billing_cycle: selectedBillingCycle,
          prorate: true
        })
      });
      const data = await response.json();
      if (data.success) {
        await fetchSubscriptionData();
        setShowPlanChange(false);
      } else {
        throw new Error(data.detail || 'Plan change failed');
      }
    } catch (error) {
      console.error('Plan change failed:', error);
      alert('Failed to change plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const cancelSubscription = async (immediate: boolean) => {
    setLoading(true);
    try {
      const response = await fetch('/api/subscriptions/cancel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          immediate,
          cancellation_reason: 'User requested cancellation'
        })
      });
      const data = await response.json();
      if (data.success) {
        await fetchSubscriptionData();
        setShowCancelDialog(false);
      } else {
        throw new Error(data.detail || 'Cancellation failed');
      }
    } catch (error) {
      console.error('Cancellation failed:', error);
      alert('Failed to cancel subscription. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'trialing': return 'bg-blue-500';
      case 'past_due': return 'bg-yellow-500';
      case 'canceled': return 'bg-red-500';
      case 'cancel_at_period_end': return 'bg-orange-500';
      default: return 'bg-gray-500';
    }
  };

  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (!subscription) {
    return (
      <Card className="w-full max-w-4xl mx-auto">
        <CardContent className="p-6">
          <div className="text-center">Loading subscription information...</div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Current Subscription Overview */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="flex items-center gap-2">
                <CreditCard className="h-5 w-5" />
                Current Subscription
              </CardTitle>
              <CardDescription>
                Manage your subscription plan and usage
              </CardDescription>
            </div>
            <Badge className={`${getStatusColor(subscription.subscription_status)} text-white`}>
              {subscription.subscription_status}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Plan Information */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">Current Plan</Label>
              <div className="text-2xl font-bold capitalize">
                {subscription.plan_id.replace('_', ' ')}
              </div>
              {subscription.period && (
                <div className="text-sm text-gray-600">
                  Billing period: {formatDate(subscription.period.start)} - {formatDate(subscription.period.end)}
                </div>
              )}
            </div>

            {/* Usage Overview */}
            <div className="space-y-4">
              <Label className="text-sm font-medium">Usage This Period</Label>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Operations</span>
                  <span>{subscription.usage.operations} / {subscription.limits.operations === -1 ? '∞' : subscription.limits.operations}</span>
                </div>
                {subscription.limits.operations !== -1 && (
                  <Progress value={subscription.usage_percentage.operations} className="h-2" />
                )}
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Team Members</span>
                  <span>{subscription.usage.users} / {subscription.limits.users === -1 ? '∞' : subscription.limits.users}</span>
                </div>
                {subscription.limits.users !== -1 && (
                  <Progress value={subscription.usage_percentage.users} className="h-2" />
                )}
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Campaigns</span>
                  <span>{subscription.usage.campaigns} / {subscription.limits.campaigns === -1 ? '∞' : subscription.limits.campaigns}</span>
                </div>
                {subscription.limits.campaigns !== -1 && (
                  <Progress value={subscription.usage_percentage.campaigns} className="h-2" />
                )}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="space-y-3">
              <Label className="text-sm font-medium">Actions</Label>
              <div className="space-y-2">
                <Dialog open={showPlanChange} onOpenChange={setShowPlanChange}>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="w-full">
                      Change Plan
                    </Button>
                  </DialogTrigger>
                  <PlanChangeDialog />
                </Dialog>

                <Dialog open={showCancelDialog} onOpenChange={setShowCancelDialog}>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="w-full text-red-600 hover:text-red-700">
                      Cancel Subscription
                    </Button>
                  </DialogTrigger>
                  <CancelSubscriptionDialog />
                </Dialog>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Usage Warnings */}
      {(subscription.usage_percentage.operations > 80 || 
        subscription.usage_percentage.users > 80 || 
        subscription.usage_percentage.campaigns > 80) && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            You're approaching your usage limits. Consider upgrading your plan to avoid service interruptions.
          </AlertDescription>
        </Alert>
      )}

      {/* Tabs for detailed information */}
      <Tabs defaultValue="billing" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="billing">Billing History</TabsTrigger>
          <TabsTrigger value="usage">Detailed Usage</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>
        
        <TabsContent value="billing" className="space-y-4">
          <BillingHistory />
        </TabsContent>
        
        <TabsContent value="usage" className="space-y-4">
          <UsageAnalytics />
        </TabsContent>
        
        <TabsContent value="settings" className="space-y-4">
          <SubscriptionSettings />
        </TabsContent>
      </Tabs>
    </div>
  );

  function PlanChangeDialog() {
    return (
      <DialogContent className="max-w-4xl">
        <DialogHeader>
          <DialogTitle>Change Subscription Plan</DialogTitle>
          <DialogDescription>
            Select a new plan that better fits your needs. Changes will be prorated.
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="currency">Currency</Label>
              <Select value={selectedCurrency} onValueChange={setSelectedCurrency}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="USD">USD ($)</SelectItem>
                  <SelectItem value="EUR">EUR (€)</SelectItem>
                  <SelectItem value="GBP">GBP (£)</SelectItem>
                  <SelectItem value="INR">INR (₹)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="billing-cycle">Billing Cycle</Label>
              <Select value={selectedBillingCycle} onValueChange={setSelectedBillingCycle}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="monthly">Monthly</SelectItem>
                  <SelectItem value="yearly">Yearly</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {availablePlans.map((plan) => (
              <Card key={plan.plan_id} className={`cursor-pointer transition-colors ${
                plan.plan_id === subscription?.plan_id ? 'ring-2 ring-blue-500' : ''
              }`}>
                <CardHeader>
                  <CardTitle className="text-lg">{plan.name}</CardTitle>
                  <div className="text-2xl font-bold">
                    {formatCurrency(
                      selectedBillingCycle === 'monthly' ? plan.pricing.monthly : plan.pricing.yearly,
                      plan.pricing.currency
                    )}
                    <span className="text-sm font-normal text-gray-600">
                      /{selectedBillingCycle === 'monthly' ? 'month' : 'year'}
                    </span>
                  </div>
                  {selectedBillingCycle === 'yearly' && plan.pricing.yearly_discount > 0 && (
                    <Badge variant="secondary" className="w-fit">
                      Save {plan.pricing.yearly_discount}%
                    </Badge>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Operations</span>
                        <span>{plan.limits.operations === -1 ? 'Unlimited' : plan.limits.operations.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Team Members</span>
                        <span>{plan.limits.users === -1 ? 'Unlimited' : plan.limits.users}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Campaigns</span>
                        <span>{plan.limits.campaigns === -1 ? 'Unlimited' : plan.limits.campaigns}</span>
                      </div>
                    </div>
                    
                    <Separator />
                    
                    <div className="space-y-1">
                      {plan.features.slice(0, 3).map((feature, index) => (
                        <div key={index} className="flex items-center text-sm">
                          <CheckCircle className="h-3 w-3 text-green-500 mr-2 flex-shrink-0" />
                          {feature}
                        </div>
                      ))}
                    </div>

                    {plan.plan_id !== subscription?.plan_id && (
                      <Button 
                        className="w-full"
                        onClick={() => changePlan(plan.plan_id)}
                        disabled={loading}
                      >
                        {loading ? 'Processing...' : 'Select Plan'}
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {taxCalculation && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Tax Calculation</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Subtotal:</span>
                    <span>{formatCurrency(taxCalculation.subtotal, taxCalculation.currency)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>{taxCalculation.tax_type.toUpperCase()} ({(taxCalculation.tax_rate * 100).toFixed(1)}%):</span>
                    <span>{formatCurrency(taxCalculation.tax_amount, taxCalculation.currency)}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between font-medium">
                    <span>Total:</span>
                    <span>{formatCurrency(taxCalculation.total_amount, taxCalculation.currency)}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </DialogContent>
    );
  }

  function CancelSubscriptionDialog() {
    return (
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Cancel Subscription</DialogTitle>
          <DialogDescription>
            Are you sure you want to cancel your subscription? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-4">
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Your subscription will remain active until the end of your current billing period 
              ({subscription?.period ? formatDate(subscription.period.end) : 'end of period'}).
            </AlertDescription>
          </Alert>
          
          <div className="flex gap-3">
            <Button 
              variant="outline" 
              onClick={() => cancelSubscription(false)}
              disabled={loading}
              className="flex-1"
            >
              {loading ? 'Processing...' : 'Cancel at Period End'}
            </Button>
            <Button 
              variant="destructive" 
              onClick={() => cancelSubscription(true)}
              disabled={loading}
              className="flex-1"
            >
              {loading ? 'Processing...' : 'Cancel Immediately'}
            </Button>
          </div>
        </div>
      </DialogContent>
    );
  }

  function BillingHistory() {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Billing History</CardTitle>
          <CardDescription>Your recent invoices and payments</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-gray-500 py-8">
            Billing history will be displayed here
          </div>
        </CardContent>
      </Card>
    );
  }

  function UsageAnalytics() {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Usage Analytics</CardTitle>
          <CardDescription>Detailed breakdown of your usage patterns</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center text-gray-500 py-8">
            Usage analytics will be displayed here
          </div>
        </CardContent>
      </Card>
    );
  }

  function SubscriptionSettings() {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Subscription Settings</CardTitle>
          <CardDescription>Configure your subscription preferences</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <Label htmlFor="country">Country</Label>
              <Select value={customerCountry} onValueChange={setCustomerCountry}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="US">United States</SelectItem>
                  <SelectItem value="GB">United Kingdom</SelectItem>
                  <SelectItem value="DE">Germany</SelectItem>
                  <SelectItem value="FR">France</SelectItem>
                  <SelectItem value="IN">India</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }
};

export default SubscriptionManager;