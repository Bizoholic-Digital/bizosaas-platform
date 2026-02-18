import * as React from "react"
import { cn } from "../../lib/utils"
import Link from "next/link"

interface FooterLink {
    label: string
    href: string
}

interface FooterColumn {
    title: string
    links: FooterLink[]
}

interface FooterProps extends React.HTMLAttributes<HTMLElement> {
    brandName?: string
    description?: string
    columns?: FooterColumn[]
    copyright?: string
}

export const Footer = React.forwardRef<HTMLElement, FooterProps>(
    ({ className, brandName = "Brand", description, columns = [], copyright, ...props }, ref) => {
        return (
            <footer
                ref={ref}
                className={cn(
                    "bg-background border-t border-white/10 py-16 md:py-24",
                    className
                )}
                {...props}
            >
                <div className="container">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12 lg:gap-8 mb-16">

                        {/* Brand Column */}
                        <div className="lg:col-span-2">
                            <Link href="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent mb-6 inline-block">
                                {brandName}
                            </Link>
                            {description && (
                                <p className="text-muted-foreground max-w-sm text-lg leading-relaxed">
                                    {description}
                                </p>
                            )}
                        </div>

                        {/* Link Columns */}
                        {columns.map((column) => (
                            <div key={column.title}>
                                <h4 className="font-semibold text-foreground mb-6">{column.title}</h4>
                                <ul className="space-y-4">
                                    {column.links.map((link) => (
                                        <li key={link.href}>
                                            <Link
                                                href={link.href}
                                                className="text-muted-foreground hover:text-primary transition-colors block"
                                            >
                                                {link.label}
                                            </Link>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>

                    <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
                        <p className="text-muted-foreground text-sm">
                            {copyright || `© ${new Date().getFullYear()} ${brandName}. All rights reserved.`}
                        </p>
                        <div className="flex gap-6 text-sm text-muted-foreground">
                            <Link href="/privacy" className="hover:text-foreground transition-colors">Privacy Policy</Link>
                            <Link href="/terms" className="hover:text-foreground transition-colors">Terms of Service</Link>
                            <Link href="/status" className="hover:text-foreground transition-colors">Status</Link>
                        </div>
                    </div>
                </div>
            </footer>
        )
    }
)
Footer.displayName = "Footer"
