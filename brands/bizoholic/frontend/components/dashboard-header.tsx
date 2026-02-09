'use client'

import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import { Badge } from '@/components/ui/badge'
import { Search, Settings, User, LogOut, HelpCircle } from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'
import { RealTimeNotifications } from './real-time-notifications'
import { WebSocketStatus } from './websocket-status'
import { ThemeSwitcher } from './theme-switcher'

const pageNames: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/dashboard/campaigns': 'Campaigns',
  '/dashboard/agents': 'AI Agents',
  '/dashboard/analytics': 'Analytics',
  '/dashboard/crm': 'Leads & CRM',
  '/dashboard/content': 'Content Hub',
  '/dashboard/integrations': 'Integrations',
  '/dashboard/billing': 'Billing',
  '/dashboard/settings': 'Settings',
  '/dashboard/super-admin': 'Super Admin'
}

export function DashboardHeader() {
  const pathname = usePathname()
  const { user, logout } = useAuth()

  const currentPageName = pageNames[pathname || ''] || 'Dashboard'

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-4 md:px-6">
        <div className="flex flex-1 items-center gap-4">
          <h1 className="text-lg font-semibold md:text-xl">{currentPageName}</h1>

          {/* Page-specific badges */}
          {pathname === '/dashboard/super-admin' && (
            <Badge variant="outline" className="bg-yellow-100 text-yellow-800 border-yellow-300">
              God Mode
            </Badge>
          )}
          {pathname === '/dashboard/agents' && (
            <Badge variant="secondary" className="bg-blue-100 text-blue-800">
              AI Powered
            </Badge>
          )}
          {pathname === '/dashboard/campaigns' && (
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Automated
            </Badge>
          )}
        </div>

        <div className="flex items-center gap-4">
          {/* Search Button */}
          <Button variant="outline" size="sm" className="hidden md:flex">
            <Search className="h-4 w-4 mr-2" />
            Search
          </Button>

          {/* WebSocket Status */}
          <WebSocketStatus />

          {/* Real-time Notifications */}
          <RealTimeNotifications />

          {/* Theme Switcher */}
          <ThemeSwitcher />

          {/* Help Button */}
          <Button variant="ghost" size="sm">
            <HelpCircle className="h-4 w-4" />
          </Button>

          {/* User Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src="/avatars/user.jpg" alt={user?.first_name} />
                  <AvatarFallback>
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="text-xs leading-none text-muted-foreground">
                    {user?.email}
                  </p>
                  <div className="flex items-center gap-2 pt-1">
                    {user?.role === 'super_admin' && (
                      <Badge variant="secondary" className="text-xs">
                        Admin
                      </Badge>
                    )}
                  </div>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <User className="mr-2 h-4 w-4" />
                <span>Profile</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={logout}>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}