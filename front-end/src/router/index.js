import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AnalysisView from '../views/AnalysisView.vue';
import DashboardView from '../views/DashboardView.vue';
import { useAnalysisStore } from "../stores/useAnalysisStore";
import { useAuthStore } from "../stores/useAuthStore";
import { useLocaleStore } from "../stores/useLocaleStore";

const routes = [
    {
        path: '/:locale(id)?',
        name: 'home',
        component: HomeView
    },
    {
        path:'/:locale(id)?/profile',
        name: 'profile',
        component: AnalysisView
    },
    {
        path: '/:locale(id)?/dashboard',
        name: 'dashboard',
        component: DashboardView,
        beforeEnter: (to, from, next) => {
            const store = useAnalysisStore();
            if (!store.hasResult && to.name !== 'profile') {
                next({ name: 'profile', params: to.params });
            } else {
                next();
            }
        }
    },
    {
        path: '/:locale(id)?/login',
        name: 'login',
        component: () => import('../views/LoginView.vue')
    },
    {
        path: '/:locale(id)?/signup',
        name: 'signup',
        component: () => import('../views/SignupView.vue')
    },
    {
        path: '/:locale(id)?/history',
        name: 'history',
        component: () => import('../views/HistoryView.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/:locale(id)?/saved',
        name: 'saved',
        component: () => import('../views/SavedProductsView.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/'
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
    const locale = useLocaleStore();

    locale.applyRouteLocale(to.params.locale);

    if (auth.token && !auth.user) {
        try {
            await auth.hydrate();
        } catch (error) {
            if (to.meta.requiresAuth) {
                return { name: 'login', params: to.params };
            }
        }
    }

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return { name: 'login', params: to.params };
    }

    if ((to.name === 'login' || to.name === 'signup') && auth.isAuthenticated) {
        return { name: 'profile', params: to.params };
    }
});

export default router;
