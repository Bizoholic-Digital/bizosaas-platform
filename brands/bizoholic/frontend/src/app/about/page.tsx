import { NavBar, Hero, Footer, CtaSection } from "@bizosaas/ui";
import { Users, Lightbulb, Target, Rocket } from "lucide-react";

export default function AboutPage() {
    const navLinks = [
        { label: "Home", href: "/" },
        { label: "Services", href: "/services" },
        { label: "Blog", href: "/blog" },
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
    ];

    const values = [
        {
            title: "Innovation First",
            description: "We constantly push the boundaries of what's possible with AI to keep our clients ahead of the curve.",
            icon: <Lightbulb className="w-8 h-8 text-primary" />
        },
        {
            title: "Customer Centric",
            description: "Our solutions are built with the end-user in mind, ensuring meaningful engagement and lasting relationships.",
            icon: <Users className="w-8 h-8 text-primary" />
        },
        {
            title: "Integrity & Transparency",
            description: "We believe in honest partnerships and clear communication about data, algorithms, and results.",
            icon: <Target className="w-8 h-8 text-primary" />
        },
        {
            title: "Accelerated Growth",
            description: "Our focus is always on delivering measurable ROI and scaling your business profitably.",
            icon: <Rocket className="w-8 h-8 text-primary" />
        }
    ];

    return (
        <main className="min-h-screen bg-background">
            <NavBar brandName="Bizoholic" links={navLinks} />

            <Hero
                badge="About Bizoholic"
                title={
                    <>
                        Pioneering the <span className="text-primary italic">Autonomous</span> Marketing Era
                    </>
                }
                subtitle="We help forward-thinking companies harness the power of artificial intelligence to automate complexity and unlock exponential growth."
                className="pt-32 pb-12"
            />

            <section className="py-24 bg-background">
                <div className="container px-4 md:px-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-32">
                        <div>
                            <h2 className="text-3xl md:text-4xl font-bold mb-6">Our Mission</h2>
                            <p className="text-lg text-muted-foreground mb-6 leading-relaxed">
                                At Bizoholic, we believe that the future of marketing isn't just about more data—it's about better intelligence. Our mission is to democratize high-end AI marketing tools, making them accessible to businesses of all sizes who want to scale without scaling their workload.
                            </p>
                            <p className="text-lg text-muted-foreground leading-relaxed">
                                Founded in 2024, our team of AI researchers, design-obsessed marketers, and data scientists have come together to build a platform that doesn't just suggest actions—it executes them autonomously.
                            </p>
                        </div>
                        <div className="relative">
                            <div className="aspect-square rounded-2xl bg-gradient-to-br from-primary/20 to-secondary/20 border border-white/10 flex items-center justify-center overflow-hidden">
                                <div className="w-48 h-48 bg-primary/20 blur-[80px] rounded-full absolute" />
                                <Target className="w-32 h-32 text-primary relative z-10" />
                            </div>
                        </div>
                    </div>

                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Core Values</h2>
                        <p className="text-muted-foreground text-lg max-w-2xl mx-auto">The principles that guide our product, our culture, and our commitment to your success.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {values.map((v, i) => (
                            <div key={i} className="p-8 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm transition-all hover:bg-white/10 hover:border-primary/50 text-center flex flex-col items-center">
                                <div className="mb-6 p-4 rounded-xl bg-primary/10">
                                    {v.icon}
                                </div>
                                <h3 className="text-xl font-bold mb-3">{v.title}</h3>
                                <p className="text-muted-foreground">{v.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <CtaSection
                title="Be Part of the Future"
                subtitle="Join the 500+ businesses who have already automated their marketing journey with Bizoholic."
                primaryCtaText="Join Our Team"
                primaryCtaLink="/careers"
            />

            <Footer
                brandName="Bizoholic"
                description="Scaling businesses with intelligent AI-powered marketing automation."
                columns={[
                    {
                        title: "Company",
                        links: [
                            { label: "Our Story", href: "/about" },
                            { label: "Services", href: "/services" },
                            { label: "Blog", href: "/blog" },
                            { label: "Careers", href: "/careers" },
                        ]
                    },
                    {
                        title: "Resources",
                        links: [
                            { label: "Documentation", href: "/docs" },
                            { label: "Case Studies", href: "/case-studies" },
                            { label: "Status Page", href: "/status" },
                            { label: "Help Center", href: "/help" },
                        ]
                    },
                    {
                        title: "Legal",
                        links: [
                            { label: "Privacy Policy", href: "/privacy" },
                            { label: "Terms of Service", href: "/terms" },
                        ]
                    }
                ]}
            />
        </main>
    );
}
