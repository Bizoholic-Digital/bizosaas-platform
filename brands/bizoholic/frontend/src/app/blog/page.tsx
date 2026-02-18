import { NavBar, Hero, BlogCard, Footer, CtaSection } from "@bizosaas/ui";

export default function BlogPage() {
    const navLinks = [
        { label: "Home", href: "/" },
        { label: "Services", href: "/services" },
        { label: "Blog", href: "/blog" },
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
    ];

    const posts = [
        {
            title: "The Future of AI in Marketing Automation",
            excerpt: "Discover how machine learning is redefining the way brands interact with customers in 2026.",
            category: "AI & Innovation",
            author: "Alex Rivera",
            date: "Feb 15, 2026",
            readTime: "8 min",
            href: "/blog/future-of-ai",
            imageSrc: "/blog/post1.jpg"
        },
        {
            title: "5 Strategies to Lower Your Customer Acquisition Cost",
            excerpt: "Learn how we helped a SaaS company reduce their CAC by 45% using predictive analytics.",
            category: "Growth",
            author: "Sarah Chen",
            date: "Feb 10, 2026",
            readTime: "12 min",
            href: "/blog/lower-cac-strategies",
            imageSrc: "/blog/post2.jpg"
        },
        {
            title: "Mastering Omnichannel Workflows",
            excerpt: "Sync your message across every platform without losing the human touch.",
            category: "Automation",
            author: "James Wilson",
            date: "Feb 5, 2026",
            readTime: "6 min",
            href: "/blog/omnichannel-mastery",
            imageSrc: "/blog/post3.jpg"
        },
        {
            title: "Ethical AI: Protecting Data Privacy",
            excerpt: "How to leverage advanced algorithms while maintaining customer trust and compliance.",
            category: "Privacy",
            author: "Elena Rodriguez",
            date: "Jan 28, 2026",
            readTime: "10 min",
            href: "/blog/ethical-ai-privacy",
            imageSrc: "/blog/post4.jpg"
        },
        {
            title: "Predictive Lead Scoring 101",
            excerpt: "Stop wasting time on low-quality leads and focus on high-intent prospects with AI.",
            category: "Sales",
            author: "Mark Thompson",
            date: "Jan 20, 2026",
            readTime: "7 min",
            href: "/blog/predictive-lead-scoring",
            imageSrc: "/blog/post5.jpg"
        },
        {
            title: "The Rise of Voice Commerce",
            excerpt: "Preparing your brand for the next frontier of shopping and customer engagement.",
            category: "Future Tech",
            author: "Aisha Khan",
            date: "Jan 12, 2026",
            readTime: "9 min",
            href: "/blog/voice-commerce-rise",
            imageSrc: "/blog/post6.jpg"
        }
    ];

    return (
        <main className="min-h-screen bg-background">
            <NavBar brandName="Bizoholic" links={navLinks} />

            <Hero
                badge="Bizoholic Blog"
                title={
                    <>
                        Insights for the <span className="text-primary italic">AI-Driven</span> Marketer
                    </>
                }
                subtitle="Exploring the intersection of technology, data, and human creativity to scale the world's most innovative brands."
                className="pt-32 pb-12"
            />

            <section className="py-24">
                <div className="container px-4 md:px-6">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
                        <div>
                            <h2 className="text-3xl font-bold tracking-tight text-foreground">Recent Articles</h2>
                            <p className="text-muted-foreground mt-2">The latest from our research and design teams.</p>
                        </div>
                        <div className="flex gap-2">
                            <button className="px-4 py-2 rounded-full border border-border bg-white/5 text-sm hover:bg-white/10 transition-colors">All Topics</button>
                            <button className="px-4 py-2 rounded-full border border-border bg-white/5 text-sm hover:bg-white/10 transition-colors">AI & Tech</button>
                            <button className="px-4 py-2 rounded-full border border-border bg-white/5 text-sm hover:bg-white/10 transition-colors">Growth</button>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {posts.map((post, index) => (
                            <BlogCard
                                key={index}
                                title={post.title}
                                excerpt={post.excerpt}
                                category={post.category}
                                author={post.author}
                                date={post.date}
                                readTime={post.readTime}
                                href={post.href}
                                imageSrc={post.imageSrc}
                            />
                        ))}
                    </div>
                </div>
            </section>

            <CtaSection
                title="Stay Ahead of the Curve"
                subtitle="Subscribe to our weekly digest for the latest AI marketing trends and growth strategies."
                primaryCtaText="Subscribe Now"
                primaryCtaLink="#"
            />

            <Footer
                brandName="Bizoholic"
                description="Scaling businesses with intelligent AI-powered marketing automation."
                columns={[
                    {
                        title: "Blog Categories",
                        links: [
                            { label: "AI & Innovation", href: "/blog/category/ai" },
                            { label: "Growth Strategies", href: "/blog/category/growth" },
                            { label: "Automation", href: "/blog/category/automation" },
                            { label: "Data Privacy", href: "/blog/category/privacy" },
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
