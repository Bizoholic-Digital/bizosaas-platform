import Link from "next/link";
import { getAllPosts } from "@/lib/mdx"; // Import from our new utility
import { ArrowRight, CheckCircle2 } from "lucide-react";

export default function Home() {
    // Fetch all services from MDX
    const services = getAllPosts("services");

    return (
        <div className="flex flex-col min-h-screen">
            {/* Hero Section */}
            <section className="px-4 py-24 mx-auto max-w-7xl sm:px-6 lg:px-8">
                <div className="max-w-3xl mx-auto text-center">
                    <h1 className="text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl md:text-6xl">
                        The World's First <span className="text-primary">AI-Native</span> Digital Agency
                    </h1>
                    <p className="mt-6 text-xl text-muted-foreground">
                        Bizoholic replaces expensive retainers with autonomous AI agents.
                        Get enterprise-grade SEO, Social Media, and Content Marketing at a fraction of the cost.
                    </p>
                    <div className="mt-10 flex justify-center gap-4">
                        <Link
                            href="/dashboard/register"
                            className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-primary-foreground bg-primary rounded-md hover:bg-primary/90 transition-colors"
                        >
                            Get Started
                            <ArrowRight className="ml-2 w-4 h-4" />
                        </Link>
                        <Link
                            href="/pricing"
                            className="inline-flex items-center justify-center px-8 py-3 text-base font-medium text-foreground bg-secondary rounded-md hover:bg-secondary/80 transition-colors"
                        >
                            View Pricing
                        </Link>
                    </div>
                </div>
            </section>

            {/* Services Section (Dynamic from MDX) */}
            <section className="py-24 bg-muted/50">
                <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                            Our AI Services
                        </h2>
                        <p className="mt-4 text-lg text-muted-foreground">
                            Select a specialization to deploy your autonomous agent.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
                        {services.map((service) => (
                            <Link
                                key={service.slug}
                                href={`/services/${service.slug}`}
                                className="group relative p-8 bg-card border rounded-2xl hover:shadow-lg transition-all hover:-translate-y-1"
                            >
                                <div className="flex flex-col h-full">
                                    <h3 className="text-xl font-semibold text-foreground mb-3 group-hover:text-primary transition-colors">
                                        {service.title}
                                    </h3>
                                    <p className="text-muted-foreground flex-grow mb-6">
                                        {service.description}
                                    </p>

                                    {/* Feature Preview */}
                                    {service.features && Array.isArray(service.features) && (
                                        <ul className="space-y-2 mb-6">
                                            {service.features.slice(0, 3).map((feature: string) => (
                                                <li key={feature} className="flex items-center text-sm text-muted-foreground">
                                                    <CheckCircle2 className="w-4 h-4 mr-2 text-primary" />
                                                    {feature}
                                                </li>
                                            ))}
                                        </ul>
                                    )}

                                    <div className="flex items-center text-sm font-medium text-primary mt-auto">
                                        Learn more <ArrowRight className="ml-2 w-4 h-4" />
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
}
