import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ["var(--font-space-grotesk)"],
        body: ["var(--font-manrope)"]
      },
      colors: {
        brand: {
          50: "#edf7f5",
          100: "#d4ede8",
          200: "#a9dbd1",
          300: "#73c1b1",
          400: "#469d91",
          500: "#2e7f74",
          600: "#23645d",
          700: "#1f504b",
          800: "#1d3f3c",
          900: "#1a3634"
        }
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(14px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        }
      },
      animation: {
        "fade-up": "fade-up 500ms ease-out"
      }
    }
  },
  plugins: []
};

export default config;

