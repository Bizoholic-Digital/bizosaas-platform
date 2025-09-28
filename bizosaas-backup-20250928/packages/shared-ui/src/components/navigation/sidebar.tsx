'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  DashboardIcon, 
  GearIcon, 
  PersonIcon,
  BarChartIcon,
  ComponentInstanceIcon
} from '@radix-ui/react-icons';

const navigation = [
  { name: 'Dashboard', href: '/', icon: DashboardIcon },
  { name: 'Analytics', href: '/analytics', icon: BarChartIcon },
  { name: 'Bizoholic', href: '/bizoholic', icon: ComponentInstanceIcon },
  { name: 'CoreLDove', href: '/coreldove', icon: ComponentInstanceIcon },
  { name: 'Clients', href: '/clients', icon: PersonIcon },
  { name: 'Settings', href: '/settings', icon: GearIcon },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="w-64 bg-gray-900 text-white">
      <div className="p-6">
        <h1 className="text-xl font-bold">BizOSaaS</h1>
      </div>
      <nav className="mt-6">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center px-6 py-3 text-sm font-medium ${
                isActive
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}