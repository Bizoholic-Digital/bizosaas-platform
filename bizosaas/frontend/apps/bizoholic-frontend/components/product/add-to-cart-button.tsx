"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { toast } from "sonner"
import { SaleorProduct, SaleorProductVariant } from "@/lib/saleor-api"
import { cn } from "@/lib/utils"
import { ShoppingCart, Loader2, CheckCircle } from "lucide-react"

interface AddToCartButtonProps {
  product: SaleorProduct
  variant: SaleorProductVariant | null
  quantity: number
  disabled?: boolean
  className?: string
  size?: "sm" | "default" | "lg"
}

export function AddToCartButton({
  product,
  variant,
  quantity,
  disabled = false,
  className,
  size = "default"
}: AddToCartButtonProps) {
  const [isAdding, setIsAdding] = useState(false)
  const [isAdded, setIsAdded] = useState(false)

  const handleAddToCart = async () => {
    if (!variant || disabled) return

    try {
      setIsAdding(true)
      
      // Simulate API call to add to cart
      // In a real implementation, this would call your cart API
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Add to cart logic here
      const cartItem = {
        productId: product.id,
        variantId: variant.id,
        quantity,
        title: product.name,
        price: variant.pricing?.price?.gross.amount || 0,
        image: product.thumbnail?.url || product.media?.[0]?.url,
        sku: variant.sku
      }

      // Store in localStorage as a simple cart implementation
      const existingCart = JSON.parse(localStorage.getItem('cart') || '[]')
      const existingItemIndex = existingCart.findIndex(
        (item: any) => item.variantId === variant.id
      )

      if (existingItemIndex >= 0) {
        existingCart[existingItemIndex].quantity += quantity
      } else {
        existingCart.push(cartItem)
      }

      localStorage.setItem('cart', JSON.stringify(existingCart))
      
      // Dispatch cart update event
      window.dispatchEvent(new CustomEvent('cartUpdated', { detail: existingCart }))
      
      setIsAdded(true)
      toast.success(`Added ${product.name} to cart!`, {
        description: `Quantity: ${quantity}`,
      })
      
      // Reset added state after 2 seconds
      setTimeout(() => setIsAdded(false), 2000)
      
    } catch (error) {
      console.error('Failed to add to cart:', error)
      toast.error('Failed to add to cart', {
        description: 'Please try again later.'
      })
    } finally {
      setIsAdding(false)
    }
  }

  const isDisabled = disabled || !variant || isAdding
  const price = variant?.pricing?.price?.gross.amount ? variant.pricing.price.gross.amount.toFixed(2) : '0.00'
  
  return (
    <Button
      onClick={handleAddToCart}
      disabled={isDisabled}
      size={size}
      className={cn(
        "bg-red-600 hover:bg-red-700 text-white font-medium transition-all duration-200",
        isAdded && "bg-green-600 hover:bg-green-700",
        className
      )}
    >
      {isAdding ? (
        <>
          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
          Adding...
        </>
      ) : isAdded ? (
        <>
          <CheckCircle className="h-4 w-4 mr-2" />
          Added!
        </>
      ) : (
        <>
          <ShoppingCart className="h-4 w-4 mr-2" />
          Add to Cart - ${price}
        </>
      )}
    </Button>
  )
}

// Hook to manage cart state
export function useCart() {
  const [cart, setCart] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)

  // Load cart from localStorage on mount
  useEffect(() => {
    try {
      const savedCart = localStorage.getItem('cart')
      if (savedCart) {
        setCart(JSON.parse(savedCart))
      }
    } catch (error) {
      console.error('Failed to load cart:', error)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Listen for cart updates
  useEffect(() => {
    const handleCartUpdate = (event: any) => {
      setCart(event.detail || [])
    }

    if (typeof window !== 'undefined') {
      window.addEventListener('cartUpdated', handleCartUpdate)
      return () => window.removeEventListener('cartUpdated', handleCartUpdate)
    }
  }, [])

  const addToCart = (item: any) => {
    const existingItemIndex = cart.findIndex(cartItem => cartItem.variantId === item.variantId)
    let newCart

    if (existingItemIndex >= 0) {
      newCart = [...cart]
      newCart[existingItemIndex].quantity += item.quantity
    } else {
      newCart = [...cart, item]
    }

    setCart(newCart)
    localStorage.setItem('cart', JSON.stringify(newCart))
    window.dispatchEvent(new CustomEvent('cartUpdated', { detail: newCart }))
  }

  const removeFromCart = (variantId: string) => {
    const newCart = cart.filter(item => item.variantId !== variantId)
    setCart(newCart)
    localStorage.setItem('cart', JSON.stringify(newCart))
    window.dispatchEvent(new CustomEvent('cartUpdated', { detail: newCart }))
  }

  const updateQuantity = (variantId: string, quantity: number) => {
    if (quantity <= 0) {
      removeFromCart(variantId)
      return
    }

    const newCart = cart.map(item => 
      item.variantId === variantId ? { ...item, quantity } : item
    )
    setCart(newCart)
    localStorage.setItem('cart', JSON.stringify(newCart))
    window.dispatchEvent(new CustomEvent('cartUpdated', { detail: newCart }))
  }

  const clearCart = () => {
    setCart([])
    localStorage.removeItem('cart')
    window.dispatchEvent(new CustomEvent('cartUpdated', { detail: [] }))
  }

  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0)
  const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  return {
    cart,
    isLoading,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    totalItems,
    totalPrice
  }
}