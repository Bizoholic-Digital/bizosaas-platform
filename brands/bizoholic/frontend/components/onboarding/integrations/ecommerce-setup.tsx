'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  ShoppingCart, ExternalLink, CheckCircle, Zap, 
  Package, TrendingUp, Users, ArrowRight, RefreshCw, AlertTriangle
} from 'lucide-react'

interface EcommerceSetupProps {
  businessData: any
  onComplete: (data: any) => void
  onCancel: () => void
}

type EcommercePlatform = 'shopify' | 'woocommerce' | 'none'

export function EcommerceSetup({ businessData, onComplete, onCancel }: EcommerceSetupProps) {
  const [selectedPlatform, setSelectedPlatform] = useState<EcommercePlatform>('shopify')
  const [storeUrl, setStoreUrl] = useState('')
  const [isConnecting, setIsConnecting] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'success' | 'error'>('idle')

  const platforms = {
    shopify: {
      name: 'Shopify',
      description: 'Connect your Shopify store for product and order management',
      icon: '🛍️',
      setup_time: '5-10 minutes',
      features: [
        'Product catalog sync',
        'Order tracking',
        'Inventory management',
        'Customer segmentation',
        'Abandoned cart recovery',
        'Sales analytics'
      ]
    },
    woocommerce: {
      name: 'WooCommerce',
      description: 'Connect your WordPress WooCommerce store',
      icon: '🏪',
      setup_time: '10-15 minutes',
      features: [
        'Product sync',
        'Order management',
        'Customer data',
        'Sales reporting',
        'Email automation',
        'Conversion tracking'
      ]
    },
    none: {
      name: 'No E-commerce',
      description: 'Skip e-commerce integration for now',
      icon: '⏭️',
      setup_time: 'Skip',
      features: [
        'Service-based business focus',
        'Lead generation priority',
        'B2B marketing emphasis',
        'Can add e-commerce later'
      ]
    }
  }

  const handleConnect = async () => {
    if (selectedPlatform === 'none') {
      onComplete({
        platform: 'none',
        skipped: true,
        connectedAt: new Date().toISOString()
      })
      return
    }

    if (!storeUrl) {
      alert('Please enter your store URL')
      return
    }

    setIsConnecting(true)
    setConnectionStatus('connecting')

    try {
      // Simulate OAuth connection process
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      setConnectionStatus('success')
      
      // Auto-complete after successful connection
      setTimeout(() => {
        handleComplete()
      }, 1000)
      
    } catch (error) {
      setConnectionStatus('error')
    } finally {
      setIsConnecting(false)
    }
  }

  const handleComplete = () => {
    const setupData = {
      platform: selectedPlatform,
      storeUrl: selectedPlatform !== 'none' ? storeUrl : null,
      connectedAt: new Date().toISOString(),
      features: {
        product_sync: selectedPlatform !== 'none',
        order_tracking: selectedPlatform !== 'none',
        inventory_management: selectedPlatform !== 'none',
        customer_segmentation: selectedPlatform !== 'none',
        abandoned_cart: selectedPlatform !== 'none',
        sales_analytics: selectedPlatform !== 'none'
      },
      skipped: selectedPlatform === 'none'
    }
    
    onComplete(setupData)
  }

  const renderPlatformCard = (platform: EcommercePlatform) => {
    const config = platforms[platform]
    const isSelected = selectedPlatform === platform
    
    return (
      <Card 
        key={platform}
        className={`cursor-pointer transition-all ${
          isSelected ? 'ring-2 ring-blue-500 border-blue-200' : 'hover:shadow-md'
        }`}
        onClick={() => setSelectedPlatform(platform)}
      >
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{config.icon}</span>
              <div>
                <div>{config.name}</div>
                <div className="text-xs text-muted-foreground font-normal">
                  {config.setup_time}
                </div>
              </div>
            </div>
            {isSelected && <CheckCircle className="h-5 w-5 text-blue-600" />}
          </CardTitle>
          <CardDescription>{config.description}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-1">
            {config.features.slice(0, 3).map((feature) => (
              <div key={feature} className="flex items-center gap-2 text-sm text-muted-foreground">
                <CheckCircle className="h-3 w-3 text-green-500" />
                {feature}
              </div>
            ))}
            {config.features.length > 3 && (
              <div className="text-xs text-muted-foreground">
                +{config.features.length - 3} more features
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start gap-3">
        <ShoppingCart className="h-6 w-6 text-orange-600 mt-1" />
        <div>
          <h3 className="font-semibold text-lg">E-commerce Integration</h3>
          <p className="text-sm text-muted-foreground">
            Connect your online store for comprehensive sales and marketing automation
          </p>
        </div>
      </div>

      {/* Platform Selection */}
      <div className="space-y-4">
        <h4 className="font-medium">Choose your e-commerce platform:</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(platforms).map(([platform, config]) => 
            renderPlatformCard(platform as EcommercePlatform)
          )}
        </div>
      </div>

      {/* Store URL Input */}
      {selectedPlatform !== 'none' && (
        <div className="space-y-4">
          <h4 className="font-medium">Store Connection:</h4>
          
          <Alert className="border-blue-200 bg-blue-50">
            <Zap className="h-4 w-4 text-blue-600" />
            <AlertDescription className="text-blue-700">
              We'll connect to your {platforms[selectedPlatform].name} store using OAuth 2.0 
              for secure, authorized access to your store data.
            </AlertDescription>
          </Alert>

          <div className="space-y-3">
            <div>
              <Label htmlFor="store-url">
                {selectedPlatform === 'shopify' ? 'Shopify Store URL' : 'WooCommerce Store URL'}
              </Label>
              <Input
                id="store-url"
                placeholder={
                  selectedPlatform === 'shopify' 
                    ? 'your-store.myshopify.com' 
                    : 'yourstore.com'
                }
                value={storeUrl}
                onChange={(e) => setStoreUrl(e.target.value)}
              />
              <p className="text-xs text-muted-foreground mt-1">
                {selectedPlatform === 'shopify' 
                  ? 'Enter your Shopify store domain (without https://)'
                  : 'Enter your WordPress/WooCommerce site domain'
                }
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { icon: Package, title: 'Product Sync', desc: 'Real-time inventory updates' },
                { icon: TrendingUp, title: 'Sales Analytics', desc: 'Revenue & conversion tracking' },
                { icon: Users, title: 'Customer Data', desc: 'Segmentation & targeting' }
              ].map(({ icon: Icon, title, desc }) => (
                <div key={title} className="text-center p-3 rounded-lg bg-gray-50">
                  <Icon className="h-6 w-6 text-orange-600 mx-auto mb-2" />
                  <h5 className="font-semibold text-sm">{title}</h5>
                  <p className="text-xs text-muted-foreground">{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Connection Status */}
      {connectionStatus === 'connecting' && (
        <Alert className="border-blue-200 bg-blue-50">
          <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
          <AlertDescription className="text-blue-700">
            Connecting to your {platforms[selectedPlatform].name} store...
          </AlertDescription>
        </Alert>
      )}

      {connectionStatus === 'success' && (
        <Alert className="border-green-200 bg-green-50">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-700">
            <div className="space-y-2">
              <strong>Successfully connected to {platforms[selectedPlatform].name}!</strong>
              <div className="text-sm space-y-1">
                <div>✅ Store data access authorized</div>
                <div>✅ Product catalog sync initiated</div>
                <div>✅ Order tracking enabled</div>
                <div>✅ Customer segmentation ready</div>
              </div>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {connectionStatus === 'error' && (
        <Alert className="border-red-200 bg-red-50">
          <AlertTriangle className="h-4 w-4 text-red-600" />
          <AlertDescription className="text-red-700">
            Failed to connect to your store. Please check the URL and try again.
          </AlertDescription>
        </Alert>
      )}

      {/* Skip Option Note */}
      {selectedPlatform === 'none' && (
        <Alert>
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription>
            <strong>No problem!</strong> You can add e-commerce integration later from your dashboard. 
            We'll focus on lead generation and service-based marketing for now.
          </AlertDescription>
        </Alert>
      )}

      {/* What You'll Get */}
      {selectedPlatform !== 'none' && (
        <Card className="border-dashed">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">E-commerce Marketing Features</CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="grid grid-cols-2 gap-3 text-sm">
              {[
                'Abandoned cart recovery emails',
                'Product recommendation engine',
                'Customer lifetime value tracking',
                'Inventory-based campaign pausing',
                'Cross-sell & upsell automation',
                'Revenue attribution reporting',
                'Customer journey mapping',
                'Seasonal campaign optimization'
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  {feature}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex justify-between">
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        
        <div className="flex gap-2">
          {selectedPlatform !== 'none' && connectionStatus !== 'success' && (
            <Button
              onClick={handleConnect}
              disabled={isConnecting || !storeUrl}
            >
              {isConnecting ? (
                <>
                  <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                  Connecting...
                </>
              ) : (
                <>
                  Connect Store
                  <ExternalLink className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
          )}
          
          <Button
            onClick={handleComplete}
            disabled={selectedPlatform !== 'none' && connectionStatus !== 'success'}
            variant={selectedPlatform === 'none' ? 'default' : 'outline'}
          >
            {selectedPlatform === 'none' ? 'Skip for Now' : 'Complete Setup'}
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}