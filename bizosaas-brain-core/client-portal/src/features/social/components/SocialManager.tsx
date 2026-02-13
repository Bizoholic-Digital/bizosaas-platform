'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Loader2, Send, CheckCircle2, XCircle, Twitter, Linkedin, Instagram, Facebook, RefreshCw } from 'lucide-react'
import { brainGateway } from '@/lib/brain-gateway-client'
import { toast } from '@/hooks/use-toast'

export function SocialManager() {
    const [topic, setTopic] = useState('')
    const [platform, setPlatform] = useState('twitter')
    const [isGenerating, setIsGenerating] = useState(false)
    const [workflowId, setWorkflowId] = useState<string | null>(null)
    const [status, setStatus] = useState<string | null>(null)
    const [draft, setDraft] = useState<any>(null)

    const handleGenerate = async () => {
        if (!topic) {
            toast({ title: 'Topic required', variant: 'destructive' })
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
            toast({ title: 'Generation started' })
        } catch (err) {
            toast({ title: 'Failed to start generation', variant: 'destructive' })
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
            toast({ title: 'Post approved and scheduled!' })
            setStatus('scheduling')
        } catch (err) {
            toast({ title: 'Failed to approve', variant: 'destructive' })
        }
    }

    const handleReject = async () => {
        if (!workflowId) return
        const notes = prompt('Reason for rejection?')
        if (!notes) return
        try {
            await brainGateway.social.rejectPost(workflowId, notes)
            toast({ title: 'Revision requested' })
            setStatus('revision_requested')
        } catch (err) {
            toast({ title: 'Failed to reject', variant: 'destructive' })
        }
    }

    return (
        <div className="space-y-6">
            <Card className="border-none shadow-xl bg-gradient-to-br from-slate-900 to-slate-800 text-white">
                <CardHeader>
                    <CardTitle className="text-2xl flex items-center gap-2">
                        <Send className="w-6 h-6 text-blue-400" />
                        Social Content Writer
                    </CardTitle>
                    <CardDescription className="text-slate-400">
                        Generate and schedule high-impact social media posts using your brand persona.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid gap-2">
                        <Label htmlFor="topic">What should we write about?</Label>
                        <Input
                            id="topic"
                            placeholder="e.g. The impact of AI on small business productivity"
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            className="bg-slate-800 border-slate-700 text-white"
                        />
                    </div>

                    <div className="flex gap-4">
                        <Tabs value={platform} onValueChange={setPlatform} className="w-full">
                            <TabsList className="bg-slate-800 border-slate-700">
                                <TabsTrigger value="twitter" className="gap-2"><Twitter className="w-4 h-4" /> X</TabsTrigger>
                                <TabsTrigger value="linkedin" className="gap-2"><Linkedin className="w-4 h-4" /> LinkedIn</TabsTrigger>
                                <TabsTrigger value="instagram" className="gap-2"><Instagram className="w-4 h-4" /> Instagram</TabsTrigger>
                            </TabsList>
                        </Tabs>
                    </div>
                </CardContent>
                <CardFooter>
                    <Button
                        onClick={handleGenerate}
                        disabled={isGenerating || (status === 'generating')}
                        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold"
                    >
                        {isGenerating || status === 'generating' ? (
                            <Loader2 className="w-4 h-4 animate-spin mr-2" />
                        ) : (
                            <RefreshCw className="w-4 h-4 mr-2" />
                        )}
                        {status === 'generating' ? 'Generating Draft...' : 'Generate Social Post'}
                    </Button>
                </CardFooter>
            </Card>

            {draft && (
                <Card className="border-slate-800 bg-slate-900/50 backdrop-blur-sm">
                    <CardHeader>
                        <div className="flex justify-between items-center">
                            <CardTitle className="text-lg flex items-center gap-2 text-white">
                                <CheckCircle2 className="w-5 h-5 text-green-400" />
                                Draft Preview
                            </CardTitle>
                            <Badge variant={status === 'awaiting_approval' ? 'default' : 'secondary'}>
                                {status?.replace('_', ' ').toUpperCase()}
                            </Badge>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="p-4 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 whitespace-pre-wrap">
                            {draft.text || draft.caption || JSON.stringify(draft)}
                        </div>
                        {draft.image_prompt && (
                            <div className="mt-4 p-3 rounded bg-blue-900/20 border border-blue-900/30 text-xs text-blue-300">
                                <strong>Image Prompt:</strong> {draft.image_prompt}
                            </div>
                        )}
                    </CardContent>
                    {status === 'awaiting_approval' && (
                        <CardFooter className="flex gap-3 justify-end">
                            <Button variant="outline" onClick={handleReject} className="border-red-900 text-red-400 hover:bg-red-900/20">
                                <XCircle className="w-4 h-4 mr-2" /> Reject
                            </Button>
                            <Button onClick={handleApprove} className="bg-green-600 hover:bg-green-700 text-white">
                                <CheckCircle2 className="w-4 h-4 mr-2" /> Approve & Schedule
                            </Button>
                        </CardFooter>
                    )}
                </Card>
            )}
        </div>
    )
}
