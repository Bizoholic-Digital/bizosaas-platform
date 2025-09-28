"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu"
import { toast } from "sonner"
import { SaleorProduct } from "@/lib/saleor-api"
import { cn } from "@/lib/utils"
import { 
  Share2, 
  Facebook, 
  Twitter, 
  Link as LinkIcon, 
  Mail, 
  MessageCircle,
  Copy,
  CheckCircle
} from "lucide-react"

interface ProductShareButtonsProps {
  product: SaleorProduct
  currentUrl: string
  className?: string
}

export function ProductShareButtons({ product, currentUrl, className }: ProductShareButtonsProps) {
  const [copied, setCopied] = useState(false)
  
  const shareData = {
    title: product.name,
    text: product.description || `Check out ${product.name} on CoreLDove`,
    url: currentUrl,
    image: product.thumbnail?.url || product.media?.[0]?.url || ''
  }
  
  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(currentUrl)
      setCopied(true)
      toast.success('Link copied to clipboard!')
      
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy link:', error)
      toast.error('Failed to copy link')
    }
  }
  
  const handleNativeShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share(shareData)
      } catch (error) {
        if ((error as Error).name !== 'AbortError') {
          console.error('Failed to share:', error)
        }
      }
    }
  }
  
  const shareLinks = {
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(currentUrl)}`,
    twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(currentUrl)}&text=${encodeURIComponent(shareData.text)}`,
    whatsapp: `https://wa.me/?text=${encodeURIComponent(`${shareData.text} ${currentUrl}`)}`,
    email: `mailto:?subject=${encodeURIComponent(shareData.title)}&body=${encodeURIComponent(`${shareData.text}\n\n${currentUrl}`)}`
  }
  
  const openShareWindow = (url: string) => {
    window.open(url, 'share-window', 'width=600,height=400,scrollbars=yes,resizable=yes')
  }
  
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
        Share:
      </span>
      
      {/* Native Share (Mobile) */}
      {typeof navigator !== 'undefined' && 'share' in navigator && (
        <Button
          variant="outline"
          size="sm"
          onClick={handleNativeShare}
          className="border-red-200 hover:border-red-300 hover:text-red-600"
        >
          <Share2 className="h-4 w-4" />
        </Button>
      )}
      
      {/* Social Share Buttons */}
      <div className="flex items-center gap-1">
        <Button
          variant="outline"
          size="sm"
          onClick={() => openShareWindow(shareLinks.facebook)}
          className="border-blue-200 hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50"
          title="Share on Facebook"
        >
          <Facebook className="h-4 w-4" />
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => openShareWindow(shareLinks.twitter)}
          className="border-sky-200 hover:border-sky-300 hover:text-sky-600 hover:bg-sky-50"
          title="Share on Twitter"
        >
          <Twitter className="h-4 w-4" />
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => openShareWindow(shareLinks.whatsapp)}
          className="border-green-200 hover:border-green-300 hover:text-green-600 hover:bg-green-50"
          title="Share on WhatsApp"
        >
          <MessageCircle className="h-4 w-4" />
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => window.location.href = shareLinks.email}
          className="border-gray-200 hover:border-gray-300 hover:text-gray-600 hover:bg-gray-50"
          title="Share via Email"
        >
          <Mail className="h-4 w-4" />
        </Button>
      </div>
      
      {/* Copy Link Button */}
      <Button
        variant="outline"
        size="sm"
        onClick={handleCopyLink}
        className={cn(
          "border-red-200 hover:border-red-300 hover:text-red-600 hover:bg-red-50 transition-all",
          copied && "border-green-300 text-green-600 bg-green-50"
        )}
        title="Copy Link"
      >
        {copied ? (
          <CheckCircle className="h-4 w-4" />
        ) : (
          <Copy className="h-4 w-4" />
        )}
      </Button>
      
      {/* More Options Dropdown */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="outline"
            size="sm"
            className="border-gray-200 hover:border-gray-300 hover:text-gray-600"
          >
            <Share2 className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-48">
          <DropdownMenuItem 
            onClick={() => openShareWindow(shareLinks.facebook)}
            className="cursor-pointer"
          >
            <Facebook className="h-4 w-4 mr-2" />
            Facebook
          </DropdownMenuItem>
          <DropdownMenuItem 
            onClick={() => openShareWindow(shareLinks.twitter)}
            className="cursor-pointer"
          >
            <Twitter className="h-4 w-4 mr-2" />
            Twitter
          </DropdownMenuItem>
          <DropdownMenuItem 
            onClick={() => openShareWindow(shareLinks.whatsapp)}
            className="cursor-pointer"
          >
            <MessageCircle className="h-4 w-4 mr-2" />
            WhatsApp
          </DropdownMenuItem>
          <DropdownMenuItem 
            onClick={() => window.location.href = shareLinks.email}
            className="cursor-pointer"
          >
            <Mail className="h-4 w-4 mr-2" />
            Email
          </DropdownMenuItem>
          <DropdownMenuItem 
            onClick={handleCopyLink}
            className="cursor-pointer"
          >
            <LinkIcon className="h-4 w-4 mr-2" />
            Copy Link
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}