<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-content">
        <div class="footer-info">
          <h3>CoTrip</h3>
          <p>您的旅行规划助手，让每次出行都轻松愉快</p>
        </div>
        <div class="footer-copyright">
          <p>&copy; 2023 CoTrip. 保留所有权利。</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
// Footer组件逻辑
</script>

<style scoped>
.footer {
  background-color: #009CC6;
  color: white;
  padding: 20px 0;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.footer-info h3 {
  color: #FFA939;
  margin-bottom: 10px;
}

.footer-info p {
  margin-bottom: 15px;
  opacity: 0.9;
}

.footer-copyright p {
  font-size: 14px;
  opacity: 0.8;
}
</style>