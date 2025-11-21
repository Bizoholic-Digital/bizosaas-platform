import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// POST /api/brain/saleor/cart/lines - Add item to cart
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/cart/lines`, {
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
    console.error('Error adding item to cart via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to add item to cart', details: error.message },
      { status: 500 }
    )
  }
}

// PUT /api/brain/saleor/cart/lines - Update cart line quantity
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/cart/lines`, {
      method: 'PUT',
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
    console.error('Error updating cart line via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to update cart line', details: error.message },
      { status: 500 }
    )
  }
}

// DELETE /api/brain/saleor/cart/lines - Remove item from cart
export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/saleor/cart/lines`, {
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
    console.error('Error removing item from cart via Brain API:', error)
    return NextResponse.json(
      { error: 'Failed to remove item from cart', details: error.message },
      { status: 500 }
    )
  }
}