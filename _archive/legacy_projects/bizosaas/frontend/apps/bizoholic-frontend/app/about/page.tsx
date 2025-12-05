'use client'

import Link from 'next/link'
import Image from 'next/image'
import { Header } from '@/components/header'
import { Footer } from '@/components/footer'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, TrendingUp, Users, Target, Zap } from 'lucide-react'

export default function AboutPage() {
  const teamMembers = [
    {
      name: "Sarah Johnson",
      role: "CEO & Founder",
      image: "https://placehold.co/400x400/2563eb/ffffff?text=SJ",
      bio: "15+ years in digital marketing, former Google marketing lead"
    },
    {
      name: "Michael Chen", 
      role: "Head of Strategy",
      image: "https://placehold.co/400x400/2563eb/ffffff?text=MC", 
      bio: "Data-driven strategist with expertise in growth marketing"
    },
    {
      name: "Emily Rodriguez",
      role: "Creative Director", 
      image: "https://placehold.co/400x400/2563eb/ffffff?text=ER",
      bio: "Award-winning designer with a passion for brand storytelling"
    },
    {
      name: "David Kim",
      role: "Tech Lead",
      image: "https://placehold.co/400x400/2563eb/ffffff?text=DK",
      bio: "Full-stack developer specializing in marketing automation"
    }
  ]

  const stats = [
    { number: "500+", label: "Clients Served" },
    { number: "1200%", label: "Average ROI" },
    { number: "50M+", label: "Impressions Generated" },
    { number: "95%", label: "Client Retention" }
  ]

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-indigo-50 to-cyan-50 py-20">
        <div className="container">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
              About <span className="text-primary">Bizoholic</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
              We're a team of marketing mavericks, data scientists, and creative visionaries who believe 
              every business deserves to be addicted to success.
            </p>
            <div className="flex items-center justify-center text-primary">
              <Zap className="w-6 h-6 mr-2" />
              <span className="text-lg font-medium">Turning businesses into success stories since 2018</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-background">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-primary mb-2">{stat.number}</div>
                <div className="text-muted-foreground font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-muted-foreground mb-6">
                We exist to make businesses addicted to growth. Through data-driven strategies, 
                cutting-edge technology, and relentless creativity, we transform marketing challenges 
                into competitive advantages.
              </p>
              <p className="text-lg text-muted-foreground mb-8">
                Every campaign we create, every strategy we implement, and every result we deliver 
                is designed to create a sustainable addiction to success that grows with your business.
              </p>
              <div className="space-y-4">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-3">
                    <TrendingUp className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <span className="text-foreground font-medium">Data-Driven Decision Making</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-3">
                    <Zap className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <span className="text-foreground font-medium">AI-Powered Marketing Automation</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-3">
                    <Target className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <span className="text-foreground font-medium">Transparent Reporting & Analytics</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="aspect-square bg-gradient-to-br from-indigo-400 to-cyan-400 rounded-2xl flex items-center justify-center">
                <TrendingUp className="w-32 h-32 text-white" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-background">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Meet the Team
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              The marketing addicts behind your success stories
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <div key={index} className="text-center group">
                <div className="aspect-square bg-muted rounded-2xl mb-6 overflow-hidden relative group-hover:scale-105 transition-transform duration-300">
                  <Image 
                    src={member.image} 
                    alt={member.name}
                    fill
                    className="object-cover"
                  />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-2">{member.name}</h3>
                <p className="text-primary font-medium mb-3">{member.role}</p>
                <p className="text-muted-foreground text-sm">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Our Values
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              The principles that drive everything we do
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardContent className="pt-8">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <Zap className="w-8 h-8 text-primary-foreground" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-4">Innovation First</h3>
                <p className="text-muted-foreground">
                  We stay ahead of marketing trends and technologies to give our clients a competitive edge.
                </p>
              </CardContent>
            </Card>
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardContent className="pt-8">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <TrendingUp className="w-8 h-8 text-primary-foreground" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-4">Results Driven</h3>
                <p className="text-muted-foreground">
                  Every strategy is measured, optimized, and refined to deliver maximum ROI for our clients.
                </p>
              </CardContent>
            </Card>
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardContent className="pt-8">
                <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <Users className="w-8 h-8 text-primary-foreground" />
                </div>
                <h3 className="text-xl font-bold text-foreground mb-4">Client Partnership</h3>
                <p className="text-muted-foreground">
                  We believe in true partnerships, working as an extension of your team to achieve shared goals.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Get Addicted to Success?
          </h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Join hundreds of businesses that have transformed their marketing with Bizoholic.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/contact">
              <Button size="lg" variant="secondary" className="px-8">
                Start Your Journey
              </Button>
            </Link>
            <Link href="/portfolio">
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-primary">
                View Our Work
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}