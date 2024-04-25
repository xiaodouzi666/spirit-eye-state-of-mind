import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import 'nprogress/nprogress.css'

const Chat = () => import('../views/Chat/index.vue');


const routes: RouteRecordRaw[] = [
    {
        path: '/',
        name: 'Home',
        component: Chat,
    },
    
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

export default router;
