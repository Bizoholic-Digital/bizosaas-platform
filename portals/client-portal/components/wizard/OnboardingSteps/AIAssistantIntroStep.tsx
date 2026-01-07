import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Bot, Sparkles, ShieldCheck, Zap, ArrowRight } from 'lucide-react';

interface Props {
    discovery: any;
    agent: any;
    onUpdate: (data: any) => void;
    onNext: () => void;
}

export function AIAssistantIntroStep({ discovery, agent, onUpdate, onNext }: Props) {
    const googleDetected = discovery?.google?.filter((s: any) => s.status === 'detected') || [];
    const microsoftDetected = discovery?.microsoft?.filter((s: any) => s.status === 'detected') || [];
    const totalDetected = googleDetected.length + microsoftDetected.length;

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
            <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-2xl mb-4 text-blue-600">
                    <Bot size={32} />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 tracking-tight">Meet Your AI Success Manager</h2>
                <p className="text-gray-500 mt-2 text-lg">Your dedicated advocate for seamless growth.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="border-2 border-blue-100 bg-blue-50/30 overflow-hidden relative">
                    <CardContent className="p-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Sparkles className="text-blue-600" size={20} />
                            <h3 className="font-bold text-gray-900">Programmatic Setup</h3>
                        </div>
                        <p className="text-sm text-gray-600 mb-6">
                            We've identified <strong>{totalDetected} services</strong> linked to your accounts.
                            My team can automatically configure them for you, saving hours of manual work.
                        </p>

                        <div className="space-y-2">
                            {googleDetected.map((s: any) => (
                                <div key={s.id} className="flex items-center justify-between bg-white px-3 py-2 rounded-lg border border-blue-100 text-xs shadow-sm">
                                    <span className="text-gray-700 font-medium">{s.name}</span>
                                    <Badge variant="secondary" className="bg-green-100 text-green-700 hover:bg-green-100 border-0">Ready</Badge>
                                </div>
                            ))}
                            {microsoftDetected.map((s: any) => (
                                <div key={s.id} className="flex items-center justify-between bg-white px-3 py-2 rounded-lg border border-blue-100 text-xs shadow-sm">
                                    <span className="text-gray-700 font-medium">{s.name}</span>
                                    <Badge variant="secondary" className="bg-blue-100 text-blue-700 hover:bg-blue-100 border-0">Ready</Badge>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                <div className="space-y-4">
                    <div className="flex gap-4 items-start p-4 bg-white rounded-xl border-gray-100 border">
                        <div className="p-2 bg-green-50 text-green-600 rounded-lg">
                            <ShieldCheck size={20} />
                        </div>
                        <div>
                            <h4 className="font-semibold text-gray-900">Safe & Secure</h4>
                            <p className="text-sm text-gray-500 line-clamp-2">Only relevant marketing and business data is accessed. No personal data shared.</p>
                        </div>
                    </div>

                    <div className="flex gap-4 items-start p-4 bg-white rounded-xl border-gray-100 border">
                        <div className="p-2 bg-orange-50 text-orange-600 rounded-lg">
                            <Zap size={20} />
                        </div>
                        <div>
                            <h4 className="font-semibold text-gray-900">One-Click Enablement</h4>
                            <p className="text-sm text-gray-500 line-clamp-2">If a service isn't active on your console, we'll provision it programmatically.</p>
                        </div>
                    </div>

                    <div className="pt-4">
                        <Button
                            onClick={onNext}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-6 rounded-xl shadow-lg flex items-center justify-center gap-2 group"
                        >
                            Confirm Team & Proceed
                            <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                        </Button>
                        <p className="text-[10px] text-gray-400 text-center mt-3">
                            By proceeding, you authorize your AI CSM to coordinate with your connected accounts.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
