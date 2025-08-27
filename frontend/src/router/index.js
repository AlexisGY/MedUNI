import { createRouter, createWebHistory } from 'vue-router'
import HomeView     from '../views/HomeView.vue'
import LoginView    from '../views/LoginView.vue'
import ReservarView from '../views/ReservarView.vue'
import PanelView    from '../views/PanelView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',        name: 'home',     component: HomeView },
    { path: '/login',   name: 'login',    component: LoginView },
    { path: '/reservar',name: 'reservar', component: ReservarView, meta: { requiresAuth: true } },
    { path: '/panel',   name: 'panel',    component: PanelView,    meta: { requiresAuth: true } },
    { path: '/about', redirect: '/login' },
    { path: '/:pathMatch(.*)*', component: { template: '<div class="p-3">404</div>' } },
  ],
})

// guard sencillo usando localStorage
router.beforeEach((to) => {
  const isAuth = !!localStorage.getItem('token')
  if (to.meta.requiresAuth && !isAuth) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})
export default router
