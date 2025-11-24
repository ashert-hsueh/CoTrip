<template>
  <div class="register-form">
    <h2>创建新账户</h2>
    <el-form
      :model="registerForm"
      :rules="rules"
      ref="registerFormRef"
      label-width="80px"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="registerForm.username"
          placeholder="请输入用户名"
          prefix-icon="el-icon-user"
          autocomplete="username"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="registerForm.email"
          placeholder="请输入邮箱"
          prefix-icon="el-icon-message"
          type="email"
          autocomplete="email"
        ></el-input>
      </el-form-item>
      
      <el-form-item label="密码" prop="password">
        <el-input
          v-model="registerForm.password"
          placeholder="请输入密码"
          prefix-icon="el-icon-lock"
          type="password"
          show-password
          @input="validatePasswordStrength"
          autocomplete="new-password"
        ></el-input>
        <div v-if="passwordStrength > 0" class="password-strength">
          <div class="strength-label">密码强度：</div>
          <div class="strength-bars">
            <div
              v-for="i in 4"
              :key="i"
              class="strength-bar"
              :class="{
                'weak': i <= 1 && passwordStrength === 1,
                'medium': i <= 2 && passwordStrength === 2,
                'strong': i <= 3 && passwordStrength === 3,
                'very-strong': i <= 4 && passwordStrength === 4
              }"
            ></div>
          </div>
        </div>
        <div class="password-tip">
          密码需包含8-20位字符，至少包含三种字符类型（大写字母、小写字母、数字、特殊字符）
        </div>
      </el-form-item>
      
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input
          v-model="registerForm.confirmPassword"
          placeholder="请再次输入密码"
          prefix-icon="el-icon-lock"
          type="password"
          show-password
          autocomplete="new-password"
        ></el-input>
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          @click="handleRegister"
          :loading="loading"
          class="register-button"
        >
          注册
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElForm } from 'element-plus'
import { userService } from '../api/userService'

// 定义事件
const emit = defineEmits<{
  'register-success': []
}>()

// 响应式数据
const registerFormRef = ref<InstanceType<typeof ElForm>>()
const loading = ref(false)
const passwordStrength = ref(0)
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 验证密码强度
const validatePasswordStrength = () => {
  const password = registerForm.password
  if (!password) {
    passwordStrength.value = 0
    return
  }
  
  let strength = 0
  
  // 检查字符类型
  if (/[A-Z]/.test(password)) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  
  passwordStrength.value = strength
}

// 自定义密码强度验证规则
const validatePassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入密码'))
    return
  }
  
  if (value.length < 8 || value.length > 20) {
    callback(new Error('密码长度必须在8-20位之间'))
    return
  }
  
  let strength = 0
  if (/[A-Z]/.test(value)) strength++
  if (/[a-z]/.test(value)) strength++
  if (/[0-9]/.test(value)) strength++
  if (/[^A-Za-z0-9]/.test(value)) strength++
  
  if (strength < 3) {
    callback(new Error('密码必须包含至少三种字符类型'))
    return
  }
  
  callback()
}

// 自定义确认密码验证规则
const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请确认密码'))
    return
  }
  
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
    return
  }
  
  callback()
}

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在2-50个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    await userService.register(
      registerForm.username,
      registerForm.email,
      registerForm.password
    )
    
    // 触发注册成功事件
    emit('register-success')
    
  } catch (error: any) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('注册失败，请稍后重试')
      console.error('Register error:', error)
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-form {
  text-align: center;
}

.register-form h2 {
  margin-bottom: 30px;
  color: #009CC6;
}

.register-button {
  width: 100%;
  background-color: #009CC6;
  border-color: #009CC6;
}

.register-button:hover {
  background-color: #0088aa;
  border-color: #0088aa;
}

.password-strength {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
}

.strength-label {
  margin-right: 8px;
  color: #606266;
}

.strength-bars {
  display: flex;
  gap: 4px;
}

.strength-bar {
  width: 30px;
  height: 4px;
  background-color: #e4e7ed;
  border-radius: 2px;
}

.strength-bar.weak {
  background-color: #f56c6c;
}

.strength-bar.medium {
  background-color: #e6a23c;
}

.strength-bar.strong {
  background-color: #67c23a;
}

.strength-bar.very-strong {
  background-color: #009CC6;
}

.password-tip {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  text-align: left;
}
</style>