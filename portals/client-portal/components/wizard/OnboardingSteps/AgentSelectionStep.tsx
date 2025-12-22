import React from 'react';
import { AgentConfig } from '../types/onboarding';
import { Bot, Briefcase, MessagesSquare, Sparkles, User } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface Props {
    data: AgentConfig;
    onUpdate: (data: Partial<AgentConfig>) => void;
}

const PERSONAS = [
    {
        id: 'marketing_manager',
        title: 'Marketing Manager',
        icon: Sparkles,
        description: 'Strategizes campaigns, manages content, and optimizes ROI.'
    },
    {
        id: 'sales_rep',
        title: 'Sales Representative',
        icon: Briefcase,
        description: 'Engages leads, follows up, and closes deals.'
    },
    {
        id: 'support_agent',
        title: 'Support Specialist',
        icon: MessagesSquare,
        description: 'Handles customer inquiries and resolves issues 24/7.'
    },
    {
        id: 'general_assistant',
        title: 'General Assistant',
        icon: Bot,
        description: 'Helps with scheduling, reminders, and basic tasks.'
    }
];

export function AgentSelectionStep({ data, onUpdate }: Props) {
    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Setup Your AI Agent</h2>
                <p className="text-gray-500">Choose a persona to help manage your business.</p>
            </div>

            <div className="grid md:grid-cols-2 gap-4 mb-8">
                {PERSONAS.map(persona => {
                    const Icon = persona.icon;
                    const isSelected = data.persona === persona.id;
                    return (
                        <Card
                            key={persona.id}
                            className={`cursor-pointer transition-all border-2 ${isSelected ? 'border-blue-500 bg-blue-50/20' : 'border-transparent hover:border-gray-200'
                                }`}
                            onClick={() => onUpdate({ persona: persona.id as any })}
                        >
                            <CardContent className="p-4 flex items-start gap-4">
                                <div className={`p-3 rounded-lg ${isSelected ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-500'}`}>
                                    <Icon size={24} />
                                </div>
                                <div>
                                    <h3 className={`font-semibold ${isSelected ? 'text-blue-900' : 'text-gray-900'}`}>
                                        {persona.title}
                                    </h3>
                                    <p className="text-sm text-gray-500 mt-1">
                                        {persona.description}
                                    </p>
                                </div>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>

            <div className="grid md:grid-cols-2 gap-6 bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
                <div className="space-y-2">
                    <Label>Agent Name</Label>
                    <div className="relative">
                        <User className="absolute left-3 top-3 text-gray-400" size={18} />
                        <Input
                            value={data.name}
                            onChange={(e) => onUpdate({ name: e.target.value })}
                            className="pl-10"
                            placeholder="e.g. Alex"
                        />
                    </div>
                </div>

                <div className="space-y-2">
                    <Label>Communication Tone</Label>
                    <Select
                        value={data.tone}
                        onValueChange={(val: any) => onUpdate({ tone: val })}
                    >
                        <SelectTrigger>
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="professional">Professional & Formal</SelectItem>
                            <SelectItem value="friendly">Friendly & Casual</SelectItem>
                            <SelectItem value="witty">Witty & engaging</SelectItem>
                            <SelectItem value="urgent">Direct & Action-Oriented</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg flex gap-3 text-sm text-blue-700">
                <Bot className="shrink-0" size={20} />
                <p>
                    "Hi! I'm <strong>{data.name}</strong>. I'll act as your <strong>{PERSONAS.find(p => p.id === data.persona)?.title}</strong> using a <strong>{data.tone}</strong> tone."
                </p>
            </div>
        </div>
    );
}
