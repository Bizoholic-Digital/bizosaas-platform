'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MessageSquare, Mail, Phone, Calendar, ArrowLeft, CheckCircle2, XCircle, Search } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { toast } from 'sonner';
import { Input } from '@/components/ui/input';

interface LeadCenterProps {
    listing: any;
    onBack: () => void;
}

export default function LeadCenter({ listing, onBack }: LeadCenterProps) {
    const [enquiries, setEnquiries] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedEnquiry, setSelectedEnquiry] = useState<any>(null);

    useEffect(() => {
        const fetchEnquiries = async () => {
            try {
                const data = await brainApi.directory.getEnquiries(listing.id);
                setEnquiries(data);
            } catch (err) {
                console.error("Failed to fetch enquiries", err);
            } finally {
                setLoading(false);
            }
        };
        fetchEnquiries();
    }, [listing.id]);

    const handleStatusUpdate = async (enquiryId: string, status: string) => {
        try {
            await brainApi.directory.updateEnquiryStatus(enquiryId, status);
            setEnquiries(prev => prev.map(e => e.id === enquiryId ? { ...e, status } : e));
            if (selectedEnquiry?.id === enquiryId) {
                setSelectedEnquiry(prev => ({ ...prev, status }));
            }
            toast.success(`Enquiry marked as ${status}`);
        } catch (err) {
            toast.error("Failed to update status");
        }
    };

    if (loading) {
        return <div className="p-8 text-center">Loading leads...</div>;
    }

    return (
        <div className="p-6 space-y-6 animate-in fade-in duration-500">
            <div className="flex items-center gap-4">
                <Button variant="ghost" onClick={onBack} className="p-2 h-10 w-10 rounded-full">
                    <ArrowLeft className="w-5 h-5" />
                </Button>
                <div>
                    <h2 className="text-2xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">Lead Center</h2>
                    <p className="text-sm text-gray-500 font-medium">Managing enquiries for <span className="text-blue-600">[{listing.business_name}]</span></p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Leads List */}
                <div className="lg:col-span-1 space-y-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <Input placeholder="Search leads..." className="pl-10 rounded-xl" />
                    </div>

                    <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                        {enquiries.length === 0 ? (
                            <div className="text-center py-12 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border-2 border-dashed border-gray-100 dark:border-gray-800">
                                <MessageSquare className="w-10 h-10 mx-auto mb-2 text-gray-300" />
                                <p className="text-sm font-bold text-gray-400">No leads yet</p>
                            </div>
                        ) : (
                            enquiries.map((enquiry) => (
                                <Card
                                    key={enquiry.id}
                                    onClick={() => setSelectedEnquiry(enquiry)}
                                    className={`cursor-pointer transition-all border-none shadow-sm hover:shadow-md ${selectedEnquiry?.id === enquiry.id ? 'ring-2 ring-blue-500 bg-blue-50/50 dark:bg-blue-900/10' : 'bg-white dark:bg-gray-900'
                                        }`}
                                >
                                    <CardHeader className="p-4 flex flex-row items-center justify-between space-y-0">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center font-bold text-blue-600">
                                                {enquiry.name[0]}
                                            </div>
                                            <div>
                                                <CardTitle className="text-sm font-bold truncate max-w-[120px]">{enquiry.name}</CardTitle>
                                                <CardDescription className="text-[10px] font-medium uppercase tracking-widest">
                                                    {new Date(enquiry.created_at).toLocaleDateString()}
                                                </CardDescription>
                                            </div>
                                        </div>
                                        <Badge className={`text-[9px] font-black uppercase px-1.5 py-0 ${enquiry.status === 'new' ? 'bg-blue-500' :
                                                enquiry.status === 'read' ? 'bg-gray-500' :
                                                    enquiry.status === 'replied' ? 'bg-green-500' : 'bg-red-500'
                                            }`}>
                                            {enquiry.status}
                                        </Badge>
                                    </CardHeader>
                                </Card>
                            ))
                        )}
                    </div>
                </div>

                {/* Lead Detail */}
                <div className="lg:col-span-2">
                    {selectedEnquiry ? (
                        <Card className="bg-white dark:bg-gray-900 border-none shadow-xl h-full flex flex-col">
                            <CardHeader className="border-b border-gray-50 dark:border-gray-800 p-8">
                                <div className="flex justify-between items-start">
                                    <div className="flex gap-4">
                                        <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center text-blue-600 text-2xl font-black">
                                            {selectedEnquiry.name[0]}
                                        </div>
                                        <div>
                                            <CardTitle className="text-2xl font-black uppercase tracking-tight">{selectedEnquiry.name}</CardTitle>
                                            <div className="flex flex-wrap gap-4 mt-2">
                                                <a href={`mailto:${selectedEnquiry.email}`} className="flex items-center gap-1.5 text-sm font-bold text-gray-500 hover:text-blue-600">
                                                    <Mail className="w-3.5 h-3.5" /> {selectedEnquiry.email}
                                                </a>
                                                <a href={`tel:${selectedEnquiry.phone}`} className="flex items-center gap-1.5 text-sm font-bold text-gray-500 hover:text-blue-600">
                                                    <Phone className="w-3.5 h-3.5" /> {selectedEnquiry.phone}
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        <Button
                                            onClick={() => handleStatusUpdate(selectedEnquiry.id, 'replied')}
                                            variant="outline"
                                            className="h-10 px-4 rounded-xl font-bold border-green-200 text-green-600 hover:bg-green-50 gap-2"
                                            disabled={selectedEnquiry.status === 'replied'}
                                        >
                                            <CheckCircle2 className="w-4 h-4" /> Mark Replied
                                        </Button>
                                        <Button
                                            onClick={() => handleStatusUpdate(selectedEnquiry.id, 'spam')}
                                            variant="ghost"
                                            className="h-10 px-4 rounded-xl font-bold text-red-500 hover:bg-red-50 gap-2"
                                            disabled={selectedEnquiry.status === 'spam'}
                                        >
                                            <XCircle className="w-4 h-4" /> Mark Spam
                                        </Button>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="p-8 flex-1">
                                <div className="space-y-6">
                                    <div>
                                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Subject</p>
                                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">{selectedEnquiry.subject || 'Enquiry from Directory'}</h3>
                                    </div>
                                    <div>
                                        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Message</p>
                                        <div className="p-6 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-gray-100 dark:border-gray-800 text-gray-700 dark:text-gray-300 leading-relaxed italic">
                                            "{selectedEnquiry.message}"
                                        </div>
                                    </div>
                                    <div className="pt-4 flex gap-8">
                                        <div>
                                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Source</p>
                                            <Badge variant="outline" className="font-bold border-blue-200 text-blue-600 uppercase text-[9px]">
                                                {selectedEnquiry.source || 'Direct'}
                                            </Badge>
                                        </div>
                                        <div>
                                            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Received On</p>
                                            <p className="text-sm font-bold flex items-center gap-1.5">
                                                <Calendar className="w-4 h-4 text-gray-400" /> {new Date(selectedEnquiry.created_at).toLocaleString()}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ) : (
                        <div className="h-full bg-gray-50 dark:bg-gray-800/30 rounded-3xl border-2 border-dashed border-gray-100 dark:border-gray-800 flex flex-col items-center justify-center text-center p-12">
                            <div className="w-20 h-20 bg-white dark:bg-gray-900 rounded-2xl shadow-sm flex items-center justify-center mb-6">
                                <MessageSquare className="w-10 h-10 text-gray-200" />
                            </div>
                            <h3 className="text-xl font-black text-gray-300 uppercase tracking-tighter">Select a lead to view details</h3>
                            <p className="text-sm text-gray-400 font-medium max-w-xs mt-2">Choose an enquiry from the left panel to manage customer communication.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
