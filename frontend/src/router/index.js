import {createRouter, createWebHistory} from 'vue-router'
import RegistrationPage from '@/views/RegistrationPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import HomePage from '@/views/HomePage.vue'
import Layout from "@/components/Layout.vue";
import TeamsPage from "@/views/TeamsPage.vue";
import ChatsPage from "@/views/ChatsPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import PremiumPage from "@/views/PremiumPage.vue";

const routes = [
    {
        path: '/register',
        name: 'Register',
        component: RegistrationPage
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginPage
    },
    {
        path: '/',
        component: Layout,
        children: [
            {
                path: '',
                name: 'Home',
                component: HomePage
            },
            {
                path: '/teams',
                name: 'Teams',
                component: TeamsPage
            },
            {
                path: '/chats',
                name: 'Chats',
                component: ChatsPage
            },
            {
                path: '/profile',
                name: 'Profile',
                component: ProfilePage
            },
            {
                path: '/premium',
                name: 'Premium',
                component: PremiumPage
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
