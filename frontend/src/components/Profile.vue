<template>
  <div class="profile-container">
    <h2>个人档案</h2>
    
    <div class="profile-info">
      <div class="info-item">
        <label>用户名:</label>
        <span>{{ user.username }}</span>
      </div>
      <div class="info-item">
        <label>邮箱:</label>
        <span>{{ user.email }}</span>
      </div>
    </div>

    <div class="profile-sections">
      <!-- 修改用户名 -->
      <div class="section">
        <h3>修改用户名</h3>
        <form class="form" @submit.prevent="handleUpdateUsername">
          <div class="form-group">
            <label for="newUsername">新用户名</label>
            <input
              id="newUsername"
              type="text"
              v-model="usernameForm.newUsername"
              placeholder="请输入新用户名"
              required
              :class="{ 'error': usernameErrors.newUsername }"
            />
            <span class="error-message" v-if="usernameErrors.newUsername">{{ usernameErrors.newUsername }}</span>
          </div>

          <button type="submit" class="submit-button" :disabled="isUpdatingUsername">
            {{ isUpdatingUsername ? '修改中...' : '修改用户名' }}
          </button>

          <div class="success-message" v-if="usernameSuccessMessage">{{ usernameSuccessMessage }}</div>
          <div class="error-message" v-if="usernameGeneralError">{{ usernameGeneralError }}</div>
        </form>
      </div>

      <!-- 修改密码 -->
      <div class="section">
        <h3>修改密码</h3>
        <form class="form" @submit.prevent="handleUpdatePassword">
          <div class="form-group">
            <label for="currentPassword">原密码</label>
            <input
              id="currentPassword"
              type="password"
              v-model="passwordForm.currentPassword"
              placeholder="请输入原密码"
              required
              :class="{ 'error': passwordErrors.currentPassword }"
            />
            <span class="error-message" v-if="passwordErrors.currentPassword">{{ passwordErrors.currentPassword }}</span>
          </div>

          <div class="form-group">
            <label for="newPassword">新密码</label>
            <input
              id="newPassword"
              type="password"
              v-model="passwordForm.newPassword"
              placeholder="请输入新密码"
              required
              :class="{ 'error': passwordErrors.newPassword }"
            />
            <span class="error-message" v-if="passwordErrors.newPassword">{{ passwordErrors.newPassword }}</span>
            <div class="password-strength" v-if="passwordForm.newPassword.length > 0">
              <div 
                class="strength-bar"
                :class="passwordStrengthClass"
              ></div>
              <span class="strength-text">{{ passwordStrengthText }}</span>
            </div>
          </div>

          <div class="form-group">
            <label for="confirmNewPassword">确认新密码</label>
            <input
              id="confirmNewPassword"
              type="password"
              v-model="passwordForm.confirmNewPassword"
              placeholder="请再次输入新密码"
              required
              :class="{ 'error': passwordErrors.confirmNewPassword }"
            />
            <span class="error-message" v-if="passwordErrors.confirmNewPassword">{{ passwordErrors.confirmNewPassword }}</span>
          </div>

          <button type="submit" class="submit-button" :disabled="isUpdatingPassword || !isPasswordStrongEnough">
            {{ isUpdatingPassword ? '修改中...' : '修改密码' }}
          </button>

          <div class="success-message" v-if="passwordSuccessMessage">{{ passwordSuccessMessage }}</div>
          <div class="error-message" v-if="passwordGeneralError">{{ passwordGeneralError }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';

interface User {
  id: number;
  username: string;
  email: string;
}

interface UsernameForm {
  newUsername: string;
}

interface PasswordForm {
  currentPassword: string;
  newPassword: string;
  confirmNewPassword: string;
}

interface UsernameErrors {
  newUsername: string | null;
}

interface PasswordErrors {
  currentPassword: string | null;
  newPassword: string | null;
  confirmNewPassword: string | null;
}

interface UpdateResponse {
  message: string;
  user: User;
}

const props = defineProps<{
  user: User;
  token: string;
}>();

const emit = defineEmits(['user-updated']);

const usernameForm = reactive<UsernameForm>({
  newUsername: ''
});

const passwordForm = reactive<PasswordForm>({
  currentPassword: '',
  newPassword: '',
  confirmNewPassword: ''
});

const usernameErrors = reactive<UsernameErrors>({
  newUsername: null
});

const passwordErrors = reactive<PasswordErrors>({
  currentPassword: null,
  newPassword: null,
  confirmNewPassword: null
});

const usernameSuccessMessage = ref<string | null>(null);
const usernameGeneralError = ref<string | null>(null);
const passwordSuccessMessage = ref<string | null>(null);
const passwordGeneralError = ref<string | null>(null);

const isUpdatingUsername = ref<boolean>(false);
const isUpdatingPassword = ref<boolean>(false);

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

const passwordStrength = computed(() => checkPasswordStrength(passwordForm.newPassword));

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

const isPasswordStrongEnough = computed(() => passwordStrength.value >= 3);

// 验证用户名表单
const validateUsernameForm = (): boolean => {
  usernameErrors.newUsername = null;
  usernameSuccessMessage.value = null;
  usernameGeneralError.value = null;
  let isValid = true;

  if (!usernameForm.newUsername.trim()) {
    usernameErrors.newUsername = '请输入新用户名';
    isValid = false;
  } else if (usernameForm.newUsername.length < 3 || usernameForm.newUsername.length > 50) {
    usernameErrors.newUsername = '用户名长度必须在3到50个字符之间';
    isValid = false;
  } else if (usernameForm.newUsername === props.user.username) {
    usernameErrors.newUsername = '新用户名不能与当前用户名相同';
    isValid = false;
  }

  return isValid;
};

// 验证密码表单
const validatePasswordForm = (): boolean => {
  passwordErrors.currentPassword = null;
  passwordErrors.newPassword = null;
  passwordErrors.confirmNewPassword = null;
  passwordSuccessMessage.value = null;
  passwordGeneralError.value = null;
  let isValid = true;

  if (!passwordForm.currentPassword.trim()) {
    passwordErrors.currentPassword = '请输入原密码';
    isValid = false;
  }

  if (!passwordForm.newPassword.trim()) {
    passwordErrors.newPassword = '请输入新密码';
    isValid = false;
  } else if (passwordForm.newPassword.length < 8 || passwordForm.newPassword.length > 20) {
    passwordErrors.newPassword = '密码长度必须在8到20个字符之间';
    isValid = false;
  } else if (!isPasswordStrongEnough.value) {
    passwordErrors.newPassword = '密码强度不足，需要包含大写字母、小写字母、数字和特殊字符中的至少三种';
    isValid = false;
  }

  if (!passwordForm.confirmNewPassword.trim()) {
    passwordErrors.confirmNewPassword = '请确认新密码';
    isValid = false;
  } else if (passwordForm.newPassword !== passwordForm.confirmNewPassword) {
    passwordErrors.confirmNewPassword = '两次输入的密码不一致';
    isValid = false;
  }

  if (passwordForm.currentPassword === passwordForm.newPassword) {
    passwordErrors.newPassword = '新密码不能与原密码相同';
    isValid = false;
  }

  return isValid;
};

// 修改用户名
const handleUpdateUsername = async () => {
  if (!validateUsernameForm()) {
    return;
  }

  isUpdatingUsername.value = true;

  try {
    const response = await axios.put<UpdateResponse>('http://localhost:8000/api/users/update-username', {
      new_username: usernameForm.newUsername
    }, {
      headers: {
        'Authorization': `Bearer ${props.token}`
      }
    });

    usernameSuccessMessage.value = response.data.message;
    usernameForm.newUsername = '';
    
    // 通知父组件用户信息已更新
    emit('user-updated', response.data.user);
  } catch (error: any) {
    if (error.response?.status === 400) {
      usernameGeneralError.value = '用户名已存在或不符合要求';
    } else if (error.response?.status === 401) {
      usernameGeneralError.value = '未授权访问，请重新登录';
    } else {
      usernameGeneralError.value = '修改用户名失败，请稍后重试';
    }
  } finally {
    isUpdatingUsername.value = false;
  }
};

// 修改密码
const handleUpdatePassword = async () => {
  if (!validatePasswordForm()) {
    return;
  }

  isUpdatingPassword.value = true;

  try {
    const response = await axios.put<UpdateResponse>('http://localhost:8000/api/users/update-password', {
      current_password: passwordForm.currentPassword,
      new_password: passwordForm.newPassword
    }, {
      headers: {
        'Authorization': `Bearer ${props.token}`
      }
    });

    passwordSuccessMessage.value = response.data.message;
    passwordForm.currentPassword = '';
    passwordForm.newPassword = '';
    passwordForm.confirmNewPassword = '';
  } catch (error: any) {
    if (error.response?.status === 400) {
      passwordGeneralError.value = '原密码错误或新密码不符合要求';
    } else if (error.response?.status === 401) {
      passwordGeneralError.value = '未授权访问，请重新登录';
    } else {
      passwordGeneralError.value = '修改密码失败，请稍后重试';
    }
  } finally {
    isUpdatingPassword.value = false;
  }
};

// 清除消息
const clearMessages = () => {
  usernameSuccessMessage.value = null;
  usernameGeneralError.value = null;
  passwordSuccessMessage.value = null;
  passwordGeneralError.value = null;
};

// 监听表单变化，清除消息
const watchFormChanges = () => {
  clearMessages();
};

// 监听表单变化
watch(() => [usernameForm.newUsername, passwordForm.currentPassword, passwordForm.newPassword, passwordForm.confirmNewPassword], () => {
  watchFormChanges();
}, { deep: true });

// 组件挂载时添加监听
onMounted(() => {
  // 可以在这里添加一些初始化逻辑
});
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

.profile-container h2 {
  text-align: center;
  color: #009CC6;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.profile-info {
  background-color: #F9F3EE;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-item label {
  font-weight: 600;
  color: #333;
  min-width: 80px;
}

.info-item span {
  color: #666;
}

.profile-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.section {
  background-color: #F9F3EE;
  padding: 1.5rem;
  border-radius: 8px;
}

.section h3 {
  color: #009CC6;
  margin-bottom: 1.5rem;
  font-size: 1.4rem;
}

.form {
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

.success-message {
  color: #51CF66;
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
  align-self: flex-start;
}

.submit-button:hover:not(:disabled) {
  background-color: #FF981F;
}

.submit-button:disabled {
  background-color: #D4D4D4;
  cursor: not-allowed;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-info {
    padding: 1rem;
  }

  .section {
    padding: 1rem;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .submit-button {
    align-self: stretch;
  }
}
</style>
