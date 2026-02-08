"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { Logo } from "@/components/ui/logo";
import { useTenantTheme } from "@/components/tenant-theme-provider";
import {
  LayoutDashboard,
  Users,
  Settings,
  BarChart3,
  Menu,
  LogOut,
  Bot,
  Zap,
  CreditCard,
  Building,
  Target,
  PieChart,
  Megaphone,
  TrendingUp,
  ShoppingCart,
  Palette,
  Crown,
  MessageCircle,
  Headphones,
  Key,
  Monitor,
  Globe,
  Briefcase,
} from "lucide-react";
import { useAuthStore } from "@/lib/auth-store";
import { DarkModeToggle } from "@/components/DarkModeToggle";

// Hierarchical navigation structure with proper grouping
interface NavigationSection {
  title: string
  items: NavigationItem[]
}

interface NavigationItem {
  name: string
  href: string
  icon: any
  description: string
  badge?: string
  children?: NavigationItem[]
}

const navigation: NavigationSection[] = [
  {
    title: "Dashboard",
    items: [
      {
        name: "Overview",
        href: "/dashboard",
        icon: LayoutDashboard,
        description: "Dashboard overview and key metrics"
      },
      {
        name: "Unified Dashboard",
        href: "/dashboard/unified",
        icon: Monitor,
        description: "Central command center for all platform services",
        badge: "New"
      },
      {
        name: "Feature Access",
        href: "/dashboard/features",
        icon: Key,
        description: "Tier-based feature access and subscription management",
        badge: "Demo"
      }
    ]
  },
  {
    title: "AI & Automation",
    items: [
      {
        name: "AI Agents",
        href: "/dashboard/agents",
        icon: Bot,
        description: "Monitor and manage AI agents",
        badge: "Active"
      },
      {
        name: "Campaigns",
        href: "/dashboard/campaigns",
        icon: Target,
        description: "Manage AI-powered marketing campaigns",
        badge: "AI"
      },
      {
        name: "Analytics",
        href: "/dashboard/analytics",
        icon: BarChart3,
        description: "Performance analytics and insights"
      }
    ]
  },
  {
    title: "CRM Management",
    items: [
      {
        name: "CRM Overview",
        href: "/dashboard/crm",
        icon: Users,
        description: "Lead management and customer data",
        children: [
          {
            name: "Leads",
            href: "/dashboard/crm/leads",
            icon: Target,
            description: "Lead tracking and qualification"
          },
          {
            name: "Customers",
            href: "/dashboard/crm/customers",
            icon: Users,
            description: "Customer relationship management"
          },
          {
            name: "Pipeline",
            href: "/dashboard/crm/pipeline",
            icon: TrendingUp,
            description: "Sales pipeline management"
          }
        ]
      }
    ]
  },
  {
    title: "E-commerce Management",
    items: [
      {
        name: "CoreLDove Dashboard",
        href: "/dashboard/coreldove",
        icon: ShoppingCart,
        description: "AI-powered dropshipping platform",
        badge: "AI",
        children: [
          {
            name: "Orders",
            href: "/dashboard/coreldove/orders",
            icon: ShoppingCart,
            description: "Order management and fulfillment"
          },
          {
            name: "Products",
            href: "/dashboard/coreldove/products",
            icon: PieChart,
            description: "Product catalog and inventory"
          },
          {
            name: "Suppliers",
            href: "/dashboard/coreldove/suppliers",
            icon: Building,
            description: "Supplier network management"
          }
        ]
      }
    ]
  },
  {
    title: "Content & Communications",
    items: [
      {
        name: "Content Management",
        href: "/dashboard/cms",
        icon: Globe,
        description: "Multi-tenant Wagtail CMS with site-based isolation",
        badge: "CMS"
      },
      {
        name: "Content Hub",
        href: "/dashboard/content",
        icon: Palette,
        description: "AI-generated content and assets"
      },
      {
        name: "Client Support",
        href: "/dashboard/support",
        icon: MessageCircle,
        description: "Chat, support requests, and client communications",
        badge: "Live"
      }
    ]
  },
  {
    title: "Business Operations",
    items: [
      {
        name: "Business Operations",
        href: "/dashboard/business-operations",
        icon: Briefcase,
        description: "Payment processing, communications, SEO, and business analytics",
        badge: "Phase 4"
      },
      {
        name: "Integrations",
        href: "/dashboard/integrations",
        icon: Zap,
        description: "Platform integrations and APIs"
      },
      {
        name: "BYOK Management",
        href: "/dashboard/byok",
        icon: Key,
        description: "Bring Your Own Key configurations and billing",
        badge: "BYOK"
      }
    ]
  },
  {
    title: "Account Management",
    items: [
      {
        name: "Billing",
        href: "/dashboard/billing",
        icon: CreditCard,
        description: "Subscription and billing management"
      },
      {
        name: "Settings",
        href: "/dashboard/settings",
        icon: Settings,
        description: "Account and company settings"
      }
    ]
  }
];

