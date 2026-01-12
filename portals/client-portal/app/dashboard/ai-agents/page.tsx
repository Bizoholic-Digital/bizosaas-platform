'use client'

import { useState, useEffect } from 'react'
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
import DashboardLayout from '@/components/ui/dashboard-layout'
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
import type { AgentCategory } from '@/lib/ai/types'

import { useSetHeader } from '@/lib/contexts/HeaderContext'

export default function AIAgentsPage() {
    useSetHeader("AI Agents", "Manage and deploy specialized AI intelligence");
    const router = useRouter()
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedCategory, setSelectedCategory] = useState<string>('all')
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')

    const [agents, setAgents] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const fetchAgents = async () => {
            try {
                const { brainApi } = await import('@/lib/brain-api')
                const data = await brainApi.agents.list()
                setAgents(data)
            } catch (error) {
                console.error('Failed to fetch agents:', error)
            } finally {
                setLoading(false)
            }
        }
        fetchAgents()
    }, [])

    const activeAgents = agents.filter(a => a.status === 'active')

    // Filter agents
    const filteredAgents = agents.filter((agent) => {
        const matchesSearch =
            agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            agent.description.toLowerCase().includes(searchQuery.toLowerCase())
        const matchesCategory =
            selectedCategory === 'all' || agent.category === selectedCategory
        return matchesSearch && matchesCategory
    })

    if (loading) {
        return <div className="p-8">Loading agents...</div>
    }

    const categories = [
        { value: 'all', label: 'All Categories', count: agents.length },
        { value: 'general', label: 'General', count: agents.filter(a => a.category === 'general').length },
        { value: 'marketing', label: 'Marketing', count: agents.filter(a => a.category === 'marketing').length },
        { value: 'content', label: 'Content', count: agents.filter(a => a.category === 'content').length },
        { value: 'seo', label: 'SEO', count: agents.filter(a => a.category === 'seo').length },
        { value: 'social_media', label: 'Social Media', count: agents.filter(a => a.category === 'social_media').length },
        { value: 'analytics', label: 'Analytics', count: agents.filter(a => a.category === 'analytics').length },
        { value: 'email_marketing', label: 'Email Marketing', count: agents.filter(a => a.category === 'email_marketing').length },
        { value: 'crm', label: 'CRM', count: agents.filter(a => a.category === 'crm').length },
        { value: 'ecommerce', label: 'E-commerce', count: agents.filter(a => a.category === 'ecommerce').length },
        { value: 'design', label: 'Design', count: agents.filter(a => a.category === 'design').length },
        { value: 'automation', label: 'Automation', count: agents.filter(a => a.category === 'automation').length },
        { value: 'research', label: 'Research', count: agents.filter(a => a.category === 'research').length },
        { value: 'customer_support', label: 'Support', count: agents.filter(a => a.category === 'customer_support').length },
    ]

    return (
        <div className="flex-1 space-y-6 p-8">
            {/* Header Actions */}
            <div className="flex items-center justify-end">
                <Button onClick={() => router.push('/ai-agents/create')}>
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
                        <div className="text-2xl font-bold">{agents.length}</div>
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
                            {agents.length > 0 ? Math.round((activeAgents.length / agents.length) * 100) : 0}% enabled
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
                    <div className="grid gap-4 md:grid-cols-2">
                        <Card>
                            <CardHeader>
                                <CardTitle>Daily Requests</CardTitle>
                                <CardDescription>Last 7 days volume</CardDescription>
                            </CardHeader>
                            <CardContent className="h-[200px] flex items-end gap-2">
                                {[40, 60, 45, 90, 75, 85, 100].map((h, i) => (
                                    <div key={i} className="flex-1 bg-indigo-500 rounded-t-sm" style={{ height: `${h}%` }} />
                                ))}
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader>
                                <CardTitle>Cost by Category</CardTitle>
                                <CardDescription>Distribution of spend</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-4">
                                    {[
                                        { name: 'Marketing', value: 45, color: 'bg-blue-500' },
                                        { name: 'Content', value: 30, color: 'bg-purple-500' },
                                        { name: 'Research', value: 25, color: 'bg-emerald-500' }
                                    ].map(item => (
                                        <div key={item.name} className="space-y-1">
                                            <div className="flex justify-between text-sm">
                                                <span>{item.name}</span>
                                                <span className="font-bold">{item.value}%</span>
                                            </div>
                                            <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                                                <div className={`h-full ${item.color}`} style={{ width: `${item.value}%` }} />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
                </TabsContent>

                <TabsContent value="logs">
                    <Card>
                        <CardHeader>
                            <CardTitle>Conversation History</CardTitle>
                            <CardDescription>Real-time execution logs from your agents</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="rounded-md border overflow-hidden">
                                <table className="w-full text-sm">
                                    <thead className="bg-slate-50 dark:bg-slate-900 border-b">
                                        <tr>
                                            <th className="text-left p-3 font-medium">Agent</th>
                                            <th className="text-left p-3 font-medium">Action</th>
                                            <th className="text-left p-3 font-medium">Status</th>
                                            <th className="text-right p-3 font-medium">Time</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y">
                                        {[
                                            { agent: 'Marketing Strategist', action: 'SEO Audit', status: 'Success', time: '2m ago' },
                                            { agent: 'Content Creator', action: 'Draft Blog Post', status: 'In Progress', time: '5m ago' },
                                            { agent: 'Data Analyst', action: 'Monthly Report', status: 'Failed', time: '1h ago' }
                                        ].map((log, i) => (
                                            <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-900/50">
                                                <td className="p-3 font-medium">{log.agent}</td>
                                                <td className="p-3 text-slate-500 dark:text-slate-400">{log.action}</td>
                                                <td className="p-3">
                                                    <Badge variant={log.status === 'Success' ? 'default' : log.status === 'Failed' ? 'destructive' : 'secondary'}>
                                                        {log.status}
                                                    </Badge>
                                                </td>
                                                <td className="p-3 text-right text-slate-400">{log.time}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}
