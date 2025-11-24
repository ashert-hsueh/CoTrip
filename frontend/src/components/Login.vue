<template>
  <div class="login-form">
    <h2>欢迎登录 CoTrip</h2>
    <el-form
      :model="loginForm"
      :rules="rules"
      ref="loginFormRef"
      label-width="80px"
    >
      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="loginForm.email"
          placeholder="请输入邮箱"
          prefix-icon="el-icon-message"
          type="email"
          autocomplete="email"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="loginForm.password"
          placeholder="请输入密码"
          prefix-icon="el-icon-lock"
          type="password"
          show-password
          autocomplete="current-password"
        ></el-input>
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          @click="handleLogin"
          :loading="loading"
          class="login-button"
        >
          登录
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElForm } from 'element-plus'
import { userService } from '../api/userService'

// 定义事件
const emit = defineEmits<{
  'login-success': []
}>()

// 路由实例
const router = useRouter()

// 响应式数据
const loginFormRef = ref<InstanceType<typeof ElForm>>()
const loading = ref(false)
const loginForm = reactive({
  email: '',
  password: ''
})

// 表单验证规则
const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const response = await userService.login(loginForm.email, loginForm.password)
    
    // 保存token和用户信息
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('tokenType', response.data.token_type)
    
    // 获取并保存用户信息
    const userResponse = await userService.getCurrentUser()
    localStorage.setItem('user', JSON.stringify(userResponse.data))
    
    // 触发登录成功事件
    emit('login-success')
    
    // 登录成功后延迟一下再跳转，确保状态更新完成
    setTimeout(() => {
      router.push('/')
    }, 500)
    
  } catch (error: any) {
    if (error.response?.status === 401) {
      ElMessage.error('邮箱或密码错误')
    } else {
      ElMessage.error('登录失败，请稍后重试')
      console.error('Login error:', error)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-form {
  text-align: center;
}

.login-form h2 {
  margin-bottom: 30px;
  color: #009CC6;
}

.login-button {
  width: 100%;
  background-color: #009CC6;
  border-color: #009CC6;
}

.login-button:hover {
  background-color: #0088aa;
  border-color: #0088aa;
}
</style>