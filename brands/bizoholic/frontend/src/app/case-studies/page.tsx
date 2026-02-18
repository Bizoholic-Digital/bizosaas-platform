import { NavBar, Hero, Footer, Button } from "@bizosaas/ui";
import { ArrowRight, Star } from "lucide-react";

export default function CaseStudiesPage() {
    const navLinks = [
        { label: "Home", href: "/" },
        { label: "Services", href: "/services" },
        { label: "Blog", href: "/blog" },
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
    ];

    const cases = [
        {
            company: "Luminary SaaS",
            title: "How Luminary Scaled Lead Gen by 300% in 90 Days",
            stat: "300%",
            statDesc: "Increase in MQLs",
            summary: "Luminary was struggling with manual lead scoring. We implemented our AI scoring model and automated follow-ups.",
            category: "SaaS Automation",
            color: "from-blue-500/20"
        },
        {
            company: "EcoStore Direct",
            title: "Reducing CAC for a Multi-Million Dollar E-commerce Brand",
            stat: "42%",
            statDesc: "Reduction in CAC",
            summary: "By leveraging predictive ad targeting, EcoStore optimized their spend across 5 social channels simultaneously.",
            category: "E-commerce",
            color: "from-green-500/20"
        },
        {
            company: "Nexus Financial",
            title: "Ensuring 100% Compliance in Automated Ad Campaigns",
            stat: "No Violations",
            statDesc: "Since Implementation",
            summary: "Nexus required strict regulatory oversight. Our AI compliance agent monitors every piece of text in real-time.",
            category: "FinTech Support",
            color: "from-purple-500/20"
        }
    ];

    return (
        <main className="min-h-screen bg-background">
            <NavBar brandName="Bizoholic" links={navLinks} />

            <Hero
                badge="Customer Success"
                title={
                    <>
                        Real Stories, <span className="text-primary italic">Real Growth</span>
                    </>
                }
                subtitle="See how companies across industries are leveraging Bizoholic to transform their marketing operations and scale exponentially."
                className="pt-32 pb-12"
            />

            <section className="py-24">
                <div className="container px-4 md:px-6">
                    <div className="space-y-12">
                        {cases.map((cs, i) => (
                            <div
                                key={i}
                                className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur-sm transition-all hover:bg-white/10"
                            >
                                <div className={`absolute inset-0 bg-gradient-to-r ${cs.color} to-transparent opacity-0 transition-opacity group-hover:opacity-100`} />

                                <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 items-center p-8 md:p-12 gap-12">
                                    <div className="lg:col-span-3 text-center lg:text-left">
                                        <div className="text-5xl md:text-7xl font-bold text-primary mb-2">{cs.stat}</div>
                                        <div className="text-muted-foreground font-medium uppercase tracking-widest text-sm">{cs.statDesc}</div>
                                    </div>

                                    <div className="lg:col-span-6">
                                        <div className="flex items-center gap-2 text-primary font-bold mb-4">
                                            <Star className="w-4 h-4 fill-current" />
                                            {cs.company}
                                        </div>
                                        <h2 className="text-2xl md:text-3xl font-bold mb-6 group-hover:text-primary transition-colors">
                                            {cs.title}
                                        </h2>
                                        <p className="text-lg text-muted-foreground leading-relaxed mb-8">
                                            {cs.summary}
                                        </p>
                                        <div className="inline-flex items-center rounded-full bg-white/5 border border-white/10 px-4 py-1 text-xs font-medium uppercase tracking-wider">
                                            {cs.category}
                                        </div>
                                    </div>

                                    <div className="lg:col-span-3 flex justify-center lg:justify-end">
                                        <Button variant="ghost" className="group-hover:translate-x-2 transition-transform h-14 rounded-xl text-lg">
                                            Read Full Story <ArrowRight className="ml-2 w-5 h-5" />
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <section className="py-24 border-t border-white/10">
                <div className="container text-center">
                    <h2 className="text-3xl md:text-5xl font-bold mb-12">Trusted by Global Leaders</h2>
                    <div className="flex flex-wrap justify-center gap-12 md:gap-24 grayscale opacity-50 hover:grayscale-0 transition-all duration-700">
                        {/* Using descriptive text placeholders instead of actual images as per rules */}
                        <div className="text-2xl font-black tracking-tighter italic">LUMINARY</div>
                        <div className="text-2xl font-serif">NEXUS</div>
                        <div className="text-2xl font-mono uppercase tracking-[0.5em]">ECOSTORE</div>
                        <div className="text-2xl font-black italic">GLOBAL</div>
                        <div className="text-2xl font-bold tracking-widest">NEXUS</div>
                    </div>
                </div>
            </section>

            <Footer
                brandName="Bizoholic"
                description="Scaling businesses with intelligent AI-powered marketing automation."
                columns={[
                    {
                        title: "Insights",
                        links: [
                            { label: "Case Studies", href: "/case-studies" },
                            { label: "Blog", href: "/blog" },
                            { label: "Whitepapers", href: "/docs" },
                            { label: "Webinars", href: "/events" },
                        ]
                    },
                    {
                        title: "Company",
                        links: [
                            { label: "About Us", href: "/about" },
                            { label: "Services", href: "/services" },
                            { label: "Careers", href: "/careers" },
                            { label: "Contact", href: "/contact" },
                        ]
                    },
                    {
                        title: "Social",
                        links: [
                            { label: "LinkedIn", href: "#" },
                            { label: "Twitter / X", href: "#" },
                            { label: "YouTube", href: "#" },
                        ]
                    }
                ]}
            />
        </main>
    );
}
