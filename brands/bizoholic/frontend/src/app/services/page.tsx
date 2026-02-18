import { NavBar, Hero, ServiceCard, Footer, CtaSection } from "@bizosaas/ui";
import {
    Bot,
    BarChart3,
    Target,
    Zap,
    MessageSquare,
    Globe,
    Search,
    Mail,
    ShieldCheck
} from "lucide-react";

export default function ServicesPage() {
    const navLinks = [
        { label: "Home", href: "/" },
        { label: "Services", href: "/services" },
        { label: "Blog", href: "/blog" },
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
    ];

    const services = [
        {
            title: "AI Marketing Strategy",
            description: "Data-driven marketing blueprints powered by advanced AI to identify growth opportunities and optimize your ROI.",
            icon: <Target className="w-6 h-6" />,
            link: "/services/strategy"
        },
        {
            title: "Automated Content Creation",
            description: "Scale your content production without sacrificing quality. Our AI generates SEO-optimized articles, social posts, and ad copy.",
            icon: <Bot className="w-6 h-6" />,
            link: "/services/content"
        },
        {
            title: "Predictive Analytics",
            description: "Anticipate customer behavior and market trends with high-precision forecasting models built into your dashboard.",
            icon: <BarChart3 className="w-6 h-6" />,
            link: "/services/analytics"
        },
        {
            title: "Omnichannel Automation",
            description: "Sync your marketing efforts across email, SMS, and social media with intelligent workflows that adapt in real-time.",
            icon: <Zap className="w-6 h-6" />,
            link: "/services/automation"
        },
        {
            title: "AI Chatbots & Support",
            description: "24/7 intelligent customer engagement that handles inquiries, qualifies leads, and improves conversion rates.",
            icon: <MessageSquare className="w-6 h-6" />,
            link: "/services/chatbots"
        },
        {
            title: "Global SEO Optimization",
            description: "Multi-language search engine optimization to help your brand dominate international markets effortlessly.",
            icon: <Globe className="w-6 h-6" />,
            link: "/services/seo"
        },
        {
            title: "Precision Ad Targeting",
            description: "Machine learning algorithms that refine your audience segments to lower CAC and increase lifetime value.",
            icon: <Search className="w-6 h-6" />,
            link: "/services/advertising"
        },
        {
            title: "Smart Email Campaigns",
            description: "Hyper-personalized email marketing that triggers based on behavioral cues, ensuring maximum engagement.",
            icon: <Mail className="w-6 h-6" />,
            link: "/services/email"
        },
        {
            title: "Data Security & Compliance",
            description: "Enterprise-grade protection for your marketing data, ensuring full compliance with GDPR, CCPA, and more.",
            icon: <ShieldCheck className="w-6 h-6" />,
            link: "/services/compliance"
        }
    ];

    return (
        <main className="min-h-screen bg-background">
            <NavBar brandName="Bizoholic" links={navLinks} />

            <Hero
                badge="Our Services"
                title={
                    <>
                        Comprehensive <span className="text-primary italic">AI Marketing</span> Solutions
                    </>
                }
                subtitle="Everything you need to automate your growth and dominate your industry with the power of artificial intelligence."
                className="pt-32 pb-12"
            />

            <section className="py-24 bg-background">
                <div className="container px-4 md:px-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {services.map((service, index) => (
                            <ServiceCard
                                key={index}
                                title={service.title}
                                description={service.description}
                                icon={service.icon}
                                link={service.link}
                            />
                        ))}
                    </div>
                </div>
            </section>

            <CtaSection
                title="Ready to Transform Your Marketing?"
                subtitle="Join 500+ forward-thinking companies already using Bizoholic to scale their operations."
                primaryCtaText="Contact Sales"
                primaryCtaLink="/contact"
                reviewCount="500"
            />

            <Footer
                brandName="Bizoholic"
                description="Scaling businesses with intelligent AI-powered marketing automation."
                columns={[
                    {
                        title: "Services",
                        links: services.slice(0, 4).map(s => ({ label: s.title, href: s.link }))
                    },
                    {
                        title: "Company",
                        links: [
                            { label: "About Us", href: "/about" },
                            { label: "Blog", href: "/blog" },
                            { label: "Careers", href: "/careers" },
                            { label: "Contact", href: "/contact" },
                        ]
                    },
                    {
                        title: "Legal",
                        links: [
                            { label: "Privacy Policy", href: "/privacy" },
                            { label: "Terms of Service", href: "/terms" },
                            { label: "Cookie Policy", href: "/cookies" },
                        ]
                    }
                ]}
            />
        </main>
    );
}
