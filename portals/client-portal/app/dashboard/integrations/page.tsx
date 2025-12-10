'use client'

import { useState } from 'react'
import {
    Search,
    LayoutGrid,
    List,
    CheckCircle2,
    PlusCircle,
    Settings2,
    ExternalLink,
    ShoppingCart,
    Users,
    FileText,
    KanbanSquare,
    Globe,
    Wallet
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'

type IntegrationStatus = 'connected' | 'disconnected' | 'pending'

interface Integration {
    id: string
    name: string
    description: string
    category: 'crm' | 'cms' | 'ecommerce' | 'marketing' | 'tasks' | 'projects' | 'billing'
    icon: any
    status: IntegrationStatus
    fields: { name: string; label: string; type: string; placeholder?: string }[]
}

const integrations: Integration[] = [
    {
        id: 'fluentcrm',
        name: 'FluentCRM',
        description: 'Marketing automation and CRM inside WordPress.',
        category: 'crm',
        icon: Users,
        status: 'disconnected',
        fields: [
            { name: 'url', label: 'WordPress URL', type: 'url', placeholder: 'https://your-site.com' },
            { name: 'username', label: 'Username', type: 'text' },
            { name: 'application_password', label: 'Application Password', type: 'password' }
        ]
    },
    {
        id: 'wordpress',
        name: 'WordPress',
        description: 'Sync pages, posts, and media from your WP site.',
        category: 'cms',
        icon: Globe,
        status: 'connected',
        fields: [
            { name: 'url', label: 'WordPress URL', type: 'url' },
            { name: 'username', label: 'Username', type: 'text' },
            { name: 'application_password', label: 'Application Password', type: 'password' }
        ]
    },
    {
        id: 'woocommerce',
        name: 'WooCommerce',
        description: 'Sync products, orders, and customers.',
        category: 'ecommerce',
        icon: ShoppingCart,
        status: 'disconnected',
        fields: [
            { name: 'url', label: 'Store URL', type: 'url' },
            { name: 'consumer_key', label: 'Consumer Key', type: 'text' },
            { name: 'consumer_secret', label: 'Consumer Secret', type: 'password' }
        ]
    },
    {
        id: 'trello',
        name: 'Trello',
        description: 'Manage tasks and projects with Kanban boards.',
        category: 'tasks',
        icon: KanbanSquare,
        status: 'disconnected',
        fields: [
            { name: 'api_key', label: 'API Key', type: 'text' },
            { name: 'api_token', label: 'API Token', type: 'password' }
        ]
    },
    {
        id: 'plane',
        name: 'Plane.so',
        description: 'Open source project management api-first tool.',
        category: 'projects',
        icon: FileText,
        status: 'disconnected',
        fields: [
            { name: 'url', label: 'Instance URL', type: 'url', placeholder: 'https://app.plane.so' },
            { name: 'api_key', label: 'API Key', type: 'password' },
            { name: 'workspace_slug', label: 'Workspace Slug', type: 'text' }
        ]
    },
    {
        id: 'lago',
        name: 'Lago Billing',
        description: 'Open source metering and usage-based billing.',
        category: 'billing',
        icon: Wallet,
        status: 'pending',
        fields: [
            { name: 'api_url', label: 'API URL', type: 'url', placeholder: 'http://localhost:3000' },
            { name: 'api_key', label: 'API Key', type: 'password' }
        ]
    }
]

export default function IntegrationsPage() {
    const [activeTab, setActiveTab] = useState('all')
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedIntegration, setSelectedIntegration] = useState<Integration | null>(null)

    const filteredIntegrations = integrations.filter(integration => {
        const matchesSearch = integration.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            integration.description.toLowerCase().includes(searchQuery.toLowerCase())
        const matchesTab = activeTab === 'all' || integration.category === activeTab
        return matchesSearch && matchesTab
    })

    return (
        <div className="container mx-auto p-6 space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white">Integrations</h1>
                    <p className="text-muted-foreground mt-2">
                        Connect your tools to BizOSaaS and unlock the power of AI Agents.
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <div className="relative w-full md:w-64">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search integrations..."
                            className="pl-8 bg-slate-900 border-slate-700"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                </div>
            </div>

            <Tabs defaultValue="all" className="w-full" onValueChange={setActiveTab}>
                <TabsList className="w-full justify-start bg-slate-900 border border-slate-800 p-0 h-auto flex-wrap">
                    <TabsTrigger value="all" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">All</TabsTrigger>
                    <TabsTrigger value="crm" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">CRM</TabsTrigger>
                    <TabsTrigger value="cms" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">CMS</TabsTrigger>
                    <TabsTrigger value="ecommerce" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">E-Commerce</TabsTrigger>
                    <TabsTrigger value="tasks" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">Tasks</TabsTrigger>
                    <TabsTrigger value="projects" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">Projects</TabsTrigger>
                    <TabsTrigger value="billing" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white px-4 py-2">Billing</TabsTrigger>
                </TabsList>

                <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredIntegrations.map((integration) => (
                        <Card key={integration.id} className="bg-slate-900 border-slate-800 flex flex-col hover:border-blue-500/50 transition-colors">
                            <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
                                <div className="h-10 w-10 rounded-lg bg-blue-900/20 flex items-center justify-center text-blue-500">
                                    <integration.icon className="h-5 w-5" />
                                </div>
                                {integration.status === 'connected' && (
                                    <Badge className="bg-green-500/10 text-green-500 hover:bg-green-500/20 border-green-500/20">
                                        Connected
                                    </Badge>
                                )}
                                {integration.status === 'pending' && (
                                    <Badge className="bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20 border-yellow-500/20">
                                        Pending
                                    </Badge>
                                )}
                            </CardHeader>
                            <CardContent className="flex-1">
                                <CardTitle className="text-xl text-white mb-2">{integration.name}</CardTitle>
                                <CardDescription className="text-slate-400">
                                    {integration.description}
                                </CardDescription>
                            </CardContent>
                            <CardFooter>
                                <Dialog>
                                    <DialogTrigger asChild>
                                        <Button
                                            variant={integration.status === 'connected' ? "outline" : "default"}
                                            className={`w-full ${integration.status === 'connected' ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'bg-blue-600 hover:bg-blue-700'}`}
                                            onClick={() => setSelectedIntegration(integration)}
                                        >
                                            {integration.status === 'connected' ? (
                                                <>
                                                    <Settings2 className="mr-2 h-4 w-4" /> Configure
                                                </>
                                            ) : (
                                                <>
                                                    <PlusCircle className="mr-2 h-4 w-4" /> Connect
                                                </>
                                            )}
                                        </Button>
                                    </DialogTrigger>
                                    <DialogContent className="bg-slate-900 border-slate-800 text-white sm:max-w-[425px]">
                                        <DialogHeader>
                                            <DialogTitle>Connect {integration.name}</DialogTitle>
                                            <DialogDescription className="text-slate-400">
                                                Enter your credentials to connect {integration.name} to BizOSaaS.
                                            </DialogDescription>
                                        </DialogHeader>
                                        <div className="grid gap-4 py-4">
                                            {integration.fields.map((field) => (
                                                <div key={field.name} className="space-y-2">
                                                    <Label htmlFor={field.name} className="text-right">
                                                        {field.label}
                                                    </Label>
                                                    <Input
                                                        id={field.name}
                                                        type={field.type}
                                                        placeholder={field.placeholder}
                                                        className="bg-slate-800 border-slate-700 text-white"
                                                    />
                                                </div>
                                            ))}
                                        </div>
                                        <DialogFooter>
                                            <Button variant="outline" className="border-slate-700 text-slate-300 hover:bg-slate-800">Cancel</Button>
                                            <Button className="bg-blue-600 hover:bg-blue-700">Save Changes</Button>
                                        </DialogFooter>
                                    </DialogContent>
                                </Dialog>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </Tabs>
        </div>
    )
}
