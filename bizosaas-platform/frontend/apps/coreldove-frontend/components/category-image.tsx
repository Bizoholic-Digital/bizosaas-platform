'use client'

import { useEffect, useState } from 'react'

interface CategoryImageProps {
  categoryName: string
  className?: string
  alt?: string
}

export default function CategoryImage({ categoryName, className, alt }: CategoryImageProps) {
  const [imageData, setImageData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetchCategoryImage()
  }, [categoryName])

  const fetchCategoryImage = async () => {
    try {
      setLoading(true)
      const response = await fetch(`/api/brain/images/categories?category=${encodeURIComponent(categoryName)}&size=medium`)
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.image) {
          setImageData(data.image)
        }
      }
    } catch (error) {
      console.error('Error fetching category image:', error)
      setError(true)
    } finally {
      setLoading(false)
    }
  }

  const getFallbackImage = () => {
    const categoryImages = {
      "Mobile Accessories": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=600&h=400&fit=crop&auto=format&q=80",
      "Home & Kitchen": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&h=400&fit=crop&auto=format&q=80", 
      "Clothing": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&h=400&fit=crop&auto=format&q=80",
      "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=600&h=400&fit=crop&auto=format&q=80",
      "Fitness Equipment": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop&auto=format&q=80",
      "Beauty Products": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&h=400&fit=crop&auto=format&q=80",
      "Home Decor": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop&auto=format&q=80",
    }

    const normalizedName = categoryName?.trim() || ''
    
    // Try exact match
    if (categoryImages[normalizedName as keyof typeof categoryImages]) {
      return categoryImages[normalizedName as keyof typeof categoryImages]
    }
    
    // Try partial match
    const categoryKeys = Object.keys(categoryImages)
    const matchedKey = categoryKeys.find(key => 
      key.toLowerCase().includes(normalizedName.toLowerCase()) ||
      normalizedName.toLowerCase().includes(key.toLowerCase())
    )
    
    if (matchedKey) {
      return categoryImages[matchedKey as keyof typeof categoryImages]
    }
    
    // Default to Electronics
    return categoryImages["Electronics"]
  }

  if (loading) {
    return (
      <div className={`bg-gray-200 animate-pulse ${className || ''}`}>
        <div className="w-full h-full flex items-center justify-center">
          <div className="text-gray-400">Loading...</div>
        </div>
      </div>
    )
  }

  const imageSrc = imageData?.url || getFallbackImage()
  const imageAlt = imageData?.alt || alt || `${categoryName} - Premium Products Category`

  return (
    <img 
      src={imageSrc}
      alt={imageAlt}
      title={imageData?.title}
      className={className}
      onError={(e) => {
        if (!error) {
          setError(true)
          e.currentTarget.src = getFallbackImage()
        }
      }}
    />
  )
}