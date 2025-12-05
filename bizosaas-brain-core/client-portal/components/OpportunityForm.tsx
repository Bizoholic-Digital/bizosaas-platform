'use client';

import React, { useState } from 'react';
import { Modal } from './Modal';

interface OpportunityFormProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (opportunityData: any) => void;
    initialData?: any;
}

export const OpportunityForm: React.FC<OpportunityFormProps> = ({
    isOpen,
    onClose,
    onSubmit,
    initialData
}) => {
    const [formData, setFormData] = useState({
        title: initialData?.title || '',
        value: initialData?.value || '',
        currency: initialData?.currency || 'USD',
        stage: initialData?.stage || 'discovery',
        probability: initialData?.probability || '20',
        expected_close_date: initialData?.expected_close_date || '',
        company: initialData?.company || '',
        contact_id: initialData?.contact_id || '',
        description: initialData?.description || '',
        source: initialData?.source || 'outbound',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            value: parseFloat(formData.value),
            probability: parseInt(formData.probability)
        });
        onClose();
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title={initialData ? 'Edit Opportunity' : 'Add New Opportunity'} size="lg">
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Title */}
                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Opportunity Title *
                        </label>
                        <input
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Value */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Value *
                        </label>
                        <div className="relative">
                            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                                {formData.currency === 'USD' ? '$' : formData.currency}
                            </span>
                            <input
                                type="number"
                                name="value"
                                value={formData.value}
                                onChange={handleChange}
                                required
                                min="0"
                                step="0.01"
                                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>
                    </div>

                    {/* Currency */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Currency
                        </label>
                        <select
                            name="currency"
                            value={formData.currency}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="USD">USD - US Dollar</option>
                            <option value="EUR">EUR - Euro</option>
                            <option value="GBP">GBP - British Pound</option>
                            <option value="INR">INR - Indian Rupee</option>
                        </select>
                    </div>

                    {/* Stage */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Stage
                        </label>
                        <select
                            name="stage"
                            value={formData.stage}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="discovery">Discovery</option>
                            <option value="qualification">Qualification</option>
                            <option value="proposal">Proposal</option>
                            <option value="negotiation">Negotiation</option>
                            <option value="closed_won">Closed Won</option>
                            <option value="closed_lost">Closed Lost</option>
                        </select>
                    </div>

                    {/* Probability */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Probability (%)
                        </label>
                        <input
                            type="number"
                            name="probability"
                            value={formData.probability}
                            onChange={handleChange}
                            min="0"
                            max="100"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Expected Close Date */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Expected Close Date
                        </label>
                        <input
                            type="date"
                            name="expected_close_date"
                            value={formData.expected_close_date}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Company */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Company
                        </label>
                        <input
                            type="text"
                            name="company"
                            value={formData.company}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Contact ID */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Contact ID (Optional)
                        </label>
                        <input
                            type="text"
                            name="contact_id"
                            value={formData.contact_id}
                            onChange={handleChange}
                            placeholder="Enter Contact ID"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Source */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Source
                        </label>
                        <select
                            name="source"
                            value={formData.source}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="outbound">Outbound</option>
                            <option value="inbound">Inbound</option>
                            <option value="referral">Referral</option>
                            <option value="partner">Partner</option>
                            <option value="event">Event</option>
                        </select>
                    </div>
                </div>

                {/* Description */}
                <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Description
                    </label>
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        rows={4}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                </div>

                {/* Buttons */}
                <div className="flex justify-end gap-4 pt-4 border-t border-gray-200 dark:border-gray-800">
                    <button
                        type="button"
                        onClick={onClose}
                        className="px-6 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        {initialData ? 'Update Opportunity' : 'Create Opportunity'}
                    </button>
                </div>
            </form>
        </Modal>
    );
};
