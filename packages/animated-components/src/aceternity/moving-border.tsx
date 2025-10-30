/**
 * Moving Border Button Component (Aceternity UI)
 * A button with an animated border effect
 */

"use client"

import React, { useRef, useState } from "react"
import { motion } from "framer-motion"
import { cn } from "../utils/cn"

export interface MovingBorderProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  borderRadius?: string
  containerClassName?: string
  borderClassName?: string
  duration?: number
  as?: React.ElementType
}

export function MovingBorder({
  children,
  borderRadius = "1.75rem",
  containerClassName,
  borderClassName,
  duration = 2000,
  className,
  as: Component = "button",
  ...otherProps
}: MovingBorderProps) {
  return (
    <Component
      className={cn(
        "relative bg-transparent p-[1px] overflow-hidden",
        containerClassName
      )}
      style={{
        borderRadius: borderRadius,
      }}
      {...otherProps}
    >
      <div
        className="absolute inset-0"
        style={{ borderRadius: `calc(${borderRadius} * 0.96)` }}
      >
        <motion.div
          className={cn(
            "h-[200%] w-[200%] absolute -left-1/2 -top-1/2",
            "bg-[conic-gradient(from_var(--border-angle),transparent_0%,#3b82f6_10%,transparent_20%)]",
            borderClassName
          )}
          style={{
            transformOrigin: "50% 50%",
          }}
          animate={{
            rotate: [0, 360],
          }}
          transition={{
            duration: duration / 1000,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      </div>

      <div
        className={cn(
          "relative bg-slate-900 flex items-center justify-center w-full h-full text-sm antialiased",
          className
        )}
        style={{
          borderRadius: `calc(${borderRadius} * 0.96)`,
        }}
      >
        {children}
      </div>
    </Component>
  )
}
