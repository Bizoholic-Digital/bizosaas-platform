'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export function Footer() {
    return (
        <footer className="bg-muted/30 border-t">
            <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">

                    {/* Brand Column */}
                    <div className="col-span-1 md:col-span-1">
                        <Link href="/" className="flex items-center gap-2 font-bold text-xl mb-4">
                            <span className="text-2xl">⚡</span>
                            <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-500 to-pink-500">ThrillRing</span>
                        </Link>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                            The ultimate destination for competitive gaming. Join tournaments, climb leaderboards, and build your legacy.
                        </p>
                        <div className="flex gap-4 mt-6">
                            {/* Social Icons Placeholder */}
                            <a href="#" className="text-muted-foreground hover:text-foreground">🐦</a>
                            <a href="#" className="text-muted-foreground hover:text-foreground">👾</a> {/* Discord */}
                            <a href="#" className="text-muted-foreground hover:text-foreground">📺</a> {/* Twitch */}
                            <a href="#" className="text-muted-foreground hover:text-foreground">▶️</a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h3 className="font-semibold mb-4">Platform</h3>
                        <ul className="space-y-3 text-sm text-muted-foreground">
                            <li><Link href="/games" className="hover:text-primary">Browse Games</Link></li>
                            <li><Link href="/tournaments" className="hover:text-primary">Tournaments</Link></li>
                            <li><Link href="/leaderboard" className="hover:text-primary">Leaderboards</Link></li>
                            <li><Link href="/news" className="hover:text-primary">Gaming News</Link></li>
                        </ul>
                    </div>

                    {/* Resources */}
                    <div>
                        <h3 className="font-semibold mb-4">Resources</h3>
                        <ul className="space-y-3 text-sm text-muted-foreground">
                            <li><Link href="/about" className="hover:text-primary">About Us</Link></li>
                            <li><Link href="/support" className="hover:text-primary">Support Center</Link></li>
                            <li><Link href="/partners" className="hover:text-primary">Become a Partner</Link></li>
                            <li><Link href="/api" className="hover:text-primary">Developer API</Link></li>
                        </ul>
                    </div>

                    {/* Newsletter */}
                    <div>
                        <h3 className="font-semibold mb-4">Stay  Updated</h3>
                        <p className="text-sm text-muted-foreground mb-4">Subscribe to get tournament alerts and gaming news.</p>
                        <div className="flex gap-2">
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className="flex-1 min-w-0 h-9 rounded-md border bg-background px-3 text-sm outline-none focus:ring-1 focus:ring-primary"
                            />
                            <Button size="sm">Subscribe</Button>
                        </div>
                    </div>
                </div>

                <div className="border-t pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-muted-foreground">
                    <p>&copy; {new Date().getFullYear()} ThrillRing Gaming. All rights reserved.</p>
                    <div className="flex gap-6">
                        <Link href="/privacy" className="hover:text-foreground">Privacy Policy</Link>
                        <Link href="/terms" className="hover:text-foreground">Terms of Service</Link>
                        <Link href="/cookies" className="hover:text-foreground">Cookie Policy</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
}
