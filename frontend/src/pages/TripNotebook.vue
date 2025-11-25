<template>
  <div class="trip-notebook-container">
    <Header />

    <main class="trip-notebook-main">
      <!-- 面包屑导航 -->
      <el-breadcrumb separator="/" class="breadcrumb">
        <el-breadcrumb-item
          :to="{ name: 'TripPlanning' }"
          @click.native="handleGoBack"
        >
          <el-icon size="16"><House /></el-icon>
          我的旅行本
        </el-breadcrumb-item>
        <el-breadcrumb-item>{{ notebook?.title || '旅行本' }}</el-breadcrumb-item>
      </el-breadcrumb>

      <!-- 旅行本标题区域 -->
      <div class="notebook-header">
        <div class="notebook-info">
          <h1 class="notebook-title">{{ notebook?.title || '我的旅行本' }}</h1>
          <div class="notebook-meta">
            <span class="created-date">
              <el-icon size="16"><Calendar /></el-icon>
              创建于 {{ formattedCreateDate }}
            </span>
            <span class="update-date">
              <el-icon size="16"><EditPen /></el-icon>
              最后编辑 {{ formattedUpdateDate }}
            </span>
            <span class="destination-count" v-if="notebook?.destinations?.length">
              <el-icon size="16"><Location /></el-icon>
              {{ notebook.destinations.length }} 个目的地
            </span>
          </div>
        </div>
        <div class="notebook-actions">
          <el-button size="small" @click="handleEdit">
            <el-icon><EditPen /></el-icon>
            编辑
          </el-button>
          <el-button size="small" type="primary" @click="handleAddDestination">
            <el-icon><Plus /></el-icon>
            添加目的地
          </el-button>
        </div>
      </div>

      <!-- 主要内容区域 -->
      <div class="main-content">
        <!-- 左侧：地图组件 -->
        <div class="map-container">
          <div class="map-header">
            <h2>地图路线规划</h2>
            <div class="map-actions">
              <el-select
                v-model="transportationMode"
                placeholder="选择交通方式"
                size="small"
                @change="handleTransportationModeChange"
                :popper-options="{
                  placement: 'bottom-end',
                  modifiers: [
                    {
                      name: 'computeStyle',
                      options: {
                        gpuAcceleration: false
                      }
                    }
                  ]
                }"
              >
                <el-option label="驾车" value="driving" />
                <el-option label="步行" value="walking" />
                <el-option label="骑行" value="bicycling" />
                <el-option label="公共交通" value="transit" />
              </el-select>
              <el-button size="small" @click="handleCalculateRoute">
                <el-icon><Compass /></el-icon>
                规划路线
              </el-button>
            </div>
          </div>

          <!-- 地图搜索区域 -->
          <div class="search-container">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索目的地"
              size="small"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #append>
                <el-button @click="handleSearch" size="small">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>

            <!-- 搜索结果 -->
            <div class="search-results" v-if="searchResults.length > 0">
              <div
                v-for="result in searchResults"
                :key="result.id"
                class="search-result-item"
                @click="handleAddSearchResult(result)"
              >
                <el-icon size="16" class="result-icon"><Location /></el-icon>
                <div class="result-info">
                  <div class="result-name">{{ result.name }}</div>
                  <div class="result-address">{{ result.address }}</div>
                </div>
                <el-button size="mini" @click.stop="handleAddSearchResult(result)">
                  添加
                </el-button>
              </div>
            </div>
          </div>

          <!-- 高德地图组件 -->
          <div class="map-wrapper">
            <AMapComponent
              ref="mapComponentRef"
              :api-key="AMAP_KEY"
              :destinations="notebook?.destinations || []"
              :routes="routes"
              :transportation-mode="transportationMode"
              @location-selected="handleLocationSelected"
            />
          </div>
        </div>

        <!-- 右侧：目的地列表 -->
        <div class="sidebar">
          <div class="sidebar-section">
            <h3 class="sidebar-title">
              <el-icon><Location /></el-icon>
              目的地列表
            </h3>
            <div class="destination-list">
              <div
                v-for="(destination, index) in notebook?.destinations || []"
                :key="destination.id"
                class="destination-item"
              >
                <div class="destination-index">{{ index + 1 }}</div>
                <div class="destination-info">
                  <div class="destination-name">{{ destination.name }}</div>
                  <div class="destination-address">{{ destination.address }}</div>
                  <div class="destination-actions">
                    <el-button
                      size="mini"
                      text
                      @click="handleSetOrigin(destination)"
                      :disabled="originId === destination.id"
                    >
                      {{ originId === destination.id ? '起点' : '设为起点' }}
                    </el-button>
                    <el-button
                      size="mini"
                      text
                      @click="handleSetDestination(destination)"
                      :disabled="destId === destination.id"
                    >
                      {{ destId === destination.id ? '终点' : '设为终点' }}
                    </el-button>
                  </div>
                </div>
                <el-button
                  size="mini"
                  text
                  @click="handleRemoveDestination(destination.id)"
                  type="danger"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>

              <div v-if="(!notebook?.destinations || notebook.destinations.length === 0)" class="empty-state">
                <el-icon size="48" class="empty-icon"><Location /></el-icon>
                <p>暂无目的地，点击上方"添加目的地"按钮</p>
                <p>或在地图上搜索并添加</p>
              </div>
            </div>
          </div>

          <!-- 路线信息区域 -->
          <div class="sidebar-section" v-if="routes.length > 0">
            <h3 class="sidebar-title">
              <el-icon><Navigation /></el-icon>
              路线信息
            </h3>
            <div class="route-info">
              <div class="route-summary">
                <div class="route-distance">
                  <span class="label">距离：</span>
                  <span class="value">{{ totalDistance }}</span>
                </div>
                <div class="route-duration">
                  <span class="label">预计时间：</span>
                  <span class="value">{{ totalDuration }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Header from '../components/Header.vue';
import Footer from '../components/Footer.vue';
import AMapComponent from '../components/AMapComponent.vue';
import {
  House,
  Calendar,
  EditPen,
  Location,
  Plus,
  Search,
  Compass,
  Delete
} from '@element-plus/icons-vue';
import { searchPlaces, getRoute } from '../api/amap';
import type {
  TripNotebook,
  Destination,
  Route,
  TransportationMode
} from '../types/trip';

// 环境变量
const AMAP_KEY = import.meta.env.VITE_AMAP_KEY;

// 路由参数
const route = useRoute();
const router = useRouter();
const notebookId = route.params.id as string;

// 旅行本数据
const notebook = ref<TripNotebook | null>(null);
const routes = ref<Route[]>([]);

// 搜索相关
const searchKeyword = ref('');
const searchResults = ref<any[]>([]);

// 路线规划相关
const transportationMode = ref<TransportationMode>('driving');
const originId = ref<string | null>(null);
const destId = ref<string | null>(null);

// 地图组件引用
const mapComponentRef = ref<InstanceType<typeof AMapComponent> | null>(null);

// 模拟旅行本数据
const mockNotebooks: TripNotebook[] = [
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
  }
];

