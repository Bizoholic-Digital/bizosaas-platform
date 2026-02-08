'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Building2, MapPin, Globe, Phone, Mail, Camera, Save, ArrowRight, ArrowLeft } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { toast } from 'sonner';

interface ListingWizardProps {
    onComplete: () => void;
    onCancel: () => void;
    initialData?: any;
}

export default function ListingWizard({ onComplete, onCancel, initialData }: ListingWizardProps) {
    const [step, setStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        business_name: initialData?.business_name || '',
        business_slug: initialData?.business_slug || '',
        category: initialData?.category || '',
        description: initialData?.description || '',
        address: initialData?.address || '',
        city: initialData?.city || '',
        state: initialData?.state || '',
        country: initialData?.country || '',
        zip_code: initialData?.zip_code || '',
        phone: initialData?.phone || '',
        whatsapp: initialData?.whatsapp || '',
        email: initialData?.email || '',
        website: initialData?.website || '',
        video_url: initialData?.video_url || '',
        ...initialData
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const nextStep = () => setStep(prev => prev + 1);
    const prevStep = () => setStep(prev => prev - 1);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            await brainApi.directory.createListing(formData);
            toast.success("Listing created successfully!");
            onComplete();
        } catch (err) {
            console.error(err);
            toast.error("Failed to create listing");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto py-8 px-4">
            <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-3xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">
                        {initialData ? 'Edit Listing' : 'Create New Listing'}
                    </h2>
                    <Button variant="ghost" onClick={onCancel}>Cancel</Button>
                </div>

                {/* Stepper */}
                <div className="flex items-center gap-2">
                    {[1, 2, 3].map((s) => (
                        <div key={s} className="flex items-center gap-2">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${step === s ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' :
                                    step > s ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-800 text-gray-500'
                                }`}>
                                {s}
                            </div>
                            {s < 3 && <div className={`w-12 h-0.5 ${step > s ? 'bg-green-500' : 'bg-gray-200 dark:bg-gray-800'}`} />}
                        </div>
                    ))}
                </div>
            </div>

            <Card className="border-none shadow-xl bg-white dark:bg-gray-900 overflow-hidden">
                <CardHeader className="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
                    <CardTitle className="text-lg uppercase tracking-tight font-black">
                        {step === 1 && "Basic Information"}
                        {step === 2 && "Location & Contact"}
                        {step === 3 && "Media & Social"}
                    </CardTitle>
                    <CardDescription>
                        {step === 1 && "Tell us about your business. This will be the main info on your profile."}
                        {step === 2 && "Where can customers find you? Verification helps build trust."}
                        {step === 3 && "Add a video tour and social links to make your profile stand out."}
                    </CardDescription>
                </CardHeader>
                <CardContent className="p-8">
                    {step === 1 && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Business Name</Label>
                                    <Input
                                        name="business_name"
                                        value={formData.business_name}
                                        onChange={handleInputChange}
                                        placeholder="e.g. Bizoholic Digital"
                                        className="rounded-xl h-12 border-gray-200"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Business Slug</Label>
                                    <div className="flex items-center gap-2">
                                        <div className="bg-gray-50 dark:bg-gray-800 px-3 h-12 flex items-center rounded-xl border border-gray-200 text-sm font-medium text-gray-400">
                                            bizolocal.net/
                                        </div>
                                        <Input
                                            name="business_slug"
                                            value={formData.business_slug}
                                            onChange={handleInputChange}
                                            placeholder="bizoholic-digital"
                                            className="rounded-xl h-12 border-gray-200"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Description</Label>
                                <Textarea
                                    name="description"
                                    value={formData.description}
                                    onChange={handleInputChange}
                                    placeholder="Describe your business, services, and legacy..."
                                    className="rounded-xl min-h-[120px] border-gray-200"
                                />
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Category</Label>
                                <Input
                                    name="category"
                                    value={formData.category}
                                    onChange={handleInputChange}
                                    placeholder="e.g. Digital Agency, Restaurant, etc."
                                    className="rounded-xl h-12 border-gray-200"
                                />
                            </div>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Street Address</Label>
                                <Input
                                    name="address"
                                    value={formData.address}
                                    onChange={handleInputChange}
                                    placeholder="123 Growth Lane"
                                    className="rounded-xl h-12 border-gray-200"
                                />
                            </div>

                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="space-y-2 col-span-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">City</Label>
                                    <Input name="city" value={formData.city} onChange={handleInputChange} className="rounded-xl h-12" />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">State</Label>
                                    <Input name="state" value={formData.state} onChange={handleInputChange} className="rounded-xl h-12" />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">ZIP</Label>
                                    <Input name="zip_code" value={formData.zip_code} onChange={handleInputChange} className="rounded-xl h-12" />
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Phone Number</Label>
                                    <Input name="phone" value={formData.phone} onChange={handleInputChange} placeholder="+1 (555) 000-0000" className="rounded-xl h-12" />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">WhatsApp Number</Label>
                                    <Input name="whatsapp" value={formData.whatsapp} onChange={handleInputChange} placeholder="+1 (555) 000-0000" className="rounded-xl h-12" />
                                </div>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Website URL</Label>
                                <Input name="website" value={formData.website} onChange={handleInputChange} placeholder="https://example.com" className="rounded-xl h-12" />
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Video Tour URL (YouTube/Vimeo)</Label>
                                <Input name="video_url" value={formData.video_url} onChange={handleInputChange} placeholder="https://youtube.com/watch?v=..." className="rounded-xl h-12" />
                            </div>

                            <div className="p-6 bg-blue-50 dark:bg-blue-900/10 rounded-2xl border border-blue-100 dark:border-blue-900/30 flex items-start gap-4">
                                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center shrink-0 text-white">
                                    <Camera className="w-5 h-5" />
                                </div>
                                <div>
                                    <h4 className="font-bold text-blue-900 dark:text-blue-100 uppercase tracking-tight">AI Image Enhancement</h4>
                                    <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                                        After creating your listing, you can use our AI to generates beautiful cover images and logos if you don't have them.
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="flex justify-between items-center mt-12 pt-6 border-t border-gray-100 dark:border-gray-800">
                        <Button
                            variant="ghost"
                            onClick={step === 1 ? onCancel : prevStep}
                            className="font-bold text-gray-500 gap-2"
                        >
                            <ArrowLeft className="w-4 h-4" /> {step === 1 ? 'Cancel' : 'Previous'}
                        </Button>

                        {step < 3 ? (
                            <Button
                                onClick={nextStep}
                                className="bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl px-8 h-12 gap-2 shadow-lg shadow-blue-500/20"
                            >
                                Next Step <ArrowRight className="w-4 h-4" />
                            </Button>
                        ) : (
                            <Button
                                onClick={handleSubmit}
                                disabled={loading}
                                className="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-bold rounded-xl px-12 h-12 gap-2 shadow-xl shadow-blue-500/20"
                            >
                                {loading && <RefreshCw className="w-4 h-4 animate-spin" />}
                                <Save className="w-4 h-4" /> Save Listing
                            </Button>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

const RefreshCw = ({ className }: { className?: string }) => (
    <svg className={className} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" ><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" /><path d="M3 21v-5h5" /></svg>
);