// Super Admin navigation (only visible to super admins)
const superAdminNavigation = [
  {
    name: "Super Admin",
    href: "/dashboard/super-admin",
    icon: Crown,
    description: "System overview and multi-company management",
    badge: "God Mode"
  },
];

// Company switching navigation for multi-company users
const companyNavigation = [
  {
    name: "BizOholic Marketing",
    href: "http://localhost:3001",
    icon: Building,
    description: "Marketing agency platform",
    external: true,
    category: "frontend"
  },
  {
    name: "CoreLDove E-commerce", 
    href: "http://localhost:3002",
    icon: ShoppingCart,
    description: "AI-powered dropshipping platform",
    external: true,
    category: "frontend"
  },
];

// Backend dashboard navigation for super admins
const backendNavigation = [
  {
    name: "Saleor E-commerce Admin",
    href: "http://localhost:9020",
    icon: ShoppingCart,
    description: "Product catalog and order management",
    external: true,
    badge: "Admin"
  },
  {
    name: "Wagtail CMS Admin",
    href: "http://localhost:8006/admin/",
    icon: Palette,
    description: "Content management system",
    external: true,
    badge: "CMS"
  },
  {
    name: "Temporal Workflow UI",
    href: "http://localhost:8088",
    icon: Bot,
    description: "Workflow monitoring and debugging",
    external: true,
    badge: "Workflows"
  },
];

