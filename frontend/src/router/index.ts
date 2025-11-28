import { createRouter, createWebHistory } from 'vue-router';
import UserManagement from '../pages/UserManagement.vue';
import Home from '../pages/Home.vue';
import TripPlanning from '../pages/TripPlanning.vue';
import ExpenseManagement from '../pages/ExpenseManagement.vue';
import LedgerListPage from '../pages/LedgerListPage.vue';
import LedgerDetailPage from '../pages/LedgerDetailPage.vue';

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
  {
    path: '/ledgers',
    name: 'LedgerList',
    component: LedgerListPage,
  },
  {
    path: '/ledgers/:id',
    name: 'LedgerDetail',
    component: LedgerDetailPage,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
