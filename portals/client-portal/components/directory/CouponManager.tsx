'use client';

import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tag, Plus, ArrowLeft, Save, Trash2, Calendar, Scissors, ExternalLink, Ticket } from 'lucide-react';
import { brainApi } from '@/lib/brain-api';
import { toast } from 'sonner';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

interface CouponManagerProps {
    listing: any;
    onBack: () => void;
}

export default function CouponManager({ listing, onBack }: CouponManagerProps) {
    const [coupons, setCoupons] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        code: '',
        discount_value: '',
        expiry_date: '',
        terms_link: '',
    });

    const fetchCoupons = async () => {
        setLoading(true);
        try {
            const data = await brainApi.directory.getCoupons(listing.id);
            setCoupons(data);
        } catch (err) {
            console.error("Failed to fetch coupons", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCoupons();
    }, [listing.id]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            await brainApi.directory.createCoupon(listing.id, {
                ...formData,
                expiry_date: formData.expiry_date ? new Date(formData.expiry_date).toISOString() : null,
            });
            toast.success("Promotion created successfully!");
            setShowForm(false);
            setFormData({
                title: '',
                description: '',
                code: '',
                discount_value: '',
                expiry_date: '',
                terms_link: '',
            });
            fetchCoupons();
        } catch (err) {
            toast.error("Failed to create promotion");
        } finally {
            setSubmitting(false);
        }
    };

    if (loading && coupons.length === 0) {
        return <div className="p-8 text-center italic text-gray-500">Retrieving offers...</div>;
    }

    return (
        <div className="p-6 space-y-6 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" onClick={onBack} className="p-2 h-10 w-10 rounded-full">
                        <ArrowLeft className="w-5 h-5" />
                    </Button>
                    <div>
                        <h2 className="text-2xl font-black text-gray-900 dark:text-white uppercase tracking-tighter">Coupon Manager</h2>
                        <p className="text-sm text-gray-500 font-medium">Manage offers and deals for <span className="text-blue-600">[{listing.business_name}]</span></p>
                    </div>
                </div>
                {!showForm && (
                    <Button
                        onClick={() => setShowForm(true)}
                        className="bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl px-6 py-2 shadow-lg shadow-green-500/20 gap-2"
                    >
                        <Plus className="w-4 h-4" /> Create Offer
                    </Button>
                )}
            </div>

            {showForm ? (
                <Card className="border-none shadow-xl bg-white dark:bg-gray-900 overflow-hidden">
                    <CardHeader className="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-800">
                        <CardTitle className="text-lg uppercase tracking-tight font-black">Promotion Campaign</CardTitle>
                        <CardDescription>Launch a new deal or coupon code for your customers.</CardDescription>
                    </CardHeader>
                    <CardContent className="p-8">
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Promotion Title</Label>
                                    <Input
                                        name="title"
                                        required
                                        value={formData.title}
                                        onChange={handleInputChange}
                                        placeholder="e.g. Early Bird Lunch Special"
                                        className="rounded-xl h-12"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Discount Value</Label>
                                    <Input
                                        name="discount_value"
                                        required
                                        value={formData.discount_value}
                                        onChange={handleInputChange}
                                        placeholder="e.g. 20% OFF or $10 Voucher"
                                        className="rounded-xl h-12"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Short Description</Label>
                                <Textarea
                                    name="description"
                                    value={formData.description}
                                    onChange={handleInputChange}
                                    placeholder="Briefly explain the offer..."
                                    className="rounded-xl min-h-[80px]"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Promo Code (If applicable)</Label>
                                    <div className="relative">
                                        <Ticket className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                                        <Input
                                            name="code"
                                            value={formData.code}
                                            onChange={handleInputChange}
                                            placeholder="BIZ2024"
                                            className="rounded-xl h-12 pl-10 uppercase font-bold tracking-widest"
                                        />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Expiry Date</Label>
                                    <Input
                                        name="expiry_date"
                                        type="date"
                                        value={formData.expiry_date}
                                        onChange={handleInputChange}
                                        className="rounded-xl h-12"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label className="text-xs font-black uppercase tracking-widest text-gray-500">Terms & Conditions Link (Optional)</Label>
                                <Input
                                    name="terms_link"
                                    value={formData.terms_link}
                                    onChange={handleInputChange}
                                    placeholder="https://example.com/terms"
                                    className="rounded-xl h-12"
                                />
                            </div>

                            <div className="flex justify-end gap-3 pt-6 border-t border-gray-100 dark:border-gray-800">
                                <Button type="button" variant="ghost" onClick={() => setShowForm(false)} className="font-bold">Cancel</Button>
                                <Button
                                    type="submit"
                                    disabled={submitting}
                                    className="bg-green-600 hover:bg-green-700 text-white font-bold rounded-xl px-8 h-12 gap-2 shadow-lg shadow-green-500/20"
                                >
                                    <Save className="w-4 h-4" /> {submitting ? 'Creating...' : 'Launch Promotion'}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {coupons.length === 0 ? (
                        <div className="col-span-full py-20 text-center bg-gray-50 dark:bg-gray-800/30 rounded-3xl border-2 border-dashed border-gray-100 dark:border-gray-800">
                            <Tag className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                            <h3 className="text-xl font-black text-gray-400 uppercase tracking-tighter">No Active Offers</h3>
                            <p className="text-sm text-gray-500 mt-2 max-w-xs mx-auto">Launch a promotion to incentivize new customers!</p>
                            <Button variant="outline" onClick={() => setShowForm(true)} className="mt-6 rounded-xl font-bold border-green-200 text-green-600 hover:bg-green-50">Add First Coupon</Button>
                        </div>
                    ) : (
                        coupons.map((coupon) => (
                            <Card key={coupon.id} className="overflow-hidden bg-white dark:bg-gray-900 border-2 border-gray-50 dark:border-gray-800 shadow-sm hover:shadow-xl transition-all relative">
                                <div className="absolute top-0 right-0 w-16 h-16 bg-green-500/10 rounded-bl-[40px] flex items-start justify-end p-3 text-green-600">
                                    <Scissors className="w-5 h-5" />
                                </div>
                                <CardHeader className="p-6">
                                    <Badge className="bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300 font-black px-3 py-1 mb-2 uppercase tracking-tight text-[10px]">
                                        {coupon.discount_value}
                                    </Badge>
                                    <CardTitle className="text-xl font-black uppercase tracking-tighter leading-tight">{coupon.title}</CardTitle>
                                    {coupon.code && (
                                        <div className="mt-3 p-2 bg-gray-50 dark:bg-gray-800 rounded-lg border-2 border-dashed border-gray-200 dark:border-gray-700 flex items-center justify-between">
                                            <span className="text-xs font-black uppercase tracking-widest text-gray-400 ml-2">Code:</span>
                                            <span className="text-sm font-black text-blue-600 tracking-widest mr-2">{coupon.code}</span>
                                        </div>
                                    )}
                                </CardHeader>
                                <CardContent className="px-6 pb-6">
                                    <p className="text-xs text-gray-500 font-medium line-clamp-2 mb-6 italic">
                                        "{coupon.description || 'Exclusive directory offer.'}"
                                    </p>
                                    <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
                                        <div className="flex items-center gap-1.5 text-[10px] font-black uppercase text-gray-400">
                                            <Calendar className="w-3.5 h-3.5" />
                                            {coupon.expiry_date ? `Exp: ${new Date(coupon.expiry_date).toLocaleDateString()}` : 'No Expiry'}
                                        </div>
                                        <div className="flex gap-2">
                                            {coupon.terms_link && (
                                                <Button variant="ghost" size="sm" className="h-8 w-8 p-0 rounded-full" asChild title="Terms">
                                                    <a href={coupon.terms_link} target="_blank" rel="noopener noreferrer"><ExternalLink className="w-4 h-4" /></a>
                                                </Button>
                                            )}
                                            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 rounded-full text-red-500 hover:bg-red-50">
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
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
