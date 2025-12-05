/**
 * CorelDove Shopping Cart Page - View and Manage Cart Items
 * Integrates with Zustand cart store for state management
 */

'use client'

import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '../../components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card'
import { Badge } from '../../components/ui/badge'
import { Input } from '../../components/ui/input'
import { useTenantTheme } from '../../hooks/useTenantTheme'
import { useCart, type CartItem } from '../../lib/stores/cart-store'
import { 
  ArrowRight, 
  ShoppingCart, 
  Plus,
  Minus,
  Trash2,
  ArrowLeft,
  CreditCard,
  Tag,
  Truck,
  Shield
} from 'lucide-react'

export default function CartPage() {
  const { config } = useTenantTheme()
  const { 
    items, 
    totalItems, 
    totalAmount, 
    currency,
    updateQuantity,
    removeItem,
    clearCart
  } = useCart()

  const [promoCode, setPromoCode] = useState('')
  const [promoApplied, setPromoApplied] = useState(false)
  const [promoDiscount, setPromoDiscount] = useState(0)
  const [isUpdating, setIsUpdating] = useState<string | null>(null)

  const handleQuantityChange = async (productId: string, newQuantity: number) => {
    setIsUpdating(productId)
    updateQuantity(productId, newQuantity)
    
    // Simulate API call delay for UX
    setTimeout(() => {
      setIsUpdating(null)
    }, 300)
  }

  const handleRemoveItem = (productId: string) => {
    removeItem(productId)
  }

  const handleApplyPromoCode = () => {
    // Simple promo code logic - in real app, this would call an API
    const validCodes = {
      'WELCOME10': 0.10,
      'SAVE20': 0.20,
      'FIRST15': 0.15
    }
    
    if (validCodes[promoCode as keyof typeof validCodes]) {
      setPromoDiscount(validCodes[promoCode as keyof typeof validCodes])
      setPromoApplied(true)
    } else {
      alert('Invalid promo code')
    }
  }

  const subtotal = totalAmount
  const discountAmount = subtotal * promoDiscount
  const shippingCost = subtotal > 50 ? 0 : 5.99
  const tax = (subtotal - discountAmount + shippingCost) * 0.08 // 8% tax
  const finalTotal = subtotal - discountAmount + shippingCost + tax

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900/95 backdrop-blur supports-[backdrop-filter]:bg-gray-900/90 sticky top-0 z-50">
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
          
          <nav className="ml-auto flex items-center space-x-6">
            <Link href="/products" className="text-sm font-medium text-gray-300 hover:text-white">
              Products
            </Link>
            <Link href="/categories" className="text-sm font-medium text-gray-300 hover:text-white">
              Categories
            </Link>
            <Link href="/about" className="text-sm font-medium text-gray-300 hover:text-white">
              About
            </Link>
            <Link href="/contact" className="text-sm font-medium text-gray-300 hover:text-white">
              Contact
            </Link>
            <Link href="/cart" className="relative text-red-400">
              <ShoppingCart className="h-5 w-5" />
              {totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </Link>
            <Link href="/auth/login">
              <Button size="sm" className="bg-red-500 hover:bg-red-600 text-white">
                Sign In
              </Button>
            </Link>
          </nav>
        </div>
      </header>

      {/* Breadcrumb */}
      <div className="border-b bg-muted/30 py-4">
        <div className="container">
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Link href="/" className="hover:text-foreground">Home</Link>
            <ArrowRight className="h-4 w-4" />
            <span className="text-foreground">Shopping Cart</span>
          </div>
        </div>
      </div>

      <main className="flex-1 py-8">
        <div className="container">
          <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

          {items.length === 0 ? (
            /* Empty Cart */
            <div className="text-center py-16">
              <div className="w-24 h-24 mx-auto bg-muted rounded-full flex items-center justify-center mb-6">
                <ShoppingCart className="h-12 w-12 text-muted-foreground" />
              </div>
              <h2 className="text-2xl font-semibold mb-2">Your cart is empty</h2>
              <p className="text-muted-foreground mb-8">
                Add some products to your cart to get started with your order.
              </p>
              <div className="flex gap-4 justify-center">
                <Button asChild size="lg" className="bg-red-500 hover:bg-red-600">
                  <Link href="/products">
                    Start Shopping
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
                <Button variant="outline" size="lg" asChild>
                  <Link href="/categories">Browse Categories</Link>
                </Button>
              </div>
            </div>
          ) : (
            <div className="grid lg:grid-cols-3 gap-8">
              {/* Cart Items */}
              <div className="lg:col-span-2 space-y-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold">Cart Items ({totalItems})</h2>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={clearCart}
                    className="text-muted-foreground hover:text-destructive"
                  >
                    Clear All
                  </Button>
                </div>

                {items.map((item: CartItem) => (
                  <Card key={item.id}>
                    <CardContent className="p-6">
                      <div className="flex gap-4">
                        {/* Product Image */}
                        <Link href={`/products/${item.slug}`} className="flex-shrink-0">
                          <div className="w-20 h-20 relative overflow-hidden rounded-lg border">
                            {item.thumbnail ? (
                              <Image
                                src={item.thumbnail.url}
                                alt={item.thumbnail.alt}
                                fill
                                className="object-cover"
                              />
                            ) : (
                              <div className="w-full h-full bg-muted flex items-center justify-center">
                                <ShoppingCart className="h-6 w-6 text-muted-foreground" />
                              </div>
                            )}
                          </div>
                        </Link>

                        {/* Product Details */}
                        <div className="flex-1">
                          <div className="flex justify-between items-start">
                            <div>
                              <Link 
                                href={`/products/${item.slug}`}
                                className="font-semibold hover:text-red-500 line-clamp-2"
                              >
                                {item.name}
                              </Link>
                              <Badge variant="outline" className="mt-1">
                                {item.category.name}
                              </Badge>
                              {item.description && (
                                <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                                  {item.description}
                                </p>
                              )}
                            </div>
                            
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleRemoveItem(item.productId)}
                              className="text-muted-foreground hover:text-destructive"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>

                          {/* Price and Quantity Controls */}
                          <div className="flex items-center justify-between mt-4">
                            <div className="flex items-center gap-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleQuantityChange(item.productId, item.quantity - 1)}
                                disabled={item.quantity <= 1 || isUpdating === item.productId}
                              >
                                <Minus className="h-3 w-3" />
                              </Button>
                              <span className="w-12 text-center font-medium">
                                {isUpdating === item.productId ? '...' : item.quantity}
                              </span>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleQuantityChange(item.productId, item.quantity + 1)}
                                disabled={item.quantity >= (item.maxQuantity || 10) || isUpdating === item.productId}
                              >
                                <Plus className="h-3 w-3" />
                              </Button>
                              <span className="text-xs text-muted-foreground ml-2">
                                {!item.inStock ? 'Out of stock' : `${item.maxQuantity || 10} max`}
                              </span>
                            </div>

                            <div className="text-right">
                              <div className="font-semibold text-red-500">
                                ${(item.pricing.priceRange.start.gross.amount * item.quantity).toFixed(2)}
                              </div>
                              <div className="text-sm text-muted-foreground">
                                ${item.pricing.priceRange.start.gross.amount} each
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Order Summary */}
              <div className="space-y-6">
                {/* Promo Code */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Tag className="h-4 w-4" />
                      Promo Code
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex gap-2">
                      <Input
                        placeholder="Enter promo code"
                        value={promoCode}
                        onChange={(e) => setPromoCode(e.target.value)}
                        disabled={promoApplied}
                      />
                      <Button 
                        onClick={handleApplyPromoCode}
                        disabled={!promoCode || promoApplied}
                        variant="outline"
                      >
                        Apply
                      </Button>
                    </div>
                    {promoApplied && (
                      <div className="text-sm text-green-600 flex items-center gap-1">
                        ✓ Promo code applied: {(promoDiscount * 100)}% off
                      </div>
                    )}
                  </CardContent>
                </Card>

                {/* Order Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Order Summary</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between">
                      <span>Subtotal ({totalItems} items)</span>
                      <span>${subtotal.toFixed(2)}</span>
                    </div>
                    
                    {promoApplied && (
                      <div className="flex justify-between text-green-600">
                        <span>Discount ({(promoDiscount * 100)}% off)</span>
                        <span>-${discountAmount.toFixed(2)}</span>
                      </div>
                    )}
                    
                    <div className="flex justify-between">
                      <span>Shipping</span>
                      <span>{shippingCost === 0 ? 'FREE' : `$${shippingCost.toFixed(2)}`}</span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span>Tax</span>
                      <span>${tax.toFixed(2)}</span>
                    </div>
                    
                    <div className="border-t" />
                    
                    <div className="flex justify-between font-semibold text-lg">
                      <span>Total</span>
                      <span className="text-red-500">${finalTotal.toFixed(2)} {currency}</span>
                    </div>
                    
                    <Button className="w-full bg-red-500 hover:bg-red-600" size="lg" asChild>
                      <Link href="/checkout">
                        <CreditCard className="mr-2 h-4 w-4" />
                        Proceed to Checkout
                      </Link>
                    </Button>
                    
                    <Button variant="outline" className="w-full" asChild>
                      <Link href="/products">
                        <ArrowLeft className="mr-2 h-4 w-4" />
                        Continue Shopping
                      </Link>
                    </Button>
                  </CardContent>
                </Card>

                {/* Trust Badges */}
                <Card>
                  <CardContent className="pt-6">
                    <div className="grid grid-cols-3 gap-4 text-center text-sm">
                      <div>
                        <Truck className="h-6 w-6 text-red-500 mx-auto mb-2" />
                        <div className="font-medium">Free Shipping</div>
                        <div className="text-xs text-muted-foreground">Orders $50+</div>
                      </div>
                      <div>
                        <Shield className="h-6 w-6 text-red-500 mx-auto mb-2" />
                        <div className="font-medium">Secure</div>
                        <div className="text-xs text-muted-foreground">SSL Protected</div>
                      </div>
                      <div>
                        <ArrowLeft className="h-6 w-6 text-red-500 mx-auto mb-2 rotate-180" />
                        <div className="font-medium">Easy Returns</div>
                        <div className="text-xs text-muted-foreground">30 days</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white pt-16 pb-8">
        <div className="container">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 pt-8">
            <div>
              <h3 className="font-semibold mb-6">Shop</h3>
              <div className="space-y-3">
                <Link href="/products" className="block text-gray-300 hover:text-white transition-colors">
                  All Products
                </Link>
                <Link href="/categories" className="block text-gray-300 hover:text-white transition-colors">
                  Categories
                </Link>
                <Link href="/products?filter=featured" className="block text-gray-300 hover:text-white transition-colors">
                  Special Deals
                </Link>
                <Link href="/products?filter=new" className="block text-gray-300 hover:text-white transition-colors">
                  New Arrivals
                </Link>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6">Company</h3>
              <div className="space-y-3">
                <Link href="/about" className="block text-gray-300 hover:text-white transition-colors">
                  About Us
                </Link>
                <Link href="/careers" className="block text-gray-300 hover:text-white transition-colors">
                  Careers
                </Link>
                <Link href="/press" className="block text-gray-300 hover:text-white transition-colors">
                  Press
                </Link>
                <Link href="/contact" className="block text-gray-300 hover:text-white transition-colors">
                  Contact
                </Link>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6">Support</h3>
              <div className="space-y-3">
                <Link href="/help" className="block text-gray-300 hover:text-white transition-colors">
                  Help Center
                </Link>
                <Link href="/returns" className="block text-gray-300 hover:text-white transition-colors">
                  Returns
                </Link>
                <Link href="/shipping" className="block text-gray-300 hover:text-white transition-colors">
                  Shipping Info
                </Link>
                <Link href="/track" className="block text-gray-300 hover:text-white transition-colors">
                  Track Order
                </Link>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-6">Legal</h3>
              <div className="space-y-3">
                <Link href="/privacy" className="block text-gray-300 hover:text-white transition-colors">
                  Privacy Policy
                </Link>
                <Link href="/terms" className="block text-gray-300 hover:text-white transition-colors">
                  Terms of Service
                </Link>
                <Link href="/refund" className="block text-gray-300 hover:text-white transition-colors">
                  Refund Policy
                </Link>
              </div>
            </div>
          </div>
          
          <div className="border-t border-gray-800 pt-12 mt-12 text-center text-gray-400">
            <p>&copy; 2024 {config.branding.companyName}. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}