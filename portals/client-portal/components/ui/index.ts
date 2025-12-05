// Re-export all UI components for easier imports
export { Button } from './button'
export { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './card'
export { Badge } from './badge'
export { Input } from './input'

// Simple placeholder components for missing UI elements
import * as React from "react"
import { cn } from "@/lib/utils"

// Label component
export const Label = React.forwardRef<
  HTMLLabelElement,
  React.LabelHTMLAttributes<HTMLLabelElement>
>(({ className, ...props }, ref) => (
  <label
    ref={ref}
    className={cn("text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70", className)}
    {...props}
  />
))
Label.displayName = "Label"

// Checkbox component
export const Checkbox = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input
    type="checkbox"
    ref={ref}
    className={cn("h-4 w-4 rounded border border-gray-300", className)}
    {...props}
  />
))
Checkbox.displayName = "Checkbox"

// Separator component
export const Separator = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("border-b border-gray-200", className)} {...props} />
)

// Textarea component
export const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.TextareaHTMLAttributes<HTMLTextAreaElement>
>(({ className, ...props }, ref) => (
  <textarea
    ref={ref}
    className={cn("w-full rounded-md border border-gray-300 px-3 py-2", className)}
    {...props}
  />
))
Textarea.displayName = "Textarea"

// Simple Select components
export const Select = ({ children }: { children: React.ReactNode }) => <div>{children}</div>
export const SelectContent = ({ children }: { children: React.ReactNode }) => <div>{children}</div>
export const SelectItem = ({ children, value }: { children: React.ReactNode; value: string }) => <option value={value}>{children}</option>
export const SelectTrigger = ({ children }: { children: React.ReactNode }) => <div>{children}</div>
export const SelectValue = ({ placeholder }: { placeholder?: string }) => <span>{placeholder}</span>

// Simple Tabs components
export const Tabs = ({ children }: { children: React.ReactNode }) => <div>{children}</div>
export const TabsContent = ({ children }: { children: React.ReactNode }) => <div>{children}</div>
export const TabsList = ({ children }: { children: React.ReactNode }) => <div className="flex space-x-2">{children}</div>
export const TabsTrigger = ({ children }: { children: React.ReactNode }) => <button className="px-4 py-2 border rounded">{children}</button>

// Simple RadioGroup components
export const RadioGroup = ({ children }: { children: React.ReactNode }) => <div>{children}</div>
export const RadioGroupItem = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ ...props }, ref) => (
  <input type="radio" ref={ref} className="h-4 w-4" {...props} />
))
RadioGroupItem.displayName = "RadioGroupItem"