import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import AnalysisView from '../views/AnalysisView.vue';
import DashboardView from '../views/DashboardView.vue';
import { useAnalysisStore } from "../stores/useAnalysisStore";

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
    }
]

const router =  createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0 };
    }
});

export default router;
