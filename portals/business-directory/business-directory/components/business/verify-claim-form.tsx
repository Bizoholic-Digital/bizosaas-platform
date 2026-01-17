'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { CheckCircle2, Loader2, ArrowRight, RefreshCcw, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { businessAPI } from '@/lib/api';

interface VerifyClaimFormProps {
    claimId: string;
}

export function VerifyClaimForm({ claimId }: VerifyClaimFormProps) {
    const router = useRouter();
    const [code, setCode] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [resendLoading, setResendLoading] = useState(false);
    const [resendSuccess, setResendSuccess] = useState(false);

    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (code.length !== 6) {
            setError('Please enter a valid 6-digit code');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const result = await businessAPI.verifyClaim(claimId, code);
            if (result.success) {
                setSuccess(true);
                // Redirect after a brief delay
                setTimeout(() => {
                    router.push(`/business/${result.listing_id || ''}`);
                }, 3000);
            } else {
                setError(result.error || 'Verification failed');
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'Something went wrong');
        } finally {
            setLoading(false);
        }
    };

    const handleResend = async () => {
        if (resendLoading) return;
        setResendLoading(true);
        setError(null);
        setResendSuccess(false);

        try {
            const result = await businessAPI.resendVerificationCode(claimId);
            if (result.success) {
                setResendSuccess(true);
                // Clear success message after 5 seconds
                setTimeout(() => setResendSuccess(false), 5000);
            } else {
                setError(result.error || "Failed to resend code");
            }
        } catch (err: any) {
            setError("Failed to resend code. Please try again.");
        } finally {
            setResendLoading(false);
        }
    };

    if (success) {
        return (
            <Card className="max-w-md mx-auto border-green-200 bg-green-50/30">
                <CardContent className="pt-8 pb-8 text-center space-y-4">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <CheckCircle2 className="w-10 h-10 text-green-600" />
                    </div>
                    <CardTitle className="text-2xl font-bold text-green-900">Verified Successfully!</CardTitle>
                    <CardDescription className="text-green-800 font-medium">
                        Your claim has been approved. You now have full control over your business listing.
                    </CardDescription>
                    <p className="text-sm text-green-700">
                        Redirecting you to your business profile...
                    </p>
                    <Button variant="outline" className="mt-4" asChild>
                        <a href="/">Go to Homepage</a>
                    </Button>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="max-w-md mx-auto shadow-lg border-primary/20">
            <CardHeader className="text-center">
                <CardTitle className="text-2xl font-bold">Enter Verification Code</CardTitle>
                <CardDescription>
                    We've sent a 6-digit verification code to your business contact. Please enter it below to confirm your claim.
                </CardDescription>
            </CardHeader>

            <form onSubmit={handleSubmit}>
                <CardContent className="space-y-6">
                    {error && (
                        <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm flex items-start">
                            <AlertCircle className="w-4 h-4 mr-2 mt-0.5 flex-shrink-0" />
                            {error}
                        </div>
                    )}

                    {resendSuccess && (
                        <div className="p-3 bg-green-50 border border-green-200 text-green-700 rounded-md text-sm flex items-center justify-center">
                            <CheckCircle2 className="w-4 h-4 mr-2" />
                            Code resent successfully!
                        </div>
                    )}

                    <div className="flex justify-center">
                        <Input
                            type="text"
                            maxLength={6}
                            placeholder="0 0 0 0 0 0"
                            className="text-center text-3xl font-bold tracking-[0.5em] h-16 w-full max-w-[280px]"
                            value={code}
                            onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                            autoFocus
                        />
                    </div>

                    <p className="text-center text-sm text-muted-foreground">
                        The code will expire in 60 minutes.
                    </p>
                </CardContent>

                <CardFooter className="flex flex-col space-y-4">
                    <Button type="submit" className="w-full text-lg h-12" disabled={loading || code.length !== 6}>
                        {loading ? (
                            <>
                                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                                Verifying...
                            </>
                        ) : (
                            'Verify Code'
                        )}
                    </Button>

                    <button
                        type="button"
                        className="text-sm text-primary hover:underline flex items-center justify-center font-medium disabled:opacity-50"
                        onClick={handleResend}
                        disabled={resendLoading}
                    >
                        {resendLoading ? (
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        ) : (
                            <RefreshCcw className="w-4 h-4 mr-2" />
                        )}
                        {resendLoading ? 'Sending...' : 'Resend Code'}
                    </button>
                </CardFooter>
            </form>
        </Card>
    );
}
