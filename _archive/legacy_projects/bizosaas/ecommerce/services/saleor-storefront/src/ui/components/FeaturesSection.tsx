import { LinkWithChannel } from "../atoms/LinkWithChannel";

const features = [
	{
		icon: "🚚",
		title: "Free Shipping",
		description: "Free shipping on orders over $75. Fast and reliable delivery worldwide.",
		color: "from-blue-50 to-blue-100"
	},
	{
		icon: "🔒",
		title: "Secure Payment",
		description: "256-bit SSL encryption ensures your payment information is always secure.",
		color: "from-green-50 to-green-100"
	},
	{
		icon: "↩️",
		title: "Easy Returns",
		description: "30-day return policy with free return shipping on all orders.",
		color: "from-purple-50 to-purple-100"
	},
	{
		icon: "💬",
		title: "24/7 Support",
		description: "Round-the-clock customer support via chat, email, or phone.",
		color: "from-orange-50 to-orange-100"
	},
	{
		icon: "🎯",
		title: "AI Recommendations",
		description: "Smart product suggestions powered by advanced AI algorithms.",
		color: "from-pink-50 to-pink-100"
	},
	{
		icon: "⚡",
		title: "Fast Checkout",
		description: "Lightning-fast checkout process with multiple payment options.",
		color: "from-indigo-50 to-indigo-100"
	}
];

export function FeaturesSection() {
	return (
		<section className="section-padding bg-white">
			<div className="container-custom">
				{/* Section Header */}
				<div className="mb-16 text-center">
					<h2 className="mb-4 text-3xl font-bold text-gray-900 md:text-4xl lg:text-5xl">
						Why Choose CoreLDove?
					</h2>
					<p className="mx-auto max-w-2xl text-lg text-gray-600">
						We're committed to providing an exceptional shopping experience with premium features 
						and world-class customer service.
					</p>
				</div>

				{/* Features Grid */}
				<div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
					{features.map((feature, index) => (
						<div
							key={index}
							className={`group relative rounded-2xl bg-gradient-to-br ${feature.color} p-8 transition-all duration-300 hover:scale-105 hover:shadow-xl`}
						>
							{/* Icon */}
							<div className="mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-white text-3xl shadow-lg">
								{feature.icon}
							</div>

							{/* Content */}
							<h3 className="mb-3 text-xl font-semibold text-gray-900">
								{feature.title}
							</h3>
							<p className="text-gray-700">
								{feature.description}
							</p>

							{/* Hover Effect */}
							<div className="absolute inset-0 rounded-2xl bg-white/20 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
						</div>
					))}
				</div>

				{/* Call to Action */}
				<div className="mt-16 text-center">
					<div className="inline-flex flex-col items-center gap-6 rounded-2xl bg-gradient-to-r from-slate-50 to-gray-50 p-8 shadow-lg md:flex-row md:gap-8">
						<div className="flex-1 text-left">
							<h3 className="mb-2 text-2xl font-bold text-gray-900">
								Ready to Experience Premium E-commerce?
							</h3>
							<p className="text-gray-600">
								Join thousands of satisfied customers who trust CoreLDove for their shopping needs.
							</p>
						</div>
						<div className="flex flex-col gap-3 sm:flex-row">
							<LinkWithChannel
								href="/products"
								className="inline-flex items-center justify-center rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-3 text-white transition-all duration-300 hover:from-blue-700 hover:to-blue-800 hover:shadow-lg"
							>
								Browse Products
								<svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
								</svg>
							</LinkWithChannel>
							<LinkWithChannel
								href="/categories"
								className="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-6 py-3 text-gray-700 transition-all duration-300 hover:bg-gray-50 hover:shadow-md"
							>
								View Categories
							</LinkWithChannel>
						</div>
					</div>
				</div>
			</div>
		</section>
	);
}