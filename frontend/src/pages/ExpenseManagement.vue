<template>
  <div class="expense-management-container">
    <Header />

    
    <main class="expense-management-main">
      <div class="page-header">
        <h1>账单管理</h1>
        <p>记录和管理旅行中的各项开销，自动计算每人应付金额</p>
      </div>
      
      <div class="expense-management-content">
        <div class="expense-list-section">
          <div class="expense-list-container">
            <div class="expense-list-header">
              <h2>账单列表</h2>
              <el-button type="primary" @click="handleAddExpense">
                <el-icon><Plus /></el-icon>
                添加账单
              </el-button>
            </div>
            <div class="expense-list-placeholder">
              <span class="expense-icon">🧾</span>
              <p>账单列表功能将在后续版本中实现</p>
            </div>
          </div>
        </div>
        
        <div class="expense-summary-section">
          <div class="expense-summary-container">
            <h2>费用汇总</h2>
            <div class="expense-summary-placeholder">
              <span class="summary-icon">💰</span>
              <p>费用汇总功能将在后续版本中实现</p>
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
import { Plus } from '@element-plus/icons-vue';

const handleAddExpense = () => {
  // 添加账单逻辑
  console.log('添加账单');
};
</script>

<style scoped>
.expense-management-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
}

.expense-management-main {
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

.expense-management-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.expense-list-section {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

.expense-list-container {
  height: 100%;
}

.expense-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.expense-list-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.expense-list-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 2px dashed #dcdfe6;
}

.expense-icon {
  font-size: 64px;
  margin-bottom: 10px;
}

.expense-list-placeholder p {
  font-size: 16px;
  color: #909399;
}

.expense-summary-section {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 30px;
}

.expense-summary-container h2 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
}

.expense-summary-placeholder {
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 2px dashed #dcdfe6;
}

.summary-icon {
  font-size: 64px;
  margin-bottom: 10px;
}

.expense-summary-placeholder p {
  font-size: 16px;
  color: #909399;
}

.expense-management-footer {
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
  .expense-management-content {
    grid-template-columns: 1fr;
  }
}
</style>
