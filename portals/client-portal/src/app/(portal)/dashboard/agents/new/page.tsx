'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import {
    ArrowLeft,
    Save,
    Bot,
    Target,
    Search,
    Check,
    ChevronRight,
    Info,
    Loader2
} from 'lucide-react'
import { brainGateway } from '@/lib/brain-gateway-client'
import { useTenant } from '@/contexts/TenantContext'
import { toast } from 'sonner'

const TOOL_OPTIONS = [
    { id: 'google_search', name: 'Google Search', description: 'Real-time web search capability' },
    { id: 'postgres_query', name: 'DB Browser', description: 'Query your linked databases' },
    { id: 'temporal_workflows', name: 'Workflow Engine', description: 'Trigger and monitor background tasks' },
    { id: 'marketing_analytics', name: 'SEO Insights', description: 'Access search engine ranking data' }
]

const CATEGORIES = ['Marketing', 'Sales', 'Operations', 'Research', 'Support']

export default function NewAgentPage() {
    const router = useRouter()
    const { currentTenant } = useTenant()
    const [loading, setLoading] = useState(false)

    // Form State
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        role: '',
        category: 'Marketing',
        instructions: '',
        icon: '🤖',
        color: '#4f46e5',
        cost_tier: 'standard',
        capabilities: [] as string[],
        tools: [] as string[]
    })

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!formData.name || !formData.role) {
            toast.error('Please fill in required fields')
            return
        }

        try {
            setLoading(true)
            const newAgent = await brainGateway.agents.create({
                ...formData,
                capabilities: [formData.role, ...formData.capabilities]
            })
            toast.success('AI Agent deployed successfully')
            router.push(`/dashboard/agents/${newAgent.id}`)
        } catch (err) {
            console.error('Failed to create agent:', err)
            toast.error('Failed to create agent. Please try again.')
            setLoading(false)
        }
    }

    const toggleTool = (id: string) => {
        setFormData(prev => ({
            ...prev,
            tools: prev.tools.includes(id)
                ? prev.tools.filter(t => t !== id)
                : [...prev.tools, id]
        }))
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <button
                onClick={() => router.push('/dashboard/agents')}
                className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
                <ArrowLeft className="h-4 w-4" />
                <span>Back to Agents</span>
            </button>

            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
                <div className="p-8 border-b border-gray-100 bg-gray-50/50">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-white rounded-2xl shadow-sm text-3xl">
                            {formData.icon}
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">Build New AI Agent</h1>
                            <p className="text-gray-600">Define the intelligence, tools, and constraints for your autonomous agent.</p>
                        </div>
                    </div>
                </div>

                <form onSubmit={handleSubmit} className="p-8 space-y-8">
                    {/* Basic Identity */}
                    <section className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest">1. Basic Identity</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-sm font-semibold text-gray-700">Agent Name <span className="text-red-500">*</span></label>
                                <input
                                    type="text"
                                    value={formData.name}
                                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-solid-900/10 focus:outline-none"
                                    placeholder="e.g. SEO Content Strategist"
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-semibold text-gray-700">Category</label>
                                <select
                                    value={formData.category}
                                    onChange={e => setFormData({ ...formData, category: e.target.value })}
                                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-solid-900/10 focus:outline-none appearance-none"
                                >
                                    {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                                </select>
                            </div>
                            <div className="md:col-span-2 space-y-2">
                                <label className="text-sm font-semibold text-gray-700">Role & Goal <span className="text-red-500">*</span></label>
                                <input
                                    type="text"
                                    value={formData.role}
                                    onChange={e => setFormData({ ...formData, role: e.target.value })}
                                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-solid-900/10 focus:outline-none"
                                    placeholder="e.g. Analyzing top ranking competitors and drafting SEO-optimized blog outlines."
                                    required
                                />
                            </div>
                            <div className="md:col-span-2 space-y-2">
                                <label className="text-sm font-semibold text-gray-700">Description</label>
                                <textarea
                                    value={formData.description}
                                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                                    className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-solid-900/10 focus:outline-none h-20"
                                    placeholder="Brief summary of what this agent does..."
                                />
                            </div>
                        </div>
                    </section>

                    {/* Tools & Capabilities */}
                    <section className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest">2. Tools & Intelligence</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {TOOL_OPTIONS.map(tool => (
                                <div
                                    key={tool.id}
                                    onClick={() => toggleTool(tool.id)}
                                    className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${formData.tools.includes(tool.id)
                                            ? 'border-solid-900 bg-solid-50 ring-2 ring-solid-900/10'
                                            : 'border-gray-100 bg-gray-50/50 hover:border-gray-200'
                                        }`}
                                >
                                    <div className="flex items-start justify-between">
                                        <div>
                                            <h3 className="font-bold text-gray-900 text-sm">{tool.name}</h3>
                                            <p className="text-xs text-gray-500 mt-1">{tool.description}</p>
                                        </div>
                                        {formData.tools.includes(tool.id) && (
                                            <div className="h-5 w-5 bg-solid-900 text-white rounded-full flex items-center justify-center p-1">
                                                <Check className="h-3 w-3" />
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Instructions */}
                    <section className="space-y-4">
                        <div className="flex items-center justify-between">
                            <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest">3. Core Intelligence</h2>
                            <div className="flex items-center gap-1 text-[10px] text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full font-bold">
                                <Info className="h-3 w-3" />
                                <span>AI GUIDED</span>
                            </div>
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-semibold text-gray-700">System Instructions (Prompt)</label>
                            <textarea
                                value={formData.instructions}
                                onChange={e => setFormData({ ...formData, instructions: e.target.value })}
                                className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-solid-900/10 focus:outline-none h-60 font-mono text-sm"
                                placeholder="Talk to the agent like a colleague: 'You are an expert in... your tasks always involve... never do X... always output in format Y...'"
                            />
                        </div>
                    </section>

                    {/* Configuration */}
                    <section className="space-y-4">
                        <h2 className="text-sm font-bold text-gray-400 uppercase tracking-widest">4. Resource Config</h2>
                        <div className="flex gap-4">
                            {['standard', 'premium', 'enterprise'].map(tier => (
                                <button
                                    key={tier}
                                    type="button"
                                    onClick={() => setFormData({ ...formData, cost_tier: tier as any })}
                                    className={`flex-1 py-3 px-4 rounded-xl border-2 capitalize font-bold text-sm transition-all ${formData.cost_tier === tier
                                            ? 'border-solid-900 text-solid-900 bg-solid-50'
                                            : 'border-gray-100 text-gray-400'
                                        }`}
                                >
                                    {tier}
                                </button>
                            ))}
                        </div>
                    </section>

                    <div className="pt-6 border-t border-gray-100 flex items-center justify-end gap-4">
                        <button
                            type="button"
                            onClick={() => router.push('/dashboard/agents')}
                            className="px-6 py-2 text-sm font-bold text-gray-600 hover:text-gray-900"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-8 py-2 bg-solid-900 text-white font-bold rounded-xl hover:bg-solid-800 transition-colors flex items-center gap-2 disabled:opacity-50"
                        >
                            {loading && <Loader2 className="h-4 w-4 animate-spin" />}
                            Deploy Intelligence
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}
