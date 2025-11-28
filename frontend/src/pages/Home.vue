<template>
  <div class="home-container">
    <Header />


    <main class="home-main">
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">欢迎使用 CoTrip</h1>
          <p class="hero-subtitle">协同旅行规划平台，让每一次出行都更轻松、有序和透明</p>
          <div class="hero-buttons">
            <router-link to="/trip-planning" class="btn btn-primary">开始规划旅行</router-link>
            <router-link to="/ledgers" class="btn btn-secondary">账本管理</router-link>
          </div>
        </div>
        <div class="hero-image">
          <img src="../assets/travel.png" alt="旅行规划" />
        </div>
      </section>

      <section class="features-section">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🗺️</div>
            <h3 class="feature-title">地图路线规划</h3>
            <p class="feature-description">在交互式地图上添加目的地，生成最佳路线</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💰</div>
            <h3 class="feature-title">旅行预算估算</h3>
            <p class="feature-description">智能估算旅行费用，帮助您合理规划预算</p>
          </div>
          <div class="feature-card" @click="goToLedgers">
            <div class="feature-icon">🧾</div>
            <h3 class="feature-title">账本管理</h3>
            <p class="feature-description">轻松记录和管理旅行中的各项开销</p>
            <div class="feature-action">
              <span>立即使用 <el-icon><ArrowRight /></el-icon></span>
            </div>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🤝</div>
            <h3 class="feature-title">自动拆账</h3>
            <p class="feature-description">智能计算每人应付金额，生成最小转账方案</p>
          </div>
        </div>
      </section>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';
import { ArrowRight } from '@element-plus/icons-vue';

const router = useRouter();

const goToLedgers = () => {
  router.push('/ledgers');
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
}

.home-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 60px;
  gap: 40px;
}

.hero-content {
  flex: 1;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 20px;
}

.hero-subtitle {
  font-size: 20px;
  color: #606266;
  margin-bottom: 40px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 20px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #FFA939;
  color: white;
}

.btn-primary:hover {
  background-color: #FF8C00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 169, 57, 0.3);
}

.btn-secondary {
  background-color: white;
  color: #FFA939;
  border: 2px solid #FFA939;
}

.btn-secondary:hover {
  background-color: #FFA939;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 169, 57, 0.3);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.home-footer {
  background-color: #303133;
  color: white;
  padding: 20px 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
  font-size: 14px;
}

.hero-image img {
  max-width: 100%;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.features-section {
  text-align: center;
}

.section-title {
  font-size: 36px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 40px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.feature-card {
  background-color: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-card:hover .feature-action {
  opacity: 1;
  transform: translateY(0);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.feature-description {
  font-size: 16px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 16px;
}

.feature-action {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(180deg, transparent, rgba(255, 169, 57, 0.1));
  padding: 20px;
  text-align: right;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  color: #FFA939;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.home-footer {
  background-color: #303133;
  color: white;
  text-align: center;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-buttons {
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
