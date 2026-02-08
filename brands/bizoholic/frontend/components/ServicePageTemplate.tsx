"use client"

import Link from 'next/link'
import { ArrowLeft, Bot, CheckCircle, Star, Quote } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { LucideIcon } from 'lucide-react'

interface ServiceFeature {
    icon: LucideIcon
    title: string
    description: string
}

interface CampaignType {
    name: string
    description: string
    results: string[]
}

interface PricingPlan {
    name: string
    price: string
    period: string
    description: string
    subscribers?: string
    features: string[]
    popular?: boolean
}

interface Testimonial {
    name: string
    role: string
    company: string
    content: string
    rating: number
    image?: string
}

interface FAQ {
    question: string
    answer: string
}

interface ServicePageProps {
    // Hero Section
    serviceName: string
    serviceDescription: string
    heroIcon: LucideIcon
    ctaPrimary: string
    ctaSecondary: string
    rating: string
    statsText: string
    heroHighlights: string[]

    // Features Section
    featuresTitle: string
    featuresDescription: string
    features: ServiceFeature[]

    // Campaign/Use Cases Section
    campaignTitle: string
    campaignDescription: string
    campaignTypes: CampaignType[]

    // Benefits Section
    benefitsTitle: string
    benefitsDescription: string
    benefits: string[]
    comparisonTitle?: string
    comparisonItems?: { label: string; value: string }[]

    // Social Proof Section
    testimonials: Testimonial[]

    // Pricing Section
    pricingTitle: string
    pricingDescription: string
    pricing: PricingPlan[]

    // FAQ Section
    faqs: FAQ[]

    // CTA Section
    ctaTitle: string
    ctaDescription: string
    ctaButtons: { text: string; variant: 'default' | 'outline' | 'secondary' }[]
}

