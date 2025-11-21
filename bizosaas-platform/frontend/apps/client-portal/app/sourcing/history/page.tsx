'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui';
import Link from 'next/link';

interface ImportJob {
	id: string;
	created_at: string;
	status: string;
	total_products: number;
	successful: number;
	failed: number;
}

export default function ImportHistory() {
	const [jobs, setJobs] = useState<ImportJob[]>([]);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		fetchImportHistory();
	}, []);

	const fetchImportHistory = async () => {
		try {
			// API call will be implemented when backend is integrated
			const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
			const response = await fetch(`${apiUrl}/api/v1/amazon/import-history`);

			if (response.ok) {
				const data = await response.json();
				setJobs(data.jobs || []);
			}
		} catch (err) {
			console.error('Failed to fetch import history:', err);
		} finally {
			setIsLoading(false);
		}
	};

	const getStatusColor = (status: string) => {
		switch (status) {
			case 'completed':
				return 'text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30';
			case 'processing':
				return 'text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30';
			case 'failed':
				return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30';
			default:
				return 'text-gray-600 dark:text-gray-400 bg-gray-100 dark:bg-gray-800';
		}
	};

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-3xl font-bold text-gray-900 dark:text-white">Import History</h1>
					<p className="text-gray-600 dark:text-gray-400 mt-2">
						View past product imports and their status
					</p>
				</div>
				<Link href="/sourcing">
					<button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors flex items-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							className="h-4 w-4 mr-2"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
						</svg>
						Back to Dashboard
					</button>
				</Link>
			</div>

			{isLoading ? (
				<Card>
					<CardContent className="py-12 text-center">
						<svg
							className="animate-spin h-8 w-8 text-gray-400 mx-auto"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
						>
							<circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
							<path
								className="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							></path>
						</svg>
						<p className="text-gray-600 dark:text-gray-400 mt-4">Loading import history...</p>
					</CardContent>
				</Card>
			) : jobs.length === 0 ? (
				<Card>
					<CardContent className="py-12 text-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							className="h-16 w-16 text-gray-400 mx-auto mb-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth={2}
								d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						<h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
							No Import History
						</h3>
						<p className="text-gray-600 dark:text-gray-400 mb-4">
							You haven't imported any products yet
						</p>
						<Link href="/sourcing/search">
							<button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
								Start Importing Products
							</button>
						</Link>
					</CardContent>
				</Card>
			) : (
				<Card>
					<CardHeader>
						<CardTitle>Recent Imports</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-4">
							{jobs.map((job) => (
								<div
									key={job.id}
									className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
								>
									<div className="flex-1">
										<div className="flex items-center justify-between mb-2">
											<h4 className="font-semibold text-gray-900 dark:text-white">
												Import Job #{job.id}
											</h4>
											<span
												className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
													job.status
												)}`}
											>
												{job.status.charAt(0).toUpperCase() + job.status.slice(1)}
											</span>
										</div>
										<div className="flex items-center text-sm text-gray-600 dark:text-gray-400 space-x-6">
											<span>{new Date(job.created_at).toLocaleDateString()}</span>
											<span>{job.total_products} products</span>
											<span className="text-green-600 dark:text-green-400">
												{job.successful} successful
											</span>
											{job.failed > 0 && (
												<span className="text-red-600 dark:text-red-400">
													{job.failed} failed
												</span>
											)}
										</div>
									</div>
									<button className="ml-4 p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
										<svg
											xmlns="http://www.w3.org/2000/svg"
											className="h-5 w-5 text-gray-600 dark:text-gray-400"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
										>
											<path
												strokeLinecap="round"
												strokeLinejoin="round"
												strokeWidth={2}
												d="M9 5l7 7-7 7"
											/>
										</svg>
									</button>
								</div>
							))}
						</div>
					</CardContent>
				</Card>
			)}
		</div>
	);
}
