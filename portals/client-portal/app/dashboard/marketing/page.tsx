'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import {
    Mail, Users, Send, Loader2, Plus, Edit, Trash2,
    MoreVertical, Sparkles, BarChart3, TrendingUp,
    Target, MessageSquare, BrainCircuit, ArrowUpRight,
    Zap, RefreshCw, Rocket, Globe, Megaphone, Share2, CheckCircle2, AlertCircle
} from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import { ScrollArea } from '@/components/ui/scroll-area';
import { CampaignWizardSelector } from '@/components/CampaignWizardSelector';

interface Campaign {
    id: string;
    name: string;
    status: string;
    type: string;
    subject?: string;
    stats?: {
        open_rate: number;
        click_rate: number;
        emails_sent: number;
    }
}

export default function MarketingPage() {
    const { isConnected: isMailchimpConnected, isLoading: statusLoading } = useConnectorStatus('mailchimp', 'marketing');
    const [campaigns, setCampaigns] = useState<Campaign[]>([
        { id: '1', name: 'Winter Flash Sale', status: 'running', type: 'Google Ads', stats: { open_rate: 0, click_rate: 3.4, emails_sent: 0 } },
        { id: '2', name: 'New Year Newsletter', status: 'sent', type: 'Email', stats: { open_rate: 24.5, click_rate: 1.2, emails_sent: 12500 } },
        { id: '3', name: 'Social Brand Awareness', status: 'paused', type: 'Social Media', stats: { open_rate: 0, click_rate: 0.8, emails_sent: 0 } }
    ]);
    const [isLoadingData, setIsLoadingData] = useState(false);
    const [activeTab, setActiveTab] = useState('hub');
    const [showWizard, setShowWizard] = useState(false);

    const [aiInsights] = useState([
        {
            title: "Optimize Ad Targeting",
            content: "Your Google Ads 'Winter Flash Sale' is performing 15% better in Southeast regions. Consider shifting 10% budget from Northeast to maximize ROI.",
            type: 'info'
        },
        {
            title: "Email Personalization Boost",
            content: "Adding first names to subject lines in your next newsletter is predicted to increase open rates by 8.4%.",
            type: 'success'
        }
    ]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            const campaignsData = await brainApi.marketing.getCampaigns().catch(() => ({ data: [] }));
            if (campaignsData.data?.length > 0) {
                setCampaigns(prev => [...prev, ...campaignsData.data]);
            }
        } catch (error) {
            console.error('Failed to load marketing data:', error);
        } finally {
            setIsLoadingData(false);
        }
    };

    if (statusLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (showWizard) {
        return (
            <div className="p-6">
                <Button variant="ghost" className="mb-4" onClick={() => setShowWizard(false)}>
                    &larr; Back to Dashboard
                </Button>
                <CampaignWizardSelector />
            </div>
        );
    }

    return (
        <div className="p-6 space-y-6">
            {/* Header section with Premium feel */}
            <div className="flex flex-col md:flex-row md:items-center justify-end gap-4">
                <div className="flex items-center gap-2">
                    <Button variant="outline" className="gap-2 h-11" onClick={loadData}>
                        <RefreshCw className={`w-4 h-4 ${isLoadingData ? 'animate-spin' : ''}`} />
                        Sync Platforms
                    </Button>
                    <Button className="bg-blue-600 hover:bg-blue-700 text-white shadow-xl shadow-blue-500/20 h-11 px-6 rounded-xl font-bold gap-2"
                        onClick={() => setShowWizard(true)}>
                        <Rocket className="w-5 h-5" />
                        Launch New Campaign
                    </Button>
                </div>
            </div>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="border-none bg-indigo-50 dark:bg-indigo-950/20 shadow-sm border-l-4 border-l-indigo-500">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Target className="w-5 h-5 text-indigo-600" />
                            <Badge variant="secondary" className="bg-indigo-100 text-indigo-700">Active</Badge>
                        </div>
                        <p className="text-xs font-bold text-indigo-800 dark:text-indigo-300 uppercase tracking-widest">Total Ads Budget</p>
                        <h3 className="text-3xl font-black mt-1 text-indigo-950 dark:text-indigo-50">$12,450.00</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-emerald-50 dark:bg-emerald-950/20 shadow-sm border-l-4 border-l-emerald-500">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <TrendingUp className="w-5 h-5 text-emerald-600" />
                            <Badge variant="secondary" className="bg-emerald-100 text-emerald-700">+18.2%</Badge>
                        </div>
                        <p className="text-xs font-bold text-emerald-800 dark:text-emerald-300 uppercase tracking-widest">Total Conversions</p>
                        <h3 className="text-3xl font-black mt-1 text-emerald-950 dark:text-emerald-50">842</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-blue-50 dark:bg-blue-950/20 shadow-sm border-l-4 border-l-blue-500">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Send className="w-5 h-5 text-blue-600" />
                            <Badge variant="secondary" className="bg-blue-100 text-blue-700">Omni</Badge>
                        </div>
                        <p className="text-xs font-bold text-blue-800 dark:text-blue-300 uppercase tracking-widest">Global Reach</p>
                        <h3 className="text-3xl font-black mt-1 text-blue-950 dark:text-blue-50">45.2K</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-amber-50 dark:bg-amber-950/20 shadow-sm border-l-4 border-l-amber-500">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <BrainCircuit className="w-5 h-5 text-amber-600" />
                            <Badge variant="secondary" className="bg-amber-100 text-amber-700">Optimal</Badge>
                        </div>
                        <p className="text-xs font-bold text-amber-800 dark:text-amber-300 uppercase tracking-widest">AI Efficiency Score</p>
                        <h3 className="text-3xl font-black mt-1 text-amber-950 dark:text-amber-50">94/100</h3>
                    </CardContent>
                </Card>
            </div>

            {/* Main Content Tabs */}
            <Tabs defaultValue="hub" className="w-full" onValueChange={setActiveTab}>
                <div className="overflow-x-auto pb-2 -mx-2 px-2 scrollbar-hide">
                    <TabsList className="flex w-max md:w-full md:grid md:grid-cols-5 lg:w-[750px] mb-8 bg-slate-100/50 dark:bg-slate-800/50 p-1 rounded-xl">
                        <TabsTrigger value="hub" className="rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 whitespace-nowrap px-6 md:px-3">The Hub</TabsTrigger>
                        <TabsTrigger value="active" className="rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 whitespace-nowrap px-6 md:px-3">Live Campaigns</TabsTrigger>
                        <TabsTrigger value="ai-audit" className="rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 flex items-center gap-1 whitespace-nowrap px-6 md:px-3">
                            <Sparkles className="w-3.5 h-3.5 text-blue-500" /> AI Insights
                        </TabsTrigger>
                        <TabsTrigger value="audiences" className="rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 whitespace-nowrap px-6 md:px-3">Audiences</TabsTrigger>
                        <TabsTrigger value="connectors" className="rounded-lg data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 whitespace-nowrap px-6 md:px-3">Platforms</TabsTrigger>
                    </TabsList>
                </div>

                {/* Hub View Content */}
                <TabsContent value="hub" className="space-y-6 animate-in fade-in duration-500">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Featured Action Cards */}
                        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
                            <Card className="bg-gradient-to-br from-blue-600 to-blue-800 text-white border-none group cursor-pointer overflow-hidden"
                                onClick={() => setShowWizard(true)}>
                                <CardHeader>
                                    <Target className="w-10 h-10 mb-2 opacity-80 group-hover:scale-110 transition-transform" />
                                    <CardTitle>Google Ads Master</CardTitle>
                                    <CardDescription className="text-blue-100">Launch search, display and YouTube ads with AI bid optimization.</CardDescription>
                                </CardHeader>
                                <CardFooter>
                                    <Button variant="ghost" className="text-white hover:bg-white/10 w-full justify-between">
                                        Start Wizard <ArrowUpRight className="w-4 h-4" />
                                    </Button>
                                </CardFooter>
                            </Card>

                            <Card className="bg-gradient-to-br from-purple-600 to-indigo-800 text-white border-none group cursor-pointer overflow-hidden"
                                onClick={() => setShowWizard(true)}>
                                <CardHeader>
                                    <Share2 className="w-10 h-10 mb-2 opacity-80 group-hover:scale-110 transition-transform" />
                                    <CardTitle>Social Dominance</CardTitle>
                                    <CardDescription className="text-purple-100">Orchestrate Meta, LinkedIn and TikTok campaigns simultaneously.</CardDescription>
                                </CardHeader>
                                <CardFooter>
                                    <Button variant="ghost" className="text-white hover:bg-white/10 w-full justify-between">
                                        Open Social Lab <ArrowUpRight className="w-4 h-4" />
                                    </Button>
                                </CardFooter>
                            </Card>

                            <Card className="bg-gradient-to-br from-emerald-600 to-teal-800 text-white border-none group cursor-pointer overflow-hidden"
                                onClick={() => setShowWizard(true)}>
                                <CardHeader>
                                    <Mail className="w-10 h-10 mb-2 opacity-80 group-hover:scale-110 transition-transform" />
                                    <CardTitle>Email Automation</CardTitle>
                                    <CardDescription className="text-emerald-100">Configure drip sequences and behavior-based mailing lists.</CardDescription>
                                </CardHeader>
                                <CardFooter>
                                    <Button variant="ghost" className="text-white hover:bg-white/10 w-full justify-between">
                                        Design Sequence <ArrowUpRight className="w-4 h-4" />
                                    </Button>
                                </CardFooter>
                            </Card>

                            <Card className="bg-gradient-to-br from-orange-500 to-pink-600 text-white border-none group cursor-pointer overflow-hidden">
                                <CardHeader>
                                    <BarChart3 className="w-10 h-10 mb-2 opacity-80 group-hover:scale-110 transition-transform" />
                                    <CardTitle>Unified Analytics</CardTitle>
                                    <CardDescription className="text-orange-100">Compare ROAS across all channels in a single visual dashboard.</CardDescription>
                                </CardHeader>
                                <CardFooter>
                                    <Button variant="ghost" className="text-white hover:bg-white/10 w-full justify-between">
                                        View BI Portal <ArrowUpRight className="w-4 h-4" />
                                    </Button>
                                </CardFooter>
                            </Card>
                        </div>

                        {/* Recent Alerts & Quick News */}
                        <div className="space-y-6">
                            <Card className="bg-slate-900 text-white border-none">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm font-bold uppercase tracking-widest text-slate-400">Campaign Health</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="flex items-center justify-between">
                                        <span className="text-sm">Active Channels</span>
                                        <div className="flex -space-x-2">
                                            <div className="w-6 h-6 rounded-full bg-blue-500 border-2 border-slate-900" />
                                            <div className="w-6 h-6 rounded-full bg-purple-500 border-2 border-slate-900" />
                                            <div className="w-6 h-6 rounded-full bg-green-500 border-2 border-slate-900" />
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <div className="flex justify-between text-xs mb-1">
                                            <span>Budget Utilized</span>
                                            <span>84%</span>
                                        </div>
                                        <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                            <div className="bg-blue-500 h-full w-[84%]" />
                                        </div>
                                    </div>
                                    <Button className="w-full bg-slate-800 hover:bg-slate-700 border-none text-xs">Manage Global Spending</Button>
                                </CardContent>
                            </Card>

                            <Card>
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm font-bold">Latest AI Logs</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <ScrollArea className="h-[200px] pr-4">
                                        <div className="space-y-4">
                                            {[
                                                { time: '5m ago', msg: 'Adjusted Google bid on "CRM Software" +10%', icon: <Zap className="w-3 h-3 text-emerald-500" /> },
                                                { time: '1h ago', msg: 'Email bounce rate 0.2% - Optimal health', icon: <CheckCircle2 className="w-3 h-3 text-blue-500" /> },
                                                { time: '3h ago', msg: 'New audience segment "High Intent" created', icon: <Users className="w-3 h-3 text-purple-500" /> },
                                                { time: 'Yesterday', msg: 'Budget warning for LinkedIn: 95% spent', icon: <AlertCircle className="w-3 h-3 text-amber-500" /> }
                                            ].map((log, i) => (
                                                <div key={i} className="flex gap-3 items-start text-xs">
                                                    <div className="mt-1">{log.icon}</div>
                                                    <div>
                                                        <p className="font-semibold">{log.msg}</p>
                                                        <p className="text-muted-foreground">{log.time}</p>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </ScrollArea>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </TabsContent>

                {/* Live Campaigns View */}
                <TabsContent value="active" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {campaigns.map(campaign => (
                            <Card key={campaign.id} className="group hover:border-blue-400 hover:shadow-lg transition-all border-l-4"
                                style={{ borderLeftColor: campaign.status === 'running' ? '#3b82f6' : '#64748b' }}>
                                <CardHeader className="pb-2">
                                    <div className="flex items-center justify-between mb-2">
                                        <Badge className={campaign.status === 'running' ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-700'}>
                                            {campaign.status.toUpperCase()}
                                        </Badge>
                                        <Badge variant="outline">{campaign.type}</Badge>
                                    </div>
                                    <CardTitle className="text-xl font-bold">{campaign.name}</CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                                            <p className="text-[10px] text-muted-foreground uppercase font-bold">Performance</p>
                                            <div className="flex items-center gap-1 mt-1">
                                                <TrendingUp className="w-4 h-4 text-emerald-500" />
                                                <span className="text-lg font-black">{campaign.stats?.click_rate || '3.2'}%</span>
                                            </div>
                                        </div>
                                        <div className="p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl">
                                            <p className="text-[10px] text-muted-foreground uppercase font-bold">Engagement</p>
                                            <div className="flex items-center gap-1 mt-1">
                                                <Users className="w-4 h-4 text-blue-500" />
                                                <span className="text-lg font-black">{campaign.stats?.emails_sent ? (campaign.stats.emails_sent / 1000).toFixed(1) + 'K' : 'Active'}</span>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                                <CardFooter className="pt-2 border-t mt-4 flex gap-2">
                                    <Button variant="ghost" size="sm" className="flex-1">Edit</Button>
                                    <Button variant="ghost" size="sm" className="flex-1 text-blue-600">Full Data</Button>
                                    <Button variant="ghost" size="icon" className="text-red-500"><Trash2 className="w-4 h-4" /></Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                {/* AI Insights Content */}
                <TabsContent value="ai-audit" className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                        <div className="lg:col-span-3 space-y-6">
                            <h3 className="text-2xl font-black flex items-center gap-2">
                                <Sparkles className="w-6 h-6 text-blue-500" />
                                Agent Recommendations
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {aiInsights.map((insight, i) => (
                                    <Card key={i} className="bg-white dark:bg-slate-900 border-2 border-blue-100 dark:border-blue-900/30 overflow-hidden">
                                        <div className="bg-blue-600 h-1.5 w-full" />
                                        <CardHeader>
                                            <CardTitle className="text-lg flex items-center gap-2">
                                                <BrainCircuit className="w-5 h-5 text-blue-600" />
                                                {insight.title}
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="text-sm text-muted-foreground leading-relaxed">{insight.content}</p>
                                        </CardContent>
                                        <CardFooter className="bg-slate-50 dark:bg-slate-800/50 py-3">
                                            <Button variant="link" className="text-blue-600 font-bold p-0">Execute with Agent &rarr;</Button>
                                        </CardFooter>
                                    </Card>
                                ))}
                            </div>

                            <Card className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white border-none p-8 relative overflow-hidden">
                                <div className="relative z-10 max-w-lg">
                                    <h2 className="text-3xl font-black mb-4 flex items-center gap-3">
                                        <MessageSquare className="w-8 h-8 text-blue-400" />
                                        Chat with Marketing Agent
                                    </h2>
                                    <p className="text-slate-300 mb-6">Ask your dedicated AI Marketing Strategist to analyze campaigns, project future ROAS, or generate ad copy for your next launch.</p>
                                    <div className="flex gap-2">
                                        <Input className="bg-slate-800/80 border-slate-700 h-12 text-lg" placeholder="e.g. 'Audit my Google Ads budget for this month'" />
                                        <Button className="h-12 bg-blue-600 hover:bg-blue-700 px-8 font-bold">Consult</Button>
                                    </div>
                                </div>
                                <div className="absolute -right-20 -bottom-20 opacity-10 rotate-12">
                                    <BrainCircuit className="w-96 h-96" />
                                </div>
                            </Card>
                        </div>

                        <div className="space-y-6">
                            <Card className="bg-gradient-to-b from-blue-600 to-blue-800 text-white border-none p-6 shadow-2xl">
                                <p className="text-xs font-bold uppercase tracking-widest text-blue-200 mb-2">Industry Percentile</p>
                                <div className="text-5xl font-black">92%</div>
                                <p className="text-sm mt-4 text-blue-100 leading-relaxed">Your campaign efficiency is in the <span className="font-bold">top 8%</span> of your vertical. AI optimization is working exceptionally well.</p>
                            </Card>

                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-sm font-bold">Optimization Log</CardTitle>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <ScrollArea className="h-[300px] px-6">
                                        <div className="pb-6 divide-y">
                                            {[...Array(5)].map((_, i) => (
                                                <div key={i} className="py-4">
                                                    <div className="flex items-center gap-2 mb-1">
                                                        <div className="w-2 h-2 rounded-full bg-emerald-500" />
                                                        <span className="text-xs font-bold uppercase tracking-wider">Bid Adjusted</span>
                                                    </div>
                                                    <p className="text-sm font-medium">Changed bid for "Marketing Platform" from $4.20 to $4.55 in Group B.</p>
                                                    <p className="text-[10px] text-muted-foreground mt-1">Today at {10 - i}:00 AM</p>
                                                </div>
                                            ))}
                                        </div>
                                    </ScrollArea>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </TabsContent>

                {/* Platforms/Connectors View */}
                <TabsContent value="connectors" className="animate-in fade-in duration-700">
                    <Card className="border-2 border-dashed border-slate-200 dark:border-slate-800 p-12 text-center bg-slate-50/30 dark:bg-slate-900/20">
                        <Globe className="w-16 h-16 text-slate-300 mx-auto mb-4" />
                        <h3 className="text-xl font-bold">Connected Marketing Stack</h3>
                        <p className="text-muted-foreground max-w-sm mx-auto mt-2">Manage your integrations with Google, Meta, Mailchimp, and other advertising platforms.</p>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mt-12">
                            <Card className="flex items-center p-4 gap-4">
                                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                                    <Target className="w-6 h-6 text-blue-600" />
                                </div>
                                <div className="text-left flex-1">
                                    <p className="font-bold text-sm">Google Ads</p>
                                    <Badge variant="outline" className="text-[10px] text-green-600 font-bold border-green-200">Connected</Badge>
                                </div>
                                <Button size="sm" variant="ghost" className="text-xs">Settings</Button>
                            </Card>

                            <Card className="flex items-center p-4 gap-4">
                                <div className="w-12 h-12 bg-amber-100 dark:bg-amber-900/30 rounded-lg flex items-center justify-center">
                                    <Mail className="w-6 h-6 text-amber-600" />
                                </div>
                                <div className="text-left flex-1">
                                    <p className="font-bold text-sm">Mailchimp</p>
                                    <Badge variant="outline" className={`text-[10px] font-bold ${isMailchimpConnected ? 'text-green-600 border-green-200' : 'text-slate-400'}`}>
                                        {isMailchimpConnected ? 'Connected' : 'Disconnected'}
                                    </Badge>
                                </div>
                                <Button size="sm" variant="ghost" className="text-xs">Configure</Button>
                            </Card>

                            <Card className="flex items-center p-4 gap-4">
                                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                                    <Users className="w-6 h-6 text-purple-600" />
                                </div>
                                <div className="text-left flex-1">
                                    <p className="font-bold text-sm">Meta Business</p>
                                    <Badge variant="outline" className="text-[10px] text-slate-400">Not Linked</Badge>
                                </div>
                                <Button size="sm" className="bg-purple-600 text-white text-xs">Connect</Button>
                            </Card>
                        </div>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
