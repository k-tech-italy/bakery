// tailwind.config.js
// const colors = require('tailwindcss/colors');
const defaultTheme = require('tailwindcss/defaultTheme');
const colors = require('tailwindcss/colors');
const plugin = require('tailwindcss/plugin')

const orange = {
    50: '#fff7ed',
    100: '#ffedd5',
    200: '#fed7aa',
    // 300: '#fdba74',
    300: '#FF9933',
    400: '#fb923c',
    500: '#f97316',
    600: '#ea580c',
    700: '#c2410c',
    800: '#9a3412',
    900: '#7c2d12',
};

const bob = {
    DEFAULT: "#00a8b5",
    primary: "#00a8b5",
    secondary: "#59add4",
    orange: '#FF6B18',
    azure: '#59ADE6',
    blu: '#00354e',
    fuchsia: '#dc0d7a',
    green: '#58947a',
    yellow: '#caa61b',
    red: '#cd2d25',
};

const accent = {
    DEFAULT: '#11AAE9',
};
const BOB_COLORS ={
    bob: bob,
    primary: "#00C1CC",
    secondary: "#6699CC",
    selected: "#00C1CC",
    orange: orange,
    accent: accent,
}
SAFE_COLORS = [];

Object.keys(BOB_COLORS.bob).forEach(function (key) {
    SAFE_COLORS.push(`bg-bob-${key}`);
    SAFE_COLORS.push(`text-bob-${key}`);
})

module.exports = {
    purge: {
        enabled: process.env.NODE_ENV === "production",
        content: ['./src/sos/**/templates/**/*.html',
                  './src/sos/**/email_templates/**/*.html',
                  './src/sos/web/assets/**/*.html'
        ],
        options: {
            safelist: {
                standard: SAFE_COLORS
            }
        }
    },
    darkMode: 'class', // or 'media' or 'class'
    corePlugins: {
        fontFamily: true,
    },
    theme: {
        screens: {
            'xs': '360px',
            'sm': '640px',
            'md': '768px',
            'lg': '1024px',
            'xl': '1280px',
            '2xl': '1536px',
            '3xl': '2000px',
        },
        extend: {
            // animation: {
            //     'balloon': 'bounce 1s linear animation-direction',
            // },
            keyframes: {
                'fade-in-down': {
                    '0%': {
                        opacity: '0',
                        transform: 'translateY(-10px)'
                    },
                    '100%': {
                        opacity: '1',
                        transform: 'translateY(0)'
                    },
                }
            },
            animation: {
                'fade-in-down': 'fade-in-down 0.5s ease-out'
            },
            margin: {
                '-18': '-4.5rem',
                '18': '4.5rem',
            },
            width: {
                '1/8': '12.5%',
                '2/8': '25%',
                '3/8': '37.5%',
                '4/8': '50%',
                '5/8': '62.5%',
                '6/8': '75%',
                '7/8': '87.5%',
            },
            colors: BOB_COLORS,
        },
        fontSize: {
            'xxs': '.50rem',
            'xs': '.75rem',
            'sm': '.8rem',
            'tiny': '.875rem',
            'base': '1rem',
            'lg': '1.125rem',
            'xl': '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem',
            '5xl': '3rem',
            '6xl': '4rem',
            '7xl': '5rem',
        },
        fontFamily: {
            sans: ['Capriola', 'system-ui', '-apple-system', 'BlinkMacSystemFont',],
            open: ['"Open Sans"', 'sans-serif'],
            mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', "Liberation Mono",
                '"Courier New"', "monospace"],
            code: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', "Liberation Mono",
                '"Courier New"', "monospace"]
        },
        borderRadius: {
            'none': '0',
            'sm': '0.125rem',
            DEFAULT: '0.25rem',
            'md': '0.375rem',
            'lg': '0.5rem',
            'xl ': '12px',
            '2xl': '20px',
            '3xl': '40px',
            'full': '9999px',

            'xlarge': '20px',
            'xxl': '40px'
        },
    },
    variants: {
        extend: {
            opacity: ['disabled'],
            cursor: ['hover', 'focus', 'disabled'],
        }
    },
    plugins: [
        plugin(function({ addUtilities }){
            const newUtilities = {
                '.safe-top' : {
                    paddingTop: 'constant(safe-area-inset-top)',
                    paddingTop: 'env(safe-area-inset-top)'
                },
                '.safe-left' : {
                    paddingLeft: 'constant(safe-area-inset-left)',
                    paddingLeft: 'env(safe-area-inset-left)'
                },
                '.safe-right' : {
                    paddingRight: 'constant(safe-area-inset-right)',
                    paddingRight: 'env(safe-area-inset-right)'
                },
                '.safe-bottom' : {
                    paddingBottom: 'constant(safe-area-inset-bottom)',
                    paddingBottom: 'env(safe-area-inset-bottom)'
                }
            }

            addUtilities( newUtilities );
        })
    ],
};
