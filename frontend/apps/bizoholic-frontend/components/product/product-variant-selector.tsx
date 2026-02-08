"use client"

import { useState } from "react"
import { SaleorProductVariant, SaleorAttribute } from "@/lib/saleor-api"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { CheckCircle, AlertCircle } from "lucide-react"

interface ProductVariantSelectorProps {
  variants: SaleorProductVariant[]
  selectedVariant: SaleorProductVariant | null
  onVariantChange: (variant: SaleorProductVariant) => void
  options: SaleorAttribute[]
  className?: string
}

export function ProductVariantSelector({
  variants,
  selectedVariant,
  onVariantChange,
  options,
  className
}: ProductVariantSelectorProps) {
  // Simplified variant selector - just show available variants
  if (!variants || variants.length <= 1) {
    return null
  }

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-lg">Select Variant</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 gap-3">
          {variants.map((variant, index) => {
            const isSelected = selectedVariant?.id === variant.id
            const isAvailable = (variant.quantityAvailable || 0) > 0
            
            return (
              <Button
                key={variant.id || index}
                variant={isSelected ? "default" : "outline"}
                className={cn(
                  "h-auto p-4 justify-start text-left",
                  !isAvailable && "opacity-50 cursor-not-allowed"
                )}
                onClick={() => isAvailable && onVariantChange(variant)}
                disabled={!isAvailable}
              >
                <div className="flex items-center justify-between w-full">
                  <div>
                    <div className="font-medium">
                      {variant.name || `Variant ${index + 1}`}
                    </div>
                    {variant.sku && (
                      <div className="text-sm text-gray-500">
                        SKU: {variant.sku}
                      </div>
                    )}
                  </div>
                  <div className="flex items-center space-x-2">
                    {variant.pricing?.price && (
                      <Badge variant="secondary">
                        ${variant.pricing.price.gross.amount}
                      </Badge>
                    )}
                    {isAvailable ? (
                      <CheckCircle className="h-4 w-4 text-green-500" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-red-500" />
                    )}
                  </div>
                </div>
              </Button>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}