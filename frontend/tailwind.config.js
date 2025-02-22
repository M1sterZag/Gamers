/** @type {import('tailwindcss').Config} */

import defaultTheme from 'tailwindcss/defaultTheme';

export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {
            colors: {
                fon: "#111214",
                primary: "#8244FF",
                primary_hover: "#8E5FEC",
                secondary: "#1B1C1E",
                accent: "#50FA7B",
                accent_hover: "#2AE359",
                text: "#E8D8C9",
            },
            fontFamily: {
                montserrat: ["Montserrat", "sans-serif"],
                sans: ['Montserrat', ...defaultTheme.fontFamily.sans],
            },
            fontSize: {
                s48: "48px",
                s32: "32px",
                s20: "20px",
                s16: "16px",
                s12: "12px"
            },
            borderRadius: {
                brs: "8px",
            },
        },
    },
    plugins: [],
};
