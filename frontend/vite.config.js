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
            // Для авторизации: /api/auth/register → http://localhost:8000/auth/register
            '/api/auth': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''), // Убираем /api, оставляем /auth
            },
            // Для всего остального: /api/teams → http://localhost:8000/teams
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''), // Убираем /api, оставляем остальной путь
            },
            '/ws': {
                target: 'ws://localhost:8000/ws/chats',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/ws/, ''),
            }
        },
    },
});