// 格式化日期
const formattedCreateDate = computed(() => {
  if (!notebook.value?.createdAt) return '';
  const date = new Date(notebook.value.createdAt);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
});

const formattedUpdateDate = computed(() => {
  if (!notebook.value?.updatedAt) return '';
  const date = new Date(notebook.value.updatedAt);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
});

// 总距离和时间
const totalDistance = computed(() => {
  if (routes.value.length === 0) return '0 km';
  const total = routes.value.reduce((sum, route) => {
    const distance = parseFloat(route.distance || '0');
    return sum + distance;
  }, 0);
  return `${total.toFixed(1)} km`;
});

const totalDuration = computed(() => {
  if (routes.value.length === 0) return '0 分钟';
  const total = routes.value.reduce((sum, route) => {
    const duration = parseFloat(route.duration || '0');
    return sum + duration;
  }, 0);
  if (total < 60) {
    return `${Math.round(total)} 分钟`;
  } else {
    const hours = Math.floor(total / 60);
    const minutes = Math.round(total % 60);
    return `${hours}小时${minutes}分钟`;
  }
});

// 获取旅行本数据
const getNotebookData = () => {
  // 模拟API请求
  const foundNotebook = mockNotebooks.find(n => n.id === notebookId);
  if (foundNotebook) {
    notebook.value = { ...foundNotebook };
    // 默认设置第一个目的地为起点
    if (foundNotebook.destinations && foundNotebook.destinations.length > 0) {
      const firstDest = foundNotebook.destinations[0];
      if (firstDest) {
        originId.value = firstDest.id;
      }
      // 如果有多个目的地，设置第二个为终点
      if (foundNotebook.destinations.length > 1) {
        const secondDest = foundNotebook.destinations[1];
        if (secondDest) {
          destId.value = secondDest.id;
        }
      }
    }
  }
};

