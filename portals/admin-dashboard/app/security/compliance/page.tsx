'use client';

import React, { useState, useEffect } from 'react';
import {
    ShieldCheck,
    Lock,
    Globe,
    FileCheck,
    AlertCircle,
    CheckCircle2,
    Server,
    ChevronRight,
    Fingerprint,
    Info
} from 'lucide-react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell
} from 'recharts';

interface ComplianceControl {
    id: string;
    label: string;
    passed: boolean;
}

interface ComplianceFramework {
    name: string;
    status: string;
    score: number;
    controls: ComplianceControl[];
}

interface ComplianceData {
    phase: string;
    overall_score: number;
    frameworks: ComplianceFramework[];
}

export default function ComplianceCenterPage() {
    const [data, setData] = useState<ComplianceData | null>(null);
    const [loading, setLoading] = useState(true);
    const [selectedFramework, setSelectedFramework] = useState<number>(0);

    useEffect(() => {
        // Fetch from backend
        const fetchData = async () => {
            try {
                const response = await fetch('/api/admin/compliance/status');
                const json = await response.json();
                setData(json);
            } catch (e) {
                console.error("Failed to fetch compliance status", e);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50/50 dark:bg-gray-900/50">
                <div className="flex flex-col items-center">
                    <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                    <p className="mt-4 text-gray-500 font-medium">Validating compliance protocols...</p>
                </div>
            </div>
        );
    }

    const chartData = data?.frameworks.map(f => ({
        name: f.name,
        score: f.score
    })) || [];

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-black text-gray-900 dark:text-white tracking-tight">Compliance Center</h1>
                    <p className="text-gray-500 dark:text-gray-400 mt-1 flex items-center gap-2">
                        <Globe className="w-4 h-4" />
                        Active Target: <span className="font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider text-xs">{data?.phase}</span>
                    </p>
                </div>
                <div className="bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm flex items-center gap-4">
                    <div className="text-right">
                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest leading-none">Global Trust Score</p>
                        <p className="text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">{data?.overall_score}%</p>
                    </div>
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                        <ShieldCheck className="w-7 h-7 text-blue-600" />
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Score Overview */}
                <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-6 shadow-sm overflow-hidden relative group">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-lg font-bold flex items-center gap-2">
                            <BarChart className="w-5 h-5 text-blue-500" />
                            Framework Readiness
                        </h2>
                        <div className="text-xs text-blue-600 dark:text-blue-400 font-bold bg-blue-50 dark:bg-blue-900/30 px-3 py-1 rounded-full border border-blue-100 dark:border-blue-800">
                            LIVE AUDIT
                        </div>
                    </div>

                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                <XAxis
                                    dataKey="name"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fontSize: 10, fontWeight: 700, fill: '#6B7280' }}
                                />
                                <YAxis
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fontSize: 10, fontWeight: 700, fill: '#6B7280' }}
                                    domain={[0, 100]}
                                />
                                <Tooltip
                                    cursor={{ fill: 'rgba(59, 130, 246, 0.05)' }}
                                    contentStyle={{
                                        borderRadius: '12px',
                                        border: 'none',
                                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                                        fontSize: '12px',
                                        fontWeight: 'bold'
                                    }}
                                />
                                <Bar dataKey="score" radius={[8, 8, 0, 0]} barSize={40}>
                                    {chartData.map((entry, index) => (
                                        <Cell
                                            key={`cell-${index}`}
                                            fill={entry.score > 90 ? '#10B981' : entry.score > 70 ? '#3B82F6' : '#F59E0B'}
                                            fillOpacity={selectedFramework === index ? 1 : 0.7}
                                        />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Global Strategy */}
                <div className="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-2xl p-6 text-white shadow-lg shadow-blue-500/20 flex flex-col justify-between">
                    <div>
                        <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center mb-6">
                            <Globe className="w-6 h-6" />
                        </div>
                        <h3 className="text-xl font-black tracking-tight mb-2">Expansion Strategy</h3>
                        <p className="text-blue-100 text-sm leading-relaxed mb-6">
                            Our Phase 1 focus is US Small Businesses. We have automatically activated
                            SOC2, CCPA, and HIPAA readiness checkpoints. Global expansion for EU (GDPR)
                            is scheduled for Q3 2026.
                        </p>
                    </div>

                    <div className="space-y-3">
                        <div className="flex items-center justify-between text-xs bg-white/10 p-3 rounded-xl border border-white/10">
                            <span className="font-bold">Phase 1 (US)</span>
                            <span className="bg-green-400 text-green-950 px-2 py-0.5 rounded-full font-black text-[9px] uppercase">Active</span>
                        </div>
                        <div className="flex items-center justify-between text-xs bg-white/5 p-3 rounded-xl opacity-60">
                            <span className="font-bold">Phase 2 (EU/Global)</span>
                            <span className="bg-yellow-400 text-yellow-950 px-2 py-0.5 rounded-full font-black text-[9px] uppercase">Coming Soon</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data?.frameworks.map((framework, idx) => (
                    <div
                        key={framework.name}
                        onClick={() => setSelectedFramework(idx)}
                        className={`cursor-pointer group relative overflow-hidden bg-white dark:bg-gray-800 rounded-2xl border transition-all duration-300 ${selectedFramework === idx
                                ? 'border-blue-500 ring-4 ring-blue-500/10 shadow-lg'
                                : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 shadow-sm'
                            }`}
                    >
                        <div className="p-6">
                            <div className="flex items-center justify-between mb-4">
                                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${framework.status === 'compliant' ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'
                                    }`}>
                                    {framework.name === 'CCPA / CPRA' ? <Fingerprint /> : <FileCheck />}
                                </div>
                                <div className="text-2xl font-black text-gray-900 dark:text-white">{framework.score}%</div>
                            </div>

                            <h3 className="font-bold text-gray-900 dark:text-white mb-1">{framework.name}</h3>
                            <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest">
                                {framework.status === 'compliant' ? 'Audit Passed' : 'Action Required'}
                            </p>

                            <div className="mt-6 space-y-3">
                                {framework.controls.map(control => (
                                    <div key={control.id} className="flex items-center justify-between group/item">
                                        <span className="text-xs text-gray-600 dark:text-gray-400">{control.label}</span>
                                        {control.passed ? (
                                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                                        ) : (
                                            <AlertCircle className="w-4 h-4 text-yellow-500" />
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {selectedFramework === idx && (
                            <div className="absolute bottom-0 left-0 right-0 h-1 bg-blue-500"></div>
                        )}
                    </div>
                ))}

                {/* Placeholder for New Standards */}
                <div className="bg-gray-50/50 dark:bg-gray-800/20 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700 flex flex-col items-center justify-center p-8 text-center group hover:bg-white dark:hover:bg-gray-800 hover:border-blue-500 transition-all cursor-pointer">
                    <div className="w-12 h-12 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-50">
                        <Server className="w-6 h-6 text-gray-400 group-hover:text-blue-500" />
                    </div>
                    <h4 className="font-bold text-gray-900 dark:text-white">Add New Standard</h4>
                    <p className="text-xs text-gray-500 mt-1">PCI-DSS, ISO 27001, etc.</p>
                </div>
            </div>

            {/* Compliance Detailed Logic Box */}
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden shadow-sm">
                <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-900/50 flex items-center justify-between">
                    <h3 className="font-bold text-gray-900 dark:text-white flex items-center gap-2 text-sm">
                        <Lock className="w-4 h-4 text-gray-400" />
                        Platform Security Controls
                    </h3>
                    <span className="text-[10px] bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded font-black text-gray-500">SYSTEM GENERATED</span>
                </div>
                <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    <div className="space-y-1">
                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest">Encryption</p>
                        <p className="text-xs font-bold text-gray-700 dark:text-gray-200">AES-256 for all at-rest data in Vault</p>
                    </div>
                    <div className="space-y-1">
                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest">Authentication</p>
                        <p className="text-xs font-bold text-gray-700 dark:text-gray-200">Clerk Enterprise MFA Enabled</p>
                    </div>
                    <div className="space-y-1">
                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest">Data Residency</p>
                        <p className="text-xs font-bold text-gray-700 dark:text-gray-200">Primary: US-East (Virginia)</p>
                    </div>
                    <div className="space-y-1">
                        <p className="text-[10px] text-gray-400 uppercase font-black tracking-widest">Audit Policy</p>
                        <p className="text-xs font-bold text-gray-700 dark:text-gray-200">365-day Retention Policy</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
