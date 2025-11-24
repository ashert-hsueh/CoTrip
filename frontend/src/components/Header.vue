<template>
  <header class="header">
    <div class="header-container">
      <div class="logo-container">
        <span class="logo">CoTrip</span>
        <span class="logo-text">旅行规划助手</span>
      </div>
      
      <nav class="nav">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/user" class="nav-item">用户管理</router-link>
        <router-link to="/trip" class="nav-item">旅行规划</router-link>
        <router-link to="/expense" class="nav-item">账单管理</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
// Header组件逻辑
</script>

<style scoped>
.header {
  background-color: #F9F3EE;
  padding: 15px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  color: #FFA939;
  margin-right: 10px;
}

.logo-text {
  font-size: 16px;
  color: #009CC6;
}

.nav {
  display: flex;
  gap: 30px;
}

.nav-item {
  color: #009CC6;
  font-size: 16px;
  text-decoration: none;
  padding: 5px 10px;
  transition: all 0.3s ease;
  border-radius: 4px;
}

.nav-item:hover {
  color: #FFA939;
  background-color: rgba(255, 169, 57, 0.1);
}

.nav-item.router-link-active {
  color: #FFA939;
  font-weight: bold;
  background-color: rgba(255, 169, 57, 0.1);
}
</style>