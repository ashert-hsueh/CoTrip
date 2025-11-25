<template>
  <div class="map-component">
    <div class="map-container" ref="mapContainer">
      <!-- 地图将通过JavaScript动态加载 -->
      <div v-if="loading" class="map-loading">
        <div class="loading-content">
          <el-icon size="48" class="loading-icon"><Loading /></el-icon>
          <p>地图加载中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { Loading } from '@element-plus/icons-vue';
import type { TransportationMode, Destination, Route } from '../types/trip';

interface Props {
  // 高德地图API密钥
  apiKey?: string;
  // 已有的目的地
  destinations?: Destination[];
  // 路线数据
  routes?: Route[];
  // 交通方式
  transportationMode?: TransportationMode;
}


const props = defineProps<Props>();
const emit = defineEmits<{
  // 地点选择事件
  'location-selected': [location: string, name?: string, address?: string];
  // 目的地添加事件
  'destination-added': [destination: Destination];
  // 路线更新事件
  'route-updated': [routes: Route[]];
}>();

const mapContainer = ref<HTMLDivElement | null>(null);
const loading = ref(true);

// 本地路线数据
const localRoutes = ref<Route[]>([]);

let map: any = null;
let markers: any[] = [];
let polyline: any = null;

// 加载高德地图
const loadAMapScript = () => {
  return new Promise<void>((resolve, reject) => {
    if (window.AMap) {
      resolve();
      return;
    }

    const apiKey = props.apiKey || import.meta.env.VITE_AMAP_KEY;
    if (!apiKey) {
      reject(new Error('请配置高德地图API密钥'));
      return;
    }

    const script = document.createElement('script');
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${apiKey}&plugin=AMap.Geocoder,AMap.Driving,AMap.Walking,AMap.Bicycling,AMap.Transfer,AMap.Scale,AMap.ToolBar`;
    script.type = 'text/javascript';
    script.onload = () => {
      resolve();
    };
    script.onerror = () => {
      reject(new Error('高德地图加载失败'));
    };
    document.head.appendChild(script);
  });
};

// 初始化地图
const initMap = async () => {
  try {
    await loadAMapScript();

    if (!mapContainer.value) return;

    // 创建地图实例
    map = new (window as any).AMap.Map(mapContainer.value, {
      resizeEnable: true,
      zoom: 11,
      center: [116.397428, 39.90923], // 默认北京
      mapStyle: 'amap://styles/light', // 浅色风格
      pitch: 0,
      rotation: 0
    });

    // 添加地图控件
    map.addControl(new (window as any).AMap.ToolBar({ position: 'RB' }));
    map.addControl(new (window as any).AMap.Scale({ position: 'RB' }));

    // 监听地图点击事件
    map.on('click', (e: any) => {
      const location = `${e.lnglat.lng},${e.lnglat.lat}`;
      emit('location-selected', location);
    });

    // 如果有初始目的地，添加标记
    if (props.destinations && props.destinations.length > 0) {
      props.destinations.forEach((dest) => {
        addMarker(dest);
      });
    }

    // 如果有初始路线，绘制路线
    if (props.routes && props.routes.length > 0) {
      localRoutes.value = [...props.routes];
      drawRoutes(props.routes);
    }

    loading.value = false;
  } catch (error) {
    console.error('地图初始化失败:', error);
    ElMessage.error('地图加载失败，请检查API配置');
    loading.value = false;
  }
};

// 添加标记
const addMarker = (place: Destination) => {
  const location = place.location;
  const [lon, lat] = location.split(',').map(Number);
  const name = place.name;

  const marker = new (window as any).AMap.Marker({
    position: [lon, lat],
    title: name,
    icon: new (window as any).AMap.Icon({
      size: new (window as any).AMap.Size(36, 48),
      image: 'https://webapi.amap.com/theme/v1.3/markers/n/place.png',
      imageSize: new (window as any).AMap.Size(36, 48),
      imageOffset: new (window as any).AMap.Pixel(-18, -48)
    }),
    anchor: 'bottom-center',
    map: map
  });

  // 添加点击事件
  marker.on('click', () => {
    map.setCenter([lon, lat]);
    map.setZoom(15);
  });

  // 添加信息窗口
  const infoWindow = new (window as any).AMap.InfoWindow({
    content: `<div style="padding: 12px;">
                <h4 style="margin: 0 0 8px 0; font-size: 16px;">${name}</h4>
                <p style="margin: 0; font-size: 12px; color: #666;">
                  ${place.address}
                </p>
              </div>`,
    offset: new (window as any).AMap.Pixel(0, -50)
  });

  marker.on('mouseover', () => {
    infoWindow.open(map, marker.getPosition());
  });

  marker.on('mouseout', () => {
    infoWindow.close();
  });

  markers.push(marker);
};

// 清除所有标记
const clearMarkers = () => {
  markers.forEach((marker) => {
    map.remove(marker);
  });
  markers = [];
};

// 清除路线
const clearRoute = () => {
  if (polyline) {
    map.remove(polyline);
    polyline = null;
  }
  localRoutes.value = [];
};


// 绘制单条路线
const drawRoute = (route: Route) => {
  if (!route.path) return;

  // 解析路线坐标
  const path = route.path.split(';').map((point: string) => {
    const [lon, lat] = point.split(',').map(Number);
    return [lon, lat];
  });

  // 根据交通方式设置不同的颜色
  const colorMap: Record<TransportationMode, string> = {
    driving: '#FFA939', // 橙色
    walking: '#70CDE5', // 蓝色
    bicycling: '#009CC6', // 深蓝色
    transit: '#52C41A' // 绿色
  };

  const color = colorMap[route.mode] || '#FFA939';

  const line = new (window as any).AMap.Polyline({
    path: path,
    strokeColor: color,
    strokeWeight: 6,
    strokeOpacity: 0.8,
    strokeStyle: 'solid',
    lineJoin: 'round',
    lineCap: 'round',
    zIndex: 50
  });

  map.add(line);
  return line;
};

// 绘制多条路线
const drawRoutes = (routes: Route[]) => {
  if (!routes || routes.length === 0) return;

  clearRoute();

  const lines: any[] = [];
  routes.forEach((route) => {
    const line = drawRoute(route);
    if (line) {
      lines.push(line);
    }
  });

  if (lines.length > 0) {
    // 调整地图视野以显示所有路线
    const bounds = new (window as any).AMap.Bounds();
    lines.forEach((line) => {
      bounds.extend(line.getPath());
    });
    map.setFitView(bounds, 50);
  }
};


// 组件挂载时初始化地图
onMounted(() => {
  initMap();
});

// 组件卸载时清理资源
onUnmounted(() => {
  if (map) {
    map.destroy();
  }
});

// 监听目的地变化
watch(
  () => props.destinations,
  (newDestinations) => {
    if (newDestinations && newDestinations.length > 0) {
      clearMarkers();
      newDestinations.forEach((dest) => {
        addMarker(dest);
      });

      // 如果有多个目的地，自动调整视野
      if (newDestinations.length > 0) {
        const bounds = new (window as any).AMap.Bounds();
        newDestinations.forEach((dest) => {
          const [lon, lat] = dest.location.split(',').map(Number);
          bounds.extend([lon, lat]);
        });
        map.setFitView(bounds, 50);
      }
    }
  },
  { deep: true }
);

// 监听路线变化
watch(
  () => props.routes,
  (newRoutes) => {
    if (newRoutes && newRoutes.length > 0) {
      localRoutes.value = [...newRoutes];
      drawRoutes(newRoutes);
    }
  },
  { deep: true }
);

// 组件挂载时初始化地图
onMounted(() => {
  initMap();
});

// 组件卸载时清理资源
onUnmounted(() => {
  if (map) {
    map.destroy();
  }
});
</script>

<style scoped>
.map-component {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  position: relative;
}

.map-container {
  flex: 1;
  position: relative;
  background-color: #f5f7fa;
  overflow: hidden;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.loading-content {
  text-align: center;
  color: #606266;
}

.loading-icon {
  color: #70CDE5;
  margin-bottom: 15px;
}

.loading-content p {
  margin: 0;
  font-size: 16px;
}

/* 地图控件样式调整 */
:deep(.amap-toolbar) {
  border: none !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}

:deep(.amap-scale) {
  bottom: 20px !important;
  right: 20px !important;
  background-color: rgba(255, 255, 255, 0.9) !important;
  border-radius: 4px !important;
  padding: 4px 8px !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

:deep(.amap-info-window) {
  border-radius: 8px !important;
  overflow: hidden !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

:deep(.amap-info-window-content) {
  padding: 0 !important;
}
</style>