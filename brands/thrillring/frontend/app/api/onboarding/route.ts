import { NextRequest, NextResponse } from 'next/server'

interface OnboardingData {
  // Company Info
  companyName: string
  industry: string
  companySize: string
  website: string
  description: string
  
  // Marketing Goals
  primaryGoals: string[]
  monthlyBudget: string
  targetAudience: string
  currentChallenges: string[]
  
  // Integrations
  selectedIntegrations: string[]
  
  // Team
  teamMembers: Array<{
    email: string
    role: string
  }>
}

interface WorkflowRequest {
  workflow_type: string
  tenant_id: string
  user_id: string
  input_data: Record<string, any>
}

async function startTemporalWorkflow(data: OnboardingData, userId: string, tenantId: string) {
  try {
    // Connect to Temporal service (running on port 8000 via AI agents)
    const temporalResponse = await fetch('http://localhost:8000/api/workflows/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        workflow_type: 'ai_customer_onboarding',
        tenant_id: tenantId,
        user_id: userId,
        input_data: {
          onboarding_data: data,
          automation_steps: [
            'setup_tenant_infrastructure',
            'configure_selected_integrations',
            'create_initial_campaigns',
            'setup_ai_agents',
            'generate_onboarding_report'
          ],
          priority: 'high'
        }
      } as WorkflowRequest)
    })

    if (!temporalResponse.ok) {
      throw new Error(`Temporal workflow failed: ${temporalResponse.statusText}`)
    }

    return await temporalResponse.json()
  } catch (error) {
    console.error('Temporal workflow error:', error)
    // Fallback to direct processing if Temporal is unavailable
    return {
      workflow_id: `fallback_${Date.now()}`,
      status: 'fallback_mode',
      message: 'Onboarding processed without workflow automation'
    }
  }
}

export async function POST(req: NextRequest) {
  try {
    const data: OnboardingData = await req.json()
    
    // Validate required fields
    if (!data.companyName || !data.industry) {
      return NextResponse.json(
        { error: 'Company name and industry are required' },
        { status: 400 }
      )
    }

    // Get user/tenant info from headers or auth context
    const userId = req.headers.get('x-user-id') || 'demo-user'
    const tenantId = req.headers.get('x-tenant-id') || 'demo-tenant'

    console.log('Starting onboarding workflow for:', {
      company: data.companyName,
      industry: data.industry,
      userId,
      tenantId
    })

    // Start Temporal workflow for comprehensive onboarding automation
    const workflowResult = await startTemporalWorkflow(data, userId, tenantId)

    // Create tenant configuration
    const tenantConfig = {
      tenant_id: tenantId,
      company_info: {
        name: data.companyName,
        industry: data.industry,
        size: data.companySize,
        website: data.website,
        description: data.description
      },
      marketing_config: {
        goals: data.primaryGoals,
        budget: data.monthlyBudget,
        target_audience: data.targetAudience,
        challenges: data.currentChallenges
      },
      integrations: data.selectedIntegrations,
      team_members: data.teamMembers,
      onboarding_workflow: workflowResult,
      created_at: new Date().toISOString()
    }

    // Store configuration (in production, this would go to database)
    console.log('Tenant configuration created:', tenantConfig)

    // Trigger AI agent initialization workflows
    const agentWorkflows = []
    
    if (data.primaryGoals.includes('Generate more leads')) {
      agentWorkflows.push('lead_generation_setup')
    }
    
    if (data.primaryGoals.includes('Improve conversion rates')) {
      agentWorkflows.push('conversion_optimization_setup')
    }
    
    if (data.selectedIntegrations.includes('google-ads')) {
      agentWorkflows.push('google_ads_campaign_setup')
    }
    
    if (data.selectedIntegrations.includes('meta-ads')) {
      agentWorkflows.push('meta_ads_campaign_setup')
    }

    // Start parallel AI agent workflows (logic-first approach)
    const agentPromises = agentWorkflows.map(async (workflowType) => {
      try {
        const agentResponse = await fetch('http://localhost:8000/api/workflows/start', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            workflow_type: workflowType,
            tenant_id: tenantId,
            user_id: userId,
            input_data: {
              company_data: tenantConfig.company_info,
              marketing_data: tenantConfig.marketing_config
            }
          } as WorkflowRequest)
        })
        
        if (agentResponse.ok) {
          return await agentResponse.json()
        }
        return null
      } catch (error) {
        console.error(`Failed to start ${workflowType}:`, error)
        return null
      }
    })

    const agentResults = await Promise.all(agentPromises)

    return NextResponse.json({
      success: true,
      tenant_id: tenantId,
      workflow_id: workflowResult.workflow_id,
      agent_workflows: agentResults.filter(Boolean),
      message: 'Onboarding completed successfully',
      next_steps: [
        'Review your dashboard',
        'Complete integration setup',
        'Launch your first campaign'
      ]
    })

  } catch (error) {
    console.error('Onboarding API error:', error)
    return NextResponse.json(
      { error: 'Internal server error during onboarding' },
      { status: 500 }
    )
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url)
  const workflowId = searchParams.get('workflow_id')
  
  if (!workflowId) {
    return NextResponse.json(
      { error: 'workflow_id parameter required' },
      { status: 400 }
    )
  }

  try {
    // Get workflow status from Temporal
    const statusResponse = await fetch(`http://localhost:8000/api/workflows/status/${workflowId}`)
    
    if (!statusResponse.ok) {
      throw new Error('Failed to get workflow status')
    }

    const statusData = await statusResponse.json()
    
    return NextResponse.json({
      workflow_id: workflowId,
      status: statusData.status,
      progress: statusData.progress || 0,
      completed_steps: statusData.completed_steps || [],
      current_step: statusData.current_step || 'initializing',
      estimated_completion: statusData.estimated_completion
    })

  } catch (error) {
    console.error('Workflow status error:', error)
    return NextResponse.json(
      { error: 'Failed to get workflow status' },
      { status: 500 }
    )
  }
}