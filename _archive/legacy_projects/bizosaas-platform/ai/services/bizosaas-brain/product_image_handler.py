#!/usr/bin/env python3
"""
Product Image Handler for BizOSaaS Brain API
Manages product images from Amazon SP-API with SEO optimization and fallback support
"""

import logging
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
from urllib.parse import quote

logger = logging.getLogger(__name__)

@dataclass
class ProductImage:
    """Product image data structure with SEO metadata"""
    url: str
    alt_text: str
    title: str
    width: int = 400
    height: int = 400
    size_variant: str = "main"  # main, thumbnail, large, extra_large
    source: str = "amazon"  # amazon, unsplash, placeholder
    seo_optimized: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "alt": self.alt_text,
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "size_variant": self.size_variant,
            "source": self.source,
            "seo_optimized": self.seo_optimized
        }

@dataclass
class ProductImageSet:
    """Complete set of product images with variants"""
    main: ProductImage
    thumbnail: Optional[ProductImage] = None
    large: Optional[ProductImage] = None
    gallery: Optional[List[ProductImage]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"main": self.main.to_dict()}
        if self.thumbnail:
            result["thumbnail"] = self.thumbnail.to_dict()
        if self.large:
            result["large"] = self.large.to_dict()
        if self.gallery:
            result["gallery"] = [img.to_dict() for img in self.gallery]
        return result

