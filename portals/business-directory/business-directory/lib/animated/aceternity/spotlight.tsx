/**
 * Spotlight Component (Aceternity UI)
 * An animated spotlight effect that follows mouse movement
 */

"use client"

import React, { useEffect, useRef } from "react"
import { motion } from "framer-motion"
import { cn } from "../utils/cn"

export interface SpotlightProps {
  className?: string
  fill?: string
}

export function Spotlight({ className, fill = "white" }: SpotlightProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [position, setPosition] = React.useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      setPosition({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      })
    }

    const container = containerRef.current
    container?.addEventListener("mousemove", handleMouseMove)

    return () => {
      container?.removeEventListener("mousemove", handleMouseMove)
    }
  }, [])

  return (
    <div ref={containerRef} className={cn("relative h-full w-full", className)}>
      <motion.div
        className="pointer-events-none absolute z-50 h-[200px] w-[200px] rounded-full blur-3xl"
        style={{
          background: `radial-gradient(circle, ${fill} 0%, transparent 80%)`,
          left: position.x - 100,
          top: position.y - 100,
        }}
        animate={{
          left: position.x - 100,
          top: position.y - 100,
        }}
        transition={{
          type: "spring",
          stiffness: 150,
          damping: 15,
        }}
      />
    </div>
  )
}
