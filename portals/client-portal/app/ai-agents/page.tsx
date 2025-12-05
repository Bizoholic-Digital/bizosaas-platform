'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import {
    Search,
    Filter,
    Grid3x3,
    List,
    Plus,
    Sparkles,
    Settings,
    TrendingUp,
    Key,
    Activity,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { getAllAgents, getAgentsByCategory, getActiveAgents } from '@/lib/ai'
import type { AgentCategory } from '@/lib/ai/types'

export default function AIAgentsPage() {
    const router = useRouter()
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

    const allAgents = getAllAgents()
    const activeAgents = getActiveAgents()

    // Filter agents
    const filteredAgents = allAgents.filter((agent) => {
        const matchesSearch =
            agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            agent.description.toLowerCase().includes(searchQuery.toLowerCase())
        const matchesCategory =
            selectedCategory === 'all' || agent.category === selectedCategory
        return matchesSearch && matchesCategory
    })

    const categories = [
        { value: 'all', label: 'All Categories', count: allAgents.length },
        { value: 'general', label: 'General', count: getAgentsByCategory('general').length },
        { value: 'marketing', label: 'Marketing', count: getAgentsByCategory('marketing').length },
        { value: 'content', label: 'Content', count: getAgentsByCategory('content').length },
        { value: 'seo', label: 'SEO', count: getAgentsByCategory('seo').length },
        { value: 'social_media', label: 'Social Media', count: getAgentsByCategory('social_media').length },
        { value: 'analytics', label: 'Analytics', count: getAgentsByCategory('analytics').length },
        { value: 'email_marketing', label: 'Email Marketing', count: getAgentsByCategory('email_marketing').length },
        { value: 'crm', label: 'CRM', count: getAgentsByCategory('crm').length },
        { value: 'ecommerce', label: 'E-commerce', count: getAgentsByCategory('ecommerce').length },
        { value: 'design', label: 'Design', count: getAgentsByCategory('design').length },
        { value: 'automation', label: 'Automation', count: getAgentsByCategory('automation').length },
        { value: 'research', label: 'Research', count: getAgentsByCategory('research').length },
        { value: 'customer_support', label: 'Support', count: getAgentsByCategory('customer_support').length },
    ]

    return (
        <div className="flex-1 space-y-6 p-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
                        <Sparkles className="h-8 w-8 text-blue-600" />
                        AI Agents
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        Manage and configure your 93 specialized AI agents
                    </p>
                </div>
                <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    Create Custom Agent
                </Button>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
                        <Sparkles className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{allAgents.length}</div>
                        <p className="text-xs text-muted-foreground">Across 13 categories</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
                        <Activity className="h-4 w-4 text-green-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">{activeAgents.length}</div>
                        <p className="text-xs text-muted-foreground">
                            {Math.round((activeAgents.length / allAgents.length) * 100)}% enabled
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">This Month</CardTitle>
                        <TrendingUp className="h-4 w-4 text-blue-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">1,234</div>
                        <p className="text-xs text-muted-foreground">Total requests</p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
                        <Key className="h-4 w-4 text-purple-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">$45.67</div>
                        <p className="text-xs text-muted-foreground">Using BYOK</p>
                    </CardContent>
                </Card>
            </div>

            {/* Tabs */}
            <Tabs defaultValue="library" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="library">Agent Library</TabsTrigger>
                    <TabsTrigger value="byok">BYOK Management</TabsTrigger>
                    <TabsTrigger value="analytics">Usage Analytics</TabsTrigger>
                    <TabsTrigger value="logs">Agent Logs</TabsTrigger>
                </TabsList>

                <TabsContent value="library" className="space-y-4">
                    {/* Filters */}
                    <div className="flex items-center gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                            <Input
                                placeholder="Search agents..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                            <SelectTrigger className="w-[200px]">
                                <SelectValue placeholder="Category" />
                            </SelectTrigger>
                            <SelectContent>
                                {categories.map((cat) => (
                                    <SelectItem key={cat.value} value={cat.value}>
                                        {cat.label} ({cat.count})
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <div className="flex gap-2">
                            <Button
                                variant={viewMode === 'grid' ? 'default' : 'outline'}
                                size="icon"
                                onClick={() => setViewMode('grid')}
                            >
                                <Grid3x3 className="h-4 w-4" />
                            </Button>
                            <Button
                                variant={viewMode === 'list' ? 'default' : 'outline'}
                                size="icon"
                                onClick={() => setViewMode('list')}
                            >
                                <List className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>

                    {/* Agent Grid/List */}
                    <div
                        className={
                            viewMode === 'grid'
                                ? 'grid gap-4 md:grid-cols-2 lg:grid-cols-3'
                                : 'space-y-4'
                        }
                    >
                        {filteredAgents.map((agent) => (
                            <Card
                                key={agent.id}
                                className="cursor-pointer hover:shadow-lg transition-shadow"
                                onClick={() => router.push(`/ai-agents/${agent.id}`)}
                            >
                                <CardHeader>
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <CardTitle className="text-lg">{agent.name}</CardTitle>
                                            <CardDescription className="mt-1">
                                                {agent.description}
                                            </CardDescription>
                                        </div>
                                        <Badge
                                            variant={agent.status === 'active' ? 'default' : 'secondary'}
                                        >
                                            {agent.status}
                                        </Badge>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-3">
                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-muted-foreground">Category</span>
                                            <Badge variant="outline">{agent.category}</Badge>
                                        </div>
                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-muted-foreground">Cost Tier</span>
                                            <Badge
                                                variant={
                                                    agent.costTier === 'free'
                                                        ? 'default'
                                                        : agent.costTier === 'standard'
                                                            ? 'secondary'
                                                            : 'destructive'
                                                }
                                            >
                                                {agent.costTier}
                                            </Badge>
                                        </div>
                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-muted-foreground">Capabilities</span>
                                            <span className="font-medium">{agent.capabilities.length}</span>
                                        </div>
                                        <Button className="w-full mt-4" size="sm">
                                            <Settings className="mr-2 h-4 w-4" />
                                            Configure
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {filteredAgents.length === 0 && (
                        <div className="text-center py-12">
                            <p className="text-muted-foreground">No agents found matching your criteria</p>
                        </div>
                    )}
                </TabsContent>

                <TabsContent value="byok">
                    <Card>
                        <CardHeader>
                            <CardTitle>BYOK Management</CardTitle>
                            <CardDescription>
                                Manage your API keys for all 20+ services
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <p className="text-muted-foreground">
                                Configure your own API keys to reduce costs and maintain control over your integrations.
                            </p>
                            <Button onClick={() => router.push('/ai-agents/byok')}>
                                Go to BYOK Management
                            </Button>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="analytics">
                    <Card>
                        <CardHeader>
                            <CardTitle>Usage Analytics</CardTitle>
                            <CardDescription>
                                Monitor agent usage, costs, and performance
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground">Analytics dashboard coming soon...</p>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="logs">
                    <Card>
                        <CardHeader>
                            <CardTitle>Agent Logs</CardTitle>
                            <CardDescription>
                                View conversation history and debug information
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground">Agent logs coming soon...</p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}
