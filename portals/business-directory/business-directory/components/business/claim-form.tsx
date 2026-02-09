'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Shield, Mail, Phone, ArrowRight, Loader2, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { businessAPI } from '@/lib/api';
import { Business } from '@/types/business';

interface ClaimFormProps {
    business: Business;
}

export function ClaimForm({ business }: ClaimFormProps) {
    const router = useRouter();
    const [method, setMethod] = useState<'email' | 'phone'>('email');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [contactInfo, setContactInfo] = useState({
        email: business.contact?.email || '',
        phone: business.contact?.phone || '',
        name: ''
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const result = await businessAPI.claimBusiness(business.id, method, {
                ...contactInfo,
                businessId: business.id
            });

            if (result.id) {
                // Success - redirect to verification
                router.push(`/claim/verify/${result.id}`);
            } else {
                throw new Error('Failed to create claim request');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Card className="max-w-2xl mx-auto border-t-4 border-t-primary">
            <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                    <Shield className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-2xl font-bold">Claim {business.name}</CardTitle>
                <CardDescription>
                    Verify your ownership of this business to manage your profile, reply to reviews, and access premium features.
                </CardDescription>
            </CardHeader>

            <form onSubmit={handleSubmit}>
                <CardContent className="space-y-6">
                    {error && (
                        <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm">
                            {error}
                        </div>
                    )}

                    <div className="space-y-4">
                        <div className="grid gap-2">
                            <Label htmlFor="name">Your Full Name</Label>
                            <Input
                                id="name"
                                placeholder="John Doe"
                                required
                                value={contactInfo.name}
                                onChange={(e) => setContactInfo({ ...contactInfo, name: e.target.value })}
                            />
                        </div>

                        <div className="space-y-3">
                            <Label>Choose Verification Method</Label>
                            <RadioGroup
                                value={method}
                                onValueChange={(v: string) => setMethod(v as 'email' | 'phone')}
                                className="grid gap-4"
                            >
                                <div className="flex items-center space-x-3 space-y-0 rounded-md border p-4 cursor-pointer hover:bg-slate-50 transition-colors">
                                    <RadioGroupItem value="email" id="email-method" />
                                    <Label htmlFor="email-method" className="flex flex-1 items-center cursor-pointer">
                                        <Mail className="w-5 h-5 mr-3 text-muted-foreground" />
                                        <div className="flex-1">
                                            <p className="font-medium">Verify via Email</p>
                                            <p className="text-sm text-muted-foreground">We'll send a code to the business email</p>
                                        </div>
                                    </Label>
                                </div>
                                <div className="flex items-center space-x-3 space-y-0 rounded-md border p-4 cursor-pointer hover:bg-slate-50 transition-colors">
                                    <RadioGroupItem value="phone" id="phone-method" />
                                    <Label htmlFor="phone-method" className="flex flex-1 items-center cursor-pointer">
                                        <Phone className="w-5 h-5 mr-3 text-muted-foreground" />
                                        <div className="flex-1">
                                            <p className="font-medium">Verify via Phone</p>
                                            <p className="text-sm text-muted-foreground">Receive a text or call to the business phone</p>
                                        </div>
                                    </Label>
                                </div>
                            </RadioGroup>
                        </div>

                        {method === 'email' ? (
                            <div className="grid gap-2">
                                <Label htmlFor="email">Business Email</Label>
                                <Input
                                    id="email"
                                    type="email"
                                    placeholder="contact@business.com"
                                    required
                                    value={contactInfo.email}
                                    onChange={(e) => setContactInfo({ ...contactInfo, email: e.target.value })}
                                />
                                <p className="text-xs text-muted-foreground">We will only use this for verification and official communications.</p>
                            </div>
                        ) : (
                            <div className="grid gap-2">
                                <Label htmlFor="phone">Business Phone Number</Label>
                                <Input
                                    id="phone"
                                    type="tel"
                                    placeholder="+1 (555) 000-0000"
                                    required
                                    value={contactInfo.phone}
                                    onChange={(e) => setContactInfo({ ...contactInfo, phone: e.target.value })}
                                />
                                <p className="text-xs text-muted-foreground">Ensure this is the official business number listed on Google or your website.</p>
                            </div>
                        )}
                    </div>
                </CardContent>

                <CardFooter className="flex flex-col space-y-4">
                    <Button type="submit" className="w-full" disabled={loading}>
                        {loading ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Processing Request...
                            </>
                        ) : (
                            <>
                                Continue to Verification
                                <ArrowRight className="ml-2 h-4 w-4" />
                            </>
                        )}
                    </Button>
                    <p className="text-center text-xs text-muted-foreground px-6">
                        By continuing, you confirm that you are an authorized representative of <strong>{business.name}</strong> and agree to our Terms of Service.
                    </p>
                </CardFooter>
            </form>
        </Card>
    );
}
