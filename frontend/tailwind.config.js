/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg:     '#05070f',
        bg1:    '#080c18',
        bg2:    '#0c1220',
        bg3:    '#101828',
        acc:    '#5b9fff',
        grn:    '#2dd4a4',
        ora:    '#f5834a',
        pur:    '#9d78f5',
        pnk:    '#e8689a',
        yel:    '#f5c842',
        t0:     '#f4f8ff',
        t1:     '#a0b4d0',
        t2:     '#566880',
        t3:     '#2d3a4a',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-up':    'fadeUp 0.4s ease forwards',
      },
      keyframes: {
        fadeUp: {
          '0%':   { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
