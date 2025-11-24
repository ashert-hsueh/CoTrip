<script setup lang="ts">
import UserManagement from './components/UserManagement.vue'
</script>

<template>
  <UserManagement />
</template>

<style>
/* 全局样式 */
:root {
  /* 主要颜色变量 */
  --primary-color: #009CC6;
  --secondary-color: #FFA939;
  --background-color: #F9F3EE;
  --accent-color: #70CDE5;
  --text-color: #333333;
  --white: #FFFFFF;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
}

/* 确保页面占满整个视口 */
#app {
  min-height: 100vh;
}
</style>
