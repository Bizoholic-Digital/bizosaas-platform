import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// POST /api/brain/saleor/discounts - Apply discount/voucher to checkout
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/discounts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Brain API responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error applying discount via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to apply discount', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE /api/brain/saleor/discounts - Remove discount/voucher from checkout
export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/discounts`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`Brain API responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error removing discount via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to remove discount', details: error.message },
      { status: 500 }
    )
  }
}

// GET /api/brain/saleor/discounts - Validate voucher code
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const voucherCode = searchParams.get('code')
    
    if (!voucherCode) {
      return NextResponse.json(
        { error: 'Voucher code is required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/discounts?code=${voucherCode}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`Brain API responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error validating voucher from Brain API:', error)
    
    // Return validation failure
    const fallbackData = {
      voucher: null,
      isValid: false,
      error: 'Voucher validation service unavailable',
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}