// 搜索地点
const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    searchResults.value = [];
    return;
  }

  try {
    const data = await searchPlaces(searchKeyword.value);
    if (data.status === '1' && data.pois) {
      searchResults.value = data.pois.map((poi: any) => ({
        id: poi.id,
        name: poi.name,
        address: poi.address,
        location: poi.location,
        type: poi.type
      }));
    }
  } catch (error) {
    console.error('搜索失败:', error);
  }
};

// 添加搜索结果到目的地
const handleAddSearchResult = (result: any) => {
  if (!notebook.value) return;

  const newDestination: Destination = {
    id: result.id,
    name: result.name,
    address: result.address,
    location: result.location
  };

  if (!notebook.value.destinations) {
    notebook.value.destinations = [];
  }

  notebook.value.destinations.push(newDestination);
  searchResults.value = [];
  searchKeyword.value = '';
};

// 添加目的地
const handleAddDestination = () => {
  // 这里可以添加添加目的地的逻辑
  console.log('添加目的地');
};

// 编辑旅行本
const handleEdit = () => {
  // 这里可以添加编辑旅行本的逻辑
  console.log('编辑旅行本');
};

// 设置起点
const handleSetOrigin = (destination: Destination) => {
  originId.value = destination.id;
};

// 设置终点
const handleSetDestination = (destination: Destination) => {
  destId.value = destination.id;
};

// 删除目的地
const handleRemoveDestination = (destinationId: string) => {
  if (!notebook.value?.destinations) return;

  notebook.value.destinations = notebook.value.destinations.filter(
    d => d.id !== destinationId
  );

  // 如果删除的是起点或终点，重新设置
  if (originId.value === destinationId) {
    originId.value = notebook.value.destinations[0]?.id || null;
  }
  if (destId.value === destinationId) {
    destId.value = notebook.value.destinations[1]?.id || null;
  }
};

// 交通方式改变
const handleTransportationModeChange = () => {
  console.log('交通方式改变:', transportationMode.value);
  // 这里可以添加交通方式改变后的逻辑
};

// 计算路线
const handleCalculateRoute = async () => {
  if (!originId.value || !destId.value || !notebook.value?.destinations) {
    console.error('请选择起点和终点');
    return;
  }

  const originDest = notebook.value.destinations.find(d => d.id === originId.value);
  const destDest = notebook.value.destinations.find(d => d.id === destId.value);

  if (!originDest || !destDest) {
    console.error('起点或终点不存在');
    return;
  }

  try {
    const routeData = await getRoute(
      originDest.location,
      destDest.location,
      transportationMode.value
    );

    if (routeData && routeData.status === '1' && routeData.route) {
      // 处理路线数据
      const newRoutes: Route[] = routeData.route.paths.map((path: any, index: number) => ({
        id: `route-${Date.now()}-${index}`,
        origin: originDest.location,
        destination: destDest.location,
        mode: transportationMode.value,
        distance: path.distance,
        duration: path.duration,
        path: path.polyline
      }));

      routes.value = newRoutes;
      console.log('路线规划成功:', newRoutes);
    }
  } catch (error) {
    console.error('路线规划失败:', error);
  }
};

