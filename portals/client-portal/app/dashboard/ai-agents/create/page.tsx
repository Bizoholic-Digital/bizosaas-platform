'use client';

import React, { useState } from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useRouter } from 'next/navigation';
import { Bot, Sparkles, Zap, Shield, ArrowLeft, Palette, Database, Mail, CheckSquare } from 'lucide-react';
import { toast } from 'sonner';
import { agentsApi } from '@/lib/api/agents';

export default function CreateAgentPage() {
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);

    // Form State
    const [formData, setFormData] = useState({
        name: '',
        category: 'marketing',
        role: '',
        color: '#4f46e5',
        instructions: '',
        tools: ['web_browser'],
        capabilities: ['general_assistance']
    });

    const handleCreate = async () => {
        if (!formData.name || !formData.instructions) {
            toast.error("Please fill in the agent name and instructions.");
            return;
        }

        setLoading(true);
        try {
            const res = await agentsApi.createAgent({
                name: formData.name,
                category: formData.category,
                role: formData.role,
                color: formData.color,
                instructions: formData.instructions,
                tools: formData.tools,
                capabilities: formData.capabilities
            });

            if (res.data) {
                toast.success("AI Agent configured and deployed!");
                router.push('/dashboard/ai-agents'); // Redirect back to library
            }
        } catch (error: any) {
            console.error('Failed to create agent:', error);
            toast.error(error.message || "Failed to deploy agent engine.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 max-w-3xl mx-auto space-y-6">
            <Button variant="ghost" className="mb-4" onClick={() => router.back()}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Back to Library
            </Button>

            <div className="flex items-center justify-between mb-8">
                {[1, 2, 3].map((s) => (
                    <div key={s} className="flex items-center gap-2">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold transition-all ${step >= s ? 'bg-indigo-600 text-white' : 'bg-slate-200 text-slate-500'}`}>
                            {s}
                        </div>
                        <span className={`text-sm font-medium ${step >= s ? 'text-indigo-600' : 'text-slate-400'}`}>
                            {s === 1 ? 'Identity' : s === 2 ? 'Intelligence' : 'Deploy'}
                        </span>
                        {s < 3 && <div className={`w-12 h-0.5 ${step > s ? 'bg-indigo-600' : 'bg-slate-200'}`} />}
                    </div>
                ))}
            </div>

            <Card className="shadow-2xl border-indigo-100 dark:border-slate-800 overflow-hidden">
                <CardHeader className="bg-indigo-50/50 dark:bg-indigo-950/20 pb-8 border-b border-indigo-100 dark:border-slate-800">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-indigo-600 rounded-2xl text-white shadow-lg shadow-indigo-200 dark:shadow-none">
                            <Bot className="w-8 h-8" />
                        </div>
                        <div>
                            <CardTitle className="text-2xl font-bold">
                                {step === 1 ? "Agent Persona" : step === 2 ? "Configure Intelligence" : "Review & Deploy"}
                            </CardTitle>
                            <CardDescription>Define how your agent identifies and behaves.</CardDescription>
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="pt-8 space-y-8">
                    {step === 1 && (
                        <div className="space-y-6 animate-in slide-in-from-right-4 duration-300">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label htmlFor="name">Agent Name</Label>
                                    <Input
                                        id="name"
                                        placeholder="e.g. Sales Optimizer Prime"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="category">Specialization</Label>
                                    <Select
                                        value={formData.category}
                                        onValueChange={(val) => setFormData({ ...formData, category: val })}
                                    >
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="marketing">Marketing Specialist</SelectItem>
                                            <SelectItem value="sales">Sales Assistant</SelectItem>
                                            <SelectItem value="ops">Ops Coordinator</SelectItem>
                                            <SelectItem value="support">Customer Support</SelectItem>
                                            <SelectItem value="general">General Purpose</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="role">Role Title</Label>
                                <Input
                                    id="role"
                                    placeholder="e.g. Content Strategy Lead"
                                    value={formData.role}
                                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="color">Brand Color</Label>
                                <div className="flex gap-4">
                                    {['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'].map(c => (
                                        <button
                                            key={c}
                                            className={`w-8 h-8 rounded-full border-2 shadow-sm transition-all ${formData.color === c ? 'border-indigo-600 scale-110' : 'border-white'}`}
                                            style={{ backgroundColor: c }}
                                            onClick={() => setFormData({ ...formData, color: c })}
                                        />
                                    ))}
                                    <Button variant="outline" size="icon" className="w-8 h-8"><Palette className="w-4 h-4" /></Button>
                                </div>
                            </div>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-6 animate-in slide-in-from-right-4 duration-300">
                            <div className="space-y-2">
                                <Label htmlFor="instructions">System Instructions (Prompt)</Label>
                                <Textarea
                                    id="instructions"
                                    placeholder="Explain how this agent should act, its tone, and its specific goals..."
                                    className="min-h-[150px] font-mono text-sm"
                                    value={formData.instructions}
                                    onChange={(e) => setFormData({ ...formData, instructions: e.target.value })}
                                />
                            </div>
                            <div className="space-y-4">
                                <Label>Enabled Toolsets</Label>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    {[
                                        { id: 'web_browser', name: 'Web Browser', icon: <Zap className="w-4 h-4" /> },
                                        { id: 'database', name: 'Database Connector', icon: <Database className="w-4 h-4" /> },
                                        { id: 'email', name: 'Email Dispatcher', icon: <Mail className="w-4 h-4" /> },
                                        { id: 'task', name: 'Task Executor', icon: <CheckSquare className="w-4 h-4" /> }
                                    ].map(tool => (
                                        <div
                                            key={tool.id}
                                            className={`flex items-center justify-between p-3 rounded-xl border transition-colors cursor-pointer ${formData.tools.includes(tool.id) ? 'border-indigo-200 bg-indigo-50/50' : 'border-slate-100 hover:bg-slate-50'}`}
                                            onClick={() => {
                                                const newTools = formData.tools.includes(tool.id)
                                                    ? formData.tools.filter(t => t !== tool.id)
                                                    : [...formData.tools, tool.id];
                                                setFormData({ ...formData, tools: newTools });
                                            }}
                                        >
                                            <div className="flex items-center gap-2">
                                                {tool.icon}
                                                <span className="text-sm font-medium">{tool.name}</span>
                                            </div>
                                            <div className={`w-10 h-5 rounded-full flex items-center px-1 transition-colors ${formData.tools.includes(tool.id) ? 'bg-indigo-600' : 'bg-slate-200'}`}>
                                                <div className={`w-3 h-3 bg-white rounded-full transition-transform ${formData.tools.includes(tool.id) ? 'translate-x-5' : 'translate-x-0'}`} />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="space-y-6 animate-in slide-in-from-right-4 duration-300">
                            <div className="bg-slate-50 dark:bg-slate-900 p-6 rounded-2xl border border-slate-100 dark:border-slate-800 space-y-4">
                                <div className="flex justify-between">
                                    <span className="text-slate-500">Resource Allocation</span>
                                    <span className="font-bold">Standard Compute</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-slate-500">Intelligence Tier</span>
                                    <span className="font-bold">GPT-4o Optimized</span>
                                </div>
                                <div className="flex justify-between">
                                    <span className="text-slate-500">Est. Operating Cost</span>
                                    <span className="font-bold text-indigo-600">~$0.12 / run</span>
                                </div>
                            </div>
                            <div className="flex items-center gap-2 p-4 bg-amber-50 rounded-xl border border-amber-100 text-amber-800 text-sm">
                                <Shield className="w-5 h-5 flex-shrink-0" />
                                This agent will have access to your connected services data based on your BYOK configuration.
                            </div>
                        </div>
                    )}
                </CardContent>

                <CardFooter className="bg-indigo-50/50 dark:bg-indigo-950/20 pt-8 flex justify-between gap-3 border-t border-indigo-100 dark:border-slate-800 mt-8">
                    <Button variant="outline" onClick={() => setStep(Math.max(1, step - 1))} disabled={step === 1}>
                        Previous
                    </Button>
                    {step < 3 ? (
                        <Button onClick={() => setStep(step + 1)} disabled={step === 1 && !formData.name}>
                            Continue <Sparkles className="ml-2 h-4 w-4" />
                        </Button>
                    ) : (
                        <Button className="bg-indigo-600 hover:bg-indigo-700" onClick={handleCreate} disabled={loading}>
                            {loading ? "Deploying..." : "Deploy Agent Engine"} <Zap className="ml-2 h-4 w-4" />
                        </Button>
                    )}
                </CardFooter>
            </Card>
        </div>
    );
}
