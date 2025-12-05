import Link from "next/link";
import Image from "next/image";
import { LinkWithChannel } from "../atoms/LinkWithChannel";
import { ChannelSelect } from "./ChannelSelect";
import { ChannelsListDocument, MenuGetBySlugDocument } from "@/gql/graphql";
import { executeGraphQL } from "@/lib/graphql";

export async function Footer({ channel }: { channel: string }) {
	const footerLinks = await executeGraphQL(MenuGetBySlugDocument, {
		variables: { slug: "footer", channel },
		revalidate: 60 * 60 * 24,
	});
	const channels = process.env.SALEOR_APP_TOKEN
		? await executeGraphQL(ChannelsListDocument, {
				withAuth: false, // disable cookie-based auth for this call
				headers: {
					// and use app token instead
					Authorization: `Bearer ${process.env.SALEOR_APP_TOKEN}`,
				},
		  })
		: null;
	const currentYear = new Date().getFullYear();

	return (
		<footer className="bg-slate-900 text-white">
			<div className="container-custom">
				{/* Main Footer Content */}
				<div className="grid grid-cols-1 gap-8 py-16 md:grid-cols-2 lg:grid-cols-4">
					{/* Company Info */}
					<div className="lg:col-span-2">
						<div className="mb-6">
							<h2 className="text-2xl font-bold">CoreLDove</h2>
							<p className="mt-2 text-slate-300">Premium E-commerce Platform</p>
						</div>
						<p className="mb-6 text-slate-400 leading-relaxed">
							Experience the future of online shopping with our AI-powered e-commerce platform. 
							We offer premium products, exceptional service, and innovative technology to deliver 
							an unmatched shopping experience.
						</p>
						
						{/* Contact Info */}
						<div className="space-y-3">
							<div className="flex items-center gap-3">
								<svg className="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
								</svg>
								<span className="text-slate-300">123 Commerce Street, Tech City, TC 12345</span>
							</div>
							<div className="flex items-center gap-3">
								<svg className="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
								</svg>
								<span className="text-slate-300">+1 (555) 123-4567</span>
							</div>
							<div className="flex items-center gap-3">
								<svg className="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
								</svg>
								<span className="text-slate-300">support@coreldove.com</span>
							</div>
						</div>
					</div>

					{/* Quick Links */}
					<div>
						<h3 className="mb-6 text-lg font-semibold">Quick Links</h3>
						<ul className="space-y-3">
							<li><LinkWithChannel href="/products" className="text-slate-400 hover:text-white transition-colors">All Products</LinkWithChannel></li>
							<li><LinkWithChannel href="/categories" className="text-slate-400 hover:text-white transition-colors">Categories</LinkWithChannel></li>
							<li><LinkWithChannel href="/collections" className="text-slate-400 hover:text-white transition-colors">Collections</LinkWithChannel></li>
							<li><LinkWithChannel href="/search" className="text-slate-400 hover:text-white transition-colors">Search</LinkWithChannel></li>
							<li><LinkWithChannel href="/account" className="text-slate-400 hover:text-white transition-colors">My Account</LinkWithChannel></li>
							<li><LinkWithChannel href="/cart" className="text-slate-400 hover:text-white transition-colors">Shopping Cart</LinkWithChannel></li>
						</ul>
					</div>

					{/* Customer Service */}
					<div>
						<h3 className="mb-6 text-lg font-semibold">Customer Service</h3>
						<ul className="space-y-3">
							<li><LinkWithChannel href="/help" className="text-slate-400 hover:text-white transition-colors">Help Center</LinkWithChannel></li>
							<li><LinkWithChannel href="/contact" className="text-slate-400 hover:text-white transition-colors">Contact Us</LinkWithChannel></li>
							<li><LinkWithChannel href="/shipping" className="text-slate-400 hover:text-white transition-colors">Shipping Info</LinkWithChannel></li>
							<li><LinkWithChannel href="/returns" className="text-slate-400 hover:text-white transition-colors">Returns & Exchanges</LinkWithChannel></li>
							<li><LinkWithChannel href="/size-guide" className="text-slate-400 hover:text-white transition-colors">Size Guide</LinkWithChannel></li>
							<li><LinkWithChannel href="/track-order" className="text-slate-400 hover:text-white transition-colors">Track Your Order</LinkWithChannel></li>
						</ul>
					</div>

					{/* Dynamic Menu Items */}
					{footerLinks.menu?.items?.map((item) => {
						return (
							<div key={item.id} className="lg:col-span-1">
								<h3 className="mb-6 text-lg font-semibold">{item.name}</h3>
								<ul className="space-y-3">
									{item.children?.map((child) => {
										if (child.category) {
											return (
												<li key={child.id}>
													<LinkWithChannel href={`/categories/${child.category.slug}`} className="text-slate-400 hover:text-white transition-colors">
														{child.category.name}
													</LinkWithChannel>
												</li>
											);
										}
										if (child.collection) {
											return (
												<li key={child.id}>
													<LinkWithChannel href={`/collections/${child.collection.slug}`} className="text-slate-400 hover:text-white transition-colors">
														{child.collection.name}
													</LinkWithChannel>
												</li>
											);
										}
										if (child.page) {
											return (
												<li key={child.id}>
													<LinkWithChannel href={`/pages/${child.page.slug}`} className="text-slate-400 hover:text-white transition-colors">
														{child.page.title}
													</LinkWithChannel>
												</li>
											);
										}
										if (child.url) {
											return (
												<li key={child.id}>
													<LinkWithChannel href={child.url} className="text-slate-400 hover:text-white transition-colors">{child.name}</LinkWithChannel>
												</li>
											);
										}
										return null;
									})}
								</ul>
							</div>
						);
					})}
				</div>

				{/* Newsletter and Social */}
				<div className="border-t border-slate-800 py-8">
					<div className="grid grid-cols-1 gap-8 md:grid-cols-2">
						{/* Social Media */}
						<div>
							<h4 className="mb-4 text-lg font-semibold">Follow Us</h4>
							<div className="flex space-x-4">
								<button className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white transition-colors hover:bg-blue-700">
									<svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
										<path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
									</svg>
								</button>
								<button className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-800 text-white transition-colors hover:bg-blue-900">
									<svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
										<path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
									</svg>
								</button>
								<button className="flex h-10 w-10 items-center justify-center rounded-full bg-pink-600 text-white transition-colors hover:bg-pink-700">
									<svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
										<path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.099.12.112.225.085.346-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.752-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001 12.017.001z"/>
									</svg>
								</button>
								<button className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white transition-all hover:scale-105">
									<svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
										<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
									</svg>
								</button>
							</div>
						</div>

						{/* Trust Badges */}
						<div>
							<h4 className="mb-4 text-lg font-semibold">Security & Trust</h4>
							<div className="flex flex-wrap gap-4">
								<div className="flex items-center gap-2 rounded-lg bg-slate-800 px-3 py-2">
									<svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
										<path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
									</svg>
									<span className="text-sm">SSL Secured</span>
								</div>
								<div className="flex items-center gap-2 rounded-lg bg-slate-800 px-3 py-2">
									<svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
										<path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
										<path fillRule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" />
									</svg>
									<span className="text-sm">Secure Payment</span>
								</div>
								<div className="flex items-center gap-2 rounded-lg bg-slate-800 px-3 py-2">
									<svg className="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
										<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.719c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
									</svg>
									<span className="text-sm">5-Star Rated</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				{/* Channel Select */}
				{channels?.channels && (
					<div className="border-t border-slate-800 py-6">
						<div className="flex items-center gap-4 text-slate-400">
							<span className="text-sm">Change currency:</span> 
							<ChannelSelect channels={channels.channels} />
						</div>
					</div>
				)}

				{/* Bottom Bar */}
				<div className="flex flex-col justify-between border-t border-slate-800 py-8 sm:flex-row sm:items-center">
					<div className="mb-4 sm:mb-0">
						<p className="text-sm text-slate-400">
							Copyright &copy; {currentYear} CoreLDove, Inc. All rights reserved.
						</p>
						<div className="mt-2 flex space-x-6 text-sm text-slate-400">
							<LinkWithChannel href="/privacy" className="hover:text-white">Privacy Policy</LinkWithChannel>
							<LinkWithChannel href="/terms" className="hover:text-white">Terms of Service</LinkWithChannel>
							<LinkWithChannel href="/cookies" className="hover:text-white">Cookie Policy</LinkWithChannel>
						</div>
					</div>
					<div className="flex items-center gap-2 text-sm text-slate-400">
						<span>Powered by</span>
						<Link target="_blank" href="https://saleor.io/" className="hover:text-white">
							Saleor
						</Link>
						<Link href="https://github.com/saleor/saleor" target="_blank" className="opacity-50 hover:opacity-100">
							<Image alt="Saleor github repository" height={16} width={16} src="/github-mark.svg" />
						</Link>
					</div>
				</div>
			</div>
		</footer>
	);
}
