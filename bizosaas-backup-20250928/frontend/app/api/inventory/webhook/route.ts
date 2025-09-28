import { NextRequest, NextResponse } from 'next/server'
import { inventorySync } from '@/lib/inventory-sync'
import { headers } from 'next/headers'
import crypto from 'crypto'

// Webhook handler for Amazon SP-API notifications
export async function POST(request: NextRequest) {
  try {
    const body = await request.text()
    const signature = headers().get('x-amz-sns-message-signature')
    
    // Verify webhook signature (simplified - should use proper SNS verification)
    if (!verifyAmazonWebhook(body, signature)) {
      return NextResponse.json(
        { error: 'Invalid signature' },
        { status: 401 }
      )
    }

    const payload = JSON.parse(body)
    
    // Handle different notification types
    switch (payload.NotificationType || payload.eventType) {
      case 'LISTINGS_ITEM_ISSUES_CHANGE':
        await handleListingIssuesChange(payload)
        break
        
      case 'LISTINGS_ITEM_MFN_QUANTITY_CHANGE':
        await handleQuantityChange(payload)
        break
        
      case 'PRICE_CHANGE':
        await handlePriceChange(payload)
        break
        
      case 'INVENTORY_HEALTH':
        await handleInventoryHealth(payload)
        break
        
      default:
        console.log('Unknown notification type:', payload.NotificationType)
    }

    return NextResponse.json({ success: true })

  } catch (error) {
    console.error('Webhook processing error:', error)
    return NextResponse.json(
      { error: 'Failed to process webhook' },
      { status: 500 }
    )
  }
}

// Verify Amazon webhook signature (simplified)
function verifyAmazonWebhook(body: string, signature: string | null): boolean {
  if (!signature) return false
  
  // In production, implement proper AWS SNS signature verification
  // This is a simplified check for demo purposes
  const expectedSignature = crypto
    .createHmac('sha256', process.env.AMAZON_WEBHOOK_SECRET || 'default-secret')
    .update(body)
    .digest('hex')
  
  return signature === expectedSignature
}

// Handle listing issues changes
async function handleListingIssuesChange(payload: any) {
  try {
    const { SellerId, MarketplaceId, Asin, Issues } = payload.Payload
    
    // Create alert for listing issues
    inventorySync.handleWebhook('listing_issues', {
      asin: Asin,
      sellerId: SellerId,
      marketplaceId: MarketplaceId,
      issues: Issues,
      timestamp: new Date().toISOString()
    })
    
    // Trigger sync for this specific product
    await inventorySync.syncProduct(Asin)
    
  } catch (error) {
    console.error('Error handling listing issues change:', error)
  }
}

// Handle quantity changes
async function handleQuantityChange(payload: any) {
  try {
    const { SellerId, MarketplaceId, Asin, MfnQuantity } = payload.Payload
    
    // Create alert if quantity is low
    if (MfnQuantity !== undefined && MfnQuantity <= 10) {
      inventorySync.handleWebhook('low_stock', {
        asin: Asin,
        sellerId: SellerId,
        marketplaceId: MarketplaceId,
        quantity: MfnQuantity,
        timestamp: new Date().toISOString(),
        alertType: MfnQuantity === 0 ? 'out_of_stock' : 'low_stock'
      })
    }
    
    // Trigger sync for this specific product
    await inventorySync.syncProduct(Asin)
    
  } catch (error) {
    console.error('Error handling quantity change:', error)
  }
}

// Handle price changes
async function handlePriceChange(payload: any) {
  try {
    const { SellerId, MarketplaceId, Asin, NewPrice, OldPrice } = payload.Payload
    
    // Calculate price variance
    const variance = OldPrice > 0 ? Math.abs(NewPrice - OldPrice) / OldPrice * 100 : 0
    
    // Create alert for significant price changes
    if (variance > 10) { // 10% variance threshold
      inventorySync.handleWebhook('price_variance', {
        asin: Asin,
        sellerId: SellerId,
        marketplaceId: MarketplaceId,
        oldPrice: OldPrice,
        newPrice: NewPrice,
        variance: variance,
        timestamp: new Date().toISOString()
      })
    }
    
    // Trigger sync for this specific product
    await inventorySync.syncProduct(Asin)
    
  } catch (error) {
    console.error('Error handling price change:', error)
  }
}

// Handle inventory health notifications
async function handleInventoryHealth(payload: any) {
  try {
    const { SellerId, MarketplaceId, InventoryItems } = payload.Payload
    
    for (const item of InventoryItems || []) {
      const { Asin, AvailableQuantity, ReservedQuantity, InboundQuantity } = item
      
      // Create alerts for inventory issues
      if (AvailableQuantity <= 5) {
        inventorySync.handleWebhook('inventory_health', {
          asin: Asin,
          sellerId: SellerId,
          marketplaceId: MarketplaceId,
          availableQuantity: AvailableQuantity,
          reservedQuantity: ReservedQuantity,
          inboundQuantity: InboundQuantity,
          timestamp: new Date().toISOString(),
          alertType: AvailableQuantity === 0 ? 'out_of_stock' : 'low_stock'
        })
      }
    }
    
  } catch (error) {
    console.error('Error handling inventory health:', error)
  }
}

// GET endpoint for webhook verification (required by some webhook providers)
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const challenge = searchParams.get('hub.challenge')
  const verifyToken = searchParams.get('hub.verify_token')
  
  // Verify token matches expected value
  if (verifyToken === process.env.AMAZON_WEBHOOK_VERIFY_TOKEN) {
    return new NextResponse(challenge)
  }
  
  return NextResponse.json({ error: 'Invalid verify token' }, { status: 403 })
}