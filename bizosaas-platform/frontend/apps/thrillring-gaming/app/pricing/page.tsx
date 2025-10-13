"use client"

import { useState } from 'react'
import { Check, Star } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { 
  subscriptionPlans, 
  paymentUtils,
  type Currency
} from '@/lib/payments'



export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly')
  const [currency] = useState<Currency>('USD') // Default to USD for US market
  const [userCountry] = useState('US') // Target US market primarily
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleGetStarted = async (planId: string) => {
    setLoading(true)
    setSelectedPlan(planId)

    try {
      // Redirect to checkout page where user can select payment gateway
      window.location.href = `/checkout?plan=${planId}&billing=${billingCycle}`
    } catch (error) {
      console.error('Navigation error:', error)
    } finally {
      setLoading(false)
      setSelectedPlan(null)
    }
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      
      <main className="flex-1">
        {/* Header Section */}
        <section className="py-20 text-center">
          <div className="container">
            <Badge variant="outline" className="mb-4">
              💰 Transparent Pricing
            </Badge>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Choose Your <span className="text-primary">AI Marketing</span> Plan
            </h1>
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Scale your business with AI-powered marketing automation. 
              Simple pricing for US businesses.
            </p>

            {/* Billing Cycle Toggle */}
            <div className="flex items-center justify-center gap-3 mb-12">
              <span className={`text-sm ${billingCycle === 'monthly' ? 'text-foreground' : 'text-muted-foreground'}`}>
                Monthly
              </span>
              <Switch
                checked={billingCycle === 'yearly'}
                onCheckedChange={(checked) => setBillingCycle(checked ? 'yearly' : 'monthly')}
              />
              <span className={`text-sm ${billingCycle === 'yearly' ? 'text-foreground' : 'text-muted-foreground'}`}>
                Yearly
              </span>
              {billingCycle === 'yearly' && (
                <Badge variant="secondary" className="ml-2">
                  Save up to 20%
                </Badge>
              )}
            </div>
          </div>
        </section>

        {/* Pricing Cards */}
        <section className="pb-20">
          <div className="container">
            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
              {subscriptionPlans.map((plan) => {
                const price = paymentUtils.getPlanPrice(plan, currency, billingCycle)
                const savings = billingCycle === 'yearly' 
                  ? paymentUtils.getSavingsPercentage(plan, currency)
                  : 0

                return (
                  <Card key={plan.id} className={`relative ${plan.popular ? 'ring-2 ring-primary' : ''}`}>
                    {plan.popular && (
                      <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                        <Badge className="bg-primary text-primary-foreground">
                          <Star className="h-3 w-3 mr-1" />
                          Most Popular
                        </Badge>
                      </div>
                    )}
                    
                    <CardHeader className="text-center pb-6">
                      <CardTitle className="text-2xl">{plan.name}</CardTitle>
                      <CardDescription className="text-base">
                        {plan.description}
                      </CardDescription>
                      
                      <div className="mt-6">
                        <div className="flex items-baseline justify-center gap-2">
                          <span className="text-4xl font-bold">
                            {paymentUtils.formatPrice(price, currency)}
                          </span>
                          <span className="text-muted-foreground">
                            /{billingCycle === 'yearly' ? 'year' : 'month'}
                          </span>
                        </div>
                        
                        {billingCycle === 'yearly' && savings > 0 && (
                          <p className="text-sm text-green-600 mt-2">
                            Save {savings}% with yearly billing
                          </p>
                        )}
                        
                        {billingCycle === 'monthly' && (
                          <p className="text-sm text-muted-foreground mt-2">
                            Billed monthly
                          </p>
                        )}
                      </div>
                    </CardHeader>

                    <CardContent className="space-y-6">
                      {/* Features */}
                      <ul className="space-y-3">
                        {plan.features.map((feature, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <Check className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                            <span className="text-sm">{feature}</span>
                          </li>
                        ))}
                      </ul>

                      {/* Primary CTA */}
                      <div className="pt-4 border-t">
                        <Button
                          onClick={() => handleGetStarted(plan.id)}
                          disabled={loading && selectedPlan === plan.id}
                          className={`w-full h-12 ${plan.popular ? 'btn-gradient' : ''}`}
                          variant={plan.popular ? "default" : "outline"}
                        >
                          {loading && selectedPlan === plan.id ? (
                            "Processing..."
                          ) : (
                            `Get Started with ${plan.name}`
                          )}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>

            {/* Money-back guarantee */}
            <div className="mt-16 text-center">
              <div className="max-w-2xl mx-auto">
                <h3 className="text-2xl font-bold mb-4">30-Day Money-Back Guarantee</h3>
                <p className="text-muted-foreground">
                  Try our AI marketing platform risk-free. If you're not completely satisfied, 
                  we'll refund your money within 30 days, no questions asked.
                </p>
              </div>
            </div>

            {/* FAQ Section */}
            <div className="mt-20">
              <h3 className="text-2xl font-bold text-center mb-8">Frequently Asked Questions</h3>
              <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
                <div>
                  <h4 className="font-semibold mb-2">What payment methods do you accept?</h4>
                  <p className="text-sm text-muted-foreground">
                    We accept all major credit cards, PayPal, and other secure payment methods. 
                    Payment options will be available during checkout.
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Can I switch between plans?</h4>
                  <p className="text-sm text-muted-foreground">
                    Yes! You can upgrade or downgrade your plan anytime. Changes take effect at your next billing cycle.
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Is there a free trial?</h4>
                  <p className="text-sm text-muted-foreground">
                    We offer a 7-day free trial for the Professional plan. No credit card required to start.
                  </p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">What's included in all plans?</h4>
                  <p className="text-sm text-muted-foreground">
                    All plans include 24/7 support, API access, and our core AI marketing agents. 
                    Higher tiers add more campaigns and premium features.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  )
}