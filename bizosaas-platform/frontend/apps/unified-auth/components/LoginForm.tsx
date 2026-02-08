'use client';

import { useState, useEffect } from 'react';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
  loading: boolean;
  error: string;
  initialEmail?: string;
  initialPassword?: string;
}

export default function LoginForm({
  onSubmit,
  loading,
  error,
  initialEmail = '',
  initialPassword = ''
}: LoginFormProps) {
  const [email, setEmail] = useState(initialEmail);
  const [password, setPassword] = useState(initialPassword);

  useEffect(() => {
    if (initialEmail) setEmail(initialEmail);
    if (initialPassword) setPassword(initialPassword);
  }, [initialEmail, initialPassword]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(email, password);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 border border-red-300 rounded-lg">
          <div className="flex items-center gap-2">
            <svg
              className="w-5 h-5 text-red-600"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p className="text-sm text-red-800">{error}</p>
          </div>
        </div>
      )}

      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Email Address
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-bizosaas-blue focus:border-transparent transition-all"
          placeholder="Enter your email address"
          disabled={loading}
        />
      </div>

      <div>
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-bizosaas-blue focus:border-transparent transition-all"
          placeholder="Enter your password"
          disabled={loading}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-gradient-to-r from-bizosaas-blue to-bizosaas-indigo text-white py-3 px-4 rounded-lg font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <svg
              className="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Authenticating...</span>
          </>
        ) : (
          <>
            <svg
              className="w-5 h-5"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
            </svg>
            <span>Sign In</span>
          </>
        )}
      </button>

      <div className="text-center text-sm text-gray-600">
        <a href="#" className="hover:text-bizosaas-blue transition-colors">
          Forgot password?
        </a>
      </div>
    </form>
  );
}