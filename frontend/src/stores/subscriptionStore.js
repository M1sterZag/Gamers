// stores/subscriptionStore.js
import {defineStore} from 'pinia';
import api from '../api';

export const useSubscriptionStore = defineStore('subscription', {
    state: () => ({
        subscriptions: [],
        currentSubscriptionId: null,
    }),
    actions: {
        setSubscriptions(subs) {
            this.subscriptions = subs;
        },
        setCurrentSubscriptionId(id) {
            this.currentSubscriptionId = id;
        },
        async checkCurrentSubscription() {
            try {
                const response = await api.get('/api/subscriptions/check_subscription');
                this.setCurrentSubscriptionId(response.data?.id || null);
            } catch (error) {
                console.error('Ошибка проверки подписки:', error);
                this.setCurrentSubscriptionId(null);
            }
        },
    },
    getters: {
        getSubscriptionById: (state) => (id) => {
            return state.subscriptions.find(sub => sub.id === id);
        }
    }
});