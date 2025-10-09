import { NextRequest, NextResponse } from 'next/server'

interface ContactSubmission {
  firstName: string
  lastName: string
  email: string
  company: string
  phone: string
  message: string
  timestamp: string
  source: string
  utm_source: string
}

export async function POST(request: NextRequest) {
  try {
    const data: ContactSubmission = await request.json()
    
    // Validate required fields
    if (!data.firstName || !data.lastName || !data.email || !data.message) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Create lead data for CRM
    const leadData = {
      // Personal Information
      first_name: data.firstName,
      last_name: data.lastName,
      email: data.email,
      company: data.company || '',
      phone: data.phone || '',
      
      // Lead Details
      message: data.message,
      source: data.source,
      utm_source: data.utm_source,
      timestamp: data.timestamp,
      
      // Lead Scoring & Classification
      lead_score: calculateLeadScore(data),
      lead_status: 'new',
      lead_type: classifyLeadType(data.message),
      priority: calculatePriority(data),
      
      // AI Insights
      interests: extractInterests(data.message),
      business_size: estimateBusinessSize(data.company, data.message),
      urgency: detectUrgency(data.message),
      
      // Campaign Data
      services_interested: extractServicesOfInterest(data.message),
      budget_estimate: estimateBudget(data.message),
      timeline: extractTimeline(data.message)
    }

    // Store in multiple systems
    const results = await Promise.allSettled([
      // Store in CRM database
      storeLead(leadData),
      
      // Send to AI agents for analysis
      processWithAIAgents(leadData),
      
      // Send notification to sales team
      notifySalesTeam(leadData),
      
      // Add to email marketing if they consent
      addToEmailMarketing(leadData)
    ])

    // Check if core operations succeeded
    const crmResult = results[0]
    if (crmResult.status === 'rejected') {
      console.error('CRM storage failed:', crmResult.reason)
    }

    return NextResponse.json({
      success: true,
      message: 'Contact form submitted successfully',
      lead_id: generateLeadId(data),
      next_steps: generateNextSteps(leadData)
    })

  } catch (error) {
    console.error('Contact form submission error:', error)
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// Helper functions for AI-powered lead processing
function calculateLeadScore(data: ContactSubmission): number {
  let score = 0
  
  // Company name increases score
  if (data.company) score += 20
  
  // Phone number shows higher intent
  if (data.phone) score += 15
  
  // Message length and quality
  const messageWords = data.message.split(' ').length
  if (messageWords > 20) score += 10
  if (messageWords > 50) score += 20
  
  // Keywords in message that indicate high intent
  const highIntentKeywords = ['urgent', 'budget', 'timeline', 'looking for', 'need help', 'struggling', 'increase', 'grow']
  const messageText = data.message.toLowerCase()
  highIntentKeywords.forEach(keyword => {
    if (messageText.includes(keyword)) score += 10
  })
  
  return Math.min(score, 100)
}

function classifyLeadType(message: string): string {
  const text = message.toLowerCase()
  
  if (text.includes('seo') || text.includes('search engine')) return 'seo_inquiry'
  if (text.includes('ads') || text.includes('ppc') || text.includes('google ads')) return 'sem_inquiry'
  if (text.includes('social media') || text.includes('facebook') || text.includes('instagram')) return 'social_media_inquiry'
  if (text.includes('email') || text.includes('newsletter')) return 'email_marketing_inquiry'
  if (text.includes('content') || text.includes('blog') || text.includes('writing')) return 'content_marketing_inquiry'
  if (text.includes('platform') || text.includes('saas') || text.includes('automation')) return 'platform_inquiry'
  
  return 'general_inquiry'
}

function calculatePriority(data: ContactSubmission): 'high' | 'medium' | 'low' {
  const score = calculateLeadScore(data)
  const urgentKeywords = ['urgent', 'asap', 'immediately', 'deadline', 'crisis']
  const hasUrgentKeywords = urgentKeywords.some(keyword => 
    data.message.toLowerCase().includes(keyword)
  )
  
  if (score > 70 || hasUrgentKeywords) return 'high'
  if (score > 40) return 'medium'
  return 'low'
}

function extractInterests(message: string): string[] {
  const interests: string[] = []
  const text = message.toLowerCase()
  
  const interestMap = {
    'seo': ['seo', 'search engine optimization', 'organic traffic', 'rankings'],
    'sem': ['google ads', 'ppc', 'paid search', 'advertising'],
    'social_media': ['social media', 'facebook', 'instagram', 'twitter', 'linkedin'],
    'email_marketing': ['email', 'newsletter', 'email marketing', 'email campaigns'],
    'content_marketing': ['content', 'blog', 'articles', 'copywriting'],
    'automation': ['automation', 'ai', 'artificial intelligence', 'workflows'],
    'analytics': ['analytics', 'tracking', 'reporting', 'data']
  }
  
  Object.entries(interestMap).forEach(([interest, keywords]) => {
    if (keywords.some(keyword => text.includes(keyword))) {
      interests.push(interest)
    }
  })
  
  return interests
}

function estimateBusinessSize(company: string, message: string): 'startup' | 'small' | 'medium' | 'enterprise' {
  const text = `${company} ${message}`.toLowerCase()
  
  if (text.includes('startup') || text.includes('just started')) return 'startup'
  if (text.includes('small business') || text.includes('local')) return 'small'
  if (text.includes('enterprise') || text.includes('corporation') || text.includes('large')) return 'enterprise'
  
  return 'medium'
}

function detectUrgency(message: string): 'high' | 'medium' | 'low' {
  const urgentWords = ['urgent', 'asap', 'immediately', 'crisis', 'emergency', 'deadline']
  const mediumWords = ['soon', 'quickly', 'fast', 'timing']
  
  const text = message.toLowerCase()
  
  if (urgentWords.some(word => text.includes(word))) return 'high'
  if (mediumWords.some(word => text.includes(word))) return 'medium'
  
  return 'low'
}

function extractServicesOfInterest(message: string): string[] {
  return extractInterests(message) // Reuse the interests extraction
}

function estimateBudget(message: string): string {
  const text = message.toLowerCase()
  
  if (text.includes('$') || text.includes('budget')) {
    // Try to extract budget numbers
    const budgetMatch = text.match(/\$?(\d+[,\d]*)/g)
    if (budgetMatch) {
      const budget = parseInt(budgetMatch[0].replace(/[$,]/g, ''))
      if (budget < 1000) return 'under_1k'
      if (budget < 5000) return '1k_5k'
      if (budget < 10000) return '5k_10k'
      if (budget < 25000) return '10k_25k'
      return 'over_25k'
    }
  }
  
  return 'not_specified'
}

function extractTimeline(message: string): string {
  const text = message.toLowerCase()
  
  if (text.includes('immediately') || text.includes('asap')) return 'immediate'
  if (text.includes('week') || text.includes('days')) return 'within_week'
  if (text.includes('month')) return 'within_month'
  if (text.includes('quarter')) return 'within_quarter'
  
  return 'not_specified'
}

// Storage and processing functions
async function storeLead(leadData: any): Promise<void> {
  try {
    // This would connect to your CRM database
    // For now, we'll use a simple API call or database storage
    const response = await fetch(`${process.env.CRM_API_URL}/leads`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.CRM_API_KEY}`,
      },
      body: JSON.stringify(leadData),
    })
    
    if (!response.ok) {
      throw new Error('Failed to store lead in CRM')
    }
  } catch (error) {
    console.error('CRM storage error:', error)
    // Fallback: Store in local database or file system
    throw error
  }
}

async function processWithAIAgents(leadData: any): Promise<void> {
  try {
    // Send to AI agents for analysis and response generation
    const response = await fetch(`${process.env.AI_AGENTS_URL}/analyze-lead`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.AI_AGENTS_API_KEY}`,
      },
      body: JSON.stringify({
        lead: leadData,
        analysis_type: 'contact_form_submission',
        requested_actions: ['lead_scoring', 'response_generation', 'service_recommendations']
      }),
    })
    
    if (!response.ok) {
      console.warn('AI agents processing failed')
    }
  } catch (error) {
    console.error('AI agents error:', error)
  }
}

