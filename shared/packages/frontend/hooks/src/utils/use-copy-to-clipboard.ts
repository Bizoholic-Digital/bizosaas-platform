/**
 * useCopyToClipboard hook
 * Copies text to clipboard with status tracking
 */

import { useState, useCallback } from 'react'

export interface UseCopyToClipboardResult {
  copiedText: string | null
  copy: (text: string) => Promise<boolean>
  isCopied: boolean
}

export function useCopyToClipboard(): UseCopyToClipboardResult {
  const [copiedText, setCopiedText] = useState<string | null>(null)
  const [isCopied, setIsCopied] = useState(false)

  const copy = useCallback(async (text: string): Promise<boolean> => {
    if (!navigator?.clipboard) {
      console.warn('Clipboard not supported')
      return false
    }

    try {
      await navigator.clipboard.writeText(text)
      setCopiedText(text)
      setIsCopied(true)

      // Reset after 2 seconds
      setTimeout(() => {
        setIsCopied(false)
      }, 2000)

      return true
    } catch (error) {
      console.warn('Copy failed', error)
      setCopiedText(null)
      setIsCopied(false)
      return false
    }
  }, [])

  return { copiedText, copy, isCopied }
}
