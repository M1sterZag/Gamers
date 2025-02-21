/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        extend: {
            colors: {
                fon: "#111214",
                primary: "#8244FF",
                primary_hover: "#8E5FEC",
                secondary: "#1B1C1E",
                accent: "#2AE359",
                accent_hover: "#50FA7B",
                text: "#E8D8C9",
            },
            fontFamily: {
                montserrat: ["Montserrat", "sans-serif"],
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
