import { createRouter, createWebHistory } from 'vue-router'
import LoginView      from '../views/LoginView.vue'
import ReservarView   from '../views/ReservarView.vue'
import CalendarView   from '../views/CalendarView.vue'
// ESPECIALIDADES
import EspecialidadesView from '../views/EspecialidadesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
  { path: '/', redirect: { name: 'login' } },
  { path: '/login',     name: 'login',    component: LoginView },
    { path: '/reservar',  name: 'reservar', component: ReservarView, meta: { requiresAuth: true } },
    { path: '/calendario',name: 'calendar', component: CalendarView, meta: { requiresAuth: true } }, 
    // ESPECIALIDADES ROUTER
    { path: '/especialidades',name: 'especialidades', component: EspecialidadesView, meta: { requiresAuth: true } },
    // 👈 nuevo
    { path: '/about', redirect: '/login' },
    { path: '/:pathMatch(.*)*', component: { template: '<div class="p-3">404</div>' } },
  ],
  scrollBehavior() { return { top: 0 } }
})

// Guard sencillo
router.beforeEach((to) => {
  const isAuth = !!localStorage.getItem('token')

  // rutas protegidas
  if (to.meta.requiresAuth && !isAuth) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // si ya está logueado y va a login, mándalo al calendario
  if (to.name === 'login' && isAuth) {
    return { name: 'calendar' }
  }
})

export default router