async function notifySalesTeam(leadData: any): Promise<void> {
  try {
    // Send Slack/Teams notification or email to sales team
    const message = `New ${leadData.priority} priority lead: ${leadData.first_name} ${leadData.last_name} from ${leadData.company}. Interested in: ${leadData.services_interested.join(', ')}`
    
    // This could be Slack webhook, email, or internal notification system
    if (process.env.SLACK_WEBHOOK_URL) {
      await fetch(process.env.SLACK_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message }),
      })
    }
  } catch (error) {
    console.error('Sales notification error:', error)
  }
}

async function addToEmailMarketing(leadData: any): Promise<void> {
  try {
    // Add to email marketing platform (like Mailchimp, ConvertKit, etc.)
    // This would be optional based on lead consent
    console.log('Adding to email marketing:', leadData.email)
  } catch (error) {
    console.error('Email marketing error:', error)
  }
}

function generateLeadId(data: ContactSubmission): string {
  const timestamp = new Date().getTime()
  const emailHash = data.email.split('@')[0]
  return `lead_${emailHash}_${timestamp}`
}

function generateNextSteps(leadData: any): string[] {
  const nextSteps = []
  
  if (leadData.priority === 'high') {
    nextSteps.push('Priority response within 2 hours')
  } else {
    nextSteps.push('Response within 24 hours')
  }
  
  if (leadData.services_interested.length > 0) {
    nextSteps.push(`Personalized ${leadData.services_interested[0]} consultation`)
  } else {
    nextSteps.push('General marketing strategy consultation')
  }
  
  nextSteps.push('AI-powered marketing audit')
  nextSteps.push('Custom proposal and pricing')
  
  return nextSteps
}