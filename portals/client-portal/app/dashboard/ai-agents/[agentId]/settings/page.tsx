'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { useToast } from "@/components/ui/use-toast";
import { ArrowLeft, Save, Bot, BrainCircuit, Wrench } from "lucide-react";
import { brainApi } from '@/lib/brain-api';

export default function AgentSettingsPage() {
    const params = useParams();
    const router = useRouter();
    const { toast } = useToast();
    const agentId = params.agentId as string;

    const [isLoading, setIsLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [agentConfig, setAgentConfig] = useState<any>({
        role: "Marketing Assistant",
        goal: "Create engaging social media content.",
        backstory: "You are an expert copywriter...",
        temperature: 0.7,
        tools: {
            "google_ads": false,
            "wordpress": true,
            "google_trends": true
        }
    });

    useEffect(() => {
        // Mock fetch config
        setTimeout(() => setIsLoading(false), 500);
    }, [agentId]);

    const handleSave = async () => {
        setSaving(true);
        // await brainApi.agents.updateConfig(agentId, agentConfig);
        setTimeout(() => {
            setSaving(false);
            toast({ title: "Settings Saved", description: "Agent configuration updated." });
        }, 800);
    };

    if (isLoading) return <div className="p-8">Loading settings...</div>;

    return (
        <div className="space-y-6 container mx-auto py-6 max-w-4xl">
            <div className="flex items-center space-x-4 mb-6">
                <Button variant="ghost" size="icon" onClick={() => router.back()}>
                    <ArrowLeft className="h-4 w-4" />
                </Button>
                <div>
                    <h2 className="text-2xl font-bold flex items-center gap-2">
                        <Bot className="h-6 w-6 text-purple-600" />
                        Agent Tuning: {agentId}
                    </h2>
                    <p className="text-muted-foreground">Customize your AI agent's behavior and capabilities.</p>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
                <div className="md:col-span-2 space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Persona & Goals</CardTitle>
                            <CardDescription>Define how the agent thinks and acts.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label>Role Description</Label>
                                <Input
                                    value={agentConfig.role}
                                    onChange={(e) => setAgentConfig({ ...agentConfig, role: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Primary Goal</Label>
                                <Input
                                    value={agentConfig.goal}
                                    onChange={(e) => setAgentConfig({ ...agentConfig, goal: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Backstory & Guidelines</Label>
                                <Textarea
                                    value={agentConfig.backstory}
                                    onChange={(e) => setAgentConfig({ ...agentConfig, backstory: e.target.value })}
                                    rows={5}
                                />
                            </div>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Tool Access</CardTitle>
                            <CardDescription>Select which integrations this agent can control.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {Object.entries(agentConfig.tools).map(([tool, enabled]: [string, any]) => (
                                <div key={tool} className="flex items-center justify-between p-3 border rounded-lg">
                                    <div className="flex items-center gap-3">
                                        <Wrench className="h-4 w-4 text-slate-500" />
                                        <span className="font-medium capitalize">{tool.replace('_', ' ')}</span>
                                    </div>
                                    <Switch
                                        checked={enabled}
                                        onCheckedChange={(checked) =>
                                            setAgentConfig({
                                                ...agentConfig,
                                                tools: { ...agentConfig.tools, [tool]: checked }
                                            })
                                        }
                                    />
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                </div>

                <div className="md:col-span-1 space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Parameters</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-6">
                            <div className="space-y-2">
                                <div className="flex justify-between">
                                    <Label>Creativity (Temperature)</Label>
                                    <span className="text-sm text-muted-foreground">{agentConfig.temperature}</span>
                                </div>
                                <input
                                    type="range"
                                    min="0" max="1" step="0.1"
                                    value={agentConfig.temperature}
                                    onChange={(e) => setAgentConfig({ ...agentConfig, temperature: parseFloat(e.target.value) })}
                                    className="w-full"
                                />
                                <p className="text-xs text-muted-foreground">
                                    Lower for factual tasks, higher for creative writing.
                                </p>
                            </div>
                        </CardContent>
                    </Card>

                    <Button size="lg" className="w-full" onClick={handleSave} disabled={saving}>
                        {saving ? <BrainCircuit className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
                        Save Changes
                    </Button>
                </div>
            </div>
        </div>
    );
}
