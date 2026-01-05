'use client';

import { SignIn, SignOutButton, SignedIn, SignedOut } from '@clerk/nextjs';

export function ClerkSignInWrapper() {
    return (
        <div className="flex flex-col items-center gap-4">
            <div className="p-2 bg-yellow-100 text-yellow-800 rounded mb-4 text-xs font-mono">
                Debug: Wrapper Loaded v2
            </div>

            <SignedIn>
                <div className="p-4 bg-green-100 text-green-800 rounded mb-4 text-center">
                    <p className="mb-2 font-bold">You are already signed in!</p>
                    <SignOutButton>
                        <button className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition">
                            Sign Out & Retry
                        </button>
                    </SignOutButton>
                </div>
            </SignedIn>

            <SignedOut>
                <SignIn
                    appearance={{
                        elements: {
                            rootBox: "mx-auto",
                            card: "shadow-2xl"
                        }
                    }}
                    routing="path"
                    path="/login"
                    forceRedirectUrl="/dashboard"
                    signUpUrl="/signup"
                />
            </SignedOut>
        </div>
    );
}
