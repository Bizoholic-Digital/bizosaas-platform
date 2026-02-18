import * as React from "react"
import { cn } from "../../lib/utils"
import { Button } from "./button"
import { ArrowRight } from "lucide-react"

interface ServiceCardProps extends React.HTMLAttributes<HTMLDivElement> {
    className?: string
    title: string
    description: string
    icon?: React.ReactNode
    link?: string
    linkText?: string
}

export const ServiceCard = React.forwardRef<HTMLDivElement, ServiceCardProps>(
    ({ className, title, description, icon, link, linkText = "Learn More", ...props }: ServiceCardProps, ref: React.ForwardedRef<HTMLDivElement>) => {
        return (
            <div
                ref={ref}
                className={cn(
                    "group relative overflow-hidden rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm transition-all hover:bg-white/10 hover:shadow-2xl hover:shadow-primary/20",
                    className
                )}
                {...props}
            >
                <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-transparent opacity-0 transition-opacity group-hover:opacity-100" />

                <div className="relative z-10 flex flex-col h-full">
                    {icon && (
                        <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-primary/20 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                            {icon}
                        </div>
                    )}

                    <h3 className="mb-2 text-xl font-semibold tracking-tight text-foreground transition-colors group-hover:text-primary">
                        {title}
                    </h3>

                    <p className="mb-6 text-muted-foreground flex-grow">
                        {description}
                    </p>

                    {link && (
                        <div className="mt-auto">
                            <Button
                                variant="link"
                                className="p-0 h-auto font-semibold text-primary group-hover:text-primary-foreground transition-colors group-hover:translate-x-1 duration-300"
                            >
                                {linkText} <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </div>
                    )}
                </div>
            </div>
        )
    }
)
ServiceCard.displayName = "ServiceCard"
