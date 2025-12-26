'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function AdminLoginPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the central login on the Client Portal
    const callbackUrl = encodeURIComponent('https://admin.bizoholic.net/dashboard');
    const loginUrl = process.env.NODE_ENV === 'production'
      ? `https://app.bizoholic.net/login?callbackUrl=${callbackUrl}`
      : `/api/auth/signin`; // Fallback for local dev

    window.location.href = loginUrl;
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">
      <div className="text-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <h1 className="text-xl font-medium text-slate-400">Redirecting to Secure Gate...</h1>
        <p className="text-sm text-slate-500">You are being moved to the central BizOSaaS login portal.</p>
      </div>
    </div>
  );
}