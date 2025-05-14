import {defineStore} from 'pinia';

export const useNotificationStore = defineStore('notification', {
    state: () => ({
        isVisible: false,
        type: 'success',
        message: '',
    }),
    actions: {
        showNotification(type, message) {
            this.type = type;
            this.message = message;
            this.isVisible = true;

            setTimeout(() => {
                this.hideNotification();
            }, 3000);
        },
        hideNotification() {
            this.isVisible = false;
        },
    },
});