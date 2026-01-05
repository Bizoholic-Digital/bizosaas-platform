'use client';

import { SignIn } from '@clerk/nextjs';

export function ClerkSignInWrapper() {
    return (
        <div className="flex flex-col items-center gap-4">
            <div className="p-2 bg-yellow-100 text-yellow-800 rounded mb-4 text-xs font-mono">
                Debug: Wrapper Loaded
            </div>
            <SignIn
                appearance={{
                    elements: {
                        rootBox: "mx-auto",
                        card: "shadow-2xl"
                    }
                }}
                redirectUrl="/dashboard"
                signUpUrl="/signup"
            />
        </div>
    );
}
