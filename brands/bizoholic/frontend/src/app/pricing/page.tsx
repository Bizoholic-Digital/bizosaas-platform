import { NavBar, Footer, Button, CtaSection } from "@bizosaas/ui";
import { Check, Zap, Rocket, Building2 } from "lucide-react";

export default function PricingPage() {
    const navLinks = [
        { label: "Home", href: "/" },
        { label: "Services", href: "/services" },
        { label: "Blog", href: "/blog" },
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
    ];

    const tiers = [
        {
            name: "Starter",
            description: "Perfect for micro-businesses looking to automate basics.",
            price: "$49",
            features: [
                "Up to 1,000 Contacts",
                "AI Content Assistant (Basic)",
                "3 Automated Workflows",
                "Email & SMS Support",
                "Standard Analytics Dashboard"
            ],
            icon: <Zap className="w-8 h-8 text-primary" />,
            buttonText: "Get Started",
            highlight: false
        },
        {
            name: "Pro",
            description: "Best for growing companies that need scale.",
            price: "$149",
            features: [
                "Up to 10,000 Contacts",
                "AI Agent (Full Access)",
                "Unlimited Workflows",
                "Priority 24/7 Support",
                "Advanced Predictive Insights",
                "Custom Branding Support"
            ],
            icon: <Rocket className="w-8 h-8 text-primary" />,
            buttonText: "Start Free Trial",
            highlight: true
        },
        {
            name: "Enterprise",
            description: "Custom solutions for large-scale operations.",
            price: "Custom",
            features: [
                "Unlimited Contacts",
                "Dedicated Account Manager",
                "On-Premise Deployment Option",
                "Custom AI Model Training",
                "SLA Guarantee",
                "SSO & Advanced Security"
            ],
            icon: <Building2 className="w-8 h-8 text-primary" />,
            buttonText: "Contact Sales",
            highlight: false
        }
    ];

    return (
        <main className="min-h-screen bg-background text-foreground">
            <NavBar brandName="Bizoholic" links={navLinks} />

            <section className="pt-48 pb-24 text-center">
                <div className="container px-4 md:px-6">
                    <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-8 animate-fade-in backdrop-blur-sm">
                        Simple, Transparent Pricing
                    </div>
                    <h1 className="text-4xl md:text-7xl font-bold mb-6 tracking-tight">
                        Scale Your Profits, <br />
                        <span className="text-primary italic">Not Your Costs</span>
                    </h1>
                    <p className="text-xl text-muted-foreground mb-16 max-w-2xl mx-auto leading-relaxed">
                        Choose the plan that fits your current needs and scale automatically as you grow. No hidden fees, ever.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-24 items-stretch">
                        {tiers.map((tier, i) => (
                            <div
                                key={i}
                                className={`flex flex-col p-8 rounded-3xl border transition-all duration-300 hover:-translate-y-2 ${tier.highlight
                                        ? "bg-gradient-to-br from-primary/10 via-background to-secondary/10 border-primary shadow-2xl shadow-primary/20 relative scale-105 z-10"
                                        : "bg-white/5 border-white/10 hover:bg-white/10"
                                    }`}
                            >
                                {tier.highlight && (
                                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground text-xs font-bold px-4 py-1 rounded-full uppercase tracking-widest">
                                        Most Popular
                                    </div>
                                )}

                                <div className="mb-8 p-4 rounded-2xl bg-primary/10 w-fit">
                                    {tier.icon}
                                </div>

                                <h3 className="text-2xl font-bold mb-2">{tier.name}</h3>
                                <p className="text-muted-foreground text-sm mb-6 flex-grow">{tier.description}</p>

                                <div className="mb-8">
                                    <span className="text-4xl font-bold">{tier.price}</span>
                                    {tier.price !== "Custom" && <span className="text-muted-foreground">/mo</span>}
                                </div>

                                <ul className="space-y-4 mb-8 text-left">
                                    {tier.features.map((feature, index) => (
                                        <li key={index} className="flex items-center gap-3 text-sm">
                                            <div className="flex-shrink-0 w-5 h-5 rounded-full bg-green-500/10 flex items-center justify-center text-green-500">
                                                <Check className="w-3 h-3" />
                                            </div>
                                            {feature}
                                        </li>
                                    ))}
                                </ul>

                                <Button
                                    variant={tier.highlight ? "default" : "outline"}
                                    className={`w-full h-14 rounded-xl text-lg mt-auto ${tier.highlight ? "shadow-lg shadow-primary/20" : ""}`}
                                >
                                    {tier.buttonText}
                                </Button>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <CtaSection
                title="Still Have Questions?"
                subtitle="Our team is ready to help you find the perfect plan for your business needs."
                primaryCtaText="Chat with Support"
                primaryCtaLink="/contact"
            />

            <Footer
                brandName="Bizoholic"
                description="Scaling businesses with intelligent AI-powered marketing automation."
                columns={[
                    {
                        title: "Plans",
                        links: [
                            { label: "Starter", href: "/pricing" },
                            { label: "Pro", href: "/pricing" },
                            { label: "Enterprise", href: "/pricing" },
                            { label: "Custom Quotes", href: "/contact" },
                        ]
                    },
                    {
                        title: "Company",
                        links: [
                            { label: "About Us", href: "/about" },
                            { label: "Services", href: "/services" },
                            { label: "Blog", href: "/blog" },
                            { label: "Careers", href: "/careers" },
                        ]
                    },
                    {
                        title: "Support",
                        links: [
                            { label: "FAQ", href: "/faq" },
                            { label: "Docs", href: "/docs" },
                            { label: "Privacy", href: "/privacy" },
                            { label: "Terms", href: "/terms" },
                        ]
                    }
                ]}
            />
        </main>
    );
}
