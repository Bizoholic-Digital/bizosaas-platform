'use client'

import { useState } from 'react'
import { AIAgentStatus } from './ai-agent-status'
import { AIAgentDetail } from './ai-agent-detail'

export function AIAgentManager() {
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null)

  const handleAgentClick = (agentId: string) => {
    setSelectedAgentId(agentId)
  }

  const handleBackToList = () => {
    setSelectedAgentId(null)
  }

  if (selectedAgentId) {
    return (
      <AIAgentDetail 
        agentId={selectedAgentId} 
        onBack={handleBackToList} 
      />
    )
  }

  return (
    <AIAgentStatus onAgentClick={handleAgentClick} />
  )
}