import * as React from "react"
import { cn } from "../../lib/utils"
import { Button } from "./button"
import { ArrowRight } from "lucide-react"

interface CTAProps extends React.HTMLAttributes<HTMLElement> {
    title: string
    subtitle: string
    primaryCtaText: string
    primaryCtaLink?: string
    rating?: number
    reviewCount?: string
}

export const CtaSection = React.forwardRef<HTMLElement, CTAProps>(
    ({ className, title, subtitle, primaryCtaText, primaryCtaLink, rating = 5, reviewCount, ...props }, ref) => {
        return (
            <section
                ref={ref}
                className={cn(
                    "py-24",
                    className
                )}
                {...props}
            >
                <div className="container">
                    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary/20 via-background to-secondary/20 border border-white/10 px-6 py-16 md:px-16 md:py-24 text-center">

                        {/* Glows */}
                        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-white/5 via-transparent to-transparent opacity-50 pointer-events-none" />

                        <div className="relative z-10 max-w-3xl mx-auto">
                            <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-white mb-6">
                                {title}
                            </h2>
                            <p className="text-lg md:text-xl text-muted-foreground mb-10">
                                {subtitle}
                            </p>

                            {rating && (
                                <div className="flex flex-col items-center gap-2 mb-8">
                                    <div className="flex gap-1 text-yellow-400">
                                        {[...Array(5)].map((_, i) => (
                                            <svg key={i} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={cn("w-5 h-5", i < Math.floor(rating) ? "text-yellow-400" : "text-gray-600")}>
                                                <path fillRule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z" clipRule="evenodd" />
                                            </svg>
                                        ))}
                                    </div>
                                    {reviewCount && (
                                        <p className="text-sm text-muted-foreground">{rating}/5 from {reviewCount}+ reviews</p>
                                    )}
                                </div>
                            )}

                            <Button size="lg" className="h-14 px-8 rounded-full text-lg shadow-xl shadow-primary/20 hover:scale-105 transition-transform">
                                {primaryCtaText} <ArrowRight className="ml-2 h-5 w-5" />
                            </Button>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
)
CtaSection.displayName = "CtaSection"
