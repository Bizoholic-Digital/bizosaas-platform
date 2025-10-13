"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Minus, Plus } from "lucide-react"

interface ProductQuantityControlProps {
  quantity: number
  onQuantityChange: (quantity: number) => void
  maxQuantity?: number
  minQuantity?: number
  disabled?: boolean
  className?: string
}

export function ProductQuantityControl({
  quantity,
  onQuantityChange,
  maxQuantity = 99,
  minQuantity = 1,
  disabled = false,
  className
}: ProductQuantityControlProps) {
  const handleDecrease = () => {
    if (quantity > minQuantity) {
      onQuantityChange(quantity - 1)
    }
  }

  const handleIncrease = () => {
    if (quantity < maxQuantity) {
      onQuantityChange(quantity + 1)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value)
    if (!isNaN(value) && value >= minQuantity && value <= maxQuantity) {
      onQuantityChange(value)
    }
  }

  return (
    <div className={cn("flex items-center", className)}>
      <div className="flex items-center border border-gray-300 rounded-lg overflow-hidden">
        <Button
          variant="ghost"
          size="sm"
          className="px-3 py-2 hover:bg-red-50 hover:text-red-600 disabled:opacity-50"
          onClick={handleDecrease}
          disabled={disabled || quantity <= minQuantity}
          type="button"
        >
          <Minus className="h-4 w-4" />
        </Button>
        
        <Input
          type="number"
          value={quantity}
          onChange={handleInputChange}
          min={minQuantity}
          max={maxQuantity}
          disabled={disabled}
          className="w-16 text-center border-none focus:ring-0 focus:border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
        />
        
        <Button
          variant="ghost"
          size="sm"
          className="px-3 py-2 hover:bg-red-50 hover:text-red-600 disabled:opacity-50"
          onClick={handleIncrease}
          disabled={disabled || quantity >= maxQuantity}
          type="button"
        >
          <Plus className="h-4 w-4" />
        </Button>
      </div>
      
      {maxQuantity > 0 && quantity > 0 && (
        <span className="ml-3 text-sm text-gray-500">
          {maxQuantity <= 10 ? `Only ${maxQuantity} available` : `${maxQuantity} available`}
        </span>
      )}
    </div>
  )
}