'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/hooks/use-auth'
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuGroup,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
  DropdownMenuSub
} from "@/components/ui/dropdown-menu"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  User,
  Settings,
  LogOut,
  Shield,
  Building,
  Key,
  Activity,
  Globe,
  Zap,
  Crown,
  Eye,
  Lock,
  ExternalLink,
  ChevronRight
} from 'lucide-react'

const ROLE_CONFIG = {
  super_admin: {
    name: 'Super Admin',
    icon: Crown,
    color: 'text-yellow-600',
    bgColor: 'bg-yellow-100'
  },
  tenant_admin: {
    name: 'Admin',
    icon: Shield,
    color: 'text-blue-600',
    bgColor: 'bg-blue-100'
  },
  user: {
    name: 'User',
    icon: User,
    color: 'text-green-600',
    bgColor: 'bg-green-100'
  },
  readonly: {
    name: 'View Only',
    icon: Eye,
    color: 'text-gray-600',
    bgColor: 'bg-gray-100'
  },
  agent: {
    name: 'Service Agent',
    icon: Zap,
    color: 'text-purple-600',
    bgColor: 'bg-purple-100'
  }
}

const PLATFORM_LINKS = {
  bizoholic: {
    name: 'Bizoholic',
    url: 'http://localhost:3000',
    icon: Zap,
    description: 'AI Marketing Platform'
  },
  coreldove: {
    name: 'CoreLDove',
    url: 'http://localhost:3002',
    icon: Globe,
    description: 'E-commerce Platform'
  },
  temporal: {
    name: 'Temporal',
    url: 'http://localhost:8088',
    icon: Activity,
    description: 'Workflow Dashboard'
  }
}

