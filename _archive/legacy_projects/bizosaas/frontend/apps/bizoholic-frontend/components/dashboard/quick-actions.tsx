'use client'

import { Plus, Zap, Users, BarChart3, Target, FileText, Palette } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import Link from 'next/link'

const quickActions = [
  {
    name: 'Create Campaign',
    icon: Target,
    href: '/dashboard/campaigns/create',
    description: 'Launch a new AI-powered campaign',
    color: 'bg-blue-500 hover:bg-blue-600'
  },
  {
    name: 'Add Client',
    icon: Users,
    href: '/dashboard/clients/create',
    description: 'Onboard a new client',
    color: 'bg-green-500 hover:bg-green-600'
  },
  {
    name: 'Build Page',
    icon: Palette,
    href: '/dashboard/page-builder',
    description: 'Create landing pages',
    color: 'bg-purple-500 hover:bg-purple-600'
  },
  {
    name: 'View Reports',
    icon: BarChart3,
    href: '/dashboard/analytics/reports',
    description: 'Check performance metrics',
    color: 'bg-orange-500 hover:bg-orange-600'
  },
  {
    name: 'AI Content',
    icon: FileText,
    href: '/dashboard/agents/content-studio',
    description: 'Generate content with AI',
    color: 'bg-pink-500 hover:bg-pink-600'
  },
  {
    name: 'Automate',
    icon: Zap,
    href: '/dashboard/integrations',
    description: 'Set up automations',
    color: 'bg-cyan-500 hover:bg-cyan-600'
  }
]

export function QuickActions() {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold">Quick Actions</h3>
          <Plus className="h-4 w-4 text-muted-foreground" />
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {quickActions.map((action) => {
            const Icon = action.icon
            return (
              <Link key={action.name} href={action.href}>
                <Button
                  variant="outline"
                  className="h-auto p-4 flex flex-col items-center space-y-2 hover:shadow-md transition-all"
                >
                  <div className={`p-2 rounded-lg text-white ${action.color}`}>
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="text-center">
                    <div className="font-medium text-xs">{action.name}</div>
                    <div className="text-xs text-muted-foreground">{action.description}</div>
                  </div>
                </Button>
              </Link>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}