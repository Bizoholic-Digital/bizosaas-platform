'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Plug, CheckCircle2, Plus } from "lucide-react"
import type { Connector } from '@/lib/brain-api'

export default function ConnectorsPage() {
    const [connectors, setConnectors] = useState<Connector[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchConnectors = async () => {
            try {
                const { brainApi } = await import('@/lib/brain-api')
                const types = await brainApi.connectors.listTypes()

                // Fetch status for each connector
                const connectorsWithStatus = await Promise.all(types.map(async (c: Connector) => {
                    try {
                        const status = await brainApi.connectors.getStatus(c.id)
                        return { ...c, status: status.status === 'connected' ? 'connected' : 'not_connected' }
                    } catch (e) {
                        return { ...c, status: 'not_connected' }
                    }
                }))

                setConnectors(connectorsWithStatus)
            } catch (error) {
                console.error('Failed to fetch connectors:', error)
            } finally {
                setLoading(false)
            }
        }
        fetchConnectors()
    }, [])

    if (loading) {
        return <div className="p-8">Loading connectors...</div>
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Connectors</h2>
                    <p className="text-muted-foreground">
                        Manage your integrations with external platforms and services.
                    </p>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" /> Add Connector
                </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {connectors.map((connector) => (
                    <Card key={connector.id}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">
                                {connector.name}
                            </CardTitle>
                            <Badge variant={connector.status === 'connected' ? 'default' : 'outline'}>
                                {connector.status === 'connected' ? 'Active' : 'Inactive'}
                            </Badge>
                        </CardHeader>
                        <CardContent>
                            <div className="flex items-center space-x-4 py-4">
                                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-xl font-bold text-slate-900 dark:bg-slate-800 dark:text-slate-100">
                                    {/* Handle icon being an SVG string or name */}
                                    {connector.name.charAt(0)}
                                </div>
                                <div className="space-y-1">
                                    <p className="text-sm text-muted-foreground">
                                        {connector.type}
                                    </p>
                                </div>
                            </div>
                            <p className="text-sm text-muted-foreground mb-4 min-h-[40px]">
                                {connector.description}
                            </p>
                            <Button className="w-full" variant={connector.status === 'connected' ? 'outline' : 'default'}>
                                {connector.status === 'connected' ? (
                                    <>
                                        <CheckCircle2 className="mr-2 h-4 w-4 text-green-500" />
                                        Configure
                                    </>
                                ) : (
                                    <>
                                        <Plug className="mr-2 h-4 w-4" />
                                        Connect
                                    </>
                                )}
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    )
}
