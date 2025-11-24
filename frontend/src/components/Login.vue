<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <form class="login-form" @submit.prevent="handleLogin">
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
      </div>

      <button type="submit" class="submit-button" :disabled="isLoading">
        {{ isLoading ? '登录中...' : '登录' }}
      </button>

      <div class="error-message" v-if="generalError">{{ generalError }}</div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import axios from 'axios';
import { emit } from 'vue';

interface FormData {
  email: string;
  password: string;
}

interface Errors {
  email: string | null;
  password: string | null;
}

interface User {
  id: number;
  username: string;
  email: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

const emit = defineEmits(['login-success']);

const formData = reactive<FormData>({
  email: '',
  password: ''
});

const errors = reactive<Errors>({
  email: null,
  password: null
});

const generalError = ref<string | null>(null);
const isLoading = ref<boolean>(false);

const validateForm = (): boolean => {
  errors.email = null;
  errors.password = null;
  generalError.value = null;
  let isValid = true;

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

  return isValid;
};

const handleLogin = async () => {
  if (!validateForm()) {
    return;
  }

  isLoading.value = true;
  generalError.value = null;

  try {
    const response = await axios.post<LoginResponse>('http://localhost:8000/api/users/login', {
      email: formData.email,
      password: formData.password
    });

    const token = response.data.access_token;
    
    // 获取用户信息
    const userResponse = await axios.get<User>('http://localhost:8000/api/users/profile', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const user = userResponse.data;
    
    // 登录成功，触发事件
    emit('login-success', user, token);
    
    // 重置表单
    formData.email = '';
    formData.password = '';
  } catch (error: any) {
    if (error.response?.status === 401) {
      generalError.value = '邮箱或密码错误';
    } else {
      generalError.value = '登录失败，请稍后重试';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
}

.login-container h2 {
  text-align: center;
  color: #009CC6;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.login-form {
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
