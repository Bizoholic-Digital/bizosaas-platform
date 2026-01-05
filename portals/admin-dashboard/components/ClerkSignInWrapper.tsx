'use client';

import { SignIn } from '@clerk/nextjs';

export function ClerkSignInWrapper() {
    return (
        <SignIn
            appearance={{
                elements: {
                    rootBox: "mx-auto",
                    card: "shadow-2xl bg-white dark:bg-gray-800"
                }
            }}
            routing="path"
            path="/login"
            forceRedirectUrl="/dashboard"
            signUpUrl="/signup"
        />
    );
}
