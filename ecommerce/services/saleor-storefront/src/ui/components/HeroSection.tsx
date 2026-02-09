"use client";

import { useState, useEffect } from "react";
import { LinkWithChannel } from "../atoms/LinkWithChannel";

const heroSlides = [
	{
		id: 1,
		title: "Premium E-commerce Solutions",
		subtitle: "Discover the Future of Online Shopping",
		description: "Experience next-generation e-commerce with AI-powered recommendations, seamless checkout, and premium customer service.",
		ctaText: "Shop Now",
		ctaLink: "/categories",
		bgImage: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 600'%3E%3Cdefs%3E%3ClinearGradient id='grad1' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23007766;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23e56404;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='1200' height='600' fill='url(%23grad1)'/%3E%3C/svg%3E"
	},
	{
		id: 2,
		title: "Innovative Product Catalog",
		subtitle: "Curated Collections for Modern Living",
		description: "Browse our carefully curated selection of premium products designed for the modern lifestyle.",
		ctaText: "Explore Collection",
		ctaLink: "/collections",
		bgImage: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 600'%3E%3Cdefs%3E%3ClinearGradient id='grad2' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23e56404;stop-opacity:1' /%3E%3Cstop offset='100%25' style='stop-color:%23007766;stop-opacity:1' /%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='1200' height='600' fill='url(%23grad2)'/%3E%3C/svg%3E"
	},
	{
		id: 3,
		title: "Smart AI Recommendations",
		subtitle: "Personalized Shopping Experience",
		description: "Let our AI-powered system recommend products tailored specifically to your preferences and needs.",
		ctaText: "Discover More",
		ctaLink: "/products",
		bgImage: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 600'%3E%3Cdefs%3E%3CradialGradient id='grad3' cx='50%25' cy='50%25' r='50%25'%3E%3Cstop offset='0%25' style='stop-color:%23007766;stop-opacity:0.8' /%3E%3Cstop offset='100%25' style='stop-color:%23e56404;stop-opacity:1' /%3E%3C/radialGradient%3E%3C/defs%3E%3Crect width='1200' height='600' fill='url(%23grad3)'/%3E%3C/svg%3E"
	}
];

export function HeroSection({ channel }: { channel: string }) {
	const [currentSlide, setCurrentSlide] = useState(0);

	useEffect(() => {
		const timer = setInterval(() => {
			setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
		}, 5000);

		return () => clearInterval(timer);
	}, []);

	const currentHero = heroSlides[currentSlide];

	return (
		<section className="relative h-[70vh] min-h-[600px] overflow-hidden bg-gradient-to-br from-slate-900 to-slate-700">
			{/* Background Image/Gradient */}
			<div 
				className="absolute inset-0 bg-cover bg-center bg-no-repeat transition-all duration-1000 ease-in-out"
				style={{ 
					backgroundImage: `url("${currentHero.bgImage}")`,
					opacity: 0.9
				}}
			/>
			
			{/* Overlay */}
			<div className="absolute inset-0 bg-black/30" />

			{/* Content */}
			<div className="relative z-10 flex h-full items-center">
				<div className="container-custom">
					<div className="max-w-3xl">
						<div className="mb-4 opacity-0 animate-fade-in" style={{ animationDelay: '0.2s', animationFillMode: 'forwards' }}>
							<span className="inline-block rounded-full bg-white/20 px-4 py-2 text-sm font-medium text-white backdrop-blur-sm">
								{currentHero.subtitle}
							</span>
						</div>
						
						<h1 className="mb-6 text-4xl font-bold leading-tight text-white opacity-0 animate-fade-in md:text-6xl lg:text-7xl" 
							style={{ animationDelay: '0.4s', animationFillMode: 'forwards' }}>
							<span className="text-balance">{currentHero.title}</span>
						</h1>
						
						<p className="mb-8 text-lg text-white/90 opacity-0 animate-fade-in md:text-xl" 
							style={{ animationDelay: '0.6s', animationFillMode: 'forwards' }}>
							<span className="text-balance">{currentHero.description}</span>
						</p>
						
						<div className="flex flex-col gap-4 opacity-0 animate-fade-in sm:flex-row" 
							style={{ animationDelay: '0.8s', animationFillMode: 'forwards' }}>
							<LinkWithChannel
								href={currentHero.ctaLink}
								className="inline-flex items-center justify-center rounded-lg bg-white px-8 py-4 text-lg font-semibold text-slate-900 transition-all duration-300 hover:bg-white/90 hover:scale-105 hover:shadow-xl"
							>
								{currentHero.ctaText}
								<svg className="ml-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
								</svg>
							</LinkWithChannel>
							
							<LinkWithChannel
								href="/about"
								className="inline-flex items-center justify-center rounded-lg border-2 border-white px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:bg-white hover:text-slate-900"
							>
								Learn More
							</LinkWithChannel>
						</div>
					</div>
				</div>
			</div>

			{/* Slide Indicators */}
			<div className="absolute bottom-8 left-1/2 z-20 flex -translate-x-1/2 space-x-3">
				{heroSlides.map((_, index) => (
					<button
						key={index}
						onClick={() => setCurrentSlide(index)}
						className={`h-3 w-3 rounded-full transition-all duration-300 ${
							index === currentSlide
								? 'bg-white shadow-lg'
								: 'bg-white/50 hover:bg-white/75'
						}`}
						aria-label={`Go to slide ${index + 1}`}
					/>
				))}
			</div>

			{/* Floating Action Buttons */}
			<div className="absolute bottom-8 right-8 z-20 flex flex-col gap-3">
				<button className="flex h-12 w-12 items-center justify-center rounded-full bg-white/20 text-white backdrop-blur-sm transition-all duration-300 hover:bg-white/30">
					<svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
					</svg>
				</button>
				
				<button className="flex h-12 w-12 items-center justify-center rounded-full bg-white/20 text-white backdrop-blur-sm transition-all duration-300 hover:bg-white/30">
					<svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
					</svg>
				</button>
			</div>

			<style jsx>{`
				@keyframes fade-in {
					from {
						opacity: 0;
						transform: translateY(30px);
					}
					to {
						opacity: 1;
						transform: translateY(0);
					}
				}
				
				.animate-fade-in {
					animation: fade-in 0.8s ease-out;
				}
			`}</style>
		</section>
	);
}