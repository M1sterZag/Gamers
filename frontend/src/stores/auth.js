import {defineStore} from 'pinia';
import api from '../api';
import {ref} from 'vue';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    const isAuthenticated = ref(false);
    const accessToken = ref(null);
    const refreshToken = ref(null);

    function setTokens(access, refresh) {
        accessToken.value = access;
        refreshToken.value = refresh;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    }

    function clearTokens() {
        accessToken.value = null;
        refreshToken.value = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        delete api.defaults.headers.common['Authorization'];
    }

    async function login(email, password) {
        try {
            const response = await api.post('/api/auth/login', {email, password});
            if (response.data.ok) {
                const access = localStorage.getItem('access_token');
                const refresh = localStorage.getItem('refresh_token');
                setTokens(access, refresh);
                await fetchUser();
                isAuthenticated.value = true;
            }
            return response.data;
        } catch (error) {
            clearTokens();
            throw error;
        }
    }

    async function register(email, username, password, confirmPassword) { // Добавляем confirmPassword
        try {
            const response = await api.post('/api/auth/register', {
                email,
                username,
                password,
                confirm_password: confirmPassword // Добавляем confirm_password
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async function logout() {
        try {
            await api.post('/api/auth/logout');
        } finally {
            clearTokens();
            user.value = null;
            isAuthenticated.value = false;
        }
    }

    async function fetchUser() {
        try {
            const response = await api.get('/api/auth/me');
            user.value = response.data;
            isAuthenticated.value = true;
        } catch (error) {
            clearTokens();
            user.value = null;
            isAuthenticated.value = false;
        }
    }

    async function refreshTokens() {
        try {
            const response = await api.post('/api/auth/refresh');
            const access = localStorage.getItem('access_token');
            const refresh = localStorage.getItem('refresh_token');
            setTokens(access, refresh);
            return response.data;
        } catch (error) {
            clearTokens();
            throw error;
        }
    }

    async function checkAuth() {
        const storedAccessToken = localStorage.getItem('access_token');
        const storedRefreshToken = localStorage.getItem('refresh_token');
        if (storedAccessToken && storedRefreshToken) {
            setTokens(storedAccessToken, storedRefreshToken);
            await fetchUser();
        }
    }

    return {
        user,
        isAuthenticated,
        accessToken,
        refreshToken,
        login,
        register,
        logout,
        fetchUser,
        refreshTokens,
        checkAuth,
    };
});