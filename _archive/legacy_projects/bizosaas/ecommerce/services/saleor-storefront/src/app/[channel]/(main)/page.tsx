import { ProductListByCollectionDocument } from "@/gql/graphql";
import { executeGraphQL } from "@/lib/graphql";
import { ProductList } from "@/ui/components/ProductList";
import { HeroSection } from "@/ui/components/HeroSection";
import { FeaturesSection } from "@/ui/components/FeaturesSection";
import { CategoryShowcase } from "@/ui/components/CategoryShowcase";
import { TestimonialsSection } from "@/ui/components/TestimonialsSection";
import { NewsletterSection } from "@/ui/components/NewsletterSection";

export const metadata = {
	title: "CoreLDove - Premium E-commerce Platform",
	description:
		"CoreLDove offers premium e-commerce solutions powered by Saleor & Next.js. Experience modern, fast, and scalable online shopping with AI-powered recommendations.",
};

export default async function Page(props: { params: Promise<{ channel: string }> }) {
	const params = await props.params;
	const data = await executeGraphQL(ProductListByCollectionDocument, {
		variables: {
			slug: "featured-products",
			channel: params.channel,
		},
		revalidate: 60,
	});

	const products = data.collection?.products?.edges.map(({ node: product }) => product) || [];

	return (
		<main className="min-h-screen">
			{/* Hero Section */}
			<HeroSection channel={params.channel} />

			{/* Features Section */}
			<FeaturesSection />

			{/* Category Showcase */}
			<CategoryShowcase channel={params.channel} />

			{/* Featured Products */}
			{products.length > 0 && (
				<ProductList 
					products={products} 
					title="Featured Products"
					description="Discover our hand-picked selection of premium products, chosen for their exceptional quality and style."
					showHeader={true}
				/>
			)}

			{/* Customer Testimonials */}
			<TestimonialsSection />

			{/* Newsletter Signup */}
			<NewsletterSection />
		</main>
	);
}
