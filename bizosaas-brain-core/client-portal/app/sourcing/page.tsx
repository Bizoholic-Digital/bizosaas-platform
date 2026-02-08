'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui';
import Link from 'next/link';

export default function SourcingDashboard() {
	const [stats] = useState({
		totalProducts: 0,
		searchesThisMonth: 0,
		importsThisMonth: 0,
		monthlyLimit: 100,
	});

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-3xl font-bold text-gray-900 dark:text-white">Amazon Product Sourcing</h1>
					<p className="text-gray-600 dark:text-gray-400 mt-2">
						Search and import products from Amazon to your store
					</p>
				</div>
			</div>

			{/* Stats Grid */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				<Card>
					<CardHeader>
						<CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
							Total Products
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.totalProducts}</div>
					</CardContent>
				</Card>

				<Card>
					<CardHeader>
						<CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
							Searches This Month
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.searchesThisMonth}</div>
					</CardContent>
				</Card>

				<Card>
					<CardHeader>
						<CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
							Imports This Month
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="text-2xl font-bold text-gray-900 dark:text-white">
							{stats.importsThisMonth} / {stats.monthlyLimit}
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardHeader>
						<CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
							Monthly Limit
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="text-2xl font-bold text-gray-900 dark:text-white">{stats.monthlyLimit}</div>
						<p className="text-xs text-gray-500 mt-1">Starter Plan</p>
					</CardContent>
				</Card>
			</div>

			{/* Quick Actions */}
			<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
				<Link href="/sourcing/search">
					<Card className="hover:shadow-lg transition-shadow cursor-pointer">
						<CardHeader>
							<div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-4">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									className="h-6 w-6 text-blue-600 dark:text-blue-400"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										strokeLinecap="round"
										strokeLinejoin="round"
										strokeWidth={2}
										d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
									/>
								</svg>
							</div>
							<CardTitle>Search Products</CardTitle>
							<CardDescription>Search Amazon catalog for products to import</CardDescription>
						</CardHeader>
					</Card>
				</Link>

				<Link href="/sourcing/import">
					<Card className="hover:shadow-lg transition-shadow cursor-pointer">
						<CardHeader>
							<div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-4">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									className="h-6 w-6 text-green-600 dark:text-green-400"
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
							</div>
							<CardTitle>Import Products</CardTitle>
							<CardDescription>Bulk import products using ASIN codes</CardDescription>
						</CardHeader>
					</Card>
				</Link>

				<Link href="/sourcing/history">
					<Card className="hover:shadow-lg transition-shadow cursor-pointer">
						<CardHeader>
							<div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-4">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									className="h-6 w-6 text-purple-600 dark:text-purple-400"
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
							</div>
							<CardTitle>Import History</CardTitle>
							<CardDescription>View past imports and their status</CardDescription>
						</CardHeader>
					</Card>
				</Link>
			</div>

			{/* Getting Started Guide */}
			<Card>
				<CardHeader>
					<CardTitle>Getting Started with Amazon Sourcing</CardTitle>
					<CardDescription>Quick guide to importing products from Amazon</CardDescription>
				</CardHeader>
				<CardContent>
					<div className="space-y-4">
						<div className="flex items-start">
							<div className="flex-shrink-0 w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mr-4">
								<span className="text-blue-600 dark:text-blue-400 font-semibold">1</span>
							</div>
							<div>
								<h4 className="font-semibold text-gray-900 dark:text-white">Search for Products</h4>
								<p className="text-gray-600 dark:text-gray-400 text-sm">
									Use the search feature to find products by keyword or browse Amazon categories
								</p>
							</div>
						</div>
						<div className="flex items-start">
							<div className="flex-shrink-0 w-8 h-8 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mr-4">
								<span className="text-green-600 dark:text-green-400 font-semibold">2</span>
							</div>
							<div>
								<h4 className="font-semibold text-gray-900 dark:text-white">Review Product Details</h4>
								<p className="text-gray-600 dark:text-gray-400 text-sm">
									Check product information, pricing, and images before importing
								</p>
							</div>
						</div>
						<div className="flex items-start">
							<div className="flex-shrink-0 w-8 h-8 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mr-4">
								<span className="text-purple-600 dark:text-purple-400 font-semibold">3</span>
							</div>
							<div>
								<h4 className="font-semibold text-gray-900 dark:text-white">Import to Your Store</h4>
								<p className="text-gray-600 dark:text-gray-400 text-sm">
									One-click import with automatic pricing and inventory sync
								</p>
							</div>
						</div>
					</div>
				</CardContent>
			</Card>
		</div>
	);
}
