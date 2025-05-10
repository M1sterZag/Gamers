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

    return {
        user,
        isAuthenticated,
        login,
        logout,
        checkAuth,
        fetchUser
    };
});