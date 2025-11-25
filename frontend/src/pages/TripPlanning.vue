<template>
  <div class="trip-planning-container">
    <Header />

    <main class="trip-planning-main">
      <div class="page-header">
        <h1>我的旅行本</h1>
        <p>记录每一次美好的旅行时光</p>
      </div>

      <!-- 旅行本列表区域 -->
      <div class="trip-notebooks-section">
        <!-- 新增旅行本按钮 -->
        <div class="add-notebook-btn-container">
          <el-button
            type="primary"
            size="large"
            @click="handleAddNotebook"
            icon="Plus"
          >
            新建旅行本
          </el-button>
        </div>

        <!-- 旅行本瀑布流布局 -->
        <div class="notebooks-grid">
          <TripNotebookCard
            v-for="notebook in tripNotebooks"
            :key="notebook.id"
            :notebook="notebook"
            @click="handleOpenNotebook(notebook.id)"
          />
        </div>

        <!-- 翻开动画容器 -->
        <div
          ref="bookOpenContainer"
          class="book-open-container"
          v-if="showBookOpenAnimation"
        >
          <div class="book-open-animation">
            <div class="book-cover front-cover">
              <div class="cover-content">
                <h2>{{ openingNotebookTitle || '我的旅行本' }}</h2>
              </div>
            </div>
            <div class="book-page">
              <div class="page-content">
                <div class="loading-spinner">
                  <el-icon size="48"><Loading /></el-icon>
                  <p>正在加载...</p>
                </div>
              </div>
            </div>
            <div class="book-cover back-cover"></div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';
import TripNotebookCard from '../components/TripNotebookCard.vue';
import { Loading } from '@element-plus/icons-vue';

// 旅行本数据类型
import type { TripNotebook as ITripNotebook } from '../types/trip';

interface TripNotebook extends ITripNotebook {
  // 添加扩展属性
}

// 旅行本列表数据
const tripNotebooks = ref<TripNotebook[]>([
  {
    id: '1',
    title: '云南大理之行',
    coverColor: '#70CDE5',
    createdAt: '2024-01-15',
    updatedAt: '2024-01-20',
    destinations: [
      {
        id: '1',
        name: '大理古城',
        address: '云南省大理白族自治州大理市大理镇',
        location: '100.23287,25.62431'
      },
      {
        id: '2',
        name: '洱海',
        address: '云南省大理白族自治州大理市',
        location: '100.18775,25.73813'
      }
    ]
  },
  {
    id: '2',
    title: '成都美食探索',
    coverColor: '#FFA939',
    createdAt: '2024-02-20',
    updatedAt: '2024-02-25',
    destinations: [
      {
        id: '3',
        name: '宽窄巷子',
        address: '四川省成都市青羊区金河路与长顺上街交叉路口',
        location: '104.06793,30.57285'
      }
    ]
  },
  {
    id: '3',
    title: '三亚海滩度假',
    coverColor: '#009CC6',
    createdAt: '2024-03-10',
    updatedAt: '2024-03-15'
  },
  {
    id: '4',
    title: '西藏高原之旅',
    coverColor: '#70CDE5',
    createdAt: '2024-04-05',
    updatedAt: '2024-04-12'
  },
  {
    id: '5',
    title: '上海都市体验',
    coverColor: '#FFA939',
    createdAt: '2024-05-18',
    updatedAt: '2024-05-22'
  },
  {
    id: '6',
    title: '杭州西湖漫步',
    coverColor: '#70CDE5',
    createdAt: '2024-06-10',
    updatedAt: '2024-06-13'
  },
  {
    id: '7',
    title: '北京古都风情',
    coverColor: '#009CC6',
    createdAt: '2024-07-22',
    updatedAt: '2024-07-28'
  },
  {
    id: '8',
    title: '厦门海岛游',
    coverColor: '#FFA939',
    createdAt: '2024-08-15',
    updatedAt: '2024-08-18'
  }
]);

const router = useRouter();
const showBookOpenAnimation = ref(false);
const openingNotebookTitle = ref('');
const bookOpenContainer = ref<HTMLElement | null>(null);

// 新增旅行本
const handleAddNotebook = () => {
  // 这里可以添加创建旅行本的逻辑
  console.log('新增旅行本');
};

// 打开旅行本
const handleOpenNotebook = (notebookId: string) => {
  const notebook = tripNotebooks.value.find(n => n.id === notebookId);
  if (notebook) {
    openingNotebookTitle.value = notebook.title;
    showBookOpenAnimation.value = true;

    // 动画持续时间
    setTimeout(() => {
      showBookOpenAnimation.value = false;
      // 导航到旅行本详情页面
      router.push(`/trip-notebook/${notebookId}`);
    }, 1500);
  }
};
</script>

<style scoped>
.trip-planning-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
  font-family: 'Microsoft YaHei', sans-serif;
}

.trip-planning-main {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 60px;
}

.page-header h1 {
  font-size: 42px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 15px;
  font-family: '华文行楷', cursive;
}

.page-header p {
  font-size: 20px;
  color: #606266;
  font-weight: 300;
}

.trip-notebooks-section {
  position: relative;
}

.add-notebook-btn-container {
  text-align: right;
  margin-bottom: 40px;
  padding: 0 20px;
}

/* 定义字体 */
@font-face {
  font-family: '华文行楷';
  src: local('华文行楷'),
       url('@/assets/fonts/HuaWenXingKai.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Butler';
  src: local('Butler'),
       url('@/assets/fonts/Butler.woff2') format('woff2'),
       url('@/assets/fonts/Butler.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

/* 瀑布流布局 */
.notebooks-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 40px;
  justify-content: center;
  padding: 0 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 旅行本翻开动画 */
.book-open-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

.book-open-animation {
  width: 300px;
  height: 400px;
  position: relative;
  transform-style: preserve-3d;
  animation: openBook 1.2s ease-in-out forwards;
}

.book-cover,
.book-page {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.front-cover {
  background: #70CDE5;
  transform-origin: left center;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 3;
}

.back-cover {
  background: #5AA8BF;
  z-index: 1;
}

.book-page {
  background: white;
  z-index: 2;
  left: 10px;
  transform: rotateY(-10deg);
}

.cover-content h2 {
  font-family: '华文行楷', cursive;
  font-size: 28px;
  text-align: center;
  padding: 0 20px;
}

.page-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner {
  text-align: center;
}

.loading-spinner p {
  margin-top: 15px;
  color: #666;
  font-size: 16px;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes openBook {
  0% {
    transform: rotateY(0deg) scale(0.8);
  }
  50% {
    transform: rotateY(30deg) scale(1.1);
  }
  100% {
    transform: rotateY(60deg) scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .trip-planning-main {
    padding: 40px 15px;
  }

  .page-header h1 {
    font-size: 32px;
  }

  .page-header p {
    font-size: 16px;
  }

  .notebooks-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 30px;
    padding: 0 15px;
  }

  .add-notebook-btn-container {
    padding: 0 15px;
  }

  .book-open-animation {
    width: 240px;
    height: 320px;
  }

  .cover-content h2 {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .notebooks-grid {
    grid-template-columns: 1fr;
    max-width: 300px;
    margin: 0 auto;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .book-open-animation {
    width: 200px;
    height: 280px;
  }

  .cover-content h2 {
    font-size: 20px;
  }
}
</style>
