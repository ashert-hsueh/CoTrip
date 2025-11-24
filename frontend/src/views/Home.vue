<template>
  <div class="home">
    <div class="hero-section">
      <h1>欢迎使用 CoTrip</h1>
      <p>您的智能旅行规划助手</p>
      <div class="cta-buttons">
        <router-link to="/trip" class="btn-primary">开始规划旅程</router-link>
        <router-link to="/user" class="btn-secondary">登录/注册</router-link>
      </div>
    </div>
    
    <div class="features-section">
      <div class="feature-card">
        <h3>智能旅行规划</h3>
        <p>根据您的喜好和预算，定制最适合您的旅行路线。</p>
      </div>
      <div class="feature-card">
        <h3>费用跟踪与管理</h3>
        <p>轻松记录旅行中的每一笔开销，实时统计预算使用情况。</p>
      </div>
      <div class="feature-card">
        <h3>个性化推荐</h3>
        <p>基于您的旅行历史，推荐您可能喜欢的新目的地和活动。</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 首页逻辑
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 80px 20px;
  background-color: #70CDE5;
  border-radius: 10px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 48px;
  color: white;
  margin-bottom: 10px;
}

.hero-section p {
  font-size: 20px;
  color: white;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 30px;
  border-radius: 30px;
  text-decoration: none;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #FFA939;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #ff9800;
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: white;
  color: #009CC6;
  border: none;
}

.btn-secondary:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

.features-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  margin-bottom: 60px;
}

.feature-card {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.feature-card h3 {
  color: #009CC6;
  margin-bottom: 15px;
  font-size: 20px;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .features-section {
    grid-template-columns: 1fr;
  }
}
</style>