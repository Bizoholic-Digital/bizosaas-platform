/**
 * Shimmer Button Component (Magic UI)
 * A button with a shimmer animation effect
 */

"use client"

import React from "react"
import { motion } from "framer-motion"
import { cn } from "../utils/cn"

export interface ShimmerButtonProps {
  children?: React.ReactNode
  className?: string
  shimmerColor?: string
  shimmerSize?: string
  borderRadius?: string
  shimmerDuration?: string
  background?: string
  onClick?: () => void
}

export function ShimmerButton({
  children,
  className,
  shimmerColor = "#ffffff",
  shimmerSize = "0.05em",
  borderRadius = "100px",
  shimmerDuration = "3s",
  background = "rgba(0, 0, 0, 1)",
  onClick,
}: ShimmerButtonProps) {
  return (
    <motion.button
      onClick={onClick}
      className={cn(
        "group relative overflow-hidden px-6 py-2 transition-transform active:scale-95",
        className
      )}
      style={{
        borderRadius,
        background,
      }}
      initial={{ "--x": "100%" } as any}
      animate={{ "--x": "-100%" } as any}
      whileTap={{ scale: 0.97 }}
      transition={{
        repeat: Infinity,
        repeatType: "loop",
        repeatDelay: 1,
        type: "spring",
        stiffness: 20,
        damping: 15,
        mass: 2,
        scale: {
          type: "spring",
          stiffness: 200,
          damping: 5,
          mass: 0.5,
        },
      }}
    >
      <span
        className={cn(
          "relative block h-full w-full text-sm uppercase tracking-wide",
          "text-neutral-100 dark:text-neutral-100"
        )}
        style={{
          maskImage: `linear-gradient(-75deg, ${shimmerColor} calc(var(--x) + 20%), transparent calc(var(--x) + 30%), ${shimmerColor} calc(var(--x) + 100%))`,
        }}
      >
        {children}
      </span>
      <span
        style={{
          mask: "linear-gradient(rgb(0,0,0), rgb(0,0,0)) content-box,linear-gradient(rgb(0,0,0), rgb(0,0,0))",
          maskComposite: "exclude",
        }}
        className="absolute inset-0 z-10 block rounded-[inherit] bg-[linear-gradient(-75deg,rgba(255,255,255,0.1)_calc(var(--x)+20%),rgba(255,255,255,0.5)_calc(var(--x)+25%),rgba(255,255,255,0.1)_calc(var(--x)+100%))] p-px"
      />
    </motion.button>
  )
}
