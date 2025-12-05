import { NextRequest, NextResponse } from 'next/server'

const SALEOR_API_URL = process.env.NEXT_PUBLIC_SALEOR_API_URL || 'http://localhost:8020/graphql/'

interface CartItem {
  id: string
  productId: string
  variantId: string
  quantity: number
  price: number
  name: string
  image: string
  attributes?: Record<string, string>
}

interface Cart {
  id: string
  items: CartItem[]
  totalQuantity: number
  subtotal: number
  tax: number
  shipping: number
  total: number
  currency: string
  discounts?: Array<{
    code: string
    amount: number
  }>
}

const CREATE_CHECKOUT_MUTATION = `
  mutation CreateCheckout($input: CheckoutCreateInput!) {
    checkoutCreate(input: $input) {
      checkout {
        id
        totalPrice {
          gross {
            amount
            currency
          }
        }
        subtotalPrice {
          gross {
            amount
            currency
          }
        }
        lines {
          id
          quantity
          variant {
            id
            name
            pricing {
              price {
                gross {
                  amount
                  currency
                }
              }
            }
            product {
              name
              thumbnail {
                url
              }
            }
          }
        }
      }
      errors {
        field
        message
      }
    }
  }
`

const ADD_TO_CHECKOUT_MUTATION = `
  mutation CheckoutLinesAdd($checkoutId: ID!, $lines: [CheckoutLineInput!]!) {
    checkoutLinesAdd(checkoutId: $checkoutId, lines: $lines) {
      checkout {
        id
        totalPrice {
          gross {
            amount
            currency
          }
        }
        subtotalPrice {
          gross {
            amount
            currency
          }
        }
        lines {
          id
          quantity
          variant {
            id
            name
            pricing {
              price {
                gross {
                  amount
                  currency
                }
              }
            }
            product {
              name
              thumbnail {
                url
              }
            }
          }
        }
      }
      errors {
        field
        message
      }
    }
  }
`

const UPDATE_CHECKOUT_LINE_MUTATION = `
  mutation CheckoutLinesUpdate($checkoutId: ID!, $lines: [CheckoutLineUpdateInput!]!) {
    checkoutLinesUpdate(checkoutId: $checkoutId, lines: $lines) {
      checkout {
        id
        totalPrice {
          gross {
            amount
            currency
          }
        }
        subtotalPrice {
          gross {
            amount
            currency
          }
        }
        lines {
          id
          quantity
          variant {
            id
            name
            pricing {
              price {
                gross {
                  amount
                  currency
                }
              }
            }
            product {
              name
              thumbnail {
                url
              }
            }
          }
        }
      }
      errors {
        field
        message
      }
    }
  }
`

const REMOVE_FROM_CHECKOUT_MUTATION = `
  mutation CheckoutLinesDelete($checkoutId: ID!, $lineIds: [ID!]!) {
    checkoutLinesDelete(checkoutId: $checkoutId, lineIds: $lineIds) {
      checkout {
        id
        totalPrice {
          gross {
            amount
            currency
          }
        }
        subtotalPrice {
          gross {
            amount
            currency
          }
        }
        lines {
          id
          quantity
          variant {
            id
            name
            pricing {
              price {
                gross {
                  amount
                  currency
                }
              }
            }
            product {
              name
              thumbnail {
                url
              }
            }
          }
        }
      }
      errors {
        field
        message
      }
    }
  }
`

const GET_CHECKOUT_QUERY = `
  query GetCheckout($id: ID!) {
    checkout(id: $id) {
      id
      totalPrice {
        gross {
          amount
          currency
        }
      }
      subtotalPrice {
        gross {
          amount
          currency
        }
      }
      lines {
        id
        quantity
        variant {
          id
          name
          pricing {
            price {
              gross {
                amount
                currency
              }
            }
          }
          product {
            name
            thumbnail {
              url
            }
          }
        }
      }
    }
  }
`

async function executeSaleorQuery(query: string, variables: any = {}) {
  try {
    const response = await fetch(SALEOR_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, variables }),
    })

    if (!response.ok) {
      throw new Error(`Saleor API error: ${response.status}`)
    }

    const data = await response.json()
    
    if (data.errors) {
      throw new Error(`GraphQL errors: ${JSON.stringify(data.errors)}`)
    }

    return data.data
  } catch (error) {
    console.error('Saleor API Error:', error)
    throw error
  }
}

function transformSaleorCheckout(saleorCheckout: any): Cart {
  const lines = saleorCheckout.lines || []
  
  const items: CartItem[] = lines.map((line: any) => ({
    id: line.id,
    productId: line.variant.product.id || line.variant.id,
    variantId: line.variant.id,
    quantity: line.quantity,
    price: line.variant.pricing?.price?.gross?.amount || 0,
    name: `${line.variant.product.name}${line.variant.name ? ` - ${line.variant.name}` : ''}`,
    image: line.variant.product.thumbnail?.url || '/placeholder-product.jpg',
  }))

  const subtotal = saleorCheckout.subtotalPrice?.gross?.amount || 0
  const total = saleorCheckout.totalPrice?.gross?.amount || 0
  const currency = saleorCheckout.totalPrice?.gross?.currency || 'USD'

  return {
    id: saleorCheckout.id,
    items,
    totalQuantity: items.reduce((sum, item) => sum + item.quantity, 0),
    subtotal,
    tax: 0, // Would be calculated by Saleor
    shipping: 0, // Would be calculated by Saleor
    total,
    currency,
  }
}

// In-memory cart storage (in production, use Redis or database)
const cartStorage = new Map<string, Cart>()

