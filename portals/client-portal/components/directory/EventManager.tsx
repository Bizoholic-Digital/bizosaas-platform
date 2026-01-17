'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, MapPin, Plus, ArrowLeft, Save, Trash2, Clock, Globe, Image as ImageIcon } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { toast } from 'sonner';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

interface EventManagerProps {
    listing: any;
    onBack: () => void;
}

export default function EventManager({ listing, onBack }: EventManagerProps) {
    const [events, setEvents] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        start_date: '',
        end_date: '',
        location: listing.address + ', ' + listing.city,
        image_url: '',
        external_link: '',
    });

    const fetchEvents = async () => {
        setLoading(true);
        try {
            const data = await brainApi.directory.getEvents(listing.id);
            setEvents(data);
        } catch (err) {
            console.error("Failed to fetch events", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEvents();
    }, [listing.id]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            await brainApi.directory.createEvent(listing.id, {
                ...formData,
                start_date: new Date(formData.start_date).toISOString(),
                end_date: formData.end_date ? new Date(formData.end_date).toISOString() : null,
            });
            toast.success("Event created successfully!");
            setShowForm(false);
            setFormData({
                title: '',
                description: '',
                start_date: '',
                end_date: '',
                location: listing.address + ', ' + listing.city,
                image_url: '',
                external_link: '',
            });
            fetchEvents();
        } catch (err) {
            toast.error("Failed to create event");
        } finally {
            setSubmitting(false);
        }
    };

    if (loading && events.length === 0) {
        return <div className="p-8 text-center italic text-gray-500">Retrieving events...</div>;
    }

    return (
        <div className="p-6 space-y-6 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" onClick={onBack} className="p-2 h-10 w-10 rounded-full">
                        <ArrowLeft className="w-5 h-5" />
                    </Button>
                    <div>
                        <h2 className="text-2xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">Event Manager</h2>
                        <p className="text-sm text-gray-500 font-medium">Promote activities for <span className="text-blue-600">[{listing.business_name}]</span></p>
                    </div>
                </div>
                {!showForm && (
                    <Button
                        onClick={() => setShowForm(true)}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl px-6 py-2 shadow-lg shadow-blue-500/20 gap-2"
                    >
                        <Plus className="w-4 h-4" /> Create Event
                    </Button>
                )}
            </div>

            {showForm ? (
                <Card className="border-none shadow-xl bg-white dark:bg-gray-900 overflow-hidden">
                    <CardHeader className="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
                        <CardTitle className="text-lg uppercase tracking-tight font-black">New Event Details</CardTitle>
                        <CardDescription>Fill in the details to announce your upcoming activity.</CardDescription>
                    </CardHeader>
                    <CardContent className="p-8">
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Event Title</Label>
                                <Input
                                    name="title"
                                    required
                                    value={formData.title}
                                    onChange={handleInputChange}
                                    placeholder="e.g. Grand Opening Anniversary"
                                    className="rounded-xl h-12"
                                />
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Description</Label>
                                <Textarea
                                    name="description"
                                    value={formData.description}
                                    onChange={handleInputChange}
                                    placeholder="Tell people what to expect..."
                                    className="rounded-xl min-h-[100px]"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Start Date & Time</Label>
                                    <Input
                                        name="start_date"
                                        type="datetime-local"
                                        required
                                        value={formData.start_date}
                                        onChange={handleInputChange}
                                        className="rounded-xl h-12"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">End Date & Time (Optional)</Label>
                                    <Input
                                        name="end_date"
                                        type="datetime-local"
                                        value={formData.end_date}
                                        onChange={handleInputChange}
                                        className="rounded-xl h-12"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Location</Label>
                                <Input
                                    name="location"
                                    value={formData.location}
                                    onChange={handleInputChange}
                                    placeholder="Where is the event taking place?"
                                    className="rounded-xl h-12"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Image URL</Label>
                                    <Input
                                        name="image_url"
                                        value={formData.image_url}
                                        onChange={handleInputChange}
                                        placeholder="Link to an event banner..."
                                        className="rounded-xl h-12"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">External Ticket/Info Link</Label>
                                    <Input
                                        name="external_link"
                                        value={formData.external_link}
                                        onChange={handleInputChange}
                                        placeholder="https://..."
                                        className="rounded-xl h-12"
                                    />
                                </div>
                            </div>

                            <div className="flex justify-end gap-3 pt-6 border-t border-gray-100 dark:border-gray-800">
                                <Button type="button" variant="ghost" onClick={() => setShowForm(false)} className="font-bold">Cancel</Button>
                                <Button
                                    type="submit"
                                    disabled={submitting}
                                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl px-8 h-12 gap-2 shadow-lg shadow-blue-500/20"
                                >
                                    <Save className="w-4 h-4" /> {submitting ? 'Creating...' : 'Announce Event'}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {events.length === 0 ? (
                        <div className="col-span-full py-20 text-center bg-gray-50 dark:bg-gray-800/30 rounded-3xl border-2 border-dashed border-gray-100 dark:border-gray-800">
                            <Calendar className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                            <h3 className="text-xl font-black text-gray-400 uppercase tracking-tighter">No Events Found</h3>
                            <p className="text-sm text-gray-500 mt-2 max-w-xs mx-auto">Create an event to bring more people to your business!</p>
                            <Button variant="outline" onClick={() => setShowForm(true)} className="mt-6 rounded-xl font-bold">Add Your First Event</Button>
                        </div>
                    ) : (
                        events.map((event) => (
                            <Card key={event.id} className="overflow-hidden bg-white dark:bg-gray-900 border-none shadow-md hover:shadow-xl transition-all group">
                                <div className="h-32 bg-gray-100 dark:bg-gray-800 relative overflow-hidden">
                                    {event.image_url ? (
                                        <img src={event.image_url} alt={event.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center text-gray-300">
                                            <ImageIcon className="w-10 h-10" />
                                        </div>
                                    )}
                                    <div className="absolute top-3 left-3">
                                        <Badge className={`uppercase font-black text-[9px] ${event.status === 'upcoming' ? 'bg-blue-500' : 'bg-green-500'
                                            }`}>
                                            {event.status}
                                        </Badge>
                                    </div>
                                </div>
                                <CardHeader className="p-4">
                                    <CardTitle className="text-lg font-black uppercase tracking-tight">{event.title}</CardTitle>
                                    <div className="space-y-2 mt-2">
                                        <div className="flex items-center gap-2 text-xs font-bold text-gray-500">
                                            <Clock className="w-3.5 h-3.5 text-blue-500" />
                                            {new Date(event.start_date).toLocaleDateString()} at {new Date(event.start_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                        <div className="flex items-center gap-2 text-xs font-bold text-gray-500 truncate">
                                            <MapPin className="w-3.5 h-3.5 text-red-500" />
                                            {event.location}
                                        </div>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-4 pt-0">
                                    <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2 italic mb-4">
                                        {event.description || "No description provided."}
                                    </p>
                                    <div className="flex gap-2">
                                        {event.external_link && (
                                            <Button variant="outline" size="sm" className="flex-1 rounded-lg text-[10px] uppercase font-black tracking-widest" asChild>
                                                <a href={event.external_link} target="_blank" rel="noopener noreferrer">
                                                    Tickets <Globe className="w-3 h-3 ml-1" />
                                                </a>
                                            </Button>
                                        )}
                                        <Button variant="ghost" size="sm" className="rounded-lg text-red-500 hover:bg-red-50 hover:text-red-600">
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}