class ProductImageHandler:
    """
    Handles product images from multiple sources with SEO optimization
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ProductImageHandler")
        
        # Category-specific image mappings from Unsplash
        self.category_images = {
            "Mobile Accessories": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91",
            "Home & Kitchen": "https://images.unsplash.com/photo-1586201375761-83865001e31c", 
            "Clothing": "https://images.unsplash.com/photo-1441986300917-64674bd600d8",
            "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661",
            "Fitness Equipment": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b",
            "Beauty Products": "https://images.unsplash.com/photo-1596462502278-27bfdc403348",
            "Home Decor": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
            "Automotive Accessories": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d",
            "Sports & Outdoor": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b",
            "Books": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570",
            "Toys": "https://images.unsplash.com/photo-1558877385-9daf4b6a7f62",
            "Jewelry": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338"
        }
        
        # Amazon image size variants
        self.amazon_image_sizes = {
            "thumbnail": {"width": 160, "height": 160, "suffix": "._SL160_"},
            "small": {"width": 300, "height": 300, "suffix": "._SL300_"},
            "medium": {"width": 500, "height": 500, "suffix": "._SL500_"},
            "large": {"width": 1000, "height": 1000, "suffix": "._SL1000_"}
        }
    
    def extract_amazon_images(self, amazon_product_data: Dict[str, Any]) -> Optional[ProductImageSet]:
        """
        Extract images from Amazon SP-API product data
        """
        try:
            # Try different possible image fields from Amazon API
            main_image_url = None
            
            # Check various possible image fields
            if 'images' in amazon_product_data:
                images = amazon_product_data['images']
                if isinstance(images, dict) and 'main' in images:
                    main_image_url = images['main'].get('url', images['main'].get('link'))
                elif isinstance(images, list) and len(images) > 0:
                    main_image_url = images[0].get('url', images[0].get('link'))
            
            # Try other common Amazon image fields
            if not main_image_url:
                for field in ['main_image', 'mainImage', 'image_url', 'imageUrl', 'primary_image']:
                    if field in amazon_product_data:
                        img_data = amazon_product_data[field]
                        if isinstance(img_data, str):
                            main_image_url = img_data
                        elif isinstance(img_data, dict):
                            main_image_url = img_data.get('url', img_data.get('link'))
                        break
            
            if main_image_url:
                product_title = amazon_product_data.get('title', amazon_product_data.get('name', 'Amazon Product'))
                
                # Create main image with SEO optimization
                main_image = ProductImage(
                    url=self._optimize_amazon_image_url(main_image_url, 'medium'),
                    alt_text=f"{product_title} - High Quality Product Image",
                    title=f"{product_title} | Premium Quality | Fast Shipping",
                    width=500,
                    height=500,
                    size_variant="main",
                    source="amazon",
                    seo_optimized=True
                )
                
                # Create thumbnail variant
                thumbnail = ProductImage(
                    url=self._optimize_amazon_image_url(main_image_url, 'thumbnail'),
                    alt_text=f"{product_title} Thumbnail",
                    title=f"{product_title} - Thumbnail View",
                    width=160,
                    height=160,
                    size_variant="thumbnail",
                    source="amazon",
                    seo_optimized=True
                )
                
                # Create large variant
                large = ProductImage(
                    url=self._optimize_amazon_image_url(main_image_url, 'large'),
                    alt_text=f"{product_title} - Detailed View",
                    title=f"{product_title} - High Resolution Image",
                    width=1000,
                    height=1000,
                    size_variant="large",
                    source="amazon",
                    seo_optimized=True
                )
                
                return ProductImageSet(
                    main=main_image,
                    thumbnail=thumbnail,
                    large=large
                )
                
        except Exception as e:
            self.logger.warning(f"Error extracting Amazon images: {e}")
            
        return None
    
    def create_fallback_images(self, product_data: Dict[str, Any]) -> ProductImageSet:
        """
        Create fallback images using category-specific Unsplash images
        """
        category = product_data.get('category', 'Electronics')
        product_title = product_data.get('title', product_data.get('name', 'Product'))
        asin = product_data.get('asin', 'unknown')
        
        # Get category-specific base image
        base_image_url = self.category_images.get(category, self.category_images['Electronics'])
        
        # Create SEO-optimized images
        main_image = ProductImage(
            url=f"{base_image_url}?w=500&h=500&fit=crop&auto=format&q=80",
            alt_text=f"{product_title} - {category} Product | ASIN: {asin}",
            title=f"{product_title} | Premium {category} | Fast Delivery | Buy Online",
            width=500,
            height=500,
            size_variant="main",
            source="unsplash",
            seo_optimized=True
        )
        
        thumbnail = ProductImage(
            url=f"{base_image_url}?w=160&h=160&fit=crop&auto=format&q=80",
            alt_text=f"{product_title} Thumbnail",
            title=f"{product_title} - Quick View",
            width=160,
            height=160,
            size_variant="thumbnail",
            source="unsplash",
            seo_optimized=True
        )
        
        large = ProductImage(
            url=f"{base_image_url}?w=1000&h=1000&fit=crop&auto=format&q=80",
            alt_text=f"{product_title} - High Resolution Image",
            title=f"{product_title} | Detailed Product View | {category}",
            width=1000,
            height=1000,
            size_variant="large",
            source="unsplash",
            seo_optimized=True
        )
        
        return ProductImageSet(
            main=main_image,
            thumbnail=thumbnail,
            large=large
        )
    
    def _optimize_amazon_image_url(self, base_url: str, size: str) -> str:
        """
        Optimize Amazon image URL for different sizes
        """
        if not base_url:
            return ""
            
        try:
            # Remove existing size suffixes
            for size_info in self.amazon_image_sizes.values():
                base_url = base_url.replace(size_info['suffix'], '')
            
            # Add new size suffix
            if size in self.amazon_image_sizes:
                size_info = self.amazon_image_sizes[size]
                # Insert size suffix before file extension
                if '.jpg' in base_url:
                    base_url = base_url.replace('.jpg', f"{size_info['suffix']}.jpg")
                elif '.png' in base_url:
                    base_url = base_url.replace('.png', f"{size_info['suffix']}.png")
                else:
                    base_url += size_info['suffix']
            
            return base_url
            
        except Exception as e:
            self.logger.warning(f"Error optimizing Amazon image URL: {e}")
            return base_url
    
    def process_product_images(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process product images with Amazon data and fallback
        """
        # Try to get Amazon images first
        amazon_images = self.extract_amazon_images(product_data)
        
        if amazon_images:
            self.logger.debug(f"Using Amazon images for product: {product_data.get('asin', 'unknown')}")
            image_set = amazon_images
        else:
            self.logger.debug(f"Using fallback images for product: {product_data.get('asin', 'unknown')}")
            image_set = self.create_fallback_images(product_data)
        
        # Return in the format expected by the API
        return {
            "images": [image_set.main.to_dict()],
            "image_variants": image_set.to_dict(),
            "seo_optimized": True
        }
    
    def create_category_image(self, category_name: str, category_slug: str) -> ProductImage:
        """
        Create SEO-optimized category images
        """
        base_url = self.category_images.get(category_name, self.category_images['Electronics'])
        
        return ProductImage(
            url=f"{base_url}?w=600&h=400&fit=crop&auto=format&q=80",
            alt_text=f"{category_name} Category - Premium Products Collection",
            title=f"{category_name} | Best Deals | Shop {category_name} Products Online",
            width=600,
            height=400,
            size_variant="category_header",
            source="unsplash",
            seo_optimized=True
        )

# Global instance
product_image_handler = ProductImageHandler()