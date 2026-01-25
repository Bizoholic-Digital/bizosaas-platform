'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import {
    ArrowLeft, Zap, Box, ShoppingCart, Mail,
    FileText, CheckCircle2, Loader2, ArrowRight
} from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { useAuth } from '../../../../components/auth/AuthProvider';
import { toast } from 'sonner';

const TEMPLATES = [
    {
        id: 'blank',
        name: 'Blank Workflow',
        description: 'Start from scratch with an empty canvas',
        icon: Box,
        color: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
    },
    {
        id: 'marketing_email',
        name: 'Marketing Sequence',
        description: 'Automated email follow-ups for new leads',
        icon: Mail,
        color: 'bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-400',
        type: 'Marketing'
    },
    {
        id: 'ecommerce_sync',
        name: 'Inventory Sync',
        description: 'Sync products between WooCommerce and ERP',
        icon: ShoppingCart,
        color: 'bg-purple-100 text-purple-600 dark:bg-purple-900/40 dark:text-purple-400',
        type: 'E-commerce'
    },
    {
        id: 'content_generation',
        name: 'Content Generator',
        description: 'AI-powered blog post generation workflow',
        icon: FileText,
        color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/40 dark:text-orange-400',
        type: 'Content'
    }
];

export default function CreateWorkflowPage() {
    const router = useRouter();
    const { getToken } = useAuth();
    const [step, setStep] = useState(1);
    const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Form State
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        trigger: 'webhook' // default
    });

    const handleSelectTemplate = (id: string) => {
        setSelectedTemplate(id);
        const template = TEMPLATES.find(t => t.id === id);
        if (template && id !== 'blank') {
            setFormData(prev => ({
                ...prev,
                name: template.name,
                description: template.description
            }));
        }
        setStep(2);
    };

    const handleCreate = async () => {
        if (!formData.name) {
            toast.error("Please provide a workflow name");
            return;
        }

        setIsSubmitting(true);
        try {
            const token = await getToken();
            await brainApi.workflows.create({
                ...formData,
                template_id: selectedTemplate,
                status: 'paused', // Start paused
                type: TEMPLATES.find(t => t.id === selectedTemplate)?.type || 'Custom'
            }, token as string);

            toast.success("Workflow created successfully");
            router.push('/dashboard/workflows');
        } catch (error) {
            console.error(error);
            toast.error("Failed to create workflow");
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-4 md:p-8">
            {/* Header */}
            <div className="flex items-center gap-4 mb-8">
                <Link href="/dashboard/workflows">
                    <Button variant="ghost" size="icon" className="rounded-full">
                        <ArrowLeft className="w-5 h-5" />
                    </Button>
                </Link>
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Create New Workflow</h1>
                    <p className="text-muted-foreground">Automate your business processes</p>
                </div>
            </div>

            {/* Steps Indicator */}
            <div className="flex items-center gap-4 mb-8">
                <div className={`flex items-center gap-2 ${step >= 1 ? 'text-purple-600' : 'text-slate-400'}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold border-2 ${step >= 1 ? 'border-purple-600 bg-purple-50' : 'border-slate-300'}`}>1</div>
                    <span className="font-medium hidden md:inline">Select Template</span>
                </div>
                <div className="h-0.5 w-12 bg-slate-200" />
                <div className={`flex items-center gap-2 ${step >= 2 ? 'text-purple-600' : 'text-slate-400'}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold border-2 ${step >= 2 ? 'border-purple-600 bg-purple-50' : 'border-slate-300'}`}>2</div>
                    <span className="font-medium hidden md:inline">Configuration</span>
                </div>
            </div>

            {/* Step 1: Templates */}
            {step === 1 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {TEMPLATES.map((template) => (
                        <Card
                            key={template.id}
                            className="cursor-pointer hover:border-purple-500 hover:shadow-md transition-all group"
                            onClick={() => handleSelectTemplate(template.id)}
                        >
                            <CardContent className="p-6 flex items-start gap-4">
                                <div className={`w-12 h-12 rounded-lg flex items-center justify-center shrink-0 ${template.color}`}>
                                    <template.icon className="w-6 h-6" />
                                </div>
                                <div className="space-y-1">
                                    <h3 className="font-bold text-lg group-hover:text-purple-600 transition-colors">{template.name}</h3>
                                    <p className="text-sm text-muted-foreground">{template.description}</p>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            {/* Step 2: Configuration */}
            {step === 2 && (
                <div className="max-w-2xl mx-auto space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Workflow Details</CardTitle>
                            <CardDescription>Configure the basic settings for your new workflow.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label>Workflow Name</Label>
                                <Input
                                    placeholder="e.g. Daily Sales Report"
                                    value={formData.name}
                                    onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                                />
                            </div>

                            <div className="space-y-2">
                                <Label>Description</Label>
                                <Textarea
                                    placeholder="Describe what this workflow does..."
                                    value={formData.description}
                                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                                />
                            </div>

                            <div className="space-y-2">
                                <Label>Trigger Type</Label>
                                <div className="grid grid-cols-2 gap-3">
                                    <div
                                        className={`p-3 border rounded-lg cursor-pointer flex items-center gap-3 ${formData.trigger === 'webhook' ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'hover:bg-slate-50 dark:hover:bg-slate-800'}`}
                                        onClick={() => setFormData(prev => ({ ...prev, trigger: 'webhook' }))}
                                    >
                                        <Zap className="w-4 h-4 text-orange-500" />
                                        <div className="text-sm font-medium">Webhook</div>
                                    </div>
                                    <div
                                        className={`p-3 border rounded-lg cursor-pointer flex items-center gap-3 ${formData.trigger === 'schedule' ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'hover:bg-slate-50 dark:hover:bg-slate-800'}`}
                                        onClick={() => setFormData(prev => ({ ...prev, trigger: 'schedule' }))}
                                    >
                                        <div className="w-4 h-4 rounded-full border-2 border-slate-400" />
                                        <div className="text-sm font-medium">Schedule</div>
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                        <CardFooter className="flex justify-between">
                            <Button variant="outline" onClick={() => setStep(1)}>Back</Button>
                            <Button onClick={handleCreate} disabled={isSubmitting} className="bg-purple-600 hover:bg-purple-700">
                                {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <CheckCircle2 className="w-4 h-4 mr-2" />}
                                Create Workflow
                            </Button>
                        </CardFooter>
                    </Card>
                </div>
            )}
        </div>
    );
}
