"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import {
  BarChart3,
  Package,
  ShoppingCart,
  Search,
  Settings,
  ArrowLeft,
  Home,
  Bell,
  User,
} from "lucide-react";

const adminNavItems = [
  {
    name: "Dashboard",
    href: "/coreldove/admin",
    icon: Home,
    description: "Overview & insights"
  },
  {
    name: "Analytics",
    href: "/coreldove/admin/analytics",
    icon: BarChart3,
    description: "Performance metrics"
  },
  {
    name: "Sourcing",
    href: "/coreldove/admin/sourcing",
    icon: Search,
    description: "Product discovery"
  },
  {
    name: "Products",
    href: "/coreldove/products",
    icon: Package,
    description: "Product catalog"
  },
  {
    name: "Inventory",
    href: "/coreldove/admin/inventory",
    icon: Package,
    description: "Stock management"
  },
  {
    name: "Orders",
    href: "/coreldove/admin/orders",
    icon: ShoppingCart,
    description: "Order processing"
  },
];

export default function CoreLDoveAdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-orange-100">
      {/* Admin Header */}
      <header className="bg-white border-b border-orange-200 sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <Link 
                href="/coreldove"
                className="flex items-center gap-2 text-orange-600 hover:text-orange-700 transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                <span className="text-sm">Back to Storefront</span>
              </Link>
              <div className="h-6 w-px bg-orange-200" />
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center">
                  <Package className="w-4 h-4 text-white" />
                </div>
                <div>
                  <h1 className="font-semibold text-gray-900">CoreLDove Admin</h1>
                  <Badge variant="secondary" className="text-xs bg-orange-100 text-orange-700">
                    Dropshipping Control Center
                  </Badge>
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <Button variant="outline" size="sm">
                <Bell className="w-4 h-4 mr-2" />
                Alerts
              </Button>
              <Button variant="outline" size="sm">
                <User className="w-4 h-4 mr-2" />
                Profile
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Admin Sidebar */}
          <aside className="lg:w-64 flex-shrink-0">
            <Card className="sticky top-24">
              <CardContent className="p-4">
                <nav className="space-y-2">
                  {adminNavItems.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;
                    
                    return (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={cn(
                          "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                          isActive
                            ? "bg-gradient-to-r from-orange-500 to-red-500 text-white"
                            : "text-gray-700 hover:bg-orange-100 hover:text-orange-700"
                        )}
                      >
                        <Icon className="w-4 h-4" />
                        <div>
                          <div>{item.name}</div>
                          {!isActive && (
                            <div className="text-xs text-gray-500">{item.description}</div>
                          )}
                        </div>
                      </Link>
                    );
                  })}
                </nav>
              </CardContent>
            </Card>
          </aside>

          {/* Admin Content */}
          <main className="flex-1 min-w-0">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}