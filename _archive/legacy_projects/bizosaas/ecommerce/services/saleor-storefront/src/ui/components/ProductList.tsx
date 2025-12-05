import { ProductElement } from "./ProductElement";
import { type ProductListItemFragment } from "@/gql/graphql";

interface ProductListProps {
	products: readonly ProductListItemFragment[];
	title?: string;
	description?: string;
	showHeader?: boolean;
}

export const ProductList = ({ 
	products, 
	title = "Featured Products",
	description = "Discover our carefully curated selection of premium products",
	showHeader = true 
}: ProductListProps) => {
	if (!products?.length) {
		return (
			<section className="section-padding bg-white">
				<div className="container-custom text-center">
					<div className="mx-auto max-w-md">
						<div className="mb-4 flex justify-center">
							<div className="flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
								<svg className="h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4-8-4m16 0v10l-8 4-8-4V7" />
								</svg>
							</div>
						</div>
						<h3 className="mb-2 text-lg font-semibold text-gray-900">No Products Found</h3>
						<p className="text-gray-600">Check back later for new arrivals.</p>
					</div>
				</div>
			</section>
		);
	}

	return (
		<section className="section-padding bg-white">
			<div className="container-custom">
				{/* Section Header */}
				{showHeader && (
					<div className="mb-12 text-center">
						<h2 className="mb-4 text-3xl font-bold text-gray-900 md:text-4xl">
							{title}
						</h2>
						{description && (
							<p className="mx-auto max-w-2xl text-lg text-gray-600">
								{description}
							</p>
						)}
					</div>
				)}

				{/* Products Grid */}
				<ul
					role="list"
					data-testid="ProductList"
					className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
				>
					{products.map((product, index) => (
						<ProductElement
							key={product.id}
							product={product}
							priority={index < 4}
							loading={index < 8 ? "eager" : "lazy"}
						/>
					))}
				</ul>

				{/* Load More Section */}
				{products.length >= 12 && (
					<div className="mt-12 text-center">
						<button className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:from-blue-700 hover:to-blue-800 hover:scale-105 hover:shadow-xl">
							Load More Products
							<svg className="ml-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
							</svg>
						</button>
					</div>
				)}
			</div>
		</section>
	);
};
