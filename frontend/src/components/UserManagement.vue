<template>
  <div class="user-management">
    <!-- 通用Header -->
    <header class="main-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo">CT</div>
          <span class="project-name">CoTrip</span>
        </div>
        <nav class="nav-menu" v-if="isLoggedIn">
          <el-menu mode="horizontal" background-color="transparent" text-color="#009CC6" active-text-color="#FFA939">
            <el-menu-item index="1" @click="navigateTo('home')">首页</el-menu-item>
            <el-menu-item index="2" @click="navigateTo('travel')">旅行规划</el-menu-item>
            <el-menu-item index="3" @click="navigateTo('bills')">账单管理</el-menu-item>
            <el-menu-item index="4" @click="showProfile" :class="{ active: currentView === 'profile' }">个人资料</el-menu-item>
            <el-menu-item index="5" @click="handleLogout">退出登录</el-menu-item>
          </el-menu>
        </nav>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <!-- 根据当前视图显示不同的组件 -->
      <Login 
        v-if="currentView === 'login'" 
        @login-success="handleLoginSuccess" 
        @switch-to-register="switchToRegister"
      />
      <Register 
        v-else-if="currentView === 'register'" 
        @register-success="handleRegisterSuccess" 
        @switch-to-login="switchToLogin"
      />
      <Profile 
        v-else-if="currentView === 'profile'" 
        @logout="handleLogout"
      />
    </main>

    <!-- 通用Footer -->
    <footer class="main-footer">
      <div class="footer-content">
        <div class="footer-info">
          <p>&copy; 2024 CoTrip. 旅行规划，让旅程更美好。</p>
        </div>
        <div class="footer-links">
          <a href="#" class="footer-link">关于我们</a>
          <a href="#" class="footer-link">使用帮助</a>
          <a href="#" class="footer-link">隐私政策</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import Login from './Login.vue'
import Register from './Register.vue'
import Profile from './Profile.vue'

// 当前视图状态
const currentView = ref<string>('login')
// 是否已登录
const isLoggedIn = ref<boolean>(false)

// 处理登录成功
const handleLoginSuccess = (user: any) => {
  isLoggedIn.value = true
  currentView.value = 'profile'
  ElMessage.success(`欢迎回来，${user.username}！`)
}

// 处理注册成功
const handleRegisterSuccess = (user: any) => {
  // 注册成功后自动切换到登录页
  currentView.value = 'login'
}

// 切换到注册页面
const switchToRegister = () => {
  currentView.value = 'register'
}

// 切换到登录页面
const switchToLogin = () => {
  currentView.value = 'login'
}

// 显示个人资料页面
const showProfile = () => {
  currentView.value = 'profile'
}

// 处理退出登录
const handleLogout = () => {
  // 清除本地存储的token和用户信息
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  isLoggedIn.value = false
  currentView.value = 'login'
  ElMessage.success('已退出登录')
}

// 页面导航（目前只是占位，后续实现）
const navigateTo = (page: string) => {
  switch (page) {
    case 'home':
      ElMessage.info('首页功能正在开发中...')
      break
    case 'travel':
      ElMessage.info('旅行规划功能正在开发中...')
      break
    case 'bills':
      ElMessage.info('账单管理功能正在开发中...')
      break
    default:
      break
  }
}

// 检查是否已登录
const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  if (token && user) {
    isLoggedIn.value = true
    currentView.value = 'profile'
  } else {
    isLoggedIn.value = false
    currentView.value = 'login'
  }
}

// 组件挂载时检查登录状态
onMounted(() => {
  checkLoginStatus()
})
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background-color: #F9F3EE;
  color: #333;
  line-height: 1.6;
}

/* 主页面容器 */
.user-management {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header样式 */
.main-header {
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 40px;
  height: 40px;
  background-color: #009CC6;
  color: white;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  font-family: 'Courier New', monospace;
}

.project-name {
  font-size: 24px;
  font-weight: bold;
  color: #009CC6;
}

.nav-menu {
  flex: 1;
  margin-left: 60px;
}

.nav-menu .el-menu {
  border-bottom: none;
}

.nav-menu .el-menu-item {
  font-size: 16px;
  padding: 0 20px;
  height: 40px;
  line-height: 40px;
}

.nav-menu .el-menu-item.active {
  color: #FFA939;
  font-weight: bold;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
}

/* Footer样式 */
.main-footer {
  background-color: white;
  padding: 30px 0;
  border-top: 1px solid #eee;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.footer-info p {
  color: #666;
  margin-bottom: 15px;
}

.footer-links {
  display: flex;
  gap: 30px;
  margin-top: 10px;
}

.footer-link {
  color: #009CC6;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-link:hover {
  color: #FFA939;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .nav-menu {
    margin-left: 0;
    width: 100%;
  }
  
  .nav-menu .el-menu-item {
    font-size: 14px;
    padding: 0 10px;
  }
  
  .footer-links {
    flex-direction: column;
    gap: 10px;
  }
  
  .main-content {
    padding: 15px;
  }
}
</style>
