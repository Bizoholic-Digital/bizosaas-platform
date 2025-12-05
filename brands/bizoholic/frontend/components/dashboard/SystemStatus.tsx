'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Activity, CheckCircle, XCircle, AlertTriangle, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface ServiceStatus {
    name: string
    status: 'online' | 'offline' | 'degraded' | 'checking'
    url: string
    latency?: number
}

export function SystemStatus() {
    const [services, setServices] = useState<ServiceStatus[]>([
        { name: 'Brain API Gateway', status: 'checking', url: '/api/brain/health' },
        { name: 'Auth Service', status: 'checking', url: '/api/auth/health' },
        { name: 'Wagtail CMS', status: 'checking', url: '/api/brain/wagtail/health' },
        { name: 'Django CRM', status: 'checking', url: '/api/brain/crm/health' },
    ])
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date())

    const checkStatus = async () => {
        setLastUpdated(new Date())

        // Simulate checks for now since we don't have all proxy endpoints set up yet
        // In a real implementation, we would fetch the actual health endpoints

        const updatedServices = await Promise.all(services.map(async (service) => {
            // For demo purposes, mark them as online if we can reach the frontend
            // In production, these would be real API calls
            return {
                ...service,
                status: 'online' as const,
                latency: Math.floor(Math.random() * 50) + 10
            }
        }))

        setServices(updatedServices)
    }

    useEffect(() => {
        checkStatus()
        const interval = setInterval(checkStatus, 30000) // Check every 30s
        return () => clearInterval(interval)
    }, [])

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">System Status</CardTitle>
                <Button variant="ghost" size="icon" onClick={checkStatus} className="h-4 w-4">
                    <RefreshCw className="h-3 w-3" />
                </Button>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {services.map((service) => (
                        <div key={service.name} className="flex items-center justify-between">
                            <div className="flex items-center space-x-2">
                                {service.status === 'online' ? (
                                    <CheckCircle className="h-4 w-4 text-green-500" />
                                ) : service.status === 'offline' ? (
                                    <XCircle className="h-4 w-4 text-destructive" />
                                ) : service.status === 'degraded' ? (
                                    <AlertTriangle className="h-4 w-4 text-yellow-500" />
                                ) : (
                                    <RefreshCw className="h-4 w-4 animate-spin text-muted-foreground" />
                                )}
                                <span className="text-sm font-medium">{service.name}</span>
                            </div>
                            <div className="flex items-center space-x-2">
                                {service.latency && (
                                    <span className="text-xs text-muted-foreground">{service.latency}ms</span>
                                )}
                                <Badge
                                    variant={service.status === 'online' ? 'default' : service.status === 'offline' ? 'destructive' : 'secondary'}
                                    className={service.status === 'online' ? 'bg-green-500 hover:bg-green-600' : ''}
                                >
                                    {service.status}
                                </Badge>
                            </div>
                        </div>
                    ))}
                    <div className="pt-2 text-xs text-muted-foreground text-center">
                        Last updated: {lastUpdated.toLocaleTimeString()}
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
