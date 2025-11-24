<template>
  <div class="profile-container">
    <div class="profile-card">
      <h2>个人资料</h2>
      
      <!-- 修改用户名表单 -->
      <div class="form-section">
        <h3>修改用户名</h3>
        <el-form :model="usernameForm" :rules="usernameRules" ref="usernameFormRef" label-width="120px">
          <el-form-item label="当前用户名">
            <el-input v-model="currentUser.username" disabled />
          </el-form-item>
          <el-form-item label="新用户名" prop="newUsername">
            <el-input v-model="usernameForm.newUsername" placeholder="请输入新用户名" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="updateUsername" class="update-btn">更新用户名</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 修改密码表单 -->
      <div class="form-section">
        <h3>修改密码</h3>
        <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
          <el-form-item label="原密码" prop="oldPassword">
            <el-input v-model="passwordForm.oldPassword" placeholder="请输入原密码" type="password" show-password />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input v-model="passwordForm.newPassword" placeholder="请输入新密码" type="password" show-password @input="checkNewPasswordStrength" />
            <div v-if="newPasswordStrengthText" class="password-strength" :class="newPasswordStrengthClass">
              {{ newPasswordStrengthText }}
            </div>
          </el-form-item>
          <el-form-item label="确认新密码" prop="confirmPassword">
            <el-input v-model="passwordForm.confirmPassword" placeholder="请再次输入新密码" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="updatePassword" class="update-btn">更新密码</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
}

interface UsernameForm {
  newUsername: string
}

interface PasswordForm {
  oldPassword: string
  newPassword: string
  confirmPassword: string
}

const emit = defineEmits<{
  logout: []
}>()

const currentUser = ref<User>({
  id: 0,
  username: '',
  email: ''
})

const usernameFormRef = ref()
const passwordFormRef = ref()

const usernameForm = reactive<UsernameForm>({
  newUsername: ''
})

const passwordForm = reactive<PasswordForm>({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const newPasswordStrength = ref<number>(0)

// 获取当前用户信息
const loadUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('请先登录')
      emit('logout')
      return
    }

    const response = await fetch('http://localhost:8000/api/users/profile', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      ElMessage.error('登录状态已过期，请重新登录')
      emit('logout')
      return
    }

    const userData = await response.json()
    currentUser.value = userData
  } catch (error) {
    console.error('Load user info error:', error)
    ElMessage.error('获取用户信息失败')
  }
}

// 检查新密码强度
const checkNewPasswordStrength = (password: string) => {
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
  
  newPasswordStrength.value = strength
}

const newPasswordStrengthText = computed(() => {
  if (passwordForm.newPassword.length === 0) return ''
  
  if (newPasswordStrength.value < 3) {
    return '密码强度不足（需要至少包含特殊字符、大写字母、小写字母、数字中的任意三种）'
  } else if (newPasswordStrength.value < 5) {
    return '密码强度中等'
  } else {
    return '密码强度强'
  }
})

const newPasswordStrengthClass = computed(() => {
  if (newPasswordStrength.value < 3) return 'weak'
  if (newPasswordStrength.value < 5) return 'medium'
  return 'strong'
})

const usernameRules = {
  newUsername: [
    { required: true, message: '请输入新用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在 2 到 50 个字符', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value === currentUser.value.username) {
          callback(new Error('新用户名与当前用户名相同'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度在 8 到 20 个字符', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value && newPasswordStrength.value < 3) {
          callback(new Error('密码强度不足，需要至少包含特殊字符、大写字母、小写字母、数字中的任意三种'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const updateUsername = async () => {
  await usernameFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          ElMessage.error('请先登录')
          emit('logout')
          return
        }

        const response = await fetch('http://localhost:8000/api/users/username', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            new_username: usernameForm.newUsername
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          ElMessage.error(errorData.detail || '更新用户名失败')
          return
        }

        const data = await response.json()
        ElMessage.success('用户名更新成功')
        // 更新本地用户信息
        currentUser.value.username = usernameForm.newUsername
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        user.username = usernameForm.newUsername
        localStorage.setItem('user', JSON.stringify(user))
        // 重置表单
        usernameForm.newUsername = ''
      } catch (error) {
        ElMessage.error('更新用户名失败，请稍后重试')
        console.error('Update username error:', error)
      }
    }
  })
}

const updatePassword = async () => {
  await passwordFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          ElMessage.error('请先登录')
          emit('logout')
          return
        }

        const response = await fetch('http://localhost:8000/api/users/password', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            old_password: passwordForm.oldPassword,
            new_password: passwordForm.newPassword
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          ElMessage.error(errorData.detail || '更新密码失败')
          return
        }

        ElMessage.success('密码更新成功')
        // 重置表单
        passwordForm.oldPassword = ''
        passwordForm.newPassword = ''
        passwordForm.confirmPassword = ''
        newPasswordStrength.value = 0
      } catch (error) {
        ElMessage.error('更新密码失败，请稍后重试')
        console.error('Update password error:', error)
      }
    }
  })
}

// 组件挂载时加载用户信息
onMounted(() => {
  // 先从localStorage获取用户信息
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    currentUser.value = JSON.parse(savedUser)
  }
  // 然后从服务器同步最新信息
  loadUserInfo()
})
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 60vh;
  background-color: #F9F3EE;
  padding: 40px 20px;
}

.profile-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
}

.profile-card h2 {
  color: #009CC6;
  text-align: center;
  margin-bottom: 40px;
  font-size: 24px;
}

.form-section {
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 1px solid #eee;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.form-section h3 {
  color: #009CC6;
  margin-bottom: 20px;
  font-size: 18px;
  border-left: 4px solid #FFA939;
  padding-left: 12px;
}

.update-btn {
  background-color: #009CC6;
  border-color: #009CC6;
  min-width: 120px;
  height: 36px;
}

.update-btn:hover {
  background-color: #007a9c;
  border-color: #007a9c;
}

.el-form-item {
  margin-bottom: 20px;
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
