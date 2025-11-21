import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Utility function to merge Tailwind CSS classes with proper conflict resolution
 * Combines clsx for conditional classes and tailwind-merge for deduplication
 *
 * @param inputs - Array of class values (strings, objects, arrays)
 * @returns Merged class string with conflicts resolved
 *
 * @example
 * cn('px-2 py-1', 'px-4') // Returns 'py-1 px-4' (px-2 is overridden)
 * cn('text-red-500', { 'text-blue-500': isBlue }) // Conditional classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Variant-based class name generator for component styling
 * Provides a type-safe way to create component variants
 */
export { cva, type VariantProps } from "class-variance-authority"

/**
 * Focus ring utility for accessibility
 * Consistent focus styles across all components
 */
export const focusRing = 'focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2'

/**
 * Animation utilities for consistent transitions
 */
export const transitions = {
  fast: 'transition-all duration-150 ease-in-out',
  normal: 'transition-all duration-200 ease-in-out',
  slow: 'transition-all duration-300 ease-in-out',
  bounce: 'transition-all duration-200 ease-bounce',
}

/**
 * Common layout utilities
 */
export const layouts = {
  flexCenter: 'flex items-center justify-center',
  flexBetween: 'flex items-center justify-between',
  flexStart: 'flex items-center justify-start',
  flexEnd: 'flex items-center justify-end',
  flexCol: 'flex flex-col',
  flexColCenter: 'flex flex-col items-center justify-center',
}

/**
 * Responsive grid utilities
 */
export const grids = {
  responsive: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4',
  auto: 'grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]',
  dense: 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 grid-flow-dense',
}

/**
 * Typography utilities for consistent text styling
 */
export const typography = {
  h1: 'scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl',
  h2: 'scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0',
  h3: 'scroll-m-20 text-2xl font-semibold tracking-tight',
  h4: 'scroll-m-20 text-xl font-semibold tracking-tight',
  p: 'leading-7 [&:not(:first-child)]:mt-6',
  blockquote: 'mt-6 border-l-2 pl-6 italic',
  code: 'relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold',
  lead: 'text-xl text-muted-foreground',
  large: 'text-lg font-semibold',
  small: 'text-sm font-medium leading-none',
  muted: 'text-sm text-muted-foreground',
}

/**
 * Border utilities for consistent styling
 */
export const borders = {
  subtle: 'border border-border',
  emphasis: 'border-2 border-primary',
  dashed: 'border border-dashed border-border',
  none: 'border-0',
}

/**
 * Shadow utilities for depth and elevation
 */
export const shadows = {
  card: 'shadow-sm',
  elevated: 'shadow-md',
  floating: 'shadow-lg',
  overlay: 'shadow-xl',
}

/**
 * Interactive state utilities
 */
export const interactive = {
  hover: 'hover:bg-accent hover:text-accent-foreground',
  active: 'active:scale-95',
  disabled: 'disabled:pointer-events-none disabled:opacity-50',
  clickable: 'cursor-pointer',
}

/**
 * Container utilities for consistent spacing
 */
export const containers = {
  page: 'container mx-auto px-4 sm:px-6 lg:px-8',
  section: 'py-12 lg:py-16',
  card: 'rounded-lg border bg-card p-6 shadow-sm',
  dialog: 'fixed inset-0 z-50 bg-background/80 backdrop-blur-sm',
}