/**
 * BizOSaaS Design System
 * Main entry point for the shared design system
 */

// Components
export * from './components'

// Design Tokens
export * from './tokens'

// Utilities
export * from './utils/cn'

// Styles (for CSS imports)
export const styles = {
  globals: './styles/globals.css',
  components: './styles/components.css',
}

// Version
export const version = '1.0.0'

// Theme configuration
export const themeConfig = {
  darkMode: 'class',
  prefix: '',
  separator: ':',
}

export default {
  version,
  themeConfig,
  styles,
}