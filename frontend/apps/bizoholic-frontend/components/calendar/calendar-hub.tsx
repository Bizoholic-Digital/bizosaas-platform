'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { CalendarDays, Bot, Users, Settings, Calendar as CalendarIcon, TrendingUp } from 'lucide-react'

import { CampaignCalendar } from './campaign-calendar'
import { AgentScheduler } from './agent-scheduler'
import { ClientMeetings } from './client-meetings'
import { MaintenanceWindows } from './maintenance-windows'

interface CalendarHubProps {
  tenantId?: string
  userRole?: 'super_admin' | 'admin' | 'client'
  className?: string
}

export function CalendarHub({ tenantId, userRole = 'admin', className }: CalendarHubProps) {
  const [activeTab, setActiveTab] = useState('campaigns')

  // Determine which tabs to show based on user role
  const availableTabs = [
    {
      key: 'campaigns',
      label: 'Campaign Calendar',
      icon: <TrendingUp className="h-4 w-4" />,
      description: 'Marketing campaigns and milestones',
      component: <CampaignCalendar tenantId={tenantId} className="mt-0" />,
      roles: ['super_admin', 'admin', 'client']
    },
    {
      key: 'agents',
      label: 'AI Agent Scheduler',
      icon: <Bot className="h-4 w-4" />,
      description: 'AI agent tasks and automation',
      component: <AgentScheduler tenantId={tenantId} className="mt-0" />,
      roles: ['super_admin', 'admin', 'client']
    },
    {
      key: 'meetings',
      label: 'Client Meetings',
      icon: <Users className="h-4 w-4" />,
      description: 'Client calls and sessions',
      component: <ClientMeetings tenantId={tenantId} className="mt-0" />,
      roles: ['super_admin', 'admin']
    },
    {
      key: 'maintenance',
      label: 'System Maintenance',
      icon: <Settings className="h-4 w-4" />,
      description: 'Infrastructure and updates',
      component: <MaintenanceWindows className="mt-0" />,
      roles: ['super_admin']
    }
  ].filter(tab => tab.roles.includes(userRole))

  return (
    <div className={`space-y-6 ${className}`}>
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2">
            <CalendarIcon className="h-5 w-5" />
            Calendar & Scheduling Hub
          </CardTitle>
          <CardDescription>
            Comprehensive calendar system for campaigns, AI agents, meetings, and maintenance
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-3">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4 mb-6">
              {availableTabs.map((tab) => (
                <TabsTrigger 
                  key={tab.key} 
                  value={tab.key}
                  className="flex items-center gap-2 text-sm"
                >
                  {tab.icon}
                  <span className="hidden sm:inline">{tab.label}</span>
                </TabsTrigger>
              ))}
            </TabsList>

            {availableTabs.map((tab) => (
              <TabsContent key={tab.key} value={tab.key} className="space-y-6">
                {/* Tab Description */}
                <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
                  <div className="flex items-center gap-3">
                    {tab.icon}
                    <div>
                      <h3 className="font-semibold">{tab.label}</h3>
                      <p className="text-sm text-muted-foreground">{tab.description}</p>
                    </div>
                  </div>
                  {userRole === 'super_admin' && (
                    <Badge variant="outline">
                      {userRole.replace('_', ' ').toUpperCase()}
                    </Badge>
                  )}
                </div>

                {/* Tab Content */}
                {tab.component}
              </TabsContent>
            ))}
          </Tabs>
        </CardContent>
      </Card>

      {/* Quick Calendar Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CalendarDays className="h-5 w-5" />
            Quick Overview
          </CardTitle>
          <CardDescription>
            Today's scheduled activities across all calendar types
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Today's Campaigns */}
            <div className="text-center p-4 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-950/20 dark:to-pink-950/20 rounded-lg">
              <TrendingUp className="h-8 w-8 mx-auto mb-2 text-purple-600" />
              <div className="text-2xl font-bold text-purple-700 dark:text-purple-400">3</div>
              <div className="text-sm text-purple-600 dark:text-purple-400">Campaign Events</div>
            </div>

            {/* Scheduled AI Tasks */}
            <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-950/20 dark:to-cyan-950/20 rounded-lg">
              <Bot className="h-8 w-8 mx-auto mb-2 text-blue-600" />
              <div className="text-2xl font-bold text-blue-700 dark:text-blue-400">7</div>
              <div className="text-sm text-blue-600 dark:text-blue-400">AI Agent Tasks</div>
            </div>

            {/* Client Meetings */}
            {userRole !== 'client' && (
              <div className="text-center p-4 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 rounded-lg">
                <Users className="h-8 w-8 mx-auto mb-2 text-green-600" />
                <div className="text-2xl font-bold text-green-700 dark:text-green-400">2</div>
                <div className="text-sm text-green-600 dark:text-green-400">Client Meetings</div>
              </div>
            )}

            {/* System Maintenance */}
            {userRole === 'super_admin' && (
              <div className="text-center p-4 bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-950/20 dark:to-red-950/20 rounded-lg">
                <Settings className="h-8 w-8 mx-auto mb-2 text-orange-600" />
                <div className="text-2xl font-bold text-orange-700 dark:text-orange-400">1</div>
                <div className="text-sm text-orange-600 dark:text-orange-400">Maintenance</div>
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap gap-2 mt-6 pt-6 border-t">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => setActiveTab('campaigns')}
              className="gap-2"
            >
              <TrendingUp className="h-4 w-4" />
              Schedule Campaign
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => setActiveTab('agents')}
              className="gap-2"
            >
              <Bot className="h-4 w-4" />
              Schedule AI Task
            </Button>
            {userRole !== 'client' && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setActiveTab('meetings')}
                className="gap-2"
              >
                <Users className="h-4 w-4" />
                Schedule Meeting
              </Button>
            )}
            {userRole === 'super_admin' && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setActiveTab('maintenance')}
                className="gap-2"
              >
                <Settings className="h-4 w-4" />
                Plan Maintenance
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}