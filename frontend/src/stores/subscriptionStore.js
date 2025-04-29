// stores/subscriptionStore.js
import {defineStore} from 'pinia';
import api from '../api';

export const useSubscriptionStore = defineStore('subscription', {
    state: () => ({
        subscriptions: [], // Все доступные подписки
        currentSubscriptionId: null, // ID текущей активной подписки
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
});