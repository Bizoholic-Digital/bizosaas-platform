'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
    LifeBuoy,
    Plus,
    MessageSquare,
    Clock,
    CheckCircle2,
    AlertCircle,
    Search
} from 'lucide-react';
// import { toast } from 'sonner';

export default function SupportContent() {
    const [tickets, setTickets] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [showCreate, setShowCreate] = useState(false);
    const [newTicket, setNewTicket] = useState({ subject: '', description: '', priority: 'medium' });

    // Mock loading for now, will replace with real API call
    useEffect(() => {
        setTickets([
            { id: '1', subject: 'Integration failed with WordPress', status: 'open', priority: 'high', created_at: new Date().toISOString() },
            { id: '2', subject: 'How to export leads to CSV?', status: 'resolved', priority: 'low', created_at: new Date(Date.now() - 86400000).toISOString() }
        ]);
    }, []);

    const handleCreateTicket = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        // Simulate API call
        setTimeout(() => {
            const ticket = {
                id: Math.random().toString(36).substr(2, 9),
                ...newTicket,
                status: 'open',
                created_at: new Date().toISOString()
            };
            setTickets([ticket, ...tickets]);
            setLoading(false);
            setShowCreate(false);
            setNewTicket({ subject: '', description: '', priority: 'medium' });
            // toast.success("Ticket created successfully! Our AI agent is analyzing it.");
            alert("Ticket created successfully! Our AI agent is analyzing it.");
        }, 1000);
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Support Helpdesk</h2>
                    <p className="text-muted-foreground">Get help from our team and AI assistants.</p>
                </div>
                <Button onClick={() => setShowCreate(true)} className="bg-primary hover:bg-primary/90">
                    <Plus className="mr-2 h-4 w-4" /> New Ticket
                </Button>
            </div>

            {showCreate && (
                <Card className="border-primary/20 bg-primary/5">
                    <CardHeader>
                        <CardTitle>Create New Support Request</CardTitle>
                        <CardDescription>Describe your issue and our team will get back to you shortly.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleCreateTicket} className="space-y-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Subject</label>
                                <Input
                                    placeholder="e.g., Unable to connect Google Ads"
                                    value={newTicket.subject}
                                    onChange={e => setNewTicket({ ...newTicket, subject: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Description</label>
                                <Textarea
                                    placeholder="Please provide details about your issue..."
                                    className="min-h-[100px]"
                                    value={newTicket.description}
                                    onChange={e => setNewTicket({ ...newTicket, description: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="flex justify-end gap-2">
                                <Button type="button" variant="outline" onClick={() => setShowCreate(false)}>Cancel</Button>
                                <Button type="submit" disabled={loading}>
                                    {loading ? "Creating..." : "Submit Ticket"}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            )}

            <div className="grid gap-4">
                {tickets.map((ticket) => (
                    <Card key={ticket.id} className="hover:border-primary/50 transition-colors cursor-pointer">
                        <CardContent className="p-6">
                            <div className="flex items-start justify-between">
                                <div className="flex gap-4">
                                    <div className={`p-2 rounded-full ${ticket.status === 'open' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'}`}>
                                        {ticket.status === 'open' ? <AlertCircle className="h-5 w-5" /> : <CheckCircle2 className="h-5 w-5" />}
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-lg">{ticket.subject}</h3>
                                        <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
                                            <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> {new Date(ticket.created_at).toLocaleDateString()}</span>
                                            <span className="flex items-center gap-1"><MessageSquare className="h-3 w-3" /> 0 replies</span>
                                            <Badge variant={ticket.priority === 'high' ? 'destructive' : 'secondary'}>
                                                {ticket.priority.toUpperCase()}
                                            </Badge>
                                        </div>
                                    </div>
                                </div>
                                <Badge variant={ticket.status === 'open' ? 'default' : 'outline'}>
                                    {ticket.status.toUpperCase()}
                                </Badge>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
