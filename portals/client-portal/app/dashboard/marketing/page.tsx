'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Mail, Users, Send, Loader2, Plus, Edit, Trash2, MoreVertical, Target, Share2, Calendar } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';

interface EmailList {
    id: string;
    name: string;
    subscriber_count: number;
}

interface Campaign {
    id: string;
    name: string;
    status: string;
    goal?: string;
    created_at: string;
    channels?: any[];
}

export default function MarketingPage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('mailchimp', 'marketing');
    const [lists, setLists] = useState<EmailList[]>([]);
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);

    const [activeTab, setActiveTab] = useState('campaigns');
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        goal: 'Brand Awareness',
        channel: 'email',
        subject: '',
        from_name: 'Bizoholic',
        from_email: 'noreply@bizoholic.net'
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
                brainApi.campaigns.list().catch(() => [])
            ]);

            setLists(listsData.data || []);
            setCampaigns(Array.isArray(campaignsData) ? campaignsData : []);
        } catch (error) {
            console.error('Failed to load marketing data:', error);
            toast.error('Failed to load marketing data');
        } finally {
            setIsLoadingData(false);
        }
    };

    const handleCreate = async () => {
        try {
            if (activeTab === 'lists') {
                await brainApi.marketing.createList(formData.name);
                toast.success('List created successfully');
            } else {
                // Formatting for unified campaign API
                const payload = {
                    name: formData.name,
                    goal: formData.goal,
                    channels: [
                        {
                            channel_type: formData.channel,
                            connector_id: formData.channel === 'email' ? 'mailchimp' : 'unknown',
                            config: {
                                subject: formData.subject,
                                from_name: formData.from_name,
                                from_email: formData.from_email
                            }
                        }
                    ]
                };
                await brainApi.campaigns.create(payload);
                toast.success('Campaign created successfully');
            }
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
                // Unified campaign delete (if implemented in API)
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
            goal: 'Brand Awareness',
            channel: 'email',
            subject: '',
            from_name: 'Bizoholic',
            from_email: 'noreply@bizoholic.net'
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
                description="Connect your Mailchimp account to manage email lists and campaigns."
            />
        );
    }

    const totalSubscribers = lists.reduce((sum, list) => sum + list.subscriber_count, 0);

    return (
        <div className="p-8 space-y-8 max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">Marketing & Campaigns</h1>
                    <p className="text-lg text-slate-500 dark:text-slate-400 mt-2">Scale your reach across multiple channels with AI-powered campaigns.</p>
                </div>
                <div className="flex items-center gap-3">
                    <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-2 animate-pulse" />
                        Connected: {connector?.name}
                    </Badge>
                    <Button onClick={() => setIsDialogOpen(true)} className="bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-200 dark:shadow-none">
                        <Plus className="w-4 h-4 mr-2" />
                        Create {activeTab === 'lists' ? 'List' : 'Campaign'}
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="border-none shadow-md bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-900">
                    <CardHeader className="pb-2">
                        <CardDescription className="flex items-center gap-2">
                            <Mail className="w-4 h-4 text-blue-500" />
                            Email Lists
                        </CardDescription>
                        <CardTitle className="text-3xl font-bold">{lists.length}</CardTitle>
                    </CardHeader>
                </Card>

                <Card className="border-none shadow-md bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-900">
                    <CardHeader className="pb-2">
                        <CardDescription className="flex items-center gap-2">
                            <Users className="w-4 h-4 text-emerald-500" />
                            Total Audience
                        </CardDescription>
                        <CardTitle className="text-3xl font-bold">{totalSubscribers.toLocaleString()}</CardTitle>
                    </CardHeader>
                </Card>

                <Card className="border-none shadow-md bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-900">
                    <CardHeader className="pb-2">
                        <CardDescription className="flex items-center gap-2">
                            <Target className="w-4 h-4 text-amber-500" />
                            Active Campaigns
                        </CardDescription>
                        <CardTitle className="text-3xl font-bold">{campaigns.length}</CardTitle>
                    </CardHeader>
                </Card>
            </div>

            <Card className="border-none shadow-xl">
                <CardContent className="p-0">
                    <Tabs defaultValue="campaigns" className="w-full" onValueChange={setActiveTab}>
                        <div className="px-6 pt-6 border-b border-slate-100 dark:border-slate-800">
                            <TabsList className="bg-transparent gap-8 p-0 h-auto">
                                <TabsTrigger value="campaigns" className="text-base font-semibold px-0 py-4 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:bg-transparent rounded-none transition-all">
                                    <Send className="w-5 h-5 mr-3" />
                                    Campaigns
                                </TabsTrigger>
                                <TabsTrigger value="lists" className="text-base font-semibold px-0 py-4 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:bg-transparent rounded-none transition-all">
                                    <Mail className="w-5 h-5 mr-3" />
                                    Audience Lists
                                </TabsTrigger>
                            </TabsList>
                        </div>

                        <div className="p-6">
                            <TabsContent value="lists" className="mt-0 space-y-4">
                                {isLoadingData ? (
                                    <div className="flex items-center justify-center py-12">
                                        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                                    </div>
                                ) : lists.length === 0 ? (
                                    <div className="text-center py-12 text-slate-400 bg-slate-50 dark:bg-slate-900/50 rounded-xl border-2 border-dashed">
                                        No audience lists found. Start by creating your first list.
                                    </div>
                                ) : (
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {lists.map((list) => (
                                            <Card key={list.id} className="group hover:border-blue-200 dark:hover:border-blue-800 transition-all cursor-pointer">
                                                <CardContent className="p-6">
                                                    <div className="flex items-center justify-between">
                                                        <div className="flex items-center gap-4">
                                                            <div className="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-xl">
                                                                <Mail className="w-6 h-6 text-blue-600" />
                                                            </div>
                                                            <div>
                                                                <h4 className="font-bold text-slate-900 dark:text-white">{list.name}</h4>
                                                                <p className="text-sm text-slate-500 font-medium">
                                                                    {list.subscriber_count.toLocaleString()} subscribers
                                                                </p>
                                                            </div>
                                                        </div>
                                                        <DropdownMenu>
                                                            <DropdownMenuTrigger asChild>
                                                                <Button variant="ghost" size="icon" className="group-hover:opacity-100 opacity-0 transition-opacity">
                                                                    <MoreVertical className="w-4 h-4 text-slate-400" />
                                                                </Button>
                                                            </DropdownMenuTrigger>
                                                            <DropdownMenuContent align="end">
                                                                <DropdownMenuItem onClick={() => handleDelete(list.id, 'lists')} className="text-red-600">
                                                                    <Trash2 className="w-4 h-4 mr-2" /> Delete List
                                                                </DropdownMenuItem>
                                                            </DropdownMenuContent>
                                                        </DropdownMenu>
                                                    </div>
                                                </CardContent>
                                            </Card>
                                        ))}
                                    </div>
                                )}
                            </TabsContent>

                            <TabsContent value="campaigns" className="mt-0 space-y-4">
                                {isLoadingData ? (
                                    <div className="flex items-center justify-center py-12">
                                        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                                    </div>
                                ) : campaigns.length === 0 ? (
                                    <div className="text-center py-12 text-slate-400 bg-slate-50 dark:bg-slate-900/50 rounded-xl border-2 border-dashed">
                                        No active campaigns. Create a new campaign to reach your customers.
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        {campaigns.map((campaign) => (
                                            <Card key={campaign.id} className="group hover:border-blue-200 dark:hover:border-blue-800 transition-all">
                                                <CardContent className="p-5">
                                                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                                                        <div className="flex items-center gap-4">
                                                            <div className="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-xl">
                                                                <Send className="w-6 h-6 text-blue-600" />
                                                            </div>
                                                            <div>
                                                                <h4 className="font-bold text-slate-900 dark:text-white">{campaign.name}</h4>
                                                                <div className="flex items-center gap-3 mt-1">
                                                                    <Badge variant="outline" className="text-[10px] uppercase tracking-wider font-bold">
                                                                        {campaign.status}
                                                                    </Badge>
                                                                    <span className="text-xs text-slate-400 flex items-center gap-1.5 underline decoration-dotted">
                                                                        <Target className="w-3 h-3" />
                                                                        {campaign.goal || 'General'}
                                                                    </span>
                                                                    <span className="text-xs text-slate-400 flex items-center gap-1.5 ml-2">
                                                                        <Calendar className="w-3 h-3" />
                                                                        {new Date(campaign.created_at).toLocaleDateString()}
                                                                    </span>
                                                                </div>
                                                            </div>
                                                        </div>

                                                        <div className="flex items-center gap-6">
                                                            <div className="flex -space-x-2">
                                                                <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 border-2 border-white dark:border-slate-900 flex items-center justify-center" title="Email Channel">
                                                                    <Mail className="w-4 h-4 text-blue-500" />
                                                                </div>
                                                                <div className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 border-2 border-white dark:border-slate-900 flex items-center justify-center opacity-40 cursor-not-allowed" title="Social Channel (Coming Soon)">
                                                                    <Share2 className="w-4 h-4 text-slate-400" />
                                                                </div>
                                                            </div>

                                                            <DropdownMenu>
                                                                <DropdownMenuTrigger asChild>
                                                                    <Button variant="ghost" size="icon" className="group-hover:opacity-100 md:opacity-0 transition-opacity">
                                                                        <MoreVertical className="w-4 h-4 text-slate-400" />
                                                                    </Button>
                                                                </DropdownMenuTrigger>
                                                                <DropdownMenuContent align="end">
                                                                    <DropdownMenuItem className="font-medium text-blue-600">
                                                                        <Edit className="w-4 h-4 mr-2" /> Edit Campaign
                                                                    </DropdownMenuItem>
                                                                    <DropdownMenuItem onClick={() => handleDelete(campaign.id, 'campaigns')} className="text-red-600">
                                                                        <Trash2 className="w-4 h-4 mr-2" /> Delete Campaign
                                                                    </DropdownMenuItem>
                                                                </DropdownMenuContent>
                                                            </DropdownMenu>
                                                        </div>
                                                    </div>
                                                </CardContent>
                                            </Card>
                                        ))}
                                    </div>
                                )}
                            </TabsContent>
                        </div>
                    </Tabs>
                </CardContent>
            </Card>

            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                <DialogContent className="sm:max-w-[550px] p-0 overflow-hidden border-none shadow-2xl">
                    <DialogHeader className="p-8 bg-slate-900 text-white">
                        <DialogTitle className="text-2xl font-bold">Launch New {activeTab === 'lists' ? 'Audience List' : 'Marketing Campaign'}</DialogTitle>
                        <CardDescription className="text-slate-400">
                            {activeTab === 'lists' ? 'Organize your contacts for better targeting.' : 'Define your goals and reach your customers across multiple channels.'}
                        </CardDescription>
                    </DialogHeader>
                    <div className="p-8 space-y-6">
                        <div className="space-y-2">
                            <Label htmlFor="name" className="text-sm font-bold uppercase tracking-wider text-slate-500">
                                {activeTab === 'lists' ? 'List Name' : 'Campaign Name'}
                            </Label>
                            <Input
                                id="name"
                                placeholder={activeTab === 'lists' ? 'Newsletter VIPs' : 'Holiday Launch 2025'}
                                value={formData.name}
                                className="h-12 text-lg font-medium"
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            />
                        </div>

                        {activeTab === 'campaigns' && (
                            <div className="grid grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-sm font-bold uppercase tracking-wider text-slate-500">Campaign Goal</Label>
                                    <Select
                                        value={formData.goal}
                                        onValueChange={(v) => setFormData({ ...formData, goal: v })}
                                    >
                                        <SelectTrigger className="h-12">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="Brand Awareness">Brand Awareness</SelectItem>
                                            <SelectItem value="Lead Generation">Lead Generation</SelectItem>
                                            <SelectItem value="Sales & Conversion">Sales & Conversion</SelectItem>
                                            <SelectItem value="Customer Retention">Customer Retention</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-sm font-bold uppercase tracking-wider text-slate-500">Primary Channel</Label>
                                    <Select
                                        value={formData.channel}
                                        onValueChange={(v) => setFormData({ ...formData, channel: v })}
                                    >
                                        <SelectTrigger className="h-12">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="email">Email (Mailchimp)</SelectItem>
                                            <SelectItem value="social" disabled>Social Media (Coming Soon)</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>
                        )}

                        {activeTab === 'campaigns' && formData.channel === 'email' && (
                            <>
                                <Separator />
                                <div className="space-y-4 pt-2">
                                    <div className="space-y-2">
                                        <Label htmlFor="subject" className="text-sm font-bold uppercase tracking-wider text-slate-500">Subject Line</Label>
                                        <Input
                                            id="subject"
                                            placeholder="Something catchy for your customers..."
                                            value={formData.subject}
                                            onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                                        />
                                    </div>
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label htmlFor="fromName" className="text-sm font-bold uppercase tracking-wider text-slate-500">From Name</Label>
                                            <Input id="fromName" value={formData.from_name} onChange={(e) => setFormData({ ...formData, from_name: e.target.value })} />
                                        </div>
                                        <div className="space-y-2">
                                            <Label htmlFor="fromEmail" className="text-sm font-bold uppercase tracking-wider text-slate-500">From Email</Label>
                                            <Input id="fromEmail" value={formData.from_email} onChange={(e) => setFormData({ ...formData, from_email: e.target.value })} />
                                        </div>
                                    </div>
                                </div>
                            </>
                        )}
                    </div>
                    <DialogFooter className="p-8 bg-slate-50 dark:bg-slate-900/50 border-t items-center">
                        <Button variant="ghost" onClick={() => setIsDialogOpen(false)} className="font-bold">Cancel</Button>
                        <Button onClick={handleCreate} disabled={!formData.name} className="px-8 bg-blue-600 hover:bg-blue-700 font-bold shadow-lg shadow-blue-200 dark:shadow-none">
                            Launch {activeTab === 'lists' ? 'List' : 'Campaign'}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}

const Separator = () => <div className="h-px bg-slate-100 dark:bg-slate-800 w-full" />;

