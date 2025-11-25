<template>
  <div class="user-management-container">
    <Header />

    
    <main class="user-management-main">
      <div class="page-header">
        <h1>用户管理</h1>
        <p>管理您的用户账户，包括登录、注册和个人资料设置</p>
      </div>
      
      <div class="user-management-content">
        <div class="form-container">
          <!-- 登录表单 -->
          <div v-if="activeTab === 'login'">
            <Login @go-to-register="handleGoToRegister" />
          </div>
          
          <!-- 注册表单 -->
          <div v-if="activeTab === 'register'">
            <Register @go-to-login="handleGoToLogin" />
          </div>
          
          <!-- 个人资料表单 -->
          <div v-if="activeTab === 'profile'">
            <Profile />
          </div>
        </div>
      </div>
    </main>
    
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import Profile from '../components/Profile.vue';

const activeTab = ref('login');
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
// 使用计算属性获取登录状态
const isLoggedIn = computed(() => authStore.isLoggedIn);

// 切换到注册页面
const handleGoToRegister = () => {
  activeTab.value = 'register';
  // 更新URL参数
  router.push({ path: '/user-management', query: { tab: 'register' } });
};

// 切换到登录页面
const handleGoToLogin = () => {
  activeTab.value = 'login';
  // 更新URL参数
  router.push({ path: '/user-management', query: { tab: 'login' } });
};

onMounted(() => {
  // 从localStorage中恢复登录状态
  authStore.restoreAuthState();
  
  // 检查URL参数中的tab
  const tabParam = route.query.tab as string;
  if (tabParam && ['login', 'register', 'profile'].includes(tabParam)) {
    activeTab.value = tabParam;
  }
  
  // 如果用户已登录且tab参数不是profile，则默认切换到profile
  if (isLoggedIn.value && tabParam !== 'profile') {
    activeTab.value = 'profile';
  }
});

// 监听路由变化，更新activeTab
watch(
  () => route.query.tab,
  (newTab) => {
    const tabParam = newTab as string;
    if (tabParam && ['login', 'register', 'profile'].includes(tabParam)) {
      activeTab.value = tabParam;
    }
    
    // 如果用户已登录且tab参数不是profile，则默认切换到profile
    if (isLoggedIn.value && tabParam !== 'profile') {
      activeTab.value = 'profile';
    }
  }
);
</script>

<style scoped>
.user-management-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
}

.user-management-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 18px;
  color: #606266;
}

.user-management-content {
  display: flex;
  justify-content: center;
}

.tab-navigation {
  width: 100%;
  max-width: 600px;
}

.user-management-footer {
  background-color: #303133;
  color: white;
  text-align: center;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .user-management-content {
    padding: 0 10px;
  }
}
</style>
