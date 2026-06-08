import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AnalysisView from '../views/AnalysisView.vue';
import DashboardView from '../views/DashboardView.vue';
import { useAnalysisStore } from "../stores/useAnalysisStore";
import { useAuthStore } from "../stores/useAuthStore";

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path:'/profile',
        name: 'profile',
        component: AnalysisView
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView,
        beforeEnter: (to, from, next) => {
            const store = useAnalysisStore();
            if (!store.hasResult && to.name !== 'profile') {
                next({name: 'profile'});
            } else {
                next();
            }
        }
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/signup',
        name: 'signup',
        component: () => import('../views/SignupView.vue')
    },
    {
        path: '/history',
        name: 'history',
        component: () => import('../views/HistoryView.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/saved',
        name: 'saved',
        component: () => import('../views/SavedProductsView.vue'),
        meta: { requiresAuth: true }
    }
]

const router =  createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0 };
    }
});

router.beforeEach(async (to) => {
    const auth = useAuthStore();

    if (auth.token && !auth.user) {
        try {
            await auth.hydrate();
        } catch (error) {
            if (to.meta.requiresAuth) {
                return { name: 'login' };
            }
        }
    }

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return { name: 'login' };
    }

    if ((to.name === 'login' || to.name === 'signup') && auth.isAuthenticated) {
        return { name: 'profile' };
    }
});

export default router;