export function UserProfileDropdown() {
  const { user, logout, isLoading } = useAuth()
  const [isLoggingOut, setIsLoggingOut] = useState(false)
  const router = useRouter()

  if (!user) return null

  const handleLogout = async () => {
    setIsLoggingOut(true)
    try {
      await logout()
      router.push('/auth/login')
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      setIsLoggingOut(false)
    }
  }

  const roleConfig = ROLE_CONFIG[user.user.role] || ROLE_CONFIG.user
  const RoleIcon = roleConfig.icon

  const getInitials = (user: any) => {
    if (user.user.first_name && user.user.last_name) {
      return `${user.user.first_name[0]}${user.user.last_name[0]}`.toUpperCase()
    }
    return user.user.email.slice(0, 2).toUpperCase()
  }

  const getDisplayName = (user: any) => {
    if (user.user.first_name && user.user.last_name) {
      return `${user.user.first_name} ${user.user.last_name}`
    }
    return user.user.email
  }

  const availablePlatforms = user.tenant.allowed_platforms.filter(
    platform => PLATFORM_LINKS[platform as keyof typeof PLATFORM_LINKS]
  )

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-10 w-10 rounded-full">
          <Avatar className="h-10 w-10">
            <AvatarImage src="/placeholder-avatar.png" alt={getDisplayName(user)} />
            <AvatarFallback className="text-sm font-medium">
              {getInitials(user)}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      
      <DropdownMenuContent className="w-80" align="end" forceMount>
        {/* User Info Section */}
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-3">
            <div className="flex items-center space-x-3">
              <Avatar className="h-12 w-12">
                <AvatarImage src="/placeholder-avatar.png" alt={getDisplayName(user)} />
                <AvatarFallback className="text-sm font-medium">
                  {getInitials(user)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {getDisplayName(user)}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {user.user.email}
                </p>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <Badge 
                variant="outline" 
                className={`${roleConfig.color} ${roleConfig.bgColor} border-current`}
              >
                <RoleIcon className="w-3 h-3 mr-1" />
                {roleConfig.name}
              </Badge>
              <div className="text-right">
                <p className="text-xs text-gray-500">{user.tenant.name}</p>
                <p className="text-xs text-gray-400">
                  Status: {user.tenant.status}
                </p>
              </div>
            </div>
          </div>
        </DropdownMenuLabel>

        <DropdownMenuSeparator />

        {/* Quick Actions */}
        <DropdownMenuGroup>
          <DropdownMenuItem asChild>
            <Link href="/dashboard/settings" className="cursor-pointer">
              <Settings className="mr-3 h-4 w-4" />
              <span>Settings</span>
            </Link>
          </DropdownMenuItem>
          
          <DropdownMenuItem asChild>
            <Link href="/dashboard/profile" className="cursor-pointer">
              <User className="mr-3 h-4 w-4" />
              <span>Profile</span>
            </Link>
          </DropdownMenuItem>

          {user.permissions.is_super_admin && (
            <DropdownMenuItem asChild>
              <Link href="/dashboard/super-admin" className="cursor-pointer">
                <Crown className="mr-3 h-4 w-4" />
                <span>Super Admin</span>
              </Link>
            </DropdownMenuItem>
          )}
        </DropdownMenuGroup>

        <DropdownMenuSeparator />

        {/* Platform Access */}
        <DropdownMenuSub>
          <DropdownMenuSubTrigger>
            <Globe className="mr-3 h-4 w-4" />
            <span>Switch Platform</span>
            <ChevronRight className="ml-auto h-4 w-4" />
          </DropdownMenuSubTrigger>
          <DropdownMenuSubContent className="w-64">
            <div className="p-2">
              <p className="text-xs font-medium text-gray-500 mb-2">
                Available Platforms
              </p>
              {availablePlatforms.map((platformKey) => {
                const platform = PLATFORM_LINKS[platformKey as keyof typeof PLATFORM_LINKS]
                if (!platform) return null
                
                const PlatformIcon = platform.icon
                
                return (
                  <DropdownMenuItem key={platformKey} asChild>
                    <a 
                      href={platform.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="cursor-pointer flex items-center justify-between w-full"
                    >
                      <div className="flex items-center">
                        <PlatformIcon className="mr-3 h-4 w-4" />
                        <div>
                          <div className="text-sm font-medium">{platform.name}</div>
                          <div className="text-xs text-gray-500">{platform.description}</div>
                        </div>
                      </div>
                      <ExternalLink className="h-3 w-3 text-gray-400" />
                    </a>
                  </DropdownMenuItem>
                )
              })}
              
              {availablePlatforms.length === 0 && (
                <div className="py-2 px-1">
                  <p className="text-xs text-gray-500">No platforms available</p>
                </div>
              )}
            </div>
          </DropdownMenuSubContent>
        </DropdownMenuSub>

        {/* Service Access */}
        {user.user.allowed_services.length > 0 && (
          <>
            <DropdownMenuSeparator />
            <DropdownMenuSub>
              <DropdownMenuSubTrigger>
                <Key className="mr-3 h-4 w-4" />
                <span>Service Access</span>
              </DropdownMenuSubTrigger>
              <DropdownMenuSubContent className="w-64">
                <div className="p-2">
                  <p className="text-xs font-medium text-gray-500 mb-2">
                    Enabled Services
                  </p>
                  {user.user.allowed_services.map((service) => (
                    <div key={service} className="flex items-center py-1">
                      <Lock className="mr-2 h-3 w-3 text-green-500" />
                      <span className="text-sm capitalize">{service.replace('-', ' ')}</span>
                    </div>
                  ))}
                </div>
              </DropdownMenuSubContent>
            </DropdownMenuSub>
          </>
        )}

        <DropdownMenuSeparator />

        {/* Account Info */}
        <div className="px-2 py-2">
          <div className="text-xs text-gray-500 space-y-1">
            <div className="flex justify-between">
              <span>Last Login:</span>
              <span>
                {(user.user as any).last_login_at 
                  ? new Date((user.user as any).last_login_at).toLocaleDateString()
                  : 'Never'
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span>Login Count:</span>
              <span>{(user.user as any).login_count || 'N/A'}</span>
            </div>
            <div className="flex justify-between">
              <span>Tenant ID:</span>
              <span className="font-mono text-xs truncate max-w-20">
                {user.tenant.id.split('-')[0]}...
              </span>
            </div>
          </div>
        </div>

        <DropdownMenuSeparator />

        {/* Logout */}
        <DropdownMenuItem 
          onClick={handleLogout} 
          disabled={isLoggingOut}
          className="text-red-600 focus:text-red-600"
        >
          <LogOut className="mr-3 h-4 w-4" />
          <span>{isLoggingOut ? 'Signing out...' : 'Sign out'}</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

// Compact version for mobile or smaller spaces
export function CompactUserProfile() {
  const { user, logout } = useAuth()
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  if (!user) return null

  const handleLogout = async () => {
    setIsLoggingOut(true)
    try {
      await logout()
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      setIsLoggingOut(false)
    }
  }

  const roleConfig = ROLE_CONFIG[user.user.role] || ROLE_CONFIG.user
  const RoleIcon = roleConfig.icon

  return (
    <div className="flex items-center space-x-2 p-2 rounded-lg bg-gray-50">
      <Avatar className="h-8 w-8">
        <AvatarFallback className="text-xs">
          {user.user.email.slice(0, 2).toUpperCase()}
        </AvatarFallback>
      </Avatar>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">
          {user.user.first_name || user.user.email.split('@')[0]}
        </p>
        <div className="flex items-center space-x-1">
          <RoleIcon className={`w-3 h-3 ${roleConfig.color}`} />
          <span className="text-xs text-gray-500">{roleConfig.name}</span>
        </div>
      </div>
      <Button 
        variant="ghost" 
        size="sm" 
        onClick={handleLogout}
        disabled={isLoggingOut}
        className="text-gray-500 hover:text-red-600"
      >
        <LogOut className="h-4 w-4" />
      </Button>
    </div>
  )
}