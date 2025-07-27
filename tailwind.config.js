/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./templates/**/*.j2",
    "./templates/**/*.jinja",
    "./templates/**/*.jinja2",
    "./static/**/*.js",
    "./app.py",
  ],
  safelist: [
    'dark',
    'text-white',
    'bg-white',
    'bg-dark',
    'bg-dark-800',
    'bg-dark-700',
    'bg-dark-600',
    'text-primary',
    'text-secondary',
    'bg-primary',
    'bg-secondary',
    'shadow-glow',
    'shadow-glow-blue',
    'animate-float',
    'animate-pulse-slow'
  ],
  theme: {
    extend: {
      colors: {
        'dark': '#0e0e12',
        'primary': '#00ff9d',
        'secondary': '#00d1ff',
        'accent': '#7b61ff',
        'dark-800': '#1a1a1f',
        'dark-700': '#2a2a32',
        'dark-600': '#3a3a45',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
        'display': ['Space Grotesk', 'sans-serif'],
        'mono': ['Fira Code', 'monospace']
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      },
      boxShadow: {
        'glow': '0 0 15px rgba(0, 255, 157, 0.5)',
        'glow-blue': '0 0 15px rgba(0, 209, 255, 0.5)',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
}
