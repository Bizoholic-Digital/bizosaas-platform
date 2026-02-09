import React from 'react';
import { Header } from '@/components/layout/header';
import { VerifyClaimForm } from '@/components/business/verify-claim-form';
import { ShieldCheck } from 'lucide-react';

interface Props {
    params: { id: string };
}

export default function VerifyClaimPage({ params }: Props) {
    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
            <Header />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                <div className="flex flex-col items-center mb-12">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-6">
                        <ShieldCheck className="w-8 h-8 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold text-center">Security Verification</h1>
                    <p className="text-muted-foreground text-center max-w-md mt-2">
                        To protect the integrity of our directory, we need to confirm you have access to the business's official communication channels.
                    </p>
                </div>

                <VerifyClaimForm claimId={params.id} />

                <div className="mt-20 max-w-3xl mx-auto border-t pt-12 text-center text-sm text-muted-foreground">
                    <p>Having trouble verifying? Our support team is here to help.</p>
                    <div className="flex justify-center space-x-6 mt-4">
                        <a href="/help" className="hover:text-foreground">Help Articles</a>
                        <a href="/contact" className="hover:text-foreground">Contact Support</a>
                    </div>
                </div>
            </main>
        </div>
    );
}
