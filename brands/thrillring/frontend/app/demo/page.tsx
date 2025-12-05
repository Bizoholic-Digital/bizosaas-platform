import { Metadata } from 'next'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { MainHeader } from '@/components/layout/main-header'
import { Footer } from '@/components/footer'
import { 
  Calendar,
  Clock,
  Users,
  Bot,
  TrendingUp,
  Zap,
  Target,
  BarChart3
} from 'lucide-react'

export const metadata: Metadata = {
  title: 'Request Demo - BizoSaaS AI Marketing Platform',
  description: 'Schedule a personalized demo of our AI-powered marketing automation platform. See how our 28+ AI agents can transform your business.',
}

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-background">
      <MainHeader />
      
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">
            See BizoSaaS in Action
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            Schedule a personalized demo and discover how our AI-powered marketing platform 
            can transform your business with autonomous agents and intelligent automation.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Demo Request Form */}
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Request Your Demo</CardTitle>
              <p className="text-muted-foreground">
                Fill out the form below and our team will schedule a personalized demo for you.
              </p>
            </CardHeader>
            <CardContent>
              <form className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName">First Name</Label>
                    <Input id="firstName" placeholder="John" required />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input id="lastName" placeholder="Doe" required />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="email">Business Email</Label>
                  <Input id="email" type="email" placeholder="john@company.com" required />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="company">Company Name</Label>
                  <Input id="company" placeholder="Your Company" required />
                </div>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="role">Your Role</Label>
                    <Input id="role" placeholder="Marketing Manager" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="teamSize">Team Size</Label>
                    <select className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50">
                      <option value="">Select team size</option>
                      <option value="1-10">1-10 employees</option>
                      <option value="11-50">11-50 employees</option>
                      <option value="51-200">51-200 employees</option>
                      <option value="200+">200+ employees</option>
                    </select>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="interests">Areas of Interest</Label>
                  <Textarea 
                    id="interests" 
                    placeholder="Tell us about your marketing goals and which AI automation features interest you most..."
                    className="min-h-[100px]"
                  />
                </div>
                
                <Button type="submit" className="w-full">
                  <Calendar className="h-4 w-4 mr-2" />
                  Schedule My Demo
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Demo Features */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Clock className="h-5 w-5 mr-2" />
                  What to Expect
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <div className="h-2 w-2 bg-primary rounded-full mt-2 mr-3 flex-shrink-0" />
                    <span className="text-sm">30-minute personalized walkthrough</span>
                  </li>
                  <li className="flex items-start">
                    <div className="h-2 w-2 bg-primary rounded-full mt-2 mr-3 flex-shrink-0" />
                    <span className="text-sm">Live demonstration of AI agents in action</span>
                  </li>
                  <li className="flex items-start">
                    <div className="h-2 w-2 bg-primary rounded-full mt-2 mr-3 flex-shrink-0" />
                    <span className="text-sm">Custom use case discussion for your business</span>
                  </li>
                  <li className="flex items-start">
                    <div className="h-2 w-2 bg-primary rounded-full mt-2 mr-3 flex-shrink-0" />
                    <span className="text-sm">Q&A session with our AI specialists</span>
                  </li>
                  <li className="flex items-start">
                    <div className="h-2 w-2 bg-primary rounded-full mt-2 mr-3 flex-shrink-0" />
                    <span className="text-sm">Pricing and implementation roadmap</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Bot className="h-5 w-5 mr-2" />
                  AI Agents You'll See
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 border rounded-lg">
                    <TrendingUp className="h-8 w-8 text-primary mx-auto mb-2" />
                    <div className="text-sm font-medium">Campaign Optimizer</div>
                  </div>
                  <div className="text-center p-3 border rounded-lg">
                    <Target className="h-8 w-8 text-primary mx-auto mb-2" />
                    <div className="text-sm font-medium">Lead Scorer</div>
                  </div>
                  <div className="text-center p-3 border rounded-lg">
                    <BarChart3 className="h-8 w-8 text-primary mx-auto mb-2" />
                    <div className="text-sm font-medium">Analytics AI</div>
                  </div>
                  <div className="text-center p-3 border rounded-lg">
                    <Zap className="h-8 w-8 text-primary mx-auto mb-2" />
                    <div className="text-sm font-medium">Content Creator</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="h-5 w-5 mr-2" />
                  Trusted by 500+ Companies
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Join businesses that have transformed their marketing with our AI platform:
                </p>
                <div className="grid grid-cols-3 gap-4 text-xs text-center">
                  <div className="p-2 bg-muted/50 rounded">Tech Startups</div>
                  <div className="p-2 bg-muted/50 rounded">E-commerce</div>
                  <div className="p-2 bg-muted/50 rounded">B2B Services</div>
                  <div className="p-2 bg-muted/50 rounded">Healthcare</div>
                  <div className="p-2 bg-muted/50 rounded">Finance</div>
                  <div className="p-2 bg-muted/50 rounded">Real Estate</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  )
}