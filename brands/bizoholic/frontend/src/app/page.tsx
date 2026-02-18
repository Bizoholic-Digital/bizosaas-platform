import {
  Hero,
  NavBar,
  ServiceCard,
  Footer,
  CtaSection,
  Button
} from "@bizosaas/ui";
import {
  BarChart3,
  Globe,
  Zap,
  Search,
  PenTool,
  MessageSquare,
  ArrowRight
} from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      <NavBar
        logo={<span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">Bizoholic</span>}
        actions={
          <div className="flex items-center gap-4">
            <Button variant="ghost" className="hidden md:inline-flex">Log In</Button>
            <Button className="rounded-full">Get Started</Button>
          </div>
        }
      />

      <Hero
        badge="New: AI-Powered SEO Tools"
        title={
          <>
            Scale Your Business with <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-blue-400 to-accent">Intelligent Automation</span>
          </>
        }
        subtitle="The all-in-one platform for modern agencies and SaaS businesses. Automate content, SEO, and client management."
        primaryCtaText="Start Free Trial"
        secondaryCtaText="View Demo"
        trustText="Trusted by over 10,000+ businesses"
        image={
          <div className="w-full h-full flex items-center justify-center bg-zinc-900 border border-white/10 rounded-lg">
            <div className="text-center p-8">
              <p className="text-muted-foreground mb-4">Dashboard Preview</p>
              <div className="grid grid-cols-3 gap-4 opacity-50">
                <div className="h-24 bg-white/5 rounded animate-pulse" />
                <div className="h-24 bg-white/5 rounded animate-pulse delay-75" />
                <div className="h-24 bg-white/5 rounded animate-pulse delay-150" />
              </div>
            </div>
          </div>
        }
      />

      <section className="py-24 relative">
        <div className="container">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl md:text-5xl font-bold mb-6">Everything you need to grow</h2>
            <p className="text-xl text-muted-foreground">
              Powerful tools integrated into a single platform. Stop juggling multiple subscriptions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ServiceCard
              title="AI Content Engine"
              description="Generate SEO-optimized blog posts, social media updates, and marketing copy in seconds."
              icon={<PenTool className="w-6 h-6 text-primary" />}
            />
            <ServiceCard
              title="SEO Automation"
              description="Automated keyword research, on-page optimization, and backlink tracking."
              icon={<Search className="w-6 h-6 text-primary" />}
            />
            <ServiceCard
              title="Marketing Analytics"
              description="Unified dashboard for Google Analytics, Search Console, and social insights."
              icon={<BarChart3 className="w-6 h-6 text-primary" />}
            />
            <ServiceCard
              title="Client Portals"
              description="White-labeled dashboards for your clients to view reports and approve content."
              icon={<Globe className="w-6 h-6 text-primary" />}
            />
            <ServiceCard
              title="Social Media Manager"
              description="Schedule posts, track engagement, and manage comments across all platforms."
              icon={<MessageSquare className="w-6 h-6 text-primary" />}
            />
            <ServiceCard
              title="Workflow Automation"
              description="Connect your favorite tools and automate repetitive tasks with custom workflows."
              icon={<Zap className="w-6 h-6 text-primary" />}
            />
          </div>
        </div>
      </section>

      <CtaSection
        title="Ready to transform your business?"
        subtitle="Join thousands of agencies utilizing Bizoholic to scale faster."
        primaryCtaText="Get Started Now"
        rating={4.9}
        reviewCount="500"
      />

      <Footer
        brandName="Bizoholic"
        description="Empowering businesses with intelligent automation tools."
        columns={[
          {
            title: "Product",
            links: [
              { label: "Features", href: "/features" },
              { label: "Pricing", href: "/pricing" },
              { label: "Enterprise", href: "/enterprise" },
              { label: "Roadmap", href: "/roadmap" },
            ]
          },
          {
            title: "Resources",
            links: [
              { label: "Blog", href: "/blog" },
              { label: "Documentation", href: "/docs" },
              { label: "Community", href: "/community" },
              { label: "Help Center", href: "/help" },
            ]
          },
          {
            title: "Company",
            links: [
              { label: "About", href: "/about" },
              { label: "Careers", href: "/careers" },
              { label: "Legal", href: "/legal" },
              { label: "Contact", href: "/contact" },
            ]
          }
        ]}
      />
    </main>
  );
}
