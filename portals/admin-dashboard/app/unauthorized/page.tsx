'use client';
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { PlatformBranding } from "@/components/ui/platform-branding";
import { useClerk } from "@clerk/nextjs";

export default function UnauthorizedPage() {
    const { signOut } = useClerk();

    const handleSignOut = async () => {
        await signOut({ redirectUrl: '/login' });
    };


    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 via-white to-orange-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950">
            <div className="max-w-md w-full mx-4">
                <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl p-8 space-y-8 border border-gray-200 dark:border-gray-800">
                    {/* Header */}
                    <div className="text-center space-y-4">
                        <div className="flex justify-center">
                            <div className="w-20 h-20 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center">
                                <svg
                                    className="w-10 h-10 text-red-600 dark:text-red-400"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                                    />
                                </svg>
                            </div>
                        </div>
                        <div>
                            <h2 className="text-3xl font-bold text-red-600 dark:text-red-400">
                                Access Denied
                            </h2>
                            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                                You don't have permission to access this resource
                            </p>
                        </div>
                    </div>

                    {/* Error Details */}
                    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                        <div className="space-y-2">
                            <p className="text-sm font-medium text-red-900 dark:text-red-300">
                                Required Permissions:
                            </p>
                            <ul className="text-xs text-red-700 dark:text-red-400 space-y-1 ml-4 list-disc">
                                <li>Platform Administrator</li>
                                <li>Super Administrator</li>
                            </ul>
                        </div>
                    </div>

                    {/* Message */}
                    <div className="text-center space-y-4">
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                            The BizOSaaS Admin Dashboard is restricted to platform administrators only.
                            If you believe you should have access, please contact your system administrator.
                        </p>
                    </div>

                    {/* Actions */}
                    <div className="space-y-3">
                        <Button
                            onClick={handleSignOut}
                            className="w-full h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                        >
                            <svg
                                className="w-5 h-5 mr-2"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                                />
                            </svg>
                            Sign Out & Return to Login
                        </Button>
                        <a
                            href="mailto:admin@bizosaas.com"
                            className="block text-center text-sm text-blue-600 dark:text-blue-400 hover:underline"
                        >
                            Request Access
                        </a>
                    </div>

                    {/* Footer */}
                    <div className="pt-6 border-t border-gray-200 dark:border-gray-800">
                        <div className="flex justify-center">
                            <PlatformBranding platform="BIZOSAAS" size="sm" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
