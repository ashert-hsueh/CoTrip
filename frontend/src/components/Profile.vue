<template>
  <div class="profile">
    <h2>个人资料</h2>
    
    <el-card class="user-info-card">
      <template #header>
        <div class="card-header">
          <span>用户信息</span>
        </div>
      </template>
      <div class="user-info">
        <div class="info-item">
          <span class="label">用户ID：</span>
          <span>{{ userInfo?.id }}</span>
        </div>
        <div class="info-item">
          <span class="label">邮箱：</span>
          <span>{{ userInfo?.email }}</span>
        </div>
      </div>
    </el-card>
    
    <el-card class="username-card">
      <template #header>
        <div class="card-header">
          <span>修改用户名</span>
        </div>
      </template>
      <el-form
        :model="usernameForm"
        :rules="usernameRules"
        ref="usernameFormRef"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="newUsername">
          <el-input
            v-model="usernameForm.newUsername"
            placeholder="请输入新用户名"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="handleUpdateUsername"
            :loading="usernameLoading"
          >
            更新用户名
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="password-card">
      <template #header>
        <div class="card-header">
          <span>修改密码</span>
        </div>
      </template>
      <el-form
        :model="passwordForm"
        :rules="passwordRules"
        ref="passwordFormRef"
        label-width="80px"
      >
        <el-form-item label="原密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            placeholder="请输入原密码"
            type="password"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            placeholder="请输入新密码"
            type="password"
            show-password
            @input="validateNewPasswordStrength"
          ></el-input>
          <div v-if="newPasswordStrength > 0" class="password-strength">
            <div class="strength-label">密码强度：</div>
            <div class="strength-bars">
              <div
                v-for="i in 4"
                :key="i"
                class="strength-bar"
                :class="{
                  'weak': i <= 1 && newPasswordStrength === 1,
                  'medium': i <= 2 && newPasswordStrength === 2,
                  'strong': i <= 3 && newPasswordStrength === 3,
                  'very-strong': i <= 4 && newPasswordStrength === 4
                }"
              ></div>
            </div>
          </div>
          <div class="password-tip">
            密码需包含8-20位字符，至少包含三种字符类型
          </div>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            placeholder="请再次输入新密码"
            type="password"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="handleUpdatePassword"
            :loading="passwordLoading"
          >
            更新密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <div class="logout-section">
      <el-button type="danger" @click="handleLogout">退出登录</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElForm } from 'element-plus'
import { userService } from '../api/userService'

// 定义事件
const emit = defineEmits<{
  'logout': []
}>()

// 响应式数据
const userInfo = ref<any>(null)
const usernameLoading = ref(false)
const passwordLoading = ref(false)
const newPasswordStrength = ref(0)
const usernameFormRef = ref<InstanceType<typeof ElForm>>()
const passwordFormRef = ref<InstanceType<typeof ElForm>>()

const usernameForm = reactive({
  newUsername: ''
})

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 验证新密码强度
const validateNewPasswordStrength = () => {
  const password = passwordForm.newPassword
  if (!password) {
    newPasswordStrength.value = 0
    return
  }
  
  let strength = 0
  if (/[A-Z]/.test(password)) strength++
  if (/[a-z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++
  
  newPasswordStrength.value = strength
}

// 自定义密码验证规则
const validateNewPassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请输入新密码'))
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
const validateConfirmNewPassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    callback(new Error('请确认新密码'))
    return
  }
  
  if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
    return
  }
  
  callback()
}

// 表单验证规则
const usernameRules = {
  newUsername: [
    { required: true, message: '请输入新用户名', trigger: 'blur' },
    { min: 2, max: 50, message: '用户名长度在2-50个字符之间', trigger: 'blur' }
  ]
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, validator: validateNewPassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmNewPassword, trigger: 'blur' }
  ]
}

// 获取用户信息
const getUserInfo = async () => {
  try {
    const response = await userService.getCurrentUser()
    userInfo.value = response.data
    usernameForm.newUsername = response.data.username
  } catch (error) {
    ElMessage.error('获取用户信息失败')
    console.error('Get user info error:', error)
  }
}

// 更新用户名
const handleUpdateUsername = async () => {
  if (!usernameFormRef.value) return
  
  try {
    await usernameFormRef.value.validate()
    usernameLoading.value = true
    
    await userService.updateUsername(usernameForm.newUsername)
    
    // 更新本地存储的用户信息
    const userData = JSON.parse(localStorage.getItem('user') || '{}')
    userData.username = usernameForm.newUsername
    localStorage.setItem('user', JSON.stringify(userData))
    
    ElMessage.success('用户名更新成功')
  } catch (error: any) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('更新失败，请稍后重试')
      console.error('Update username error:', error)
    }
  } finally {
    usernameLoading.value = false
  }
}

// 更新密码
const handleUpdatePassword = async () => {
  if (!passwordFormRef.value) return
  
  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true
    
    await userService.updatePassword(
      passwordForm.oldPassword,
      passwordForm.newPassword
    )
    
    ElMessage.success('密码更新成功')
    
    // 重置密码表单
    passwordForm.oldPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
    newPasswordStrength.value = 0
    
  } catch (error: any) {
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('更新失败，请稍后重试')
      console.error('Update password error:', error)
    }
  } finally {
    passwordLoading.value = false
  }
}

// 退出登录
const handleLogout = () => {
  userService.logout()
  emit('logout')
}

// 组件挂载时获取用户信息
onMounted(() => {
  getUserInfo()
})
</script>

<style scoped>
.profile {
  max-width: 600px;
  margin: 0 auto;
}

.profile h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #009CC6;
}

.user-info-card,
.username-card,
.password-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  padding: 10px 0;
}

.info-item {
  margin-bottom: 10px;
}

.info-item .label {
  font-weight: bold;
  color: #606266;
  margin-right: 10px;
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

.logout-section {
  text-align: center;
  margin-top: 30px;
}

.logout-section .el-button--danger {
  background-color: #FFA939;
  border-color: #FFA939;
}

.logout-section .el-button--danger:hover {
  background-color: #ff9800;
  border-color: #ff9800;
}
</style>