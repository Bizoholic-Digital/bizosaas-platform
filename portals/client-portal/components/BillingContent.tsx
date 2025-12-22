'use client';

import React, { useState, useEffect } from 'react';
import {
    CreditCard, FileText, Check, AlertTriangle,
    Download, Plus, Star, Shield, Zap, RefreshCw
} from 'lucide-react';
import { billingApi, SubscriptionPlan, Subscription, Invoice } from '@/lib/api/billing';
import { toast } from 'sonner';

interface BillingContentProps {
    activeTab: string;
}

export const BillingContent: React.FC<BillingContentProps> = ({ activeTab }) => {
    const [currentTab, setCurrentTab] = useState('overview');

    // Data States
    const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
    const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
    const [invoices, setInvoices] = useState<Invoice[]>([]);
    const [connection, setConnection] = useState<{ connected: boolean; platform?: string } | null>(null);

    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchBillingData();
    }, []);

    const fetchBillingData = async () => {
        setIsLoading(true);
        try {
            // Parallel fetch
            const [statusRes, plansRes, subsRes, invoicesRes] = await Promise.all([
                billingApi.getStatus(),
                billingApi.getPlans(),
                billingApi.getSubscriptions(),
                billingApi.getInvoices()
            ]);

            if (statusRes.data) setConnection(statusRes.data);
            if (plansRes.data) setPlans(plansRes.data);
            if (subsRes.data) setSubscriptions(subsRes.data);
            if (invoicesRes.data) setInvoices(invoicesRes.data);

        } catch (error) {
            console.error('Failed to fetch billing data:', error);
            toast.error("Failed to load billing information.");
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    // Mock usage data for now since backend doesn't provide it yet
    const usage = {
        leads: { used: 450, limit: 1000 },
        storage: { used: 2.5, limit: 10, unit: 'GB' },
        api_calls: { used: 15200, limit: 50000 }
    };

    // Find current plan
    const currentSubscription = subscriptions[0];
    const currentPlan = plans.find(p => p.code === currentSubscription?.plan_id) || { name: 'Free', code: 'free' };

    const renderOverview = () => (
        <div className="space-y-6">
            {/* Connection Status Banner */}
            {connection && !connection.connected && (
                <div className="bg-orange-50 text-orange-800 p-4 rounded-lg flex items-center gap-3 border border-orange-200">
                    <AlertTriangle className="h-5 w-5" />
                    <div>
                        <h4 className="font-semibold">Billing System Disconnected</h4>
                        <p className="text-sm">We are unable to connect to the billing provider. Displayed data may be outdated.</p>
                    </div>
                    <button onClick={fetchBillingData} className="ml-auto text-sm font-medium hover:underline">Retry</button>
                </div>
            )}

            {/* Current Plan Card */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-6 text-white shadow-lg">
                <div className="flex justify-between items-start">
                    <div>
                        <p className="text-purple-100 font-medium mb-1">Current Plan</p>
                        <h2 className="text-3xl font-bold mb-2">{currentPlan.name}</h2>
                        <p className="text-purple-100 opacity-90">
                            Status: <span className="font-semibold uppercase">{currentSubscription?.status || 'Inactive'}</span>
                        </p>
                        {currentSubscription?.current_period_end && (
                            <p className="text-purple-100 opacity-90 text-sm mt-1">
                                Renews: {new Date(currentSubscription.current_period_end).toLocaleDateString()}
                            </p>
                        )}
                    </div>
                    <div className="bg-white/20 p-3 rounded-lg backdrop-blur-sm">
                        <Star className="w-8 h-8 text-white" />
                    </div>
                </div>
                <div className="mt-6 flex gap-4">
                    <button className="bg-white text-purple-600 px-4 py-2 rounded-lg font-semibold hover:bg-purple-50 transition-colors">
                        Manage Subscription
                    </button>
                    <button className="bg-purple-700/50 text-white px-4 py-2 rounded-lg font-semibold hover:bg-purple-700 transition-colors">
                        View Usage
                    </button>
                </div>
            </div>

            {/* Usage Stats (Mock for now) */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white">Leads Used</h3>
                        <span className="text-xs font-medium text-gray-500">
                            {Math.round((usage.leads.used / usage.leads.limit) * 100)}%
                        </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
                        <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${(usage.leads.used / usage.leads.limit) * 100}%` }}
                        ></div>
                    </div>
                    <p className="text-sm text-gray-500">{usage.leads.used.toLocaleString()} / {usage.leads.limit.toLocaleString()} leads</p>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white">Storage</h3>
                        <span className="text-xs font-medium text-gray-500">
                            {Math.round((usage.storage.used / usage.storage.limit) * 100)}%
                        </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
                        <div
                            className="bg-green-600 h-2 rounded-full"
                            style={{ width: `${(usage.storage.used / usage.storage.limit) * 100}%` }}
                        ></div>
                    </div>
                    <p className="text-sm text-gray-500">{usage.storage.used} {usage.storage.unit} / {usage.storage.limit} {usage.storage.unit}</p>
                </div>

                <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white">API Calls</h3>
                        <span className="text-xs font-medium text-gray-500">
                            {Math.round((usage.api_calls.used / usage.api_calls.limit) * 100)}%
                        </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-2">
                        <div
                            className="bg-purple-600 h-2 rounded-full"
                            style={{ width: `${(usage.api_calls.used / usage.api_calls.limit) * 100}%` }}
                        ></div>
                    </div>
                    <p className="text-sm text-gray-500">{(usage.api_calls.used / 1000).toFixed(1)}k / {(usage.api_calls.limit / 1000).toFixed(0)}k calls</p>
                </div>
            </div>
        </div>
    );

    const renderPlans = () => (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {plans.map((plan) => {
                const isCurrent = currentSubscription?.plan_id === plan.code;
                return (
                    <div
                        key={plan.id || plan.code}
                        className={`relative bg-white dark:bg-gray-900 rounded-lg border ${isCurrent
                            ? 'border-purple-500 dark:border-purple-500 ring-2 ring-purple-500/20'
                            : 'border-gray-200 dark:border-gray-800'
                            } p-6 flex flex-col`}
                    >
                        {isCurrent && (
                            <div className="absolute top-0 right-0 bg-purple-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">
                                CURRENT PLAN
                            </div>
                        )}
                        <div className="mb-4">
                            <h3 className="text-lg font-bold text-gray-900 dark:text-white">{plan.name}</h3>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Inclusive of taxes & fees</p>
                        </div>
                        <div className="mb-6">
                            <span className="text-3xl font-bold text-gray-900 dark:text-white">{plan.currency} {plan.amount}</span>
                            <span className="text-gray-500 dark:text-gray-400">/{plan.interval}</span>
                        </div>
                        {/* Features list would come from API or hardcoded map based on plan code */}
                        <ul className="space-y-3 mb-8 flex-1">
                            <li className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                                <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                                Core Platform Access
                            </li>
                            <li className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                                <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                                {plan.trial_period_days ? `${plan.trial_period_days}-day Free Trial` : 'Instant Access'}
                            </li>
                        </ul>
                        <button
                            className={`w-full py-2 rounded-lg font-semibold transition-colors ${isCurrent
                                ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed'
                                : 'bg-blue-600 text-white hover:bg-blue-700'
                                }`}
                            disabled={isCurrent}
                        >
                            {isCurrent ? 'Current Plan' : 'Upgrade'}
                        </button>
                    </div>
                )
            })}
            {plans.length === 0 && (
                <div className="col-span-3 text-center py-12 text-gray-500">
                    No plans available.
                </div>
            )}
        </div>
    );

    const renderPaymentMethods = () => (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Payment Methods</h3>
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 text-sm">
                    <Plus className="w-4 h-4" /> Add Method
                </button>
            </div>

            {/* Mock payment methods for visual consistency until API ready */}
            <div className="space-y-4">
                <div className="text-center py-8 text-gray-500 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-dashed border-gray-200 dark:border-gray-700">
                    <CreditCard className="w-8 h-8 mx-auto mb-2 text-gray-400" />
                    <p>Manage payment methods in the Client Portal Billing settings.</p>
                </div>
            </div>
        </div>
    );

    const renderInvoices = () => (
        <div className="bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 overflow-hidden">
            <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-800">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Invoice</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Amount</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Download</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                    {invoices.length === 0 ? (
                        <tr><td colSpan={5} className="px-6 py-12 text-center text-gray-500">No invoices found.</td></tr>
                    ) : (
                        invoices.map((invoice) => (
                            <tr key={invoice.id}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                    {invoice.id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                    {new Date(invoice.created_at).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                    {invoice.currency} {(invoice.amount_due).toFixed(2)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                                        {invoice.status || 'Paid'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button className="text-blue-600 hover:text-blue-800 dark:hover:text-blue-400">
                                        <Download className="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        )))}
                </tbody>
            </table>
        </div>
    );

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Billing & Subscription</h2>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-200 dark:border-gray-800">
                <nav className="-mb-px flex space-x-8">
                    {['Overview', 'Plans', 'Payment Methods', 'Invoices'].map((tab) => {
                        const tabKey = tab.toLowerCase().replace(' ', '-');
                        return (
                            <button
                                key={tab}
                                onClick={() => setCurrentTab(tabKey)}
                                className={`
                  whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm
                  ${currentTab === tabKey
                                        ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'}
                `}
                            >
                                {tab}
                            </button>
                        );
                    })}
                </nav>
            </div>

            {/* Content */}
            <div className="mt-6">
                {currentTab === 'overview' && renderOverview()}
                {currentTab === 'plans' && renderPlans()}
                {currentTab === 'payment-methods' && renderPaymentMethods()}
                {currentTab === 'invoices' && renderInvoices()}
            </div>
        </div>
    );
};
