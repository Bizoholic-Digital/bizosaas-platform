'use client';

import React from 'react';
import { DollarSign, TrendingUp, AlertCircle, Info } from 'lucide-react';

interface CampaignBudget {
    dailyLimit: number;
    currency: string;
}

interface CampaignBudgetSetupProps {
    budget: CampaignBudget;
    onUpdate: (budget: CampaignBudget) => void;
}

export function CampaignBudgetSetup({ budget, onUpdate }: CampaignBudgetSetupProps) {
    const MIN_BUDGET = 10;

    const handleBudgetChange = (value: string) => {
        const numValue = parseFloat(value);
        onUpdate({ ...budget, dailyLimit: isNaN(numValue) ? 0 : numValue });
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Campaign Budget</h2>
                <p className="text-gray-600 dark:text-gray-400">
                    Set your daily advertising budget. You can adjust this at any time in your dashboard.
                </p>
            </div>

            <div className="max-w-md mx-auto">
                <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                        Daily Budget (USD)
                    </label>
                    <div className="relative mb-6">
                        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                            <DollarSign className="h-6 w-6 text-gray-400" />
                        </div>
                        <input
                            type="number"
                            min={MIN_BUDGET}
                            step="1"
                            value={budget.dailyLimit}
                            onChange={(e) => handleBudgetChange(e.target.value)}
                            className="block w-full pl-12 pr-4 py-4 text-2xl font-bold border border-gray-300 dark:border-gray-600 rounded-xl bg-gray-50 dark:bg-gray-900 focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                            placeholder="0.00"
                        />
                    </div>

                    {budget.dailyLimit < MIN_BUDGET && (
                        <div className="flex items-center space-x-2 text-amber-600 dark:text-amber-400 text-sm mb-6 bg-amber-50 dark:bg-amber-900/20 p-3 rounded-lg border border-amber-100 dark:border-amber-800">
                            <AlertCircle className="h-5 w-5 flex-shrink-0" />
                            <span>Minimum daily budget is ${MIN_BUDGET} to ensure effective campaign learning.</span>
                        </div>
                    )}

                    <div className="space-y-4">
                        <div className="flex justify-between text-sm">
                            <span className="text-gray-600 dark:text-gray-400">Monthly Projection</span>
                            <span className="font-semibold text-gray-900 dark:text-white">
                                ${(budget.dailyLimit * 30.4).toFixed(2)}
                            </span>
                        </div>
                        <div className="h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-blue-600 transition-all duration-500"
                                style={{ width: `${Math.min((budget.dailyLimit / 100) * 100, 100)}%` }}
                            />
                        </div>
                    </div>
                </div>

                <div className="mt-8 grid grid-cols-1 gap-4">
                    <div className="flex items-start space-x-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
                        <TrendingUp className="h-5 w-5 text-blue-600 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-blue-900 dark:text-blue-300">Optimization Goal</p>
                            <p className="text-xs text-blue-800/80 dark:text-blue-400/80">
                                We'll automatically allocate this budget across your selected platforms for maximum ROI.
                            </p>
                        </div>
                    </div>
                    <div className="flex items-start space-x-3 p-4 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700">
                        <Info className="h-5 w-5 text-gray-400 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">No Hidden Fees</p>
                            <p className="text-xs text-gray-600 dark:text-gray-400">
                                100% of this budget goes directly to ad spend on your connected platforms.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
