<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人资料</h2>
          <p>管理您的账户信息</p>
        </div>
      </template>
      
      <div class="profile-content">
        <div class="user-info">
          <h3>基本信息</h3>
          <div class="info-item">
            <label>用户ID:</label>
            <span>{{ userInfo?.userId }}</span>
          </div>
          <div class="info-item">
            <label>用户名:</label>
            <span>{{ userInfo?.username }}</span>
          </div>
          <div class="info-item">
            <label>邮箱:</label>
            <span>{{ userInfo?.email }}</span>
          </div>
        </div>
        
        <el-divider />
        
        <div class="update-username-section">
          <h3>修改用户名</h3>
          <el-form
            ref="updateUsernameFormRef"
            :model="updateUsernameForm"
            :rules="updateUsernameRules"
            label-width="100px"
            class="update-username-form"
          >
            <el-form-item label="新用户名" prop="newUsername">
              <el-input
                v-model="updateUsernameForm.newUsername"
                placeholder="请输入新用户名"
                prefix-icon="User"
                size="large"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                @click="handleUpdateUsername"
                :loading="updatingUsername"
                size="large"
              >
                更新用户名
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-divider />
        
        <div class="update-password-section">
          <h3>修改密码</h3>
          <el-form
            ref="updatePasswordFormRef"
            :model="updatePasswordForm"
            :rules="updatePasswordRules"
            label-width="100px"
            class="update-password-form"
          >
            <el-form-item label="原密码" prop="oldPassword">
              <el-input
                v-model="updatePasswordForm.oldPassword"
                type="password"
                placeholder="请输入原密码"
                prefix-icon="Lock"
                show-password
                size="large"
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="updatePasswordForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                prefix-icon="Lock"
                show-password
                size="large"
              />
            </el-form-item>
            
            <el-form-item label="确认新密码" prop="confirmNewPassword">
              <el-input
                v-model="updatePasswordForm.confirmNewPassword"
                type="password"
                placeholder="请再次输入新密码"
                prefix-icon="Lock"
                show-password
                size="large"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                @click="handleUpdatePassword"
                :loading="updatingPassword"
                size="large"
              >
                更新密码
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-divider />
        
        <div class="logout-section">
          <el-button
            type="danger"
            @click="handleLogout"
            size="large"
          >
            退出登录
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { updateUsername, updatePassword } from '../api/user';

const userInfo = ref<any>(null);
const updateUsernameFormRef = ref();
const updatePasswordFormRef = ref();
const updatingUsername = ref(false);
const updatingPassword = ref(false);

const updateUsernameForm = reactive({
  newUsername: '',
});

const updatePasswordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmNewPassword: '',
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
  
  if (value !== updatePasswordForm.newPassword) {
    return callback(new Error('两次输入的密码不一致'));
  }
  
  callback();
};

const updateUsernameRules = {
  newUsername: [
    { required: true, message: '请输入新用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
  ],
};

const updatePasswordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度在 8 到 20 个字符', trigger: 'blur' },
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, max: 20, message: '密码长度在 8 到 20 个字符', trigger: 'blur' },
    { validator: validatePasswordStrength, trigger: 'blur' },
  ],
  confirmNewPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
};

onMounted(() => {
  // 从本地存储获取用户信息
  const userInfoStr = localStorage.getItem('userInfo');
  if (userInfoStr) {
    userInfo.value = JSON.parse(userInfoStr);
  }
});

const handleUpdateUsername = async () => {
  if (!updateUsernameFormRef.value || !userInfo.value) return;
  
  try {
    const valid = await updateUsernameFormRef.value.validate();
    if (valid) {
      updatingUsername.value = true;
      const result = await updateUsername({
        user_id: userInfo.value.userId,
        new_username: updateUsernameForm.newUsername,
      });
      
      if (result.success) {
        ElMessage.success(result.message);
        
        // 更新本地存储的用户信息
        userInfo.value.username = result.username;
        localStorage.setItem('userInfo', JSON.stringify(userInfo.value));
        
        // 重置表单
        updateUsernameForm.newUsername = '';
      } else {
        ElMessage.error(result.message);
      }
    }
  } catch (error) {
    console.error('更新用户名失败:', error);
    ElMessage.error('更新用户名失败，请稍后重试');
  } finally {
    updatingUsername.value = false;
  }
};

const handleUpdatePassword = async () => {
  if (!updatePasswordFormRef.value || !userInfo.value) return;
  
  try {
    const valid = await updatePasswordFormRef.value.validate();
    if (valid) {
      updatingPassword.value = true;
      const result = await updatePassword({
        user_id: userInfo.value.userId,
        old_password: updatePasswordForm.oldPassword,
        new_password: updatePasswordForm.newPassword,
      });
      
      if (result.success) {
        ElMessage.success(result.message);
        
        // 重置表单
        updatePasswordForm.oldPassword = '';
        updatePasswordForm.newPassword = '';
        updatePasswordForm.confirmNewPassword = '';
      } else {
        ElMessage.error(result.message);
      }
    }
  } catch (error) {
    console.error('更新密码失败:', error);
    ElMessage.error('更新密码失败，请稍后重试');
  } finally {
    updatingPassword.value = false;
  }
};

const handleLogout = () => {
  // 清除本地存储的用户信息
  localStorage.removeItem('userInfo');
  
  // 刷新页面以更新登录状态
  window.location.reload();
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}

.profile-card {
  width: 100%;
  max-width: 600px;
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

.profile-content {
  padding: 20px;
}

.user-info {
  margin-bottom: 20px;
}

.user-info h3 {
  margin: 0 0 20px 0;
  color: #303133;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.info-item label {
  font-weight: 500;
  color: #303133;
  margin-right: 10px;
  width: 80px;
}

.info-item span {
  color: #606266;
}

.update-username-section {
  margin-bottom: 20px;
}

.update-username-section h3 {
  margin: 0 0 20px 0;
  color: #303133;
}

.update-username-form {
  max-width: 400px;
}

.update-password-section {
  margin-bottom: 20px;
}

.update-password-section h3 {
  margin: 0 0 20px 0;
  color: #303133;
}

.update-password-form {
  max-width: 400px;
}

.logout-section {
  text-align: center;
}
</style>