function generateCartId(): string {
  return Math.random().toString(36).substr(2, 9)
}

function getOrCreateLocalCart(cartId?: string): Cart {
  if (cartId && cartStorage.has(cartId)) {
    return cartStorage.get(cartId)!
  }

  const newCart: Cart = {
    id: generateCartId(),
    items: [],
    totalQuantity: 0,
    subtotal: 0,
    tax: 0,
    shipping: 0,
    total: 0,
    currency: 'USD',
  }

  cartStorage.set(newCart.id, newCart)
  return newCart
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const cartId = searchParams.get('cartId')

  try {
    if (cartId) {
      // Try to fetch from Saleor first
      try {
        const data = await executeSaleorQuery(GET_CHECKOUT_QUERY, { id: cartId })
        if (data.checkout) {
          const cart = transformSaleorCheckout(data.checkout)
          return NextResponse.json(cart)
        }
      } catch (saleorError) {
        console.log('Saleor not available, using local cart')
      }
    }

    // Fallback to local cart
    const cart = getOrCreateLocalCart(cartId)
    return NextResponse.json(cart)

  } catch (error) {
    console.error('Error fetching cart:', error)
    return NextResponse.json(
      { error: 'Failed to fetch cart' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { action, cartId, productId, variantId, quantity = 1 } = body

    if (action === 'add') {
      // Try Saleor first
      try {
        if (cartId) {
          // Add to existing checkout
          const data = await executeSaleorQuery(ADD_TO_CHECKOUT_MUTATION, {
            checkoutId: cartId,
            lines: [{ variantId, quantity }]
          })

          if (data.checkoutLinesAdd?.checkout) {
            const cart = transformSaleorCheckout(data.checkoutLinesAdd.checkout)
            return NextResponse.json(cart)
          }
        } else {
          // Create new checkout
          const data = await executeSaleorQuery(CREATE_CHECKOUT_MUTATION, {
            input: {
              lines: [{ variantId, quantity }]
            }
          })

          if (data.checkoutCreate?.checkout) {
            const cart = transformSaleorCheckout(data.checkoutCreate.checkout)
            return NextResponse.json(cart)
          }
        }
      } catch (saleorError) {
        console.log('Saleor not available, using local cart')
      }

      // Fallback to local cart
      const cart = getOrCreateLocalCart(cartId)
      const existingItem = cart.items.find(item => item.variantId === variantId)

      if (existingItem) {
        existingItem.quantity += quantity
      } else {
        // In production, you'd fetch product details from Saleor
        cart.items.push({
          id: `local-${Date.now()}`,
          productId: productId || variantId,
          variantId,
          quantity,
          price: 99.99, // Placeholder price
          name: 'Product Name', // Placeholder name
          image: '/placeholder-product.jpg',
        })
      }

      // Recalculate totals
      cart.totalQuantity = cart.items.reduce((sum, item) => sum + item.quantity, 0)
      cart.subtotal = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
      cart.total = cart.subtotal // Simplified for demo

      cartStorage.set(cart.id, cart)
      return NextResponse.json(cart)
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 })

  } catch (error) {
    console.error('Error managing cart:', error)
    return NextResponse.json(
      { error: 'Failed to manage cart' },
      { status: 500 }
    )
  }
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json()
    const { cartId, lineId, quantity } = body

    // Try Saleor first
    try {
      const data = await executeSaleorQuery(UPDATE_CHECKOUT_LINE_MUTATION, {
        checkoutId: cartId,
        lines: [{ id: lineId, quantity }]
      })

      if (data.checkoutLinesUpdate?.checkout) {
        const cart = transformSaleorCheckout(data.checkoutLinesUpdate.checkout)
        return NextResponse.json(cart)
      }
    } catch (saleorError) {
      console.log('Saleor not available, using local cart')
    }

    // Fallback to local cart
    const cart = getOrCreateLocalCart(cartId)
    const item = cart.items.find(item => item.id === lineId)

    if (item) {
      item.quantity = quantity
      if (quantity <= 0) {
        cart.items = cart.items.filter(item => item.id !== lineId)
      }

      // Recalculate totals
      cart.totalQuantity = cart.items.reduce((sum, item) => sum + item.quantity, 0)
      cart.subtotal = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
      cart.total = cart.subtotal

      cartStorage.set(cart.id, cart)
    }

    return NextResponse.json(cart)

  } catch (error) {
    console.error('Error updating cart:', error)
    return NextResponse.json(
      { error: 'Failed to update cart' },
      { status: 500 }
    )
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const body = await request.json()
    const { cartId, lineIds } = body

    // Try Saleor first
    try {
      const data = await executeSaleorQuery(REMOVE_FROM_CHECKOUT_MUTATION, {
        checkoutId: cartId,
        lineIds
      })

      if (data.checkoutLinesDelete?.checkout) {
        const cart = transformSaleorCheckout(data.checkoutLinesDelete.checkout)
        return NextResponse.json(cart)
      }
    } catch (saleorError) {
      console.log('Saleor not available, using local cart')
    }

    // Fallback to local cart
    const cart = getOrCreateLocalCart(cartId)
    cart.items = cart.items.filter(item => !lineIds.includes(item.id))

    // Recalculate totals
    cart.totalQuantity = cart.items.reduce((sum, item) => sum + item.quantity, 0)
    cart.subtotal = cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
    cart.total = cart.subtotal

    cartStorage.set(cart.id, cart)
    return NextResponse.json(cart)

  } catch (error) {
    console.error('Error removing from cart:', error)
    return NextResponse.json(
      { error: 'Failed to remove from cart' },
      { status: 500 }
    )
  }
}