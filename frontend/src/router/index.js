import {createRouter, createWebHistory} from 'vue-router';
import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import RegistrationPage from '../views/RegistrationPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import TeamsPage from '../views/TeamsPage.vue';
import TeamDetails from '../views/TeamDetails.vue';
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
        component: Layout,
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
                meta: {requiresAuth: true},
            },
            {
                path: '/team/:id',
                name: 'Team',
                component: TeamDetails,
                meta: {requiresAuth: true},
                props: true,
            },
            {
                path: '/profile',
                name: 'Profile',
                component: ProfilePage,
                meta: {requiresAuth: true},
            },
            {
                path: '/create-team',
                name: 'CreateTeam',
                component: TeamsPage,
                meta: {requiresAuth: true},
            },
            {
                path: '/premium',
                name: 'Premium',
                component: PremiumPage,
                meta: {requiresAuth: true},
            },
            {
                path: '/payment',
                name: 'Payment',
                component: () => import('../views/PaymentPage.vue'),
                meta: {requiresAuth: true},
            },
        ],
    },
    {
        path: '/admin',
        meta: {requiresAuth: true}, // Требуется авторизация
        children: [
            {
                path: '',
                name: 'AdminPanel',
                component: () => import('../views/AdminPanel.vue'), // Главная страница админ-панели
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

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login');
    } else if (to.path.startsWith('/admin') && !authStore.user?.is_admin) {
        next('/'); // Перенаправление обычных пользователей
    } else {
        next();
    }
});

export default router;