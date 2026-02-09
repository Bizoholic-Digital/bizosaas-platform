import Link from "next/link";
import { Check } from "lucide-react";

export default function PricingPage() {
    const plans = [
        {
            name: "Solo",
            description: "For solopreneurs and creators starting their journey.",
            price: "$49",
            period: "/month",
            features: [
                "1 AI Agent",
                "Basic SEO (Site Audit)",
                "Social Media Scheduling (5 posts/mo)",
                "Basic Analytics",
                "Community Support",
            ],
            cta: "Start Free Trial",
            highlight: false,
        },
        {
            name: "Pro",
            description: "For growing businesses tackling multiple channels.",
            price: "$149",
            period: "/month",
            features: [
                "3 AI Agents",
                "Advanced SEO & Keyword Research",
                "Unlimited Social Media Scheduling",
                "Content Generation Engine",
                "Priority Email Support",
                "Includes Premium MCP Modules",
            ],
            cta: "Get Started",
            highlight: true,
        },
        {
            name: "Agency",
            description: "For managing multiple brands or clients.",
            price: "$499",
            period: "/month",
            features: [
                "Unlimited AI Agents",
                "White-label Reports",
                "API Access",
                "Custom Workflows",
                "Dedicated Success Manager",
                "All Premium MCPs Included",
            ],
            cta: "Contact Sales",
            highlight: false,
        },
    ];

    return (
        <div className="flex flex-col min-h-screen py-24">
            <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">

                {/* Header */}
                <div className="text-center mb-16">
                    <h1 className="text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl">
                        Pricing that Scales with You
                    </h1>
                    <p className="mt-4 text-xl text-muted-foreground max-w-2xl mx-auto">
                        Start small with our high-impact AI tools. Upgrade only when you see the ROI.
                        <br />
                        <span className="text-primary font-medium">7-day free trial on all plans.</span>
                    </p>
                </div>

                {/* Pricing Cards */}
                <div className="grid grid-cols-1 gap-8 md:grid-cols-3 mb-24">
                    {plans.map((plan) => (
                        <div
                            key={plan.name}
                            className={`relative flex flex-col p-8 bg-card border rounded-2xl ${plan.highlight
                                    ? "border-primary shadow-2xl scale-105 z-10"
                                    : "border-border shadow-sm"
                                }`}
                        >
                            {plan.highlight && (
                                <div className="absolute top-0 right-0 left-0 -mt-4 text-center">
                                    <span className="inline-block px-4 py-1 text-xs font-semibold tracking-wider text-primary-foreground uppercase bg-primary rounded-full">
                                        Most Popular
                                    </span>
                                </div>
                            )}
                            <div className="mb-6">
                                <h3 className="text-2xl font-bold text-foreground">{plan.name}</h3>
                                <p className="mt-2 text-muted-foreground">{plan.description}</p>
                            </div>
                            <div className="mb-6">
                                <span className="text-4xl font-extrabold text-foreground">{plan.price}</span>
                                <span className="text-muted-foreground">{plan.period}</span>
                            </div>
                            <ul className="space-y-4 mb-8 flex-grow">
                                {plan.features.map((feature) => (
                                    <li key={feature} className="flex items-center text-muted-foreground">
                                        <Check className="w-5 h-5 mr-3 text-primary flex-shrink-0" />
                                        {feature}
                                    </li>
                                ))}
                            </ul>
                            <Link
                                href="/dashboard/register"
                                className={`w-full inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-md transition-colors ${plan.highlight
                                        ? "text-primary-foreground bg-primary hover:bg-primary/90"
                                        : "text-foreground bg-secondary hover:bg-secondary/80"
                                    }`}
                            >
                                {plan.cta}
                            </Link>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
