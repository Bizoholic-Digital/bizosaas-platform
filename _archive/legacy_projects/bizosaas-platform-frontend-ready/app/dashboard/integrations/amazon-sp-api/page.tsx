'use client'

import { AmazonSPAPIIntegration } from '@/components/integrations/amazon-sp-api-integration'
import { useUser } from '@/hooks/use-user'

export default function AmazonSPAPIPage() {
  const { user } = useUser()
  
  return (
    <div className="flex-1 space-y-6 p-8 pt-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Amazon SP-API Integration</h2>
          <p className="text-muted-foreground">
            AI-powered Amazon marketplace operations through the Brain API Gateway
          </p>
        </div>
      </div>
      
      <AmazonSPAPIIntegration tenantId={(user as any)?.organization_id || 'default'} />
    </div>
  )
}