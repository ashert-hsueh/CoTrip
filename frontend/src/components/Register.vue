<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form class="register-form" @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">用户名</label>
        <input
          id="username"
          type="text"
          v-model="formData.username"
          placeholder="请输入您的用户名"
          required
          :class="{ 'error': errors.username }"
        />
        <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
      </div>

      <div class="form-group">
        <label for="email">邮箱</label>
        <input
          id="email"
          type="email"
          v-model="formData.email"
          placeholder="请输入您的邮箱"
          required
          :class="{ 'error': errors.email }"
        />
        <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input
          id="password"
          type="password"
          v-model="formData.password"
          placeholder="请输入您的密码"
          required
          :class="{ 'error': errors.password }"
        />
        <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
        <div class="password-strength" v-if="formData.password.length > 0">
          <div 
            class="strength-bar"
            :class="passwordStrengthClass"
          ></div>
          <span class="strength-text">{{ passwordStrengthText }}</span>
        </div>
      </div>

      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <input
          id="confirmPassword"
          type="password"
          v-model="formData.confirmPassword"
          placeholder="请再次输入您的密码"
          required
          :class="{ 'error': errors.confirmPassword }"
        />
        <span class="error-message" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
      </div>

      <button type="submit" class="submit-button" :disabled="isLoading">
        {{ isLoading ? '注册中...' : '注册' }}
      </button>

      <div class="error-message" v-if="generalError">{{ generalError }}</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import axios from 'axios';

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface Errors {
  username: string | null;
  email: string | null;
  password: string | null;
  confirmPassword: string | null;
}

interface User {
  id: number;
  username: string;
  email: string;
}

interface RegisterResponse {
  id: number;
  username: string;
  email: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

const emit = defineEmits(['register-success']);

const formData = reactive<FormData>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const errors = reactive<Errors>({
  username: null,
  email: null,
  password: null,
  confirmPassword: null
});

const generalError = ref<string | null>(null);
const isLoading = ref<boolean>(false);

// 密码强度检查
const checkPasswordStrength = (password: string): number => {
  let strength = 0;
  
  // 长度检查
  if (password.length >= 8) {
    strength += 1;
  }
  
  // 包含小写字母
  if (/[a-z]/.test(password)) {
    strength += 1;
  }
  
  // 包含大写字母
  if (/[A-Z]/.test(password)) {
    strength += 1;
  }
  
  // 包含数字
  if (/[0-9]/.test(password)) {
    strength += 1;
  }
  
  // 包含特殊字符
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    strength += 1;
  }
  
  return strength;
};

const passwordStrength = computed(() => checkPasswordStrength(formData.password));

const passwordStrengthClass = computed(() => {
  switch (passwordStrength.value) {
    case 0:
    case 1:
      return 'weak';
    case 2:
      return 'medium';
    case 3:
    case 4:
    case 5:
      return 'strong';
    default:
      return '';
  }
});

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 0:
    case 1:
      return '密码强度：弱';
    case 2:
      return '密码强度：中等';
    case 3:
    case 4:
    case 5:
      return '密码强度：强';
    default:
      return '';
  }
});



const validateForm = (): boolean => {
  errors.username = null;
  errors.email = null;
  errors.password = null;
  errors.confirmPassword = null;
  generalError.value = null;
  let isValid = true;

  // 验证用户名
  if (!formData.username.trim()) {
    errors.username = '请输入用户名';
    isValid = false;
  } else if (formData.username.length < 3 || formData.username.length > 50) {
    errors.username = '用户名长度必须在3到50个字符之间';
    isValid = false;
  }

  // 验证邮箱
  if (!formData.email.trim()) {
    errors.email = '请输入邮箱';
    isValid = false;
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
    errors.email = '请输入有效的邮箱地址';
    isValid = false;
  }

  // 验证密码
    if (!formData.password.trim()) {
      errors.password = '请输入密码';
      isValid = false;
    } else if (formData.password.length < 8 || formData.password.length > 20) {
      errors.password = '密码长度必须在8到20个字符之间';
      isValid = false;
    }

  // 验证确认密码
  if (!formData.confirmPassword.trim()) {
    errors.confirmPassword = '请确认密码';
    isValid = false;
  } else if (formData.password !== formData.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致';
    isValid = false;
  }

  return isValid;
};

const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }

  isLoading.value = true;
  generalError.value = null;

  try {
    // 注册用户
    const registerResponse = await axios.post<RegisterResponse>('http://localhost:8000/api/users/register', {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      confirm_password: formData.confirmPassword
    });

    const user = registerResponse.data;
    
    // 自动登录
    const loginResponse = await axios.post<LoginResponse>('http://localhost:8000/api/users/login', {
      email: formData.email,
      password: formData.password
    });

    const token = loginResponse.data.access_token;
    
    // 注册成功，触发事件
    emit('register-success', user, token);
    
    // 重置表单
    formData.username = '';
    formData.email = '';
    formData.password = '';
    formData.confirmPassword = '';
  } catch (error: any) {
    if (error.response?.status === 400) {
      generalError.value = '用户名或邮箱已存在，或密码不符合要求';
    } else {
      generalError.value = '注册失败，请稍后重试';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
}

.register-container h2 {
  text-align: center;
  color: #009CC6;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
}

.form-group input {
  padding: 0.75rem;
  border: 2px solid #70CDE5;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #009CC6;
}

.form-group input.error {
  border-color: #FF6B6B;
}

.error-message {
  color: #FF6B6B;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* 密码强度样式 */
.password-strength {
  margin-top: 0.5rem;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  margin-bottom: 0.25rem;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.strength-bar.weak {
  width: 33%;
  background-color: #FF6B6B;
}

.strength-bar.medium {
  width: 66%;
  background-color: #FFA939;
}

.strength-bar.strong {
  width: 100%;
  background-color: #51CF66;
}

.strength-text {
  font-size: 0.875rem;
  color: #666;
}

.submit-button {
  background-color: #FFA939;
  color: #F9F3EE;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover:not(:disabled) {
  background-color: #FF981F;
}

.submit-button:disabled {
  background-color: #D4D4D4;
  cursor: not-allowed;
}
</style>
