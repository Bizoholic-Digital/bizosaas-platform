import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Plug, CheckCircle2, Plus } from "lucide-react"

const connectors = [
    {
        id: "wordpress",
        name: "WordPress",
        description: "Connect your WordPress site to sync posts, pages, and media.",
        icon: "W",
        status: "connected",
        type: "CMS"
    },
    {
        id: "zoho-crm",
        name: "Zoho CRM",
        description: "Sync leads, contacts, and deals with Zoho CRM.",
        icon: "Z",
        status: "not_connected",
        type: "CRM"
    },
    {
        id: "google-analytics",
        name: "Google Analytics 4",
        description: "View website traffic and performance metrics.",
        icon: "G",
        status: "not_connected",
        type: "Analytics"
    },
    {
        id: "shopify",
        name: "Shopify",
        description: "Sync products, orders, and customer data.",
        icon: "S",
        status: "not_connected",
        type: "E-commerce"
    },
    {
        id: "facebook-ads",
        name: "Meta Ads",
        description: "Manage and optimize your Facebook and Instagram ads.",
        icon: "M",
        status: "not_connected",
        type: "Marketing"
    }
]

export default function ConnectorsPage() {
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
                                    {connector.icon}
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
