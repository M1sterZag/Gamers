import {defineStore} from 'pinia';
import api from '../api';
import {ref} from 'vue';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    const isAuthenticated = ref(false);

    async function fetchUser() {
        try {
            const response = await api.get('/api/auth/me');
            user.value = response.data;
            isAuthenticated.value = true;
        } catch (error) {
            user.value = null;
            isAuthenticated.value = false;
        }
    }

    async function login(email, password) {
        await api.post('/api/auth/login', {email, password});
        await fetchUser();
    }

    async function logout() {
        await api.post('/api/auth/logout');
        user.value = null;
        isAuthenticated.value = false;
    }

    async function checkAuth() {
        await fetchUser();
    }

    async function register(email, username, password, confirmPassword) {
        try {
            const response = await api.post('/api/auth/register', {
                email,
                username,
                password,
                confirm_password: confirmPassword
            });
        } catch (error) {
            throw error;
        }
    }

    return {
        user,
        isAuthenticated,
        login,
        logout,
        checkAuth,
        register,
        fetchUser
    };
});