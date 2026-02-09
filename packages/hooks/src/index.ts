// API Hooks
export { useProjects, type UseProjectsOptions, type UseProjectsResult } from './api/use-projects'

// UI Hooks
export {
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
} from './ui/use-media-query'

export {
  useToast,
  type Toast,
  type ToastType,
  type UseToastResult,
} from './ui/use-toast'

// Utility Hooks
export { useDebounce } from './utils/use-debounce'
export { useLocalStorage } from './utils/use-local-storage'
export {
  useCopyToClipboard,
  type UseCopyToClipboardResult,
} from './utils/use-copy-to-clipboard'
