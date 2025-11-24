<template>
  <div class="user-management-container">
    <header class="header">
      <div class="logo">
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="14" stroke="#FFA939" stroke-width="2"/>
          <path d="M10 16L14 20L22 12" stroke="#FFA939" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <h1>CoTrip</h1>
      </div>
      <nav class="nav">
        <a href="#" class="nav-link">首页</a>
        <a href="#" class="nav-link">旅行规划</a>
        <a href="#" class="nav-link active">用户管理</a>
        <a href="#" class="nav-link">账单管理</a>
      </nav>
      <div class="user-info">
        <span class="welcome-text">欢迎, {{ currentUser?.username }}</span>
        <button class="logout-button" @click="handleLogout">
          退出登录
        </button>
      </div>
    </header>

    <main class="main-content">
      <div class="profile-container">
        <h2>个人档案</h2>
        <div class="profile-info">
          <div class="info-item">
            <label>用户名:</label>
            <span>{{ currentUser?.username }}</span>
          </div>
          <div class="info-item">
            <label>邮箱:</label>
            <span>{{ currentUser?.email }}</span>
          </div>
        </div>
        <div v-if="currentUser && token">
          <Profile :user="currentUser" :token="token" @user-updated="handleUserUpdated" />
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>&copy; 2023 CoTrip. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Profile from '../components/Profile.vue';

interface User {
  id: number;
  username: string;
  email: string;
}

const router = useRouter();
const currentUser = ref<User | null>(null);
const token = ref<string | null>(null);

// 检查本地存储中是否有用户信息
const checkAuth = async () => {
  console.log('进入checkAuth函数');
  const storedToken = localStorage.getItem('token');
  const storedUser = localStorage.getItem('user');
  console.log('localStorage中的token:', storedToken);
  console.log('localStorage中的user:', storedUser);
  if (storedToken && storedUser) {
    try {
      currentUser.value = JSON.parse(storedUser);
      token.value = storedToken;
      console.log('解析用户信息成功，currentUser:', currentUser.value);
      console.log('解析用户信息成功，token:', token.value);
    } catch (error) {
      console.error('解析用户信息失败:', error);
      // 如果解析失败，跳转到登录页面
      router.push('/auth');
    }
  } else {
    console.log('没有找到登录信息，跳转到登录页面');
    // 如果没有登录信息，跳转到登录页面
    router.push('/auth');
  }
};

const handleUserUpdated = (updatedUser: User) => {
  currentUser.value = updatedUser;
  localStorage.setItem('user', JSON.stringify(updatedUser));
};

const handleLogout = () => {
  currentUser.value = null;
  token.value = null;
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/auth');
};

onMounted(() => {
  checkAuth();
});
</script>

<style scoped>
.user-management-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
}

.header {
  background-color: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-text {
  color: #333;
  font-weight: 500;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo h1 {
  font-size: 1.5rem;
  color: #009CC6;
  font-weight: 600;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #009CC6;
}

.nav-link.active {
  color: #009CC6;
  border-bottom: 2px solid #009CC6;
  padding-bottom: 0.25rem;
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #E0E0E0;
  flex-wrap: wrap;
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

.tab-button:disabled {
  color: #999;
  cursor: not-allowed;
}

.logout-button {
  background-color: #FF6B6B;
  color: #F9F3EE;
  border-radius: 6px;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #FF5252;
}

.profile-container {
  background-color: #FFFFFF;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.profile-container h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #009CC6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  margin-top: 1rem;
  color: #666;
  font-size: 1rem;
}

.tab-panel {
  display: none;
}

.tab-panel.active {
  display: block;
}

.footer {
  background-color: #FFFFFF;
  padding: 1rem;
  text-align: center;
  color: #666;
  border-top: 1px solid #E0E0E0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav {
    gap: 1rem;
  }

  .user-info {
    flex-direction: column;
    gap: 0.5rem;
  }

  .main-content {
    padding: 1rem;
  }

  .profile-container {
    padding: 1rem;
  }

  .logout-button {
    margin-left: 0;
  }

  .tab-content {
    padding: 1rem;
  }
}
</style>
