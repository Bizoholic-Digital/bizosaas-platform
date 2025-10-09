/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        trading: {
          green: '#00D084',
          red: '#F7525F',
          blue: '#2962FF',
          dark: '#131722',
          chart: '#1E222D',
        },
      },
      animation: {
        'price-up': 'flash-green 0.5s ease-in-out',
        'price-down': 'flash-red 0.5s ease-in-out',
      },
      keyframes: {
        'flash-green': {
          '0%': { backgroundColor: 'transparent' },
          '50%': { backgroundColor: 'rgba(0, 208, 132, 0.2)' },
          '100%': { backgroundColor: 'transparent' },
        },
        'flash-red': {
          '0%': { backgroundColor: 'transparent' },
          '50%': { backgroundColor: 'rgba(247, 82, 95, 0.2)' },
          '100%': { backgroundColor: 'transparent' },
        },
      },
    },
  },
  plugins: [],
}