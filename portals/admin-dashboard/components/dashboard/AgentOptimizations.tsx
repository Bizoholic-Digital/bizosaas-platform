'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { Sparkles, CheckCircle2, AlertCircle, TrendingUp, Settings2, PlayCircle } from 'lucide-react'

interface Optimization {
    id: string
    type: string
    description: string
    improvement: string
    impact: 'High' | 'Medium' | 'Low'
    status: 'pending' | 'approved' | 'rejected' | 'executed'
    auto_execute: boolean
    suggestedAt: string
}

export function AgentOptimizations() {
    const [optimizations, setOptimizations] = useState<Optimization[]>([])
    const [totalSavings, setTotalSavings] = useState<{ amount: number, currency: string, period: string } | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchOptimizations()
    }, [])

    const fetchOptimizations = async () => {
        try {
            const res = await fetch('/api/admin/agents/optimizations')
            if (res.ok) {
                const data = await res.json()
                setOptimizations(data.optimizations || [])
                setTotalSavings(data.total_savings || null)
            }
        } catch (err) {
            console.error('Failed to fetch optimizations:', err)
        } finally {
            setIsLoading(false)
        }
    }

    const handleApprove = async (id: string) => {
        try {
            const res = await fetch(`/api/admin/agents/optimizations/${id}/approve`, { method: 'POST' })
            if (res.ok) {
                setOptimizations(prev => prev.map(opt =>
                    opt.id === id ? { ...opt, status: 'approved' } : opt
                ))
            }
        } catch (err) {
            console.error('Failed to approve:', err)
        }
    }

    const handleToggleAuto = async (id: string, enabled: boolean) => {
        try {
            const res = await fetch(`/api/admin/agents/optimizations/${id}/toggle-auto`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled })
            })
            if (res.ok) {
                setOptimizations(prev => prev.map(opt =>
                    opt.id === id ? { ...opt, auto_execute: enabled } : opt
                ))
            }
        } catch (err) {
            console.error('Failed to toggle auto:', err)
        }
    }

    if (isLoading) return <div className="animate-pulse h-48 bg-slate-100 dark:bg-slate-800 rounded-2xl" />

    return (
        <Card className="border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-indigo-600 to-blue-600 text-white p-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-white/20 rounded-lg backdrop-blur-md">
                            <Sparkles className="h-5 w-5 text-yellow-300" />
                        </div>
                        <div>
                            <CardTitle className="text-xl font-black tracking-tight">AI Agent Optimizations</CardTitle>
                            <CardDescription className="text-indigo-100 font-medium">Autonomous performance & cost improvements</CardDescription>
                        </div>
                    </div>
                    <Badge className="bg-yellow-400 text-slate-900 font-black border-none px-3 py-1">
                        {optimizations.filter(o => o.status === 'pending').length} PENDING
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="p-0">
                <div className="divide-y divide-slate-100 dark:divide-slate-800">
                    {optimizations.length === 0 ? (
                        <div className="p-12 text-center space-y-4">
                            <div className="inline-flex p-4 bg-slate-50 dark:bg-slate-900 rounded-full">
                                <CheckCircle2 className="h-8 w-8 text-green-500" />
                            </div>
                            <h4 className="text-lg font-bold text-slate-900 dark:text-white">System is optimal</h4>
                            <p className="text-sm text-slate-500 max-w-xs mx-auto">AI agents are currently operating at peak efficiency. No optimizations suggested.</p>
                        </div>
                    ) : (
                        optimizations.map((opt) => (
                            <div key={opt.id} className="p-6 hover:bg-slate-50 dark:hover:bg-slate-900/50 transition-colors group">
                                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                                    <div className="space-y-3 flex-1">
                                        <div className="flex items-center gap-2">
                                            <Badge variant={opt.impact === 'High' ? 'destructive' : 'secondary'} className="font-black text-[10px] uppercase">
                                                {opt.impact} Impact
                                            </Badge>
                                            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{opt.type}</span>
                                        </div>
                                        <h4 className="text-lg font-black text-slate-900 dark:text-white leading-tight">
                                            {opt.description}
                                        </h4>
                                        <p className="text-sm text-slate-600 dark:text-slate-400 font-medium">
                                            <span className="text-indigo-500 font-bold italic mr-1">Suggested improvement:</span>
                                            {opt.improvement}
                                        </p>
                                    </div>

                                    <div className="flex flex-col items-stretch md:items-end gap-3 shrink-0 w-full md:w-auto">
                                        <div className="flex items-center justify-between md:justify-end gap-3 p-3 bg-slate-100/50 dark:bg-slate-800/50 rounded-2xl border border-slate-200/50 dark:border-slate-700/50 backdrop-blur-sm">
                                            <div className="flex flex-col">
                                                <span className="text-[10px] font-black uppercase text-slate-500 tracking-wider">Auto-Execute</span>
                                                <span className="text-[9px] text-slate-400 font-bold">AI managed</span>
                                            </div>
                                            <Switch
                                                checked={opt.auto_execute}
                                                onCheckedChange={(checked) => handleToggleAuto(opt.id, checked)}
                                                className="data-[state=checked]:bg-indigo-600"
                                            />
                                        </div>

                                        {opt.status === 'pending' ? (
                                            <Button
                                                size="sm"
                                                onClick={() => handleApprove(opt.id)}
                                                className="bg-indigo-600 hover:bg-indigo-700 text-white font-black rounded-xl px-8 py-6 text-sm shadow-xl shadow-indigo-500/20 w-full md:w-auto transition-all active:scale-95 group"
                                            >
                                                <PlayCircle className="w-4 h-4 mr-2 group-hover:animate-pulse" />
                                                Approve & Run
                                            </Button>
                                        ) : (
                                            <div className="flex items-center justify-center gap-2 text-green-500 font-black text-xs px-6 py-3 bg-green-50 dark:bg-green-900/20 rounded-xl border border-green-100 dark:border-green-900/20 w-full md:w-auto">
                                                <CheckCircle2 className="h-4 w-4" />
                                                {opt.status.toUpperCase()}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {optimizations.length > 0 && (
                    <div className="p-4 bg-slate-50 dark:bg-slate-900/80 border-t border-slate-100 dark:border-slate-800 flex justify-between items-center">
                        <div className="flex items-center gap-2 text-[10px] font-black uppercase text-slate-400">
                            <TrendingUp className="h-3 w-3" />
                            Potential Cost Savings: <span className="text-green-500">
                                {totalSavings ? `${totalSavings.currency === 'USD' ? '$' : ''}${totalSavings.amount.toFixed(2)} / ${totalSavings.period === 'mo' ? 'mo' : totalSavings.period}` : '--'}
                            </span>
                        </div>
                        <Button variant="ghost" size="sm" className="text-[10px] font-black uppercase tracking-widest h-auto py-1">
                            View History
                        </Button>
                    </div>
                )}
            </CardContent>
        </Card>
    )
}
