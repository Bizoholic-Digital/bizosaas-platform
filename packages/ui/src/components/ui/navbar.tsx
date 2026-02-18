"use client"

import * as React from "react"
import { cn } from "../../lib/utils"
import { Button } from "./button"
import Link from "next/link"

interface NavLink {
    label: string
    href: string
}

interface NavBarProps extends React.HTMLAttributes<HTMLElement> {
    className?: string
    brandName?: string
    logo?: React.ReactNode
    links?: NavLink[]
    actions?: React.ReactNode
    sticky?: boolean
}

export const NavBar = React.forwardRef<HTMLElement, NavBarProps>(
    ({ className, brandName = "Brand", logo, links = [] as NavLink[], actions, sticky = true, ...props }: NavBarProps, ref: React.ForwardedRef<HTMLElement>) => {
        const [scrolled, setScrolled] = React.useState(false)
        const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)

        React.useEffect(() => {
            const handleScroll = () => {
                setScrolled(window.scrollY > 20)
            }
            window.addEventListener("scroll", handleScroll)
            return () => window.removeEventListener("scroll", handleScroll)
        }, [])

        return (
            <header
                ref={ref}
                className={cn(
                    "fixed top-0 left-0 right-0 z-50 transition-all duration-300 w-full border-b",
                    scrolled
                        ? "border-white/10 bg-background/80 backdrop-blur-md py-3 shadow-lg"
                        : "border-transparent bg-transparent py-5",
                    !sticky && "relative",
                    className
                )}
                {...props}
            >
                <div className="container flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-2 font-bold text-xl tracking-tight hover:opacity-90 transition-opacity">
                        {logo}
                        <span className={cn("text-foreground", scrolled ? "" : "text-white")}>{brandName}</span>
                    </Link>

                    {/* Desktop Menu */}
                    <nav className="hidden md:flex items-center gap-8">
                        {links.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={cn(
                                    "text-sm font-medium transition-colors hover:text-primary",
                                    scrolled ? "text-muted-foreground" : "text-white/80 hover:text-white"
                                )}
                            >
                                {link.label}
                            </Link>
                        ))}
                    </nav>

                    {/* Desktop Actions */}
                    <div className="hidden md:flex items-center gap-4">
                        {actions || (
                            <>
                                <Button variant="ghost" className={scrolled ? "" : "text-white hover:bg-white/10 hover:text-white"}>
                                    Log in
                                </Button>
                                <Button variant="default" className="font-semibold">
                                    Get Started
                                </Button>
                            </>
                        )}
                    </div>

                    {/* Mobile Menu Button */}
                    <Button
                        variant="ghost"
                        size="icon"
                        className="md:hidden text-foreground"
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                    >
                        {mobileMenuOpen ? (
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18" /><path d="m6 6 12 12" /></svg>
                        ) : (
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12" /><line x1="4" x2="20" y1="6" y2="6" /><line x1="4" x2="20" y1="18" y2="18" /></svg>
                        )}
                        <span className="sr-only">Toggle menu</span>
                    </Button>
                </div>

                {/* Mobile Menu Overlay */}
                {mobileMenuOpen && (
                    <div className="md:hidden absolute top-full left-0 right-0 bg-background border-b border-border p-4 shadow-xl animate-in slide-in-from-top-2">
                        <nav className="flex flex-col gap-4">
                            {links.map((link) => (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    className="text-lg font-medium py-2 px-4 hover:bg-muted rounded-md transition-colors"
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    {link.label}
                                </Link>
                            ))}
                            <div className="h-px bg-border my-2" />
                            <div className="flex flex-col gap-3 p-2">
                                {/* Mobile Actions - duplicating or using actions prop if flexible */}
                                {actions ? (
                                    <div className="flex flex-col gap-3">{actions}</div>
                                ) : (
                                    <>
                                        <Button variant="outline" className="w-full justify-start">Log in</Button>
                                        <Button className="w-full">Get Started</Button>
                                    </>
                                )}
                            </div>
                        </nav>
                    </div>
                )}
            </header>
        )
    }
)
NavBar.displayName = "NavBar"
