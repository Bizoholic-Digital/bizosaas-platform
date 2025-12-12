'use client';

import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, CheckCircle2, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

function CallbackContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [status, setStatus] = useState<'processing' | 'success' | 'error'>('processing');
    const [message, setMessage] = useState('Completing integration setup...');

    useEffect(() => {
        const handleCallback = async () => {
            const code = searchParams.get('code');
            const state = searchParams.get('state');
            const error = searchParams.get('error');

            if (error) {
                setStatus('error');
                setMessage(`Authorization failed: ${error}`);
                return;
            }

            if (!code || !state) {
                setStatus('error');
                setMessage('Invalid callback parameters. Missing code or state.');
                return;
            }

            try {
                // Decode state to get connectorId and tenantId
                // State format: tenant_id:connector_id
                const parts = state.split(':');
                if (parts.length < 2) {
                    throw new Error('Invalid state format');
                }
                const tenantId = parts[0];
                const connectorId = parts[1];

                const response = await fetch('/api/brain/oauth/callback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code,
                        state,
                        connector_id: connectorId,
                        tenant_id: tenantId,
                        redirect_uri: window.location.origin + window.location.pathname // Must match what was sent in auth URL
                    }),
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || data.message || 'Failed to exchange token');
                }

                setStatus('success');
                setMessage(`Successfully connected ${connectorId}! Redirecting...`);

                // Redirect back to integrations page after short delay
                setTimeout(() => {
                    router.push('/dashboard/integrations');
                }, 2000);

            } catch (err: any) {
                console.error('Callback error:', err);
                setStatus('error');
                setMessage(err.message || 'An error occurred during connection.');
            }
        };

        handleCallback();
    }, [searchParams, router]);

    return (
        <Card className="w-full max-w-md bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800">
            <CardHeader>
                <CardTitle className="text-center">Integration Setup</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center justify-center space-y-4 py-6">
                {status === 'processing' && (
                    <>
                        <Loader2 className="w-12 h-12 text-blue-500 animate-spin" />
                        <p className="text-gray-600 dark:text-gray-400 text-center">{message}</p>
                    </>
                )}

                {status === 'success' && (
                    <>
                        <CheckCircle2 className="w-12 h-12 text-green-500" />
                        <p className="text-green-600 dark:text-green-400 font-medium text-center">{message}</p>
                    </>
                )}

                {status === 'error' && (
                    <>
                        <XCircle className="w-12 h-12 text-red-500" />
                        <p className="text-red-600 dark:text-red-400 font-medium text-center">{message}</p>
                        <Button
                            onClick={() => router.push('/dashboard/integrations')}
                            className="mt-4"
                            variant="outline"
                        >
                            Return to Integrations
                        </Button>
                    </>
                )}
            </CardContent>
        </Card>
    );
}

export default function IntegrationsCallbackPage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950 p-4">
            <Suspense fallback={<Loader2 className="w-12 h-12 text-blue-500 animate-spin" />}>
                <CallbackContent />
            </Suspense>
        </div>
    );
}
