import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import {
    Bot,
    Plus,
    Settings,
    Zap,
    Shield,
    Search,
    Filter,
    MoreVertical,
    ChevronRight,
    Play,
    Activity,
    BarChart3,
    Lightbulb
} from 'lucide-react'
import { brainGateway, type Agent, type AgentOptimization } from '@/lib/brain-gateway-client'
import { useTenant } from '@/contexts/TenantContext'

export default function AgentsPage() {
    const router = useRouter()
    const { currentTenant } = useTenant()
    const [agents, setAgents] = useState<Agent[]>([])
    const [optimizations, setOptimizations] = useState<AgentOptimization[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [activeTab, setActiveTab] = useState<'all' | 'system' | 'custom'>('all')

    useEffect(() => {
        if (!currentTenant) return

        const fetchData = async () => {
            try {
                setLoading(true)
                const [agentsRes, optsRes] = await Promise.all([
                    brainGateway.agents.list(),
                    brainGateway.agents.listOptimizations()
                ])
                setAgents(agentsRes)
                setOptimizations(optsRes.optimizations)
                setLoading(false)
            } catch (err) {
                console.error('Failed to fetch agents data:', err)
                setError('Failed to load agents. Please try again.')
                setLoading(false)
            }
        }

        fetchData()
    }, [currentTenant])

    const filteredAgents = agents.filter(agent => {
        if (activeTab === 'system') return agent.is_system
        if (activeTab === 'custom') return !agent.is_system
        return true
    })

    const stats = {
        total: agents.length,
        active: agents.filter(a => a.status === 'active').length,
        optimizations: optimizations.filter(o => o.status === 'pending').length,
        custom: agents.filter(a => !a.is_system).length
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">AI Agents</h1>
                    <p className="text-gray-600 mt-1">
                        Manage your specialized AI agents and optimize their performance.
                    </p>
                </div>
                <button
                    onClick={() => router.push('/dashboard/agents/new')}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-solid-900 text-white rounded-lg hover:bg-solid-800 transition-colors"
                >
                    <Plus className="h-4 w-4" />
                    <span>Create Custom Agent</span>
                </button>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                            <Bot className="h-5 w-5" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Total Agents</p>
                            <p className="text-xl font-bold text-gray-900">{stats.total}</p>
                        </div>
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-green-50 text-green-600 rounded-lg">
                            <Zap className="h-5 w-5" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Active Now</p>
                            <p className="text-xl font-bold text-gray-900">{stats.active}</p>
                        </div>
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-orange-50 text-orange-600 rounded-lg">
                            <Lightbulb className="h-5 w-5" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Optimizations</p>
                            <p className="text-xl font-bold text-gray-900">{stats.optimizations}</p>
                        </div>
                    </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-purple-50 text-purple-600 rounded-lg">
                            <Settings className="h-5 w-5" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Custom Built</p>
                            <p className="text-xl font-bold text-gray-900">{stats.custom}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main List */}
                <div className="lg:col-span-2 space-y-4">
                    <div className="flex items-center justify-between border-b border-gray-200 pb-2">
                        <div className="flex gap-4">
                            <button
                                onClick={() => setActiveTab('all')}
                                className={`pb-2 px-1 text-sm font-medium transition-colors border-b-2 ${activeTab === 'all' ? 'border-solid-900 text-solid-900' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
                            >
                                All Agents
                            </button>
                            <button
                                onClick={() => setActiveTab('system')}
                                className={`pb-2 px-1 text-sm font-medium transition-colors border-b-2 ${activeTab === 'system' ? 'border-solid-900 text-solid-900' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
                            >
                                System
                            </button>
                            <button
                                onClick={() => setActiveTab('custom')}
                                className={`pb-2 px-1 text-sm font-medium transition-colors border-b-2 ${activeTab === 'custom' ? 'border-solid-900 text-solid-900' : 'border-transparent text-gray-500 hover:text-gray-700'}`}
                            >
                                Custom
                            </button>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="relative">
                                <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                                <input
                                    type="text"
                                    placeholder="Search agents..."
                                    className="pl-9 pr-4 py-1.5 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-solid-900/10 w-48 md:w-64"
                                />
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 gap-4">
                        {loading ? (
                            [1, 2, 3].map(i => (
                                <div key={i} className="h-32 bg-white rounded-xl border border-gray-100 animate-pulse" />
                            ))
                        ) : filteredAgents.length > 0 ? (
                            filteredAgents.map(agent => (
                                <div key={agent.id} className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow group">
                                    <div className="flex items-start gap-4">
                                        <div className="h-12 w-12 rounded-xl flex items-center justify-center text-2xl shadow-sm" style={{ backgroundColor: agent.color + '20', color: agent.color }}>
                                            {agent.icon || '🤖'}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-2">
                                                <h3 className="font-semibold text-gray-900 truncate">{agent.name}</h3>
                                                {agent.is_system && (
                                                    <span className="px-2 py-0.5 bg-solid-50 text-solid-700 text-[10px] font-bold uppercase rounded-full">System</span>
                                                )}
                                                <span className={`h-2 w-2 rounded-full ${agent.status === 'active' ? 'bg-green-500' : 'bg-gray-300'}`} title={agent.status} />
                                            </div>
                                            <p className="text-sm text-gray-600 mt-1 line-clamp-1">{agent.description}</p>
                                            <div className="flex flex-wrap gap-2 mt-3">
                                                {agent.capabilities.slice(0, 3).map(cap => (
                                                    <span key={cap} className="px-2 py-1 bg-gray-50 text-gray-600 text-xs rounded-md border border-gray-100">{cap}</span>
                                                ))}
                                                {agent.capabilities.length > 3 && (
                                                    <span className="px-2 py-1 bg-gray-50 text-gray-400 text-xs rounded-md border border-gray-100">+{agent.capabilities.length - 3} more</span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-2 self-center opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button
                                                onClick={() => router.push(`/dashboard/agents/${agent.id}?tab=performance`)}
                                                className="p-2 text-gray-400 hover:text-solid-900 hover:bg-solid-50 rounded-lg transition-colors"
                                            >
                                                <BarChart3 className="h-5 w-5" />
                                            </button>
                                            <button
                                                onClick={() => router.push(`/dashboard/agents/${agent.id}?tab=config`)}
                                                className="p-2 text-gray-400 hover:text-solid-900 hover:bg-solid-50 rounded-lg transition-colors"
                                            >
                                                <Settings className="h-5 w-5" />
                                            </button>
                                            <button
                                                onClick={() => router.push(`/dashboard/agents/${agent.id}`)}
                                                className="p-2 text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                                            >
                                                <ChevronRight className="h-5 w-5" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
                                <Bot className="h-12 w-12 text-gray-400 mx-auto mb-3" />
                                <h3 className="text-lg font-medium text-gray-900">No agents found</h3>
                                <p className="text-gray-500 mt-1">Try changing your search or create a new custom agent.</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Sidebar Controls */}
                <div className="space-y-6">
                    {/* Optimization Queue */}
                    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                        <div className="p-4 border-b border-gray-200 bg-gray-50/50 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <Zap className="h-4 w-4 text-orange-500" />
                                <h2 className="font-semibold text-gray-900">Optimization Queue</h2>
                            </div>
                            <span className="px-2 py-0.5 bg-orange-100 text-orange-700 text-xs font-bold rounded-full">{optimizations.length}</span>
                        </div>
                        <div className="divide-y divide-gray-100">
                            {optimizations.length > 0 ? (
                                optimizations.slice(0, 5).map(opt => (
                                    <div key={opt.id} className="p-4 hover:bg-gray-50 transition-colors">
                                        <p className="text-sm font-medium text-gray-900 line-clamp-1">{opt.description}</p>
                                        <p className="text-xs text-gray-500 mt-1 line-clamp-2">{opt.improvement}</p>
                                        <div className="flex items-center justify-between mt-3">
                                            <span className={`text-[10px] font-bold uppercase ${opt.impact === 'High' ? 'text-red-600' : opt.impact === 'Medium' ? 'text-orange-600' : 'text-blue-600'
                                                }`}>{opt.impact} Impact</span>
                                            <button className="text-xs font-semibold text-solid-900 hover:text-solid-700">View Details</button>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="p-8 text-center">
                                    <Shield className="h-8 w-8 text-green-500 mx-auto mb-2 opacity-20" />
                                    <p className="text-sm text-gray-500">All agents are currently optimized</p>
                                </div>
                            )}
                        </div>
                        {optimizations.length > 5 && (
                            <button className="w-full py-3 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors border-t border-gray-100 font-medium">
                                View All Suggestions
                            </button>
                        )}
                    </div>

                    {/* Performance Overview */}
                    <div className="bg-solid-900 text-white rounded-xl p-6 shadow-sm overflow-hidden relative">
                        <div className="relative z-10">
                            <h2 className="font-semibold flex items-center gap-2 mb-4">
                                <BarChart3 className="h-4 w-4" />
                                Global Performance
                            </h2>
                            <div className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <span className="text-xs text-solid-200">Success Rate</span>
                                    <span className="text-sm font-bold">98.4%</span>
                                </div>
                                <div className="w-full bg-solid-800 rounded-full h-1.5">
                                    <div className="bg-green-400 h-1.5 rounded-full" style={{ width: '98.4%' }} />
                                </div>
                                <div className="flex items-center justify-between pt-2">
                                    <span className="text-xs text-solid-200">Avg Response</span>
                                    <span className="text-sm font-bold">1.2s</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-xs text-solid-200">Weekly Savings</span>
                                    <span className="text-sm font-bold text-green-400">$124.50</span>
                                </div>
                            </div>
                            <button className="w-full mt-6 py-2 bg-white/10 hover:bg-white/20 transition-colors rounded-lg text-xs font-semibold backdrop-blur-sm">
                                View Full Analytics
                            </button>
                        </div>
                        <div className="absolute -right-8 -bottom-8 h-32 w-32 bg-solid-800 rounded-full opacity-50" />
                    </div>
                </div>
            </div>
        </div>
    )
}
