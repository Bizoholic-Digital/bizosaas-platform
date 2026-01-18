'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Search, Grid, User } from 'lucide-react';
import { cn } from '@/lib/utils';

export function MobileNav() {
    const pathname = usePathname();

    const links = [
        { href: '/', icon: Home, label: 'Home' },
        { href: '/search', icon: Search, label: 'Search' },
        { href: '/c', icon: Grid, label: 'Categories' },
        { href: '/dashboard/my-businesses', icon: User, label: 'My Biz' },
    ];

    return (
        <div className="fixed bottom-0 left-0 right-0 z-50 bg-white dark:bg-slate-900 border-t border-gray-200 dark:border-gray-800 md:hidden pb-safe">
            <div className="flex justify-around items-center h-16 px-2">
                {links.map(({ href, icon: Icon, label }) => {
                    const isActive = pathname === href || (href !== '/' && pathname.startsWith(href));
                    return (
                        <Link
                            key={href}
                            href={href}
                            prefetch={false}
                            className={cn(
                                "flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors duration-200",
                                isActive
                                    ? "text-primary dark:text-primary"
                                    : "text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
                            )}
                        >
                            <Icon className={cn("w-6 h-6", isActive && "fill-current/20")} strokeWidth={isActive ? 2.5 : 2} />
                            <span className="text-[10px] font-medium">{label}</span>
                        </Link>
                    );
                })}
            </div>
        </div>
    );
}
