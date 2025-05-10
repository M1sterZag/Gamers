import {defineStore} from 'pinia';
import axios from 'axios';

export const useProfileStore = defineStore('profile', {
    state: () => ({
        profile: {
            nickname: '',
            avatar: null,
            aboutMe: '',
            recentCommands: [],
            recentFriends: []
        },
        loading: false,
        error: null
    }),

    actions: {
        async fetchProfile(userId) {
            this.loading = true;
            try {
                const response = await axios.get(`/api/profile/${userId}`);
                this.profile = response.data;
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },

        async updateProfile(profileData) {
            this.loading = true;
            try {
                const response = await axios.put('/api/profile', profileData);
                this.profile = response.data;
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },
    }
});