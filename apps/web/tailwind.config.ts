import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0D1117",
        surface: "#161B22",
        border: "#21262D",
        primary: "#E6EDF3",
        muted: "#8B949E",
        accent: "#1F6FEB",
        danger: "#F85149",
        warning: "#E3B341",
        success: "#3FB950",
        alert: "#F0883E",
      },
    },
  },
  plugins: [],
};
export default config;