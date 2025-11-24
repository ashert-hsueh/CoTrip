<template>
  <div class="user-page">
    <UserManagement @logout="handleLogout" />
  </div>
</template>

<script setup lang="ts">
import UserManagement from '../components/UserManagement.vue'

// 定义事件
const emit = defineEmits<{
  'logout': []
}>()

// 处理退出登录
const handleLogout = () => {
  emit('logout')
}
</script>

<style scoped>
.user-page {
  max-width: 800px;
  margin: 0 auto;
}
</style>