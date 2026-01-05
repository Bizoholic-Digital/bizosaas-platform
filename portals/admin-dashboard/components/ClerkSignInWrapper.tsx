'use client';

import { SignIn } from '@clerk/nextjs';

export function ClerkSignInWrapper() {
    return (
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
    );
}
