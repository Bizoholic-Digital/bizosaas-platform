import { Metadata } from "next"
import { notFound } from "next/navigation"
import Link from "next/link"
import { AlertCircle, ChevronLeft } from "lucide-react"

import { saleorStoreAPI, saleorAPI } from "@/lib/saleor-api"
import { ProductDetailClient } from "@/components/product/product-detail-client"
import { Button } from "@/components/ui/button"

function ProductNotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950/20 dark:to-orange-950/20">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            Product Not Found
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            The product you're looking for doesn't exist or has been removed.
          </p>
          <Button asChild>
            <Link href="/">
              <ChevronLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
          </Button>
        </div>
      </div>
    </div>
  )
}

export default async function ProductDetailPage({ 
  params 
}: { 
  params: { slug: string } 
}) {
  const slug = params.slug

  try {
    // Try to find product by slug first
    const products = await saleorStoreAPI.getProducts({ first: 1, filter: { slug: slug } })
    
    let product;
    if (products.products.edges.length === 0) {
      // Try by ID if slug doesn't work
      try {
        const result = await saleorStoreAPI.getProduct(slug)
        product = result.product
      } catch {
        notFound()
      }
    } else {
      product = products.products.edges[0].node
    }

    if (!product) {
      notFound()
    }

    return <ProductDetailClient initialProduct={product} slug={slug} />
  } catch (error) {
    console.error('Failed to fetch product:', error)
    notFound()
  }

}

// Generate metadata for SEO
export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  try {
    const products = await saleorStoreAPI.getProducts({ first: 1, filter: { slug: params.slug } })
    const product = products.products.edges[0]?.node

    if (!product) {
      return {
        title: 'Product Not Found',
        description: 'The requested product could not be found.',
      }
    }

    const price = product.variants?.[0]?.pricing?.price?.gross.amount || 0
    const currency = product.variants?.[0]?.pricing?.price?.gross.currency || 'USD'

    return {
      title: `${product.name} - CoreLDove`,
      description: product.description || `${product.name} - High quality products at CoreLDove`,
      keywords: product.metadata?.find(m => m.key === 'keywords')?.value || '',
      openGraph: {
        title: `${product.name} - CoreLDove`,
        description: product.description || `${product.name} - High quality products at CoreLDove`,
        images: [{
          url: product.thumbnail?.url || product.media?.[0]?.url || '',
          width: 800,
          height: 800,
          alt: product.name,
        }],
        type: 'website',
      },
      twitter: {
        card: 'summary_large_image',
        title: `${product.name} - CoreLDove`,
        description: product.description || `${product.name} - High quality products at CoreLDove`,
        images: [product.thumbnail?.url || product.media?.[0]?.url || ''],
      },
      alternates: {
        canonical: `${process.env.NEXT_PUBLIC_BASE_URL}/products/${params.slug}`,
      },
      other: {
        'product:price:amount': price.toString(),
        'product:price:currency': currency.toUpperCase(),
      },
    }
  } catch (error) {
    console.error('Failed to generate metadata:', error)
    return {
      title: 'Product - CoreLDove',
      description: 'High quality products at CoreLDove',
    }
  }
}

// Disable static generation to prevent build-time API calls
export const dynamic = 'force-dynamic'

// Generate static params for static generation (optional) - DISABLED
// export async function generateStaticParams() {
//   try {
//     const products = await saleorAPI.getProducts({ first: 100 })
//     return products.products.edges.map((edge) => ({
//       slug: edge.node.slug || edge.node.id,
//     }))
//   } catch (error) {
//     console.error('Failed to generate static params:', error)
//     return []
//   }
// }