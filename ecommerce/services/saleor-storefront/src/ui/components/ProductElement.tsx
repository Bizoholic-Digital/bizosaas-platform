"use client";

import { useState } from "react";
import { LinkWithChannel } from "../atoms/LinkWithChannel";
import { ProductImageWrapper } from "@/ui/atoms/ProductImageWrapper";

import type { ProductListItemFragment } from "@/gql/graphql";
import { formatMoneyRange } from "@/lib/utils";

export function ProductElement({
	product,
	loading,
	priority,
}: { product: ProductListItemFragment } & { loading: "eager" | "lazy"; priority?: boolean }) {
	const [isWishlisted, setIsWishlisted] = useState(false);
	const [isHovered, setIsHovered] = useState(false);

	const handleWishlistToggle = (e: React.MouseEvent) => {
		e.preventDefault();
		e.stopPropagation();
		setIsWishlisted(!isWishlisted);
	};

	const handleQuickView = (e: React.MouseEvent) => {
		e.preventDefault();
		e.stopPropagation();
		// TODO: Implement quick view modal
		console.log("Quick view:", product.name);
	};

	const isOnSale = product?.pricing?.priceRange?.start?.gross?.amount !== product?.pricing?.priceRange?.stop?.gross?.amount;
	const hasVariants = product?.variants?.length > 1;

	return (
		<li data-testid="ProductElement">
			<div 
				className="group relative overflow-hidden rounded-2xl bg-white shadow-sm transition-all duration-300 hover:shadow-xl card-hover"
				onMouseEnter={() => setIsHovered(true)}
				onMouseLeave={() => setIsHovered(false)}
			>
				<LinkWithChannel href={`/products/${product.slug}`} key={product.id}>
					{/* Product Image Container */}
					<div className="relative aspect-square overflow-hidden rounded-t-2xl bg-gray-50">
						{/* Sale Badge */}
						{isOnSale && (
							<div className="absolute left-3 top-3 z-10 rounded-full bg-red-500 px-3 py-1 text-xs font-medium text-white">
								Sale
							</div>
						)}

						{/* New Badge */}
						<div className="absolute right-3 top-3 z-10 rounded-full bg-green-500 px-3 py-1 text-xs font-medium text-white">
							New
						</div>

						{/* Product Image */}
						{product?.thumbnail?.url && (
							<ProductImageWrapper
								loading={loading}
								src={product.thumbnail.url}
								alt={product.thumbnail.alt ?? ""}
								width={512}
								height={512}
								sizes={"512px"}
								priority={priority}
								className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
							/>
						)}

						{/* Wishlist Button */}
						<button
							onClick={handleWishlistToggle}
							className={`absolute right-3 bottom-3 z-10 flex h-10 w-10 items-center justify-center rounded-full backdrop-blur-sm transition-all duration-300 ${
								isWishlisted 
									? 'bg-red-500 text-white' 
									: 'bg-white/80 text-gray-700 hover:bg-red-500 hover:text-white'
							} ${isHovered ? 'translate-y-0 opacity-100' : 'translate-y-2 opacity-0'}`}
						>
							<svg className="h-5 w-5" fill={isWishlisted ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
								<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
							</svg>
						</button>

						{/* Quick Actions Overlay */}
						<div className={`absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/60 to-transparent p-4 transition-all duration-300 ${
							isHovered ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'
						}`}>
							<div className="flex gap-2">
								<button
									onClick={handleQuickView}
									className="flex-1 rounded-lg bg-white/20 px-3 py-2 text-sm font-medium text-white backdrop-blur-sm transition-colors hover:bg-white/30"
								>
									Quick View
								</button>
								<button className="flex-1 rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700">
									Add to Cart
								</button>
							</div>
						</div>
					</div>

					{/* Product Info */}
					<div className="p-4">
						{/* Category */}
						<p className="mb-1 text-xs font-medium text-blue-600 uppercase tracking-wider" data-testid="ProductElement_Category">
							{product.category?.name}
						</p>

						{/* Product Name */}
						<h3 className="mb-2 text-base font-semibold text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors duration-300">
							{product.name}
						</h3>

						{/* Rating (Mock data for now) */}
						<div className="mb-2 flex items-center gap-1">
							<div className="flex">
								{[...Array(5)].map((_, i) => (
									<svg key={i} className="h-4 w-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
										<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
									</svg>
								))}
							</div>
							<span className="text-xs text-gray-500">(4.5)</span>
						</div>

						{/* Price and Variants */}
						<div className="flex items-center justify-between">
							<div>
								<p className="text-lg font-bold text-gray-900" data-testid="ProductElement_PriceRange">
									{formatMoneyRange({
										start: product?.pricing?.priceRange?.start?.gross,
										stop: product?.pricing?.priceRange?.stop?.gross,
									})}
								</p>
								{hasVariants && (
									<p className="text-xs text-gray-500">
										{product?.variants?.length} variants
									</p>
								)}
							</div>

							{/* Stock Status */}
							<div className="flex items-center gap-1">
								<div className="h-2 w-2 rounded-full bg-green-400"></div>
								<span className="text-xs text-gray-600">In Stock</span>
							</div>
						</div>

						{/* Availability Badge */}
						<div className="mt-3 flex items-center justify-between">
							<span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700">
								<svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
									<path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
								</svg>
								Available
							</span>
							
							{/* Free Shipping Badge */}
							<span className="text-xs text-gray-500">
								🚚 Free shipping
							</span>
						</div>
					</div>
				</LinkWithChannel>
			</div>
		</li>
	);
}
