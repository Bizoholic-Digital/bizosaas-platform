'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Bot, 
  BarChart3, 
  Users, 
  Megaphone, 
  Settings, 
  HelpCircle,
  CreditCard,
  Zap,
  FileText,
  Target,
  TrendingUp,
  Shield,
  Database,
  Palette,
  ChevronDown
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { useState } from 'react'

const navigation = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: BarChart3,
    current: false,
  },
  {
    name: 'AI Agents',
    href: '/dashboard/agents',
    icon: Bot,
    current: false,
    badge: '12',
    children: [
      { name: 'Campaign Strategy', href: '/dashboard/agents/campaign-strategy' },
      { name: 'Content Studio', href: '/dashboard/agents/content-studio' },
      { name: 'SEO Optimizer', href: '/dashboard/agents/seo-optimizer' },
      { name: 'Social Media', href: '/dashboard/agents/social-media' },
      { name: 'Analytics', href: '/dashboard/agents/analytics' },
    ]
  },
  {
    name: 'Campaigns',
    href: '/dashboard/campaigns',
    icon: Target,
    current: false,
    children: [
      { name: 'Active Campaigns', href: '/dashboard/campaigns/active' },
      { name: 'Create Campaign', href: '/dashboard/campaigns/create' },
      { name: 'Templates', href: '/dashboard/campaigns/templates' },
      { name: 'A/B Tests', href: '/dashboard/campaigns/ab-tests' },
    ]
  },
  {
    name: 'Analytics',
    href: '/dashboard/analytics',
    icon: TrendingUp,
    current: false,
    children: [
      { name: 'Performance', href: '/dashboard/analytics/performance' },
      { name: 'Attribution', href: '/dashboard/analytics/attribution' },
      { name: 'Custom Reports', href: '/dashboard/analytics/reports' },
      { name: 'Real-time', href: '/dashboard/analytics/realtime' },
    ]
  },
  {
    name: 'Clients',
    href: '/dashboard/clients',
    icon: Users,
    current: false,
    children: [
      { name: 'All Clients', href: '/dashboard/clients' },
      { name: 'Add Client', href: '/dashboard/clients/create' },
      { name: 'Client Reports', href: '/dashboard/clients/reports' },
    ]
  },
  {
    name: 'Page Builder',
    href: '/dashboard/page-builder',
    icon: Palette,
    current: false,
    badge: 'New',
  },
  {
    name: 'Reports',
    href: '/dashboard/reports',
    icon: FileText,
    current: false,
  },
  {
    name: 'Integrations',
    href: '/dashboard/integrations',
    icon: Zap,
    current: false,
  },
]

const secondaryNavigation = [
  {
    name: 'Billing',
    href: '/dashboard/billing',
    icon: CreditCard,
  },
  {
    name: 'Data & Security',
    href: '/dashboard/security',
    icon: Shield,
  },
  {
    name: 'Database',
    href: '/dashboard/database',
    icon: Database,
  },
  {
    name: 'Settings',
    href: '/dashboard/settings',
    icon: Settings,
  },
  {
    name: 'Help & Support',
    href: '/dashboard/help',
    icon: HelpCircle,
  },
]

export function DashboardSidebar() {
  const pathname = usePathname()
  const [openSections, setOpenSections] = useState<string[]>(['AI Agents', 'Campaigns'])

  const toggleSection = (sectionName: string) => {
    setOpenSections(prev => 
      prev.includes(sectionName) 
        ? prev.filter(name => name !== sectionName)
        : [...prev, sectionName]
    )
  }

  const isCurrentPath = (href: string) => {
    if (href === '/dashboard') {
      return pathname === href
    }
    return pathname?.startsWith(href) || false
  }

  return (
    <div className="flex h-full flex-col overflow-y-auto border-r bg-muted/10">
      {/* Logo */}
      <div className="flex h-16 shrink-0 items-center px-6 border-b">
        <Link href="/dashboard" className="flex items-center space-x-2">
          <Bot className="h-8 w-8 text-primary" />
          <span className="text-xl font-bold">Bizoholic</span>
        </Link>
      </div>
      
      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        <div className="space-y-1">
          {navigation.map((item) => {
            const current = isCurrentPath(item.href)
            
            if (item.children) {
              const isOpen = openSections.includes(item.name)
              return (
                <Collapsible key={item.name} open={isOpen} onOpenChange={() => toggleSection(item.name)}>
                  <CollapsibleTrigger asChild>
                    <Button
                      variant={current ? 'secondary' : 'ghost'}
                      className={cn(
                        'w-full justify-start px-3 py-2 text-sm font-medium',
                        current
                          ? 'bg-secondary text-secondary-foreground'
                          : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                      )}
                    >
                      <item.icon className="mr-3 h-4 w-4" />
                      <span className="flex-1 text-left">{item.name}</span>
                      {item.badge && (
                        <Badge variant="secondary" className="ml-2 h-5 px-1.5 text-xs">
                          {item.badge}
                        </Badge>
                      )}
                      <ChevronDown 
                        className={cn(
                          'ml-2 h-4 w-4 transition-transform',
                          isOpen && 'rotate-180'
                        )} 
                      />
                    </Button>
                  </CollapsibleTrigger>
                  <CollapsibleContent className="space-y-1 pl-6">
                    {item.children.map((child) => {
                      const childCurrent = isCurrentPath(child.href)
                      return (
                        <Link key={child.name} href={child.href}>
                          <Button
                            variant={childCurrent ? 'secondary' : 'ghost'}
                            size="sm"
                            className={cn(
                              'w-full justify-start px-3 py-1.5 text-sm',
                              childCurrent
                                ? 'bg-secondary/50 text-secondary-foreground'
                                : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                            )}
                          >
                            {child.name}
                          </Button>
                        </Link>
                      )
                    })}
                  </CollapsibleContent>
                </Collapsible>
              )
            }
            
            return (
              <Link key={item.name} href={item.href}>
                <Button
                  variant={current ? 'secondary' : 'ghost'}
                  className={cn(
                    'w-full justify-start px-3 py-2 text-sm font-medium',
                    current
                      ? 'bg-secondary text-secondary-foreground'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  )}
                >
                  <item.icon className="mr-3 h-4 w-4" />
                  {item.name}
                  {item.badge && (
                    <Badge variant="secondary" className="ml-auto h-5 px-1.5 text-xs">
                      {item.badge}
                    </Badge>
                  )}
                </Button>
              </Link>
            )
          })}
        </div>
        
        <Separator className="my-4" />
        
        {/* Secondary Navigation */}
        <div className="space-y-1">
          {secondaryNavigation.map((item) => {
            const current = isCurrentPath(item.href)
            return (
              <Link key={item.name} href={item.href}>
                <Button
                  variant={current ? 'secondary' : 'ghost'}
                  className={cn(
                    'w-full justify-start px-3 py-2 text-sm',
                    current
                      ? 'bg-secondary text-secondary-foreground'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                  )}
                >
                  <item.icon className="mr-3 h-4 w-4" />
                  {item.name}
                </Button>
              </Link>
            )
          })}
        </div>
      </nav>
      
      {/* Upgrade Prompt */}
      <div className="p-4 border-t">
        <div className="rounded-lg bg-gradient-to-r from-primary/10 to-accent/10 p-3 text-center">
          <p className="text-sm font-medium mb-2">Upgrade to Pro</p>
          <p className="text-xs text-muted-foreground mb-3">
            Access all 28+ AI agents and enterprise features
          </p>
          <Button size="sm" className="w-full">
            Upgrade Now
          </Button>
        </div>
      </div>
    </div>
  )
}