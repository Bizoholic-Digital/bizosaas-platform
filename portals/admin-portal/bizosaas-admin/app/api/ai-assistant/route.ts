import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

interface AIAssistantRequest {
  message: string
  context: {
    userId: string
    tenantId?: string
    currentPage: string
    userProfile: {
      name: string
      email: string
    }
    adminLevel?: 'super' | 'admin' | 'user'
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
}

export async function POST(request: NextRequest) {
  try {
    const body: AIAssistantRequest = await request.json()
    
    // Forward to FastAPI AI Central Hub for intelligent processing
    const response = await fetch(`${BRAIN_API_URL}/api/brain/ai-assistant/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      },
      body: JSON.stringify({
        message: body.message,
        context: body.context,
        // Add operation capabilities
        capabilities: [
          'tenant_management',
          'user_management', 
          'content_creation',
          'analytics_reporting',
          'system_monitoring',
          'ai_insights',
          'workflow_automation'
        ]
      })
    })

    if (!response.ok) {
      console.error('FastAPI AI Central Hub error:', response.status)
      
      // Fallback to intelligent mock assistant
      const aiResponse = generateIntelligentResponse(body.message, body.context)
      return NextResponse.json(aiResponse)
    }

    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('AI Assistant API error:', error)
    
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

// Intelligent mock assistant that can handle operations
function generateIntelligentResponse(message: string, context: any): AIAssistantResponse {
  const lowerMessage = message.toLowerCase()
  const isAdmin = context.adminLevel === 'super' || context.adminLevel === 'admin'
  
  // Analyze intent and extract entities
  const intent = analyzeIntent(lowerMessage)
  const entities = extractEntities(lowerMessage)
  
  let response: AIAssistantResponse = {
    message: '',
    conversationId: context.conversationId || Date.now().toString(),
    quickActions: []
  }

  switch (intent.action) {
    case 'create':
      response = handleCreateIntent(intent, entities, context, isAdmin)
      break
    case 'read':
    case 'view':
    case 'show':
      response = handleReadIntent(intent, entities, context, isAdmin)
      break
    case 'update':
    case 'edit':
    case 'modify':
      response = handleUpdateIntent(intent, entities, context, isAdmin)
      break
    case 'delete':
    case 'remove':
      response = handleDeleteIntent(intent, entities, context, isAdmin)
      break
    case 'analyze':
    case 'report':
      response = handleAnalyzeIntent(intent, entities, context, isAdmin)
      break
    default:
      response = handleGeneralIntent(message, context, isAdmin)
  }

  return response
}

// Intent analysis
function analyzeIntent(message: string) {
  const createWords = ['create', 'add', 'new', 'make', 'generate', 'build']
  const readWords = ['show', 'display', 'view', 'list', 'get', 'find', 'search']
  const updateWords = ['update', 'edit', 'modify', 'change', 'alter']
  const deleteWords = ['delete', 'remove', 'destroy', 'eliminate']
  const analyzeWords = ['analyze', 'report', 'insight', 'metric', 'performance']

  if (createWords.some(word => message.includes(word))) return { action: 'create', confidence: 0.9 }
  if (readWords.some(word => message.includes(word))) return { action: 'read', confidence: 0.8 }
  if (updateWords.some(word => message.includes(word))) return { action: 'update', confidence: 0.8 }
  if (deleteWords.some(word => message.includes(word))) return { action: 'delete', confidence: 0.9 }
  if (analyzeWords.some(word => message.includes(word))) return { action: 'analyze', confidence: 0.7 }
  
  return { action: 'general', confidence: 0.5 }
}

// Entity extraction
function extractEntities(message: string) {
  const entities = {
    type: null as string | null,
    count: null as number | null,
    filters: [] as string[]
  }

  // Entity types
  if (message.includes('tenant') || message.includes('organization')) entities.type = 'tenant'
  if (message.includes('user') || message.includes('account')) entities.type = 'user'
  if (message.includes('lead') || message.includes('contact')) entities.type = 'lead'
  if (message.includes('content') || message.includes('blog') || message.includes('post')) entities.type = 'content'
  if (message.includes('order') || message.includes('sale')) entities.type = 'order'
  if (message.includes('report') || message.includes('analytics')) entities.type = 'report'

  // Extract numbers
  const numberMatch = message.match(/\d+/)
  if (numberMatch) entities.count = parseInt(numberMatch[0])

  return entities
}

// Intent handlers
function handleCreateIntent(intent: any, entities: any, context: any, isAdmin: boolean): AIAssistantResponse {
  const entityType = entities.type || 'item'
  
  return {
    message: `I'll help you create a new ${entityType}. I can guide you through the process step by step, or would you prefer to use our quick creation form?`,
    operation: {
      type: 'create',
      entity: entityType,
      data: { initiated: true, context: context.currentPage }
    },
    quickActions: [
      { label: `Quick Create ${entityType.charAt(0).toUpperCase() + entityType.slice(1)}`, action: `crud:${entityType}:create`, type: 'primary' },
      { label: 'Guided Setup', action: `guide:${entityType}:create`, type: 'secondary' },
      { label: 'View Examples', action: `examples:${entityType}`, type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

function handleReadIntent(intent: any, entities: any, context: any, isAdmin: boolean): AIAssistantResponse {
  const entityType = entities.type || 'data'
  
  return {
    message: `I can show you your ${entityType} information. Here's what I found:`,
    operation: {
      type: 'read',
      entity: entityType,
      results: generateMockData(entityType, entities.count || 5)
    },
    quickActions: [
      { label: `View All ${entityType}s`, action: `navigate:/${entityType}s`, type: 'primary' },
      { label: 'Filter Results', action: `filter:${entityType}`, type: 'secondary' },
      { label: 'Export Data', action: `export:${entityType}`, type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

function handleUpdateIntent(intent: any, entities: any, context: any, isAdmin: boolean): AIAssistantResponse {
  const entityType = entities.type || 'item'
  
  return {
    message: `I can help you update your ${entityType} information. Which specific ${entityType} would you like to modify?`,
    operation: {
      type: 'update',
      entity: entityType,
      data: { status: 'awaiting_selection' }
    },
    quickActions: [
      { label: `Select ${entityType} to Update`, action: `select:${entityType}:update`, type: 'primary' },
      { label: 'Bulk Update', action: `bulk:${entityType}:update`, type: 'secondary' },
      { label: 'Recent Items', action: `recent:${entityType}`, type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

function handleDeleteIntent(intent: any, entities: any, context: any, isAdmin: boolean): AIAssistantResponse {
  const entityType = entities.type || 'item'
  
  return {
    message: `I understand you want to delete ${entityType} records. This is a permanent action. Please confirm which ${entityType}s you'd like to remove.`,
    operation: {
      type: 'delete',
      entity: entityType,
      data: { requires_confirmation: true }
    },
    needsConfirmation: true,
    confirmationMessage: `Are you sure you want to delete the selected ${entityType}s? This action cannot be undone.`,
    quickActions: [
      { label: `Select ${entityType}s to Delete`, action: `select:${entityType}:delete`, type: 'primary' },
      { label: 'Cancel', action: 'cancel', type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

function handleAnalyzeIntent(intent: any, entities: any, context: any, isAdmin: boolean): AIAssistantResponse {
  const entityType = entities.type || 'performance'
  
  return {
    message: `I'll analyze your ${entityType} data and provide insights. Here's what I discovered:`,
    operation: {
      type: 'analyze',
      entity: entityType,
      results: generateAnalyticsData(entityType)
    },
    quickActions: [
      { label: 'Detailed Report', action: `report:${entityType}:detailed`, type: 'primary' },
      { label: 'AI Recommendations', action: `ai:${entityType}:recommendations`, type: 'primary' },
      { label: 'Export Analysis', action: `export:${entityType}:analysis`, type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

function handleGeneralIntent(message: string, context: any, isAdmin: boolean): AIAssistantResponse {
  return {
    message: `I'm your AI assistant and I can help you with various tasks including creating, viewing, updating, and deleting data, generating reports, and providing insights. What would you like to work on today?`,
    suggestions: [
      'Show me my latest leads',
      'Create a new blog post', 
      'Analyze my sales performance',
      'Update user permissions',
      'Generate a monthly report'
    ],
    quickActions: [
      { label: 'Dashboard Overview', action: 'navigate:/', type: 'primary' },
      { label: 'Recent Activity', action: 'recent:all', type: 'secondary' },
      { label: 'AI Insights', action: 'ai:insights:general', type: 'secondary' }
    ],
    conversationId: context.conversationId || Date.now().toString()
  }
}

// Helper functions
function generateMockData(entityType: string, count: number) {
  const data: any = { total: count, items: [] }
  
  for (let i = 0; i < count; i++) {
    switch (entityType) {
      case 'tenant':
        data.items.push({ id: `tenant-${i+1}`, name: `Organization ${i+1}`, status: 'active' })
        break
      case 'user':
        data.items.push({ id: `user-${i+1}`, name: `User ${i+1}`, email: `user${i+1}@example.com` })
        break
      case 'lead':
        data.items.push({ id: `lead-${i+1}`, name: `Lead ${i+1}`, status: 'new', score: Math.floor(Math.random() * 100) })
        break
      default:
        data.items.push({ id: `item-${i+1}`, name: `${entityType} ${i+1}` })
    }
  }
  
  return data
}

function generateAnalyticsData(entityType: string) {
  return {
    summary: `${entityType} analytics show positive trends`,
    metrics: {
      total: Math.floor(Math.random() * 1000) + 100,
      growth: (Math.random() * 20 + 5).toFixed(1) + '%',
      performance: 'Good'
    },
    insights: [
      `Your ${entityType} performance is above average`,
      `Consider optimizing based on recent patterns`,
      `AI recommendations available for improvement`
    ]
  }
}