/**
 * CMS Content Block Components
 * Renders Wagtail CMS content blocks in the frontend
 */

import { ContentBlock, CallToActionBlock, FeatureBlock, TestimonialBlock, StatsBlock, PricingBlock } from '@/lib/wagtail-cms'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Star, ArrowRight, Check } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'

interface ContentBlocksProps {
  blocks: ContentBlock[]
  className?: string
}

export function ContentBlocks({ blocks, className = "" }: ContentBlocksProps) {
  if (!blocks || blocks.length === 0) {
    return null
  }

  return (
    <div className={className}>
      {blocks.map((block, index) => (
        <ContentBlockRenderer key={`${block.type}-${index}`} block={block} />
      ))}
    </div>
  )
}

interface ContentBlockRendererProps {
  block: ContentBlock
}

function ContentBlockRenderer({ block }: ContentBlockRendererProps) {
  switch (block.type) {
    case 'heading':
      return <HeadingBlock value={block.value} />
    case 'paragraph':
      return <ParagraphBlock value={block.value} />
    case 'image':
      return <ImageBlock value={block.value} />
    case 'cta':
      return <CTABlock value={block.value} />
    case 'features':
      return <FeaturesBlock value={block.value} />
    case 'testimonials':
      return <TestimonialsBlock value={block.value} />
    case 'stats':
      return <StatsBlock value={block.value} />
    case 'pricing':
      return <PricingBlock value={block.value} />
    case 'html':
      return <HTMLBlock value={block.value} />
    default:
      console.warn(`Unknown block type: ${block.type}`)
      return null
  }
}

function HeadingBlock({ value }: { value: string }) {
  return (
    <div className="py-8">
      <h2 className="text-3xl md:text-4xl font-bold text-center mb-6">
        {value}
      </h2>
    </div>
  )
}

function ParagraphBlock({ value }: { value: string }) {
  return (
    <div className="py-4">
      <p className="text-lg text-muted-foreground leading-relaxed">
        {value}
      </p>
    </div>
  )
}

function ImageBlock({ value }: { value: any }) {
  if (!value?.url) return null

  return (
    <div className="py-8">
      <div className="relative w-full h-64 md:h-96 rounded-lg overflow-hidden">
        <Image
          src={value.url}
          alt={value.alt || 'Content image'}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
      </div>
    </div>
  )
}

function CTABlock({ value }: { value: CallToActionBlock }) {
  const buttonVariant = value.button_style === 'primary' ? 'default' : 
                       value.button_style === 'secondary' ? 'secondary' : 
                       'outline'

  return (
    <div className="py-12">
      <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-2xl p-8 text-center">
        <h3 className="text-2xl font-bold mb-4">{value.title}</h3>
        {value.description && (
          <p className="text-lg text-muted-foreground mb-6 max-w-2xl mx-auto">
            {value.description}
          </p>
        )}
        <Link href={value.button_url}>
          <Button size="lg" variant={buttonVariant} className="btn-gradient">
            {value.button_text}
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
        </Link>
      </div>
    </div>
  )
}

function FeaturesBlock({ value }: { value: FeatureBlock[] }) {
  if (!value || value.length === 0) return null

  return (
    <div className="py-12">
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {value.map((feature, index) => (
          <Card key={index} className="text-center hover:shadow-lg transition-shadow">
            <CardHeader>
              {feature.icon && (
                <div className="w-12 h-12 mx-auto mb-4 flex items-center justify-center bg-primary/10 rounded-full">
                  {/* Icon would need to be mapped from string to component */}
                  <div className="text-2xl">{feature.icon}</div>
                </div>
              )}
              <CardTitle className="text-xl">{feature.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base">
                {feature.description}
              </CardDescription>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function TestimonialsBlock({ value }: { value: TestimonialBlock[] }) {
  if (!value || value.length === 0) return null

  return (
    <div className="py-12">
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {value.map((testimonial, index) => (
          <Card key={index} className="relative">
            <CardHeader>
              <div className="flex items-center gap-2 mb-4">
                {Array.from({ length: testimonial.rating }).map((_, i) => (
                  <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                ))}
              </div>
              <blockquote className="text-lg italic">
                "{testimonial.quote}"
              </blockquote>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-3">
                {testimonial.author_image && (
                  <div className="relative w-12 h-12 rounded-full overflow-hidden">
                    <Image
                      src={testimonial.author_image}
                      alt={testimonial.author_name}
                      fill
                      className="object-cover"
                    />
                  </div>
                )}
                <div>
                  <div className="font-semibold">{testimonial.author_name}</div>
                  {testimonial.author_title && (
                    <div className="text-sm text-muted-foreground">
                      {testimonial.author_title}
                      {testimonial.author_company && ` at ${testimonial.author_company}`}
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function StatsBlock({ value }: { value: StatsBlock[] }) {
  if (!value || value.length === 0) return null

  return (
    <div className="py-12">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
        {value.map((stat, index) => (
          <div key={index} className="text-center">
            <div className="text-3xl md:text-4xl font-bold text-primary mb-2">
              {stat.stat_number}
            </div>
            <div className="font-semibold mb-1">{stat.stat_label}</div>
            {stat.stat_description && (
              <div className="text-sm text-muted-foreground">
                {stat.stat_description}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function PricingBlock({ value }: { value: PricingBlock[] }) {
  if (!value || value.length === 0) return null

  return (
    <div className="py-12">
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
        {value.map((plan, index) => (
          <Card 
            key={index} 
            className={`relative text-center ${
              plan.is_popular ? 'border-primary ring-2 ring-primary/20 scale-105' : ''
            }`}
          >
            {plan.is_popular && (
              <Badge className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-primary">
                Most Popular
              </Badge>
            )}
            <CardHeader>
              <CardTitle className="text-2xl">{plan.plan_name}</CardTitle>
              <div className="text-4xl font-bold">
                {plan.price}
                <span className="text-lg font-normal text-muted-foreground">
                  /{plan.price_period}
                </span>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                {plan.features.map((feature, featureIndex) => (
                  <div key={featureIndex} className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-green-500 flex-shrink-0" />
                    <span className="text-sm">{feature}</span>
                  </div>
                ))}
              </div>
              <Link href={plan.cta_url}>
                <Button 
                  className="w-full mt-6" 
                  variant={plan.is_popular ? 'default' : 'outline'}
                >
                  {plan.cta_text}
                </Button>
              </Link>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

function HTMLBlock({ value }: { value: string }) {
  return (
    <div 
      className="py-4 cms-html-content"
      dangerouslySetInnerHTML={{ __html: value }}
    />
  )
}

// Component for rendering a complete Wagtail page
interface CMSPageProps {
  page: {
    title: string
    content_blocks: ContentBlock[]
    meta_description?: string
  }
  className?: string
}

export function CMSPage({ page, className = "" }: CMSPageProps) {
  return (
    <div className={className}>
      <div className="container">
        <div className="max-w-4xl mx-auto">
          <header className="py-12 text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              {page.title}
            </h1>
            {page.meta_description && (
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                {page.meta_description}
              </p>
            )}
          </header>
          
          <ContentBlocks blocks={page.content_blocks} />
        </div>
      </div>
    </div>
  )
}