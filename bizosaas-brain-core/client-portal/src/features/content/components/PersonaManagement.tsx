'use client';

import React, { useState, useEffect } from 'react';
import {
    User,
    Sparkles,
    Globe,
    Settings,
    RefreshCw,
    Save,
    Check,
    Zap,
    Twitter,
    Linkedin,
    Facebook,
    Instagram,
    ChevronRight,
    Info
} from 'lucide-react';
import { brainGateway } from '@/lib/brain-gateway-client';
import { cn } from '@/lib/utils';
import { Persona } from '@/lib/brain-gateway-client/clients/persona';

export function PersonaManagement() {
    const [persona, setPersona] = useState<Persona | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isGenerating, setIsGenerating] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [websiteUrl, setWebsiteUrl] = useState('');
    const [activeTab, setActiveTab] = useState<'core' | 'platforms'>('core');

    useEffect(() => {
        fetchPersona();
    }, []);

    const fetchPersona = async () => {
        setIsLoading(true);
        try {
            const data = await brainGateway.persona.getPersona();
            if (data && data.core_persona) {
                setPersona(data);
            }
        } catch (error) {
            console.error('Failed to fetch persona:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerate = async () => {
        setIsGenerating(true);
        try {
            const res = await brainGateway.persona.generatePersona({
                website_url: websiteUrl,
            });
            // In a real app, we'd poll for workflow completion.
            // For now, we'll show a "Generating" state and refresh after a delay.
            setTimeout(fetchPersona, 10000);
        } catch (error) {
            console.error('Failed to start persona generation:', error);
        } finally {
            setIsGenerating(false);
        }
    };

    const handleUpdate = async () => {
        if (!persona) return;
        setIsSaving(true);
        try {
            await brainGateway.persona.updatePersona(persona);
        } catch (error) {
            console.error('Failed to update persona:', error);
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center p-24">
                <RefreshCw className="w-8 h-8 text-indigo-500 animate-spin" />
            </div>
        );
    }

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 tracking-tight flex items-center gap-3">
                        <User className="w-8 h-8 text-indigo-600" />
                        Persona & Brand Voice
                    </h1>
                    <p className="text-gray-500 mt-1">Design how your AI agents represent your brand across the web.</p>
                </div>

                <div className="flex items-center gap-3">
                    {persona && (
                        <button
                            onClick={handleUpdate}
                            disabled={isSaving}
                            className="px-4 py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all flex items-center gap-2 font-medium shadow-sm disabled:opacity-50"
                        >
                            {isSaving ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                            Save Changes
                        </button>
                    )}
                </div>
            </div>

            {!persona ? (
                <div className="bg-white rounded-2xl border-2 border-dashed border-gray-200 p-12 text-center max-w-2xl mx-auto">
                    <div className="w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-6">
                        <Sparkles className="w-8 h-8 text-indigo-600" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900">Define Your Brand Persona</h3>
                    <p className="text-gray-500 mt-2 mb-8 text-lg">
                        Our AI can autonomously extract your brand voice from your website or onboarding data.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-3">
                        <input
                            type="text"
                            placeholder="e.g., https://yourbrand.com"
                            className="flex-1 px-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all shadow-sm"
                            value={websiteUrl}
                            onChange={(e) => setWebsiteUrl(e.target.value)}
                        />
                        <button
                            onClick={handleGenerate}
                            disabled={isGenerating}
                            className="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-all flex items-center justify-center gap-2 font-bold whitespace-nowrap shadow-md"
                        >
                            {isGenerating ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Zap className="w-5 h-5" />}
                            Generate AI Persona
                        </button>
                    </div>
                    <p className="text-xs text-gray-400 mt-4 flex items-center justify-center gap-1">
                        <Info className="w-3 h-3" />
                        Generating a persona takes about 30-60 seconds of AI processing.
                    </p>
                </div>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                    {/* Sidebar Tabs */}
                    <div className="lg:col-span-1 space-y-2">
                        <button
                            onClick={() => setActiveTab('core')}
                            className={cn(
                                "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium text-left",
                                activeTab === 'core'
                                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-200"
                                    : "bg-white text-gray-600 hover:bg-gray-50 border border-transparent"
                            )}
                        >
                            <User className="w-5 h-5" />
                            Core Persona
                        </button>
                        <button
                            onClick={() => setActiveTab('platforms')}
                            className={cn(
                                "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium text-left",
                                activeTab === 'platforms'
                                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-200"
                                    : "bg-white text-gray-600 hover:bg-gray-50 border border-transparent"
                            )}
                        >
                            <Globe className="w-5 h-5" />
                            Platform Adapters
                        </button>
                    </div>

                    {/* Main Form Content */}
                    <div className="lg:col-span-3">
                        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-8">
                            {activeTab === 'core' ? (
                                <div className="space-y-6">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <label className="text-sm font-bold text-gray-700 uppercase tracking-tight">Identity Name</label>
                                            <input
                                                type="text"
                                                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                                                value={persona.core_persona.name}
                                                onChange={(e) => setPersona({ ...persona, core_persona: { ...persona.core_persona, name: e.target.value } })}
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm font-bold text-gray-700 uppercase tracking-tight">Role / Title</label>
                                            <input
                                                type="text"
                                                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                                                value={persona.core_persona.role}
                                                onChange={(e) => setPersona({ ...persona, core_persona: { ...persona.core_persona, role: e.target.value } })}
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="space-y-2">
                                            <label className="text-sm font-bold text-gray-700 uppercase tracking-tight">Tone</label>
                                            <input
                                                type="text"
                                                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                                                value={persona.core_persona.tone}
                                                onChange={(e) => setPersona({ ...persona, core_persona: { ...persona.core_persona, tone: e.target.value } })}
                                            />
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-sm font-bold text-gray-700 uppercase tracking-tight">Writing Style</label>
                                            <input
                                                type="text"
                                                className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                                                value={persona.core_persona.style}
                                                onChange={(e) => setPersona({ ...persona, core_persona: { ...persona.core_persona, style: e.target.value } })}
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <label className="text-sm font-bold text-gray-700 uppercase tracking-tight">Detailed Persona Description</label>
                                        <textarea
                                            rows={5}
                                            className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                                            value={persona.core_persona.description}
                                            onChange={(e) => setPersona({ ...persona, core_persona: { ...persona.core_persona, description: e.target.value } })}
                                        />
                                    </div>
                                </div>
                            ) : (
                                <div className="space-y-8">
                                    <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl flex gap-3 items-start">
                                        <Sparkles className="w-5 h-5 text-amber-600 mt-0.5" />
                                        <div>
                                            <h4 className="text-sm font-bold text-amber-900 uppercase">Proactive Adaptation</h4>
                                            <p className="text-sm text-amber-800">These platform variants are automatically derived from your core persona to fit specific social network norms.</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 gap-6">
                                        {[
                                            { name: 'Twitter / X', icon: Twitter, key: 'twitter' },
                                            { name: 'LinkedIn', icon: Linkedin, key: 'linkedin' },
                                            { name: 'Facebook', icon: Facebook, key: 'facebook' },
                                            { name: 'Instagram', icon: Instagram, key: 'instagram' },
                                        ].map((platform) => (
                                            <div key={platform.key} className="flex items-start gap-6 p-6 rounded-2xl border border-gray-100 bg-gray-50/50">
                                                <div className="p-3 bg-white rounded-xl shadow-sm border border-gray-100">
                                                    <platform.icon className="w-6 h-6 text-gray-700" />
                                                </div>
                                                <div className="flex-1 space-y-3">
                                                    <div className="flex items-center justify-between">
                                                        <h4 className="font-bold text-gray-900">{platform.name}</h4>
                                                        <span className="text-[10px] font-bold uppercase text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">Active</span>
                                                    </div>
                                                    <p className="text-sm text-gray-600 leading-relaxed italic">
                                                        {persona.platform_variants?.[platform.key]?.description || `Auto-adapting ${persona.core_persona.name} for ${platform.name} content...`}
                                                    </p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
