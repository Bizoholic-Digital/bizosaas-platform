'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input'; // Assuming access to shared UI or we need to check existence
// Icons would ideally come from lucide-react if available, falling back to unicode/text
// import { Search, Menu, X, User, Bell } from 'lucide-react'; 

const NavLink = ({ href, children, active }: { href: string; children: React.ReactNode; active: boolean }) => (
    <Link href={href} className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${active ? 'bg-primary/10 text-primary' : 'text-muted-foreground hover:text-foreground hover:bg-muted'}`}>
        {children}
    </Link>
);

export function Navbar() {
    const pathname = usePathname();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const navItems = [
        { label: 'Games', href: '/games' },
        { label: 'Tournaments', href: '/tournaments' },
        { label: 'Leaderboard', href: '/leaderboard' },
        { label: 'News', href: '/news' },
    ];

    return (
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="flex h-16 items-center justify-between">

                    {/* Logo & Desktop Nav */}
                    <div className="flex items-center gap-8">
                        <Link href="/" className="flex items-center gap-2 font-bold text-xl">
                            <span className="text-2xl">⚡</span>
                            <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-pink-500">ThrillRing</span>
                        </Link>

                        <div className="hidden md:flex items-center gap-1">
                            {navItems.map((item) => (
                                <NavLink key={item.href} href={item.href} active={pathname === item.href || pathname?.startsWith(`${item.href}/`)}>
                                    {item.label}
                                </NavLink>
                            ))}
                        </div>
                    </div>

                    {/* Search & Actions */}
                    <div className="flex items-center gap-4">
                        <div className="hidden lg:flex relative w-64">
                            {/* Search Icon Placeholder */}
                            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-xs">🔍</span>
                            <input
                                type="text"
                                placeholder="Search games, players..."
                                className="w-full h-9 pl-9 pr-4 rounded-md border text-sm bg-muted/50 focus:bg-background focus:ring-1 focus:ring-primary outline-none transition-all"
                            />
                        </div>

                        <div className="hidden sm:flex items-center gap-2">
                            <Button variant="ghost" size="icon" className="text-muted-foreground">
                                🔔
                            </Button>
                            <Button variant="default" size="sm" className="bg-gradient-to-r from-indigo-600 to-purple-600 border-0">
                                Sign In
                            </Button>
                        </div>

                        {/* Mobile Menu Button */}
                        <button
                            className="md:hidden p-2 text-muted-foreground"
                            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        >
                            {isMobileMenuOpen ? '✕' : '☰'}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="md:hidden border-t p-4 space-y-2 bg-background">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className="block px-3 py-2 rounded-md text-base font-medium hover:bg-muted"
                            onClick={() => setIsMobileMenuOpen(false)}
                        >
                            {item.label}
                        </Link>
                    ))}
                    <div className="pt-4 border-t mt-2">
                        <Button className="w-full justify-center">Sign In</Button>
                    </div>
                </div>
            )}
        </nav>
    );
}
