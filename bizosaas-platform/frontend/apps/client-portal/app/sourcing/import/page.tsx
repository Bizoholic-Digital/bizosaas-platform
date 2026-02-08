'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, Textarea, Button } from '@/components/ui';
import Link from 'next/link';

export default function ImportProducts() {
	const [asinList, setAsinList] = useState('');
	const [isImporting, setIsImporting] = useState(false);
	const [results, setResults] = useState<any[]>([]);

	const handleBulkImport = async () => {
		if (!asinList.trim()) {
			return;
		}

		setIsImporting(true);

		try {
			const asins = asinList
				.split('\n')
				.map((line) => line.trim())
				.filter((line) => line.length > 0);

			// API call will be implemented when backend is integrated
			const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
			const response = await fetch(`${apiUrl}/api/v1/amazon/bulk-import`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					asins,
					markup_percentage: 25,
				}),
			});

			if (!response.ok) {
				throw new Error('Import failed');
			}

			const data = await response.json();
			setResults(data.results || []);
			setAsinList('');
		} catch (err) {
			console.error(err);
		} finally {
			setIsImporting(false);
		}
	};

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-3xl font-bold text-gray-900 dark:text-white">Bulk Import Products</h1>
					<p className="text-gray-600 dark:text-gray-400 mt-2">
						Import multiple products using ASIN codes
					</p>
				</div>
				<Link href="/sourcing">
					<Button variant="outline">
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
					</Button>
				</Link>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Input Section */}
				<Card>
					<CardHeader>
						<CardTitle>Enter ASIN Codes</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-4">
							<Textarea
								placeholder="Enter ASIN codes (one per line)&#10;Example:&#10;B08N5WRWNW&#10;B07XJ8C8F5&#10;B09G9FPHY6"
								value={asinList}
								onChange={(e) => setAsinList(e.target.value)}
								rows={12}
								className="font-mono text-sm"
							/>
							<Button
								onClick={handleBulkImport}
								disabled={isImporting || !asinList.trim()}
								className="w-full"
							>
								{isImporting ? (
									<>
										<svg
											className="animate-spin -ml-1 mr-2 h-4 w-4"
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
										Importing...
									</>
								) : (
									<>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											className="h-4 w-4 mr-2"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
										>
											<path
												strokeLinecap="round"
												strokeLinejoin="round"
												strokeWidth={2}
												d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
											/>
										</svg>
										Import Products
									</>
								)}
							</Button>
						</div>
					</CardContent>
				</Card>

				{/* Instructions */}
				<Card>
					<CardHeader>
						<CardTitle>How to Use Bulk Import</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-4">
							<div className="flex items-start">
								<div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mr-3">
									<span className="text-blue-600 dark:text-blue-400 font-semibold">1</span>
								</div>
								<div>
									<h4 className="font-semibold text-gray-900 dark:text-white">Collect ASINs</h4>
									<p className="text-gray-600 dark:text-gray-400 text-sm">
										Gather ASIN codes from Amazon product pages or your supplier list
									</p>
								</div>
							</div>
							<div className="flex items-start">
								<div className="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mr-3">
									<span className="text-green-600 dark:text-green-400 font-semibold">2</span>
								</div>
								<div>
									<h4 className="font-semibold text-gray-900 dark:text-white">Enter One Per Line</h4>
									<p className="text-gray-600 dark:text-gray-400 text-sm">
										Paste ASIN codes in the text box, with one ASIN per line
									</p>
								</div>
							</div>
							<div className="flex items-start">
								<div className="flex-shrink-0 w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mr-3">
									<span className="text-purple-600 dark:text-purple-400 font-semibold">3</span>
								</div>
								<div>
									<h4 className="font-semibold text-gray-900 dark:text-white">Click Import</h4>
									<p className="text-gray-600 dark:text-gray-400 text-sm">
										Products will be automatically imported with your markup applied
									</p>
								</div>
							</div>

							<div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
								<h5 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">Tips</h5>
								<ul className="space-y-1 text-sm text-blue-800 dark:text-blue-400">
									<li>• You can import up to 100 products at once</li>
									<li>• Invalid ASINs will be skipped automatically</li>
									<li>• Import progress will be shown in real-time</li>
									<li>• Check import history for completed imports</li>
								</ul>
							</div>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Results */}
			{results.length > 0 && (
				<Card>
					<CardHeader>
						<CardTitle>Import Results</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-2">
							{results.map((result, index) => (
								<div
									key={index}
									className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
								>
									<div className="flex items-center">
										<span className="text-sm font-mono text-gray-600 dark:text-gray-400 mr-4">
											{result.asin}
										</span>
										<span className="text-sm text-gray-900 dark:text-white">{result.title}</span>
									</div>
									<span
										className={`text-sm font-semibold ${
											result.success
												? 'text-green-600 dark:text-green-400'
												: 'text-red-600 dark:text-red-400'
										}`}
									>
										{result.success ? 'Success' : 'Failed'}
									</span>
								</div>
							))}
						</div>
					</CardContent>
				</Card>
			)}
		</div>
	);
}
