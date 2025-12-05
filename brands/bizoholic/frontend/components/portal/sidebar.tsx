'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
    LayoutDashboard,
    Users,
    Settings,
    CreditCard,
    HelpCircle,
    FileText,
    Bell,
    LogOut,
    Bot,
    BarChart3,
    Megaphone
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/hooks/use-auth'

export function Sidebar() {
    const pathname = usePathname()
    const { user, logout } = useAuth()

    const navigation = [
        { name: 'Dashboard', href: '/portal/dashboard', icon: LayoutDashboard },
        { name: 'CRM', href: '/portal/dashboard/crm', icon: Users },
        { name: 'Content (CMS)', href: '/portal/dashboard/content', icon: FileText },
        { name: 'AI Assistant', href: '/portal/dashboard/ai-assistant', icon: Bot },
        { name: 'My Services', href: '/portal/dashboard/services', icon: Megaphone },
        { name: 'Campaigns', href: '/portal/dashboard/campaigns', icon: Megaphone },
        { name: 'Analytics', href: '/portal/dashboard/analytics', icon: BarChart3 },
        { name: 'Billing', href: '/portal/dashboard/billing', icon: CreditCard },
        { name: 'Team', href: '/portal/dashboard/team', icon: Users },
        { name: 'Support', href: '/portal/dashboard/support', icon: HelpCircle },
        { name: 'Settings', href: '/portal/dashboard/settings', icon: Settings },
    ]

    return (
        <div className="flex h-full w-64 flex-col bg-slate-900 text-white">
            {/* Logo */}
            <div className="flex h-16 items-center px-6 border-b border-slate-800">
                <Link href="/portal/dashboard" className="flex items-center gap-2 font-bold text-xl">
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
                        const isActive = pathname === item.href
                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className={cn(
                                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                                    isActive
                                        ? 'bg-blue-600 text-white'
                                        : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                                )}
                            >
                                <item.icon className="h-5 w-5" />
                                {item.name}
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
