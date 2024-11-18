import react from '@vitejs/plugin-react';
import {defineConfig, loadEnv} from 'vite';


const ENVIRONMNET_PREFIX = 'REACT_APP';


// https://vitejs.dev/config/
export default defineConfig(({mode}) => {
    const clientEnv = loadEnv(mode, process.cwd(), ENVIRONMNET_PREFIX);

    return {
        server:{
            cors:false
        },
        plugins: [react()],
        define: {
            'process.env': clientEnv,
        },
        build: {
            outDir: "dist"
        },
        root: './',
        base: '',
        sourcemap: false,
        minify: true
    };
});
