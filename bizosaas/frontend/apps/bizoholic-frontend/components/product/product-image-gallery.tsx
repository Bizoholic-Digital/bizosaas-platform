"use client"

import { useState } from "react"
import Image from "next/image"
import { SaleorProductMedia } from "@/lib/saleor-api"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { ChevronLeft, ChevronRight, ZoomIn, Maximize2 } from "lucide-react"

interface ProductImageGalleryProps {
  images: SaleorProductMedia[]
  alt: string
  className?: string
}

export function ProductImageGallery({ images, alt, className }: ProductImageGalleryProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isZoomed, setIsZoomed] = useState(false)
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  const validImages = images.filter(img => img.url)
  
  if (validImages.length === 0) {
    return (
      <div className={cn("aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center", className)}>
        <div className="text-center text-gray-500">
          <div className="h-16 w-16 bg-gray-300 dark:bg-gray-600 rounded-lg mx-auto mb-2" />
          <p className="text-sm">No image available</p>
        </div>
      </div>
    )
  }

  const currentImage = validImages[currentIndex]

  const nextImage = () => {
    setCurrentIndex((prev) => (prev + 1) % validImages.length)
  }

  const previousImage = () => {
    setCurrentIndex((prev) => (prev - 1 + validImages.length) % validImages.length)
  }

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!isZoomed) return
    
    const rect = e.currentTarget.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width) * 100
    const y = ((e.clientY - rect.top) / rect.height) * 100
    
    setMousePosition({ x, y })
  }

  return (
    <div className={cn("space-y-4", className)}>
      {/* Main Image */}
      <div className="relative group">
        <div 
          className={cn(
            "relative aspect-square bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden cursor-zoom-in",
            isZoomed && "cursor-zoom-out"
          )}
          onMouseMove={handleMouseMove}
          onMouseEnter={() => setIsZoomed(true)}
          onMouseLeave={() => setIsZoomed(false)}
          onClick={() => setIsZoomed(!isZoomed)}
        >
          <Image
            src={currentImage.url || '/api/placeholder/600/600'}
            alt={alt}
            fill
            className={cn(
              "object-cover transition-transform duration-200",
              isZoomed && "scale-150"
            )}
            style={isZoomed ? {
              transformOrigin: `${mousePosition.x}% ${mousePosition.y}%`
            } : {}}
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            priority
          />
          
          {/* Navigation Arrows */}
          {validImages.length > 1 && (
            <>
              <Button
                variant="outline"
                size="icon"
                className="absolute left-2 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-white/90 hover:bg-white"
                onClick={(e) => {
                  e.stopPropagation()
                  previousImage()
                }}
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-white/90 hover:bg-white"
                onClick={(e) => {
                  e.stopPropagation()
                  nextImage()
                }}
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </>
          )}
          
          {/* Zoom Icon */}
          <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
            {isZoomed ? (
              <Maximize2 className="h-5 w-5 text-white bg-black/50 rounded p-1" />
            ) : (
              <ZoomIn className="h-5 w-5 text-white bg-black/50 rounded p-1" />
            )}
          </div>
          
          {/* Image Counter */}
          {validImages.length > 1 && (
            <div className="absolute bottom-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
              {currentIndex + 1} / {validImages.length}
            </div>
          )}
        </div>
      </div>

      {/* Thumbnail Strip */}
      {validImages.length > 1 && (
        <div className="flex gap-2 overflow-x-auto pb-2">
          {validImages.map((image, index) => (
            <button
              key={image.id || index}
              className={cn(
                "relative flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-colors",
                index === currentIndex 
                  ? "border-red-500" 
                  : "border-gray-200 dark:border-gray-700 hover:border-red-300"
              )}
              onClick={() => setCurrentIndex(index)}
            >
              <Image
                src={image.url || '/api/placeholder/100/100'}
                alt={`${alt} thumbnail ${index + 1}`}
                fill
                className="object-cover"
                sizes="64px"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  )
}