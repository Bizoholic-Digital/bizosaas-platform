import React from 'react'
import { AgentDashboard } from '../../components/agent-management'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Agent Management | BizOSaaS Admin',
  description: 'Comprehensive AI agent management system for monitoring, controlling, and optimizing the BizOSaaS agent ecosystem',
}

export default function AgentsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <AgentDashboard />
    </div>
  )
}