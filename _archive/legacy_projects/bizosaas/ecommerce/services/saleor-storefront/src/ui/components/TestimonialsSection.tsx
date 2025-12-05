"use client";

import { useState } from "react";

const testimonials = [
	{
		id: 1,
		name: "Sarah Johnson",
		role: "Verified Customer",
		location: "New York, NY",
		avatar: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23ec4899'/%3E%3Ctext x='50' y='65' text-anchor='middle' fill='white' font-size='40' font-family='Arial'%3ESJ%3C/text%3E%3C/svg%3E",
		content: "Absolutely love CoreLDove! The AI recommendations are spot-on and helped me discover products I never knew I needed. Fast shipping and excellent customer service.",
		rating: 5,
		orderCount: "12+ orders",
		productCategories: ["Electronics", "Fashion"]
	},
	{
		id: 2,
		name: "Michael Chen",
		role: "Premium Member",
		location: "San Francisco, CA",
		avatar: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%233b82f6'/%3E%3Ctext x='50' y='65' text-anchor='middle' fill='white' font-size='40' font-family='Arial'%3EMC%3C/text%3E%3C/svg%3E",
		content: "The checkout process is incredibly smooth, and the product quality exceeds expectations every time. CoreLDove has become my go-to for all online shopping needs.",
		rating: 5,
		orderCount: "25+ orders",
		productCategories: ["Home & Garden", "Sports"]
	},
	{
		id: 3,
		name: "Emily Rodriguez",
		role: "Verified Customer",
		location: "Austin, TX",
		avatar: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%2310b981'/%3E%3Ctext x='50' y='65' text-anchor='middle' fill='white' font-size='40' font-family='Arial'%3EER%3C/text%3E%3C/svg%3E",
		content: "Outstanding customer support! I had an issue with one order and they resolved it within hours. The return process is hassle-free, which gives me confidence to shop more.",
		rating: 5,
		orderCount: "8+ orders",
		productCategories: ["Beauty", "Books"]
	},
	{
		id: 4,
		name: "David Kim",
		role: "Business Customer",
		location: "Seattle, WA",
		avatar: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23f59e0b'/%3E%3Ctext x='50' y='65' text-anchor='middle' fill='white' font-size='40' font-family='Arial'%3EDK%3C/text%3E%3C/svg%3E",
		content: "We use CoreLDove for our office supplies and employee gifts. The bulk ordering system is efficient, and the business account features save us time and money.",
		rating: 5,
		orderCount: "50+ orders",
		productCategories: ["Electronics", "Office Supplies"]
	}
];

export function TestimonialsSection() {
	const [activeTestimonial, setActiveTestimonial] = useState(0);

	const renderStars = (rating: number) => {
		return Array.from({ length: 5 }, (_, i) => (
			<svg
				key={i}
				className={`h-5 w-5 ${i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
				viewBox="0 0 20 20"
			>
				<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
			</svg>
		));
	};

	return (
		<section className="section-padding bg-white">
			<div className="container-custom">
				{/* Section Header */}
				<div className="mb-16 text-center">
					<h2 className="mb-4 text-3xl font-bold text-gray-900 md:text-4xl lg:text-5xl">
						What Our Customers Say
					</h2>
					<p className="mx-auto max-w-2xl text-lg text-gray-600">
						Join thousands of satisfied customers who trust CoreLDove for their shopping needs.
						Read real reviews from real customers.
					</p>
				</div>

				{/* Main Testimonial Display */}
				<div className="mb-12 rounded-3xl bg-gradient-to-br from-slate-50 to-gray-50 p-8 shadow-xl md:p-12">
					<div className="mx-auto max-w-4xl">
						{/* Quote Icon */}
						<div className="mb-6 flex justify-center">
							<div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-100">
								<svg className="h-8 w-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
									<path fillRule="evenodd" d="M3 17V7c0-1.1.9-2 2-2h2a1 1 0 010 2H5v8a2 2 0 002 2h6a2 2 0 002-2v-2a1 1 0 112 0v2c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2z" />
								</svg>
							</div>
						</div>

						{/* Testimonial Content */}
						<div className="text-center">
							<blockquote className="mb-8 text-xl font-medium text-gray-900 md:text-2xl">
								"{testimonials[activeTestimonial].content}"
							</blockquote>

							{/* Rating */}
							<div className="mb-6 flex justify-center">
								{renderStars(testimonials[activeTestimonial].rating)}
							</div>

							{/* Customer Info */}
							<div className="flex items-center justify-center">
								<img
									src={testimonials[activeTestimonial].avatar}
									alt={testimonials[activeTestimonial].name}
									className="h-16 w-16 rounded-full mr-4"
								/>
								<div className="text-left">
									<h4 className="text-lg font-semibold text-gray-900">
										{testimonials[activeTestimonial].name}
									</h4>
									<p className="text-sm text-gray-600">
										{testimonials[activeTestimonial].role} • {testimonials[activeTestimonial].location}
									</p>
									<p className="text-sm text-blue-600">
										{testimonials[activeTestimonial].orderCount} • {testimonials[activeTestimonial].productCategories.join(", ")}
									</p>
								</div>
							</div>
						</div>
					</div>
				</div>

				{/* Testimonial Navigation */}
				<div className="flex justify-center space-x-4">
					{testimonials.map((testimonial, index) => (
						<button
							key={testimonial.id}
							onClick={() => setActiveTestimonial(index)}
							className={`group relative flex items-center rounded-xl p-4 transition-all duration-300 ${
								index === activeTestimonial
									? 'bg-blue-100 shadow-lg'
									: 'bg-gray-50 hover:bg-gray-100'
							}`}
						>
							<img
								src={testimonial.avatar}
								alt={testimonial.name}
								className="h-12 w-12 rounded-full mr-3"
							/>
							<div className="text-left">
								<h5 className={`text-sm font-medium ${
									index === activeTestimonial ? 'text-blue-900' : 'text-gray-900'
								}`}>
									{testimonial.name}
								</h5>
								<p className="text-xs text-gray-600">
									{testimonial.location}
								</p>
							</div>

							{/* Active Indicator */}
							{index === activeTestimonial && (
								<div className="absolute -bottom-2 left-1/2 h-1 w-8 -translate-x-1/2 rounded-full bg-blue-600" />
							)}
						</button>
					))}
				</div>

				{/* Trust Badges */}
				<div className="mt-16 flex flex-wrap items-center justify-center gap-8 opacity-60">
					<div className="flex items-center space-x-2">
						<svg className="h-6 w-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
							<path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
						</svg>
						<span className="text-sm font-medium text-gray-700">SSL Secured</span>
					</div>
					<div className="flex items-center space-x-2">
						<svg className="h-6 w-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
							<path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
						<span className="text-sm font-medium text-gray-700">Verified Reviews</span>
					</div>
					<div className="flex items-center space-x-2">
						<svg className="h-6 w-6 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
							<path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
						</svg>
						<span className="text-sm font-medium text-gray-700">Premium Quality</span>
					</div>
					<div className="flex items-center space-x-2">
						<svg className="h-6 w-6 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
							<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
						</svg>
						<span className="text-sm font-medium text-gray-700">4.9/5 Rating</span>
					</div>
				</div>
			</div>
		</section>
	);
}