'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Heart, ShoppingBag } from 'lucide-react'
import NavigationHeader from '../../components/layout/NavigationHeader'
import { Button } from '../../components/ui/button'
import useCartStore from '../../lib/stores/cartStore'

export default function WishlistPage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState<any>(null)
  const { getTotalItems } = useCartStore()

  const handleAuthAction = () => {
    if (isAuthenticated) {
      setIsAuthenticated(false)
      setUser(null)
    } else {
      window.location.href = '/auth/login'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <NavigationHeader
        cartCount={getTotalItems()}
        isAuthenticated={isAuthenticated}
        user={user}
        onAuthAction={handleAuthAction}
      />
      
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <Heart className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Your wishlist is empty</h2>
          <p className="text-gray-600 mb-8">
            Save items you love to your wishlist and keep track of what you want to buy later.
          </p>
          <Button asChild size="lg">
            <Link href="/catalog">
              <ShoppingBag className="w-4 h-4 mr-2" />
              Browse Products
            </Link>
          </Button>
        </div>
      </div>
    </div>
  )
}