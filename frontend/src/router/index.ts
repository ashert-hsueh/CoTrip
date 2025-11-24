import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('../views/User.vue')
  },
  {
    path: '/trip',
    name: 'Trip',
    component: () => import('../views/Trip.vue')
  },
  {
    path: '/expense',
    name: 'Expense',
    component: () => import('../views/Expense.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router