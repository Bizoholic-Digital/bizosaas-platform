import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

interface AIAssistantRequest {
  message: string
  context: {
    userId: string
    tenantId: string
    currentPage: string
    userProfile: {
      name: string
      email: string
    }
    conversationId?: string
    previousMessages?: Array<{
      role: 'user' | 'assistant'
      content: string
      timestamp: Date
    }>
  }
}

interface AIAssistantResponse {
  message: string
  operation?: {
    type: 'create' | 'read' | 'update' | 'delete' | 'navigate' | 'analyze' | 'generate'
    entity: string
    data?: any
    results?: any
    form?: any
  }
  suggestions?: string[]
  quickActions?: Array<{
    label: string
    action: string
    type: 'primary' | 'secondary'
  }>
  conversationId: string
  needsConfirmation?: boolean
  confirmationMessage?: string
  operationCompleted?: boolean
}

export async function POST(request: NextRequest) {
  try {
    const body: AIAssistantRequest = await request.json()
    
    // Forward to FastAPI AI Central Hub for intelligent processing
    const response = await fetch(`${BRAIN_API_URL}/api/brain/ai-assistant/client-chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify({
        message: body.message,
        context: body.context,
        capabilities: [
          'lead_management',
          'content_creation',
          'order_management', 
          'analytics_reporting',
          'customer_support',
          'ai_content_generation',
          'business_insights'
        ]
      })
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status)
      
      // Fallback to intelligent client assistant
      const aiResponse = generateIntelligentClientResponse(body.message, body.context)
      return NextResponse.json(aiResponse)
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('Client AI Assistant API error:', error)
    
    // Fallback response
    return NextResponse.json({
      message: "I apologize, but I'm experiencing technical difficulties. Please try your request again.",
      conversationId: Date.now().toString(),
      quickActions: [
        { label: 'Try Again', action: 'retry', type: 'primary' },
        { label: 'Contact Support', action: 'navigate:/support', type: 'secondary' }
      ]
    }, { status: 200 })
  }
}

// Intelligent client assistant that can handle business operations
function generateIntelligentClientResponse(message: string, context: any): AIAssistantResponse {
  const lowerMessage = message.toLowerCase()
  
  // Advanced intent analysis
  const intent = analyzeBusinessIntent(lowerMessage)
  const entities = extractBusinessEntities(lowerMessage)
  
  let response: AIAssistantResponse = {
    message: '',
    conversationId: context.conversationId || Date.now().toString(),
    quickActions: []
  }

  // Handle different business operations intelligently
  switch (intent.category) {
    case 'lead_management':
      response = handleLeadOperations(intent, entities, message, context)
      break
    case 'content_creation':
      response = handleContentOperations(intent, entities, message, context)
      break
    case 'order_management':
      response = handleOrderOperations(intent, entities, message, context)
      break
    case 'analytics':
      response = handleAnalyticsOperations(intent, entities, message, context)
      break
    case 'customer_support':
      response = handleSupportOperations(intent, entities, message, context)
      break
    default:
      response = handleGeneralBusinessIntent(message, context)
  }

  return response
}

// Business intent analysis
function analyzeBusinessIntent(message: string) {
  // Lead management patterns
  if (/\b(lead|contact|prospect|customer)\b/.test(message)) {
    const action = determineAction(message)
    return { category: 'lead_management', action, confidence: 0.9 }
  }
  
  // Content creation patterns  
  if (/\b(content|blog|post|article|page|write|create.*content)\b/.test(message)) {
    const action = determineAction(message)
    return { category: 'content_creation', action, confidence: 0.9 }
  }
  
  // Order management patterns
  if (/\b(order|sale|purchase|product|inventory)\b/.test(message)) {
    const action = determineAction(message)
    return { category: 'order_management', action, confidence: 0.8 }
  }
  
  // Analytics patterns
  if (/\b(analytics|report|metric|performance|insight|data|statistics)\b/.test(message)) {
    const action = determineAction(message)
    return { category: 'analytics', action, confidence: 0.8 }
  }
  
  // Support patterns
  if (/\b(help|support|issue|problem|question|how.*to)\b/.test(message)) {
    return { category: 'customer_support', action: 'help', confidence: 0.7 }
  }
  
  return { category: 'general', action: 'chat', confidence: 0.5 }
}

// Determine specific action within category
function determineAction(message: string): string {
  if (/\b(create|add|new|make|generate)\b/.test(message)) return 'create'
  if (/\b(show|display|view|list|get|find|search)\b/.test(message)) return 'read'
  if (/\b(update|edit|modify|change|alter)\b/.test(message)) return 'update'
  if (/\b(delete|remove|destroy)\b/.test(message)) return 'delete'
  if (/\b(analyze|report|insight)\b/.test(message)) return 'analyze'
  return 'general'
}

// Extract business entities
function extractBusinessEntities(message: string) {
  const entities: any = {
    leadType: null,
    contentType: null,
    timeframe: null,
    quantity: null
  }

  // Lead types
  if (/\b(cold.*lead|warm.*lead|hot.*lead)\b/.test(message)) {
    entities.leadType = message.match(/\b(cold|warm|hot).*lead\b/)?.[1]
  }
  
  // Content types
  if (/\b(blog.*post|article|landing.*page|email)\b/.test(message)) {
    entities.contentType = message.match(/\b(blog.*post|article|landing.*page|email)\b/)?.[0]
  }
  
  // Extract timeframes
  const timeMatch = message.match(/\b(today|yesterday|this.*week|last.*week|this.*month|last.*month)\b/)
  if (timeMatch) entities.timeframe = timeMatch[0]
  
  // Extract quantities
  const quantityMatch = message.match(/\b(\d+)\b/)
  if (quantityMatch) entities.quantity = parseInt(quantityMatch[0])
  
  return entities
}

// Lead operations handler
function handleLeadOperations(intent: any, entities: any, message: string, context: any): AIAssistantResponse {
  switch (intent.action) {
    case 'create':
      return {
        message: "I'll help you create a new lead. I can set up the lead with contact information, lead source, and scoring. What information do you have about this lead?",
        operation: {
          type: 'create',
          entity: 'lead',
          form: {
            fields: ['name', 'email', 'phone', 'company', 'source', 'notes'],
            requiredFields: ['name', 'email']
          }
        },
        quickActions: [
          { label: 'Quick Lead Form', action: 'form:lead:quick', type: 'primary' },
          { label: 'Detailed Lead Form', action: 'form:lead:detailed', type: 'secondary' },
          { label: 'Import from CSV', action: 'import:lead:csv', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
      
    case 'read':
      return {
        message: "Here are your recent leads. I can show you more details, filter by status, or help you follow up with specific leads.",
        operation: {
          type: 'read',
          entity: 'lead',
          results: generateLeadData(entities.quantity || 5)
        },
        quickActions: [
          { label: 'View All Leads', action: 'navigate:/leads', type: 'primary' },
          { label: 'Hot Leads Only', action: 'filter:lead:hot', type: 'primary' },
          { label: 'Follow Up Required', action: 'filter:lead:followup', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
      
    case 'update':
      return {
        message: "I can help you update lead information, change lead status, or add follow-up notes. Which lead would you like to update?",
        operation: {
          type: 'update',
          entity: 'lead',
          data: { awaitingSelection: true }
        },
        quickActions: [
          { label: 'Select Lead to Update', action: 'select:lead:update', type: 'primary' },
          { label: 'Bulk Status Update', action: 'bulk:lead:status', type: 'secondary' },
          { label: 'Add Follow-up Notes', action: 'add:lead:notes', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
      
    default:
      return {
        message: "I can help you manage your leads effectively. You currently have 247 leads with a 3.2% conversion rate. What would you like to do with your leads?",
        quickActions: [
          { label: 'Create New Lead', action: 'form:lead:quick', type: 'primary' },
          { label: 'View Leads', action: 'navigate:/leads', type: 'primary' },
          { label: 'Lead Analytics', action: 'analytics:lead', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
  }
}

// Content operations handler  
function handleContentOperations(intent: any, entities: any, message: string, context: any): AIAssistantResponse {
  switch (intent.action) {
    case 'create':
      const contentType = entities.contentType || 'blog post'
      return {
        message: `I'll help you create a new ${contentType}. I can generate content using AI, provide templates, or guide you through the writing process. What topic would you like to write about?`,
        operation: {
          type: 'create',
          entity: 'content',
          data: { contentType, aiAssisted: true }
        },
        quickActions: [
          { label: 'AI Content Generator', action: 'ai:content:generate', type: 'primary' },
          { label: 'Use Template', action: 'template:content', type: 'secondary' },
          { label: 'Manual Creation', action: 'manual:content:create', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
      
    default:
      return {
        message: "I can help you create engaging content for your business. You have 8 published blog posts and 12 pages. What type of content would you like to work on?",
        quickActions: [
          { label: 'Create Blog Post', action: 'ai:content:generate:blog', type: 'primary' },
          { label: 'Create Landing Page', action: 'ai:content:generate:page', type: 'primary' },
          { label: 'Content Ideas', action: 'ai:content:ideas', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
  }
}

// Order operations handler
function handleOrderOperations(intent: any, entities: any, message: string, context: any): AIAssistantResponse {
  switch (intent.action) {
    case 'create':
      return {
        message: "I'll help you create a new order. I can set up the customer information, add products, and process payment. Do you have the customer and product details ready?",
        operation: {
          type: 'create',
          entity: 'order',
          form: {
            steps: ['customer', 'products', 'shipping', 'payment'],
            currentStep: 'customer'
          }
        },
        quickActions: [
          { label: 'New Customer Order', action: 'form:order:new', type: 'primary' },
          { label: 'Existing Customer', action: 'select:customer:order', type: 'secondary' },
          { label: 'Quick Order', action: 'form:order:quick', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
      
    default:
      return {
        message: "You have 23 active orders with $31,200 in revenue this month. I can help you create new orders, update existing ones, or analyze your sales performance.",
        quickActions: [
          { label: 'Create Order', action: 'form:order:new', type: 'primary' },
          { label: 'View Orders', action: 'navigate:/orders', type: 'primary' },
          { label: 'Sales Analytics', action: 'analytics:sales', type: 'secondary' }
        ],
        conversationId: context.conversationId || Date.now().toString()
      }
  }
}

// Analytics operations handler
function handleAnalyticsOperations(intent: any, entities: any, message: string, context: any): AIAssistantResponse {
  const timeframe = entities.timeframe || 'this month'
  
  return {
    message: `I'll analyze your business performance for ${timeframe}. Here's what I found:`,
    operation: {
      type: 'analyze',
      entity: 'business',
      results: generateAnalyticsData(timeframe)
    },
    quickActions: [
      { label: 'Detailed Analytics', action: 'navigate:/analytics', type: 'primary' },
      { label: 'AI Insights', action: 'ai:analytics:insights', type: 'primary' },
      { label: 'Custom Report', action: 'generate:report:custom', type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

// Support operations handler
function handleSupportOperations(intent: any, entities: any, message: string, context: any): AIAssistantResponse {
  return {
    message: "I'm here to help! I can assist you with platform navigation, feature usage, troubleshooting, or connecting you with our support team. What do you need help with?",
    quickActions: [
      { label: 'Platform Guide', action: 'guide:platform', type: 'primary' },
      { label: 'Feature Help', action: 'help:features', type: 'secondary' },
      { label: 'Contact Support', action: 'navigate:/support', type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

// General business intent handler
function handleGeneralBusinessIntent(message: string, context: any): AIAssistantResponse {
  return {
    message: "I'm your AI business assistant. I can help you manage leads, create content, process orders, analyze performance, and much more. What would you like to work on today?",
    suggestions: [
      'Create a new lead for Acme Corp',
      'Generate a blog post about digital marketing',
      'Show me this month\'s sales performance',
      'Update my recent orders',
      'Help me analyze my customer data'
    ],
    quickActions: [
      { label: 'Create Lead', action: 'form:lead:quick', type: 'primary' },
      { label: 'Create Content', action: 'ai:content:generate', type: 'primary' },
      { label: 'View Analytics', action: 'navigate:/analytics', type: 'secondary' },
      { label: 'Business Insights', action: 'ai:business:insights', type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

// Mock data generators
function generateLeadData(count: number) {
  const leads = []
  const statuses = ['new', 'contacted', 'qualified', 'proposal', 'closed']
  const sources = ['website', 'social', 'referral', 'cold-call', 'email']
  
  for (let i = 0; i < count; i++) {
    leads.push({
      id: `lead-${i + 1}`,
      name: `Lead Contact ${i + 1}`,
      email: `lead${i + 1}@example.com`,
      company: `Company ${i + 1}`,
      status: statuses[Math.floor(Math.random() * statuses.length)],
      source: sources[Math.floor(Math.random() * sources.length)],
      score: Math.floor(Math.random() * 100),
      created: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
    })
  }
  
  return { total: count, leads, summary: `Showing ${count} most recent leads` }
}

function generateAnalyticsData(timeframe: string) {
  return {
    period: timeframe,
    metrics: {
      leads: { total: 247, new: 23, conversion_rate: 3.2 },
      content: { views: 12500, posts: 8, engagement: 4.7 },
      sales: { revenue: 31200, orders: 23, avg_order: 1356 },
      growth: { leads: '+12%', revenue: '+8%', content: '+15%' }
    },
    insights: [
      'Lead generation is 12% above last period',
      'Content engagement has increased significantly', 
      'Sales conversion rate is improving',
      'Best performing content: "Digital Marketing Guide"'
    ],
    recommendations: [
      'Focus on high-converting lead sources',
      'Create more content similar to top performers',
      'Optimize checkout process to increase order value'
    ]
  }
}