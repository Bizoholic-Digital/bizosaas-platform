import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Check, Globe, Rocket, Server } from "lucide-react"

const hostingPlans = [
    {
        name: "Premium Web Hosting",
        provider: "Hostinger",
        price: "$2.99",
        period: "/mo",
        description: "Everything you need to create your website.",
        features: [
            "Unmetered Traffic",
            "100 Websites",
            "100 GB SSD Storage",
            "Free Weekly Backups",
            "Unlimited Free SSL",
            "Free Domain"
        ],
        recommended: true,
        link: "https://hostinger.com" // Placeholder
    },
    {
        name: "Business Web Hosting",
        provider: "Hostinger",
        price: "$3.99",
        period: "/mo",
        description: "Level up with more power and enhanced features.",
        features: [
            "Increased Performance (5x)",
            "200 GB NVMe Storage",
            "Daily Backups",
            "Free CDN",
            "Dedicated IP Address"
        ],
        recommended: false,
        link: "https://hostinger.com" // Placeholder
    }
]

export default function GetWebsitePage() {
    return (
        <div className="space-y-6">
            <div className="text-center max-w-2xl mx-auto mb-10">
                <h2 className="text-3xl font-bold tracking-tight mb-2">Get Your Business Online</h2>
                <p className="text-muted-foreground">
                    Launch your professional website in minutes with our trusted partners.
                    We've negotiated the best rates for you.
                </p>
            </div>

            <div className="grid gap-8 md:grid-cols-2 max-w-4xl mx-auto">
                {hostingPlans.map((plan) => (
                    <Card key={plan.name} className={`flex flex-col ${plan.recommended ? 'border-blue-600 shadow-lg relative' : ''}`}>
                        {plan.recommended && (
                            <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                                <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">
                                    Most Popular
                                </span>
                            </div>
                        )}
                        <CardHeader>
                            <div className="text-sm font-medium text-muted-foreground mb-1">{plan.provider}</div>
                            <CardTitle className="text-2xl">{plan.name}</CardTitle>
                            <CardDescription>{plan.description}</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1">
                            <div className="mb-6">
                                <span className="text-4xl font-bold">{plan.price}</span>
                                <span className="text-muted-foreground">{plan.period}</span>
                            </div>
                            <ul className="space-y-3">
                                {plan.features.map((feature) => (
                                    <li key={feature} className="flex items-center">
                                        <Check className="mr-2 h-4 w-4 text-green-500" />
                                        <span className="text-sm">{feature}</span>
                                    </li>
                                ))}
                            </ul>
                        </CardContent>
                        <CardFooter>
                            <Button className="w-full" size="lg" variant={plan.recommended ? 'default' : 'outline'} asChild>
                                <a href={plan.link} target="_blank" rel="noopener noreferrer">
                                    Select Plan
                                </a>
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

            <div className="mt-12 grid gap-6 md:grid-cols-3 text-center">
                <div className="p-6 bg-slate-50 rounded-lg dark:bg-slate-900">
                    <div className="mx-auto w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-4 dark:bg-blue-900 dark:text-blue-300">
                        <Rocket className="h-6 w-6" />
                    </div>
                    <h3 className="font-semibold mb-2">Fast Setup</h3>
                    <p className="text-sm text-muted-foreground">Get your WordPress site up and running in under 5 minutes.</p>
                </div>
                <div className="p-6 bg-slate-50 rounded-lg dark:bg-slate-900">
                    <div className="mx-auto w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-4 dark:bg-green-900 dark:text-green-300">
                        <Server className="h-6 w-6" />
                    </div>
                    <h3 className="font-semibold mb-2">Reliable Hosting</h3>
                    <p className="text-sm text-muted-foreground">99.9% uptime guarantee ensuring your business is always open.</p>
                </div>
                <div className="p-6 bg-slate-50 rounded-lg dark:bg-slate-900">
                    <div className="mx-auto w-12 h-12 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mb-4 dark:bg-purple-900 dark:text-purple-300">
                        <Globe className="h-6 w-6" />
                    </div>
                    <h3 className="font-semibold mb-2">Free Domain</h3>
                    <p className="text-sm text-muted-foreground">Claim your unique professional domain name for free.</p>
                </div>
            </div>
        </div>
    )
}
