import { NavBar, Footer, Button } from "@bizosaas/ui";
import { Mail, Phone, MapPin, MessageSquare, Send } from "lucide-react";

export default function ContactPage() {
    const navLinks = [
        { label: "Home", href: "/" },
        { label: "Services", href: "/services" },
        { label: "Blog", href: "/blog" },
        { label: "About", href: "/about" },
        { label: "Contact", href: "/contact" },
    ];

    const contactInfo = [
        {
            title: "Email Us",
            value: "hello@bizoholic.com",
            icon: <Mail className="w-5 h-5" />,
            description: "Our team usually responds within 2 hours."
        },
        {
            title: "Call Us",
            value: "+1 (555) 000-0000",
            icon: <Phone className="w-5 h-5" />,
            description: "Mon-Fri from 8am to 5pm PST."
        },
        {
            title: "Office",
            value: "San Francisco, CA",
            icon: <MapPin className="w-5 h-5" />,
            description: "123 Innovation Way, Suite 400."
        }
    ];

    return (
        <main className="min-h-screen bg-background">
            <NavBar brandName="Bizoholic" links={navLinks} />

            <section className="pt-48 pb-24">
                <div className="container px-4 md:px-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
                        {/* Left Side: Text and Info */}
                        <div>
                            <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-sm font-medium text-primary mb-8 animate-fade-in backdrop-blur-sm">
                                <MessageSquare className="w-4 h-4 mr-2" />
                                Contact Us
                            </div>
                            <h1 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight">
                                Let's Start Your <span className="text-primary italic">AI Journey</span>
                            </h1>
                            <p className="text-xl text-muted-foreground mb-12 max-w-xl leading-relaxed">
                                Have questions about our AI marketing platform or ready to build your custom automation strategy? Our team of experts is here to help.
                            </p>

                            <div className="space-y-8">
                                {contactInfo.map((info, i) => (
                                    <div key={i} className="flex gap-4 p-6 rounded-2xl border border-white/5 bg-white/5 backdrop-blur-sm">
                                        <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                                            {info.icon}
                                        </div>
                                        <div>
                                            <h3 className="font-bold text-lg">{info.title}</h3>
                                            <p className="text-primary font-medium mb-1">{info.value}</p>
                                            <p className="text-sm text-muted-foreground">{info.description}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Right Side: Form */}
                        <div className="p-8 md:p-12 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-2xl relative">
                            <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 blur-[100px] pointer-events-none" />

                            <form className="relative z-10 space-y-6">
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">First Name</label>
                                        <input
                                            type="text"
                                            placeholder="Jane"
                                            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium">Last Name</label>
                                        <input
                                            type="text"
                                            placeholder="Doe"
                                            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Work Email</label>
                                    <input
                                        type="email"
                                        placeholder="jane@company.com"
                                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
                                    />
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Subject</label>
                                    <select className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all appearance-none cursor-pointer">
                                        <option className="bg-background">General Inquiry</option>
                                        <option className="bg-background">Product Demo</option>
                                        <option className="bg-background">Pricing Question</option>
                                        <option className="bg-background">Partnership</option>
                                    </select>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Message</label>
                                    <textarea
                                        rows={4}
                                        placeholder="How can we help you?"
                                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all resize-none"
                                    />
                                </div>

                                <Button className="w-full h-14 rounded-xl text-lg shadow-lg shadow-primary/20">
                                    Send Message <Send className="ml-2 w-5 h-5" />
                                </Button>

                                <p className="text-xs text-center text-muted-foreground mt-4">
                                    By clicking send, you agree to our <a href="/privacy" className="text-primary hover:underline">Privacy Policy</a>.
                                </p>
                            </form>
                        </div>
                    </div>
                </div>
            </section>

            <Footer
                brandName="Bizoholic"
                description="Scaling businesses with intelligent AI-powered marketing automation."
                columns={[
                    {
                        title: "Support",
                        links: [
                            { label: "Help Center", href: "/help" },
                            { label: "Documentation", href: "/docs" },
                            { label: "Community", href: "/community" },
                            { label: "Terms of Use", href: "/terms" },
                        ]
                    },
                    {
                        title: "Company",
                        links: [
                            { label: "About Us", href: "/about" },
                            { label: "Services", href: "/services" },
                            { label: "Careers", href: "/careers" },
                            { label: "Blog", href: "/blog" },
                        ]
                    },
                    {
                        title: "Contact",
                        links: [
                            { label: "Sales", href: "mailto:sales@bizoholic.com" },
                            { label: "Support", href: "mailto:support@bizoholic.com" },
                            { label: "Media", href: "mailto:media@bizoholic.com" },
                        ]
                    }
                ]}
            />
        </main>
    );
}
