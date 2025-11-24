<template>
  <div class="register-container">
    <div class="register-card">
      <h2>注册</h2>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱" type="email" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" placeholder="请输入密码" type="password" show-password @input="checkPasswordStrength" />
          <div v-if="passwordStrengthText" class="password-strength" :class="passwordStrengthClass">
            {{ passwordStrengthText }}
          </div>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" placeholder="请再次输入密码" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister" class="register-btn">注册</el-button>
          <el-button @click="switchToLogin" class="login-link">去登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'

interface RegisterForm {
  username: string
  email: string
  password: string
  confirmPassword: string
}

const emit = defineEmits<{
  registerSuccess: [user: any]
  switchToLogin: []
}>()

const registerFormRef = ref()
const registerForm = reactive<RegisterForm>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const passwordStrength = ref<number>(0)

// 密码强度检查
const checkPasswordStrength = (password: string) => {
  let strength = 0
  
  // 检查长度
  if (password.length >= 8 && password.length <= 20) {
    strength += 1
  }
  
  // 检查特殊字符
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    strength += 1
  }
  
  // 检查大写字母
  if (/[A-Z]/.test(password)) {
    strength += 1
  }
  
  // 检查小写字母
  if (/[a-z]/.test(password)) {
    strength += 1
  }
  
  // 检查数字
  if (/[0-9]/.test(password)) {
    strength += 1
  }
  
  passwordStrength.value = strength
}

const passwordStrengthText = computed(() => {
  if (registerForm.password.length === 0) return ''
  
  if (passwordStrength.value < 3) {
    return '密码强度不足（需要至少包含特殊字符、大写字母、小写字母、数字中的任意三种）'
  } else if (passwordStrength.value < 5) {
    return '密码强度中等'
  } else {
    return '密码强度强'
  }
})

const passwordStrengthClass = computed(() => {
  if (passwordStrength.value < 3) return 'weak'
  if (passwordStrength.value < 5) return 'medium'
  return 'strong'
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度在 8 到 20 个字符', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value && passwordStrength.value < 3) {
          callback(new Error('密码强度不足，需要至少包含特殊字符、大写字母、小写字母、数字中的任意三种'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const handleRegister = async () => {
  await registerFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const response = await fetch('http://localhost:8000/api/users/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: registerForm.username,
            email: registerForm.email,
            password: registerForm.password
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          ElMessage.error(errorData.detail || '注册失败')
          return
        }

        const data = await response.json()
        ElMessage.success('注册成功')
        // 注册成功后跳转到登录页
        emit('switchToLogin')
      } catch (error) {
        ElMessage.error('注册失败，请稍后重试')
        console.error('Register error:', error)
      }
    }
  })
}

const switchToLogin = () => {
  emit('switchToLogin')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  background-color: #F9F3EE;
  padding: 20px;
}

.register-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
}

.register-card h2 {
  color: #009CC6;
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
}

.register-btn {
  background-color: #009CC6;
  border-color: #009CC6;
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.register-btn:hover {
  background-color: #007a9c;
  border-color: #007a9c;
}

.login-link {
  margin-top: 15px;
  width: 100%;
  background-color: #FFA939;
  border-color: #FFA939;
  color: white;
  height: 40px;
  font-size: 16px;
}

.login-link:hover {
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

.password-strength {
  margin-top: 8px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-align: center;
}

.password-strength.weak {
  background-color: #fef0f0;
  color: #f56c6c;
  border: 1px solid #fbc4c4;
}

.password-strength.medium {
  background-color: #fdf6ec;
  color: #e6a23c;
  border: 1px solid #fac858;
}

.password-strength.strong {
  background-color: #f0f9eb;
  color: #67c23a;
  border: 1px solid #b7eb8f;
}
</style>
