import { Metadata } from 'next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { MainHeader } from '@/components/layout/main-header'
import { Footer } from '@/components/footer'
import { 
  MapPin,
  Clock,
  DollarSign,
  Users,
  Rocket,
  Heart,
  Award,
  Coffee,
  Zap,
  Brain,
  Globe,
  Target
} from 'lucide-react'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Careers - Join the AI Marketing Revolution | BizoSaaS',
  description: 'Join our team of AI innovators and marketing experts. Work on cutting-edge technology while helping businesses transform their marketing strategies.',
}

const jobs = [
  {
    title: 'Senior AI Engineer',
    department: 'Engineering',
    location: 'Remote / San Francisco',
    type: 'Full-time',
    salary: '$120k - $180k',
    description: 'Build and optimize AI agents for marketing automation. Work with cutting-edge ML/AI technologies.',
    requirements: ['Python/JavaScript expertise', '5+ years ML/AI experience', 'Marketing domain knowledge preferred'],
    posted: '2 days ago'
  },
  {
    title: 'Marketing Operations Specialist',
    department: 'Marketing',
    location: 'Remote / New York',
    type: 'Full-time',
    salary: '$80k - $120k',
    description: 'Design and implement marketing automation strategies using our AI platform.',
    requirements: ['Marketing automation expertise', 'HubSpot/Marketo experience', 'Data analysis skills'],
    posted: '1 week ago'
  },
  {
    title: 'Product Manager - AI Agents',
    department: 'Product',
    location: 'Remote / Austin',
    type: 'Full-time',
    salary: '$100k - $150k',
    description: 'Drive product strategy for our AI agent ecosystem and platform development.',
    requirements: ['5+ years PM experience', 'AI/ML product background', 'B2B SaaS expertise'],
    posted: '3 days ago'
  },
  {
    title: 'Customer Success Manager',
    department: 'Customer Success',
    location: 'Remote',
    type: 'Full-time',
    salary: '$70k - $100k',
    description: 'Help enterprise clients maximize ROI from our AI marketing platform.',
    requirements: ['Customer success experience', 'Marketing technology knowledge', 'Strong communication skills'],
    posted: '5 days ago'
  },
  {
    title: 'DevOps Engineer',
    department: 'Engineering',
    location: 'Remote / Denver',
    type: 'Full-time',
    salary: '$110k - $160k',
    description: 'Build and maintain scalable infrastructure for our AI-powered platform.',
    requirements: ['Kubernetes/Docker expertise', 'AWS/Azure experience', 'CI/CD pipeline experience'],
    posted: '1 week ago'
  },
  {
    title: 'Sales Development Representative',
    department: 'Sales',
    location: 'Remote / Chicago',
    type: 'Full-time',
    salary: '$60k - $90k + Commission',
    description: 'Generate qualified leads and drive growth for our AI marketing platform.',
    requirements: ['B2B sales experience', 'SaaS background preferred', 'Excellent communication skills'],
    posted: '4 days ago'
  }
]

const benefits = [
  {
    icon: Heart,
    title: 'Health & Wellness',
    description: 'Comprehensive health, dental, and vision insurance plus wellness stipend'
  },
  {
    icon: Clock,
    title: 'Flexible Schedule',
    description: 'Flexible working hours and unlimited PTO policy'
  },
  {
    icon: Globe,
    title: 'Remote First',
    description: 'Work from anywhere with quarterly team gatherings'
  },
  {
    icon: Rocket,
    title: 'Growth Opportunities',
    description: 'Learning budget and conference attendance support'
  },
  {
    icon: DollarSign,
    title: 'Competitive Compensation',
    description: 'Top-tier salaries plus equity in a fast-growing AI company'
  },
  {
    icon: Coffee,
    title: 'Great Perks',
    description: 'Home office setup, latest equipment, and team retreats'
  }
]

const values = [
  {
    icon: Brain,
    title: 'AI-First Mindset',
    description: 'We believe AI will transform how businesses operate and we\'re leading that change'
  },
  {
    icon: Target,
    title: 'Customer Obsession',
    description: 'Every decision we make starts with understanding and solving customer problems'
  },
  {
    icon: Zap,
    title: 'Move Fast',
    description: 'We iterate quickly, learn from failures, and ship features that matter'
  },
  {
    icon: Users,
    title: 'Team Collaboration',
    description: 'We work together across disciplines to build something greater than the sum of parts'
  }
]

