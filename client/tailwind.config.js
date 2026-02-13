/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                game: {
                    bg: '#e0f2fe', // Sky blue-ish (Sky-100)
                    card: '#f3f4f6', // Grey-100
                    cardDark: '#d1d5db', // Grey-300
                    win: '#22c55e', // Green-500
                    lose: '#ef4444', // Red-500
                    fair: '#fcfcfc', // Almost white
                    button: '#4ade80', // Green-400
                    badge: {
                        fly: '#3b82f6', // Blue-500
                        ride: '#ec4899', // Pink-500
                        neon: '#84cc16', // Lime-500
                        mega: '#a855f7', // Purple-500
                    }
                }
            },
            boxShadow: {
                'neon-blue': '0 0 10px #00fff5, 0 0 20px #00fff5',
                'neon-pink': '0 0 10px #ff00ff, 0 0 20px #ff00ff',
            },
            fontFamily: {
                sans: ['Nunito', 'sans-serif'], // Rounder font for game feel
            }
        },
    },
    plugins: [],
}
