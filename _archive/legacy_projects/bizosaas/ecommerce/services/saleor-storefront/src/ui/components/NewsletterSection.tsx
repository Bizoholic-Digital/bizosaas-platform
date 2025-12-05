"use client";

import { useState } from "react";

export function NewsletterSection() {
	const [email, setEmail] = useState("");
	const [isSubscribed, setIsSubscribed] = useState(false);
	const [isLoading, setIsLoading] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!email) return;

		setIsLoading(true);
		
		// Simulate API call
		await new Promise(resolve => setTimeout(resolve, 1000));
		
		setIsSubscribed(true);
		setIsLoading(false);
		setEmail("");
	};

	const benefits = [
		{
			icon: "🎁",
			title: "Exclusive Offers",
			description: "Get access to subscriber-only deals and early bird discounts"
		},
		{
			icon: "⚡",
			title: "New Arrivals",
			description: "Be the first to know about new products and collections"
		},
		{
			icon: "📱",
			title: "Style Tips",
			description: "Receive expert advice and styling recommendations"
		},
		{
			icon: "🏆",
			title: "VIP Access",
			description: "Priority access to sales and limited edition items"
		}
	];

	return (
		<section className="section-padding bg-gradient-to-br from-slate-900 to-slate-800 text-white">
			<div className="container-custom">
				{/* Main Content */}
				<div className="mx-auto max-w-4xl text-center">
					<div className="mb-8">
						<div className="mb-4 inline-flex items-center rounded-full bg-white/10 px-4 py-2 text-sm font-medium backdrop-blur-sm">
							<span className="mr-2">📧</span>
							Join Our Community
						</div>
						<h2 className="mb-4 text-3xl font-bold md:text-4xl lg:text-5xl">
							Stay in the Loop
						</h2>
						<p className="mx-auto max-w-2xl text-lg text-white/80">
							Subscribe to our newsletter and get 15% off your first order. 
							Plus, be the first to hear about new arrivals, exclusive offers, and insider news.
						</p>
					</div>

					{/* Newsletter Form */}
					{!isSubscribed ? (
						<form onSubmit={handleSubmit} className="mb-12">
							<div className="mx-auto max-w-md">
								<div className="flex flex-col gap-3 sm:flex-row">
									<input
										type="email"
										value={email}
										onChange={(e) => setEmail(e.target.value)}
										placeholder="Enter your email address"
										className="flex-1 rounded-lg bg-white/10 px-4 py-3 text-white placeholder-white/60 backdrop-blur-sm transition-all duration-300 focus:bg-white/20 focus:outline-none focus:ring-2 focus:ring-white/50"
										required
										disabled={isLoading}
									/>
									<button
										type="submit"
										disabled={isLoading}
										className="rounded-lg bg-white px-8 py-3 font-semibold text-slate-900 transition-all duration-300 hover:bg-white/90 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
									>
										{isLoading ? (
											<div className="flex items-center">
												<div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-slate-900 border-t-transparent"></div>
												Subscribing...
											</div>
										) : (
											"Subscribe"
										)}
									</button>
								</div>
								<p className="mt-2 text-sm text-white/60">
									Get 15% off your first order when you subscribe
								</p>
							</div>
						</form>
					) : (
						<div className="mb-12 rounded-lg bg-green-500/20 p-6 text-center backdrop-blur-sm">
							<div className="mb-2 flex justify-center">
								<div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-500">
									<svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
									</svg>
								</div>
							</div>
							<h3 className="mb-2 text-xl font-semibold">Welcome to CoreLDove!</h3>
							<p className="text-white/80">
								Thank you for subscribing. Check your email for your 15% discount code.
							</p>
						</div>
					)}

					{/* Benefits Grid */}
					<div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
						{benefits.map((benefit, index) => (
							<div key={index} className="text-center">
								<div className="mb-4 flex justify-center">
									<div className="flex h-16 w-16 items-center justify-center rounded-full bg-white/10 text-3xl backdrop-blur-sm">
										{benefit.icon}
									</div>
								</div>
								<h3 className="mb-2 text-lg font-semibold">
									{benefit.title}
								</h3>
								<p className="text-sm text-white/70">
									{benefit.description}
								</p>
							</div>
						))}
					</div>
				</div>

				{/* Social Proof */}
				<div className="mt-16 border-t border-white/20 pt-8 text-center">
					<div className="flex flex-wrap items-center justify-center gap-8 opacity-70">
						<div className="flex items-center space-x-2">
							<svg className="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
								<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
							</svg>
							<span className="text-sm">50K+ Happy Subscribers</span>
						</div>
						<div className="flex items-center space-x-2">
							<svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
								<path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" />
							</svg>
							<span className="text-sm">No Spam Guarantee</span>
						</div>
						<div className="flex items-center space-x-2">
							<svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
								<path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" />
							</svg>
							<span className="text-sm">Unsubscribe Anytime</span>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}