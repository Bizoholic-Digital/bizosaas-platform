'use client';

import React from 'react';
import { Loader2, CheckCircle2, XCircle, Clock, Activity, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

export interface WorkflowStep {
    id: string;
    name: string;
    status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
    description?: string;
    timestamp?: string;
}

export interface WorkflowProgressProps {
    workflowId: string;
    name: string;
    status: 'RUNNING' | 'COMPLETED' | 'FAILED' | 'PENDING';
    progress: number;
    steps: WorkflowStep[];
    type: 'client' | 'admin';
    className?: string;
}

export function WorkflowStatus({
    workflowId,
    name,
    status,
    progress,
    steps,
    type,
    className
}: WorkflowProgressProps) {
    const getStatusIcon = (s: string) => {
        switch (s) {
            case 'RUNNING': return <Loader2 className="w-4 h-4 animate-spin text-blue-500" />;
            case 'COMPLETED': return <CheckCircle2 className="w-4 h-4 text-green-500" />;
            case 'FAILED': return <XCircle className="w-4 h-4 text-red-500" />;
            default: return <Clock className="w-4 h-4 text-slate-400" />;
        }
    };

    const getStatusColor = (s: string) => {
        switch (s) {
            case 'RUNNING': return 'bg-blue-500';
            case 'COMPLETED': return 'bg-green-500';
            case 'FAILED': return 'bg-red-500';
            default: return 'bg-slate-300';
        }
    };

    return (
        <Card className={cn("overflow-hidden border-slate-200 dark:border-slate-800 shadow-sm", className)}>
            <CardHeader className="pb-4 bg-slate-50/50 dark:bg-slate-900/50 border-b border-slate-100 dark:border-slate-800">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className={cn("p-2 rounded-lg bg-white dark:bg-slate-800 shadow-sm border border-slate-200 dark:border-slate-700")}>
                            <Activity className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                            <CardTitle className="text-base font-semibold">{name}</CardTitle>
                            <CardDescription className="text-xs font-mono">{workflowId}</CardDescription>
                        </div>
                    </div>
                    <Badge variant={status === 'COMPLETED' ? 'secondary' : status === 'FAILED' ? 'destructive' : 'outline'}>
                        {status}
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="pt-6 space-y-6">
                {/* Progress Bar */}
                <div className="space-y-2">
                    <div className="flex justify-between text-xs font-medium">
                        <span>Progress</span>
                        <span>{Math.round(progress)}%</span>
                    </div>
                    <Progress value={progress} className="h-2" />
                </div>

                {/* Steps List */}
                <div className="space-y-4">
                    <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Execution Steps</p>
                    <div className="relative space-y-0.6">
                        {steps.map((step, index) => (
                            <div key={step.id} className="relative flex gap-4 pb-4 last:pb-0">
                                {/* Connector Line */}
                                {index < steps.length - 1 && (
                                    <div className="absolute left-[7px] top-4 bottom-0 w-[2px] bg-slate-100 dark:bg-slate-800" />
                                )}

                                <div className="relative z-10 mt-0.5">
                                    <div className={cn(
                                        "w-4 h-4 rounded-full flex items-center justify-center bg-white dark:bg-slate-900 border-2",
                                        step.status === 'COMPLETED' ? "border-green-500" :
                                            step.status === 'RUNNING' ? "border-blue-500" : "border-slate-300 dark:border-slate-700"
                                    )}>
                                        {step.status === 'COMPLETED' && <div className="w-1.5 h-1.5 rounded-full bg-green-500" />}
                                        {step.status === 'RUNNING' && <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />}
                                    </div>
                                </div>

                                <div className="flex-1 space-y-1">
                                    <div className="flex items-center justify-between">
                                        <p className={cn(
                                            "text-sm font-medium",
                                            step.status === 'COMPLETED' ? "text-slate-900 dark:text-white" : "text-slate-500"
                                        )}>
                                            {step.name}
                                        </p>
                                        {step.timestamp && (
                                            <span className="text-[10px] text-slate-400 font-mono">{step.timestamp}</span>
                                        )}
                                    </div>
                                    {step.description && (
                                        <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">
                                            {step.description}
                                        </p>
                                    )}
                                    {type === 'admin' && step.status === 'FAILED' && (
                                        <div className="mt-2 p-2 rounded bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/30">
                                            <p className="text-xs text-red-600 dark:text-red-400 font-mono break-all font-semibold">
                                                Error: Traceback captured in logs...
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {status === 'COMPLETED' && (
                    <Button variant="outline" size="sm" className="w-full mt-2 group">
                        View Results
                        <ArrowRight className="w-3 h-3 ml-2 group-hover:translate-x-1 transition-transform" />
                    </Button>
                )}
            </CardContent>
        </Card>
    );
}
