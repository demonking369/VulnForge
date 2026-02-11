/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
    theme: {
        extend: {
            colors: {
                'neuro-bg': 'rgba(10, 12, 18, 1)',
                'neuro-surface': 'rgba(18, 22, 32, 1)',
                'neuro-border': 'rgba(45, 55, 72, 0.6)',
                'neuro-text-primary': 'rgba(226, 232, 240, 1)',
                'neuro-text-secondary': 'rgba(148, 163, 184, 1)',
                'neuro-text-muted': 'rgba(100, 116, 139, 1)',
            },
            animation: {
                'progress': 'progress 1.5s ease-in-out infinite',
                'shimmer': 'shimmer 2s linear infinite',
            },
            keyframes: {
                progress: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(100%)' },
                },
                shimmer: {
                    '0%': { transform: 'translateX(-200%)' },
                    '100%': { transform: 'translateX(200%)' },
                },
            },
        },
    },
    plugins: [],
};
