<template>
  <div class="trip-planning-container">
    <Header />

    
    <main class="trip-planning-main">
      <div class="page-header">
        <h1>旅行规划</h1>
        <p>在地图上规划您的旅行路线，添加目的地和行程安排</p>
      </div>
      
      <div class="trip-planning-content">
        <div class="map-section">
          <div class="map-container">
            <h2>地图路线规划</h2>
            <div class="map-placeholder">
              <span class="map-icon">🗺️</span>
              <p>地图功能将在后续版本中实现</p>
            </div>
          </div>
        </div>
        
        <div class="itinerary-section">
          <div class="itinerary-container">
            <h2>每日行程</h2>
            <div class="itinerary-placeholder">
              <span class="itinerary-icon">📅</span>
              <p>行程管理功能将在后续版本中实现</p>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';
// 旅行规划页面逻辑
</script>

<style scoped>
.trip-planning-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
}

.trip-planning-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 18px;
  color: #606266;
}

.trip-planning-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.map-section {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

.map-container h2 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.map-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 2px dashed #dcdfe6;
}

.map-icon {
  font-size: 64px;
  margin-bottom: 10px;
}

.map-placeholder p {
  font-size: 16px;
  color: #909399;
}

.itinerary-section {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

.itinerary-container h2 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.itinerary-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 2px dashed #dcdfe6;
}

.itinerary-icon {
  font-size: 64px;
  margin-bottom: 10px;
}

.itinerary-placeholder p {
  font-size: 16px;
  color: #909399;
}

.trip-planning-footer {
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
  .trip-planning-content {
    grid-template-columns: 1fr;
  }
}
</style>
