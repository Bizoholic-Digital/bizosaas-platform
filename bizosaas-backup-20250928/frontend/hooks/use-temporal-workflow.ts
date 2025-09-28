import { useState, useEffect } from 'react'

interface WorkflowStatus {
  workflow_id: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled'
  progress: number
  completed_steps: string[]
  current_step: string
  estimated_completion?: string
  error?: string
}

interface UseTemporalWorkflowProps {
  workflowId?: string
  pollInterval?: number
}

export function useTemporalWorkflow({ workflowId, pollInterval = 2000 }: UseTemporalWorkflowProps) {
  const [status, setStatus] = useState<WorkflowStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Start a new workflow
  const startWorkflow = async (workflowType: string, inputData: Record<string, any>) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/workflows', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // In production, these would come from auth context
          'x-user-id': 'demo-user',
          'x-tenant-id': 'demo-tenant'
        },
        body: JSON.stringify({
          workflow_type: workflowType,
          tenant_id: 'demo-tenant',
          user_id: 'demo-user',
          input_data: inputData
        })
      })

      if (!response.ok) {
        throw new Error(`Workflow start failed: ${response.statusText}`)
      }

      const result = await response.json()
      
      if (result.success) {
        setStatus({
          workflow_id: result.workflow_id,
          status: result.status || 'running',
          progress: 0,
          completed_steps: [],
          current_step: 'initializing'
        })
        return result
      } else {
        throw new Error(result.error || 'Failed to start workflow')
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Get workflow status
  const getWorkflowStatus = async (id: string) => {
    try {
      const response = await fetch(`/api/workflows?action=status&workflow_id=${id}`)
      
      if (!response.ok) {
        throw new Error(`Status check failed: ${response.statusText}`)
      }

      const statusData = await response.json()
      setStatus(statusData)
      return statusData
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get status'
      setError(errorMessage)
      return null
    }
  }

  // Cancel workflow
  const cancelWorkflow = async (id: string) => {
    setLoading(true)
    try {
      const response = await fetch(`/api/workflows?workflow_id=${id}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(`Cancel failed: ${response.statusText}`)
      }

      const result = await response.json()
      
      if (result.success) {
        setStatus(prev => prev ? { ...prev, status: 'cancelled' } : null)
      }
      
      return result
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Cancel failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }

  // Poll for status updates
  useEffect(() => {
    if (!workflowId || !status || status.status === 'completed' || status.status === 'failed' || status.status === 'cancelled') {
      return
    }

    const interval = setInterval(async () => {
      await getWorkflowStatus(workflowId)
    }, pollInterval)

    return () => clearInterval(interval)
  }, [workflowId, status?.status, pollInterval])

  // Initial status fetch
  useEffect(() => {
    if (workflowId && !status) {
      getWorkflowStatus(workflowId)
    }
  }, [workflowId])

  return {
    status,
    loading,
    error,
    startWorkflow,
    getWorkflowStatus,
    cancelWorkflow,
    isRunning: status?.status === 'running' || status?.status === 'pending',
    isCompleted: status?.status === 'completed',
    isFailed: status?.status === 'failed',
    isCancelled: status?.status === 'cancelled'
  }
}

// Hook for onboarding workflow specifically
export function useOnboardingWorkflow() {
  const workflow = useTemporalWorkflow({})

  const startOnboarding = async (onboardingData: Record<string, any>) => {
    try {
      const response = await fetch('/api/onboarding', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': 'demo-user',
          'x-tenant-id': 'demo-tenant'
        },
        body: JSON.stringify(onboardingData)
      })

      if (!response.ok) {
        throw new Error(`Onboarding failed: ${response.statusText}`)
      }

      const result = await response.json()
      
      if (result.success) {
        // Set up polling for the main workflow
        workflow.getWorkflowStatus(result.workflow_id)
        return result
      } else {
        throw new Error(result.error || 'Onboarding failed')
      }
    } catch (error) {
      console.error('Onboarding workflow error:', error)
      throw error
    }
  }

  return {
    ...workflow,
    startOnboarding
  }
}