/**
 * CorelDove Checkout Page - Complete Order Process
 * Multi-step checkout with payment integration
 */

'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Input } from '../../components/ui/input'
import { Label } from '../../components/ui/label'
import { Textarea } from '../../components/ui/textarea'
import { Checkbox } from '../../components/ui/checkbox'
import { RadioGroup, RadioGroupItem } from '../../components/ui/radio-group'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../../components/ui/select'
import { Separator } from '../../components/ui/separator'
import { useTenantTheme } from '../../hooks/useTenantTheme'
import { useCart } from '../../lib/stores/cart-store'
import { 
  ArrowRight, 
  ArrowLeft,
  CreditCard,
  Truck,
  Shield,
  Check,
  User,
  MapPin,
  Package,
  Lock
} from 'lucide-react'

interface CheckoutStep {
  id: string
  title: string
  icon: React.ReactNode
  completed: boolean
}

interface BillingInfo {
  firstName: string
  lastName: string
  email: string
  phone: string
  address: string
  address2?: string
  city: string
  state: string
  zipCode: string
  country: string
}

interface ShippingMethod {
  id: string
  name: string
  description: string
  price: number
  estimatedDays: string
}

interface PaymentMethod {
  id: string
  name: string
  description: string
  icon: string
}

export default function CheckoutPage() {
  const { config } = useTenantTheme()
  const { items, totalAmount, currency, clearCart } = useCart()
  
  const [currentStep, setCurrentStep] = useState(0)
  const [billingInfo, setBillingInfo] = useState<BillingInfo>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    address2: '',
    city: '',
    state: '',
    zipCode: '',
    country: 'US'
  })
  const [sameAsShipping, setSameAsShipping] = useState(true)
  const [shippingInfo, setShippingInfo] = useState<BillingInfo>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    address2: '',
    city: '',
    state: '',
    zipCode: '',
    country: 'US'
  })
  const [selectedShipping, setSelectedShipping] = useState<string>('standard')
  const [selectedPayment, setSelectedPayment] = useState<string>('stripe')
  const [isProcessing, setIsProcessing] = useState(false)
  const [orderComplete, setOrderComplete] = useState(false)

  const steps: CheckoutStep[] = [
    {
      id: 'billing',
      title: 'Billing Information',
      icon: <User className="h-5 w-5" />,
      completed: false
    },
    {
      id: 'shipping',
      title: 'Shipping Method',
      icon: <Truck className="h-5 w-5" />,
      completed: false
    },
    {
      id: 'payment',
      title: 'Payment',
      icon: <CreditCard className="h-5 w-5" />,
      completed: false
    },
    {
      id: 'review',
      title: 'Review Order',
      icon: <Package className="h-5 w-5" />,
      completed: false
    }
  ]

  const shippingMethods: ShippingMethod[] = [
    {
      id: 'standard',
      name: 'Standard Shipping',
      description: 'Business days delivery',
      price: 5.99,
      estimatedDays: '5-7'
    },
    {
      id: 'express',
      name: 'Express Shipping',
      description: 'Faster delivery',
      price: 12.99,
      estimatedDays: '2-3'
    },
    {
      id: 'overnight',
      name: 'Overnight Shipping',
      description: 'Next business day',
      price: 24.99,
      estimatedDays: '1'
    }
  ]

  const paymentMethods: PaymentMethod[] = [
    {
      id: 'stripe',
      name: 'Credit Card',
      description: 'Visa, Mastercard, American Express',
      icon: 'credit-card'
    },
    {
      id: 'paypal',
      name: 'PayPal',
      description: 'Pay with your PayPal account',
      icon: 'paypal'
    },
    {
      id: 'apple-pay',
      name: 'Apple Pay',
      description: 'Pay with Touch ID or Face ID',
      icon: 'apple'
    }
  ]

  // Redirect to cart if empty
  useEffect(() => {
    if (items.length === 0 && !orderComplete) {
      window.location.href = '/cart'
    }
  }, [items.length, orderComplete])

  const selectedShippingMethod = shippingMethods.find(m => m.id === selectedShipping)
  const subtotal = totalAmount
  const shippingCost = selectedShippingMethod?.price || 0
  const tax = (subtotal + shippingCost) * 0.08
  const finalTotal = subtotal + shippingCost + tax

  const handleBillingInfoChange = (field: keyof BillingInfo, value: string) => {
    setBillingInfo(prev => ({ ...prev, [field]: value }))
    
    if (sameAsShipping) {
      setShippingInfo(prev => ({ ...prev, [field]: value }))
    }
  }

  const validateStep = (stepIndex: number): boolean => {
    switch (stepIndex) {
      case 0: // Billing
        return !!(billingInfo.firstName && billingInfo.lastName && billingInfo.email && 
                 billingInfo.address && billingInfo.city && billingInfo.state && billingInfo.zipCode)
      case 1: // Shipping
        return !!selectedShipping
      case 2: // Payment
        return !!selectedPayment
      default:
        return true
    }
  }

  const handleNextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, steps.length - 1))
    }
  }

  const handlePrevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0))
  }

  const handlePlaceOrder = async () => {
    setIsProcessing(true)
    
    try {
      // Simulate order processing
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // In a real app, this would call your order API
      const orderData = {
        items,
        billingInfo: sameAsShipping ? billingInfo : { billing: billingInfo, shipping: shippingInfo },
        shippingMethod: selectedShippingMethod,
        paymentMethod: selectedPayment,
        subtotal,
        shippingCost,
        tax,
        total: finalTotal
      }
      
      console.log('Order placed:', orderData)
      
      // Clear cart and show success
      clearCart()
      setOrderComplete(true)
      
    } catch (error) {
      console.error('Order failed:', error)
      alert('Order failed. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  if (orderComplete) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen py-16">
        <div className="text-center max-w-md">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <Check className="h-10 w-10 text-green-600" />
          </div>
          <h1 className="text-3xl font-bold mb-4">Order Confirmed!</h1>
          <p className="text-muted-foreground mb-8">
            Thank you for your order. We'll send you a confirmation email shortly with your order details and tracking information.
          </p>
          <div className="flex gap-4 justify-center">
            <Button asChild>
              <Link href="/products">Continue Shopping</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/orders">View Orders</Link>
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <Link href="/" className="flex items-center space-x-2">
            <Image
              src={config.branding.logo}
              alt={config.branding.companyName}
              width={120}
              height={40}
              className="h-8 w-auto"
              priority
            />
          </Link>
          <div className="ml-auto flex items-center space-x-2">
            <Lock className="h-4 w-4 text-green-600" />
            <span className="text-sm text-green-600">Secure Checkout</span>
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="border-b bg-muted/30 py-6">
        <div className="container">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                  index <= currentStep 
                    ? 'bg-red-500 border-red-500 text-white' 
                    : 'border-gray-300 text-gray-300'
                }`}>
                  {index < currentStep ? <Check className="h-5 w-5" /> : step.icon}
                </div>
                <span className={`ml-3 text-sm font-medium ${
                  index <= currentStep ? 'text-foreground' : 'text-muted-foreground'
                }`}>
                  {step.title}
                </span>
                {index < steps.length - 1 && (
                  <div className={`w-12 h-0.5 ml-6 ${
                    index < currentStep ? 'bg-red-500' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <main className="flex-1 py-8">
        <div className="container">
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Checkout Form */}
            <div className="lg:col-span-2 space-y-8">
              {/* Step 1: Billing Information */}
              {currentStep === 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <User className="h-5 w-5" />
                      Billing Information
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="firstName">First Name *</Label>
                        <Input
                          id="firstName"
                          value={billingInfo.firstName}
                          onChange={(e) => handleBillingInfoChange('firstName', e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="lastName">Last Name *</Label>
                        <Input
                          id="lastName"
                          value={billingInfo.lastName}
                          onChange={(e) => handleBillingInfoChange('lastName', e.target.value)}
                          required
                        />
                      </div>
                    </div>
                    
                    <div>
                      <Label htmlFor="email">Email Address *</Label>
                      <Input
                        id="email"
                        type="email"
                        value={billingInfo.email}
                        onChange={(e) => handleBillingInfoChange('email', e.target.value)}
                        required
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="phone">Phone Number</Label>
                      <Input
                        id="phone"
                        type="tel"
                        value={billingInfo.phone}
                        onChange={(e) => handleBillingInfoChange('phone', e.target.value)}
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="address">Street Address *</Label>
                      <Input
                        id="address"
                        value={billingInfo.address}
                        onChange={(e) => handleBillingInfoChange('address', e.target.value)}
                        required
                      />
                    </div>
                    
                    <div>
                      <Label htmlFor="address2">Apartment, suite, etc. (optional)</Label>
                      <Input
                        id="address2"
                        value={billingInfo.address2}
                        onChange={(e) => handleBillingInfoChange('address2', e.target.value)}
                      />
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <Label htmlFor="city">City *</Label>
                        <Input
                          id="city"
                          value={billingInfo.city}
                          onChange={(e) => handleBillingInfoChange('city', e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="state">State *</Label>
                        <Input
                          id="state"
                          value={billingInfo.state}
                          onChange={(e) => handleBillingInfoChange('state', e.target.value)}
                          required
                        />
                      </div>
                      <div>
                        <Label htmlFor="zipCode">ZIP Code *</Label>
                        <Input
                          id="zipCode"
                          value={billingInfo.zipCode}
                          onChange={(e) => handleBillingInfoChange('zipCode', e.target.value)}
                          required
                        />
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="sameAsShipping"
                        checked={sameAsShipping}
                        onCheckedChange={(checked) => setSameAsShipping(checked as boolean)}
                      />
                      <Label htmlFor="sameAsShipping">Shipping address is the same as billing address</Label>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Step 2: Shipping Method */}
              {currentStep === 1 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Truck className="h-5 w-5" />
                      Shipping Method
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <RadioGroup value={selectedShipping} onValueChange={setSelectedShipping}>
                      {shippingMethods.map((method) => (
                        <div key={method.id} className="flex items-center space-x-3 border rounded-lg p-4">
                          <RadioGroupItem value={method.id} id={method.id} />
                          <div className="flex-1">
                            <Label htmlFor={method.id} className="font-medium cursor-pointer">
                              {method.name}
                            </Label>
                            <p className="text-sm text-muted-foreground">{method.description}</p>
                            <p className="text-sm text-muted-foreground">{method.estimatedDays} business days</p>
                          </div>
                          <div className="font-semibold">
                            {method.price === 0 ? 'FREE' : `$${method.price.toFixed(2)}`}
                          </div>
                        </div>
                      ))}
                    </RadioGroup>
                  </CardContent>
                </Card>
              )}

              {/* Step 3: Payment Method */}
              {currentStep === 2 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <CreditCard className="h-5 w-5" />
                      Payment Method
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <RadioGroup value={selectedPayment} onValueChange={setSelectedPayment}>
                      {paymentMethods.map((method) => (
                        <div key={method.id} className="flex items-center space-x-3 border rounded-lg p-4">
                          <RadioGroupItem value={method.id} id={method.id} />
                          <div className="flex-1">
                            <Label htmlFor={method.id} className="font-medium cursor-pointer">
                              {method.name}
                            </Label>
                            <p className="text-sm text-muted-foreground">{method.description}</p>
                          </div>
                        </div>
                      ))}
                    </RadioGroup>
                    
                    {selectedPayment === 'stripe' && (
                      <div className="space-y-4 border-t pt-4">
                        <div>
                          <Label htmlFor="cardNumber">Card Number</Label>
                          <Input id="cardNumber" placeholder="1234 5678 9012 3456" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <Label htmlFor="expiry">Expiry Date</Label>
                            <Input id="expiry" placeholder="MM/YY" />
                          </div>
                          <div>
                            <Label htmlFor="cvv">CVV</Label>
                            <Input id="cvv" placeholder="123" />
                          </div>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              {/* Step 4: Review Order */}
              {currentStep === 3 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Package className="h-5 w-5" />
                      Review Your Order
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Order Items */}
                    <div>
                      <h3 className="font-semibold mb-4">Order Items</h3>
                      {items.map((item) => (
                        <div key={item.id} className="flex justify-between py-2">
                          <div>
                            <span className="font-medium">{item.name}</span>
                            <span className="text-muted-foreground ml-2">× {item.quantity}</span>
                          </div>
                          <span>${(item.pricing.priceRange.start.gross.amount * item.quantity).toFixed(2)}</span>
                        </div>
                      ))}
                    </div>
                    
                    <Separator />
                    
                    {/* Billing & Shipping */}
                    <div className="grid grid-cols-2 gap-8">
                      <div>
                        <h3 className="font-semibold mb-2">Billing Address</h3>
                        <p className="text-sm text-muted-foreground">
                          {billingInfo.firstName} {billingInfo.lastName}<br />
                          {billingInfo.address}<br />
                          {billingInfo.city}, {billingInfo.state} {billingInfo.zipCode}
                        </p>
                      </div>
                      <div>
                        <h3 className="font-semibold mb-2">Shipping Method</h3>
                        <p className="text-sm text-muted-foreground">
                          {selectedShippingMethod?.name}<br />
                          {selectedShippingMethod?.estimatedDays} business days
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Navigation Buttons */}
              <div className="flex justify-between">
                <Button
                  variant="outline"
                  onClick={handlePrevStep}
                  disabled={currentStep === 0}
                >
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </Button>
                
                {currentStep < steps.length - 1 ? (
                  <Button
                    onClick={handleNextStep}
                    disabled={!validateStep(currentStep)}
                    className="bg-red-500 hover:bg-red-600"
                  >
                    Continue
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                ) : (
                  <Button
                    onClick={handlePlaceOrder}
                    disabled={isProcessing}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    {isProcessing ? 'Processing...' : 'Place Order'}
                    <CreditCard className="ml-2 h-4 w-4" />
                  </Button>
                )}
              </div>
            </div>

            {/* Order Summary */}
            <div>
              <Card className="sticky top-6">
                <CardHeader>
                  <CardTitle>Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between">
                    <span>Subtotal</span>
                    <span>${subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Shipping</span>
                    <span>${shippingCost.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Tax</span>
                    <span>${tax.toFixed(2)}</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between font-semibold text-lg">
                    <span>Total</span>
                    <span className="text-red-500">${finalTotal.toFixed(2)} {currency}</span>
                  </div>
                  
                  {/* Trust Badges */}
                  <div className="pt-4 space-y-2">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Shield className="h-4 w-4 text-green-600" />
                      <span>SSL Secure Checkout</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Truck className="h-4 w-4 text-green-600" />
                      <span>Free shipping on orders over $50</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}