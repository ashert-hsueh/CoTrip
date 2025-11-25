<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>登录 CoTrip</h2>
          <p>欢迎回来！请登录您的账户</p>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="80px"
        class="login-form"
      >
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="loginForm.email"
            placeholder="请输入您的邮箱"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入您的密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="handleLogin"
            :loading="loading"
            block
            size="large"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-link">
        <span>还没有账户？</span>
        <el-button type="text" @click="handleGoToRegister">立即注册</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import { loginUser } from '../api/user';

// 定义事件发射器
const emit = defineEmits<{
  'go-to-register': []
}>();

const router = useRouter();
const loginFormRef = ref();
const loading = ref(false);
const authStore = useAuthStore();

const loginForm = reactive({
  email: '',
  password: '',
});

const loginRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度在 8 到 20 个字符', trigger: 'blur' },
  ],
};

const handleLogin = async () => {
  if (!loginFormRef.value) return;
  
  try {
    const valid = await loginFormRef.value.validate();
    if (valid) {
      loading.value = true;
      const result = await loginUser(loginForm);
      
      if (result.success) {
        ElMessage.success(result.message);
        
        // 更新状态管理中的登录状态
        authStore.login(result.user_id, result.username);
        
        // 保存完整的用户信息到 localStorage，供 Profile.vue 使用
        localStorage.setItem('userInfo', JSON.stringify({
          userId: result.user_id,
          username: result.username,
          email: result.email
        }));
        
        // 跳转到个人资料页面
        router.push('/user-management?tab=profile');
      } else {
        ElMessage.error(result.message);
      }
    }
  } catch (error) {
    console.error('登录失败:', error);
    ElMessage.error('登录失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const handleGoToRegister = () => {
  // 触发go-to-register事件
  emit('go-to-register');
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  text-align: center;
  margin-bottom: 20px;
}

.card-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.card-header p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.login-form {
  margin-top: 20px;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.register-link span {
  color: #606266;
}
</style>
