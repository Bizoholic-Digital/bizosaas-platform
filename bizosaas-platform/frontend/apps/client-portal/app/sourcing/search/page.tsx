'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, Input, Button } from '@/components/ui';
import Link from 'next/link';

interface Product {
	asin: string;
	title: string;
	price: string;
	image_url: string;
	rating: number;
	review_count: number;
}

export default function SearchProducts() {
	const [searchQuery, setSearchQuery] = useState('');
	const [isSearching, setIsSearching] = useState(false);
	const [results, setResults] = useState<Product[]>([]);
	const [error, setError] = useState('');

	const handleSearch = async () => {
		if (!searchQuery.trim()) {
			setError('Please enter a search query');
			return;
		}

		setIsSearching(true);
		setError('');

		try {
			// API call will be implemented when backend is integrated
			const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
			const response = await fetch(`${apiUrl}/api/v1/amazon/search`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					query: searchQuery,
					limit: 20,
				}),
			});

			if (!response.ok) {
				throw new Error('Search failed');
			}

			const data = await response.json();
			setResults(data.products || []);
		} catch (err) {
			setError('Failed to search products. Please try again.');
			console.error(err);
		} finally {
			setIsSearching(false);
		}
	};

	const handleImport = async (asin: string) => {
		// TODO: Implement import functionality
		console.log('Importing product:', asin);
	};

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-3xl font-bold text-gray-900 dark:text-white">Search Amazon Products</h1>
					<p className="text-gray-600 dark:text-gray-400 mt-2">
						Find products to import to your store
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

			{/* Search Box */}
			<Card>
				<CardHeader>
					<CardTitle>Search Amazon Catalog</CardTitle>
				</CardHeader>
				<CardContent>
					<div className="flex gap-4">
						<div className="flex-1">
							<Input
								type="text"
								placeholder="Enter product name, keyword, or ASIN..."
								value={searchQuery}
								onChange={(e) => setSearchQuery(e.target.value)}
								onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
								className="w-full"
							/>
						</div>
						<Button onClick={handleSearch} disabled={isSearching} className="px-8">
							{isSearching ? (
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
									Searching...
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
										<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
									</svg>
									Search
								</>
							)}
						</Button>
					</div>
					{error && (
						<p className="text-red-600 dark:text-red-400 text-sm mt-2">{error}</p>
					)}
				</CardContent>
			</Card>

			{/* Results */}
			{results.length > 0 && (
				<div>
					<h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
						Search Results ({results.length})
					</h2>
					<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
						{results.map((product) => (
							<Card key={product.asin} className="hover:shadow-lg transition-shadow">
								<CardContent className="p-4">
									<div className="aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
										{product.image_url ? (
											<img
												src={product.image_url}
												alt={product.title}
												className="w-full h-full object-cover"
											/>
										) : (
											<svg
												xmlns="http://www.w3.org/2000/svg"
												className="h-20 w-20 text-gray-400"
												fill="none"
												viewBox="0 0 24 24"
												stroke="currentColor"
											>
												<path
													strokeLinecap="round"
													strokeLinejoin="round"
													strokeWidth={2}
													d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
												/>
											</svg>
										)}
									</div>
									<h3 className="font-semibold text-gray-900 dark:text-white text-sm mb-2 line-clamp-2">
										{product.title}
									</h3>
									<div className="flex items-center justify-between mb-3">
										<span className="text-lg font-bold text-gray-900 dark:text-white">
											{product.price}
										</span>
										{product.rating && (
											<div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													className="h-4 w-4 text-yellow-400 mr-1"
													viewBox="0 0 20 20"
													fill="currentColor"
												>
													<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
												</svg>
												{product.rating} ({product.review_count})
											</div>
										)}
									</div>
									<p className="text-xs text-gray-500 dark:text-gray-400 mb-3">ASIN: {product.asin}</p>
									<Button
										onClick={() => handleImport(product.asin)}
										className="w-full"
										size="sm"
									>
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
										Import Product
									</Button>
								</CardContent>
							</Card>
						))}
					</div>
				</div>
			)}

			{/* Empty State */}
			{results.length === 0 && !isSearching && (
				<Card>
					<CardContent className="py-12 text-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							className="h-16 w-16 text-gray-400 mx-auto mb-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
						</svg>
						<h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
							Start Searching for Products
						</h3>
						<p className="text-gray-600 dark:text-gray-400">
							Enter a product name, keyword, or ASIN in the search box above
						</p>
					</CardContent>
				</Card>
			)}
		</div>
	);
}
