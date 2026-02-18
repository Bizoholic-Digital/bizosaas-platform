import * as React from "react"
import { cn } from "../../lib/utils"
import { Button } from "./button"
import { ArrowRight, CheckCircle2 } from "lucide-react"

interface HeroProps extends Omit<React.HTMLAttributes<HTMLDivElement>, "title"> {
    badge?: string
    title: React.ReactNode
    subtitle: string
    primaryCtaText?: string
    primaryCtaLink?: string
    secondaryCtaText?: string
    secondaryCtaLink?: string
    trustText?: string
    image?: React.ReactNode
}

export const Hero = React.forwardRef<HTMLDivElement, HeroProps>(
    ({ className, badge, title, subtitle, primaryCtaText, primaryCtaLink, secondaryCtaText, secondaryCtaLink, trustText, image, ...props }: HeroProps, ref: React.ForwardedRef<HTMLDivElement>) => {
        return (
            <section
                ref={ref}
                className={cn(
                    "relative pt-32 pb-16 md:pt-48 md:pb-32 overflow-hidden",
                    className
                )}
                {...props}
            >
                {/* Background Gradients */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-primary/20 blur-[120px] rounded-full opacity-50 pointer-events-none" />
                <div className="absolute bottom-0 right-0 w-[300px] h-[300px] bg-secondary/20 blur-[100px] rounded-full opacity-30 pointer-events-none" />

                <div className="container relative z-10 flex flex-col items-center text-center">

                    {badge && (
                        <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-8 animate-fade-in backdrop-blur-sm">
                            <span className="flex h-2 w-2 rounded-full bg-primary mr-2 animate-pulse"></span>
                            {badge}
                        </div>
                    )}

                    <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight text-foreground mb-6 max-w-4xl animate-slide-up">
                        {title}
                    </h1>

                    <p className="text-xl text-muted-foreground mb-10 max-w-2xl animate-slide-up [animation-delay:100ms]">
                        {subtitle}
                    </p>

                    <div className="flex flex-col sm:flex-row items-center gap-4 animate-slide-up [animation-delay:200ms]">
                        {primaryCtaText && (
                            <Button size="lg" className="min-w-[160px] text-lg h-14 rounded-full shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all hover:scale-105">
                                {primaryCtaText} <ArrowRight className="ml-2 h-5 w-5" />
                            </Button>
                        )}

                        {secondaryCtaText && (
                            <Button variant="outline" size="lg" className="min-w-[160px] text-lg h-14 rounded-full border-white/10 bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-all hover:scale-105">
                                {secondaryCtaText}
                            </Button>
                        )}
                    </div>

                    {trustText && (
                        <div className="mt-8 flex items-center gap-6 text-sm text-muted-foreground animate-fade-in [animation-delay:400ms]">
                            <div className="flex items-center">
                                <CheckCircle2 className="mr-2 h-4 w-4 text-green-500" />
                                No Credit Card Required
                            </div>
                            <div className="flex items-center">
                                <CheckCircle2 className="mr-2 h-4 w-4 text-green-500" />
                                14-Day Free Trial
                            </div>
                            <div className="flex items-center">
                                <CheckCircle2 className="mr-2 h-4 w-4 text-green-500" />
                                Cancel Anytime
                            </div>
                        </div>
                    )}

                    {image && (
                        <div className="mt-16 md:mt-24 w-full max-w-6xl mx-auto rounded-xl border border-white/10 bg-white/5 p-2 shadow-2xl backdrop-blur-sm animate-scale-in [animation-delay:300ms]">
                            <div className="rounded-lg overflow-hidden bg-background/50 aspect-video relative">
                                {image}
                            </div>
                        </div>
                    )}

                </div>
            </section>
        )
    }
)
Hero.displayName = "Hero"
