'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import {
    ArrowLeft,
    Save,
    Trash2,
    Zap,
    Activity,
    BarChart3,
    Shield,
    Code,
    CheckCircle2,
    AlertCircle,
    Loader2
} from 'lucide-react'
import { brainGateway, type Agent, type AgentOptimization } from '@/lib/brain-gateway-client'
import { useTenant } from '@/contexts/TenantContext'
import { toast } from 'sonner'

export default function AgentDetailPage() {
    const params = useParams()
    const router = useRouter()
    const { currentTenant } = useTenant()
    const agentId = params.agentId as string

    const [agent, setAgent] = useState<Agent | null>(null)
    const [optimizations, setOptimizations] = useState<AgentOptimization[]>([])
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [activeTab, setActiveTab] = useState<'config' | 'performance' | 'optimizations'>('config')

    // Form State
    const [instructions, setInstructions] = useState('')

    useEffect(() => {
        if (!currentTenant || !agentId) return

        const fetchData = async () => {
            try {
                setLoading(true)
                const [agentRes, optsRes] = await Promise.all([
                    brainGateway.agents.get(agentId),
                    brainGateway.agents.listOptimizations(agentId)
                ])
                setAgent(agentRes)
                setInstructions(agentRes.instructions || '')
                setOptimizations(optsRes.optimizations)
                setLoading(false)
            } catch (err) {
                console.error('Failed to fetch agent details:', err)
                toast.error('Failed to load agent details')
                setLoading(false)
            }
        }

        fetchData()
    }, [currentTenant, agentId])

    const handleSave = async () => {
        if (!agent || agent.is_system) return

        try {
            setSaving(true)
            await brainGateway.agents.update(agentId, { instructions })
            toast.success('Agent configuration updated')
            setSaving(false)
        } catch (err) {
            console.error('Failed to save agent:', err)
            toast.error('Failed to save changes')
            setSaving(false)
        }
    }

    const handleApproveOptimization = async (optId: string) => {
        try {
            await brainGateway.agents.approveOptimization(optId)
            setOptimizations(prev => prev.map(o => o.id === optId ? { ...o, status: 'approved' } : o))
            toast.success('Optimization approved')
        } catch (err) {
            toast.error('Failed to approve optimization')
        }
    }

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-96">
                <Loader2 className="h-8 w-8 text-solid-900 animate-spin" />
                <p className="text-gray-500 mt-4">Loading agent intelligence...</p>
            </div>
        )
    }

    if (!agent) {
        return (
            <div className="text-center py-20">
                <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                <h2 className="text-xl font-bold text-gray-900">Agent not found</h2>
                <button
                    onClick={() => router.push('/dashboard/agents')}
                    className="mt-4 text-solid-900 font-medium hover:underline"
                >
                    Back to Agents
                </button>
            </div>
        )
    }

    return (
        <div className="max-w-6xl mx-auto space-y-6">
            {/* Breadcrumb & Actions */}
            <div className="flex items-center justify-between">
                <button
                    onClick={() => router.push('/dashboard/agents')}
                    className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
                >
                    <ArrowLeft className="h-4 w-4" />
                    <span>Back to Agents</span>
                </button>
                <div className="flex items-center gap-3">
                    {!agent.is_system && (
                        <button
                            onClick={handleSave}
                            disabled={saving}
                            className="inline-flex items-center gap-2 px-4 py-2 bg-solid-900 text-white rounded-lg hover:bg-solid-800 transition-colors disabled:opacity-50"
                        >
                            {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                            <span>Save Changes</span>
                        </button>
                    )}
                    {!agent.is_system && (
                        <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors border border-red-100">
                            <Trash2 className="h-4 w-4" />
                        </button>
                    )}
                </div>
            </div>

            {/* Hero Section */}
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm flex flex-col md:flex-row gap-6">
                <div className="h-20 w-20 rounded-2xl flex items-center justify-center text-4xl shadow-sm" style={{ backgroundColor: agent.color + '20', color: agent.color }}>
                    {agent.icon || '🤖'}
                </div>
                <div className="flex-1">
                    <div className="flex items-center gap-3">
                        <h1 className="text-2xl font-bold text-gray-900">{agent.name}</h1>
                        {agent.is_system && (
                            <span className="px-2 py-0.5 bg-solid-50 text-solid-700 text-[10px] font-bold uppercase rounded-full">System</span>
                        )}
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${agent.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
                            }`}>
                            {agent.status}
                        </span>
                    </div>
                    <p className="text-gray-600 mt-1 max-w-2xl">{agent.description}</p>
                    <div className="flex flex-wrap gap-4 mt-4">
                        <div className="flex items-center gap-1.5 text-xs text-gray-500">
                            <Shield className="h-3.5 w-3.5" />
                            <span>Role: {agent.role}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs text-gray-500">
                            <BarChart3 className="h-3.5 w-3.5" />
                            <span>Tier: {agent.cost_tier}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs text-gray-500">
                            <Activity className="h-3.5 w-3.5" />
                            <span>Success Rate: 98.2%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-6 border-b border-gray-200">
                <button
                    onClick={() => setActiveTab('config')}
                    className={`pb-3 px-1 text-sm font-semibold transition-colors border-b-2 ${activeTab === 'config' ? 'border-solid-900 text-solid-900' : 'border-transparent text-gray-500'}`}
                >
                    Personality & Rules
                </button>
                <button
                    onClick={() => setActiveTab('performance')}
                    className={`pb-3 px-1 text-sm font-semibold transition-colors border-b-2 ${activeTab === 'performance' ? 'border-solid-900 text-solid-900' : 'border-transparent text-gray-500'}`}
                >
                    Performance
                </button>
                <button
                    onClick={() => setActiveTab('optimizations')}
                    className={`pb-3 px-1 text-sm font-semibold transition-colors border-b-2 ${activeTab === 'optimizations' ? 'border-solid-900 text-solid-900' : 'border-transparent text-gray-500'}`}
                >
                    Optimizations
                    {optimizations.filter(o => o.status === 'pending').length > 0 && (
                        <span className="ml-2 px-1.5 py-0.5 bg-orange-100 text-orange-600 text-[10px] rounded-full">
                            {optimizations.filter(o => o.status === 'pending').length}
                        </span>
                    )}
                </button>
            </div>

            {/* Content Area */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                    {activeTab === 'config' && (
                        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
                            <div className="flex items-center justify-between">
                                <h2 className="text-lg font-bold text-gray-900">System Instructions</h2>
                                {agent.is_system && (
                                    <span className="text-xs text-gray-500 flex items-center gap-1">
                                        <AlertCircle className="h-3 w-3" />
                                        Read-only platform agent
                                    </span>
                                )}
                            </div>
                            <p className="text-sm text-gray-500">
                                These instructions define exactly how the agent behaves and which rules it must follow.
                                Keep them concise for better performance.
                            </p>
                            <div className="relative">
                                <textarea
                                    value={instructions}
                                    onChange={(e) => setInstructions(e.target.value)}
                                    readOnly={agent.is_system}
                                    placeholder="Enter system prompt for the agent..."
                                    className="w-full h-96 p-4 text-sm font-mono border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-solid-900/10 resize-none bg-gray-50/30"
                                />
                                <Code className="absolute top-3 right-3 h-4 w-4 text-gray-300" />
                            </div>
                        </div>
                    )}

                    {activeTab === 'performance' && (
                        <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-6">
                            <h2 className="text-lg font-bold text-gray-900">Agent Analytics</h2>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="aspect-[16/9] bg-gray-50 rounded-xl flex items-center justify-center border border-gray-100">
                                    <p className="text-xs text-gray-400 font-mono">Usage Chart Placeholder</p>
                                </div>
                                <div className="aspect-[16/9] bg-gray-50 rounded-xl flex items-center justify-center border border-gray-100">
                                    <p className="text-xs text-gray-400 font-mono">Response Time Chart Placeholder</p>
                                </div>
                            </div>
                            <div className="space-y-4">
                                <h3 className="font-semibold text-sm text-gray-900">Detailed Metrics</h3>
                                <div className="divide-y divide-gray-100">
                                    <div className="py-3 flex justify-between text-sm">
                                        <span className="text-gray-500">Total Tokens Consumed</span>
                                        <span className="font-mono font-medium">1,245,602</span>
                                    </div>
                                    <div className="py-3 flex justify-between text-sm">
                                        <span className="text-gray-500">Average Cost / Call</span>
                                        <span className="font-mono font-medium">$0.0042</span>
                                    </div>
                                    <div className="py-3 flex justify-between text-sm">
                                        <span className="text-gray-500">Tool Execution Success</span>
                                        <span className="font-mono font-medium text-green-600">99.1%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {activeTab === 'optimizations' && (
                        <div className="space-y-4">
                            {optimizations.length > 0 ? (
                                optimizations.map(opt => (
                                    <div key={opt.id} className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
                                        <div className="flex items-start justify-between gap-4">
                                            <div className="flex items-center gap-3">
                                                <div className={`p-2 rounded-lg ${opt.type === 'prompt' ? 'bg-blue-50 text-blue-600' :
                                                        opt.type === 'performance' ? 'bg-purple-50 text-purple-600' :
                                                            'bg-green-50 text-green-600'
                                                    }`}>
                                                    <Zap className="h-5 w-5" />
                                                </div>
                                                <div>
                                                    <h3 className="font-bold text-gray-900">{opt.description}</h3>
                                                    <span className={`text-[10px] font-bold uppercase rounded-full px-2 py-0.5 ${opt.impact === 'High' ? 'bg-red-50 text-red-600' :
                                                            opt.impact === 'Medium' ? 'bg-orange-50 text-orange-600' :
                                                                'bg-blue-50 text-blue-600'
                                                        }`}>
                                                        {opt.impact} Impact
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                {opt.potential_savings && (
                                                    <div className="text-sm font-bold text-green-600">
                                                        Save ${opt.potential_savings.amount}/{opt.potential_savings.period}
                                                    </div>
                                                )}
                                                <p className="text-[10px] text-gray-400 mt-1">Suggested {new Date(opt.suggested_at).toLocaleDateString()}</p>
                                            </div>
                                        </div>
                                        <div className="mt-4 p-4 bg-gray-50 rounded-xl border border-gray-100">
                                            <p className="text-sm text-gray-600 leading-relaxed">
                                                <span className="font-bold text-gray-900 block mb-1">Recommended Improvement:</span>
                                                {opt.improvement}
                                            </p>
                                        </div>
                                        <div className="mt-4 flex items-center justify-end gap-3">
                                            <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
                                                Ignore
                                            </button>
                                            {opt.status === 'pending' ? (
                                                <button
                                                    onClick={() => handleApproveOptimization(opt.id)}
                                                    className="px-4 py-2 bg-solid-900 text-white text-sm font-bold rounded-lg hover:bg-solid-800 transition-colors flex items-center gap-2"
                                                >
                                                    <CheckCircle2 className="h-4 w-4" />
                                                    Approve & Execute
                                                </button>
                                            ) : (
                                                <span className="px-4 py-2 bg-green-50 text-green-600 text-sm font-bold rounded-lg flex items-center gap-2">
                                                    <CheckCircle2 className="h-4 w-4" />
                                                    Approved
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center py-20 bg-white rounded-2xl border border-gray-200">
                                    <Shield className="h-12 w-12 text-green-100 mx-auto mb-4" />
                                    <h3 className="text-lg font-bold text-gray-900">Optimization Peak</h3>
                                    <p className="text-gray-500">This agent is currently operating at maximum theoretical efficiency.</p>
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Support Sidebar Info */}
                <div className="space-y-6">
                    <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
                        <h3 className="font-bold text-gray-900 flex items-center gap-2">
                            <Code className="h-4 w-4" />
                            Active Tools
                        </h3>
                        <div className="space-y-2">
                            {agent.tools.map(tool => (
                                <div key={tool} className="flex items-center justify-between p-2.5 bg-gray-50 rounded-lg border border-gray-100">
                                    <span className="text-xs font-mono text-gray-700">{tool}</span>
                                    <div className="h-1.5 w-1.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]" />
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-2 py-2 text-xs font-bold text-solid-900 hover:bg-solid-50 border border-solid-100 rounded-lg transition-colors">
                            Manage Tool Permissions
                        </button>
                    </div>

                    <div className="bg-blue-50 p-6 rounded-2xl border border-blue-100 space-y-3">
                        <div className="p-2 bg-blue-100 text-blue-600 w-fit rounded-lg">
                            <Zap className="h-5 w-5" />
                        </div>
                        <h3 className="font-bold text-blue-900">Auto-Optimization</h3>
                        <p className="text-xs text-blue-800 leading-relaxed">
                            When enabled, AI will automatically apply low-risk prompt and model improvements to reduce costs and latency.
                        </p>
                        <div className="flex items-center justify-between pt-2">
                            <span className="text-xs font-bold text-blue-900">Enable Autonomous Tuning</span>
                            <div className="h-6 w-11 bg-blue-200 rounded-full relative cursor-pointer">
                                <div className="absolute top-1 left-1 h-4 w-4 bg-white rounded-full shadow-sm" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
