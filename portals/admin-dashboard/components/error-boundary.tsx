'use client';

import React from 'react';

interface ErrorBoundaryState {
    hasError: boolean;
    error?: Error;
}

interface ErrorBoundaryProps {
    children: React.ReactNode;
    fallback?: React.ComponentType<{ error: Error; reset: () => void }>;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): ErrorBoundaryState {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error('ErrorBoundary caught an error:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            const Fallback = this.props.fallback;
            if (Fallback && this.state.error) {
                return (
                    <Fallback
                        error={this.state.error}
                        reset={() => this.setState({ hasError: false, error: undefined })}
                    />
                );
            }

            return (
                <div className="min-h-[400px] flex items-center justify-center bg-gray-50 dark:bg-gray-900 rounded-xl border border-dashed border-gray-300 dark:border-gray-700">
                    <div className="max-w-md mx-auto text-center p-8">
                        <div className="bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/20 text-red-700 dark:text-red-400 px-6 py-4 rounded-xl shadow-sm">
                            <strong className="font-bold text-lg block mb-2">Something went wrong</strong>
                            <span className="text-sm">There was an unexpected error rendering this section.</span>
                            <div className="mt-4">
                                <button
                                    onClick={() => this.setState({ hasError: false, error: undefined })}
                                    className="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg text-sm transition-colors"
                                >
                                    Refresh Section
                                </button>
                            </div>
                        </div>
                        {this.state.error && (
                            <details className="mt-4 text-left">
                                <summary className="cursor-pointer text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400">View error details</summary>
                                <div className="mt-2 p-3 bg-gray-100 dark:bg-gray-800 rounded text-[10px] font-mono overflow-auto max-h-32 text-gray-700 dark:text-gray-300">
                                    {this.state.error.toString()}
                                </div>
                            </details>
                        )}
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