// 处理地图上选择的位置
const handleLocationSelected = (location: string, name?: string, address?: string) => {
  console.log('地图上选择的位置:', location, name, address);
  // 这里可以添加处理逻辑
};

// 返回上一页
const handleGoBack = () => {
  router.push({ name: 'TripPlanning' });
};

// 生命周期
onMounted(() => {
  getNotebookData();
});

onBeforeUnmount(() => {
  // 清理工作
});
</script>

<style scoped>
.trip-notebook-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F9F3EE;
  font-family: 'Microsoft YaHei', sans-serif;
}

.trip-notebook-main {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.breadcrumb {
  margin-bottom: 30px;
}

.notebook-header {
  background-color: white;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 20px;
}

.notebook-info {
  flex: 1;
  min-width: 300px;
}

.notebook-title {
  font-family: '华文行楷', cursive;
  font-size: 36px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  line-height: 1.2;
}

.notebook-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  font-size: 14px;
  color: #606266;
}

.notebook-meta span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.notebook-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  align-items: start;
}

/* 地图容器 */
.map-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.map-header {
  padding: 20px 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.map-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.map-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.search-container {
  padding: 0 20px 20px;
  position: relative;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 20px;
  right: 20px;
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 100;
  max-height: 400px;
  overflow-y: auto;
  margin-top: 5px;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: 1px solid #f5f7fa;
  transition: background-color 0.2s;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background-color: #f5f7fa;
}

.result-icon {
  color: #70CDE5;
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 2px;
}

.result-address {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.map-wrapper {
  height: 600px;
  position: relative;
}

/* 侧边栏 */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
}

.destination-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.destination-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 15px;
  background-color: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #70CDE5;
}

.destination-index {
  width: 24px;
  height: 24px;
  background-color: #70CDE5;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
  flex-shrink: 0;
  margin-top: 2px;
}

.destination-info {
  flex: 1;
  min-width: 0;
}

.destination-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 5px;
}

.destination-address {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.destination-actions {
  display: flex;
  gap: 10px;
}

.destination-actions .el-button {
  padding: 2px 8px;
  font-size: 11px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
}

.empty-icon {
  color: #dcdfe6;
  margin-bottom: 15px;
}

.empty-state p {
  margin: 5px 0;
  font-size: 14px;
}

/* 路线信息 */
.route-info {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.route-summary {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.route-distance,
.route-duration {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.route-distance .label,
.route-duration .label {
  font-size: 14px;
  color: #606266;
}

.route-distance .value,
.route-duration .value {
  font-size: 16px;
  font-weight: 500;
  color: #70CDE5;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .sidebar {
    order: -1;
  }

  .map-wrapper {
    height: 500px;
  }
}

@media (max-width: 768px) {
  .trip-notebook-main {
    padding: 20px 15px;
  }

  .notebook-header {
    padding: 20px;
  }

  .notebook-title {
    font-size: 28px;
  }

  .notebook-meta {
    gap: 10px;
    font-size: 12px;
  }

  .map-wrapper {
    height: 400px;
  }

  .map-header {
    padding: 15px 15px 0;
  }

  .search-container {
    padding: 0 15px 15px;
  }

  .search-results {
    left: 15px;
    right: 15px;
  }
}

@media (max-width: 480px) {
  .notebook-title {
    font-size: 24px;
  }

  .notebook-header {
    flex-direction: column;
    align-items: stretch;
  }

  .notebook-actions {
    justify-content: stretch;
  }

  .notebook-actions .el-button {
    flex: 1;
  }

  .map-wrapper {
    height: 300px;
  }
}
</style>
