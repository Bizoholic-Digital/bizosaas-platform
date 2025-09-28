import { NextRequest, NextResponse } from 'next/server'

const AI_AGENTS_URL = process.env.AI_AGENTS_URL || 'http://localhost:8000'
const CORELDOVE_CREWAI_URL = process.env.CORELDOVE_CREWAI_URL || 'http://localhost:8000'

interface RecommendationRequest {
  userId?: string
  category?: string
  priceRange?: {
    min: number
    max: number
  }
  previousPurchases?: string[]
  preferences?: {
    brands?: string[]
    features?: string[]
    budget?: number
  }
}

interface AIRecommendation {
  productId: string
  score: number
  reasoning: string
  category: string
  price: number
  confidence: number
  tags: string[]
}

async function fetchAIRecommendations(requestData: RecommendationRequest): Promise<AIRecommendation[]> {
  try {
    // Try CoreLDove CrewAI service first
    const crewAIResponse = await fetch(`${CORELDOVE_CREWAI_URL}/agents/product-recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_preferences: requestData.preferences || {},
        category: requestData.category || 'all',
        price_range: requestData.priceRange || { min: 0, max: 1000 },
        previous_purchases: requestData.previousPurchases || [],
        user_id: requestData.userId || 'anonymous'
      }),
      signal: AbortSignal.timeout(10000) // 10 second timeout
    })

    if (crewAIResponse.ok) {
      const data = await crewAIResponse.json()
      return data.recommendations || []
    }

    // Fallback to general AI agents service
    const aiResponse = await fetch(`${AI_AGENTS_URL}/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
      signal: AbortSignal.timeout(8000) // 8 second timeout
    })

    if (aiResponse.ok) {
      const data = await aiResponse.json()
      return data.recommendations || []
    }

    throw new Error('AI services unavailable')

  } catch (error) {
    console.error('Error fetching AI recommendations:', error)
    
    // Return smart fallback recommendations based on request
    return generateFallbackRecommendations(requestData)
  }
}

function generateFallbackRecommendations(request: RecommendationRequest): AIRecommendation[] {
  const { category, priceRange } = request
  
  const fallbackRecommendations: AIRecommendation[] = [
    {
      productId: 'rec-tech-1',
      score: 0.95,
      reasoning: 'High-quality wireless earbuds with excellent reviews and competitive pricing',
      category: 'tech',
      price: 89.99,
      confidence: 0.85,
      tags: ['bestseller', 'high-rating', 'value']
    },
    {
      productId: 'rec-sports-1',
      score: 0.92,
      reasoning: 'Versatile fitness equipment suitable for home workouts',
      category: 'sports',
      price: 24.99,
      confidence: 0.82,
      tags: ['fitness', 'home-workout', 'affordable']
    },
    {
      productId: 'rec-health-1',
      score: 0.88,
      reasoning: 'Smart health tracking device with app integration',
      category: 'health',
      price: 45.99,
      confidence: 0.78,
      tags: ['smart', 'health-tracking', 'app-connected']
    },
    {
      productId: 'rec-outdoor-1',
      score: 0.85,
      reasoning: 'Durable outdoor gear for camping and hiking enthusiasts',
      category: 'outdoor',
      price: 67.99,
      confidence: 0.75,
      tags: ['outdoor', 'durable', 'camping']
    }
  ]

  // Filter by category if specified
  let filtered = fallbackRecommendations
  if (category && category !== 'all') {
    filtered = fallbackRecommendations.filter(rec => rec.category === category)
  }

  // Filter by price range if specified
  if (priceRange) {
    filtered = filtered.filter(rec => 
      rec.price >= priceRange.min && rec.price <= priceRange.max
    )
  }

  // If no matches, return top recommendations
  if (filtered.length === 0) {
    filtered = fallbackRecommendations.slice(0, 3)
  }

  return filtered.sort((a, b) => b.score - a.score)
}

async function logRecommendationRequest(requestData: any, recommendations: AIRecommendation[]) {
  try {
    // In production, you would log this to your analytics service
    console.log('AI Recommendations Generated:', {
      timestamp: new Date().toISOString(),
      request: requestData,
      recommendationsCount: recommendations.length,
      avgConfidence: recommendations.reduce((sum, r) => sum + r.confidence, 0) / recommendations.length
    })
  } catch (error) {
    console.error('Error logging recommendation request:', error)
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json() as RecommendationRequest

    // Validate input
    if (body.priceRange && (body.priceRange.min < 0 || body.priceRange.max < body.priceRange.min)) {
      return NextResponse.json(
        { error: 'Invalid price range' },
        { status: 400 }
      )
    }

    // Fetch AI recommendations
    const recommendations = await fetchAIRecommendations(body)

    // Log the request for analytics
    await logRecommendationRequest(body, recommendations)

    return NextResponse.json({
      recommendations,
      generatedAt: new Date().toISOString(),
      requestId: Math.random().toString(36).substr(2, 9),
      source: 'coreldove-ai'
    })

  } catch (error) {
    console.error('Error in AI recommendations API:', error)
    
    return NextResponse.json(
      { 
        error: 'Failed to generate recommendations',
        fallback: true,
        recommendations: generateFallbackRecommendations({})
      },
      { status: 500 }
    )
  }
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  
  const category = searchParams.get('category') || undefined
  const userId = searchParams.get('userId') || undefined
  const minPrice = searchParams.get('minPrice')
  const maxPrice = searchParams.get('maxPrice')

  const requestData: RecommendationRequest = {
    userId,
    category,
    priceRange: (minPrice && maxPrice) ? {
      min: parseFloat(minPrice),
      max: parseFloat(maxPrice)
    } : undefined
  }

  try {
    const recommendations = await fetchAIRecommendations(requestData)

    return NextResponse.json({
      recommendations,
      generatedAt: new Date().toISOString(),
      requestId: Math.random().toString(36).substr(2, 9),
      source: 'coreldove-ai'
    })

  } catch (error) {
    console.error('Error in AI recommendations GET API:', error)
    
    return NextResponse.json(
      { 
        error: 'Failed to generate recommendations',
        fallback: true,
        recommendations: generateFallbackRecommendations(requestData)
      },
      { status: 500 }
    )
  }
}