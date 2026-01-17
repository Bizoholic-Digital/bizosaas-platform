'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
    LayoutDashboard,
    Users,
    Settings,
    CreditCard,
    HelpCircle,
    Bot,
    BarChart3,
    Megaphone,
    LogOut,
    Sparkles,
    Blocks,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/components/auth/AuthProvider'

export function Sidebar() {
    const pathname = usePathname()
    const { user, logout } = useAuth()

    // Check if user is admin or super_admin
    const isAdmin = user?.role === 'admin' || user?.role === 'super_admin'

    const navigation = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'My Services', href: '/dashboard/services', icon: Bot },
        { name: 'Campaigns', href: '/dashboard/campaigns', icon: Megaphone },
        { name: 'Analytics', href: '/dashboard/analytics', icon: BarChart3 },
        { name: 'Credits', href: '/billing/credits', icon: CreditCard },
        // AI Agents menu - only visible to admins
        ...(isAdmin ? [{
            name: 'AI Agents',
            href: '/ai-agents',
            icon: Sparkles,
            badge: '93'
        }] : []),
        { name: 'Integrations', href: '/dashboard/integrations', icon: Blocks },
        { name: 'Team', href: '/dashboard/team', icon: Users },
        { name: 'Support', href: '/dashboard/support', icon: HelpCircle },
        { name: 'Settings', href: '/dashboard/settings', icon: Settings },
    ]

    return (
        <div className="flex h-full w-64 flex-col bg-slate-900 text-white">
            {/* Logo */}
            <div className="flex h-16 items-center px-6 border-b border-slate-800">
                <Link href="/dashboard" className="flex items-center gap-2 font-bold text-xl">
                    <div className="h-8 w-8 rounded bg-blue-600 flex items-center justify-center">
                        B
                    </div>
                    <span>Bizoholic</span>
                </Link>
            </div>

            {/* Navigation */}
            <div className="flex-1 overflow-y-auto py-4">
                <nav className="space-y-1 px-3">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href || pathname.startsWith(item.href + '/')
                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className={cn(
                                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors relative',
                                    isActive
                                        ? 'bg-blue-600 text-white'
                                        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                )}
                            >
                                <item.icon className="h-5 w-5" />
                                {item.name}
                                {item.badge && (
                                    <span className="ml-auto text-xs bg-blue-500 text-white px-2 py-0.5 rounded-full">
                                        {item.badge}
                                    </span>
                                )}
                            </Link>
                        )
                    })}
                </nav>
            </div>

            {/* User Profile */}
            <div className="border-t border-slate-800 p-4">
                <div className="flex items-center gap-3 mb-4">
                    <div className="h-10 w-10 rounded-full bg-slate-700 flex items-center justify-center text-sm font-medium">
                        {user?.name?.[0] || 'U'}
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <p className="truncate text-sm font-medium text-white">
                            {user?.name || 'User'}
                        </p>
                        <p className="truncate text-xs text-slate-400">
                            {user?.email || 'user@example.com'}
                        </p>
                        {isAdmin && (
                            <p className="truncate text-xs text-blue-400 font-medium">
                                {user?.role === 'super_admin' ? 'Super Admin' : 'Admin'}
                            </p>
                        )}
                    </div>
                </div>
                <Button
                    variant="ghost"
                    className="w-full justify-start text-slate-400 hover:bg-slate-800 hover:text-white"
                    onClick={() => logout()}
                >
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out
                </Button>
            </div>
        </div>
    )
}