export default function CareersPage() {
  return (
    <div className="min-h-screen bg-background">
      <MainHeader />
      
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">
            Join the AI Marketing Revolution
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            We're building the future of marketing automation with AI agents. 
            Join our team of innovators, engineers, and marketing experts who are 
            transforming how businesses grow.
          </p>
          <div className="flex items-center justify-center gap-6 text-sm">
            <div className="flex items-center">
              <Users className="h-4 w-4 text-primary mr-2" />
              <span>50+ Team Members</span>
            </div>
            <div className="flex items-center">
              <Globe className="h-4 w-4 text-primary mr-2" />
              <span>Remote-First Culture</span>
            </div>
            <div className="flex items-center">
              <Rocket className="h-4 w-4 text-primary mr-2" />
              <span>Series A Startup</span>
            </div>
          </div>
        </div>

        {/* Company Values */}
        <div className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-4">Our Values</h2>
            <p className="text-muted-foreground">
              These principles guide how we work and the products we build
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {values.map((value) => (
              <Card key={value.title} className="text-center">
                <CardHeader className="pb-3">
                  <value.icon className="h-10 w-10 text-primary mx-auto mb-3" />
                  <CardTitle className="text-lg">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{value.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Benefits */}
        <div className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-4">Benefits & Perks</h2>
            <p className="text-muted-foreground">
              We invest in our team with comprehensive benefits and a great work environment
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {benefits.map((benefit) => (
              <Card key={benefit.title}>
                <CardHeader className="pb-3">
                  <div className="flex items-center">
                    <benefit.icon className="h-5 w-5 text-primary mr-3" />
                    <CardTitle className="text-lg">{benefit.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{benefit.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Open Positions */}
        <div className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-4">Open Positions</h2>
            <p className="text-muted-foreground">
              Find your next career opportunity with us
            </p>
          </div>
          
          <div className="space-y-6">
            {jobs.map((job) => (
              <Card key={job.title} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-start lg:items-center gap-3 mb-2">
                        <h3 className="text-xl font-semibold">{job.title}</h3>
                        <Badge variant="outline">{job.department}</Badge>
                      </div>
                      
                      <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-3">
                        <div className="flex items-center">
                          <MapPin className="h-4 w-4 mr-1" />
                          {job.location}
                        </div>
                        <div className="flex items-center">
                          <Clock className="h-4 w-4 mr-1" />
                          {job.type}
                        </div>
                        <div className="flex items-center">
                          <DollarSign className="h-4 w-4 mr-1" />
                          {job.salary}
                        </div>
                      </div>
                      
                      <p className="text-sm mb-3">{job.description}</p>
                      
                      <div className="flex flex-wrap gap-2 text-xs">
                        {job.requirements.map((req) => (
                          <Badge key={req} variant="secondary">{req}</Badge>
                        ))}
                      </div>
                    </div>
                    
                    <div className="flex flex-col items-end gap-2 lg:min-w-[150px]">
                      <Button asChild>
                        <Link href={`/careers/${job.title.toLowerCase().replace(/\s+/g, '-')}`}>
                          Apply Now
                        </Link>
                      </Button>
                      <span className="text-xs text-muted-foreground">Posted {job.posted}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Culture Section */}
        <Card className="mb-16">
          <CardContent className="p-8 text-center">
            <h3 className="text-2xl font-bold mb-4">Life at BizoSaaS</h3>
            <p className="text-muted-foreground mb-6">
              We're building more than just software – we're creating a culture where innovation thrives, 
              people grow, and everyone has the opportunity to make a meaningful impact.
            </p>
            <div className="grid md:grid-cols-3 gap-6 text-sm">
              <div>
                <Award className="h-8 w-8 text-primary mx-auto mb-3" />
                <h4 className="font-semibold mb-2">Recognition</h4>
                <p className="text-muted-foreground">Regular peer recognition and performance bonuses</p>
              </div>
              <div>
                <Users className="h-8 w-8 text-primary mx-auto mb-3" />
                <h4 className="font-semibold mb-2">Collaboration</h4>
                <p className="text-muted-foreground">Cross-functional teams working together seamlessly</p>
              </div>
              <div>
                <Rocket className="h-8 w-8 text-primary mx-auto mb-3" />
                <h4 className="font-semibold mb-2">Innovation</h4>
                <p className="text-muted-foreground">20% time for personal projects and exploration</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* CTA */}
        <Card className="text-center">
          <CardContent className="p-8">
            <h3 className="text-2xl font-bold mb-4">Don't See the Right Role?</h3>
            <p className="text-muted-foreground mb-6">
              We're always looking for talented people to join our team. Send us your resume 
              and tell us how you'd like to contribute to the AI marketing revolution.
            </p>
            <Button asChild size="lg">
              <Link href="/contact">
                <Users className="h-4 w-4 mr-2" />
                Get in Touch
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
      
      <Footer />
    </div>
  )
}