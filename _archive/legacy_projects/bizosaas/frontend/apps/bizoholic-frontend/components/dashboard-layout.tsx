"use client"

import { useState, useEffect } from "react"
import { useRouter, usePathname } from "next/navigation"
import Link from "next/link"
import Image from "next/image"
import { cn } from "@/lib/utils"
import { usePlatform, type Platform } from "@/lib/platform-config"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import {
  Bell,
  ChevronLeft,
  ChevronRight,
  Home,
  LineChart,
  Menu,
  Package,
  Package2,
  Search,
  ShoppingCart,
  Users,
  Settings,
  User,
  LogOut,
  Truck,
  BarChart3,
  DollarSign,
  TrendingUp,
  Zap,
  Globe,
  Store,
  CreditCard,
  FileText,
  MessageSquare,
  Shield,
  Palette,
  Moon,
  Sun
} from "lucide-react"
import { useTheme } from "next-themes"

interface DashboardLayoutProps {
  children: React.ReactNode
  platform?: Platform
  userRole?: "superadmin" | "admin" | "client" | "seller" | "marketplace-admin"
}

interface NavigationItem {
  title: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  badge?: string
  children?: NavigationItem[]
}

export function DashboardLayout({ 
  children, 
  platform: overridePlatform, 
  userRole = "seller" 
}: DashboardLayoutProps) {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const pathname = usePathname()
  const { theme, setTheme } = useTheme()
  
  // Use platform detection with optional override
  const { platform: detectedPlatform, config } = usePlatform()
  const platform = overridePlatform || detectedPlatform

  // Role-based navigation
  const getNavigation = (): NavigationItem[] => {
    const baseNav: NavigationItem[] = []

    if (platform === "coreldove") {
      if (userRole === "seller" || userRole === "superadmin") {
        baseNav.push(
          {
            title: "Dashboard",
            href: "/seller",
            icon: Home
          },
          {
            title: "Dropshipping",
            href: "/seller/dropshipping",
            icon: Truck,
            badge: "NEW"
          },
          {
            title: "My Products",
            href: "/seller/products",
            icon: Package
          },
          {
            title: "Orders",
            href: "/seller/orders", 
            icon: ShoppingCart,
            badge: "12"
          },
          {
            title: "Analytics",
            href: "/seller/analytics",
            icon: BarChart3
          },
          {
            title: "Earnings",
            href: "/seller/earnings",
            icon: DollarSign
          }
        )
      }
      
      if (userRole === "marketplace-admin" || userRole === "superadmin") {
        baseNav.push(
          {
            title: "Marketplace",
            href: "/admin/marketplace",
            icon: Store
          },
          {
            title: "Sellers",
            href: "/admin/sellers",
            icon: Users
          },
          {
            title: "Products",
            href: "/admin/products",
            icon: Package
          }
        )
      }
    }

    if (platform === "bizoholic") {
      baseNav.push(
        {
          title: "Dashboard",
          href: "/dashboard",
          icon: Home
        },
        {
          title: "Campaigns",
          href: "/campaigns",
          icon: TrendingUp
        },
        {
          title: "Clients",
          href: "/clients",
          icon: Users
        },
        {
          title: "Analytics",
          href: "/analytics",
          icon: LineChart
        },
        {
          title: "AI Agents",
          href: "/ai-agents",
          icon: Zap
        }
      )
    }

    if (platform === "bizosaas") {
      baseNav.push(
        {
          title: "Dashboard", 
          href: "/bizosaas",
          icon: Home
        },
        {
          title: "Directory",
          href: "/directory",
          icon: Globe
        },
        {
          title: "Services",
          href: "/services", 
          icon: Package
        },
        {
          title: "Billing",
          href: "/billing",
          icon: CreditCard
        }
      )
    }

    // Common navigation items
    baseNav.push(
      {
        title: "Messages",
        href: "/messages",
        icon: MessageSquare,
        badge: "3"
      },
      {
        title: "Settings",
        href: "/settings",
        icon: Settings
      }
    )

    return baseNav
  }

  const navigation = getNavigation()

  // User info based on role
  const getUserInfo = () => {
    switch (userRole) {
      case "superadmin":
        return { name: "Super Admin", email: "admin@bizoholic.com", avatar: "/avatars/admin.png" }
      case "seller":
        return { name: "Seller", email: "seller@coreldove.com", avatar: "/avatars/seller.png" }
      case "marketplace-admin":
        return { name: "Marketplace Admin", email: "admin@coreldove.com", avatar: "/avatars/admin.png" }
      case "client":
        return { name: "Client", email: "client@bizosaas.com", avatar: "/avatars/client.png" }
      default:
        return { name: "User", email: "user@example.com", avatar: "/avatars/default.png" }
    }
  }

  const userInfo = getUserInfo()

  const NavigationItems = ({ items }: { items: NavigationItem[] }) => (
    <div className="space-y-1">
      {items.map((item) => (
        <TooltipProvider key={item.href}>
          <Tooltip>
            <TooltipTrigger asChild>
              <Link
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all hover:bg-accent hover:text-accent-foreground",
                  pathname === item.href 
                    ? `bg-gradient-to-r ${config.primaryColor} text-white shadow-sm` 
                    : "text-muted-foreground",
                  collapsed && "justify-center px-2"
                )}
                onClick={() => setMobileOpen(false)}
              >
                <item.icon className={cn("h-4 w-4", collapsed ? "" : "mr-2")} />
                {!collapsed && (
                  <>
                    <span className="flex-1">{item.title}</span>
                    {item.badge && (
                      <Badge variant="secondary" className="ml-auto h-5 w-auto px-1.5 text-xs">
                        {item.badge}
                      </Badge>
                    )}
                  </>
                )}
              </Link>
            </TooltipTrigger>
            {collapsed && (
              <TooltipContent side="right">
                <p>{item.title}</p>
              </TooltipContent>
            )}
          </Tooltip>
        </TooltipProvider>
      ))}
    </div>
  )

  const SidebarContent = () => (
    <div className="flex h-full flex-col">
      {/* Logo */}
      <div className={cn("flex items-center border-b p-6", collapsed && "px-2 justify-center")}>
        <div className="flex items-center gap-2">
          <div className={cn("relative", collapsed ? "h-8 w-8" : "h-10 w-10")}>
            <Image
              src={config.logo}
              alt={`${config.name} Logo`}
              fill
              className="object-contain"
            />
          </div>
          {!collapsed && (
            <div className="flex flex-col">
              <span className="text-lg font-bold">{config.name}</span>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <ScrollArea className="flex-1 px-3 py-4">
        <NavigationItems items={navigation} />
      </ScrollArea>

      {/* User Profile */}
      <div className="border-t p-3">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className={cn(
                "w-full justify-start gap-2 p-2",
                collapsed && "justify-center px-2"
              )}
            >
              <Avatar className="h-8 w-8">
                <AvatarImage src={userInfo.avatar} />
                <AvatarFallback>{userInfo.name.charAt(0)}</AvatarFallback>
              </Avatar>
              {!collapsed && (
                <div className="flex-1 text-left">
                  <p className="text-sm font-medium">{userInfo.name}</p>
                  <p className="text-xs text-muted-foreground">{userInfo.email}</p>
                </div>
              )}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <User className="mr-2 h-4 w-4" />
              Profile
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <LogOut className="mr-2 h-4 w-4" />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Collapse Toggle */}
      <div className="border-t p-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setCollapsed(!collapsed)}
          className="w-full"
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </Button>
      </div>
    </div>
  )

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Desktop Sidebar */}
      <aside className={cn(
        "hidden border-r bg-card/50 transition-all duration-300 lg:block",
        collapsed ? "w-16" : "w-64"
      )}>
        <SidebarContent />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetContent side="left" className="w-64 p-0">
          <SidebarContent />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="flex h-16 items-center border-b bg-card/50 px-6 lg:px-8">
          <div className="flex items-center gap-4">
            {/* Mobile Menu Button */}
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="outline" size="icon" className="lg:hidden">
                  <Menu className="h-4 w-4" />
                </Button>
              </SheetTrigger>
            </Sheet>

            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="search"
                placeholder="Search..."
                className="w-full rounded-lg border border-input bg-background pl-10 pr-4 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>

          <div className="ml-auto flex items-center gap-4">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
            >
              <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            </Button>

            {/* Notifications */}
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="h-4 w-4" />
              <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-red-500" />
            </Button>

            {/* User Menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={userInfo.avatar} />
                    <AvatarFallback>{userInfo.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end">
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium">{userInfo.name}</p>
                    <p className="text-xs text-muted-foreground">{userInfo.email}</p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <User className="mr-2 h-4 w-4" />
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Settings className="mr-2 h-4 w-4" />
                  Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <LogOut className="mr-2 h-4 w-4" />
                  Log out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-6 lg:p-8">
          <div className="mx-auto max-w-7xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}