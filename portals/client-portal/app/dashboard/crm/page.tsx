'use client';

import { useState, useEffect } from 'react';
import { useConnectorStatus } from '@/lib/hooks/useConnectorStatus';
import { ConnectionPrompt } from '@/components/connectors/ConnectionPrompt';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Users, Briefcase, Building2, Search, Plus, Loader2 } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';

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
    const { isConnected, isLoading: statusLoading, connector } = useConnectorStatus('hubspot');
    const [contacts, setContacts] = useState<Contact[]>([]);
    const [deals, setDeals] = useState<Deal[]>([]);
    const [isLoadingData, setIsLoadingData] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        if (isConnected) {
            loadData();
        }
    }, [isConnected]);

    const loadData = async () => {
        setIsLoadingData(true);
        try {
            // Load contacts and deals from HubSpot
            const [contactsData, dealsData] = await Promise.all([
                brainApi.crm.listContacts(),
                brainApi.crm.getDeals()
            ]);

            setContacts(contactsData.data || contactsData || []);
            setDeals(dealsData.data || dealsData || []);
        } catch (error) {
            console.error('Failed to load CRM data:', error);
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

    if (!isConnected) {
        return (
            <ConnectionPrompt
                serviceName="HubSpot CRM"
                serviceIcon={<Users className="w-8 h-8 text-blue-600" />}
                description="Connect your HubSpot account to manage contacts, deals, and companies."
            />
        );
    }

    const filteredContacts = contacts.filter(contact =>
        contact.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        contact.first_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        contact.last_name?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white">CRM</h1>
                    <p className="text-muted-foreground mt-1">
                        Manage your contacts, deals, and companies
                    </p>
                </div>
                <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800">
                    <div className="w-2 h-2 rounded-full bg-green-500 mr-2" />
                    Connected to {connector?.name}
                </Badge>
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
                        <Button>
                            <Plus className="w-4 h-4 mr-2" />
                            Add Contact
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <Tabs defaultValue="contacts" className="w-full">
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
                                            <div className="text-right">
                                                {contact.company && (
                                                    <p className="text-sm text-muted-foreground">{contact.company}</p>
                                                )}
                                                {contact.phone && (
                                                    <p className="text-sm text-muted-foreground">{contact.phone}</p>
                                                )}
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
