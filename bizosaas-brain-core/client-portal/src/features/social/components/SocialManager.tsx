'use client'

import { useState, useEffect } from 'react'
import {
    Loader2,
    Send,
    CheckCircle2,
    XCircle,
    Twitter,
    Linkedin,
    Instagram,
    Facebook,
    RefreshCw
} from 'lucide-react'
import { brainGateway } from '@/lib/brain-gateway-client'
import { cn } from '@/lib/utils'

export function SocialManager() {
    const [topic, setTopic] = useState('')
    const [platform, setPlatform] = useState('twitter')
    const [isGenerating, setIsGenerating] = useState(false)
    const [workflowId, setWorkflowId] = useState<string | null>(null)
    const [status, setStatus] = useState<string | null>(null)
    const [draft, setDraft] = useState<any>(null)

    const handleGenerate = async () => {
        if (!topic) {
            return
        }

        setIsGenerating(true)
        try {
            const res = await brainGateway.social.generateContent({
                platform,
                topic,
                require_approval: true
            })
            setWorkflowId(res.workflow_id)
            setStatus('generating')
        } catch (err) {
            console.error('Failed to start generation:', err)
        } finally {
            setIsGenerating(false)
        }
    }

    const checkStatus = async () => {
        if (!workflowId) return
        try {
            const res = await brainGateway.social.getStatus(workflowId)
            setStatus(res.status)
            setDraft(res.draft)
        } catch (err) {
            console.error(err)
        }
    }

    useEffect(() => {
        let interval: any
        if (workflowId && status !== 'completed' && status !== 'revision_requested') {
            interval = setInterval(checkStatus, 3000)
        }
        return () => clearInterval(interval)
    }, [workflowId, status])

    const handleApprove = async () => {
        if (!workflowId) return
        try {
            await brainGateway.social.approvePost(workflowId)
            setStatus('scheduling')
        } catch (err) {
            console.error('Failed to approve:', err)
        }
    }

    const handleReject = async () => {
        if (!workflowId) return
        const notes = prompt('Reason for rejection?')
        if (!notes) return
        try {
            await brainGateway.social.rejectPost(workflowId, notes)
            setStatus('revision_requested')
        } catch (err) {
            console.error('Failed to reject:', err)
        }
    }

    return (
        <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden text-white">
                <div className="p-6 border-b border-slate-800 bg-slate-900/50">
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <Send className="w-5 h-5 text-blue-400" />
                        Social Content Writer
                    </h2>
                    <p className="text-sm text-slate-400 mt-1">
                        Generate and schedule high-impact social media posts using your brand persona.
                    </p>
                </div>

                <div className="p-6 space-y-6">
                    <div className="space-y-2">
                        <label htmlFor="topic" className="text-sm font-medium text-slate-300">
                            What should we write about?
                        </label>
                        <input
                            id="topic"
                            type="text"
                            placeholder="e.g. The impact of AI on small business productivity"
                            value={topic}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTopic(e.target.value)}
                            className="w-full bg-slate-800 border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                        />
                    </div>

                    <div className="space-y-3">
                        <label className="text-sm font-medium text-slate-300">Target Platform</label>
                        <div className="flex p-1 bg-slate-800 rounded-xl border border-slate-700 w-fit">
                            {[
                                { id: 'twitter', icon: Twitter, label: 'X' },
                                { id: 'linkedin', icon: Linkedin, label: 'LinkedIn' },
                                { id: 'instagram', icon: Instagram, label: 'Instagram' }
                            ].map((p) => (
                                <button
                                    key={p.id}
                                    onClick={() => setPlatform(p.id)}
                                    className={cn(
                                        "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all",
                                        platform === p.id
                                            ? "bg-blue-600 text-white shadow-lg"
                                            : "text-slate-400 hover:text-white"
                                    )}
                                >
                                    <p.icon className="w-4 h-4" />
                                    {p.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="p-6 bg-slate-900/50 border-t border-slate-800">
                    <button
                        onClick={handleGenerate}
                        disabled={isGenerating || (status === 'generating')}
                        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl shadow-lg shadow-blue-900/20 flex items-center justify-center gap-2 transition-all active:scale-[0.98]"
                    >
                        {isGenerating || status === 'generating' ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <RefreshCw className="w-4 h-4" />
                        )}
                        {status === 'generating' ? 'Generating Draft...' : 'Generate Social Post'}
                    </button>
                </div>
            </div>

            {draft && (
                <div className="bg-slate-900 border border-slate-800 rounded-2xl shadow-xl overflow-hidden text-white">
                    <div className="p-6 border-b border-slate-800 flex justify-between items-center">
                        <h3 className="text-lg font-bold flex items-center gap-2">
                            <CheckCircle2 className="w-5 h-5 text-green-400" />
                            Draft Preview
                        </h3>
                        <span className={cn(
                            "px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider",
                            status === 'awaiting_approval' ? "bg-amber-900/30 text-amber-400 border border-amber-900/50" : "bg-blue-900/30 text-blue-400 border border-blue-900/50"
                        )}>
                            {status?.replace('_', ' ')}
                        </span>
                    </div>

                    <div className="p-6 space-y-4">
                        <div className="p-5 rounded-xl bg-slate-800 border border-slate-700 text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
                            {draft.text || draft.caption || JSON.stringify(draft)}
                        </div>

                        {draft.image_prompt && (
                            <div className="p-3 rounded-lg bg-indigo-900/20 border border-indigo-900/30 text-[11px] text-indigo-300">
                                <span className="font-bold uppercase mr-2 opacity-70 italic">Image Prompt:</span>
                                {draft.image_prompt}
                            </div>
                        )}
                    </div>

                    {status === 'awaiting_approval' && (
                        <div className="p-6 bg-slate-900/50 border-t border-slate-800 flex gap-4">
                            <button
                                onClick={handleReject}
                                className="flex-1 px-4 py-2.5 rounded-xl border border-red-900/50 text-red-400 text-sm font-bold hover:bg-red-900/20 transition-all flex items-center justify-center gap-2"
                            >
                                <XCircle className="w-4 h-4" /> Request Revision
                            </button>
                            <button
                                onClick={handleApprove}
                                className="flex-[2] px-4 py-2.5 rounded-xl bg-green-600 text-white text-sm font-bold hover:bg-green-700 shadow-lg shadow-green-900/20 transition-all flex items-center justify-center gap-2"
                            >
                                <CheckCircle2 className="w-4 h-4" /> Approve & Schedule
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}
