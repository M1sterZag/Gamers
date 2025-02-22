import {createRouter, createWebHistory} from 'vue-router'
import RegistrationPage from '@/views/RegistrationPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import HomePage from '@/views/HomePage.vue'
import Layout from "@/components/Layout.vue";

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
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
