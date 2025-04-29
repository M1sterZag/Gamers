// stores/subscriptionStore.js
import {defineStore} from 'pinia';

export const useSubscriptionStore = defineStore('subscription', {
    state: () => ({
        subscriptions: [], // All available subscriptions
        currentSubscriptionId: null, // ID of the selected subscription
    }),
    actions: {
        setSubscriptions(subs) {
            this.subscriptions = subs;
        },
        setCurrentSubscriptionId(id) {
            this.currentSubscriptionId = id;
        },
        getSubscriptionById(id) {
            return this.subscriptions.find((sub) => sub.id === id);
        },
    },
});