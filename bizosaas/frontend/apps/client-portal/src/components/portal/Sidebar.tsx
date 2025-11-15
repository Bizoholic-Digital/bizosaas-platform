'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  LayoutDashboard, Users, FileText, ShoppingCart, CreditCard,
  FolderKanban, UsersRound, HeadphonesIcon, MapPin, TrendingUp,
  BarChart3, Bot, Star, Trophy, CheckSquare, Settings, Menu, X,
  Megaphone, Plug
} from 'lucide-react'
import { cn } from '@/lib/utils'

interface NavItem {
  name: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  badge?: string
  feature?: string
  requiredRole?: 'client' | 'partner' | 'moderator' | 'admin'
}

const navigationItems: NavItem[] = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'CRM',
    href: '/crm',
    icon: Users,
    feature: 'crm' as any,
  },
  {
    name: 'Content',
    href: '/content',
    icon: FileText,
  },
  {
    name: 'E-commerce',
    href: '/ecommerce',
    icon: ShoppingCart,
    feature: 'ecommerce' as any,
  },
  {
    name: 'Billing',
    href: '/billing',
    icon: CreditCard,
    feature: 'billing' as any,
  },
  {
    name: 'Projects',
    href: '/projects',
    icon: FolderKanban,
  },
  {
    name: 'Team',
    href: '/team',
    icon: UsersRound,
    requiredRole: 'partner',
  },
  {
    name: 'Support',
    href: '/support',
    icon: HeadphonesIcon,
  },
  {
    name: 'Directory',
    href: '/directory',
    icon: MapPin,
  },
  {
    name: 'Marketing',
    href: '/marketing',
    icon: Megaphone,
    feature: 'marketing' as any,
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
    feature: 'analytics' as any,
  },
  {
    name: 'AI Agents',
    href: '/ai-agents',
    icon: Bot,
    feature: 'aiAgents' as any,
  },
  {
    name: 'Reviews',
    href: '/reviews',
    icon: Star,
    feature: 'reviews' as any,
  },
  {
    name: 'Gamification',
    href: '/gamification',
    icon: Trophy,
    feature: 'gamification' as any,
  },
  {
    name: 'Approvals',
    href: '/approvals',
    icon: CheckSquare,
    badge: '3',
  },
  {
    name: 'Integrations',
    href: '/integrations',
    icon: Plug,
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
  },
]

export default function Sidebar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const pathname = usePathname()

  // Show all navigation items for now
  // TODO: Filter based on tenant features and user roles when backend is ready
  const visibleItems = navigationItems

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-white shadow-md hover:bg-gray-50"
      >
        {isMobileMenuOpen ? (
          <X className="h-6 w-6 text-gray-700" />
        ) : (
          <Menu className="h-6 w-6 text-gray-700" />
        )}
      </button>

      {/* Overlay for mobile */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-40 h-screen w-64 bg-white border-r border-gray-200 transition-transform duration-300',
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-center h-16 border-b border-gray-200">
          <h1 className="text-xl font-bold text-solid-900">BizOSaaS</h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-1">
          {visibleItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`)

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={cn(
                  'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-solid-900 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                )}
              >
                <Icon className="h-5 w-5 flex-shrink-0" />
                <span className="flex-1">{item.name}</span>
                {item.badge && (
                  <span
                    className={cn(
                      'px-2 py-0.5 text-xs font-semibold rounded-full',
                      isActive
                        ? 'bg-white text-solid-900'
                        : 'bg-solid-900 text-white'
                    )}
                  >
                    {item.badge}
                  </span>
                )}
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-gray-200 p-4">
          <p className="text-xs text-gray-500 text-center">
            © 2025 BizOSaaS
          </p>
        </div>
      </aside>
    </>
  )
}
