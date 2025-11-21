import { LinkWithChannel } from "../atoms/LinkWithChannel";

const categories = [
	{
		name: "Electronics",
		description: "Latest gadgets and tech accessories",
		image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='electronics' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%236366f1;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%233b82f6;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23electronics)'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='white' font-size='40'%3E📱%3C/text%3E%3C/svg%3E",
		slug: "electronics",
		productCount: "150+"
	},
	{
		name: "Fashion",
		description: "Trendy clothing and accessories",
		image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='fashion' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23ec4899;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23f43f5e;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23fashion)'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='white' font-size='40'%3E👕%3C/text%3E%3C/svg%3E",
		slug: "fashion",
		productCount: "300+"
	},
	{
		name: "Home & Garden",
		description: "Furniture and home decor items",
		image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='home' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%2310b981;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%2306b6d4;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23home)'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='white' font-size='40'%3E🏠%3C/text%3E%3C/svg%3E",
		slug: "home-garden",
		productCount: "200+"
	},
	{
		name: "Sports & Fitness",
		description: "Equipment for active lifestyle",
		image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='sports' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23f59e0b;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23ef4444;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23sports)'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='white' font-size='40'%3E⚽%3C/text%3E%3C/svg%3E",
		slug: "sports",
		productCount: "120+"
	},
	{
		name: "Books & Media",
		description: "Books, music, and entertainment",
		image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='books' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%238b5cf6;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%236366f1;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23books)'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='white' font-size='40'%3E📚%3C/text%3E%3C/svg%3E",
		slug: "books",
		productCount: "500+"
	},
	{
		name: "Beauty & Health",
		description: "Skincare and wellness products",
		image: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'%3E%3Cdefs%3E%3ClinearGradient id='beauty' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23ec4899;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23a855f7;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='400' height='300' fill='url(%23beauty)'/%3E%3Ctext x='200' y='150' text-anchor='middle' fill='white' font-size='40'%3E💄%3C/text%3E%3C/svg%3E",
		slug: "beauty",
		productCount: "180+"
	}
];

export function CategoryShowcase({ channel }: { channel: string }) {
	return (
		<section className="section-padding bg-gray-50">
			<div className="container-custom">
				{/* Section Header */}
				<div className="mb-16 text-center">
					<h2 className="mb-4 text-3xl font-bold text-gray-900 md:text-4xl lg:text-5xl">
						Shop by Category
					</h2>
					<p className="mx-auto max-w-2xl text-lg text-gray-600">
						Discover our wide range of products across different categories, 
						each carefully curated for quality and style.
					</p>
				</div>

				{/* Categories Grid */}
				<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
					{categories.map((category, index) => (
						<LinkWithChannel
							key={category.slug}
							href={`/categories/${category.slug}`}
							className="group relative overflow-hidden rounded-2xl bg-white shadow-md transition-all duration-300 hover:shadow-2xl card-hover"
						>
							{/* Image Container */}
							<div className="relative h-48 overflow-hidden">
								<img
									src={category.image}
									alt={category.name}
									className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
								/>
								
								{/* Overlay */}
								<div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
								
								{/* Product Count Badge */}
								<div className="absolute right-4 top-4">
									<span className="rounded-full bg-white/20 px-3 py-1 text-sm font-medium text-white backdrop-blur-sm">
										{category.productCount} Products
									</span>
								</div>
							</div>

							{/* Content */}
							<div className="relative p-6">
								<h3 className="mb-2 text-xl font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-300">
									{category.name}
								</h3>
								<p className="text-gray-600">
									{category.description}
								</p>

								{/* Arrow Icon */}
								<div className="mt-4 flex items-center text-blue-600">
									<span className="text-sm font-medium">Explore Category</span>
									<svg 
										className="ml-2 h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" 
										fill="none" 
										stroke="currentColor" 
										viewBox="0 0 24 24"
									>
										<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
									</svg>
								</div>
							</div>

							{/* Hover Effect Border */}
							<div className="absolute inset-0 rounded-2xl border-2 border-transparent transition-colors duration-300 group-hover:border-blue-200" />
						</LinkWithChannel>
					))}
				</div>

				{/* View All Categories CTA */}
				<div className="mt-16 text-center">
					<LinkWithChannel
						href="/categories"
						className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:from-blue-700 hover:to-blue-800 hover:scale-105 hover:shadow-xl"
					>
						View All Categories
						<svg className="ml-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
						</svg>
					</LinkWithChannel>
				</div>
			</div>
		</section>
	);
}