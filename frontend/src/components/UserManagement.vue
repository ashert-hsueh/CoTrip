<template>
  <div class="user-management">
    <!-- 根据登录状态显示不同内容 -->
    <template v-if="isLoggedIn">
      <div class="header">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="个人资料" name="profile"></el-tab-pane>
        </el-tabs>
      </div>
      
      <div class="content">
        <Profile @logout="handleLogout" />
      </div>
    </template>
    
    <!-- 未登录状态显示登录和注册 -->
    <template v-else>
      <div class="header">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="登录" name="login"></el-tab-pane>
          <el-tab-pane label="注册" name="register"></el-tab-pane>
        </el-tabs>
      </div>
      
      <div class="content">
        <Login v-if="activeTab === 'login'" @login-success="handleLoginSuccess" />
        <Register v-if="activeTab === 'register'" @register-success="handleRegisterSuccess" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import Login from './Login.vue'
import Register from './Register.vue'
import Profile from './Profile.vue'
import { userService } from '../api/userService'

// 响应式数据
const activeTab = ref('login')
const isLoggedIn = ref(false)

// 处理登录成功
const handleLoginSuccess = () => {
  isLoggedIn.value = true
  activeTab.value = 'profile' // 登录成功后自动切换到个人资料
  ElMessage.success('登录成功')
}

// 处理注册成功
const handleRegisterSuccess = () => {
  activeTab.value = 'login'
  ElMessage.success('注册成功，请登录')
}

// 处理退出登录
const handleLogout = () => {
  isLoggedIn.value = false
  activeTab.value = 'login'
  ElMessage.success('已退出登录')
}

// 处理标签切换
const handleTabClick = (tab: any) => {
  if (tab.paneName === 'profile' && !isLoggedIn.value) {
    ElMessage.warning('请先登录')
    activeTab.value = 'login'
  }
}

// 检查用户登录状态
const checkLoginStatus = async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      await userService.getCurrentUser()
      isLoggedIn.value = true
    } catch (error) {
      // Token无效，清除
      localStorage.removeItem('token')
      isLoggedIn.value = false
    }
  }
}

// 组件挂载时检查登录状态
onMounted(() => {
  checkLoginStatus()
})
</script>

<style scoped>
.user-management {
  max-width: 500px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  margin-bottom: 30px;
}

.content {
  background-color: #fff;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
</style>