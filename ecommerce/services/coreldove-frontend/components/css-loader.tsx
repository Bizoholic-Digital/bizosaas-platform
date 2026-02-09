'use client'

import { useEffect } from 'react'

export function CSSLoader() {
  useEffect(() => {
    // Force CSS styles to be applied
    if (typeof window !== 'undefined') {
      const style = document.createElement('style')
      style.textContent = `
        /* Ensure Tailwind base styles are applied */
        body { 
          margin: 0; 
          font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; 
          antialiased: true;
        }
        * { box-sizing: border-box; }
        
        /* Force loading of critical CSS */
        .min-h-screen { min-height: 100vh !important; }
        .bg-gray-50 { background-color: #f9fafb !important; }
        .bg-white { background-color: #ffffff !important; }
        .shadow-sm { box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important; }
        .border { border: 1px solid #e5e7eb !important; }
        .rounded-lg { border-radius: 0.5rem !important; }
        .p-6 { padding: 1.5rem !important; }
        .text-gray-900 { color: #111827 !important; }
        .text-gray-600 { color: #4b5563 !important; }
        .font-bold { font-weight: 700 !important; }
        .font-semibold { font-weight: 600 !important; }
        .text-xl { font-size: 1.25rem !important; }
        .text-2xl { font-size: 1.5rem !important; }
        .mb-4 { margin-bottom: 1rem !important; }
        .mb-8 { margin-bottom: 2rem !important; }
        .grid { display: grid !important; }
        .gap-6 { gap: 1.5rem !important; }
        .flex { display: flex !important; }
        .items-center { align-items: center !important; }
        .justify-between { justify-content: space-between !important; }
      `
      document.head.appendChild(style)
      
      // Clean up
      return () => {
        document.head.removeChild(style)
      }
    }
  }, [])

  return null
}