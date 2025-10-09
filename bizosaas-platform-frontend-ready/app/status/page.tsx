import { Metadata } from 'next'
import { MainHeader } from '@/components/layout/main-header'
import { Footer } from '@/components/footer'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  CheckCircle2,
  AlertCircle,
  Clock,
  Activity,
  Server,
  Database,
  Bot,
  Zap,
  Globe,
  Shield
} from 'lucide-react'

export const metadata: Metadata = {
  title: 'System Status - BizoSaaS AI Marketing Platform',
  description: 'Real-time status of BizoSaaS platform services, uptime, and performance metrics.',
}

const services = [
  {
    name: 'API Gateway',
    status: 'operational',
    uptime: '99.98%',
    responseTime: '145ms',
    icon: Server,
    description: 'Core API and platform access'
  },
  {
    name: 'AI Agents',
    status: 'operational',
    uptime: '99.95%',
    responseTime: '2.3s',
    icon: Bot,
    description: 'AI automation and optimization services'
  },
  {
    name: 'Database',
    status: 'operational',
    uptime: '99.99%',
    responseTime: '12ms',
    icon: Database,
    description: 'Data storage and retrieval systems'
  },
  {
    name: 'Web Application',
    status: 'operational',
    uptime: '99.97%',
    responseTime: '890ms',
    icon: Globe,
    description: 'Dashboard and user interface'
  },
  {
    name: 'Integration APIs',
    status: 'operational',
    uptime: '99.94%',
    responseTime: '340ms',
    icon: Zap,
    description: 'Third-party platform connections'
  },
  {
    name: 'Authentication',
    status: 'operational',
    uptime: '99.96%',
    responseTime: '89ms',
    icon: Shield,
    description: 'User login and security services'
  }
]

const incidents = [
  {
    title: 'Planned Maintenance - AI Agent Updates',
    status: 'scheduled',
    date: '2025-01-15',
    time: '02:00 - 04:00 UTC',
    description: 'Scheduled maintenance to deploy new AI agent capabilities and performance improvements.',
    impact: 'Minor service interruptions expected for AI automation features.'
  },
  {
    title: 'Database Performance Optimization',
    status: 'resolved',
    date: '2025-01-10',
    time: '14:30 - 15:15 UTC',
    description: 'Temporary increase in response times due to database optimization tasks.',
    impact: 'Dashboard loading times were 20-30% slower than normal.',
    resolution: 'Optimization completed successfully. Performance improved by 15% overall.'
  },
  {
    title: 'Integration API Rate Limiting',
    status: 'resolved',
    date: '2025-01-08',
    time: '09:15 - 09:45 UTC',
    description: 'Some third-party integrations experienced temporary rate limiting.',
    impact: 'Facebook and Google Ads integrations had delayed data sync.',
    resolution: 'Rate limits adjusted and all integrations restored to normal operation.'
  }
]

const metrics = [
  { label: 'Overall Uptime (30 days)', value: '99.96%', trend: 'up' },
  { label: 'Average Response Time', value: '245ms', trend: 'stable' },
  { label: 'Active Users', value: '2,847', trend: 'up' },
  { label: 'AI Automations/Hour', value: '15,234', trend: 'up' }
]

function getStatusIcon(status: string) {
  switch (status) {
    case 'operational':
      return <CheckCircle2 className="h-5 w-5 text-green-600" />
    case 'degraded':
      return <AlertCircle className="h-5 w-5 text-yellow-600" />
    case 'outage':
      return <AlertCircle className="h-5 w-5 text-red-600" />
    case 'maintenance':
      return <Clock className="h-5 w-5 text-blue-600" />
    default:
      return <CheckCircle2 className="h-5 w-5 text-green-600" />
  }
}

function getStatusBadge(status: string) {
  const variants = {
    operational: 'default',
    degraded: 'secondary',
    outage: 'destructive',
    maintenance: 'outline',
    resolved: 'default',
    scheduled: 'secondary'
  } as const

  const labels = {
    operational: 'Operational',
    degraded: 'Degraded',
    outage: 'Outage',
    maintenance: 'Maintenance',
    resolved: 'Resolved',
    scheduled: 'Scheduled'
  }

  return (
    <Badge variant={variants[status as keyof typeof variants] || 'outline'}>
      {labels[status as keyof typeof labels] || status}
    </Badge>
  )
}

export default function StatusPage() {
  return (
    <div className="min-h-screen bg-background">
      <MainHeader />
      
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">System Status</h1>
          <p className="text-xl text-muted-foreground mb-8">
            Real-time status of BizoSaaS platform services and performance metrics
          </p>
          <div className="flex items-center justify-center gap-2">
            <CheckCircle2 className="h-6 w-6 text-green-600" />
            <span className="text-lg font-semibold text-green-600">All Systems Operational</span>
          </div>
        </div>

        {/* Overall Metrics */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          {metrics.map((metric) => (
            <Card key={metric.label}>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {metric.label}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold">{metric.value}</span>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Service Status */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle>Service Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {services.map((service) => (
                <div key={service.name} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center space-x-4">
                    <service.icon className="h-5 w-5 text-muted-foreground" />
                    <div>
                      <div className="flex items-center gap-3 mb-1">
                        <span className="font-medium">{service.name}</span>
                        {getStatusIcon(service.status)}
                        {getStatusBadge(service.status)}
                      </div>
                      <p className="text-sm text-muted-foreground">{service.description}</p>
                    </div>
                  </div>
                  <div className="text-right text-sm">
                    <div className="font-medium">{service.uptime} uptime</div>
                    <div className="text-muted-foreground">{service.responseTime} avg</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Incidents */}
        <Card className="mb-12">
          <CardHeader>
            <CardTitle>Recent Incidents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {incidents.map((incident, index) => (
                <div key={index} className="border-l-4 border-l-primary pl-4 pb-6 last:pb-0">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold">{incident.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {incident.date} • {incident.time}
                      </p>
                    </div>
                    {getStatusBadge(incident.status)}
                  </div>
                  <p className="text-sm mb-2">{incident.description}</p>
                  <p className="text-sm text-muted-foreground mb-2">
                    <strong>Impact:</strong> {incident.impact}
                  </p>
                  {incident.resolution && (
                    <p className="text-sm text-muted-foreground">
                      <strong>Resolution:</strong> {incident.resolution}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Subscribe to Updates */}
        <Card className="text-center">
          <CardContent className="p-8">
            <h3 className="text-2xl font-bold mb-4">Stay Updated</h3>
            <p className="text-muted-foreground mb-6">
              Subscribe to get notified about service updates and maintenance windows
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input 
                type="email" 
                placeholder="Enter your email"
                className="flex-1 px-3 py-2 border border-input rounded-md bg-background"
              />
              <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90">
                Subscribe
              </button>
            </div>
            <p className="text-xs text-muted-foreground mt-4">
              You can unsubscribe at any time. We'll only send important service updates.
            </p>
          </CardContent>
        </Card>
      </div>
      
      <Footer />
    </div>
  )
}