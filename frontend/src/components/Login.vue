<template>
  <div class="login-container">
    <div class="login-card">
      <h2>登录</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="loginForm.email" placeholder="请输入邮箱" type="email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" placeholder="请输入密码" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" class="login-btn">登录</el-button>
          <el-button @click="switchToRegister" class="register-link">去注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

interface LoginForm {
  email: string
  password: string
}

const emit = defineEmits<{
  loginSuccess: [user: any]
  switchToRegister: []
}>()

const loginFormRef = ref()
const loginForm = reactive<LoginForm>({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await fetch('http://localhost:8000/api/users/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({
            username: loginForm.email, // OAuth2PasswordRequestForm 使用 username 字段
            password: loginForm.password
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          ElMessage.error(errorData.detail || '登录失败')
          return
        }

        const data = await response.json()
        // 保存token到localStorage
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        ElMessage.success('登录成功')
        emit('loginSuccess', data.user)
      } catch (error) {
        ElMessage.error('登录失败，请稍后重试')
        console.error('Login error:', error)
      }
    }
  })
}

const switchToRegister = () => {
  emit('switchToRegister')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  background-color: #F9F3EE;
  padding: 20px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  color: #009CC6;
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
}

.login-btn {
  background-color: #009CC6;
  border-color: #009CC6;
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.login-btn:hover {
  background-color: #007a9c;
  border-color: #007a9c;
}

.register-link {
  margin-top: 15px;
  width: 100%;
  background-color: #FFA939;
  border-color: #FFA939;
  color: white;
  height: 40px;
  font-size: 16px;
}

.register-link:hover {
  background-color: #e6952c;
  border-color: #e6952c;
  color: white;
}

.el-form-item {
  margin-bottom: 25px;
}

.el-input__wrapper {
  border-radius: 8px;
}
</style>
