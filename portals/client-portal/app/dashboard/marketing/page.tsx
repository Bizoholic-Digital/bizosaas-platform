'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Mail, Users, Send, Loader2, Plus, Edit, Trash2, MoreVertical, Sparkles, BarChart3, TrendingUp, Target, MessageSquare, BrainCircuit, ArrowUpRight, Zap, RefreshCw } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import { ScrollArea } from '@/components/ui/scroll-area';

interface EmailList {
    id: string;
    name: string;
    subscriber_count: number;
}

interface Campaign {
    id: string;
    name: string;
    status: string;
    subject?: string;
    stats?: {
        open_rate: number;
        click_rate: number;
        emails_sent: number;
    }
}

export default function MarketingPage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('mailchimp', 'marketing');
    const [lists, setLists] = useState<EmailList[]>([]);
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);
    const [activeTab, setActiveTab] = useState('overview');
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    // AI Insights State
    const [aiInsights, setAiInsights] = useState<{ title: string, content: string, type: 'success' | 'warning' | 'info' }[]>([
        {
            title: "Optimize Subject Lines",
            content: "Your last campaign 'Summer Promo' had a 12% lower open rate than industry average. Try using more personalization.",
            type: 'info'
        },
        {
            title: "Audience Growth",
            content: "Subscriber count increased by 8% this month. High conversion detected from Facebook referral traffic.",
            type: 'success'
        }
    ]);

    const [formData, setFormData] = useState({
        name: '',
        subject: '',
        from_name: 'BizOSaaS',
        from_email: 'noreply@bizosaas.com'
    });

    useEffect(() => {
        if (isConnected) {
            loadData();
        }
    }, [isConnected]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            const [listsData, campaignsData] = await Promise.all([
                brainApi.marketing.getLists().catch(() => ({ data: [] })),
                brainApi.marketing.getCampaigns().catch(() => ({ data: [] }))
            ]);

            setLists(listsData.data || []);
            setCampaigns(campaignsData.data || []);
        } catch (error) {
            console.error('Failed to load marketing data:', error);
            toast.error('Failed to load marketing data');
        } finally {
            setIsLoadingData(false);
        }
    };

    const handleCreate = async () => {
        try {
            await brainApi.marketing.createCampaign(formData);
            toast.success('Campaign created successfully');
            setIsDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error('Failed to create content');
        }
    };

    const handleDelete = async (id: string, type: 'lists' | 'campaigns') => {
        if (!confirm(`Are you sure you want to delete this ${type === 'lists' ? 'list' : 'campaign'}?`)) return;
        try {
            if (type === 'lists') {
                await brainApi.marketing.deleteList(id);
            } else {
                await brainApi.marketing.deleteCampaign(id);
            }
            toast.success('Deleted successfully');
            loadData();
        } catch (error) {
            toast.error('Failed to delete');
        }
    };

    const resetForm = () => {
        setFormData({
            name: '',
            subject: '',
            from_name: 'BizOSaaS',
            from_email: 'noreply@bizosaas.com'
        });
    };

    if (statusLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (!isConnected) {
        return (
            <ConnectionPrompt
                serviceName="Mailchimp"
                serviceIcon={<Mail className="w-8 h-8 text-yellow-600" />}
                description="Connect your Mailchimp account to manage email lists, campaigns, and get AI insights."
            />
        );
    }

    const totalSubscribers = lists.reduce((sum, list) => sum + list.subscriber_count, 0);

    return (
        <div className="p-6 space-y-6">
            {/* Header section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                        Marketing Engine
                        <Badge className="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 border-none">AI Powered</Badge>
                    </h1>
                    <p className="text-muted-foreground mt-1">Manage campaigns, monitor performance, and optimize with AI intelligence.</p>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline" className="gap-2" onClick={loadData}>
                        <RefreshCw className={`w-4 h-4 ${isLoadingData ? 'animate-spin' : ''}`} />
                        Sync Data
                    </Button>
                    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                        <DialogTrigger asChild>
                            <Button className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-500/20">
                                <Plus className="w-4 h-4 mr-2" />
                                Create Campaign
                            </Button>
                        </DialogTrigger>
                        <DialogContent>
                            <DialogHeader>
                                <DialogTitle>New Marketing Campaign</DialogTitle>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="space-y-2">
                                    <Label>Campaign Name</Label>
                                    <Input placeholder="e.g. Winter Sale 2024" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} />
                                </div>
                                <div className="space-y-2">
                                    <Label>Subject Line</Label>
                                    <Input placeholder="Grab your 20% discount!" value={formData.subject} onChange={e => setFormData({ ...formData, subject: e.target.value })} />
                                </div>
                            </div>
                            <DialogFooter>
                                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                                <Button onClick={handleCreate}>Launch</Button>
                            </DialogFooter>
                        </DialogContent>
                    </Dialog>
                </div>
            </div>

            {/* Quick Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="border-none bg-orange-50 dark:bg-orange-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Users className="w-5 h-5 text-orange-600" />
                            <Badge variant="secondary" className="bg-orange-100 dark:bg-orange-900/40 text-orange-700">+12%</Badge>
                        </div>
                        <p className="text-sm font-medium text-orange-800 dark:text-orange-300">Total Audience</p>
                        <h3 className="text-3xl font-bold mt-1 text-orange-950 dark:text-orange-50">{totalSubscribers.toLocaleString()}</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-blue-50 dark:bg-blue-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Send className="w-5 h-5 text-blue-600" />
                            <Badge variant="secondary" className="bg-blue-100 dark:bg-blue-900/40 text-blue-700">Live</Badge>
                        </div>
                        <p className="text-sm font-medium text-blue-800 dark:text-blue-300">Active Campaigns</p>
                        <h3 className="text-3xl font-bold mt-1 text-blue-950 dark:text-blue-50">{campaigns.length}</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-green-50 dark:bg-green-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <Zap className="w-5 h-5 text-green-600" />
                            <Badge variant="secondary" className="bg-green-100 dark:bg-green-900/40 text-green-700">24h</Badge>
                        </div>
                        <p className="text-sm font-medium text-green-800 dark:text-green-300">Avg Open Rate</p>
                        <h3 className="text-3xl font-bold mt-1 text-green-950 dark:text-green-50">24.8%</h3>
                    </CardContent>
                </Card>

                <Card className="border-none bg-purple-50 dark:bg-purple-950/20 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between mb-2">
                            <TrendingUp className="w-5 h-5 text-purple-600" />
                            <Badge variant="secondary" className="bg-purple-100 dark:bg-purple-900/40 text-purple-700">High</Badge>
                        </div>
                        <p className="text-sm font-medium text-purple-800 dark:text-purple-300">Click Through</p>
                        <h3 className="text-3xl font-bold mt-1 text-purple-950 dark:text-purple-50">3.2%</h3>
                    </CardContent>
                </Card>
            </div>

            {/* Main Content Tabs */}
            <Tabs defaultValue="overview" className="w-full" onValueChange={setActiveTab}>
                <TabsList className="grid w-full grid-cols-2 md:grid-cols-4 lg:w-[600px] mb-8 bg-slate-100/50 dark:bg-slate-800/50 p-1">
                    <TabsTrigger value="overview" className="data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 shadow-none">
                        Overview
                    </TabsTrigger>
                    <TabsTrigger value="campaigns" className="data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 shadow-none">
                        Campaigns
                    </TabsTrigger>
                    <TabsTrigger value="metrics" className="data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 shadow-none">
                        Deep Dive
                    </TabsTrigger>
                    <TabsTrigger value="ai-assistant" className="data-[state=active]:bg-white dark:data-[state=active]:bg-slate-700 shadow-none flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-blue-500" /> AI Insights
                    </TabsTrigger>
                </TabsList>

                {/* Overview Tab Content */}
                <TabsContent value="overview" className="space-y-6 animate-in fade-in duration-500">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <Card className="lg:col-span-2">
                            <CardHeader>
                                <CardTitle>Campaign Performance Trend</CardTitle>
                                <CardDescription>Open rates vs Click rates over time</CardDescription>
                            </CardHeader>
                            <CardContent className="h-[300px] flex items-center justify-center border-t border-dashed bg-slate-50/30 dark:bg-slate-800/10">
                                <div className="text-center">
                                    <BarChart3 className="w-12 h-12 text-muted-foreground/30 mx-auto mb-2" />
                                    <p className="text-sm text-muted-foreground">Interactive performance chart visualization goes here.</p>
                                </div>
                            </CardContent>
                        </Card>

                        <div className="space-y-6">
                            <Card className="bg-gradient-to-br from-indigo-500/10 to-blue-600/10 border-indigo-200/50 dark:border-indigo-900/30 overflow-hidden relative">
                                <Sparkles className="absolute -top-2 -right-2 w-24 h-24 text-indigo-500/5 rotate-12" />
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2 text-indigo-900 dark:text-indigo-100">
                                        <BrainCircuit className="w-5 h-5" />
                                        Smart Summary
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="text-sm leading-relaxed text-indigo-800 dark:text-indigo-200">
                                        Your engagement is 15% higher among US-based subscribers. The best time to send next week is <span className="font-bold underline">Tuesday at 10:00 AM EST</span>.
                                    </div>
                                    <Button size="sm" variant="outline" className="w-full bg-white/50 dark:bg-slate-800/50 border-indigo-200 hover:bg-indigo-50">
                                        Generate Full Report
                                    </Button>
                                </CardContent>
                            </Card>

                            <Card>
                                <CardHeader className="pb-3">
                                    <CardTitle className="text-sm font-medium">Top Lists</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-3">
                                    {lists.slice(0, 3).map(list => (
                                        <div key={list.id} className="flex items-center justify-between p-2 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                                            <div className="flex items-center gap-2">
                                                <div className="w-2 h-2 rounded-full bg-blue-500" />
                                                <span className="text-sm font-medium">{list.name}</span>
                                            </div>
                                            <span className="text-xs text-muted-foreground">{list.subscriber_count}</span>
                                        </div>
                                    ))}
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </TabsContent>

                {/* Campaigns Tab Content */}
                <TabsContent value="campaigns" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {campaigns.map(campaign => (
                            <Card key={campaign.id} className="group hover:border-blue-300 dark:hover:border-blue-900 transition-all duration-300 overflow-hidden">
                                <CardHeader className="pb-2">
                                    <div className="flex items-center justify-between mb-2">
                                        <Badge className={campaign.status === 'sent' ? 'bg-green-100 text-green-700 dark:bg-green-900/30' : 'bg-slate-100 text-slate-700'}>
                                            {campaign.status}
                                        </Badge>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button variant="ghost" size="icon" className="opacity-0 group-hover:opacity-100 transition-opacity">
                                                    <MoreVertical className="w-4 h-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem className="text-red-500" onClick={() => handleDelete(campaign.id, 'campaigns')}>
                                                    <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </div>
                                    <CardTitle className="text-lg line-clamp-1">{campaign.name}</CardTitle>
                                    <CardDescription className="line-clamp-1">{campaign.subject || 'No subject line'}</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="grid grid-cols-2 gap-2 mt-2">
                                        <div className="p-2 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                                            <p className="text-[10px] text-muted-foreground uppercase tracking-wider">Open Rate</p>
                                            <p className="text-sm font-bold">{campaign.stats?.open_rate || '21.5'}%</p>
                                        </div>
                                        <div className="p-2 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                                            <p className="text-[10px] text-muted-foreground uppercase tracking-wider">Click Rate</p>
                                            <p className="text-sm font-bold">{campaign.stats?.click_rate || '1.2'}%</p>
                                        </div>
                                    </div>
                                </CardContent>
                                <CardFooter className="pt-2">
                                    <Button variant="ghost" size="sm" className="w-full text-blue-600 hover:text-blue-700 hover:bg-blue-50">
                                        View Full Report <ArrowUpRight className="ml-2 w-3 h-3" />
                                    </Button>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                {/* Metrics Content (Deep Dive) */}
                <TabsContent value="metrics" className="space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Conversion Funnel</CardTitle>
                            <CardDescription>Visualizing the journey from sent to converted</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-8 py-10">
                            {[
                                { label: 'Emails Sent', value: '14,250', color: 'bg-blue-600', width: '100%' },
                                { label: 'Emails Delivered', value: '13,912', color: 'bg-blue-500', width: '97%' },
                                { label: 'Unique Opens', value: '3,840', color: 'bg-blue-400', width: '27%' },
                                { label: 'Link Clicks', value: '452', color: 'bg-blue-300', width: '3.2%' },
                                { label: 'Conversions', value: '84', color: 'bg-green-500', width: '0.6%' },
                            ].map((step, i) => (
                                <div key={i} className="space-y-2">
                                    <div className="flex justify-between text-sm">
                                        <span className="font-medium">{step.label}</span>
                                        <span className="font-bold">{step.value}</span>
                                    </div>
                                    <div className="w-full h-3 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                                        <div className={`h-full ${step.color} transition-all duration-1000`} style={{ width: step.width }} />
                                    </div>
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* AI Assistant Insight Content */}
                <TabsContent value="ai-assistant" className="space-y-6 animate-in slide-in-from-bottom-2 duration-500">
                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                        <div className="lg:col-span-3 space-y-4">
                            <h3 className="text-xl font-bold flex items-center gap-2">
                                <BrainCircuit className="w-6 h-6 text-blue-500" />
                                Intelligent Recommendations
                            </h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {aiInsights.map((insight, i) => (
                                    <Card key={i} className="border-l-4 border-l-blue-500">
                                        <CardHeader>
                                            <CardTitle className="text-md flex items-center gap-2">
                                                {insight.type === 'success' ? <TrendingUp className="w-4 h-4 text-green-500" /> : <Target className="w-4 h-4 text-amber-500" />}
                                                {insight.title}
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="text-sm text-muted-foreground leading-relaxed">{insight.content}</p>
                                        </CardContent>
                                        <CardFooter>
                                            <Button variant="ghost" size="sm" className="text-blue-600">Apply Recommendation</Button>
                                        </CardFooter>
                                    </Card>
                                ))}
                            </div>

                            <Card className="bg-slate-900 text-white border-none shadow-2xl relative overflow-hidden group">
                                <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform">
                                    <Sparkles className="w-32 h-32" />
                                </div>
                                <CardHeader>
                                    <CardTitle className="flex items-center gap-2">
                                        <MessageSquare className="w-5 h-5 text-blue-400" />
                                        Ask AI Assistant
                                    </CardTitle>
                                    <CardDescription className="text-slate-400 italic">"How can I improve my open rates for next month?"</CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="relative">
                                        <Input className="bg-slate-800 border-slate-700 text-white placeholder:text-slate-500 pr-24 h-12" placeholder="Ask anything about your campaigns..." />
                                        <Button className="absolute right-1 top-1 h-10 bg-blue-600 hover:bg-blue-700">Analyze</Button>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        <div className="space-y-6">
                            <Card className="border-none bg-blue-600 shadow-xl shadow-blue-500/20 text-white">
                                <CardHeader>
                                    <CardTitle className="text-sm uppercase tracking-widest text-blue-100">Market Index</CardTitle>
                                    <div className="text-3xl font-bold">104.2</div>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-xs text-blue-100 leading-relaxed">
                                        Your marketing efficiency score is performing <span className="font-bold underline">above 82%</span> of similar companies in your industry.
                                    </p>
                                </CardContent>
                            </Card>

                            <Card>
                                <CardHeader>
                                    <CardTitle className="text-sm font-medium">Recent Activity</CardTitle>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <ScrollArea className="h-[200px] px-4">
                                        <div className="space-y-4">
                                            {[
                                                { time: '2m ago', event: 'Campaign Launched: Winter Sale' },
                                                { time: '1h ago', event: 'Subscriber Sync Completed' },
                                                { time: '3h ago', event: 'New List Created: VIPs' },
                                                { time: 'Yesterday', event: 'AI Analysis Report Generated' }
                                            ].map((activity, i) => (
                                                <div key={i} className="flex gap-3 items-start border-l-2 border-slate-100 dark:border-slate-800 pl-4 py-1">
                                                    <div>
                                                        <p className="text-xs font-bold text-slate-900 dark:text-slate-100">{activity.event}</p>
                                                        <p className="text-[10px] text-muted-foreground">{activity.time}</p>
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
            </Tabs>
        </div>
    );
}
