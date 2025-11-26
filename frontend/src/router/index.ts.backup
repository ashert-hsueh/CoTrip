import { createRouter, createWebHistory } from 'vue-router';
import UserManagement from '../pages/UserManagement.vue';
import Home from '../pages/Home.vue';
import TripPlanning from '../pages/TripPlanning.vue';
import ExpenseManagement from '../pages/ExpenseManagement.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: UserManagement,
  },
  {
    path: '/trip-planning',
    name: 'TripPlanning',
    component: TripPlanning,
  },
  {
    path: '/expense-management',
    name: 'ExpenseManagement',
    component: ExpenseManagement,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
