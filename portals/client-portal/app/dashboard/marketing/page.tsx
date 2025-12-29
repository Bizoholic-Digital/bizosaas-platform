'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Mail, Users, Send, Loader2, Plus, Edit, Trash2, MoreVertical } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import Link from 'next/link';

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
}

export default function MarketingPage() {
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('mailchimp', 'marketing');
    const [lists, setLists] = useState<EmailList[]>([]);
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);

    const [activeTab, setActiveTab] = useState('lists');
    const [isDialogOpen, setIsDialogOpen] = useState(false);
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
            if (activeTab === 'lists') {
                await brainApi.marketing.createList({ name: formData.name });
                toast.success('List created successfully');
            } else {
                await brainApi.marketing.createCampaign(formData);
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
                description="Connect your Mailchimp account to manage email lists and campaigns."
            />
        );
    }

    const totalSubscribers = lists.reduce((sum, list) => sum + list.subscriber_count, 0);

    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Marketing</h1>
                    <p className="text-muted-foreground mt-1">Manage your email marketing campaigns</p>
                </div>
                <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800">
                    <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
                    Connected to {connector?.name}
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Email Lists</CardTitle>
                        <Mail className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{lists.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Subscribers</CardTitle>
                        <Users className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalSubscribers.toLocaleString()}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Campaigns</CardTitle>
                        <Send className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{campaigns.length}</div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Marketing Data</CardTitle>
                        </div>
                        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                            <DialogTrigger asChild>
                                <Button>
                                    <Plus className="w-4 h-4 mr-2" />
                                    New {activeTab === 'lists' ? 'List' : 'Campaign'}
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                    <DialogTitle>Create New {activeTab === 'lists' ? 'List' : 'Campaign'}</DialogTitle>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="name">Name</Label>
                                        <Input
                                            id="name"
                                            placeholder={activeTab === 'lists' ? 'Newsletter subscribers' : 'Summer Promo 2024'}
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        />
                                    </div>
                                    {activeTab === 'campaigns' && (
                                        <>
                                            <div className="space-y-2">
                                                <Label htmlFor="subject">Subject Line</Label>
                                                <Input
                                                    id="subject"
                                                    placeholder="Exclusive Summer Offer!"
                                                    value={formData.subject}
                                                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                                                />
                                            </div>
                                            <div className="grid grid-cols-2 gap-4">
                                                <div className="space-y-2">
                                                    <Label htmlFor="fromName">From Name</Label>
                                                    <Input
                                                        id="fromName"
                                                        value={formData.from_name}
                                                        onChange={(e) => setFormData({ ...formData, from_name: e.target.value })}
                                                    />
                                                </div>
                                                <div className="space-y-2">
                                                    <Label htmlFor="fromEmail">From Email</Label>
                                                    <Input
                                                        id="fromEmail"
                                                        value={formData.from_email}
                                                        onChange={(e) => setFormData({ ...formData, from_email: e.target.value })}
                                                    />
                                                </div>
                                            </div>
                                        </>
                                    )}
                                </div>
                                <DialogFooter>
                                    <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                                    <Button onClick={handleCreate}>Create</Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="lists" className="w-full" onValueChange={setActiveTab}>
                        <TabsList className="grid w-full grid-cols-2 mb-4">
                            <TabsTrigger value="lists">
                                <Mail className="w-4 h-4 mr-2" />
                                Lists ({lists.length})
                            </TabsTrigger>
                            <TabsTrigger value="campaigns">
                                <Send className="w-4 h-4 mr-2" />
                                Campaigns ({campaigns.length})
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="lists" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : lists.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No lists found</div>
                            ) : (
                                lists.map((list) => (
                                    <div key={list.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <Mail className="w-5 h-5 text-yellow-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">{list.name}</p>
                                                <p className="text-sm text-muted-foreground">
                                                    {list.subscriber_count} subscribers
                                                </p>
                                            </div>
                                        </div>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button variant="ghost" size="icon">
                                                    <MoreVertical className="w-4 h-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem onClick={() => handleDelete(list.id, 'lists')} className="text-red-600">
                                                    <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </div>
                                ))
                            )}
                        </TabsContent>

                        <TabsContent value="campaigns" className="space-y-2">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : campaigns.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">No campaigns found</div>
                            ) : (
                                campaigns.map((campaign) => (
                                    <div key={campaign.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-slate-50 dark:hover:bg-slate-800">
                                        <div className="flex items-center gap-4">
                                            <Send className="w-5 h-5 text-blue-600" />
                                            <div>
                                                <p className="font-medium text-slate-900 dark:text-white">{campaign.name}</p>
                                                <p className="text-sm text-muted-foreground">{campaign.subject || 'No subject'}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <Badge variant={campaign.status === 'sent' ? 'default' : 'secondary'}>
                                                {campaign.status}
                                            </Badge>
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" size="icon">
                                                        <MoreVertical className="w-4 h-4" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem onClick={() => handleDelete(campaign.id, 'campaigns')} className="text-red-600">
                                                        <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </div>
                                    </div>
                                ))
                            )}
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>
        </div>
    );
}
