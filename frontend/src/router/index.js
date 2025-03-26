import {createRouter, createWebHistory} from 'vue-router';
import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegistrationPage from '../views/RegistrationPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import TeamsPage from '../views/TeamsPage.vue';
import ChatsPage from '../views/ChatsPage.vue';
import PremiumPage from '../views/PremiumPage.vue';
import Layout from '../components/Layout.vue';
import {useAuthStore} from '../stores/auth';

const routes = [
    {
        path: '/register',
        name: 'Register',
        component: RegistrationPage,
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage,
    },
    {
        path: '/',
        component: Layout, // Обёртка с сайдбаром
        children: [
            {
                path: '',
                name: 'Home',
                component: HomePage,
            },
            {
                path: '/teams',
                name: 'Teams',
                component: TeamsPage,
                meta: {requiresAuth: true}, // Требуется авторизация
            },
            {
                path: '/chats',
                name: 'Chats',
                component: ChatsPage,
                meta: {requiresAuth: true}, // Требуется авторизация
            },
            {
                path: '/profile',
                name: 'Profile',
                component: ProfilePage,
                meta: {requiresAuth: true}, // Требуется авторизация
            },
            {
                path: '/premium',
                name: 'Premium',
                component: PremiumPage,
                meta: {requiresAuth: true}, // Требуется авторизация
            },
            {
                path: '/create-team',
                name: 'CreateTeam',
                component: TeamsPage, // Предполагаю, что создание команды — это часть TeamsPage
                meta: {requiresAuth: true}, // Требуется авторизация
            },
        ],
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();
    await authStore.checkAuth(); // Проверяем авторизацию

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login'); // Неавторизованных на защищённые маршруты перенаправляем на логин
    } else if (['/login', '/register'].includes(to.path) && authStore.isAuthenticated) {
        next('/'); // Авторизованных с логина/регистрации перенаправляем на главную
    } else {
        next(); // Разрешаем переход
    }
});

export default router;