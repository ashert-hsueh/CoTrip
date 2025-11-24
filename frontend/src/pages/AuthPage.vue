<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo">
        <svg width="48" height="48" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="14" stroke="#FFA939" stroke-width="2"/>
          <path d="M10 16L14 20L22 12" stroke="#FFA939" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1>CoTrip</h1>
      </div>

      <div class="tabs">
        <button class="tab-button" :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">
          登录
        </button>
        <button class="tab-button" :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">
          注册
        </button>
      </div>

      <div class="tab-content">
        <div v-if="activeTab === 'login'" class="tab-panel" :class="{ active: activeTab === 'login' }">
          <Login @login-success="handleLoginSuccess" />
        </div>
        <div v-if="activeTab === 'register'" class="tab-panel" :class="{ active: activeTab === 'register' }">
          <Register @register-success="handleRegisterSuccess" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';

interface User {
  id: number;
  username: string;
  email: string;
}

const router = useRouter();
const activeTab = ref('login');

const handleLoginSuccess = (user: User, token: string) => {
  console.log('登录成功，用户信息:', user);
  console.log('登录成功，token:', token);
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
  console.log('存储到localStorage成功');
  console.log('准备跳转到/user-management');
  router.push('/user-management');
};

const handleRegisterSuccess = (user: User, token: string) => {
  localStorage.setItem('token', token);
  localStorage.setItem('user', JSON.stringify(user));
  router.push('/user-management');
};
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #F9F3EE;
}

.auth-card {
  background-color: #FFFFFF;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.logo h1 {
  font-size: 1.8rem;
  color: #009CC6;
  font-weight: 600;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #E0E0E0;
}

.tab-button {
  background: none;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-button:hover:not(:disabled) {
  color: #009CC6;
  border-bottom-color: #009CC6;
}

.tab-button.active {
  color: #009CC6;
  border-bottom-color: #009CC6;
}

.tab-content {
  min-height: 300px;
}

.tab-panel {
  display: none;
}

.tab-panel.active {
  display: block;
}
</style>