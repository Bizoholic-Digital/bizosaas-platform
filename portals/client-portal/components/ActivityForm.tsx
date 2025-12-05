'use client';

import React, { useState } from 'react';
import { Modal } from './Modal';

interface ActivityFormProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (activityData: any) => void;
    initialData?: any;
}

export const ActivityForm: React.FC<ActivityFormProps> = ({
    isOpen,
    onClose,
    onSubmit,
    initialData
}) => {
    const [formData, setFormData] = useState({
        type: initialData?.type || 'call',
        subject: initialData?.subject || '',
        description: initialData?.description || '',
        date: initialData?.date || '',
        duration: initialData?.duration || '30',
        status: initialData?.status || 'planned',
        priority: initialData?.priority || 'medium',
        assigned_to: initialData?.assigned_to || '',
        contact_id: initialData?.contact_id || '',
        deal_id: initialData?.deal_id || '',
        lead_id: initialData?.lead_id || '',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            duration: parseInt(formData.duration)
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
        <Modal isOpen={isOpen} onClose={onClose} title={initialData ? 'Edit Activity' : 'Add New Activity'} size="lg">
            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Type */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Type *
                        </label>
                        <select
                            name="type"
                            value={formData.type}
                            onChange={handleChange}
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="call">Call</option>
                            <option value="meeting">Meeting</option>
                            <option value="email">Email</option>
                            <option value="task">Task</option>
                            <option value="demo">Demo</option>
                            <option value="lunch">Lunch</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    {/* Subject */}
                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Subject *
                        </label>
                        <input
                            type="text"
                            name="subject"
                            value={formData.subject}
                            onChange={handleChange}
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Date */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Date & Time *
                        </label>
                        <input
                            type="datetime-local"
                            name="date"
                            value={formData.date}
                            onChange={handleChange}
                            required
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Duration */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Duration (minutes)
                        </label>
                        <input
                            type="number"
                            name="duration"
                            value={formData.duration}
                            onChange={handleChange}
                            min="0"
                            step="15"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Status */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Status
                        </label>
                        <select
                            name="status"
                            value={formData.status}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="planned">Planned</option>
                            <option value="completed">Completed</option>
                            <option value="cancelled">Cancelled</option>
                            <option value="rescheduled">Rescheduled</option>
                        </select>
                    </div>

                    {/* Priority */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Priority
                        </label>
                        <select
                            name="priority"
                            value={formData.priority}
                            onChange={handleChange}
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>

                    {/* Assigned To */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Assigned To *
                        </label>
                        <input
                            type="text"
                            name="assigned_to"
                            value={formData.assigned_to}
                            onChange={handleChange}
                            required
                            placeholder="Username or Email"
                            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Related To (Optional) */}
                    <div className="md:col-span-2 border-t border-gray-200 dark:border-gray-800 pt-4 mt-2">
                        <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-4">Related To (Optional)</h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                    Lead ID
                                </label>
                                <input
                                    type="text"
                                    name="lead_id"
                                    value={formData.lead_id}
                                    onChange={handleChange}
                                    className="w-full px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                    Contact ID
                                </label>
                                <input
                                    type="text"
                                    name="contact_id"
                                    value={formData.contact_id}
                                    onChange={handleChange}
                                    className="w-full px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-sm"
                                />
                            </div>
                            <div>
                                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                                    Deal ID
                                </label>
                                <input
                                    type="text"
                                    name="deal_id"
                                    value={formData.deal_id}
                                    onChange={handleChange}
                                    className="w-full px-3 py-1.5 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-sm"
                                />
                            </div>
                        </div>
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
                        {initialData ? 'Update Activity' : 'Create Activity'}
                    </button>
                </div>
            </form>
        </Modal>
    );
};
