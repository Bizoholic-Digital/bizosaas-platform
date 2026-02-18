import * as React from "react"
import { cn } from "../../lib/utils"
// import Image from "next/image" // Assumed available or handled via prop
import Link from "next/link"
import { ArrowUpRight } from "lucide-react"

interface BlogCardProps extends React.HTMLAttributes<HTMLDivElement> {
    className?: string
    title: string
    excerpt: string
    category: string
    author?: string
    date?: string
    readTime?: string
    imageSrc?: string
    href: string
}

export const BlogCard = React.forwardRef<HTMLDivElement, BlogCardProps>(
    ({ className, title, excerpt, category, author, date, readTime, imageSrc, href, ...props }: BlogCardProps, ref: React.ForwardedRef<HTMLDivElement>) => {
        return (
            <Link href={href} className="group block h-full">
                <article
                    ref={ref}
                    className={cn(
                        "h-full flex flex-col overflow-hidden rounded-2xl bg-card border border-border/50 transition-all hover:bg-card/80 hover:border-primary/50 hover:shadow-lg",
                        className
                    )}
                    {...props}
                >
                    {imageSrc ? (
                        <div className="aspect-[16/9] w-full bg-muted overflow-hidden">
                            {/* Placeholder for image - in real usage, pass Image component or img tag */}
                            <div className="w-full h-full bg-muted-foreground/10 group-hover:scale-105 transition-transform duration-500" />
                        </div>
                    ) : (
                        <div className="p-6 pb-0 flex items-start justify-between">
                            <span className="inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary ring-1 ring-inset ring-primary/20">
                                {category}
                            </span>
                            {readTime && <span className="text-xs text-muted-foreground">{readTime} read</span>}
                        </div>
                    )}

                    <div className="flex flex-1 flex-col p-6">
                        <h3 className="mt-2 text-xl font-bold leading-snug text-foreground group-hover:text-primary transition-colors">
                            {title}
                        </h3>
                        <p className="mt-4 flex-1 text-muted-foreground text-sm leading-relaxed line-clamp-3">
                            {excerpt}
                        </p>

                        <div className="mt-8 flex items-center justify-between gap-4 border-t border-border pt-4 text-xs text-muted-foreground">
                            <div className="flex items-center gap-2">
                                {author && <span className="font-medium text-foreground">{author}</span>}
                                {date && <span>• {date}</span>}
                            </div>
                            <ArrowUpRight className="h-4 w-4 transition-transform group-hover:translate-x-1 group-hover:-translate-y-1 text-primary" />
                        </div>
                    </div>
                </article>
            </Link>
        )
    }
)
BlogCard.displayName = "BlogCard"
