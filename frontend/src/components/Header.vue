<template>
  <header class="header">
    <div class="header-content">
      <div class="logo">
        <span class="logo-icon">🌍</span>
        <span class="logo-text">CoTrip</span>
      </div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/trip-planning" class="nav-link" :class="{ active: $route.path === '/trip-planning' }">旅行规划</router-link>
        <router-link to="/ledgers" class="nav-link" :class="{ active: $route.path === '/ledgers' }">账本管理</router-link>
        <router-link to="/user-management" class="nav-link" :class="{ active: $route.path === '/user-management' }">用户管理</router-link>
      </nav>
      <div class="user-actions" v-if="!authStore.isLoggedIn">
        <router-link to="/user-management?tab=login" class="btn btn-secondary">登录</router-link>
        <router-link to="/user-management?tab=register" class="btn btn-primary">注册</router-link>
      </div>
      <div class="user-info" v-else>
        <span class="welcome-text">欢迎, {{ authStore.username }}</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '../store/auth';

const authStore = useAuthStore();
// 从localStorage中恢复登录状态
authStore.restoreAuthState();
</script>

<style scoped>
.header {
  background: linear-gradient(135deg, #FFA939 0%, #FF8C00 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 24px;
  font-weight: 600;
}

.logo-icon {
  margin-right: 8px;
  font-size: 32px;
}

.nav-menu {
  display: flex;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: opacity 0.3s ease;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.active {
  opacity: 0.8;
  border-bottom: 2px solid white;
}

.user-actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: white;
  color: #FFA939;
  border: 2px solid white;
}

.btn-primary:hover {
  background-color: transparent;
  color: white;
}

.btn-secondary {
  background-color: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background-color: white;
  color: #FFA939;
}
</style>
