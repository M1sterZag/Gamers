import {defineConfig} from 'vite';
import {fileURLToPath, URL} from 'url';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
    server: {
        proxy: {
            // api/teams → http://localhost:8000/teams | http://backend:8000/teams
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''), // Убираем /api, оставляем остальной путь
            },
            '/ws': {
                target: 'ws://localhost:8000/ws/chats',
                changeOrigin: true,
                ws: true,
                rewrite: (path) => path.replace(/^\/ws/, ''),
            }
        },
    },
});