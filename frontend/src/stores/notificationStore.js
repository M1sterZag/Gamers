// stores/notificationStore.js
import {defineStore} from 'pinia';

export const useNotificationStore = defineStore('notification', {
    state: () => ({
        isVisible: false,
        type: 'success', // 'success' или 'error'
        message: '',
    }),
    actions: {
        showNotification(type, message) {
            this.type = type;
            this.message = message;
            this.isVisible = true;

            // Автоматически скрыть через 3 секунды
            setTimeout(() => {
                this.hideNotification();
            }, 3000);
        },
        hideNotification() {
            this.isVisible = false;
        },
    },
});