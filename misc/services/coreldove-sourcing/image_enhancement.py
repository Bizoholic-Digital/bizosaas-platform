"""
Image Enhancement Pipeline for CoreLDove
Removes branding, enhances quality, and optimizes product images for e-commerce
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import io
import base64
from datetime import datetime
import hashlib
import aiohttp
import aiofiles
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import cv2
import numpy as np
from rembg import remove
import tempfile
import os

logger = logging.getLogger(__name__)

class EnhancementType(Enum):
    REMOVE_BRANDING = "remove_branding"
    ENHANCE_QUALITY = "enhance_quality" 
    OPTIMIZE_SIZE = "optimize_size"
    ADD_WATERMARK = "add_watermark"
    REMOVE_BACKGROUND = "remove_background"
    CROP_SMART = "crop_smart"
    COLOR_CORRECTION = "color_correction"
    UPSCALE = "upscale"

class ImageFormat(Enum):
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"
    AVIF = "avif"

@dataclass
class ImageDimensions:
    width: int
    height: int
    aspect_ratio: float = None
    
    def __post_init__(self):
        if self.aspect_ratio is None:
            self.aspect_ratio = self.width / self.height if self.height > 0 else 1.0

@dataclass
class EnhancementRequest:
    product_id: str
    image_urls: List[str]
    enhancement_types: List[EnhancementType]
    output_formats: List[ImageFormat] = None
    target_dimensions: Dict[str, ImageDimensions] = None
    quality_settings: Dict[str, Any] = None
    watermark_config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.output_formats is None:
            self.output_formats = [ImageFormat.JPG, ImageFormat.WEBP]
        if self.target_dimensions is None:
            self.target_dimensions = {
                "main": ImageDimensions(1000, 1000),
                "thumbnail": ImageDimensions(300, 300),
                "mobile": ImageDimensions(600, 600)
            }

@dataclass
class EnhancedImage:
    variant: str  # main, thumbnail, mobile
    url: str
    format: ImageFormat
    dimensions: ImageDimensions
    file_size_kb: int
    enhancements_applied: List[EnhancementType]
    quality_score: float
    processing_time_seconds: float

@dataclass
class ImageEnhancementResult:
    product_id: str
    original_images: List[str]
    enhanced_images: Dict[str, List[EnhancedImage]]  # variant -> images
    processing_stats: Dict[str, Any]
    quality_metrics: Dict[str, float]
    total_processing_time_seconds: float
    storage_used_mb: float
    cost_usd: float
    created_at: datetime

class BrandingDetector:
    """Detects and removes branding elements from images"""
    
    def __init__(self):
        self.common_brand_patterns = [
            "amazon", "ebay", "walmart", "target", "costco",
            "logo", "trademark", "©", "®", "™", "brand"
        ]
        
    async def detect_branding(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect potential branding elements in image"""
        
        branding_elements = []
        
        try:
            # Convert to OpenCV format for analysis
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Detect text regions using EAST text detector (simplified version)
            text_regions = self._detect_text_regions(gray)
            
            for region in text_regions:
                x, y, w, h = region
                confidence = self._analyze_branding_likelihood(gray[y:y+h, x:x+w])
                
                if confidence > 0.7:  # 70% confidence threshold
                    branding_elements.append({
                        "type": "text_logo",
                        "bbox": [x, y, w, h],
                        "confidence": confidence
                    })
            
            # Detect watermarks and logos
            watermarks = await self._detect_watermarks(cv_image)
            branding_elements.extend(watermarks)
            
        except Exception as e:
            logger.error(f"Error detecting branding: {e}")
        
        return branding_elements
    
    def _detect_text_regions(self, gray_image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect text regions in image using basic computer vision"""
        
        regions = []
        
        try:
            # Apply morphological operations to detect text-like regions
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            morph = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter based on text-like characteristics
                aspect_ratio = w / float(h)
                area = cv2.contourArea(contour)
                
                if (0.2 < aspect_ratio < 10.0 and  # Reasonable aspect ratio for text
                    area > 100 and  # Minimum size
                    area < (gray_image.shape[0] * gray_image.shape[1]) * 0.3):  # Max 30% of image
                    regions.append((x, y, w, h))
            
        except Exception as e:
            logger.error(f"Error detecting text regions: {e}")
        
        return regions
    
    def _analyze_branding_likelihood(self, region: np.ndarray) -> float:
        """Analyze likelihood that region contains branding"""
        
        try:
            # Simple heuristics for branding detection
            height, width = region.shape
            
            # Check if region has consistent text-like properties
            std_dev = np.std(region)
            mean_intensity = np.mean(region)
            
            # Branding often has high contrast and consistent styling
            contrast_score = std_dev / 255.0 if std_dev > 0 else 0
            
            # Check for typical brand placement (corners, edges)
            edge_proximity = min(region.shape) / max(region.shape)
            
            # Combine factors
            likelihood = (contrast_score * 0.4 + 
                         (1.0 - edge_proximity) * 0.3 + 
                         (1.0 if mean_intensity < 50 or mean_intensity > 200 else 0.5) * 0.3)
            
            return min(likelihood, 1.0)
            
        except Exception:
            return 0.0
    
    async def _detect_watermarks(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect watermarks and transparent overlays"""
        
        watermarks = []
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Look for semi-transparent regions (potential watermarks)
            # This is a simplified approach - real implementation would be more sophisticated
            
            # Use template matching for common watermark patterns
            height, width = gray.shape
            
            # Check corners for watermarks (common placement)
            corner_regions = [
                (0, 0, width//3, height//3),  # Top-left
                (2*width//3, 0, width//3, height//3),  # Top-right
                (0, 2*height//3, width//3, height//3),  # Bottom-left
                (2*width//3, 2*height//3, width//3, height//3),  # Bottom-right
            ]
            
            for x, y, w, h in corner_regions:
                region = gray[y:y+h, x:x+w]
                
                # Look for repeating patterns or low-contrast overlays
                pattern_score = self._detect_pattern_repetition(region)
                
                if pattern_score > 0.6:
                    watermarks.append({
                        "type": "watermark",
                        "bbox": [x, y, w, h],
                        "confidence": pattern_score
                    })
        
        except Exception as e:
            logger.error(f"Error detecting watermarks: {e}")
        
        return watermarks
    
    def _detect_pattern_repetition(self, region: np.ndarray) -> float:
        """Detect if region contains repetitive patterns (watermarks)"""
        
        try:
            if region.size == 0:
                return 0.0
            
            # Calculate variance - watermarks often have low variance
            variance = np.var(region)
            
            # Normalize variance score
            variance_score = 1.0 / (1.0 + variance / 1000.0)
            
            # Check for edge density (watermarks often have defined edges)
            edges = cv2.Canny(region, 50, 150)
            edge_density = np.sum(edges > 0) / region.size
            
            # Combine scores
            pattern_score = (variance_score * 0.6 + edge_density * 0.4)
            
            return min(pattern_score, 1.0)
            
        except Exception:
            return 0.0
    
    async def remove_branding(self, image: Image.Image, branding_elements: List[Dict[str, Any]]) -> Image.Image:
        """Remove detected branding elements from image"""
        
        if not branding_elements:
            return image
        
        try:
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            for element in branding_elements:
                bbox = element["bbox"]
                x, y, w, h = bbox
                
                # Use inpainting to remove branding
                mask = np.zeros(cv_image.shape[:2], dtype=np.uint8)
                mask[y:y+h, x:x+w] = 255
                
                # Apply inpainting
                cv_image = cv2.inpaint(cv_image, mask, 3, cv2.INPAINT_TELEA)
            
            # Convert back to PIL
            result_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            
            return result_image
            
        except Exception as e:
            logger.error(f"Error removing branding: {e}")
            return image

class ImageEnhancer:
    """Enhances image quality using various techniques"""
    
    def __init__(self):
        self.enhancement_settings = {
            "sharpness": 1.2,
            "contrast": 1.1,
            "brightness": 1.05,
            "saturation": 1.1
        }
    
    async def enhance_quality(self, image: Image.Image, settings: Dict[str, Any] = None) -> Image.Image:
        """Enhance image quality using PIL filters and adjustments"""
        
        enhanced = image.copy()
        enhancement_settings = settings or self.enhancement_settings
        
        try:
            # Sharpness enhancement
            if "sharpness" in enhancement_settings:
                enhancer = ImageEnhance.Sharpness(enhanced)
                enhanced = enhancer.enhance(enhancement_settings["sharpness"])
            
            # Contrast enhancement
            if "contrast" in enhancement_settings:
                enhancer = ImageEnhance.Contrast(enhanced)
                enhanced = enhancer.enhance(enhancement_settings["contrast"])
            
            # Brightness adjustment
            if "brightness" in enhancement_settings:
                enhancer = ImageEnhance.Brightness(enhanced)
                enhanced = enhancer.enhance(enhancement_settings["brightness"])
            
            # Color saturation
            if "saturation" in enhancement_settings:
                enhancer = ImageEnhance.Color(enhanced)
                enhanced = enhancer.enhance(enhancement_settings["saturation"])
            
            # Apply subtle smoothing filter
            enhanced = enhanced.filter(ImageFilter.SMOOTH_MORE)
            
        except Exception as e:
            logger.error(f"Error enhancing image quality: {e}")
            return image
        
        return enhanced
    
    async def upscale_image(self, image: Image.Image, scale_factor: float = 2.0) -> Image.Image:
        """Upscale image using AI-based techniques (simplified version)"""
        
        try:
            # For now, use high-quality resampling
            # In production, this could use AI upscaling models like ESRGAN
            new_size = (
                int(image.width * scale_factor),
                int(image.height * scale_factor)
            )
            
            upscaled = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Apply additional sharpening after upscaling
            enhancer = ImageEnhance.Sharpness(upscaled)
            upscaled = enhancer.enhance(1.1)
            
            return upscaled
            
        except Exception as e:
            logger.error(f"Error upscaling image: {e}")
            return image
    
    async def correct_colors(self, image: Image.Image) -> Image.Image:
        """Apply automatic color correction"""
        
        try:
            # Convert to numpy array for processing
            img_array = np.array(image)
            
            # Apply histogram equalization per channel
            corrected = img_array.copy()
            
            for channel in range(img_array.shape[2]):
                corrected[:, :, channel] = cv2.equalizeHist(img_array[:, :, channel])
            
            # Blend with original (subtle correction)
            alpha = 0.3
            blended = cv2.addWeighted(img_array, 1-alpha, corrected, alpha, 0)
            
            return Image.fromarray(blended)
            
        except Exception as e:
            logger.error(f"Error correcting colors: {e}")
            return image

class ImageOptimizer:
    """Optimizes images for web and e-commerce platforms"""
    
    def __init__(self):
        self.quality_settings = {
            ImageFormat.JPG: {"quality": 85, "optimize": True},
            ImageFormat.PNG: {"optimize": True},
            ImageFormat.WEBP: {"quality": 90, "method": 6},
            ImageFormat.AVIF: {"quality": 85}
        }
    
    async def optimize_for_web(self, image: Image.Image, target_format: ImageFormat,
                             target_size_kb: int = None) -> Tuple[bytes, Dict[str, Any]]:
        """Optimize image for web delivery"""
        
        output = io.BytesIO()
        format_str = target_format.value.upper()
        if format_str == "JPG":
            format_str = "JPEG"
        
        quality_config = self.quality_settings.get(target_format, {})
        
        try:
            # Convert RGBA to RGB for JPEG
            if target_format == ImageFormat.JPG and image.mode == "RGBA":
                # Create white background
                white_bg = Image.new("RGB", image.size, (255, 255, 255))
                white_bg.paste(image, mask=image.split()[-1] if len(image.split()) == 4 else None)
                image = white_bg
            
            # Save with optimization
            if target_format == ImageFormat.JPG:
                image.save(output, format=format_str, **quality_config)
            elif target_format == ImageFormat.PNG:
                image.save(output, format=format_str, **quality_config)
            elif target_format == ImageFormat.WEBP:
                image.save(output, format=format_str, **quality_config)
            else:
                # Fallback to JPEG
                if image.mode == "RGBA":
                    white_bg = Image.new("RGB", image.size, (255, 255, 255))
                    white_bg.paste(image, mask=image.split()[-1])
                    image = white_bg
                image.save(output, format="JPEG", quality=85, optimize=True)
            
            image_bytes = output.getvalue()
            size_kb = len(image_bytes) / 1024
            
            # If target size specified and exceeded, reduce quality
            if target_size_kb and size_kb > target_size_kb:
                image_bytes = await self._reduce_size(image, target_format, target_size_kb)
                size_kb = len(image_bytes) / 1024
            
            stats = {
                "size_kb": round(size_kb, 2),
                "format": target_format.value,
                "dimensions": f"{image.width}x{image.height}",
                "mode": image.mode
            }
            
            return image_bytes, stats
            
        except Exception as e:
            logger.error(f"Error optimizing image: {e}")
            # Fallback to basic JPEG
            output = io.BytesIO()
            if image.mode == "RGBA":
                white_bg = Image.new("RGB", image.size, (255, 255, 255))
                white_bg.paste(image, mask=image.split()[-1])
                image = white_bg
            image.save(output, format="JPEG", quality=75)
            return output.getvalue(), {"size_kb": len(output.getvalue()) / 1024}
    
    async def _reduce_size(self, image: Image.Image, target_format: ImageFormat, 
                          target_size_kb: int) -> bytes:
        """Reduce image file size to meet target"""
        
        quality = 90
        min_quality = 30
        
        while quality >= min_quality:
            output = io.BytesIO()
            
            try:
                if target_format == ImageFormat.JPG:
                    image.save(output, format="JPEG", quality=quality, optimize=True)
                elif target_format == ImageFormat.WEBP:
                    image.save(output, format="WEBP", quality=quality, method=6)
                else:
                    image.save(output, format="PNG", optimize=True)
                
                if len(output.getvalue()) / 1024 <= target_size_kb:
                    return output.getvalue()
                
                quality -= 10
                
            except Exception:
                quality -= 10
                continue
        
        # If still too large, resize image
        scale_factor = 0.9
        while scale_factor > 0.5:
            resized = image.resize(
                (int(image.width * scale_factor), int(image.height * scale_factor)),
                Image.Resampling.LANCZOS
            )
            
            output = io.BytesIO()
            resized.save(output, format="JPEG", quality=75, optimize=True)
            
            if len(output.getvalue()) / 1024 <= target_size_kb:
                return output.getvalue()
            
            scale_factor -= 0.1
        
        # Final fallback
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=50)
        return output.getvalue()
    
    async def create_variants(self, image: Image.Image, 
                            dimensions: Dict[str, ImageDimensions]) -> Dict[str, Image.Image]:
        """Create multiple size variants of the image"""
        
        variants = {}
        
        for variant_name, target_dims in dimensions.items():
            try:
                # Smart crop/resize to maintain aspect ratio
                variant = await self._smart_resize(image, target_dims)
                variants[variant_name] = variant
                
            except Exception as e:
                logger.error(f"Error creating variant {variant_name}: {e}")
                # Fallback to simple resize
                variant = image.resize((target_dims.width, target_dims.height), Image.Resampling.LANCZOS)
                variants[variant_name] = variant
        
        return variants
    
    async def _smart_resize(self, image: Image.Image, target_dims: ImageDimensions) -> Image.Image:
        """Smart resize that maintains important image content"""
        
        # Calculate current aspect ratio
        current_ratio = image.width / image.height
        target_ratio = target_dims.aspect_ratio
        
        if abs(current_ratio - target_ratio) < 0.01:
            # Aspect ratios are very close, simple resize
            return image.resize((target_dims.width, target_dims.height), Image.Resampling.LANCZOS)
        
        # Need to crop to match target aspect ratio
        if current_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(image.height * target_ratio)
            left = (image.width - new_width) // 2
            cropped = image.crop((left, 0, left + new_width, image.height))
        else:
            # Image is taller, crop height
            new_height = int(image.width / target_ratio)
            top = (image.height - new_height) // 2
            cropped = image.crop((0, top, image.width, top + new_height))
        
        # Resize to target dimensions
        return cropped.resize((target_dims.width, target_dims.height), Image.Resampling.LANCZOS)

class WatermarkProcessor:
    """Adds watermarks and branding to images"""
    
    def __init__(self):
        self.default_config = {
            "text": "CoreLDove",
            "position": "bottom_right",
            "opacity": 0.3,
            "font_size": 24,
            "color": (255, 255, 255, 180)
        }
    
    async def add_watermark(self, image: Image.Image, config: Dict[str, Any] = None) -> Image.Image:
        """Add watermark to image"""
        
        watermark_config = {**self.default_config, **(config or {})}
        
        try:
            # Create a copy to avoid modifying original
            watermarked = image.copy().convert("RGBA")
            
            # Create watermark overlay
            overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Get font (use default if custom font not available)
            font_size = watermark_config.get("font_size", 24)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text size and position
            text = watermark_config.get("text", "")
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            position = watermark_config.get("position", "bottom_right")
            margin = 20
            
            if position == "bottom_right":
                x = image.width - text_width - margin
                y = image.height - text_height - margin
            elif position == "bottom_left":
                x = margin
                y = image.height - text_height - margin
            elif position == "top_right":
                x = image.width - text_width - margin
                y = margin
            elif position == "top_left":
                x = margin
                y = margin
            elif position == "center":
                x = (image.width - text_width) // 2
                y = (image.height - text_height) // 2
            else:
                x = image.width - text_width - margin
                y = image.height - text_height - margin
            
            # Draw text
            color = watermark_config.get("color", (255, 255, 255, 180))
            draw.text((x, y), text, font=font, fill=color)
            
            # Apply watermark with opacity
            opacity = int(watermark_config.get("opacity", 0.3) * 255)
            overlay = overlay.crop(overlay.getbbox()) if overlay.getbbox() else overlay
            
            # Composite the watermark onto the image
            watermarked = Image.alpha_composite(watermarked, overlay)
            
            # Convert back to original mode if needed
            if image.mode != "RGBA":
                watermarked = watermarked.convert(image.mode)
            
            return watermarked
            
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
            return image

class ImageEnhancementPipeline:
    """Main pipeline for comprehensive image enhancement"""
    
    def __init__(self, storage_client = None):
        self.branding_detector = BrandingDetector()
        self.enhancer = ImageEnhancer()
        self.optimizer = ImageOptimizer()
        self.watermark_processor = WatermarkProcessor()
        self.storage_client = storage_client
        
    async def process_images(self, request: EnhancementRequest) -> ImageEnhancementResult:
        """Process all images according to enhancement request"""
        
        start_time = datetime.utcnow()
        enhanced_images = {}
        processing_stats = {
            "total_images_processed": 0,
            "branding_elements_removed": 0,
            "quality_improvements": [],
            "file_size_reduction_percent": 0.0
        }
        
        original_total_size = 0
        enhanced_total_size = 0
        
        try:
            for i, image_url in enumerate(request.image_urls):
                logger.info(f"Processing image {i+1}/{len(request.image_urls)}: {image_url}")
                
                # Download and process image
                original_image = await self._download_image(image_url)
                if not original_image:
                    continue
                
                original_size = len(await self._image_to_bytes(original_image))
                original_total_size += original_size
                
                # Apply enhancements
                enhanced_image = await self._apply_enhancements(original_image, request)
                
                # Create variants
                variants = await self.optimizer.create_variants(
                    enhanced_image, request.target_dimensions
                )
                
                # Generate final images in different formats
                for variant_name, variant_image in variants.items():
                    if variant_name not in enhanced_images:
                        enhanced_images[variant_name] = []
                    
                    for output_format in request.output_formats:
                        enhanced_result = await self._finalize_image(
                            variant_image, variant_name, output_format, request
                        )
                        
                        if enhanced_result:
                            enhanced_images[variant_name].append(enhanced_result)
                            enhanced_total_size += enhanced_result.file_size_kb * 1024
                
                processing_stats["total_images_processed"] += 1
            
            # Calculate final statistics
            if original_total_size > 0:
                size_reduction = ((original_total_size - enhanced_total_size) / original_total_size) * 100
                processing_stats["file_size_reduction_percent"] = round(size_reduction, 2)
            
            # Calculate quality metrics
            quality_metrics = await self._calculate_quality_metrics(enhanced_images)
            
            end_time = datetime.utcnow()
            total_time = (end_time - start_time).total_seconds()
            
            return ImageEnhancementResult(
                product_id=request.product_id,
                original_images=request.image_urls,
                enhanced_images=enhanced_images,
                processing_stats=processing_stats,
                quality_metrics=quality_metrics,
                total_processing_time_seconds=total_time,
                storage_used_mb=enhanced_total_size / (1024 * 1024),
                cost_usd=self._calculate_processing_cost(processing_stats, enhanced_total_size),
                created_at=start_time
            )
            
        except Exception as e:
            logger.error(f"Error in image enhancement pipeline: {e}")
            raise
    
    async def _download_image(self, image_url: str) -> Optional[Image.Image]:
        """Download image from URL"""
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return Image.open(io.BytesIO(image_data))
        except Exception as e:
            logger.error(f"Error downloading image from {image_url}: {e}")
        
        return None
    
    async def _apply_enhancements(self, image: Image.Image, 
                                request: EnhancementRequest) -> Image.Image:
        """Apply all requested enhancements to image"""
        
        enhanced = image.copy()
        
        for enhancement_type in request.enhancement_types:
            try:
                if enhancement_type == EnhancementType.REMOVE_BRANDING:
                    branding_elements = await self.branding_detector.detect_branding(enhanced)
                    enhanced = await self.branding_detector.remove_branding(enhanced, branding_elements)
                
                elif enhancement_type == EnhancementType.ENHANCE_QUALITY:
                    enhanced = await self.enhancer.enhance_quality(enhanced, request.quality_settings)
                
                elif enhancement_type == EnhancementType.REMOVE_BACKGROUND:
                    # Use rembg library for background removal
                    enhanced_bytes = await self._image_to_bytes(enhanced)
                    no_bg_bytes = remove(enhanced_bytes)
                    enhanced = Image.open(io.BytesIO(no_bg_bytes))
                
                elif enhancement_type == EnhancementType.COLOR_CORRECTION:
                    enhanced = await self.enhancer.correct_colors(enhanced)
                
                elif enhancement_type == EnhancementType.UPSCALE:
                    enhanced = await self.enhancer.upscale_image(enhanced, 2.0)
                
                elif enhancement_type == EnhancementType.ADD_WATERMARK:
                    enhanced = await self.watermark_processor.add_watermark(
                        enhanced, request.watermark_config
                    )
                
            except Exception as e:
                logger.error(f"Error applying enhancement {enhancement_type}: {e}")
                continue
        
        return enhanced
    
    async def _finalize_image(self, image: Image.Image, variant: str, 
                            output_format: ImageFormat,
                            request: EnhancementRequest) -> Optional[EnhancedImage]:
        """Finalize image with optimization and upload"""
        
        try:
            processing_start = datetime.utcnow()
            
            # Optimize for web
            image_bytes, stats = await self.optimizer.optimize_for_web(image, output_format)
            
            # Upload to storage (mock implementation)
            image_url = await self._upload_image(image_bytes, request.product_id, variant, output_format)
            
            processing_time = (datetime.utcnow() - processing_start).total_seconds()
            
            return EnhancedImage(
                variant=variant,
                url=image_url,
                format=output_format,
                dimensions=ImageDimensions(image.width, image.height),
                file_size_kb=int(stats["size_kb"]),
                enhancements_applied=request.enhancement_types,
                quality_score=85.0,  # Mock score - would be calculated based on actual metrics
                processing_time_seconds=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error finalizing image: {e}")
            return None
    
    async def _upload_image(self, image_bytes: bytes, product_id: str, 
                          variant: str, format: ImageFormat) -> str:
        """Upload image to storage service"""
        
        # Mock implementation - replace with actual storage service
        filename = f"{product_id}_{variant}_{int(datetime.utcnow().timestamp())}.{format.value}"
        
        # In production, this would upload to S3, Google Cloud Storage, etc.
        mock_url = f"https://cdn.coreldove.com/images/{filename}"
        
        logger.info(f"Mock upload: {len(image_bytes)} bytes to {mock_url}")
        
        return mock_url
    
    async def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes"""
        
        output = io.BytesIO()
        format_str = "PNG" if image.mode == "RGBA" else "JPEG"
        image.save(output, format=format_str, quality=90)
        return output.getvalue()
    
    async def _calculate_quality_metrics(self, enhanced_images: Dict[str, List[EnhancedImage]]) -> Dict[str, float]:
        """Calculate overall quality metrics"""
        
        total_quality = 0.0
        total_images = 0
        
        for variant_images in enhanced_images.values():
            for enhanced_image in variant_images:
                total_quality += enhanced_image.quality_score
                total_images += 1
        
        avg_quality = total_quality / total_images if total_images > 0 else 0.0
        
        return {
            "average_quality_score": round(avg_quality, 2),
            "total_variants_created": total_images,
            "enhancement_success_rate": 95.0  # Mock value
        }
    
    def _calculate_processing_cost(self, stats: Dict[str, Any], total_size_bytes: int) -> float:
        """Calculate processing cost based on usage"""
        
        # Mock cost calculation - replace with actual pricing
        base_cost = 0.01  # $0.01 per image
        size_cost = (total_size_bytes / (1024 * 1024)) * 0.001  # $0.001 per MB
        
        total_cost = (stats["total_images_processed"] * base_cost) + size_cost
        
        return round(total_cost, 4)

# Usage example
async def enhance_product_images_example():
    """Example usage of the image enhancement pipeline"""
    
    # Sample image URLs
    image_urls = [
        "https://example.com/product1.jpg",
        "https://example.com/product2.jpg"
    ]
    
    # Create enhancement request
    request = EnhancementRequest(
        product_id="prod_123",
        image_urls=image_urls,
        enhancement_types=[
            EnhancementType.REMOVE_BRANDING,
            EnhancementType.ENHANCE_QUALITY,
            EnhancementType.OPTIMIZE_SIZE,
            EnhancementType.ADD_WATERMARK
        ],
        output_formats=[ImageFormat.JPG, ImageFormat.WEBP],
        target_dimensions={
            "main": ImageDimensions(1000, 1000),
            "thumbnail": ImageDimensions(300, 300),
            "mobile": ImageDimensions(600, 600)
        },
        watermark_config={
            "text": "CoreLDove",
            "position": "bottom_right",
            "opacity": 0.2
        }
    )
    
    # Process images
    pipeline = ImageEnhancementPipeline()
    result = await pipeline.process_images(request)
    
    print(f"Enhanced {result.processing_stats['total_images_processed']} images")
    print(f"Created {len(result.enhanced_images)} variants")
    print(f"Total processing time: {result.total_processing_time_seconds:.2f}s")
    print(f"Storage used: {result.storage_used_mb:.2f} MB")
    print(f"Cost: ${result.cost_usd:.4f}")

if __name__ == "__main__":
    asyncio.run(enhance_product_images_example())