export default function ServicePageTemplate({
    serviceName,
    serviceDescription,
    heroIcon: HeroIcon,
    ctaPrimary,
    ctaSecondary,
    rating,
    statsText,
    heroHighlights,
    featuresTitle,
    featuresDescription,
    features,
    campaignTitle,
    campaignDescription,
    campaignTypes,
    benefitsTitle,
    benefitsDescription,
    benefits,
    comparisonTitle,
    comparisonItems,
    testimonials,
    pricingTitle,
    pricingDescription,
    pricing,
    faqs,
    ctaTitle,
    ctaDescription,
    ctaButtons
}: ServicePageProps) {
    return (
        <div className="flex flex-col min-h-screen">
            <Header />

            {/* Breadcrumb */}
            <div className="bg-muted/30 py-4">
                <div className="container">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Link href="/" className="hover:text-primary">Home</Link>
                        <span>/</span>
                        <Link href="/services" className="hover:text-primary">Services</Link>
                        <span>/</span>
                        <span className="text-foreground">{serviceName}</span>
                    </div>
                </div>
            </div>

            {/* Hero Section */}
            <section className="py-20 md:py-32">
                <div className="container">
                    <div className="grid lg:grid-cols-2 gap-12 items-center">
                        <div>
                            <Link href="/services" className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary mb-6">
                                <ArrowLeft className="h-4 w-4" />
                                Back to Services
                            </Link>

                            <Badge variant="outline" className="mb-4">
                                <Bot className="h-4 w-4 mr-2" />
                                AI + Expert Based Solution
                            </Badge>

                            <h1 className="text-4xl md:text-5xl font-bold mb-6">
                                {serviceName}
                            </h1>

                            <p className="text-xl text-muted-foreground mb-8">
                                {serviceDescription}
                            </p>

                            <div className="flex flex-col sm:flex-row gap-4 mb-8">
                                <Button size="lg" className="btn-gradient">
                                    {ctaPrimary}
                                </Button>
                                <Button variant="outline" size="lg">
                                    {ctaSecondary}
                                </Button>
                            </div>

                            <div className="flex items-center gap-6 text-sm">
                                <div className="flex items-center gap-2">
                                    <div className="flex text-yellow-400">
                                        {Array.from({ length: 5 }).map((_, i) => (
                                            <Star key={i} className="h-4 w-4 fill-current" />
                                        ))}
                                    </div>
                                    <span>{rating}</span>
                                </div>
                                <div>{statsText}</div>
                            </div>
                        </div>

                        <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8">
                            <HeroIcon className="h-16 w-16 text-primary mb-6" />
                            <h3 className="text-2xl font-bold mb-4">Ready to Transform Your Marketing?</h3>
                            <p className="text-muted-foreground mb-6">
                                Our AI creates personalized campaigns while expert strategists ensure your success.
                            </p>
                            <div className="space-y-3">
                                {heroHighlights.map((highlight, index) => (
                                    <div key={index} className="flex items-center gap-2">
                                        <CheckCircle className="h-5 w-5 text-green-500" />
                                        <span className="text-sm">{highlight}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 bg-muted/30">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            {featuresTitle}
                        </h2>
                        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                            {featuresDescription}
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {features.map((feature, index) => (
                            <Card key={index} className="text-center">
                                <CardHeader>
                                    <feature.icon className="h-12 w-12 text-primary mx-auto mb-4" />
                                    <CardTitle className="text-xl">{feature.title}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <CardDescription className="text-base">
                                        {feature.description}
                                    </CardDescription>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* Campaign Types / Use Cases Section */}
            <section className="py-20">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            {campaignTitle}
                        </h2>
                        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                            {campaignDescription}
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8">
                        {campaignTypes.map((campaign, index) => (
                            <Card key={index}>
                                <CardHeader>
                                    <CardTitle className="text-xl">{campaign.name}</CardTitle>
                                    <CardDescription className="text-base">{campaign.description}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-2">
                                        {campaign.results.map((result, resultIndex) => (
                                            <div key={resultIndex} className="flex items-center gap-2">
                                                <CheckCircle className="h-4 w-4 text-green-500" />
                                                <span className="text-sm font-medium">{result}</span>
                                            </div>
                                        ))}
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* Benefits Section */}
            <section className="py-20 bg-muted/30">
                <div className="container">
                    <div className="grid lg:grid-cols-2 gap-12 items-center">
                        <div>
                            <h2 className="text-3xl md:text-4xl font-bold mb-6">
                                {benefitsTitle}
                            </h2>
                            <p className="text-lg text-muted-foreground mb-8">
                                {benefitsDescription}
                            </p>
                            <div className="space-y-4">
                                {benefits.map((benefit, index) => (
                                    <div key={index} className="flex items-start gap-3">
                                        <CheckCircle className="h-6 w-6 text-green-500 mt-0.5" />
                                        <span className="text-lg">{benefit}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                        {comparisonTitle && comparisonItems && (
                            <div className="space-y-6">
                                <Card className="p-6">
                                    <h3 className="text-xl font-bold mb-4">{comparisonTitle}</h3>
                                    <div className="space-y-4">
                                        {comparisonItems.map((item, index) => (
                                            <div key={index} className="flex justify-between items-center">
                                                <span>{item.label}</span>
                                                <Badge variant="default">{item.value}</Badge>
                                            </div>
                                        ))}
                                    </div>
                                </Card>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Social Proof / Testimonials Section */}
            <section className="py-20">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            What Our <span className="text-primary">Clients Say</span>
                        </h2>
                        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                            Join thousands of satisfied clients who have transformed their marketing with our AI-powered solutions.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {testimonials.map((testimonial, index) => (
                            <Card key={index} className="relative">
                                <CardHeader>
                                    <Quote className="h-8 w-8 text-primary/20 absolute top-4 right-4" />
                                    <div className="flex text-yellow-400 mb-4">
                                        {Array.from({ length: testimonial.rating }).map((_, i) => (
                                            <Star key={i} className="h-4 w-4 fill-current" />
                                        ))}
                                    </div>
                                    <CardDescription className="text-base text-foreground">
                                        "{testimonial.content}"
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="flex items-center gap-3">
                                        <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                                            {testimonial.name.charAt(0)}
                                        </div>
                                        <div>
                                            <p className="font-semibold">{testimonial.name}</p>
                                            <p className="text-sm text-muted-foreground">{testimonial.role}, {testimonial.company}</p>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* Pricing Section */}
            <section className="py-20 bg-muted/30">
                <div className="container">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            {pricingTitle}
                        </h2>
                        <p className="text-lg text-muted-foreground">
                            {pricingDescription}
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                        {pricing.map((plan, index) => (
                            <Card key={index} className={`relative ${plan.popular ? 'border-primary shadow-lg scale-105' : ''}`}>
                                {plan.popular && (
                                    <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
                                        Most Popular
                                    </Badge>
                                )}
                                <CardHeader className="text-center">
                                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                                    <CardDescription>{plan.description}</CardDescription>
                                    <div className="py-4">
                                        <span className="text-4xl font-bold">{plan.price}</span>
                                        <span className="text-muted-foreground">{plan.period}</span>
                                    </div>
                                    {plan.subscribers && (
                                        <Badge variant="outline" className="text-xs">
                                            {plan.subscribers}
                                        </Badge>
                                    )}
                                </CardHeader>
                                <CardContent>
                                    <ul className="space-y-3 mb-6">
                                        {plan.features.map((feature, featureIndex) => (
                                            <li key={featureIndex} className="flex items-center gap-2">
                                                <CheckCircle className="h-4 w-4 text-green-500" />
                                                <span className="text-sm">{feature}</span>
                                            </li>
                                        ))}
                                    </ul>
                                    <Button className="w-full" variant={plan.popular ? 'default' : 'outline'}>
                                        Start {plan.name} Plan
                                    </Button>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* FAQ Section */}
            <section className="py-20">
                <div className="container max-w-4xl">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            Frequently Asked <span className="text-primary">Questions</span>
                        </h2>
                        <p className="text-lg text-muted-foreground">
                            Everything you need to know about our {serviceName.toLowerCase()} service.
                        </p>
                    </div>

                    <div className="space-y-6">
                        {faqs.map((faq, index) => (
                            <Card key={index}>
                                <CardHeader>
                                    <CardTitle className="text-lg">{faq.question}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-muted-foreground">{faq.answer}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-muted/30">
                <div className="container">
                    <div className="bg-gradient-to-r from-primary to-accent rounded-2xl p-12 text-center text-white">
                        <h2 className="text-3xl md:text-4xl font-bold mb-4">
                            {ctaTitle}
                        </h2>
                        <p className="text-xl mb-8 opacity-90">
                            {ctaDescription}
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            {ctaButtons.map((button, index) => (
                                <Button
                                    key={index}
                                    size="lg"
                                    variant={button.variant}
                                    className={button.variant === 'outline' ? 'border-white text-white hover:bg-white hover:text-primary bg-transparent' : ''}
                                >
                                    {button.text}
                                </Button>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            <Footer />
        </div>
    )
}
