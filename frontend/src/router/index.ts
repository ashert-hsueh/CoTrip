import { createRouter, createWebHistory } from 'vue-router'
import UserManagement from '../pages/UserManagement.vue'
import AuthPage from '../pages/AuthPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: AuthPage
  },
  {
    path: '/auth',
    name: 'auth',
    component: AuthPage
  },
  {
    path: '/user-management',
    name: 'user-management',
    component: UserManagement,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 导航守卫，确保需要认证的页面只有登录后才能访问
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = localStorage.getItem('token')
  
  if (requiresAuth && !isAuthenticated) {
    next('/auth')
  } else {
    next()
  }
})

export default router