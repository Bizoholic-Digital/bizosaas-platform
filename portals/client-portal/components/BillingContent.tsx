'use client';

import React, { useState, useEffect } from 'react';
import {
    CreditCard, FileText, Check, AlertTriangle,
    Download, Plus, Star, Shield, Zap
} from 'lucide-react';

interface BillingContentProps {
    activeTab: string;
}

export const BillingContent: React.FC<BillingContentProps> = ({ activeTab }) => {
    const [currentTab, setCurrentTab] = useState('overview');
    const [data, setData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/api/brain/billing');
                if (response.ok) {
                    const result = await response.json();
                    setData(result);
                }
            } catch (error) {
                console.error('Failed to fetch billing data:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (!data) return null;

    const { subscription, usage, invoices, payment_methods: paymentMethods } = data;

    const plans = [
        {
            name: 'Basic',
            price: '$29',
            period: '/month',
            description: 'Essential features for small businesses',
            features: ['5 Team Members', '1,000 Leads', 'Basic Analytics', 'Email Support'],
            current: subscription.plan === 'Basic',
            color: 'blue'
        },
        {
            name: 'Professional',
            price: '$99',
            period: '/month',
            description: 'Advanced tools for growing companies',
            features: ['Unlimited Team Members', '10,000 Leads', 'Advanced Analytics', 'Priority Support', 'AI Assistant'],
            current: subscription.plan === 'Professional',
            color: 'purple'
        },
        {
            name: 'Enterprise',
            price: 'Custom',
            period: '',
            description: 'Tailored solutions for large organizations',
            features: ['Unlimited Everything', 'Custom Integrations', 'Dedicated Account Manager', 'SLA', 'On-premise Option'],
            current: subscription.plan === 'Enterprise',
            color: 'gray'
        }
    ];

    const renderOverview = () => (
        <div className="space-y-6">
            {/* Current Plan Card */}
            <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg p-6 text-white shadow-lg">
                <div className="flex justify-between items-start">
                    <div>
                        <p className="text-purple-100 font-medium mb-1">Current Plan</p>
                        <h2 className="text-3xl font-bold mb-2">{subscription.plan}</h2>
                        <p className="text-purple-100 opacity-90">
                            Next billing date: <span className="font-semibold">{new Date(subscription.next_billing_date).toLocaleDateString()}</span>
                        </p>
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

            {/* Usage Stats */}
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
            {plans.map((plan) => (
                <div
                    key={plan.name}
                    className={`relative bg-white dark:bg-gray-900 rounded-lg border ${plan.current
                        ? 'border-purple-500 dark:border-purple-500 ring-2 ring-purple-500/20'
                        : 'border-gray-200 dark:border-gray-800'
                        } p-6 flex flex-col`}
                >
                    {plan.current && (
                        <div className="absolute top-0 right-0 bg-purple-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">
                            CURRENT PLAN
                        </div>
                    )}
                    <div className="mb-4">
                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">{plan.name}</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{plan.description}</p>
                    </div>
                    <div className="mb-6">
                        <span className="text-3xl font-bold text-gray-900 dark:text-white">{plan.price}</span>
                        <span className="text-gray-500 dark:text-gray-400">{plan.period}</span>
                    </div>
                    <ul className="space-y-3 mb-8 flex-1">
                        {plan.features.map((feature, idx) => (
                            <li key={idx} className="flex items-center text-sm text-gray-600 dark:text-gray-300">
                                <Check className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" />
                                {feature}
                            </li>
                        ))}
                    </ul>
                    <button
                        className={`w-full py-2 rounded-lg font-semibold transition-colors ${plan.current
                            ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 cursor-not-allowed'
                            : 'bg-blue-600 text-white hover:bg-blue-700'
                            }`}
                        disabled={plan.current}
                    >
                        {plan.current ? 'Current Plan' : 'Upgrade'}
                    </button>
                </div>
            ))}
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

            <div className="space-y-4">
                {paymentMethods.map((method) => (
                    <div key={method.id} className="flex items-center justify-between p-4 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg">
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-8 bg-gray-100 dark:bg-gray-800 rounded flex items-center justify-center">
                                <CreditCard className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                            </div>
                            <div>
                                <p className="font-medium text-gray-900 dark:text-white">
                                    {method.type} ending in {method.last4}
                                </p>
                                <p className="text-sm text-gray-500">Expires {method.expiry}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            {method.default && (
                                <span className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 px-2 py-1 rounded-full">
                                    Default
                                </span>
                            )}
                            <button className="text-gray-400 hover:text-red-600">Delete</button>
                        </div>
                    </div>
                ))}
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
                    {invoices.map((invoice) => (
                        <tr key={invoice.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                {invoice.id}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                {invoice.date}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                                {invoice.amount}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                                <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                                    {invoice.status}
                                </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                <button className="text-blue-600 hover:text-blue-800 dark:hover:text-blue-400">
                                    <Download className="w-4 h-4" />
                                </button>
                            </td>
                        </tr>
                    ))}
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
