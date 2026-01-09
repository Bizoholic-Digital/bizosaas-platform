'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Users, Briefcase, Building2, Search, Plus, Loader2, Edit, Trash2, MoreVertical, Phone, Mail } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';

interface Contact {
    id: string;
    email: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
    company?: string;
}

interface Deal {
    id: string;
    title: string;
    value: number;
    stage: string;
    pipeline?: string;
    close_date?: string;
}

export default function CRMPage() {
    const { isConnected: hubspotConnected, connector: hubspotConnector } = useConnectorStatus('hubspot');
    const { isConnected: fluentcrmConnected, connector: fluentcrmConnector } = useConnectorStatus('fluentcrm');
    const { isLoading: statusLoading } = useConnectorStatus('', 'crm'); // Just for loading state

    const [activeConnector, setActiveConnector] = useState<'hubspot' | 'fluentcrm' | null>(null);
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [deals, setDeals] = useState<Deal[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');

    const [activeTab, setActiveTab] = useState('contacts');
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [selectedContact, setSelectedContact] = useState<Contact | null>(null);
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        company: ''
    });

    const [dealFormData, setDealFormData] = useState({
        title: '',
        value: '',
        stage: 'appointmentsched',
        pipeline: 'default',
        close_date: ''
    });

    const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);

    // Set initial active connector
    useEffect(() => {
        if (hubspotConnected) {
            setActiveConnector('hubspot');
        } else if (fluentcrmConnected) {
            setActiveConnector('fluentcrm');
        }
    }, [hubspotConnected, fluentcrmConnected]);

    useEffect(() => {
        if (activeConnector) {
            loadData();
        }
    }, [activeConnector]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            // Include connector header if the backend needs hint, 
            // though brain-gateway should handle it via user session/config
            const [contactsData, dealsData] = await Promise.all([
                brainApi.crm.getContacts(),
                brainApi.crm.getDeals()
            ]);

            setContacts(contactsData.data || contactsData || []);
            setDeals(dealsData.data || dealsData || []);
        } catch (error) {
            console.error('Failed to load CRM data:', error);
            toast.error('Failed to load CRM data');
        } finally {
            setIsLoadingData(false);
        }
    };

    const handleCreate = async () => {
        try {
            if (activeTab === 'contacts') {
                await brainApi.crm.createContact(formData);
                toast.success('Contact created successfully');
            } else {
                await brainApi.crm.createDeal({
                    ...dealFormData,
                    value: parseFloat(dealFormData.value)
                });
                toast.success('Deal created successfully');
            }
            setIsDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error(`Failed to create ${activeTab === 'contacts' ? 'contact' : 'deal'}`);
        }
    };

    const handleUpdate = async () => {
        try {
            if (activeTab === 'contacts') {
                if (!selectedContact) return;
                await brainApi.crm.updateContact(selectedContact.id, formData);
                toast.success('Contact updated successfully');
            } else {
                if (!selectedDeal) return;
                await brainApi.crm.updateDeal(selectedDeal.id, {
                    ...dealFormData,
                    value: parseFloat(dealFormData.value)
                });
                toast.success('Deal updated successfully');
            }
            setIsDialogOpen(false);
            resetForm();
            loadData();
        } catch (error) {
            toast.error(`Failed to update ${activeTab === 'contacts' ? 'contact' : 'deal'}`);
        }
    };

    const handleDelete = async (id: string) => {
        if (!confirm(`Are you sure you want to delete this ${activeTab === 'contacts' ? 'contact' : 'deal'}?`)) return;
        try {
            if (activeTab === 'contacts') {
                await brainApi.crm.deleteContact(id);
            } else {
                await brainApi.crm.deleteDeal(id);
            }
            toast.success(`${activeTab === 'contacts' ? 'Contact' : 'Deal'} deleted successfully`);
            loadData();
        } catch (error) {
            toast.error(`Failed to delete ${activeTab === 'contacts' ? 'contact' : 'deal'}`);
        }
    };

    const openEditDeal = (deal: Deal) => {
        setSelectedDeal(deal);
        setDealFormData({
            title: deal.title,
            value: deal.value.toString(),
            stage: deal.stage,
            pipeline: deal.pipeline || 'default',
            close_date: deal.close_date || ''
        });
        setIsEditing(true);
        setIsDialogOpen(true);
    };

    const openEdit = (contact: Contact) => {
        setSelectedContact(contact);
        setFormData({
            first_name: contact.first_name || '',
            last_name: contact.last_name || '',
            email: contact.email,
            phone: contact.phone || '',
            company: contact.company || ''
        });
        setIsEditing(true);
        setIsDialogOpen(true);
    };

    const resetForm = () => {
        setFormData({ first_name: '', last_name: '', email: '', phone: '', company: '' });
        setDealFormData({ title: '', value: '', stage: 'appointmentsched', pipeline: 'default', close_date: '' });
        setIsEditing(false);
        setSelectedContact(null);
        setSelectedDeal(null);
    };

    if (statusLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            </div>
        );
    }

    if (!hubspotConnected && !fluentcrmConnected) {
        return (
            <div className="space-y-6 max-w-4xl mx-auto p-6">
                <div className="text-center space-y-2 mb-8">
                    <h1 className="text-3xl font-bold">Connect Your CRM</h1>
                    <p className="text-muted-foreground text-lg">Choose a CRM to manage your contacts and deals.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <ConnectionPrompt
                        serviceName="HubSpot CRM"
                        serviceIcon={<Users className="w-8 h-8 text-orange-600" />}
                        description="Professional CRM for growing businesses. Sync deals and contacts seamlessly."
                        actionUrl="/dashboard/connectors?category=crm"
                    />
                    <ConnectionPrompt
                        serviceName="FluentCRM"
                        serviceIcon={<Building2 className="w-8 h-8 text-blue-600" />}
                        description="Self-hosted marketing automation for WordPress. High performance and privacy."
                        actionUrl="/dashboard/connectors?category=crm"
                    />
                </div>
            </div>
        );
    }

    const currentConnector = activeConnector === 'hubspot' ? hubspotConnector : fluentcrmConnector;
    const isConnected = !!activeConnector;

    const filteredContacts = contacts.filter(contact =>
        contact.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        contact.first_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        contact.last_name?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="p-6 space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">CRM Dashboard</h1>
                    <p className="text-muted-foreground mt-1 text-sm">
                        Unified view of your {currentConnector?.name || 'CRM'} data
                    </p>
                </div>

                <div className="flex items-center gap-3">
                    {(hubspotConnected && fluentcrmConnected) && (
                        <div className="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 p-1 rounded-lg border border-slate-200 dark:border-slate-700">
                            <Button
                                variant={activeConnector === 'hubspot' ? "default" : "ghost"}
                                size="sm"
                                onClick={() => setActiveConnector('hubspot')}
                                className="h-8 text-xs px-3"
                            >
                                HubSpot
                            </Button>
                            <Button
                                variant={activeConnector === 'fluentcrm' ? "default" : "ghost"}
                                size="sm"
                                onClick={() => setActiveConnector('fluentcrm')}
                                className="h-8 text-xs px-3"
                            >
                                FluentCRM
                            </Button>
                        </div>
                    )}
                    <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800 whitespace-nowrap">
                        <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
                        Connected: {currentConnector?.name}
                    </Badge>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Contacts</CardTitle>
                        <Users className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{contacts.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Active Deals</CardTitle>
                        <Briefcase className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{deals.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium">Total Value</CardTitle>
                        <Building2 className="w-4 h-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            ${deals.reduce((sum, deal) => sum + deal.value, 0).toLocaleString()}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Main Content */}
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>CRM Data</CardTitle>
                            <CardDescription>View and manage your contacts and deals</CardDescription>
                        </div>
                        <Dialog open={isDialogOpen} onOpenChange={(open) => {
                            setIsDialogOpen(open);
                            if (!open) resetForm();
                        }}>
                            <DialogTrigger asChild>
                                <Button>
                                    <Plus className="w-4 h-4 mr-2" />
                                    Add {activeTab === 'contacts' ? 'Contact' : 'Deal'}
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                    <DialogTitle>{isEditing ? 'Edit' : 'Add New'} {activeTab === 'contacts' ? 'Contact' : 'Deal'}</DialogTitle>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    {activeTab === 'contacts' ? (
                                        <>
                                            <div className="grid grid-cols-2 gap-4">
                                                <div className="space-y-2">
                                                    <Label htmlFor="firstName">First Name</Label>
                                                    <Input
                                                        id="firstName"
                                                        value={formData.first_name}
                                                        onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                                                    />
                                                </div>
                                                <div className="space-y-2">
                                                    <Label htmlFor="lastName">Last Name</Label>
                                                    <Input
                                                        id="lastName"
                                                        value={formData.last_name}
                                                        onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                                                    />
                                                </div>
                                            </div>
                                            <div className="space-y-2">
                                                <Label htmlFor="email">Email</Label>
                                                <Input
                                                    id="email"
                                                    type="email"
                                                    value={formData.email}
                                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                                />
                                            </div>
                                            <div className="space-y-2">
                                                <Label htmlFor="phone">Phone</Label>
                                                <Input
                                                    id="phone"
                                                    value={formData.phone}
                                                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                                />
                                            </div>
                                            <div className="space-y-2">
                                                <Label htmlFor="company">Company</Label>
                                                <Input
                                                    id="company"
                                                    value={formData.company}
                                                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                                                />
                                            </div>
                                        </>
                                    ) : (
                                        <>
                                            <div className="space-y-2">
                                                <Label htmlFor="title">Deal Title</Label>
                                                <Input
                                                    id="title"
                                                    value={dealFormData.title}
                                                    onChange={(e) => setDealFormData({ ...dealFormData, title: e.target.value })}
                                                />
                                            </div>
                                            <div className="grid grid-cols-2 gap-4">
                                                <div className="space-y-2">
                                                    <Label htmlFor="value">Value ($)</Label>
                                                    <Input
                                                        id="value"
                                                        type="number"
                                                        value={dealFormData.value}
                                                        onChange={(e) => setDealFormData({ ...dealFormData, value: e.target.value })}
                                                    />
                                                </div>
                                                <div className="space-y-2">
                                                    <Label htmlFor="closeDate">Close Date</Label>
                                                    <Input
                                                        id="closeDate"
                                                        type="date"
                                                        value={dealFormData.close_date}
                                                        onChange={(e) => setDealFormData({ ...dealFormData, close_date: e.target.value })}
                                                    />
                                                </div>
                                            </div>
                                            <div className="space-y-2">
                                                <Label htmlFor="stage">Stage</Label>
                                                <Input
                                                    id="stage"
                                                    value={dealFormData.stage}
                                                    onChange={(e) => setDealFormData({ ...dealFormData, stage: e.target.value })}
                                                />
                                            </div>
                                        </>
                                    )}
                                </div>
                                <DialogFooter>
                                    <Button variant="outline" onClick={() => setIsDialogOpen(false)}>Cancel</Button>
                                    <Button onClick={isEditing ? handleUpdate : handleCreate}>
                                        {isEditing ? 'Save Changes' : `Add ${activeTab === 'contacts' ? 'Contact' : 'Deal'}`}
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="contacts" className="w-full" onValueChange={setActiveTab}>
                        <TabsList className="grid w-full grid-cols-2 mb-4">
                            <TabsTrigger value="contacts">
                                <Users className="w-4 h-4 mr-2" />
                                Contacts ({contacts.length})
                            </TabsTrigger>
                            <TabsTrigger value="deals">
                                <Briefcase className="w-4 h-4 mr-2" />
                                Deals ({deals.length})
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="contacts" className="space-y-4">
                            {/* Search */}
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                <Input
                                    placeholder="Search contacts..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="pl-10"
                                />
                            </div>

                            {/* Contacts List */}
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : filteredContacts.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">
                                    No contacts found
                                </div>
                            ) : (
                                <div className="space-y-2">
                                    {filteredContacts.map((contact) => (
                                        <div
                                            key={contact.id}
                                            className="flex items-center justify-between p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
                                        >
                                            <div className="flex items-center gap-4">
                                                <div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                                                    <Users className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                                                </div>
                                                <div>
                                                    <p className="font-medium text-slate-900 dark:text-white">
                                                        {contact.first_name} {contact.last_name}
                                                    </p>
                                                    <p className="text-sm text-muted-foreground">{contact.email}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-6">
                                                <div className="hidden md:block text-right">
                                                    {contact.company && (
                                                        <p className="text-sm font-medium text-slate-900 dark:text-white">{contact.company}</p>
                                                    )}
                                                    {contact.phone && (
                                                        <p className="text-sm text-muted-foreground">{contact.phone}</p>
                                                    )}
                                                </div>
                                                <DropdownMenu>
                                                    <DropdownMenuTrigger asChild>
                                                        <Button variant="ghost" size="icon">
                                                            <MoreVertical className="w-4 h-4" />
                                                        </Button>
                                                    </DropdownMenuTrigger>
                                                    <DropdownMenuContent align="end">
                                                        <DropdownMenuItem onClick={() => openEdit(contact)}>
                                                            <Edit className="w-4 h-4 mr-2" /> Edit
                                                        </DropdownMenuItem>
                                                        <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(contact.id)}>
                                                            <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                        </DropdownMenuItem>
                                                    </DropdownMenuContent>
                                                </DropdownMenu>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </TabsContent>

                        <TabsContent value="deals" className="space-y-4">
                            {isLoadingData ? (
                                <div className="flex items-center justify-center py-12">
                                    <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                                </div>
                            ) : deals.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">
                                    No deals found
                                </div>
                            ) : (
                                <div className="space-y-2">
                                    {deals.map((deal) => (
                                        <div
                                            key={deal.id}
                                            className="flex items-center justify-between p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
                                        >
                                            <div className="flex items-center gap-4">
                                                <div className="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                                                    <Briefcase className="w-5 h-5 text-green-600 dark:text-green-400" />
                                                </div>
                                                <div>
                                                    <p className="font-medium text-slate-900 dark:text-white">{deal.title}</p>
                                                    <p className="text-sm text-muted-foreground">Stage: {deal.stage}</p>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-6">
                                                <div className="text-right">
                                                    <p className="font-semibold text-slate-900 dark:text-white">
                                                        ${deal.value.toLocaleString()}
                                                    </p>
                                                    {deal.close_date && (
                                                        <p className="text-sm text-muted-foreground">
                                                            Close: {new Date(deal.close_date).toLocaleDateString()}
                                                        </p>
                                                    )}
                                                </div>
                                                <DropdownMenu>
                                                    <DropdownMenuTrigger asChild>
                                                        <Button variant="ghost" size="icon">
                                                            <MoreVertical className="w-4 h-4" />
                                                        </Button>
                                                    </DropdownMenuTrigger>
                                                    <DropdownMenuContent align="end">
                                                        <DropdownMenuItem onClick={() => openEditDeal(deal)}>
                                                            <Edit className="w-4 h-4 mr-2" /> Edit
                                                        </DropdownMenuItem>
                                                        <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(deal.id)}>
                                                            <Trash2 className="w-4 h-4 mr-2" /> Delete
                                                        </DropdownMenuItem>
                                                    </DropdownMenuContent>
                                                </DropdownMenu>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </TabsContent>
                    </Tabs>
                </CardContent>
            </Card>
        </div>
    );
}