function SidebarContent() {
  const pathname = usePathname();
  const { user, logout } = useAuthStore();
  const { config } = useTenantTheme();

  return (
    <div className="flex h-full flex-col">
      <div className="flex h-16 items-center border-b px-6">
        <Logo 
          href="/dashboard" 
          priority={true}
          showText={true}
          width={32}
          height={32}
          className="flex items-center space-x-2"
        />
      </div>

      <ScrollArea className="flex-1 px-3 py-6">
        {/* Super Admin Navigation (if applicable) */}
        {user?.role === 'super-admin' && (
          <div className="mb-6">
            <nav className="space-y-1">
              {superAdminNavigation.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={cn(
                      "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors group border border-yellow-200 bg-gradient-to-r from-yellow-50 to-amber-50",
                      isActive
                        ? "bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-900 border-yellow-300"
                        : "text-yellow-800 hover:bg-gradient-to-r hover:from-yellow-100 hover:to-amber-100 hover:border-yellow-300"
                    )}
                  >
                    <div className="flex items-center">
                      <item.icon className="mr-3 h-4 w-4 text-yellow-600" />
                      <div>
                        <div>{item.name}</div>
                      </div>
                    </div>
                    {item.badge && (
                      <Badge variant="outline" className="text-xs bg-yellow-100 text-yellow-800 border-yellow-300">
                        {item.badge}
                      </Badge>
                    )}
                  </Link>
                );
              })}
            </nav>
          </div>
        )}

        {/* Hierarchical Navigation */}
        <nav className="space-y-4">
          {navigation.map((section, sectionIndex) => (
            <div key={section.title} className="space-y-2">
              {/* Section Header */}
              <div className="px-3 mb-2">
                <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  {section.title}
                </h3>
              </div>
              
              {/* Section Items */}
              <div className="space-y-1">
                {section.items.map((item) => {
                  const isActive = pathname === item.href;
                  const hasChildren = item.children && item.children.length > 0;
                  const isParentActive = hasChildren && item.children.some(child => pathname === child.href);
                  
                  return (
                    <div key={item.name}>
                      {/* Parent Item */}
                      <Link
                        href={item.href}
                        className={cn(
                          "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors group",
                          isActive || isParentActive
                            ? "bg-primary text-primary-foreground"
                            : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                        )}
                      >
                        <div className="flex items-center">
                          <item.icon className="mr-3 h-4 w-4" />
                          <div>
                            <div>{item.name}</div>
                          </div>
                        </div>
                        {item.badge && (
                          <Badge variant="secondary" className="text-xs">
                            {item.badge}
                          </Badge>
                        )}
                      </Link>
                      
                      {/* Child Items */}
                      {hasChildren && (isActive || isParentActive) && (
                        <div className="ml-6 mt-1 space-y-1">
                          {item.children.map((child) => {
                            const isChildActive = pathname === child.href;
                            return (
                              <Link
                                key={child.name}
                                href={child.href}
                                className={cn(
                                  "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors group",
                                  isChildActive
                                    ? "bg-accent text-accent-foreground border-l-2 border-primary"
                                    : "text-muted-foreground hover:bg-accent/50 hover:text-accent-foreground"
                                )}
                              >
                                <div className="flex items-center">
                                  <child.icon className="mr-3 h-3 w-3" />
                                  <div>
                                    <div className="text-xs">{child.name}</div>
                                  </div>
                                </div>
                              </Link>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>

        {/* Bizoholic Admin Navigation */}
        {user?.role === 'bizoholic-admin' && (
          <div className="mt-8">
            <div className="px-3 mb-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                {config.branding.companyName} Website
              </h3>
            </div>
            <nav className="space-y-1">
              <Link
                href="/dashboard/bizoholic"
                className={cn(
                  "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors group border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50",
                  pathname === '/dashboard/bizoholic'
                    ? "bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-900 border-blue-300"
                    : "text-blue-800 hover:bg-gradient-to-r hover:from-blue-100 hover:to-indigo-100 hover:border-blue-300"
                )}
              >
                <div className="flex items-center">
                  <Globe className="mr-3 h-4 w-4 text-blue-600" />
                  <div>Website Manager</div>
                </div>
                <Badge variant="outline" className="text-xs bg-blue-100 text-blue-800 border-blue-300">
                  CMS
                </Badge>
              </Link>
              <Link
                href="http://localhost:8006/admin/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors group"
              >
                <div className="flex items-center">
                  <Palette className="mr-3 h-4 w-4" />
                  <div>Wagtail Admin</div>
                </div>
                <Badge variant="outline" className="text-xs">
                  External
                </Badge>
              </Link>
            </nav>
          </div>
        )}

        {/* CoreLDove Admin Navigation */}
        {user?.role === 'coreldove-admin' && (
          <div className="mt-8">
            <div className="px-3 mb-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                CoreLDove E-commerce
              </h3>
            </div>
            <nav className="space-y-1">
              <Link
                href="/dashboard/coreldove"
                className={cn(
                  "flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors group border border-green-200 bg-gradient-to-r from-green-50 to-emerald-50",
                  pathname === '/dashboard/coreldove'
                    ? "bg-gradient-to-r from-green-100 to-emerald-100 text-green-900 border-green-300"
                    : "text-green-800 hover:bg-gradient-to-r hover:from-green-100 hover:to-emerald-100 hover:border-green-300"
                )}
              >
                <div className="flex items-center">
                  <ShoppingCart className="mr-3 h-4 w-4 text-green-600" />
                  <div>E-commerce Manager</div>
                </div>
                <Badge variant="outline" className="text-xs bg-green-100 text-green-800 border-green-300">
                  Saleor
                </Badge>
              </Link>
              <Link
                href="http://localhost:9020"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors group"
              >
                <div className="flex items-center">
                  <ShoppingCart className="mr-3 h-4 w-4" />
                  <div>Saleor Admin</div>
                </div>
                <Badge variant="outline" className="text-xs">
                  External
                </Badge>
              </Link>
            </nav>
          </div>
        )}

        {/* Company Navigation */}
        {user?.role === 'super-admin' && (
          <div className="mt-8">
            <div className="px-3 mb-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Company Platforms
              </h3>
            </div>
            <nav className="space-y-1">
              {companyNavigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  target={item.external ? "_blank" : "_self"}
                  rel={item.external ? "noopener noreferrer" : ""}
                  className="flex items-center rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors group"
                >
                  <item.icon className="mr-3 h-4 w-4" />
                  <div>
                    <div>{item.name}</div>
                  </div>
                  {item.external && (
                    <div className="ml-auto">
                      <Badge variant="outline" className="text-xs">
                        External
                      </Badge>
                    </div>
                  )}
                </Link>
              ))}
            </nav>
          </div>
        )}

        {/* Backend Dashboard Navigation */}
        {user?.role === 'super-admin' && (
          <div className="mt-6">
            <div className="px-3 mb-2">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Backend Dashboards
              </h3>
            </div>
            <nav className="space-y-1">
              {backendNavigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  target={item.external ? "_blank" : "_self"}
                  rel={item.external ? "noopener noreferrer" : ""}
                  className="flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors group"
                >
                  <div className="flex items-center">
                    <item.icon className="mr-3 h-4 w-4" />
                    <div>
                      <div>{item.name}</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {item.badge && (
                      <Badge variant="outline" className="text-xs">
                        {item.badge}
                      </Badge>
                    )}
                    {item.external && (
                      <Badge variant="secondary" className="text-xs">
                        External
                      </Badge>
                    )}
                  </div>
                </Link>
              ))}
            </nav>
          </div>
        )}
      </ScrollArea>

      <div className="border-t p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="text-sm">
            <p className="font-medium">
              {user?.firstName} {user?.lastName}
            </p>
            <p className="text-muted-foreground text-xs">{user?.email}</p>
            {user?.subscription && (
              <Badge variant="outline" className="text-xs mt-1">
                {user.subscription.plan} {user.subscription.status === 'trial' ? 'Trial' : ''}
              </Badge>
            )}
          </div>
          <DarkModeToggle />
        </div>
        <Button variant="outline" size="sm" onClick={logout} className="w-full">
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </Button>
      </div>
    </div>
  );
}

export function DashboardSidebar() {
  return (
    <>
      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:z-50 lg:block lg:w-72 lg:bg-background lg:border-r">
        <SidebarContent />
      </div>

      {/* Mobile Sidebar */}
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="lg:hidden">
            <Menu className="h-4 w-4" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-72 p-0">
          <SidebarContent />
        </SheetContent>
      </Sheet>
    </>
  );
}
