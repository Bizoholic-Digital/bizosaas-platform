'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ChevronLeft, Play, Pause, RefreshCw, Layers, Shield, Database, Send, CheckCircle2, Clock } from 'lucide-react';
import Link from 'next/link';

import { brainApi } from '@/lib/brain-api';
import { useAuth } from '@clerk/nextjs';

export default function WorkflowVisualizationPage() {
    const { id } = useParams();
    const { getToken } = useAuth();
    const [steps, setSteps] = React.useState<any[]>([]);
    const [isLoading, setIsLoading] = React.useState(true);

    React.useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            try {
                const token = await getToken();
                const data = await brainApi.workflows.getExecutionData(id as string, token as string);

                // Map the simple DAG response to our UI steps
                const mappedSteps = data.nodes.map((node: any) => ({
                    id: node.id,
                    name: node.type === 'trigger' ? 'Trigger' : 'Action',
                    description: node.label,
                    status: node.status,
                    icon: getIconForNode(node.type)
                }));
                setSteps(mappedSteps);
            } catch (error) {
                console.error("Failed to fetch execution data:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, [id]);

    const getIconForNode = (type: string) => {
        switch (type) {
            case 'trigger': return <Layers className="w-5 h-5 text-blue-600" />;
            case 'action': return <Shield className="w-5 h-5 text-purple-600" />;
            default: return <Database className="w-5 h-5 text-slate-400" />;
        }
    };

    return (
        <div className="p-6 max-w-5xl mx-auto space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/dashboard/workflows">
                        <Button variant="ghost" size="icon">
                            <ChevronLeft className="w-5 h-5" />
                        </Button>
                    </Link>
                    <div>
                        <h1 className="text-2xl font-bold">Workflow Visualization</h1>
                        <p className="text-sm text-muted-foreground">ID: {id}</p>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm">
                        <Pause className="w-4 h-4 mr-2" />
                        Pause Workflow
                    </Button>
                    <Button size="sm" className="bg-blue-600">
                        <RefreshCw className="w-4 h-4 mr-2" />
                        Re-run
                    </Button>
                </div>
            </div>

            <Card className="border-none shadow-sm bg-slate-50 dark:bg-slate-900/50 min-h-[500px] flex items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 opacity-10 pointer-events-none" style={{ backgroundImage: 'radial-gradient(#6366f1 1px, transparent 1px)', backgroundSize: '20px 20px' }} />

                {isLoading ? (
                    <div className="flex flex-col items-center gap-4">
                        <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
                        <p className="text-sm text-muted-foreground">Loading execution path...</p>
                    </div>
                ) : (
                    <div className="relative z-10 flex flex-col items-center gap-12 w-full max-w-sm">
                        {steps.map((step, index) => (
                            <div key={step.id} className="relative w-full">
                                <Card className={`relative z-20 transition-all border-2 ${step.status === 'running' ? 'border-purple-500 shadow-lg shadow-purple-500/20 scale-105' : 'border-white dark:border-slate-800'}`}>
                                    <CardContent className="p-4 flex items-center gap-4">
                                        <div className={`p-2 rounded-lg ${step.status === 'completed' ? 'bg-emerald-100 text-emerald-600' : step.status === 'running' ? 'bg-purple-100 text-purple-600' : 'bg-slate-100 text-slate-400'}`}>
                                            {step.status === 'completed' ? <CheckCircle2 className="w-5 h-5" /> : step.icon}
                                        </div>
                                        <div className="flex-1">
                                            <h4 className="font-semibold text-sm">{step.name}</h4>
                                            <p className="text-xs text-muted-foreground">{step.description}</p>
                                        </div>
                                        {step.status === 'running' && (
                                            <RefreshCw className="w-4 h-4 animate-spin text-purple-600" />
                                        )}
                                    </CardContent>
                                </Card>

                                {index < steps.length - 1 && (
                                    <div className="absolute left-1/2 -bottom-12 w-0.5 h-12 bg-slate-200 dark:bg-slate-700 -translate-x-1/2">
                                        <div className={`absolute top-0 left-0 w-full bg-blue-500 transition-all duration-1000 ${index < 2 ? 'h-full' : 'h-0'}`} />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardContent className="p-4">
                        <h4 className="text-xs font-bold uppercase text-muted-foreground mb-2">Total Executions</h4>
                        <div className="text-2xl font-black">1,248</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-4">
                        <h4 className="text-xs font-bold uppercase text-muted-foreground mb-2">Avg. Execution Time</h4>
                        <div className="text-2xl font-black">12.4s</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-4">
                        <h4 className="text-xs font-bold uppercase text-muted-foreground mb-2">Error Rate</h4>
                        <div className="text-2xl font-black text-emerald-600">0.2%</div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
