'use client';

import { useState } from 'react';
import LoginForm from '@/components/LoginForm';
import TestCredentials from '@/components/TestCredentials';

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedEmail, setSelectedEmail] = useState('');
  const [selectedPassword, setSelectedPassword] = useState('');
  const [showTestCreds, setShowTestCreds] = useState(true); // Dev mode toggle

  const handleLogin = async (email: string, password: string) => {
    setLoading(true);
    setError('');

    try {
      // Call auth service directly (temporary workaround)
      const response = await fetch('http://localhost:8008/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // Important for cookies
        body: JSON.stringify({
          email,
          password
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Invalid credentials');
      }

      const data = await response.json();

      // Store tokens
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      localStorage.setItem('user_data', JSON.stringify(data.user));

      // Check for return URL parameter
      const urlParams = new URLSearchParams(window.location.search);
      const returnUrl = urlParams.get('return_url');

      if (returnUrl) {
        // If there's a return URL, redirect there with auth data
        const decodedReturnUrl = decodeURIComponent(returnUrl);
        const authParams = new URLSearchParams({
          token: data.access_token,
          user: encodeURIComponent(JSON.stringify(data.user))
        });
        window.location.href = `${decodedReturnUrl}?${authParams.toString()}`;
      } else {
        // Role-based routing (default behavior)
        const role = data.user.role;

        console.log('Login successful! User role:', role);
        console.log('Redirecting based on role...');

        switch (role) {
          case 'super_admin':
            window.location.href = 'http://localhost:8005'; // SQLAdmin
            break;
          case 'tenant_admin':
            window.location.href = 'http://localhost:3009'; // Admin Dashboard
            break;
          case 'user':
            window.location.href = 'http://localhost:3001'; // Client Portal
            break;
          default:
            window.location.href = 'http://localhost:3001';
        }
      }
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCredential = (email: string, password: string) => {
    setSelectedEmail(email);
    setSelectedPassword(password);
    // Auto-login after selection
    handleLogin(email, password);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>

      <div className="relative z-10 bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md border border-gray-100">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-block p-3 bg-gradient-to-br from-bizosaas-blue to-bizosaas-purple rounded-xl mb-4">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            BizOSaaS Platform
          </h1>
          <p className="text-gray-600">Unified Authentication Portal</p>
        </div>

        {/* Login Form */}
        <LoginForm
          onSubmit={handleLogin}
          loading={loading}
          error={error}
          initialEmail={selectedEmail}
          initialPassword={selectedPassword}
        />

        {/* Test Credentials (Dev Mode) */}
        {showTestCreds && (
          <TestCredentials onSelectCredential={handleSelectCredential} />
        )}

        {/* Footer */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="text-center space-y-2">
            <p className="text-xs text-gray-500 font-semibold">
              Powered by Brain Gateway AI
            </p>
            <div className="flex items-center justify-center gap-4 text-xs text-gray-400">
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                93 AI Agents
              </span>
              <span>•</span>
              <span>Multi-Tenant</span>
              <span>•</span>
              <span>Secured</span>
            </div>
          </div>
        </div>

        {/* Dev Mode Toggle */}
        <button
          onClick={() => setShowTestCreds(!showTestCreds)}
          className="mt-4 w-full text-xs text-gray-400 hover:text-gray-600 transition-colors"
        >
          {showTestCreds ? '🔒 Hide' : '🧪 Show'} Test Credentials
        </button>
      </div>

      {/* Version Info */}
      <div className="absolute bottom-4 right-4 text-xs text-gray-400">
        v2.1.0 • {new Date().getFullYear()}
      </div>
    </div>
  );
}