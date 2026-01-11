'use client'

import { Bell, Search, Menu } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useAuth } from '@/components/auth/AuthProvider'

import { ThemeToggle } from '@/components/theme-toggle'

export function Header() {
    const { user, logout } = useAuth()

    return (
        <header className="flex h-16 items-center justify-between border-b bg-white px-6 dark:bg-slate-950 dark:border-slate-800">
            {/* Mobile Menu Trigger (Hidden on Desktop) */}
            <Button variant="ghost" size="icon" className="md:hidden mr-4">
                <Menu className="h-5 w-5" />
            </Button>

            {/* Search */}
            <div className="flex flex-1 items-center max-w-md">
                <div className="relative w-full">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        type="search"
                        placeholder="Search..."
                        className="w-full bg-slate-50 pl-9 dark:bg-slate-900"
                    />
                </div>
            </div>

            {/* Right Actions */}
            <div className="flex items-center gap-4">
                {/* Impersonation Indicator */}
                {typeof window !== 'undefined' && localStorage.getItem('impersonation_token') && (
                    <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400 rounded-full text-xs font-semibold border border-amber-200 dark:border-amber-800">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
                        </span>
                        Viewing as User
                        <Button
                            variant="ghost"
                            size="sm"
                            className="h-4 p-0 ml-2 text-amber-900 hover:text-amber-950 dark:text-amber-300 dark:hover:text-amber-200 font-bold"
                            onClick={() => {
                                localStorage.removeItem('impersonation_token');
                                window.location.href = '/dashboard';
                            }}
                        >
                            Exit
                        </Button>
                    </div>
                )}

                <ThemeToggle />

                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="relative">
                            <Bell className="h-5 w-5" />
                            <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-red-600" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-80">
                        <DropdownMenuLabel>Notifications</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <div className="max-h-[300px] overflow-y-auto">
                            <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                                <div className="flex w-full items-center justify-between font-semibold">
                                    <span>Campaign Ready</span>
                                    <span className="text-[10px] text-muted-foreground">2m ago</span>
                                </div>
                                <p className="text-xs text-muted-foreground">Your "Summer Sale" campaign is ready for review.</p>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                                <div className="flex w-full items-center justify-between font-semibold">
                                    <span>New Lead</span>
                                    <span className="text-[10px] text-muted-foreground">1h ago</span>
                                </div>
                                <p className="text-xs text-muted-foreground">A new lead joined through your landing page.</p>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem className="flex flex-col items-start gap-1 p-4 cursor-pointer">
                                <div className="flex w-full items-center justify-between font-semibold">
                                    <span>System Update</span>
                                    <span className="text-[10px] text-muted-foreground">5h ago</span>
                                </div>
                                <p className="text-xs text-muted-foreground">BizOS v5.1 has been deployed with new AI features.</p>
                            </DropdownMenuItem>
                        </div>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="w-full text-center justify-center font-semibold text-blue-600">
                            Clear all notifications
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>

                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                            <div className="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center">
                                {user?.name?.[0] || 'U'}
                            </div>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent className="w-56" align="end" forceMount>
                        <DropdownMenuLabel className="font-normal">
                            <div className="flex flex-col space-y-1">
                                <p className="text-sm font-medium leading-none">{user?.name}</p>
                                <p className="text-xs leading-none text-muted-foreground">
                                    {user?.email}
                                </p>
                            </div>
                        </DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>Profile</DropdownMenuItem>
                        <DropdownMenuItem>Billing</DropdownMenuItem>
                        <DropdownMenuItem>Settings</DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem onClick={() => logout()}>
                            Log out
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
        </header>
    )
}
