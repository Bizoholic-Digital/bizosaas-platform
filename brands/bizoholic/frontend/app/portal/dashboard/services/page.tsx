'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Bot, Megaphone, BarChart3, ArrowRight, CheckCircle } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function MyServicesPage() {
    const router = useRouter()

    const services = [
        {
            title: 'AI Campaign Management',
            description: 'Automated campaign optimization across all channels',
            icon: Megaphone,
            status: 'Active',
            features: ['Multi-channel posting', 'AI content generation', 'Performance tracking'],
            link: '/portal/dashboard/campaigns'
        },
        {
            title: 'Marketing Automation',
            description: 'Streamline your marketing workflows with AI',
            icon: Bot,
            status: 'Active',
            features: ['Email sequences', 'Lead scoring', 'Chatbot integration'],
            link: '/portal/dashboard/automation'
        },
        {
            title: 'Performance Analytics',
            description: 'Deep insights into your marketing performance',
            icon: BarChart3,
            status: 'Inactive',
            features: ['Real-time dashboard', 'ROI tracking', 'Custom reports'],
            link: '/portal/dashboard/analytics'
        }
    ]

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold">My Services</h1>
                <p className="text-muted-foreground mt-1">
                    Manage your active subscriptions and services
                </p>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {services.map((service, index) => (
                    <Card key={index} className="flex flex-col">
                        <CardHeader>
                            <div className="flex items-center justify-between mb-2">
                                <div className="p-2 bg-primary/10 rounded-lg">
                                    <service.icon className="h-6 w-6 text-primary" />
                                </div>
                                <span className={`text-xs px-2 py-1 rounded-full ${service.status === 'Active'
                                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100'
                                        : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
                                    }`}>
                                    {service.status}
                                </span>
                            </div>
                            <CardTitle>{service.title}</CardTitle>
                            <CardDescription>{service.description}</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 flex flex-col">
                            <div className="flex-1 space-y-2 mb-6">
                                {service.features.map((feature, i) => (
                                    <div key={i} className="flex items-center text-sm text-muted-foreground">
                                        <CheckCircle className="h-4 w-4 mr-2 text-green-500" />
                                        {feature}
                                    </div>
                                ))}
                            </div>
                            <Button onClick={() => router.push(service.link)} className="w-full">
                                Manage Service <ArrowRight className="ml-2 h-4 w-4" />
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    )
}
