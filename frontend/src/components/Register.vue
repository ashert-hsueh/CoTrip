<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>注册 CoTrip</h2>
          <p>创建一个新账户，开始您的旅行规划</p>
        </div>
      </template>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入您的用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入您的邮箱"
            prefix-icon="Message"
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入您的密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入您的密码"
            prefix-icon="Lock"
            show-password
            size="large"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            @click="handleRegister"
            :loading="loading"
            block
            size="large"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-link">
        <span>已经有账户？</span>
        <el-button type="text" @click="handleGoToLogin">立即登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { registerUser } from '../api/user';

// 定义事件发射器
const emit = defineEmits<{
  'go-to-login': []
}>();

const registerFormRef = ref();
const loading = ref(false);

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
});

// 密码强度验证函数
const validatePasswordStrength = (rule: any, value: string, callback: any) => {
  if (!value) {
    return callback(new Error('请输入密码'));
  }
  
  // 密码强度要求：至少包含8-20个字符，且包含大写字母、小写字母、数字和特殊字符中的任意三种
  const regex = /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{8,20}$/;
  
  if (!regex.test(value)) {
    return callback(new Error('密码必须包含大写字母、小写字母、数字和特殊字符中的任意三种'));
  }
  
  callback();
};

// 确认密码验证函数
const validateConfirmPassword = (rule: any, value: string, callback: any) => {
  if (!value) {
    return callback(new Error('请再次输入密码'));
  }
  
  if (value !== registerForm.password) {
    return callback(new Error('两次输入的密码不一致'));
  }
  
  callback();
};

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度在 8 到 20 个字符', trigger: 'blur' },
    { validator: validatePasswordStrength, trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
};

const handleRegister = async () => {
  if (!registerFormRef.value) return;
  
  try {
    const valid = await registerFormRef.value.validate();
    if (valid) {
      loading.value = true;
      // 只发送后端期望的三个字段
      const { username, email, password } = registerForm;
      const result = await registerUser({ username, email, password });
      
      if (result.success) {
        ElMessage.success(result.message);
        
        // 切换到登录标签页
        handleGoToLogin();
      } else {
        ElMessage.error(result.message);
      }
    }
  } catch (error) {
    console.error('注册失败:', error);
    ElMessage.error('注册失败，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const handleGoToLogin = () => {
  // 触发go-to-login事件
  emit('go-to-login');
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}

.register-card {
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

.register-form {
  margin-top: 20px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.login-link span {
  color: #606266;
}
</style>
